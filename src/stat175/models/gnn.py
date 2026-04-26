"""GNN encoders behind a unified interface.

We expose three architectures (GraphSAGE, GAT, GCN) so the architecture
ablation in Milestone 5 can swap them with a single config flag.
All encoders take a sparse one-hot feature matrix and produce
fixed-dimensional node embeddings.
"""

from __future__ import annotations

from dataclasses import dataclass

import scipy.sparse as sp
import torch
from torch import nn
from torch_geometric.nn import GATConv, GCNConv, SAGEConv


@dataclass(frozen=True)
class GNNConfig:
    arch: str = "graphsage"
    in_dim: int = 0
    hidden_dim: int = 64
    embed_dim: int = 32
    n_layers: int = 2
    dropout: float = 0.1
    heads: int = 4  # only used by GAT


class GNNEncoder(nn.Module):
    """Stacked message-passing encoder: features -> embeddings."""

    def __init__(self, config: GNNConfig):
        super().__init__()
        if config.in_dim <= 0:
            raise ValueError("config.in_dim must be set to the feature dimensionality")
        self.config = config
        layers: list[nn.Module] = []
        in_dim = config.in_dim
        for layer_index in range(config.n_layers):
            out_dim = config.embed_dim if layer_index == config.n_layers - 1 else config.hidden_dim
            if config.arch == "graphsage":
                layers.append(SAGEConv(in_dim, out_dim))
            elif config.arch == "gat":
                heads = 1 if layer_index == config.n_layers - 1 else config.heads
                layers.append(GATConv(in_dim, out_dim // heads, heads=heads, concat=heads > 1))
            elif config.arch == "gcn":
                layers.append(GCNConv(in_dim, out_dim))
            else:
                raise ValueError(f"unknown GNN arch {config.arch!r}")
            in_dim = out_dim
        self.layers = nn.ModuleList(layers)
        self.dropout = nn.Dropout(p=config.dropout)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        h = x
        for layer_index, layer in enumerate(self.layers):
            h = layer(h, edge_index)
            if layer_index < len(self.layers) - 1:
                h = torch.relu(h)
                h = self.dropout(h)
        return h


def features_to_torch(features: sp.csr_array) -> torch.Tensor:
    """Convert an scipy sparse one-hot matrix to a dense float tensor.

    For our sizes (max ~5k feature dims) dense is fine and avoids
    fragility around torch sparse on different builds.
    """
    return torch.from_numpy(features.toarray()).float()


def adjacency_to_edge_index(adjacency: sp.csr_array) -> torch.Tensor:
    """Convert a CSR adjacency to the symmetric (2, E) edge_index expected by PyG."""
    coo = adjacency.tocoo()
    rows = torch.from_numpy(coo.row.astype("int64"))
    cols = torch.from_numpy(coo.col.astype("int64"))
    edge_index = torch.stack([rows, cols], dim=0)
    return edge_index
