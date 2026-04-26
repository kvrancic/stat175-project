"""Sanity checks on the SIS simulator."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from stat175.sim.sis import SISConfig, run_sis, spectral_radius  # noqa: E402


def _erdos_renyi(n: int, p: float, seed: int) -> sp.csr_array:
    rng = np.random.default_rng(seed)
    upper = (rng.random((n, n)) < p) & (np.triu(np.ones((n, n)), k=1).astype(bool))
    adjacency = upper | upper.T
    return sp.csr_array(adjacency.astype(np.int8))


def test_below_threshold_dies_out():
    """R0 < 1 should drive the SIS prevalence to ~0 in the long run."""
    adjacency = _erdos_renyi(200, p=0.05, seed=42)
    lam = spectral_radius(adjacency)
    config = SISConfig(beta=0.5 / lam * 0.10, gamma=0.10, n_steps=200, burn_in=100, n_realizations=10, seed=42)
    result = run_sis(adjacency, config)
    assert result.steady_state_prevalence < 0.01


def test_above_threshold_persists():
    """R0 > 1 should yield a persistent endemic plateau."""
    adjacency = _erdos_renyi(200, p=0.05, seed=42)
    lam = spectral_radius(adjacency)
    config = SISConfig(beta=3.0 / lam * 0.10, gamma=0.10, n_steps=300, burn_in=200, n_realizations=10, seed=42)
    result = run_sis(adjacency, config)
    assert result.steady_state_prevalence > 0.10


def test_steady_state_monotone_in_R0():
    """Higher R0 -> higher steady-state prevalence on the same graph."""
    adjacency = _erdos_renyi(150, p=0.06, seed=7)
    lam = spectral_radius(adjacency)
    gamma = 0.10
    prevalences = []
    for R0 in (1.5, 3.0, 6.0):
        config = SISConfig(
            beta=R0 / lam * gamma,
            gamma=gamma,
            n_steps=300,
            burn_in=200,
            n_realizations=15,
            seed=42,
        )
        prevalences.append(run_sis(adjacency, config).steady_state_prevalence)
    assert prevalences == sorted(prevalences)
