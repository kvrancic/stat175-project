"""Edge cost functions.

Primary cost (per ``docs/Project Outline.txt``): ``c_e = sigmoid(<x_u, x_v>)``
on L2-normalized one-hot endpoint features. Variants are provided for the
robustness panel and for the ablation study.

All functions return a length-``m`` ndarray of nonnegative costs aligned with
the COO row order of the input adjacency.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp


def sigmoid_dot(features: sp.csr_array, edges: np.ndarray) -> np.ndarray:
    """sigmoid(<x_u, x_v>) — Outline's primary cost proxy."""
    inner = _edge_dot_product(features, edges)
    return _sigmoid(inner)


def cosine(features: sp.csr_array, edges: np.ndarray) -> np.ndarray:
    """Cosine similarity on already L2-normalized features. Bounded in [-1, 1]; rescaled to [0, 1]."""
    inner = _edge_dot_product(features, edges)
    return (inner + 1.0) / 2.0


def raw_dot(features: sp.csr_array, edges: np.ndarray) -> np.ndarray:
    """Raw dot product, clipped to be nonnegative for downstream divisions."""
    return np.clip(_edge_dot_product(features, edges), a_min=0.0, a_max=None)


def uniform(_: sp.csr_array, edges: np.ndarray) -> np.ndarray:
    """All edges equal cost — recovers the cardinality-minimization formulation."""
    return np.ones(edges.shape[0], dtype=np.float64)


def oracle_lognormal(_: sp.csr_array, edges: np.ndarray, seed: int = 42) -> np.ndarray:
    """Costs drawn i.i.d. from log-normal — robustness against feature-correlated cost."""
    rng = np.random.default_rng(seed)
    return rng.lognormal(mean=0.0, sigma=1.0, size=edges.shape[0])


def edges_from_adjacency(adjacency: sp.csr_array) -> np.ndarray:
    """Return an (m, 2) array of (u, v) pairs with u < v for an undirected graph."""
    upper = sp.triu(adjacency, k=1).tocoo()
    return np.column_stack([upper.row, upper.col]).astype(np.int64)


def _edge_dot_product(features: sp.csr_array, edges: np.ndarray) -> np.ndarray:
    """Compute <x_u, x_v> for every (u, v) row in ``edges``."""
    if features.shape[0] == 0:
        return np.zeros(edges.shape[0], dtype=np.float64)
    left = features[edges[:, 0]]
    right = features[edges[:, 1]]
    elementwise = left.multiply(right)
    return np.asarray(elementwise.sum(axis=1)).ravel().astype(np.float64)


def _sigmoid(values: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-values))


COST_FUNCTIONS: dict[str, object] = {
    "sigmoid_dot": sigmoid_dot,
    "cosine": cosine,
    "raw_dot": raw_dot,
    "uniform": uniform,
    "oracle_lognormal": oracle_lognormal,
}


def compute_costs(
    name: str,
    features: sp.csr_array,
    edges: np.ndarray,
    **kwargs,
) -> np.ndarray:
    """Dispatch to a registered cost function by string name."""
    if name not in COST_FUNCTIONS:
        raise KeyError(f"unknown cost function {name!r}; choose from {sorted(COST_FUNCTIONS)}")
    return COST_FUNCTIONS[name](features, edges, **kwargs)
