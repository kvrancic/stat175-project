#!/usr/bin/env python
"""Train one GNN encoder per campus and persist them under data/processed/.

Self-supervised link-prediction objective; trains in seconds per campus.
The trained encoder produces embeddings z_v whose pairwise sigmoid dot
product gives the GNN policy's learned edge cost.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from stat175.data.facebook100 import CAMPUSES  # noqa: E402
from stat175.models.gnn import GNNConfig  # noqa: E402
from stat175.models.training import TrainingConfig, train_link_prediction  # noqa: E402

PROCESSED_DIR = REPO_ROOT / "data" / "processed"
MODELS_DIR = REPO_ROOT / "data" / "processed" / "gnn_encoders"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=REPO_ROOT / "configs" / "default.yaml")
    parser.add_argument("--arch", type=str, default=None, help="Override architecture (graphsage/gat/gcn)")
    parser.add_argument("--force", action="store_true", help="Retrain even if cached encoder exists")
    args = parser.parse_args()

    with open(args.config) as cfg_file:
        config = yaml.safe_load(cfg_file)
    gnn_cfg = config["gnn"]
    arch = args.arch if args.arch is not None else gnn_cfg["arch"]

    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    from scripts._cache_loader import load_cache  # type: ignore[import-not-found]

    for name in CAMPUSES:
        target = MODELS_DIR / f"{name}_{arch}.pt"
        if target.exists() and not args.force:
            print(f"[skip] {target.name} already trained")
            continue
        cache = load_cache(name)
        adjacency = cache["adjacency"]
        features = cache["features"]
        gnn_config = GNNConfig(
            arch=arch,
            in_dim=int(features.shape[1]),
            hidden_dim=int(gnn_cfg["hidden_dim"]),
            embed_dim=int(gnn_cfg["embed_dim"]),
            n_layers=int(gnn_cfg["n_layers"]),
            dropout=float(gnn_cfg["dropout"]),
        )
        training_config = TrainingConfig(
            epochs=int(gnn_cfg["epochs"]),
            lr=float(gnn_cfg["learning_rate"]),
            weight_decay=float(gnn_cfg["weight_decay"]),
            seed=int(config["seed"]),
            max_train_pairs=int(gnn_cfg.get("max_train_pairs", 200000)),
        )
        print(f"[train] {name} ({arch}, {adjacency.shape[0]} nodes)")
        start = time.time()
        result = train_link_prediction(adjacency, features, gnn_config, training_config)
        # The encoder may have been rebuilt with projected in_dim during training;
        # save the actual encoder's config (not the original) so reload uses the
        # right input dimensionality.
        config_to_save = {
            "arch": gnn_config.arch,
            "in_dim": int(result.encoder.config.in_dim),
            "hidden_dim": int(result.encoder.config.hidden_dim),
            "embed_dim": int(result.encoder.config.embed_dim),
            "n_layers": int(result.encoder.config.n_layers),
            "dropout": float(result.encoder.config.dropout),
            "heads": int(result.encoder.config.heads),
        }
        torch.save(
            {
                "state_dict": result.encoder.state_dict(),
                "config": config_to_save,
                "train_losses": result.train_losses,
                "val_aurocs": result.val_aurocs,
                "projection_matrix": result.projection_matrix,
            },
            target,
        )
        elapsed = time.time() - start
        print(
            f"  saved {target.name}  (elapsed = {elapsed:.1f}s, "
            f"final loss = {result.train_losses[-1]:.4f}, val AUROC = {result.val_aurocs[-1]:.4f})"
        )

    return 0


def load_encoder(campus_name: str, arch: str = "graphsage", device: str = "cpu"):
    """Reload a saved encoder for use in scripts/04_run_pareto.py."""
    target = MODELS_DIR / f"{campus_name}_{arch}.pt"
    if not target.exists():
        raise FileNotFoundError(
            f"{target} not found; run scripts/03_train_gnn.py to train the GNN."
        )
    payload = torch.load(target, map_location=device, weights_only=False)
    config = GNNConfig(**payload["config"])
    from stat175.models.gnn import GNNEncoder  # local import to avoid hard dep at module load

    encoder = GNNEncoder(config).to(device)
    encoder.load_state_dict(payload["state_dict"])
    encoder.eval()
    return encoder


if __name__ == "__main__":
    raise SystemExit(main())
