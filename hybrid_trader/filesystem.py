from __future__ import annotations

from datetime import date
from pathlib import Path


def ensure_hive_partition(base_dir: Path, symbol: str, timeframe: str, dt: date) -> Path:
    """Create a Hive-style partition path for *symbol* at *dt* and return it."""
    path = (
        base_dir
        / f"symbol={symbol}"
        / f"timeframe={timeframe}"
        / f"year={dt.year:04d}"
        / f"month={dt.month:02d}"
        / f"day={dt.day:02d}"
    )
    path.mkdir(parents=True, exist_ok=True)
    return path
