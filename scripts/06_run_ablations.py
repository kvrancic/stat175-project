#!/usr/bin/env python
"""Run the three ablation studies: GNN architecture, cost function, synthetic topology.

Each writes its own parquet under results/.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.sparse as sp
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from scripts._cache_loader import load_cache  # noqa: E402

from stat175.costs.edge_costs import compute_costs, edges_from_adjacency  # noqa: E402
from stat175.data.facebook100 import CAMPUSES  # noqa: E402
from stat175.data.synthetic import matched_to_campus  # noqa: E402
from stat175.eval.pareto import ParetoSweep, sweep_pareto  # noqa: E402
from stat175.models.gnn import GNNConfig  # noqa: E402
from stat175.models.training import TrainingConfig, train_link_prediction  # noqa: E402
from stat175.policies.betweenness import EdgeBetweennessOverCost  # noqa: E402
from stat175.policies.distance_threshold import DistanceThreshold  # noqa: E402
from stat175.policies.gnn_policy import GNNPolicy  # noqa: E402
from stat175.policies.random_baseline import RandomEdgeRemoval  # noqa: E402
from stat175.sim.sis import spectral_radius  # noqa: E402

RESULTS_DIR = REPO_ROOT / "results"


def gnn_arch_ablation(default_config: dict, ablation_config: dict) -> pd.DataFrame:
    rows = []
    archs = ablation_config["gnn"]["variants"]
    R0_grid = ablation_config["sis"]["R0_grid"]
    budget_fractions = ablation_config["budget_fractions"]
    n_realizations = int(ablation_config["sis"]["n_realizations"])
    gamma = float(default_config["sis"]["gamma"])
    seed = int(default_config["seed"])

    for campus_name in default_config["campuses"]:
        cache = load_cache(campus_name)
        adjacency = cache["adjacency"]
        edges = cache["edges"]
        costs = cache["sigmoid_dot_costs"]
        features = cache["features"]
        lam = spectral_radius(adjacency)

        for arch in archs:
            print(f"[arch-ablation] {campus_name} {arch}: training...")
            gnn_cfg = GNNConfig(
                arch=arch,
                in_dim=int(features.shape[1]),
                hidden_dim=int(default_config["gnn"]["hidden_dim"]),
                embed_dim=int(default_config["gnn"]["embed_dim"]),
                n_layers=int(default_config["gnn"]["n_layers"]),
                dropout=float(default_config["gnn"]["dropout"]),
            )
            training_cfg = TrainingConfig(
                epochs=int(default_config["gnn"]["epochs"]),
                lr=float(default_config["gnn"]["learning_rate"]),
                weight_decay=float(default_config["gnn"]["weight_decay"]),
                seed=seed,
            )
            start = time.time()
            res = train_link_prediction(adjacency, features, gnn_cfg, training_cfg)
            print(f"  trained in {time.time() - start:.1f}s; val AUROC={res.val_aurocs[-1]:.4f}")

            policy = GNNPolicy(res.encoder, features, device="cpu")
            for R0 in R0_grid:
                beta = R0 * gamma / lam
                sweep = ParetoSweep(
                    campus=campus_name,
                    policy_name=f"gnn_{arch}",
                    R0=float(R0),
                    gamma=gamma,
                    beta=beta,
                    budget_fractions=budget_fractions,
                    n_realizations=n_realizations,
                    n_steps=int(default_config["sis"]["n_steps"]),
                    burn_in=int(default_config["sis"]["burn_in"]),
                    n_seeds=int(default_config["sis"]["n_seeds"]),
                    seed=seed,
                )
                df = sweep_pareto(policy, adjacency, edges, costs, sweep)
                df["arch"] = arch
                rows.append(df)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def cost_function_ablation(default_config: dict, ablation_config: dict) -> pd.DataFrame:
    rows = []
    R0_grid = ablation_config["sis"]["R0_grid"]
    budget_fractions = ablation_config["budget_fractions"]
    n_realizations = int(ablation_config["sis"]["n_realizations"])
    gamma = float(default_config["sis"]["gamma"])
    seed = int(default_config["seed"])
    variants = ablation_config["cost_functions"]["variants"]

    from scripts.train_gnn_helpers import load_encoder  # noqa: E402

    for campus_name in default_config["campuses"]:
        cache = load_cache(campus_name)
        adjacency = cache["adjacency"]
        edges = cache["edges"]
        features = cache["features"]
        lam = spectral_radius(adjacency)
        try:
            encoder = load_encoder(campus_name)
            gnn_policy = GNNPolicy(encoder, features, device="cpu")
        except FileNotFoundError as exc:
            print(f"[skip] {exc}")
            gnn_policy = None

        for cost_name in variants:
            costs = compute_costs(cost_name, features, edges)
            policies = {
                "random": RandomEdgeRemoval(),
                "betweenness": EdgeBetweennessOverCost(betweenness_pivots=500),
                "distance_threshold": DistanceThreshold(),
            }
            if gnn_policy is not None:
                policies["gnn"] = gnn_policy

            for policy_name, policy in policies.items():
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
                        n_steps=int(default_config["sis"]["n_steps"]),
                        burn_in=int(default_config["sis"]["burn_in"]),
                        n_seeds=int(default_config["sis"]["n_seeds"]),
                        seed=seed,
                    )
                    df = sweep_pareto(policy, adjacency, edges, costs, sweep)
                    df["cost_function"] = cost_name
                    rows.append(df)
                    print(
                        f"  {campus_name:12s} cost={cost_name:18s} {policy_name:18s} R0={R0:>4} done"
                    )
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def synthetic_topology_ablation(default_config: dict, ablation_config: dict) -> pd.DataFrame:
    rows = []
    R0_grid = ablation_config["sis"]["R0_grid"]
    budget_fractions = ablation_config["budget_fractions"]
    n_realizations = int(ablation_config["sis"]["n_realizations"])
    gamma = float(default_config["sis"]["gamma"])
    seed = int(default_config["seed"])
    variants = ablation_config["synthetic"]["variants"]

    template = ablation_config["synthetic"]["template_campus"]
    cache = load_cache(template)
    template_campus_obj = type(
        "MockCampus",
        (),
        {
            "n_nodes": int(cache["adjacency"].shape[0]),
            "n_edges": int(sp.triu(cache["adjacency"], k=1).nnz),
            "adjacency": cache["adjacency"],
            "name": template,
        },
    )()

    for kind in variants:
        adjacency = matched_to_campus(template_campus_obj, kind, seed=seed)
        edges = edges_from_adjacency(adjacency)
        n = adjacency.shape[0]
        # Synthetic graphs have no real features; use random one-hot of node IDs
        # as a degenerate feature matrix that supports the cost code without
        # introducing leakage.
        identity_feats = sp.eye_array(n, format="csr").astype("float32")
        # Cost: use sigmoid(<x, x>) with random degree-binned vectors as a stable proxy.
        rng = np.random.default_rng(seed)
        features = sp.csr_array(rng.normal(size=(n, 16)).astype("float32"))
        costs = compute_costs("sigmoid_dot", features, edges)

        lam = spectral_radius(adjacency)
        policies = {
            "random": RandomEdgeRemoval(),
            "betweenness": EdgeBetweennessOverCost(betweenness_pivots=300),
            "distance_threshold": DistanceThreshold(),
        }
        for policy_name, policy in policies.items():
            for R0 in R0_grid:
                beta = R0 * gamma / lam
                sweep = ParetoSweep(
                    campus=f"synth_{kind}",
                    policy_name=policy_name,
                    R0=float(R0),
                    gamma=gamma,
                    beta=beta,
                    budget_fractions=budget_fractions,
                    n_realizations=n_realizations,
                    n_steps=int(default_config["sis"]["n_steps"]),
                    burn_in=int(default_config["sis"]["burn_in"]),
                    n_seeds=int(default_config["sis"]["n_seeds"]),
                    seed=seed,
                )
                df = sweep_pareto(policy, adjacency, edges, costs, sweep)
                df["topology"] = kind
                rows.append(df)
                print(f"  synth-{kind} {policy_name:18s} R0={R0:>4} done")
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--ablation",
        type=str,
        default="all",
        choices=("all", "gnn_arch", "cost_function", "synthetic_topology"),
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
        if out_path.exists() and not getattr(args, "force", False):
            print(f"[skip] {out_path} already exists; pass --force to rerun")
            return
        df = builder(default_config, cfg)
        df.to_parquet(out_path, index=False)
        print(f"\n[saved] {out_path}  ({len(df)} rows)")

    if args.ablation in ("all", "gnn_arch"):
        run_one(
            "gnn_arch",
            gnn_arch_ablation,
            REPO_ROOT / "configs" / "experiments" / "ablation_gnn_arch.yaml",
            RESULTS_DIR / "ablation_gnn_arch.parquet",
        )
    if args.ablation in ("all", "cost_function"):
        run_one(
            "cost_function",
            cost_function_ablation,
            REPO_ROOT / "configs" / "experiments" / "ablation_cost_function.yaml",
            RESULTS_DIR / "ablation_cost_function.parquet",
        )
    if args.ablation in ("all", "synthetic_topology"):
        run_one(
            "synthetic_topology",
            synthetic_topology_ablation,
            REPO_ROOT / "configs" / "experiments" / "ablation_synthetic_topology.yaml",
            RESULTS_DIR / "ablation_synthetic_topology.parquet",
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
