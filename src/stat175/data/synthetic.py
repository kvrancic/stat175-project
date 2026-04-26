"""Synthetic graph generators for the topology ablation (Milestone 5).

Generates ER, BA, WS, configuration-model, and SBM graphs sized to mimic an
average Facebook100 campus, returning sparse adjacencies + dummy node features
in the same shape as Facebook100 features so downstream code is uniform.
"""

from __future__ import annotations

import networkx as nx
import numpy as np
import scipy.sparse as sp

from .facebook100 import CampusData


def erdos_renyi(n: int, m: int, seed: int = 42) -> sp.csr_array:
    rng = np.random.default_rng(seed)
    p = (2 * m) / (n * (n - 1))
    graph = nx.fast_gnp_random_graph(n, p, seed=int(rng.integers(0, 2**31 - 1)))
    return _to_csr(graph)


def barabasi_albert(n: int, mean_degree: float, seed: int = 42) -> sp.csr_array:
    m_edges_per_step = max(1, int(round(mean_degree / 2)))
    graph = nx.barabasi_albert_graph(n, m_edges_per_step, seed=seed)
    return _to_csr(graph)


def watts_strogatz(n: int, mean_degree: float, p_rewire: float = 0.1, seed: int = 42) -> sp.csr_array:
    k = max(2, int(round(mean_degree)))
    if k % 2 == 1:
        k += 1
    graph = nx.watts_strogatz_graph(n, k, p_rewire, seed=seed)
    return _to_csr(graph)


def configuration_model(degree_sequence: np.ndarray, seed: int = 42) -> sp.csr_array:
    """Configuration model preserving the given degree sequence (parallel/self-edges removed)."""
    sequence = degree_sequence.astype(int).tolist()
    if sum(sequence) % 2 == 1:
        # Networkx requires an even-sum sequence; trim the smallest nonzero entry.
        nonzero = [i for i, value in enumerate(sequence) if value > 0]
        if nonzero:
            sequence[nonzero[0]] -= 1
    graph = nx.configuration_model(sequence, seed=seed)
    graph = nx.Graph(graph)  # collapse parallel edges
    graph.remove_edges_from(nx.selfloop_edges(graph))
    return _to_csr(graph)


def stochastic_block_model(
    block_sizes: list[int],
    p_within: float = 0.05,
    p_between: float = 0.005,
    seed: int = 42,
) -> sp.csr_array:
    n_blocks = len(block_sizes)
    probability_matrix = np.full((n_blocks, n_blocks), p_between)
    np.fill_diagonal(probability_matrix, p_within)
    graph = nx.stochastic_block_model(block_sizes, probability_matrix.tolist(), seed=seed)
    return _to_csr(graph)


def matched_to_campus(campus: CampusData, kind: str, seed: int = 42) -> sp.csr_array:
    """Build a synthetic graph matched in size/density to a real campus."""
    n = campus.n_nodes
    m = campus.n_edges
    mean_degree = (2 * m) / max(1, n)
    if kind == "er":
        return erdos_renyi(n, m, seed=seed)
    if kind == "ba":
        return barabasi_albert(n, mean_degree, seed=seed)
    if kind == "ws":
        return watts_strogatz(n, mean_degree, seed=seed)
    if kind == "config":
        degrees = np.asarray(campus.adjacency.sum(axis=1), dtype=int).ravel()
        return configuration_model(degrees, seed=seed)
    if kind == "sbm":
        # Coarse: split into 4 equal blocks calibrated to the campus density.
        block_size = n // 4
        block_sizes = [block_size, block_size, block_size, n - 3 * block_size]
        density = (2 * m) / (n * (n - 1)) if n > 1 else 0.0
        return stochastic_block_model(
            block_sizes,
            p_within=min(1.0, 5 * density),
            p_between=density / 5,
            seed=seed,
        )
    raise ValueError(f"unknown synthetic kind: {kind!r}")


def _to_csr(graph: nx.Graph) -> sp.csr_array:
    matrix = nx.to_scipy_sparse_array(graph, format="csr", dtype=np.int8, weight=None)
    matrix.setdiag(0)
    matrix.eliminate_zeros()
    return matrix
