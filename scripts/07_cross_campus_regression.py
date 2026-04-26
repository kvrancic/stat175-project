#!/usr/bin/env python
"""Cross-campus regression of per-policy AUC on graph descriptive statistics.

Reads ``results/main_pareto.parquet``, computes structural stats per
campus, fits a linear regression of AUC against those stats per
(policy, R0), and writes ``results/cross_campus_regression.parquet``.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from scripts._cache_loader import load_cache  # noqa: E402

from stat175.eval.regression import compute_stats, fit_per_policy  # noqa: E402
from stat175.viz.plots import auc_table  # noqa: E402

RESULTS_DIR = REPO_ROOT / "results"


def main() -> int:
    main_path = RESULTS_DIR / "main_pareto.parquet"
    if not main_path.exists():
        print(f"[err] {main_path} not found; run scripts/04_run_pareto.py first.", file=sys.stderr)
        return 1
    df = pd.read_parquet(main_path)
    auc = auc_table(df)
    print(auc.head())

    stats_by_campus = {}
    for campus_name in sorted(df["campus"].unique()):
        cache = load_cache(campus_name)
        stats = compute_stats(cache["adjacency"], cache["attributes"])
        stats_by_campus[campus_name] = stats
        print(f"[stats] {campus_name}: {stats}")

    regression = fit_per_policy(auc, stats_by_campus)
    out_path = RESULTS_DIR / "cross_campus_regression.parquet"
    regression.to_parquet(out_path, index=False)
    print(f"\n[saved] {out_path}  ({len(regression)} coefficient rows)")

    stats_path = RESULTS_DIR / "campus_structural_stats.csv"
    pd.DataFrame.from_records(
        [{"campus": k, **v.__dict__} for k, v in stats_by_campus.items()]
    ).to_csv(stats_path, index=False)
    print(f"[saved] {stats_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
