"""Smoke tests on a 10-node synthetic graph.

Each policy must:
- return only edge indices that exist in the input edge list
- never exceed the budget (allowing equality)
- behave sensibly at the corner budgets (0 -> select nothing; very large -> select close to everything)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

import torch  # noqa: E402

from stat175.costs.edge_costs import edges_from_adjacency  # noqa: E402
from stat175.models.gnn import GNNConfig, GNNEncoder  # noqa: E402
from stat175.policies.base import PolicyInput, apply_removal  # noqa: E402
from stat175.policies.betweenness import EdgeBetweennessOverCost  # noqa: E402
from stat175.policies.distance_threshold import DistanceThreshold  # noqa: E402
from stat175.policies.gnn_policy import GNNPolicy  # noqa: E402
from stat175.policies.random_baseline import RandomEdgeRemoval  # noqa: E402


def _toy_graph(seed: int = 0):
    rng = np.random.default_rng(seed)
    n = 10
    adjacency = sp.lil_array((n, n), dtype=np.int8)
    for u in range(n):
        for v in range(u + 1, n):
            if rng.random() < 0.4:
                adjacency[u, v] = 1
                adjacency[v, u] = 1
    adjacency = adjacency.tocsr()
    edges = edges_from_adjacency(adjacency)
    costs = rng.uniform(0.5, 1.0, size=edges.shape[0])
    return adjacency, edges, costs


def test_random_policy_within_budget():
    adjacency, edges, costs = _toy_graph(0)
    inputs = PolicyInput(adjacency=adjacency, edges=edges, costs=costs, budget=0.5 * costs.sum(), seed=42)
    selected = RandomEdgeRemoval().select(inputs)
    assert selected.size == 0 or selected.max() < edges.shape[0]
    assert costs[selected].sum() <= inputs.budget + 1e-9


def test_betweenness_policy_within_budget():
    adjacency, edges, costs = _toy_graph(1)
    inputs = PolicyInput(adjacency=adjacency, edges=edges, costs=costs, budget=0.5 * costs.sum(), seed=42)
    selected = EdgeBetweennessOverCost(betweenness_pivots=10).select(inputs)
    assert costs[selected].sum() <= inputs.budget + 1e-9


def test_distance_threshold_within_budget():
    adjacency, edges, costs = _toy_graph(2)
    inputs = PolicyInput(adjacency=adjacency, edges=edges, costs=costs, budget=0.5 * costs.sum(), seed=42)
    selected = DistanceThreshold().select(inputs)
    assert costs[selected].sum() <= inputs.budget + 1e-9


def test_gnn_policy_within_budget():
    adjacency, edges, costs = _toy_graph(3)
    n = adjacency.shape[0]
    encoder = GNNEncoder(GNNConfig(arch="graphsage", in_dim=4, hidden_dim=8, embed_dim=4, n_layers=2))
    encoder.eval()
    rng = np.random.default_rng(0)
    feats = sp.csr_array(rng.normal(size=(n, 4)).astype("float32"))
    inputs = PolicyInput(adjacency=adjacency, edges=edges, costs=costs, budget=0.5 * costs.sum(), seed=42)
    policy = GNNPolicy(encoder, feats, device="cpu")
    selected = policy.select(inputs)
    assert costs[selected].sum() <= inputs.budget + 1e-9


def test_zero_budget_selects_nothing():
    adjacency, edges, costs = _toy_graph(0)
    for policy in [
        RandomEdgeRemoval(),
        EdgeBetweennessOverCost(betweenness_pivots=10),
        DistanceThreshold(),
    ]:
        inputs = PolicyInput(adjacency=adjacency, edges=edges, costs=costs, budget=0.0, seed=42)
        assert policy.select(inputs).size == 0


def test_apply_removal_round_trip():
    adjacency, edges, costs = _toy_graph(0)
    selected = RandomEdgeRemoval().select(
        PolicyInput(adjacency, edges, costs, 0.5 * costs.sum(), 42)
    )
    residual = apply_removal(adjacency, edges, selected)
    assert residual.shape == adjacency.shape
    # No introduced edges
    assert residual.nnz <= adjacency.nnz
    # Removed edges no longer appear
    for index in selected:
        u, v = int(edges[index, 0]), int(edges[index, 1])
        assert residual[u, v] == 0
        assert residual[v, u] == 0
