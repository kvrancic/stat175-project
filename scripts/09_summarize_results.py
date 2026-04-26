#!/usr/bin/env python
"""Print and persist a clean numerical summary of the main Pareto results.

Outputs:
  - results/summary/main_pareto_summary.csv (per (campus, R0, policy):
    steady-state at each budget, AUC, AUC rank, prevalence reduction at 5%)
  - results/summary/headline_numbers.json (numbers the lightning-talk
    transcript and the paper's results section quote directly)

Idempotent: rerun whenever the underlying parquet is regenerated.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from stat175.viz.plots import auc_table  # noqa: E402

RESULTS_DIR = REPO_ROOT / "results"
SUMMARY_DIR = RESULTS_DIR / "summary"


def main() -> int:
    main_path = RESULTS_DIR / "main_pareto.parquet"
    if not main_path.exists():
        print(f"[err] {main_path} not found; run scripts/04_run_pareto.py first.", file=sys.stderr)
        return 1

    df = pd.read_parquet(main_path)
    SUMMARY_DIR.mkdir(parents=True, exist_ok=True)

    # Tidy per (campus, policy, R0, budget) summary.
    summary = (
        df.assign(
            steady_ci_width=df["steady_state_ci_high"] - df["steady_state_ci_low"],
        )
        .sort_values(["campus", "R0", "policy", "budget_fraction"])
        .reset_index(drop=True)
    )
    summary.to_csv(SUMMARY_DIR / "main_pareto_summary.csv", index=False)
    print(f"[saved] {SUMMARY_DIR / 'main_pareto_summary.csv'}")

    # AUC table + rank within each (campus, R0).
    auc = auc_table(df)
    auc["rank_in_campus_R0"] = (
        auc.groupby(["campus", "R0"])["auc"].rank(method="min").astype(int)
    )
    auc.to_csv(SUMMARY_DIR / "auc_by_policy_campus.csv", index=False)
    print(f"[saved] {SUMMARY_DIR / 'auc_by_policy_campus.csv'}")

    # Headline numbers for the lightning talk and the paper's results section.
    headline: dict = {}
    headline["per_R0_winner"] = {}
    for R0 in sorted(df["R0"].unique()):
        sub = auc[auc["R0"] == R0]
        wins = sub[sub["rank_in_campus_R0"] == 1]["policy"].value_counts().to_dict()
        headline["per_R0_winner"][float(R0)] = {
            policy: int(count) for policy, count in wins.items()
        }
    headline["budget_5pct_reduction"] = {}
    no_removal = df[df["budget_fraction"] == 0.0].set_index(
        ["campus", "R0", "policy"]
    )["steady_state_prevalence"]
    five_pct = df[np.isclose(df["budget_fraction"], 0.05)].set_index(
        ["campus", "R0", "policy"]
    )["steady_state_prevalence"]
    common = no_removal.index.intersection(five_pct.index)
    reduction = (no_removal[common] - five_pct[common]).reset_index(name="reduction")
    headline["budget_5pct_reduction"] = (
        reduction.groupby(["R0", "policy"])["reduction"].mean().reset_index().to_dict(orient="records")
    )

    headline_path = SUMMARY_DIR / "headline_numbers.json"
    headline_path.write_text(json.dumps(headline, indent=2, default=str))
    print(f"[saved] {headline_path}")

    print("\n=== Per-R0 winner counts (across 5 campuses) ===")
    for R0, counts in headline["per_R0_winner"].items():
        print(f"  R0={R0}: {counts}")

    print("\n=== Mean steady-state reduction at 5% budget (vs no removal) ===")
    reduction_pivot = reduction.pivot_table(
        index="policy", columns="R0", values="reduction", aggfunc="mean"
    )
    print(reduction_pivot.to_string(float_format=lambda x: f"{x:+.4f}"))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
