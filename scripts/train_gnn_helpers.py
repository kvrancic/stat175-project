"""Reload helpers for trained GNN encoders.

Importable as ``scripts.train_gnn_helpers`` so other scripts (notably
``scripts/04_run_pareto.py``) can fetch a previously trained encoder by
campus name without duplicating model-construction logic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = REPO_ROOT / "data" / "processed" / "gnn_encoders"

if str(REPO_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "src"))


def load_encoder(campus_name: str, arch: str = "graphsage", device: str = "cpu"):
    target = MODELS_DIR / f"{campus_name}_{arch}.pt"
    if not target.exists():
        raise FileNotFoundError(
            f"{target} not found; run scripts/03_train_gnn.py to train the GNN."
        )
    payload = torch.load(target, map_location=device, weights_only=False)
    from stat175.models.gnn import GNNConfig, GNNEncoder

    config = GNNConfig(**payload["config"])
    encoder = GNNEncoder(config).to(device)
    encoder.load_state_dict(payload["state_dict"])
    encoder.eval()
    encoder.projection_matrix = payload.get("projection_matrix")  # numpy or None
    return encoder
