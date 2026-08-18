"""
IESA Configuration Loader
~~~~~~~~~~~~~~~~~~~~~~~~~
Loads environment variables from a .env file and provides sensible defaults
for all configurable parameters. Every other module should import from here
rather than reading os.environ directly.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from project root (one level above code/)
# ---------------------------------------------------------------------------
_PROJECT_ROOT = Path(__file__).resolve().parent.parent  # …/code/
_ENV_FILE = _PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=_ENV_FILE)


def _env(key: str, default: str | None = None) -> str | None:
    """Read an environment variable with an optional default."""
    return os.getenv(key, default)


def _env_int(key: str, default: int) -> int:
    """Read an environment variable as an integer."""
    raw = os.getenv(key)
    if raw is None:
        return default
    try:
        return int(raw, 0)  # base 0 → auto-detect hex (0x3C) or decimal
    except ValueError:
        return default


# ---------------------------------------------------------------------------
# Application settings
# ---------------------------------------------------------------------------

# Database
DATABASE_PATH: str = _env("DATABASE_PATH", str(_PROJECT_ROOT / "data" / "iesa.db"))

# Logging
LOG_LEVEL: str = _env("LOG_LEVEL", "INFO").upper()
LOG_DIR: str = _env("LOG_DIR", str(_PROJECT_ROOT / "logs"))

# OLED display (I²C)
OLED_I2C_ADDRESS: int = _env_int("OLED_I2C_ADDRESS", 0x3C)
OLED_WIDTH: int = _env_int("OLED_WIDTH", 128)
OLED_HEIGHT: int = _env_int("OLED_HEIGHT", 64)

# Guest data retention
GUEST_RETENTION_HOURS: int = _env_int("GUEST_RETENTION_HOURS", 24)

# ---------------------------------------------------------------------------
# USB Camera (video / face recognition)
# ---------------------------------------------------------------------------
CAMERA_DEVICE: str = _env("CAMERA_DEVICE", "/dev/video0")
CAMERA_WIDTH: int = _env_int("CAMERA_WIDTH", 640)
CAMERA_HEIGHT: int = _env_int("CAMERA_HEIGHT", 480)
CAMERA_FPS: int = _env_int("CAMERA_FPS", 30)

# ---------------------------------------------------------------------------
# Raspberry Pi AI HAT+ (Hailo-8L accelerator)
# Used for on-device speech recognition and voice recognition
# ---------------------------------------------------------------------------
AI_HAT_ENABLED: bool = _env("AI_HAT_ENABLED", "true").lower() in ("true", "1", "yes")
AI_HAT_DEVICE: str = _env("AI_HAT_DEVICE", "/dev/hailo0")
SPEECH_SAMPLE_RATE: int = _env_int("SPEECH_SAMPLE_RATE", 16000)
SPEECH_LANGUAGE: str = _env("SPEECH_LANGUAGE", "en")

# ---------------------------------------------------------------------------
# Convenience: collect everything into a dict for logging / health checks
# ---------------------------------------------------------------------------

def as_dict() -> dict:
    """Return all settings as a plain dictionary."""
    return {
        "DATABASE_PATH": DATABASE_PATH,
        "LOG_LEVEL": LOG_LEVEL,
        "LOG_DIR": LOG_DIR,
        "OLED_I2C_ADDRESS": hex(OLED_I2C_ADDRESS),
        "OLED_WIDTH": OLED_WIDTH,
        "OLED_HEIGHT": OLED_HEIGHT,
        "GUEST_RETENTION_HOURS": GUEST_RETENTION_HOURS,
        "CAMERA_DEVICE": CAMERA_DEVICE,
        "CAMERA_RESOLUTION": f"{CAMERA_WIDTH}x{CAMERA_HEIGHT}",
        "CAMERA_FPS": CAMERA_FPS,
        "AI_HAT_ENABLED": AI_HAT_ENABLED,
        "AI_HAT_DEVICE": AI_HAT_DEVICE,
        "SPEECH_SAMPLE_RATE": SPEECH_SAMPLE_RATE,
        "SPEECH_LANGUAGE": SPEECH_LANGUAGE,
    }
