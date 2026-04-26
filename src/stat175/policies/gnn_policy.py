"""GNN-based learned policy — Outline policy 3, the novel contribution.

Implements the Outline language exactly:
  - GNN learns node embeddings z_v.
  - Edge costs derived from embedding similarity:  c_e^GNN = sigmoid(<z_u, z_v>).
  - Policy selects lowest-cost edges that achieve containment.

"Achieve containment" is operationalized via the NetMelt eigenscore
(Tong et al. 2012, anchor paper from useful-readings-A.md sec 3): the
contribution of edge (u, v) to the leading eigenvalue of the adjacency
is approximately u_v_prod = u_i * v_j + u_j * v_i, where u and v are the
left/right components of the leading eigenvector. Removing edges with
high u_v_prod / cost yields the maximum reduction in lambda_1(A) per unit
of social cost, which (by the spectral threshold tau_c = 1 / lambda_1(A))
is the principled definition of "achieving containment cheaply".

Training is delegated to ``stat175.models.training.train_link_prediction``,
which trains a GNN encoder via self-supervised link prediction on the
campus's friendship graph. Trained encoders can be cached in a dict
keyed by campus name so the policy can be re-used across budgets and
experiments without re-training.
"""

from __future__ import annotations

import numpy as np
import scipy.sparse as sp
import torch

from ..models.gnn import GNNEncoder, adjacency_to_edge_index, features_to_torch
from .base import Policy, PolicyInput, greedy_fill_by_score


class GNNPolicy:
    name = "gnn"

    def __init__(
        self,
        encoder: GNNEncoder,
        features: sp.csr_array,
        epsilon: float = 1e-6,
        device: str = "cpu",
    ):
        self.encoder = encoder
        self.features = features
        self.epsilon = epsilon
        self.device = device
        self._cached_embeddings: np.ndarray | None = None
        self._cached_eigenvector: np.ndarray | None = None
        self._cached_adjacency_id: int | None = None

    def select(self, inputs: PolicyInput) -> np.ndarray:
        adjacency_id = id(inputs.adjacency)
        if self._cached_adjacency_id != adjacency_id:
            self._cached_embeddings = None
            self._cached_eigenvector = None
            self._cached_adjacency_id = adjacency_id
        embeddings = self._embed(inputs.adjacency)

        # Learned per-edge cost: sigmoid(<z_u, z_v>).
        u_index = inputs.edges[:, 0]
        v_index = inputs.edges[:, 1]
        inner = (embeddings[u_index] * embeddings[v_index]).sum(axis=1)
        learned_cost = 1.0 / (1.0 + np.exp(-inner))

        # Structural impact via NetMelt eigenscore on the residual adjacency.
        if self._cached_eigenvector is None:
            self._cached_eigenvector = _leading_eigenvector(inputs.adjacency)
        leading_eigenvector = self._cached_eigenvector
        eigenscore = 2.0 * leading_eigenvector[u_index] * leading_eigenvector[v_index]

        # Bang-for-buck: containment impact per unit social cost.
        score = eigenscore / np.clip(learned_cost, self.epsilon, None)
        return greedy_fill_by_score(score, inputs.costs, inputs.budget)

    def _embed(self, adjacency: sp.csr_array) -> np.ndarray:
        adjacency_id = id(adjacency)
        if self._cached_embeddings is not None and self._cached_adjacency_id == adjacency_id:
            return self._cached_embeddings
        self.encoder.eval()
        projection = getattr(self.encoder, "projection_matrix", None)
        if projection is not None:
            projected = self.features @ projection
            feature_tensor = torch.from_numpy(np.asarray(projected, dtype=np.float32)).to(
                torch.device(self.device)
            )
        else:
            feature_tensor = features_to_torch(self.features).to(torch.device(self.device))
        edge_index = adjacency_to_edge_index(adjacency).to(torch.device(self.device))
        with torch.no_grad():
            embeddings = self.encoder(feature_tensor, edge_index)
        embeddings_np = embeddings.detach().cpu().numpy()
        self._cached_embeddings = embeddings_np
        self._cached_adjacency_id = adjacency_id
        return embeddings_np


def _leading_eigenvector(adjacency: sp.csr_array) -> np.ndarray:
    """Return the leading (largest-eigenvalue) eigenvector of the adjacency."""
    from scipy.sparse.linalg import eigsh

    matrix = adjacency.astype(np.float64)
    _, eigenvectors = eigsh(matrix, k=1, which="LA")
    return eigenvectors[:, 0]


_: Policy = GNNPolicy.__new__(GNNPolicy)  # type-check only; real instances need an encoder
