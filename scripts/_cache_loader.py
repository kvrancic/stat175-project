"""Shared helper to reload cached campus artifacts produced by scripts/02_build_features.py.

Kept under scripts/ rather than src/ because it is glue code, not a library
function. Importable as ``scripts._cache_loader`` because scripts/__init__.py
exists alongside it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import scipy.sparse as sp

REPO_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = REPO_ROOT / "data" / "processed"

if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))


def load_cache(name: str) -> dict:
    """Reload cached campus artifacts (adjacency, features, edges, sigmoid_dot costs)."""
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
