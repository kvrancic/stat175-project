"""Stochastic SIR simulator (robustness check for the SIS primary).

Per discrete time step:
- Each susceptible with k infected neighbors becomes infected w.p. 1 - (1 - beta)^k.
- Each infected becomes recovered (immune) with probability gamma.
- Recovered nodes never return to S.

Output focuses on final epidemic size (fraction ever infected) and peak
prevalence; steady-state is trivially zero in SIR so we omit it.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp


@dataclass(frozen=True)
class SIRConfig:
    beta: float
    gamma: float
    n_steps: int = 200
    n_seeds: int = 10
    n_realizations: int = 50
    seed: int = 42


@dataclass(frozen=True)
class SIRResult:
    per_step_prevalence_mean: np.ndarray  # currently infected fraction per step
    per_step_recovered_mean: np.ndarray  # cumulative recovered (= ever-infected once epidemic ends) per step
    final_epidemic_size: float  # fraction ever infected, mean across realizations
    final_epidemic_size_ci95: tuple[float, float]
    peak_prevalence: float


def run_sir(
    adjacency: sp.csr_array,
    config: SIRConfig,
    initial_infected: np.ndarray | None = None,
) -> SIRResult:
    n = int(adjacency.shape[0])
    rng = np.random.default_rng(config.seed)
    if not (0.0 <= config.beta < 1.0):
        raise ValueError(f"beta must be in [0, 1), got {config.beta}")
    log_one_minus_beta = np.log1p(-config.beta) if config.beta > 0 else 0.0

    per_step_inf = np.zeros((config.n_realizations, config.n_steps + 1))
    per_step_rec = np.zeros((config.n_realizations, config.n_steps + 1))
    final_sizes = np.zeros(config.n_realizations)

    for realization_index in range(config.n_realizations):
        if initial_infected is None:
            seeds = rng.choice(n, size=min(config.n_seeds, n), replace=False)
        else:
            seeds = np.asarray(initial_infected, dtype=np.int64)
        infected = np.zeros(n, dtype=bool)
        recovered = np.zeros(n, dtype=bool)
        infected[seeds] = True

        per_step_inf[realization_index, 0] = infected.mean()
        per_step_rec[realization_index, 0] = recovered.mean()

        for step_index in range(1, config.n_steps + 1):
            susceptible = ~(infected | recovered)
            infected_count = adjacency.astype(np.int32) @ infected.astype(np.int32)
            if log_one_minus_beta == 0.0:
                infect_probability = np.zeros_like(infected_count, dtype=np.float64)
            else:
                infect_probability = 1.0 - np.exp(log_one_minus_beta * infected_count)
            new_infections = susceptible & (rng.random(n) < infect_probability)
            recoveries = infected & (rng.random(n) < config.gamma)

            recovered = recovered | recoveries
            infected = (infected & ~recoveries) | new_infections

            per_step_inf[realization_index, step_index] = infected.mean()
            per_step_rec[realization_index, step_index] = recovered.mean()

            if not infected.any():
                # Once the epidemic dies out the rest of the trajectory is constant.
                per_step_inf[realization_index, step_index:] = 0.0
                per_step_rec[realization_index, step_index:] = recovered.mean()
                break

        final_sizes[realization_index] = float((infected | recovered).mean())

    mean_inf = per_step_inf.mean(axis=0)
    mean_rec = per_step_rec.mean(axis=0)
    final_mean = float(final_sizes.mean())
    if final_sizes.size > 1:
        boot_indices = rng.integers(0, final_sizes.size, size=(1000, final_sizes.size))
        boot_means = final_sizes[boot_indices].mean(axis=1)
        ci_low = float(np.quantile(boot_means, 0.025))
        ci_high = float(np.quantile(boot_means, 0.975))
    else:
        ci_low = ci_high = final_mean
    return SIRResult(
        per_step_prevalence_mean=mean_inf,
        per_step_recovered_mean=mean_rec,
        final_epidemic_size=final_mean,
        final_epidemic_size_ci95=(ci_low, ci_high),
        peak_prevalence=float(mean_inf.max()),
    )
