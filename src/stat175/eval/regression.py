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
    """Univariate AUC ~ predictor fits, one per (policy, R0, predictor).

    With only 5 campuses a multivariate fit on 8 predictors is exactly
    determined and uninformative (R^2 = 1 by construction). Reporting the
    *univariate* slope and Pearson correlation per predictor gives a
    defensible qualitative direction ("policy AUC tends to rise with
    modularity") that the paper's discussion can lean on without
    overstating significance. n_observations = 5 throughout, so all
    inferences are explicitly small-sample.
    """
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
        campus_to_auc = dict(zip(group["campus"], group["auc"]))
        common_campuses = [c for c in campus_to_auc if c in stats_by_campus]
        if len(common_campuses) < 3:
            continue
        y = np.array([campus_to_auc[c] for c in common_campuses], dtype=float)
        for key in feature_keys:
            x = np.array(
                [getattr(stats_by_campus[c], key) for c in common_campuses], dtype=float
            )
            if np.allclose(x.std(), 0.0) or np.allclose(y.std(), 0.0):
                slope = float("nan")
                intercept = float("nan")
                pearson_r = float("nan")
                r2 = float("nan")
            else:
                model = LinearRegression()
                model.fit(x.reshape(-1, 1), y)
                slope = float(model.coef_[0])
                intercept = float(model.intercept_)
                r2 = float(model.score(x.reshape(-1, 1), y))
                pearson_r = float(np.corrcoef(x, y)[0, 1])
            rows.append(
                {
                    "policy": policy,
                    "R0": float(R0),
                    "predictor": key,
                    "slope": slope,
                    "intercept": intercept,
                    "pearson_r": pearson_r,
                    "R2": r2,
                    "n_observations": int(len(y)),
                }
            )
    return pd.DataFrame(rows)
