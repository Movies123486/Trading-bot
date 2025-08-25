from __future__ import annotations

import importlib
import socket
import struct
import sys
import time
from typing import Dict, List


REQUIRED_DEPENDENCIES: List[str] = [
    "pandas",
    "pyarrow",
    "pydantic",
    "requests",
]


def check_python_version(min_version: tuple[int, int] = (3, 10)) -> bool:
    """Return True if the running Python version meets the minimum."""
    return sys.version_info >= min_version


def check_dependencies() -> List[str]:
    """Return a list of missing dependencies."""
    missing = []
    for dep in REQUIRED_DEPENDENCIES:
        if importlib.util.find_spec(dep) is None:
            missing.append(dep)
    return missing


def _get_ntp_time(server: str, timeout: float = 5.0) -> float:
    """Query *server* for the current time and return it as a UNIX timestamp."""
    port = 123
    buf = 1024
    address = (server, port)
    msg = b"\x1b" + 47 * b"\0"
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        client.settimeout(timeout)
        client.sendto(msg, address)
        data, _ = client.recvfrom(buf)
    finally:
        client.close()
    if data:
        t = struct.unpack("!12I", data)[10]
        t -= 2208988800
        return t
    raise RuntimeError("no data received from NTP server")


def check_ntp_sync(server: str, max_offset: float = 1.0) -> float:
    """Check system clock against NTP *server*.

    Returns the absolute offset in seconds. Raises ``RuntimeError`` if the
    offset exceeds ``max_offset``.
    """
    ntp_time = _get_ntp_time(server)
    local_time = time.time()
    offset = local_time - ntp_time
    if abs(offset) > max_offset:
        raise RuntimeError(
            f"System clock offset {offset:.2f}s exceeds allowed {max_offset}s"
        )
    return offset


def check_environment(ntp_server: str) -> Dict[str, object]:
    """Run environment checks and return results as a dictionary."""
    results: Dict[str, object] = {
        "python_version_ok": check_python_version(),
        "missing_dependencies": check_dependencies(),
    }
    try:
        results["ntp_offset"] = check_ntp_sync(ntp_server)
    except Exception as exc:  # pragma: no cover - network failure scenario
        results["ntp_error"] = str(exc)
    return results
