from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any


class JsonFormatter(logging.Formatter):
    """A simple JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - formatting
        data: dict[str, Any] = {
            "timestamp": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
        }
        # include selected extras
        for key in ("details", "path"):
            if hasattr(record, key):
                data[key] = getattr(record, key)
        if record.exc_info:
            data["exception"] = self.formatException(record.exc_info)
        return json.dumps(data)


def configure_logging(level: str = "INFO") -> logging.Logger:
    """Configure root logger to output JSON logs to stdout."""
    logger = logging.getLogger()
    logger.setLevel(level.upper())
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logger.handlers = [handler]
    return logger
