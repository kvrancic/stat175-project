"""Colab/A100 helper: re-train the link-prediction GNN at full fidelity.

This is the cluster/Colab-friendly variant of `scripts/03_train_gnn.py`. The
local sprint trained encoders at hidden_dim=32, embed_dim=16, 40 epochs,
with a TruncatedSVD-64 pre-projection of the one-hot feature matrix because
Harvard1 was 21.5 s/epoch on CPU. On an A100 each epoch is sub-second, so
we can drop the pre-projection, double the GNN width, and quintuple the
epoch count without paying real wall-clock cost.

The output is `data/processed/gnn_encoders/<campus>_graphsage.pt` payloads
that the rest of the pipeline (scripts/04..09) reads transparently.

Usage on Colab:
    !pip install torch_geometric scipy scikit-learn
    !python notebooks/01_colab_train_full_gnn.py --campuses Harvard1 Penn94 Tennessee95

Replace the local encoder cache with the Colab-trained encoders, then re-run
`scripts/04_run_pareto.py` and beyond. None of the downstream code needs to
change; the encoder payload format is the same.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import torch

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))

from scripts._cache_loader import load_cache  # noqa: E402

from stat175.models.gnn import GNNConfig  # noqa: E402
from stat175.models.training import TrainingConfig, train_link_prediction  # noqa: E402

ENCODER_DIR = REPO_ROOT / "data" / "processed" / "gnn_encoders"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--campuses",
        nargs="*",
        default=["Caltech36", "Bowdoin47", "Harvard1", "Penn94", "Tennessee95"],
    )
    parser.add_argument("--hidden-dim", type=int, default=64)
    parser.add_argument("--embed-dim", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=200)
    parser.add_argument("--lr", type=float, default=0.005)
    parser.add_argument(
        "--no-svd",
        action="store_true",
        help="Skip TruncatedSVD pre-projection (full one-hot features into the GNN).",
    )
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    print(f"[device] {args.device}")
    ENCODER_DIR.mkdir(parents=True, exist_ok=True)
    for campus_name in args.campuses:
        cache = load_cache(campus_name)
        adjacency = cache["adjacency"]
        features = cache["features"]
        gnn_cfg = GNNConfig(
            arch="graphsage",
            in_dim=int(features.shape[1]),
            hidden_dim=int(args.hidden_dim),
            embed_dim=int(args.embed_dim),
            n_layers=2,
            dropout=0.1,
        )
        training_cfg = TrainingConfig(
            epochs=int(args.epochs),
            lr=float(args.lr),
            project_features_to=None if args.no_svd else 64,
            device=args.device,
        )
        start = time.time()
        result = train_link_prediction(adjacency, features, gnn_cfg, training_cfg)
        elapsed = time.time() - start
        print(f"  {campus_name}: trained in {elapsed:.1f}s; val AUROC={result.val_aurocs[-1]:.4f}")

        payload = {
            "config": {
                "arch": gnn_cfg.arch,
                "in_dim": result.encoder.config.in_dim,
                "hidden_dim": gnn_cfg.hidden_dim,
                "embed_dim": gnn_cfg.embed_dim,
                "n_layers": gnn_cfg.n_layers,
                "dropout": gnn_cfg.dropout,
                "heads": gnn_cfg.heads,
            },
            "state_dict": result.encoder.state_dict(),
            "projection_matrix": result.projection_matrix,
        }
        target = ENCODER_DIR / f"{campus_name}_graphsage.pt"
        torch.save(payload, target)
        print(f"  [saved] {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
