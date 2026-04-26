#!/usr/bin/env python
"""Regenerate every paper figure from the parquet result tables.

Inputs are the parquet files produced by scripts/04..07. Outputs go
into paper/figures/, overwriting whatever was there.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from stat175.viz.plots import auc_table, pareto_frontier, ranking_heatmap  # noqa: E402

RESULTS_DIR = REPO_ROOT / "results"
FIGURES_DIR = REPO_ROOT / "paper" / "figures"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--main", type=Path, default=RESULTS_DIR / "main_pareto.parquet")
    parser.add_argument(
        "--robustness",
        type=Path,
        nargs="*",
        default=[
            RESULTS_DIR / "robustness_compliance.parquet",
            RESULTS_DIR / "robustness_sir.parquet",
            RESULTS_DIR / "robustness_adversarial_seed.parquet",
        ],
    )
    parser.add_argument(
        "--ablations",
        type=Path,
        nargs="*",
        default=[
            RESULTS_DIR / "ablation_gnn_arch.parquet",
            RESULTS_DIR / "ablation_cost_function.parquet",
            RESULTS_DIR / "ablation_synthetic_topology.parquet",
        ],
    )
    args = parser.parse_args()

    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    main_path = args.main
    if not main_path.exists():
        print(f"[err] {main_path} not found; run scripts/04_run_pareto.py first.", file=sys.stderr)
        return 1
    df = pd.read_parquet(main_path)

    # One Pareto-frontier figure per R0.
    for R0 in sorted(df["R0"].unique()):
        out = FIGURES_DIR / f"main_pareto_R0_{R0:.1f}.png"
        figure = pareto_frontier(df, R0=float(R0), output_path=out)
        figure.clf()
        print(f"[fig] {out}")

    # Ranking heatmap (across all R0s, AUC-based rank within each campus).
    for R0 in sorted(df["R0"].unique()):
        out = FIGURES_DIR / f"main_ranking_R0_{R0:.1f}.png"
        figure = ranking_heatmap(df, R0=float(R0), output_path=out)
        figure.clf()
        print(f"[fig] {out}")

    # AUC table (CSV alongside the figures so the paper can quote numbers).
    auc_df = auc_table(df)
    auc_csv = FIGURES_DIR / "main_auc_table.csv"
    auc_df.to_csv(auc_csv, index=False)
    print(f"[csv] {auc_csv}")

    # Robustness / ablation panels (best-effort: only render those that exist).
    for path in args.robustness:
        if not path.exists():
            print(f"[skip] {path} not found")
            continue
        rdf = pd.read_parquet(path)
        for R0 in sorted(rdf["R0"].unique()):
            out = FIGURES_DIR / f"{path.stem}_R0_{R0:.1f}.png"
            figure = pareto_frontier(rdf, R0=float(R0), output_path=out)
            figure.clf()
            print(f"[fig] {out}")

    for path in args.ablations:
        if not path.exists():
            print(f"[skip] {path} not found")
            continue
        rdf = pd.read_parquet(path)
        for R0 in sorted(rdf["R0"].unique()):
            out = FIGURES_DIR / f"{path.stem}_R0_{R0:.1f}.png"
            figure = pareto_frontier(rdf, R0=float(R0), output_path=out)
            figure.clf()
            print(f"[fig] {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
