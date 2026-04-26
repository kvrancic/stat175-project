"""Facebook100 loader.

Each `.mat` file contains a sparse adjacency `A` and a `local_info` matrix
with one row per node and columns:
  0: student/faculty status flag
  1: gender
  2: major
  3: second major / minor
  4: dorm / house
  5: year
  6: high school
Missing data is coded 0 (per facebook100_readme_021011.txt).

We restrict to the giant connected component before downstream use.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import networkx as nx
import numpy as np
import scipy.io
import scipy.sparse as sp

ATTRIBUTE_NAMES: tuple[str, ...] = (
    "status",
    "gender",
    "major",
    "second_major",
    "dorm",
    "year",
    "high_school",
)

CAMPUSES: tuple[str, ...] = (
    "Caltech36",
    "Bowdoin47",
    "Harvard1",
    "Penn94",
    "Tennessee95",
)


@dataclass(frozen=True)
class CampusData:
    """A loaded Facebook100 campus, restricted to its giant connected component.

    Attributes
    ----------
    name
        Short campus name (e.g. "Caltech36").
    adjacency
        Sparse symmetric CSR adjacency over the giant component (n x n, binary).
    attributes
        Integer matrix (n, 7) of categorical attributes per node. 0 means missing.
    node_index_to_orig
        Maps the new contiguous node index back into the original .mat row index.
    """

    name: str
    adjacency: sp.csr_array
    attributes: np.ndarray
    node_index_to_orig: np.ndarray

    @property
    def n_nodes(self) -> int:
        return int(self.adjacency.shape[0])

    @property
    def n_edges(self) -> int:
        # Symmetric matrix; count nonzeros above the diagonal.
        upper = sp.triu(self.adjacency, k=1)
        return int(upper.nnz)

    def to_networkx(self) -> nx.Graph:
        """Build a networkx Graph view (use sparingly; the sparse matrix is canonical)."""
        graph = nx.from_scipy_sparse_array(self.adjacency, edge_attribute=None)
        for column_index, attribute_name in enumerate(ATTRIBUTE_NAMES):
            for node_index in range(self.n_nodes):
                graph.nodes[node_index][attribute_name] = int(self.attributes[node_index, column_index])
        return graph


def load_campus(name: str, data_dir: str | Path = "data/raw") -> CampusData:
    """Load a Facebook100 campus, restricted to its giant connected component.

    Parameters
    ----------
    name
        Campus identifier (e.g. "Caltech36"). The matching ``<name>.mat`` must
        exist under ``data_dir``.
    data_dir
        Directory holding the extracted .mat files.
    """
    path = Path(data_dir) / f"{name}.mat"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found. Run scripts/01_download_data.py to fetch the Facebook100 archive."
        )

    raw = scipy.io.loadmat(str(path))
    adjacency_full = sp.csr_array(raw["A"])
    attributes_full = np.asarray(raw["local_info"], dtype=np.int64)

    if adjacency_full.shape[0] != attributes_full.shape[0]:
        raise ValueError(
            f"{name}: adjacency has {adjacency_full.shape[0]} rows but local_info has {attributes_full.shape[0]}."
        )

    giant_indices = _giant_component_indices(adjacency_full)
    adjacency = adjacency_full[giant_indices, :][:, giant_indices]
    attributes = attributes_full[giant_indices]

    # Symmetrize defensively (Facebook100 is undirected; .mat sometimes has stray asymmetries).
    adjacency = (adjacency + adjacency.T) > 0
    adjacency = adjacency.astype(np.int8).tocsr()
    adjacency.setdiag(0)
    adjacency.eliminate_zeros()

    return CampusData(
        name=name,
        adjacency=adjacency,
        attributes=attributes,
        node_index_to_orig=giant_indices,
    )


def _giant_component_indices(adjacency: sp.csr_array) -> np.ndarray:
    """Return the indices of the largest connected component."""
    n_components, labels = sp.csgraph.connected_components(adjacency, directed=False)
    if n_components == 1:
        return np.arange(adjacency.shape[0])
    sizes = np.bincount(labels)
    largest_label = int(np.argmax(sizes))
    return np.flatnonzero(labels == largest_label)


def summarize(campus: CampusData) -> dict[str, float]:
    """Compute headline descriptive statistics for one campus."""
    adjacency = campus.adjacency.astype(np.float64)
    degrees = np.asarray(adjacency.sum(axis=1)).ravel()
    n = campus.n_nodes
    m = campus.n_edges
    return {
        "n_nodes": n,
        "n_edges": m,
        "density": (2 * m) / (n * (n - 1)) if n > 1 else 0.0,
        "mean_degree": float(degrees.mean()),
        "max_degree": int(degrees.max()),
        "missing_dorm_frac": float((campus.attributes[:, ATTRIBUTE_NAMES.index("dorm")] == 0).mean()),
        "missing_year_frac": float((campus.attributes[:, ATTRIBUTE_NAMES.index("year")] == 0).mean()),
    }
