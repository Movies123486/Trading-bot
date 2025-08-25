from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

from .settings import Settings


def _git_commit() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    except Exception:  # pragma: no cover - git not available
        return "unknown"


def create_run_manifest(settings: Settings, output_dir: Path) -> Path:
    """Write a run manifest JSON file and return its path."""
    manifest = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_commit": _git_commit(),
        "config": {
            "data_dir": str(settings.data_dir),
            "log_level": settings.log_level,
            "ntp_server": settings.ntp_server,
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    fname = output_dir / f"run_{datetime.utcnow().strftime('%Y%m%dT%H%M%S')}.json"
    with fname.open("w") as fh:
        json.dump(manifest, fh, indent=2)
    return fname
