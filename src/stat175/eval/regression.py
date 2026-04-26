"""Cross-campus structural regression of policy AUC on graph statistics.

For each (policy, R0) pair, fit a linear regression of the policy's
Pareto-AUC against descriptive statistics of the campus (clustering
coefficient, degree assortativity, modularity, average path length,
homophily indices on each Facebook100 attribute).

This is the move that brings the ORIGINAL "which segregation metric
matters" descriptive question back into the project at the discussion
level (per CENTRAL-KNOWLEDGE.md sec XIII.4).
"""

from __future__ import annotations

from dataclasses import dataclass

import community as community_louvain
import networkx as nx
import numpy as np
import pandas as pd
import scipy.sparse as sp
from sklearn.linear_model import LinearRegression


@dataclass(frozen=True)
class StructuralStats:
    n_nodes: int
    n_edges: int
    density: float
    mean_degree: float
    degree_variance: float
    clustering_coef: float
    assortativity: float
    modularity: float
    homophily_dorm: float
    homophily_year: float


def compute_stats(adjacency: sp.csr_array, attributes: np.ndarray) -> StructuralStats:
    """Compute the descriptive statistics used as regression predictors."""
    graph = nx.from_scipy_sparse_array(adjacency)
    n = graph.number_of_nodes()
    m = graph.number_of_edges()
    degrees = np.array([graph.degree(node) for node in graph.nodes])
    density = (2 * m) / (n * (n - 1)) if n > 1 else 0.0

    clustering = nx.transitivity(graph)
    try:
        assortativity = nx.degree_assortativity_coefficient(graph)
    except Exception:
        assortativity = float("nan")

    partition = community_louvain.best_partition(graph, random_state=42)
    modularity = community_louvain.modularity(partition, graph)

    homophily_dorm = _homophily(graph, attributes[:, 4])  # dorm column
    homophily_year = _homophily(graph, attributes[:, 5])  # year column

    return StructuralStats(
        n_nodes=int(n),
        n_edges=int(m),
        density=float(density),
        mean_degree=float(degrees.mean()),
        degree_variance=float(degrees.var()),
        clustering_coef=float(clustering),
        assortativity=float(assortativity),
        modularity=float(modularity),
        homophily_dorm=homophily_dorm,
        homophily_year=homophily_year,
    )


def _homophily(graph: nx.Graph, labels: np.ndarray) -> float:
    """Fraction of edges whose endpoints share the same nonzero label.

    Edges where either endpoint has a missing (0) label are ignored.
    """
    n_total = 0
    n_match = 0
    for u, v in graph.edges:
        l_u = int(labels[u])
        l_v = int(labels[v])
        if l_u == 0 or l_v == 0:
            continue
        n_total += 1
        if l_u == l_v:
            n_match += 1
    return float(n_match / n_total) if n_total > 0 else float("nan")


def fit_per_policy(
    auc_table: pd.DataFrame,
    stats_by_campus: dict[str, StructuralStats],
) -> pd.DataFrame:
    """Linear regression of AUC ~ structural stats, one fit per (policy, R0)."""
    feature_keys = (
        "n_nodes",
        "density",
        "mean_degree",
        "clustering_coef",
        "assortativity",
        "modularity",
        "homophily_dorm",
        "homophily_year",
    )
    rows = []
    for (policy, R0), group in auc_table.groupby(["policy", "R0"]):
        x_rows = []
        y_rows = []
        for _, record in group.iterrows():
            stats = stats_by_campus.get(record["campus"])
            if stats is None:
                continue
            x_rows.append([getattr(stats, key) for key in feature_keys])
            y_rows.append(record["auc"])
        if len(x_rows) < 3:
            continue
        x = np.asarray(x_rows)
        y = np.asarray(y_rows)
        model = LinearRegression()
        model.fit(x, y)
        for key, coefficient in zip(feature_keys, model.coef_):
            rows.append(
                {
                    "policy": policy,
                    "R0": float(R0),
                    "predictor": key,
                    "coefficient": float(coefficient),
                    "intercept": float(model.intercept_),
                    "R2": float(model.score(x, y)),
                    "n_observations": int(len(y_rows)),
                }
            )
    return pd.DataFrame(rows)
