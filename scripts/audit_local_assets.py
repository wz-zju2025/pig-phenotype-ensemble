#!/usr/bin/env python3
"""Check local files named in config/local_paths.json. Does not load models."""

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "local_paths.json"
OUT = ROOT / "outputs" / "audit.json"


def main() -> None:
    if not CONFIG.exists():
        raise SystemExit(f"missing {CONFIG}; copy config/local_paths.example.json")
    paths = json.loads(CONFIG.read_text())
    rows = []
    for key, value in paths.items():
        path = Path(value)
        exists = path.exists()
        size = path.stat().st_size if exists and path.is_file() else None
        rows.append(
            {
                "key": key,
                "exists": exists,
                "is_file": path.is_file() if exists else False,
                "is_dir": path.is_dir() if exists else False,
                "bytes": size,
            }
        )
        state = "ok" if exists else "missing"
        print(f"{state}\t{key}\t{size if size is not None else '-'}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(rows, indent=2) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
