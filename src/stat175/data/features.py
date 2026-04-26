"""Build node feature matrices from Facebook100 categorical attributes.

Strategy (per CENTRAL-KNOWLEDGE.md sec IX.4):
- Treat missing values (coded 0 in .mat) as their own category, not imputed.
- One-hot encode each attribute independently, then concatenate.
- L2-normalize each row so that the dot product of two feature vectors is
  bounded in [-1, 1] and not dominated by nodes with more present attributes
  (CENTRAL-KNOWLEDGE.md sec IX.5).
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp

from .facebook100 import ATTRIBUTE_NAMES, CampusData


def build_one_hot_features(campus: CampusData) -> sp.csr_array:
    """One-hot encode all 7 attributes (with missing-as-category) and L2-normalize rows.

    Returns
    -------
    sp.csr_array of shape (n_nodes, total_categories) with row L2 norm <= 1.
    """
    columns = []
    for attribute_index in range(len(ATTRIBUTE_NAMES)):
        columns.append(_one_hot_column(campus.attributes[:, attribute_index]))
    feature_matrix = sp.hstack(columns, format="csr")
    return _l2_normalize_rows(feature_matrix)


def _one_hot_column(column_values: np.ndarray) -> sp.csr_array:
    """One-hot encode a single integer-valued column (0 stays its own bin)."""
    unique_values, inverse = np.unique(column_values, return_inverse=True)
    n_rows = column_values.shape[0]
    n_categories = unique_values.shape[0]
    indptr = np.arange(n_rows + 1, dtype=np.int64)
    indices = inverse.astype(np.int64)
    data = np.ones(n_rows, dtype=np.float32)
    return sp.csr_array((data, indices, indptr), shape=(n_rows, n_categories))


def _l2_normalize_rows(matrix: sp.csr_array) -> sp.csr_array:
    """Divide each row by its L2 norm in place. Zero rows remain zero."""
    squared = matrix.multiply(matrix)
    row_norms = np.sqrt(np.asarray(squared.sum(axis=1)).ravel())
    row_norms[row_norms == 0] = 1.0
    inv = sp.diags_array(1.0 / row_norms, format="csr")
    return (inv @ matrix).tocsr()


def feature_matrix_shape(features: sp.csr_array) -> tuple[int, int]:
    return features.shape[0], features.shape[1]
