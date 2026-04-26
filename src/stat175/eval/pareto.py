"""Pareto evaluation harness.

Sweeps a policy across a grid of cost budgets, runs ``n_realizations``
stochastic SIS simulations on each residual graph, and returns a tidy
DataFrame with mean ± 95% bootstrap CIs for steady-state, peak, and
time-to-extinction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np
import pandas as pd
import scipy.sparse as sp

from ..policies.base import Policy, PolicyInput, apply_removal
from ..sim.sis import SISConfig, run_sis


@dataclass(frozen=True)
class ParetoSweep:
    campus: str
    policy_name: str
    R0: float
    gamma: float
    beta: float
    budget_fractions: Sequence[float]
    n_realizations: int
    n_steps: int
    burn_in: int
    n_seeds: int
    seed: int


def sweep_pareto(
    policy: Policy,
    adjacency: sp.csr_array,
    edges: np.ndarray,
    costs: np.ndarray,
    sweep: ParetoSweep,
) -> pd.DataFrame:
    total_cost = float(costs.sum())
    rows: list[dict] = []
    for budget_fraction in sweep.budget_fractions:
        budget = budget_fraction * total_cost
        inputs = PolicyInput(
            adjacency=adjacency,
            edges=edges,
            costs=costs,
            budget=budget,
            seed=sweep.seed,
        )
        if budget_fraction == 0.0:
            removed_indices = np.empty(0, dtype=np.int64)
        else:
            removed_indices = policy.select(inputs)

        residual = apply_removal(adjacency, edges, removed_indices)
        sis_config = SISConfig(
            beta=sweep.beta,
            gamma=sweep.gamma,
            n_steps=sweep.n_steps,
            burn_in=sweep.burn_in,
            n_seeds=sweep.n_seeds,
            n_realizations=sweep.n_realizations,
            seed=sweep.seed,
        )
        result = run_sis(residual, sis_config)
        ci_low, ci_high = result.steady_state_ci95
        rows.append(
            {
                "campus": sweep.campus,
                "policy": sweep.policy_name,
                "R0": sweep.R0,
                "gamma": sweep.gamma,
                "beta": sweep.beta,
                "budget_fraction": float(budget_fraction),
                "cost_used": float(costs[removed_indices].sum()) if removed_indices.size else 0.0,
                "n_edges_removed": int(removed_indices.size),
                "steady_state_prevalence": result.steady_state_prevalence,
                "steady_state_ci_low": ci_low,
                "steady_state_ci_high": ci_high,
                "peak_prevalence": result.peak_prevalence,
                "time_to_extinction": (
                    result.time_to_extinction if result.time_to_extinction is not None else float("nan")
                ),
                "lambda_residual": _spectral_radius_safe(residual),
                "n_realizations": sweep.n_realizations,
                "seed": sweep.seed,
            }
        )
    return pd.DataFrame(rows)


def _spectral_radius_safe(adjacency: sp.csr_array) -> float:
    """Return lambda_1(A) of the residual; 0 if the matrix is empty after removal."""
    if adjacency.nnz == 0:
        return 0.0
    from scipy.sparse.linalg import eigsh

    try:
        eigenvalues, _ = eigsh(adjacency.astype(np.float64), k=1, which="LA")
        return float(eigenvalues[0])
    except Exception:
        return float("nan")
