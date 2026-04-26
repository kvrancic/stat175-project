"""Self-supervised link-prediction training for the GNN policy.

The Outline says: "GNN learns node embeddings; edge costs derived from
embedding similarity". We give the GNN a clean training signal that ties
embedding similarity to social closeness: predict whether a given (u, v)
pair is an edge in the campus's friendship graph (positive) versus a
randomly sampled non-edge (negative).

After training, sigmoid(<z_u, z_v>) is naturally interpretable as the
probability that (u, v) is an edge, which is exactly the "cost of removing
this edge" interpretation we want: edges that the GNN believes "should"
exist (high homophily, lots of structural support) get a high cost.

This trains in seconds, has no dependency on the SIS simulator (so it is
robust to simulation noise), and yields a GNN whose induced cost function
is directly comparable to the hand-designed sigmoid-dot baseline.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import scipy.sparse as sp
import torch
from torch import nn

from .gnn import GNNConfig, GNNEncoder, adjacency_to_edge_index, features_to_torch


@dataclass(frozen=True)
class TrainingConfig:
    epochs: int = 100
    lr: float = 0.005
    weight_decay: float = 0.0001
    neg_sampling_ratio: int = 1
    val_fraction: float = 0.1
    seed: int = 42
    device: str = "cpu"


@dataclass
class TrainingResult:
    encoder: GNNEncoder
    train_losses: list[float]
    val_aurocs: list[float]


def train_link_prediction(
    adjacency: sp.csr_array,
    features: sp.csr_array,
    gnn_config: GNNConfig,
    training_config: TrainingConfig,
) -> TrainingResult:
    """Train ``gnn_config``-sized encoder via link-prediction BCE."""
    if gnn_config.in_dim != features.shape[1]:
        gnn_config = GNNConfig(
            arch=gnn_config.arch,
            in_dim=int(features.shape[1]),
            hidden_dim=gnn_config.hidden_dim,
            embed_dim=gnn_config.embed_dim,
            n_layers=gnn_config.n_layers,
            dropout=gnn_config.dropout,
            heads=gnn_config.heads,
        )

    torch.manual_seed(training_config.seed)
    rng = np.random.default_rng(training_config.seed)
    device = torch.device(training_config.device)

    n_nodes = int(adjacency.shape[0])
    upper = sp.triu(adjacency, k=1).tocoo()
    pos_pairs = np.column_stack([upper.row, upper.col]).astype(np.int64)

    n_pairs = pos_pairs.shape[0]
    permutation = rng.permutation(n_pairs)
    n_val = max(1, int(training_config.val_fraction * n_pairs))
    val_indices = permutation[:n_val]
    train_indices = permutation[n_val:]
    train_pos = pos_pairs[train_indices]
    val_pos = pos_pairs[val_indices]

    # Use the FULL graph for message passing (transductive link prediction)
    full_edge_index = adjacency_to_edge_index(adjacency).to(device)
    feature_tensor = features_to_torch(features).to(device)

    encoder = GNNEncoder(gnn_config).to(device)
    optimizer = torch.optim.Adam(
        encoder.parameters(),
        lr=training_config.lr,
        weight_decay=training_config.weight_decay,
    )
    bce_loss = nn.BCEWithLogitsLoss()

    train_losses: list[float] = []
    val_aurocs: list[float] = []
    for epoch_index in range(training_config.epochs):
        encoder.train()
        optimizer.zero_grad()

        embeddings = encoder(feature_tensor, full_edge_index)

        n_train_pos = train_pos.shape[0]
        neg_u = rng.integers(0, n_nodes, size=n_train_pos * training_config.neg_sampling_ratio)
        neg_v = rng.integers(0, n_nodes, size=n_train_pos * training_config.neg_sampling_ratio)
        neg_pairs = np.column_stack([neg_u, neg_v]).astype(np.int64)

        all_pairs_np = np.concatenate([train_pos, neg_pairs], axis=0)
        labels_np = np.concatenate(
            [
                np.ones(n_train_pos, dtype=np.float32),
                np.zeros(neg_pairs.shape[0], dtype=np.float32),
            ]
        )
        all_pairs = torch.from_numpy(all_pairs_np).to(device)
        labels = torch.from_numpy(labels_np).to(device)

        edge_logits = (embeddings[all_pairs[:, 0]] * embeddings[all_pairs[:, 1]]).sum(dim=-1)
        loss = bce_loss(edge_logits, labels)
        loss.backward()
        optimizer.step()
        train_losses.append(float(loss.item()))

        if (epoch_index + 1) % 10 == 0 or epoch_index == 0:
            val_score = _validation_auroc(encoder, feature_tensor, full_edge_index, val_pos, n_nodes, rng, device)
            val_aurocs.append(val_score)

    return TrainingResult(encoder=encoder, train_losses=train_losses, val_aurocs=val_aurocs)


def encode(encoder: GNNEncoder, features: sp.csr_array, adjacency: sp.csr_array, device: str = "cpu") -> np.ndarray:
    """Run the encoder once and return embeddings as a numpy array."""
    encoder.eval()
    feature_tensor = features_to_torch(features).to(torch.device(device))
    edge_index = adjacency_to_edge_index(adjacency).to(torch.device(device))
    with torch.no_grad():
        embeddings = encoder(feature_tensor, edge_index)
    return embeddings.detach().cpu().numpy()


def _validation_auroc(
    encoder: GNNEncoder,
    feature_tensor: torch.Tensor,
    edge_index: torch.Tensor,
    val_pos: np.ndarray,
    n_nodes: int,
    rng: np.random.Generator,
    device: torch.device,
) -> float:
    encoder.eval()
    with torch.no_grad():
        embeddings = encoder(feature_tensor, edge_index)
    n_pos = val_pos.shape[0]
    neg_u = rng.integers(0, n_nodes, size=n_pos)
    neg_v = rng.integers(0, n_nodes, size=n_pos)
    neg_pairs = np.column_stack([neg_u, neg_v]).astype(np.int64)
    all_pairs = np.concatenate([val_pos, neg_pairs], axis=0)
    pair_tensor = torch.from_numpy(all_pairs).to(device)
    scores = (embeddings[pair_tensor[:, 0]] * embeddings[pair_tensor[:, 1]]).sum(dim=-1)
    scores_np = scores.detach().cpu().numpy()
    labels = np.concatenate([np.ones(n_pos), np.zeros(n_pos)])

    # Quick AUROC via Mann-Whitney U.
    order = np.argsort(scores_np)
    ranks = np.empty_like(order, dtype=np.float64)
    ranks[order] = np.arange(1, scores_np.shape[0] + 1)
    n_neg = labels.shape[0] - int(labels.sum())
    sum_pos_rank = float(ranks[labels == 1].sum())
    auroc = (sum_pos_rank - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg)
    return float(auroc)
