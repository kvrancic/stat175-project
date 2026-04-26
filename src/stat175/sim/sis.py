"""Stochastic SIS simulator on a sparse adjacency matrix.

Per discrete time step:
- Each infected node recovers (I -> S) with probability gamma.
- Each susceptible node with k infected neighbors becomes infected
  with probability 1 - (1 - beta) ** k.

Outputs:
- ``per_step_prevalence``: fraction of infected nodes at every step.
- ``steady_state_prevalence``: time-averaged prevalence over the post-burn-in window.
- ``peak_prevalence``: max per-step prevalence observed.
- ``time_to_extinction``: first step where the infected count hits zero, or None.

The implementation is fully vectorized over NumPy and operates on a
``scipy.sparse.csr_array`` adjacency. Multiple independent epidemic
realizations on the same residual graph can be run in a single call by
batching the initial seed sets.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp


@dataclass(frozen=True)
class SISConfig:
    """Parameters for a stochastic SIS simulation.

    Parameters
    ----------
    beta
        Per-edge per-step transmission probability.
    gamma
        Per-step recovery probability.
    n_steps
        Total number of discrete time steps to simulate.
    burn_in
        Number of initial steps excluded when averaging steady-state prevalence.
    n_seeds
        Number of initially infected nodes per realization.
    n_realizations
        Number of independent stochastic realizations to average.
    seed
        Master random seed.
    """

    beta: float
    gamma: float
    n_steps: int = 200
    burn_in: int = 100
    n_seeds: int = 10
    n_realizations: int = 50
    seed: int = 42


@dataclass(frozen=True)
class SISResult:
    """Mean simulation outcomes across realizations on a single graph."""

    per_step_prevalence_mean: np.ndarray  # shape (n_steps + 1,)
    per_step_prevalence_std: np.ndarray  # shape (n_steps + 1,)
    steady_state_prevalence: float  # time-average over post-burn-in window, then averaged across realizations
    steady_state_ci95: tuple[float, float]
    peak_prevalence: float
    time_to_extinction: float | None  # mean first-zero step across realizations; None if any realization stays endemic


def run_sis(
    adjacency: sp.csr_array,
    config: SISConfig,
    initial_infected: np.ndarray | None = None,
) -> SISResult:
    """Run ``config.n_realizations`` independent SIS simulations and aggregate."""
    n = int(adjacency.shape[0])
    if n == 0:
        raise ValueError("adjacency must be non-empty")

    rng = np.random.default_rng(config.seed)

    # Pre-compute log(1 - beta) once so the per-step probability calculation
    # reduces to elementwise log/exp on integer neighbor counts.
    if not (0.0 <= config.beta < 1.0):
        raise ValueError(f"beta must be in [0, 1), got {config.beta}")
    log_one_minus_beta = np.log1p(-config.beta) if config.beta > 0 else 0.0

    # Cast adjacency to float32 once; matvec is the per-step bottleneck.
    adjacency_float = adjacency.astype(np.float32)

    per_step = np.zeros((config.n_realizations, config.n_steps + 1), dtype=np.float64)
    extinction_steps: list[int | None] = []

    for realization_index in range(config.n_realizations):
        if initial_infected is None:
            seeds = rng.choice(n, size=min(config.n_seeds, n), replace=False)
        else:
            seeds = np.asarray(initial_infected, dtype=np.int64)
        infected = np.zeros(n, dtype=bool)
        infected[seeds] = True

        per_step[realization_index, 0] = infected.mean()
        first_zero: int | None = None

        for step_index in range(1, config.n_steps + 1):
            infected = _sis_step(
                adjacency=adjacency_float,
                infected=infected,
                gamma=config.gamma,
                log_one_minus_beta=log_one_minus_beta,
                rng=rng,
            )
            prevalence = infected.mean()
            per_step[realization_index, step_index] = prevalence
            if first_zero is None and prevalence == 0.0:
                first_zero = step_index

        extinction_steps.append(first_zero)

    mean_curve = per_step.mean(axis=0)
    std_curve = per_step.std(axis=0, ddof=1) if config.n_realizations > 1 else np.zeros_like(mean_curve)

    burn_in = min(config.burn_in, config.n_steps - 1)
    post_burn = per_step[:, burn_in:]
    per_realization_steady = post_burn.mean(axis=1)
    steady_state = float(per_realization_steady.mean())
    ci_low, ci_high = _bootstrap_ci(per_realization_steady, rng=rng)

    if any(step is None for step in extinction_steps):
        time_to_extinction: float | None = None
    else:
        time_to_extinction = float(np.mean(extinction_steps))

    return SISResult(
        per_step_prevalence_mean=mean_curve,
        per_step_prevalence_std=std_curve,
        steady_state_prevalence=steady_state,
        steady_state_ci95=(ci_low, ci_high),
        peak_prevalence=float(mean_curve.max()),
        time_to_extinction=time_to_extinction,
    )


def _sis_step(
    adjacency: sp.csr_array,
    infected: np.ndarray,
    gamma: float,
    log_one_minus_beta: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """Advance the SIS state vector by one stochastic step."""
    susceptible = ~infected

    # Number of infected neighbors per node = A @ infected.
    infected_count = adjacency @ infected.astype(np.float32)

    # P(susceptible -> infected) = 1 - (1 - beta) ^ k
    if log_one_minus_beta == 0.0:
        infect_probability = np.zeros_like(infected_count, dtype=np.float64)
    else:
        infect_probability = 1.0 - np.exp(log_one_minus_beta * infected_count)
    new_infections = susceptible & (rng.random(size=adjacency.shape[0]) < infect_probability)

    if gamma > 0.0:
        recoveries = infected & (rng.random(size=adjacency.shape[0]) < gamma)
    else:
        recoveries = np.zeros_like(infected)

    next_state = (infected & ~recoveries) | new_infections
    return next_state


def _bootstrap_ci(
    samples: np.ndarray,
    rng: np.random.Generator,
    n_resamples: int = 1000,
    confidence: float = 0.95,
) -> tuple[float, float]:
    """Percentile bootstrap CI for the mean of ``samples``."""
    if samples.size == 0:
        return (0.0, 0.0)
    if samples.size == 1:
        value = float(samples[0])
        return (value, value)
    indices = rng.integers(0, samples.size, size=(n_resamples, samples.size))
    means = samples[indices].mean(axis=1)
    alpha = (1.0 - confidence) / 2.0
    return (float(np.quantile(means, alpha)), float(np.quantile(means, 1 - alpha)))


def spectral_radius(adjacency: sp.csr_array) -> float:
    """Leading eigenvalue lambda_1(A); the SIS epidemic threshold is 1 / lambda_1."""
    from scipy.sparse.linalg import eigsh

    matrix = adjacency.astype(np.float64)
    eigenvalues, _ = eigsh(matrix, k=1, which="LA")
    return float(eigenvalues[0])
