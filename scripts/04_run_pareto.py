#!/usr/bin/env python
"""Main Pareto experiment.

For each (campus, R0, policy, budget_fraction) cell run N stochastic SIS
simulations on the residual graph, persist all rows to a parquet file, and
emit the central frontier figure plus the cross-campus ranking heatmap.

The grid is read from the chosen experiment YAML; defaults (R0 grid,
budget grid, n_realizations, etc.) come from configs/default.yaml.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from scripts._cache_loader import load_cache  # noqa: E402

from stat175.data.facebook100 import CAMPUSES  # noqa: E402
from stat175.eval.pareto import ParetoSweep, sweep_pareto  # noqa: E402
from stat175.policies.base import Policy  # noqa: E402
from stat175.policies.betweenness import EdgeBetweennessOverCost  # noqa: E402
from stat175.policies.distance_threshold import DistanceThreshold  # noqa: E402
from stat175.policies.gnn_policy import GNNPolicy  # noqa: E402
from stat175.policies.random_baseline import RandomEdgeRemoval  # noqa: E402
from stat175.sim.sis import spectral_radius  # noqa: E402

RESULTS_DIR = REPO_ROOT / "results"


def merge_configs(config: dict, default: dict) -> dict:
    """Deep-merge `config` over `default`. Nested dicts are merged key-by-key."""
    merged = dict(default)
    for key, value in config.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = merge_configs(value, merged[key])
        else:
            merged[key] = value
    return merged


def load_yaml(path: Path) -> dict:
    with open(path) as fh:
        return yaml.safe_load(fh)


def build_policies(config: dict) -> dict[str, Policy]:
    """Construct all four policies (GNN encoders are loaded per-campus inside the run loop)."""
    return {
        "random": RandomEdgeRemoval(),
        "betweenness": EdgeBetweennessOverCost(betweenness_pivots=int(config.get("betweenness_pivots", 500))),
        "distance_threshold": DistanceThreshold(),
        # gnn is constructed per-campus from the loaded encoder
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "experiments" / "main_pareto.yaml")
    parser.add_argument("--out", type=Path, default=RESULTS_DIR / "main_pareto.parquet")
    parser.add_argument("--campuses", type=str, nargs="*", default=None)
    parser.add_argument("--policies", type=str, nargs="*", default=None)
    parser.add_argument("--cost", type=str, default=None, help="Override cost function")
    parser.add_argument("--R0-grid", type=float, nargs="*", default=None)
    parser.add_argument("--n-realizations", type=int, default=None)
    args = parser.parse_args()

    default_config = load_yaml(REPO_ROOT / "configs" / "default.yaml")
    if args.config.exists() and args.config != REPO_ROOT / "configs" / "default.yaml":
        experiment_config = load_yaml(args.config)
        config = merge_configs(experiment_config, default_config)
    else:
        config = default_config

    if args.cost is not None:
        config["cost_functions"] = {"primary": args.cost, "robustness": []}
    if args.R0_grid is not None:
        config["sis"]["R0_grid"] = args.R0_grid
    if args.n_realizations is not None:
        config["sis"]["n_realizations"] = args.n_realizations

    campuses = args.campuses if args.campuses else config["campuses"]
    policy_names = args.policies if args.policies else ["random", "betweenness", "distance_threshold", "gnn"]

    base_policies = build_policies(config)
    cost_fn_name = config["cost_functions"]["primary"]
    R0_grid = config["sis"]["R0_grid"]
    budget_fractions = config["budget_fractions"]
    gamma = float(config["sis"]["gamma"])
    n_realizations = int(config["sis"]["n_realizations"])
    n_steps = int(config["sis"]["n_steps"])
    burn_in = int(config["sis"]["burn_in"])
    n_seeds = int(config["sis"]["n_seeds"])
    seed = int(config["seed"])

    all_rows: list[pd.DataFrame] = []
    for campus_name in campuses:
        cache = load_cache(campus_name)
        adjacency = cache["adjacency"]
        features = cache["features"]
        edges = cache["edges"]
        if cost_fn_name == "sigmoid_dot":
            costs = cache["sigmoid_dot_costs"]
        else:
            from stat175.costs.edge_costs import compute_costs

            costs = compute_costs(cost_fn_name, features, edges)

        lam = spectral_radius(adjacency)
        print(f"[{campus_name}] n={adjacency.shape[0]}, m={edges.shape[0]}, lambda_1={lam:.2f}")

        # Build per-campus GNN policy by loading the trained encoder.
        policies: dict[str, Policy] = dict(base_policies)
        if "gnn" in policy_names:
            from scripts.train_gnn_helpers import load_encoder  # type: ignore[import-not-found]

            try:
                encoder = load_encoder(campus_name)
                policies["gnn"] = GNNPolicy(encoder, features, device="cpu")
            except FileNotFoundError as exc:
                print(f"  [warn] {exc}; skipping gnn for {campus_name}")
                policies.pop("gnn", None)

        for policy_name in policy_names:
            policy = policies.get(policy_name)
            if policy is None:
                continue
            for R0 in R0_grid:
                beta = R0 * gamma / lam
                sweep = ParetoSweep(
                    campus=campus_name,
                    policy_name=policy_name,
                    R0=float(R0),
                    gamma=gamma,
                    beta=beta,
                    budget_fractions=budget_fractions,
                    n_realizations=n_realizations,
                    n_steps=n_steps,
                    burn_in=burn_in,
                    n_seeds=n_seeds,
                    seed=seed,
                )
                start = time.time()
                df = sweep_pareto(policy, adjacency, edges, costs, sweep)
                elapsed = time.time() - start
                df["cost_function"] = cost_fn_name
                all_rows.append(df)
                print(
                    f"  {policy_name:18s} R0={R0:>4}: {elapsed:5.1f}s, "
                    f"steady@5%={df.loc[df['budget_fraction'] == 0.05, 'steady_state_prevalence'].mean():.3f}"
                )

    out_path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    combined = pd.concat(all_rows, ignore_index=True)
    combined.to_parquet(out_path, index=False)
    print(f"\n[saved] {out_path}  ({len(combined)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
