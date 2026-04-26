#!/usr/bin/env python
"""Download and stage the Facebook100 .mat files for the 5 chosen campuses.

Pulls the canonical Oxford Facebook100 archive from the Internet Archive,
extracts only the 5 .mat files we need into ``data/raw/``, and verifies sizes.

If ``data/raw/<Campus>.mat`` already exists for all five campuses the script
is a no-op (idempotent).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ARCHIVE_URL = "https://archive.org/download/oxford-2005-facebook-matrix/facebook100.zip"
ARCHIVE_FILE = "facebook100.zip"
CAMPUSES = ("Caltech36", "Bowdoin47", "Harvard1", "Penn94", "Tennessee95")
README_NAME = "facebook100_readme_021011.txt"

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    if all((RAW_DIR / f"{name}.mat").exists() for name in CAMPUSES):
        print(f"[ok] All {len(CAMPUSES)} .mat files already present in {RAW_DIR}.")
        return 0

    archive_path = RAW_DIR / ARCHIVE_FILE
    if not archive_path.exists():
        print(f"[fetch] Downloading {ARCHIVE_URL} (~206 MB) ...")
        if shutil.which("curl") is None:
            print("[err] curl not found on PATH; install it or download the zip manually.", file=sys.stderr)
            return 2
        rc = subprocess.run(
            ["curl", "-L", "--fail", "-o", str(archive_path), ARCHIVE_URL],
            check=False,
        ).returncode
        if rc != 0:
            print(f"[err] curl exited {rc}; archive download failed.", file=sys.stderr)
            return rc

    print(f"[extract] Extracting 5 .mat files from {archive_path} ...")
    with zipfile.ZipFile(archive_path) as zf:
        for name in CAMPUSES:
            member = f"facebook100/{name}.mat"
            destination = RAW_DIR / f"{name}.mat"
            with zf.open(member) as src, open(destination, "wb") as dst:
                shutil.copyfileobj(src, dst)
            print(f"  - {destination.name} ({destination.stat().st_size / 1024:.1f} KB)")
        readme_member = f"facebook100/{README_NAME}"
        with zf.open(readme_member) as src, open(RAW_DIR / README_NAME, "wb") as dst:
            shutil.copyfileobj(src, dst)

    print("[done] Facebook100 .mat files staged under data/raw/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
