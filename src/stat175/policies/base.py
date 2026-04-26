"""Common Policy interface for edge-removal strategies.

A policy receives the residual graph (sparse adjacency), the per-edge cost
vector, the edge list (u, v) aligned with the cost vector, and a cost budget.
It returns the indices (into ``edges``) of the edges to remove.

Concrete policies live in sibling modules. They are deliberately stateless:
expensive precomputation belongs in helper functions or in a separate
training script (e.g. for the GNN policy).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np
import scipy.sparse as sp


@dataclass(frozen=True)
class PolicyInput:
    """Bundle of arguments shared by every policy."""

    adjacency: sp.csr_array
    edges: np.ndarray  # shape (m, 2)
    costs: np.ndarray  # shape (m,)
    budget: float
    seed: int = 42


class Policy(Protocol):
    """Selects an edge removal set within the given cost budget."""

    name: str

    def select(self, inputs: PolicyInput) -> np.ndarray:
        """Return the indices into ``inputs.edges`` of edges to remove."""
        ...


def greedy_fill_by_score(
    score: np.ndarray,
    costs: np.ndarray,
    budget: float,
) -> np.ndarray:
    """Pick edges in descending score order until the cost budget is exhausted.

    Returns a 1-D ndarray of edge indices (into the ``score``/``costs`` arrays).
    """
    if score.shape != costs.shape:
        raise ValueError("score and costs must have the same shape")
    if budget <= 0:
        return np.empty(0, dtype=np.int64)
    order = np.argsort(-score)
    cumulative_cost = np.cumsum(costs[order])
    fitting = order[cumulative_cost <= budget]
    return fitting.astype(np.int64)


def apply_removal(
    adjacency: sp.csr_array,
    edges: np.ndarray,
    removed_indices: np.ndarray,
) -> sp.csr_array:
    """Return a new symmetric CSR adjacency with the given edges removed."""
    if removed_indices.size == 0:
        return adjacency.copy()
    n = int(adjacency.shape[0])
    removed_pairs = edges[removed_indices]
    rows = np.concatenate([removed_pairs[:, 0], removed_pairs[:, 1]])
    cols = np.concatenate([removed_pairs[:, 1], removed_pairs[:, 0]])
    mask = sp.coo_array(
        (np.ones(rows.shape[0], dtype=np.int8), (rows, cols)),
        shape=(n, n),
    ).tocsr()
    residual = adjacency - mask
    residual.data = np.clip(residual.data, 0, 1)
    residual.eliminate_zeros()
    return residual.tocsr()
