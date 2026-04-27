#!/usr/bin/env python
"""Run the three robustness panels: compliance, SIR alternative, adversarial seeding.

Each writes its own parquet under results/.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from scripts._cache_loader import load_cache  # noqa: E402
from scripts.train_gnn_helpers import load_encoder  # noqa: E402

from stat175.data.facebook100 import CAMPUSES  # noqa: E402
from stat175.policies.base import PolicyInput, apply_removal  # noqa: E402
from stat175.policies.betweenness import EdgeBetweennessOverCost  # noqa: E402
from stat175.policies.distance_threshold import DistanceThreshold  # noqa: E402
from stat175.policies.gnn_policy import GNNPolicy  # noqa: E402
from stat175.policies.random_baseline import RandomEdgeRemoval  # noqa: E402
from stat175.sim.sir import SIRConfig, run_sir  # noqa: E402
from stat175.sim.sis import SISConfig, run_sis, spectral_radius  # noqa: E402

RESULTS_DIR = REPO_ROOT / "results"


def policies_for(campus_name: str, features) -> dict:
    base = {
        "random": RandomEdgeRemoval(),
        "betweenness": EdgeBetweennessOverCost(betweenness_pivots=500),
        "distance_threshold": DistanceThreshold(),
    }
    try:
        encoder = load_encoder(campus_name)
        base["gnn"] = GNNPolicy(encoder, features, device="cpu")
    except FileNotFoundError:
        pass
    return base


def compliance_panel(default_config: dict, panel_config: dict) -> pd.DataFrame:
    """Apply each policy at every budget, then random-flip a fraction of
    'removed' edges back in before running SIS to simulate non-compliance.
    """
    rows = []
    rng = np.random.default_rng(int(default_config["seed"]))
    for campus_name in default_config["campuses"]:
        cache = load_cache(campus_name)
        adjacency = cache["adjacency"]
        edges = cache["edges"]
        costs = cache["sigmoid_dot_costs"]
        features = cache["features"]
        lam = spectral_radius(adjacency)
        gamma = float(default_config["sis"]["gamma"])
        for compliance in panel_config["compliance_levels"]:
            for R0 in panel_config["sis"]["R0_grid"]:
                beta = R0 * gamma / lam
                for policy_name, policy in policies_for(campus_name, features).items():
                    for budget_fraction in panel_config["budget_fractions"]:
                        budget = budget_fraction * float(costs.sum())
                        inputs = PolicyInput(adjacency, edges, costs, budget, seed=int(default_config["seed"]))
                        if budget_fraction == 0.0:
                            removed = np.empty(0, dtype=np.int64)
                        else:
                            removed = policy.select(inputs)
                        if compliance < 1.0 and removed.size:
                            n_keep_removed = int(np.ceil(compliance * removed.size))
                            kept_indices = rng.choice(removed.size, size=n_keep_removed, replace=False)
                            removed = removed[kept_indices]
                        residual = apply_removal(adjacency, edges, removed)
                        sis_config = SISConfig(
                            beta=beta,
                            gamma=gamma,
                            n_steps=int(default_config["sis"]["n_steps"]),
                            burn_in=int(default_config["sis"]["burn_in"]),
                            n_seeds=int(default_config["sis"]["n_seeds"]),
                            n_realizations=int(panel_config["sis"]["n_realizations"]),
                            seed=int(default_config["seed"]),
                        )
                        result = run_sis(residual, sis_config)
                        rows.append(
                            {
                                "campus": campus_name,
                                "policy": policy_name,
                                "compliance": float(compliance),
                                "R0": float(R0),
                                "beta": beta,
                                "gamma": gamma,
                                "budget_fraction": float(budget_fraction),
                                "n_edges_effective_removed": int(removed.size),
                                "steady_state_prevalence": result.steady_state_prevalence,
                                "steady_state_ci_low": result.steady_state_ci95[0],
                                "steady_state_ci_high": result.steady_state_ci95[1],
                                "peak_prevalence": result.peak_prevalence,
                            }
                        )
                        print(
                            f"  {campus_name:12s} compliance={compliance:.2f} R0={R0:>4} "
                            f"{policy_name:18s} budget={budget_fraction:.2f}: steady={result.steady_state_prevalence:.3f}"
                        )
    return pd.DataFrame(rows)


def sir_panel(default_config: dict, panel_config: dict) -> pd.DataFrame:
    rows = []
    for campus_name in default_config["campuses"]:
        cache = load_cache(campus_name)
        adjacency = cache["adjacency"]
        edges = cache["edges"]
        costs = cache["sigmoid_dot_costs"]
        features = cache["features"]
        lam = spectral_radius(adjacency)
        gamma = float(panel_config["sir"]["gamma"]) if "gamma" in panel_config.get("sir", {}) else float(
            default_config["sir"]["gamma"]
        )
        for R0 in panel_config["sir"]["R0_grid"]:
            beta = R0 * gamma / lam
            for policy_name, policy in policies_for(campus_name, features).items():
                for budget_fraction in panel_config["budget_fractions"]:
                    budget = budget_fraction * float(costs.sum())
                    inputs = PolicyInput(adjacency, edges, costs, budget, seed=int(default_config["seed"]))
                    if budget_fraction == 0.0:
                        removed = np.empty(0, dtype=np.int64)
                    else:
                        removed = policy.select(inputs)
                    residual = apply_removal(adjacency, edges, removed)
                    sir_config = SIRConfig(
                        beta=beta,
                        gamma=gamma,
                        n_steps=int(default_config["sir"]["n_steps"]),
                        n_seeds=int(default_config["sir"]["n_seeds"]),
                        n_realizations=int(panel_config["sir"]["n_realizations"]),
                        seed=int(default_config["seed"]),
                    )
                    result = run_sir(residual, sir_config)
                    rows.append(
                        {
                            "campus": campus_name,
                            "policy": policy_name,
                            "R0": float(R0),
                            "beta": beta,
                            "gamma": gamma,
                            "model": "SIR",
                            "budget_fraction": float(budget_fraction),
                            # Use final_epidemic_size as the "steady_state_prevalence" column so
                            # downstream plotting code can reuse the same labels.
                            "steady_state_prevalence": result.final_epidemic_size,
                            "steady_state_ci_low": result.final_epidemic_size_ci95[0],
                            "steady_state_ci_high": result.final_epidemic_size_ci95[1],
                            "peak_prevalence": result.peak_prevalence,
                        }
                    )
                    print(
                        f"  {campus_name:12s} SIR R0={R0:>4} {policy_name:18s} "
                        f"budget={budget_fraction:.2f}: final={result.final_epidemic_size:.3f}"
                    )
    return pd.DataFrame(rows)


def adversarial_seed_panel(default_config: dict, panel_config: dict) -> pd.DataFrame:
    """Replace random initial-infected nodes with the top-eigenvector-component nodes."""
    rows = []
    for campus_name in default_config["campuses"]:
        cache = load_cache(campus_name)
        adjacency = cache["adjacency"]
        edges = cache["edges"]
        costs = cache["sigmoid_dot_costs"]
        features = cache["features"]
        lam = spectral_radius(adjacency)
        gamma = float(default_config["sis"]["gamma"])
        n_seeds = int(default_config["sis"]["n_seeds"])

        from scipy.sparse.linalg import eigsh

        _, eigenvectors = eigsh(adjacency.astype(np.float64), k=1, which="LA")
        adversarial_seeds = np.argsort(-np.abs(eigenvectors[:, 0]))[:n_seeds].astype(np.int64)

        for R0 in panel_config["sis"]["R0_grid"]:
            beta = R0 * gamma / lam
            for policy_name, policy in policies_for(campus_name, features).items():
                for budget_fraction in panel_config["budget_fractions"]:
                    budget = budget_fraction * float(costs.sum())
                    inputs = PolicyInput(adjacency, edges, costs, budget, seed=int(default_config["seed"]))
                    if budget_fraction == 0.0:
                        removed = np.empty(0, dtype=np.int64)
                    else:
                        removed = policy.select(inputs)
                    residual = apply_removal(adjacency, edges, removed)
                    sis_config = SISConfig(
                        beta=beta,
                        gamma=gamma,
                        n_steps=int(default_config["sis"]["n_steps"]),
                        burn_in=int(default_config["sis"]["burn_in"]),
                        n_seeds=n_seeds,
                        n_realizations=int(panel_config["sis"]["n_realizations"]),
                        seed=int(default_config["seed"]),
                    )
                    result = run_sis(residual, sis_config, initial_infected=adversarial_seeds)
                    rows.append(
                        {
                            "campus": campus_name,
                            "policy": policy_name,
                            "R0": float(R0),
                            "beta": beta,
                            "gamma": gamma,
                            "seeding": "adversarial_top_eigenvector",
                            "budget_fraction": float(budget_fraction),
                            "steady_state_prevalence": result.steady_state_prevalence,
                            "steady_state_ci_low": result.steady_state_ci95[0],
                            "steady_state_ci_high": result.steady_state_ci95[1],
                            "peak_prevalence": result.peak_prevalence,
                        }
                    )
                    print(
                        f"  {campus_name:12s} adv-seed R0={R0:>4} {policy_name:18s} "
                        f"budget={budget_fraction:.2f}: steady={result.steady_state_prevalence:.3f}"
                    )
    return pd.DataFrame(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--panel",
        type=str,
        default="all",
        choices=("all", "compliance", "sir", "adversarial"),
    )
    parser.add_argument("--force", action="store_true", help="Rerun even if the parquet exists")
    args = parser.parse_args()

    default_config = yaml.safe_load((REPO_ROOT / "configs" / "default.yaml").read_text())
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    def deep_merge(child: dict, parent: dict) -> dict:
        merged = dict(parent)
        for key, value in child.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = deep_merge(value, merged[key])
            else:
                merged[key] = value
        return merged

    def run_one(name: str, builder, config_path: Path, out_path: Path):
        cfg = yaml.safe_load(config_path.read_text())
        cfg = deep_merge(cfg, default_config)
        # Skip if a finished parquet exists and the user did not pass --force.
        if out_path.exists() and not getattr(args, "force", False):
            print(f"[skip] {out_path} already exists; pass --force to rerun")
            return
        df = builder(default_config, cfg)
        df.to_parquet(out_path, index=False)
        print(f"\n[saved] {out_path}  ({len(df)} rows)")

    if args.panel in ("all", "compliance"):
        run_one(
            "compliance",
            compliance_panel,
            REPO_ROOT / "configs" / "experiments" / "robustness_compliance.yaml",
            RESULTS_DIR / "robustness_compliance.parquet",
        )
    if args.panel in ("all", "sir"):
        run_one(
            "sir",
            sir_panel,
            REPO_ROOT / "configs" / "experiments" / "robustness_sir.yaml",
            RESULTS_DIR / "robustness_sir.parquet",
        )
    if args.panel in ("all", "adversarial"):
        run_one(
            "adversarial",
            adversarial_seed_panel,
            REPO_ROOT / "configs" / "experiments" / "robustness_adversarial_seed.yaml",
            RESULTS_DIR / "robustness_adversarial_seed.parquet",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
