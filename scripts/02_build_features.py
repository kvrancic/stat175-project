#!/usr/bin/env python
"""Build and cache one-hot L2-normalized features for every campus.

Idempotent: skips campuses whose ``.npz`` cache already exists. Edge enumeration
and per-edge sigmoid_dot costs are also cached so downstream policies and
simulators do not rebuild them on every run.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from stat175.costs.edge_costs import compute_costs, edges_from_adjacency  # noqa: E402
from stat175.data.facebook100 import CAMPUSES, load_campus  # noqa: E402
from stat175.data.features import build_one_hot_features  # noqa: E402

PROCESSED_DIR = REPO_ROOT / "data" / "processed"


def main() -> int:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name in CAMPUSES:
        out_path = PROCESSED_DIR / f"{name}.npz"
        if out_path.exists():
            print(f"[skip] {out_path.name} already cached")
            continue
        print(f"[build] {name}")
        campus = load_campus(name)
        features = build_one_hot_features(campus)
        edges = edges_from_adjacency(campus.adjacency)
        sigmoid_costs = compute_costs("sigmoid_dot", features, edges)
        adjacency = campus.adjacency.tocoo()
        np.savez_compressed(
            out_path,
            adj_data=adjacency.data,
            adj_row=adjacency.row,
            adj_col=adjacency.col,
            adj_shape=np.asarray(adjacency.shape, dtype=np.int64),
            attributes=campus.attributes,
            features_data=features.data,
            features_indices=features.indices,
            features_indptr=features.indptr,
            features_shape=np.asarray(features.shape, dtype=np.int64),
            edges=edges,
            sigmoid_dot_costs=sigmoid_costs,
        )
        print(
            f"  n={campus.n_nodes}, m={campus.n_edges}, features={features.shape[1]} dims, "
            f"sigmoid_cost mean={sigmoid_costs.mean():.4f}"
        )
    return 0


def load_cache(name: str) -> dict:
    """Reload cached campus artifacts (used by downstream scripts)."""
    path = PROCESSED_DIR / f"{name}.npz"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found; run scripts/02_build_features.py first"
        )
    archive = np.load(path)
    adjacency = sp.coo_array(
        (archive["adj_data"], (archive["adj_row"], archive["adj_col"])),
        shape=tuple(int(v) for v in archive["adj_shape"]),
    ).tocsr()
    features = sp.csr_array(
        (archive["features_data"], archive["features_indices"], archive["features_indptr"]),
        shape=tuple(int(v) for v in archive["features_shape"]),
    )
    return {
        "name": name,
        "adjacency": adjacency,
        "features": features,
        "attributes": archive["attributes"],
        "edges": archive["edges"],
        "sigmoid_dot_costs": archive["sigmoid_dot_costs"],
    }


if __name__ == "__main__":
    raise SystemExit(main())
