"""Containment outcome metrics.

The Outline locks in:
  - primary: steady-state prevalence (SIS time-average post burn-in)
  - secondary: peak prevalence
  - tertiary: time-to-extinction (when applicable; SIR final-size or SIS first-zero step)

This module provides thin wrappers that convert simulation results into the
single-number metrics that downstream evaluation code uses to build Pareto
frontiers and ranking tables.
"""

from __future__ import annotations

import numpy as np

from ..sim.sir import SIRResult
from ..sim.sis import SISResult


def steady_state_prevalence(result: SISResult) -> float:
    """Primary outcome: SIS time-averaged post-burn-in prevalence."""
    return result.steady_state_prevalence


def peak_prevalence(result: SISResult | SIRResult) -> float:
    """Secondary outcome: max per-step prevalence observed."""
    return result.peak_prevalence


def time_to_extinction(result: SISResult) -> float | None:
    """Tertiary outcome: mean first-zero step (None if epidemic stayed endemic)."""
    return result.time_to_extinction


def final_epidemic_size(result: SIRResult) -> float:
    """SIR-only: fraction of nodes ever infected."""
    return result.final_epidemic_size


def auc_under_frontier(budget_fractions: np.ndarray, prevalence: np.ndarray) -> float:
    """Area under a Pareto curve. Lower is better.

    Used as a single-number summary per (campus, policy) for cross-campus
    ranking. We integrate via trapezoid over the budget fraction axis.
    """
    if budget_fractions.shape != prevalence.shape:
        raise ValueError("budget_fractions and prevalence must have the same shape")
    order = np.argsort(budget_fractions)
    return float(np.trapezoid(prevalence[order], budget_fractions[order]))
