from __future__ import annotations

import logging
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from flask import Flask


def configure_logging(app: Flask) -> None:
    """
    Configure console + rotating file logging via dictConfig.
    Ensures log directory exists safely.
    """
    log_dir = Path(app.config.get("LOG_DIR", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)

    log_level = str(app.config.get("LOG_LEVEL", "INFO")).upper()
    log_file = log_dir / str(app.config.get("LOG_FILE_NAME", "app.log"))

    config: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s %(levelname)s %(name)s: %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": log_level,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "level": log_level,
                "filename": str(log_file),
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": log_level,
        },
    }

    dictConfig(config)

    # Make Flask's logger align with root settings.
    app.logger.setLevel(getattr(logging, log_level, logging.INFO))
