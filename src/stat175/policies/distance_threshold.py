"""Distance Threshold — Outline policy 4 (the implementable, realistic policy).

The Outline lists this as "within X distance = remove". We implement it as a
community-bubble cut, which is the natural finite-graph analog of "stay
within your bubble":

  1. Run Louvain on the residual adjacency to obtain communities.
  2. Build a meta-graph whose nodes are communities; meta-edges connect
     communities that share at least one inter-community edge.
  3. For each edge (u, v) with community labels c_u != c_v, compute the
     shortest-path hop distance d(c_u, c_v) in the meta-graph.
  4. Cut every edge whose meta-distance exceeds X. Sweep X to express the
     cost-budget axis: starting from the largest meta-distance and stepping
     down until the cumulative cost of cuts hits the budget.

This is "remove edges to nodes more than X bubbles away" — directly
implementable as a public-health rule and the realistic counterpoint to
the GNN ideal policy, per CENTRAL-KNOWLEDGE.md §X.
"""

from __future__ import annotations

import community as community_louvain
import networkx as nx
import numpy as np

from .base import Policy, PolicyInput, greedy_fill_by_score


class DistanceThreshold:
    name = "distance_threshold"

    def __init__(self, resolution: float = 1.0):
        self.resolution = resolution

    def select(self, inputs: PolicyInput) -> np.ndarray:
        graph = nx.from_scipy_sparse_array(inputs.adjacency)
        partition = community_louvain.best_partition(
            graph,
            random_state=int(inputs.seed),
            resolution=self.resolution,
        )

        n_edges = inputs.edges.shape[0]
        community_of_node = np.zeros(graph.number_of_nodes(), dtype=np.int64)
        for node, community_id in partition.items():
            community_of_node[node] = community_id

        # Build the community meta-graph (nodes = communities, edges = shared inter-community edges).
        meta_graph = nx.Graph()
        for community_id in set(partition.values()):
            meta_graph.add_node(community_id)
        for u, v in inputs.edges:
            cu = int(community_of_node[u])
            cv = int(community_of_node[v])
            if cu != cv and not meta_graph.has_edge(cu, cv):
                meta_graph.add_edge(cu, cv)

        # All-pairs shortest path on the meta-graph (small).
        path_lengths = dict(nx.all_pairs_shortest_path_length(meta_graph))

        # Within-community distance is 0; between-community distance is the meta-graph hop count.
        meta_distances = np.zeros(n_edges, dtype=np.float64)
        for index in range(n_edges):
            u = int(inputs.edges[index, 0])
            v = int(inputs.edges[index, 1])
            cu = int(community_of_node[u])
            cv = int(community_of_node[v])
            if cu == cv:
                meta_distances[index] = 0.0
            else:
                meta_distances[index] = float(path_lengths.get(cu, {}).get(cv, len(meta_graph)))

        # Score so highest score = furthest distance per unit cost. Greedy fill until budget.
        score = meta_distances / np.clip(inputs.costs, 1e-6, None)
        return greedy_fill_by_score(score, inputs.costs, inputs.budget)


_: Policy = DistanceThreshold()
