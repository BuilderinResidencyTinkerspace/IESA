"""
IESA Logging Setup
~~~~~~~~~~~~~~~~~~
Configures a root logger with both console and rotating-file handlers.
All other modules should use ``logging.getLogger(__name__)`` – they will
inherit this configuration automatically.
"""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import settings


def setup_logging() -> logging.Logger:
    """
    Create and configure the ``iesa`` logger.

    Returns:
        The configured root logger for the application.
    """
    logger = logging.getLogger("iesa")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    # Avoid adding duplicate handlers on repeated calls
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-24s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # ── Console handler ──────────────────────────────────────────────
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)
    logger.addHandler(console)

    # ── File handler (rotating, 5 MB × 3 backups) ───────────────────
    log_dir = Path(settings.LOG_DIR)
    log_dir.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        filename=log_dir / "iesa.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    logger.debug("Logger initialised  (level=%s, dir=%s)", settings.LOG_LEVEL, log_dir)
    return logger
