"""Edge betweenness centrality / cost — Outline policy 2.

Ranks each edge by its (approximate) betweenness centrality divided by its
cost, then greedy-fills until the cost budget is exhausted.

For Penn94 / Tennessee95 / Harvard1 exact betweenness on the full edge set is
prohibitive (O(VE) ~ 10^10), so we use NetworkX's pivot-sampled estimator
with `k` source pivots controlled by ``betweenness_pivots`` in the policy
constructor (default 500, matching configs/default.yaml).
"""

from __future__ import annotations

import networkx as nx
import numpy as np

from .base import Policy, PolicyInput, greedy_fill_by_score


class EdgeBetweennessOverCost:
    name = "betweenness"

    def __init__(self, betweenness_pivots: int = 500):
        self.betweenness_pivots = betweenness_pivots
        self._cached_scores: np.ndarray | None = None
        self._cached_adjacency_id: int | None = None

    def select(self, inputs: PolicyInput) -> np.ndarray:
        adjacency_id = id(inputs.adjacency)
        if self._cached_scores is not None and self._cached_adjacency_id == adjacency_id:
            scores = self._cached_scores
        else:
            graph = nx.from_scipy_sparse_array(inputs.adjacency)
            n = graph.number_of_nodes()
            k = None if self.betweenness_pivots >= n else int(self.betweenness_pivots)
            seed = int(inputs.seed)
            if k is None:
                betweenness = nx.edge_betweenness_centrality(graph, normalized=False, seed=seed)
            else:
                betweenness = nx.edge_betweenness_centrality(graph, k=k, normalized=False, seed=seed)

            scores = np.zeros(inputs.edges.shape[0], dtype=np.float64)
            for index, (u, v) in enumerate(inputs.edges):
                edge_key = (int(u), int(v)) if (int(u), int(v)) in betweenness else (int(v), int(u))
                scores[index] = betweenness.get(edge_key, 0.0)
            self._cached_scores = scores
            self._cached_adjacency_id = adjacency_id

        # Bang-for-buck: betweenness divided by cost, with a small floor on the cost
        # so that an oracle-zero-cost edge does not dominate purely on the divisor.
        score = scores / np.clip(inputs.costs, 1e-6, None)
        return greedy_fill_by_score(score, inputs.costs, inputs.budget)


_: Policy = EdgeBetweennessOverCost()
