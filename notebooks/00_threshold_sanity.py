"""Threshold sanity check (run as a script).

Computes lambda_1(A) for each of the 5 campuses, then runs the SIS sim at
R0 in {0.8, 1.5, 3.0, 6.0} on each, and prints + persists the steady-state
prevalences. Validates that:
  - below R0 = 1 the epidemic dies out (steady state -> 0),
  - above R0 = 1 we get an endemic plateau, and
  - higher R0 yields higher steady-state prevalence.

Run from the repo root:
    uv run python notebooks/00_threshold_sanity.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from stat175.data.facebook100 import CAMPUSES, load_campus, summarize  # noqa: E402
from stat175.sim.sis import SISConfig, run_sis, spectral_radius  # noqa: E402

R0_GRID = (0.8, 1.5, 3.0, 6.0)
GAMMA = 0.10
N_REALIZATIONS = 20  # smaller for a quick sanity sweep
N_STEPS = 200
BURN_IN = 100


def main() -> int:
    rows: list[dict] = []
    for name in CAMPUSES:
        campus = load_campus(name)
        stats = summarize(campus)
        lam = spectral_radius(campus.adjacency)
        tau_c = 1.0 / lam
        print(f"\n== {name} ==")
        print(f"  n={stats['n_nodes']}, m={stats['n_edges']}, mean_deg={stats['mean_degree']:.2f}")
        print(f"  lambda_1(A) = {lam:.4f},  tau_c = 1/lambda = {tau_c:.6f}")

        for R0 in R0_GRID:
            beta = R0 * GAMMA / lam
            result = run_sis(
                campus.adjacency,
                SISConfig(
                    beta=beta,
                    gamma=GAMMA,
                    n_steps=N_STEPS,
                    burn_in=BURN_IN,
                    n_realizations=N_REALIZATIONS,
                    seed=42,
                ),
            )
            ci_low, ci_high = result.steady_state_ci95
            print(
                f"    R0={R0:>4}  beta={beta:.5f}  steady={result.steady_state_prevalence:.4f}"
                f"  CI=({ci_low:.3f}, {ci_high:.3f})  peak={result.peak_prevalence:.3f}"
            )
            rows.append(
                {
                    "campus": name,
                    "lambda_1": lam,
                    "tau_c": tau_c,
                    "R0": R0,
                    "beta": beta,
                    "gamma": GAMMA,
                    "steady_state": result.steady_state_prevalence,
                    "steady_state_ci_low": ci_low,
                    "steady_state_ci_high": ci_high,
                    "peak": result.peak_prevalence,
                }
            )

    out_dir = REPO_ROOT / "results" / "summary"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "threshold_sanity.json"
    out_path.write_text(json.dumps(rows, indent=2))
    print(f"\n[saved] {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
