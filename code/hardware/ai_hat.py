"""
AI HAT+ Manager (Stub)
~~~~~~~~~~~~~~~~~~~~~~
Manages the Raspberry Pi AI HAT+ (Hailo-8L) accelerator used for
on-device speech recognition and voice recognition.

Hardware path:
    Detects the Hailo device at the path configured in settings
    (default ``/dev/hailo0``).  The AI HAT+ connects via the Pi 5's
    M.2 PCIe slot and requires the HailoRT runtime to be installed.

Fallback path:
    If the Hailo device is not found or ``AI_HAT_ENABLED`` is set to
    ``false``, switches to *dummy mode*.  This allows development and
    testing without the physical accelerator.

.. note::
    Actual model loading and inference (HailoRT SDK) will be added in
    a later stage.  This stub provides the lifecycle hooks and health
    interface so the SystemManager can register it now.
"""

from __future__ import annotations

import logging
from pathlib import Path

from config import settings

log = logging.getLogger("iesa.ai_hat")


class AIHatManager:
    """
    Stub manager for the Raspberry Pi AI HAT+ (Hailo-8L).

    Provides ``start()`` / ``stop()`` lifecycle hooks compatible with
    :class:`SystemManager`, and a ``health()`` method for diagnostics.
    """

    def __init__(self) -> None:
        self._dummy: bool = False
        self._running: bool = False
        self._enabled: bool = settings.AI_HAT_ENABLED
        self._device_path: str = settings.AI_HAT_DEVICE
        self._sample_rate: int = settings.SPEECH_SAMPLE_RATE
        self._language: str = settings.SPEECH_LANGUAGE

        if not self._enabled:
            self._dummy = True
            log.info("AI HAT+ disabled by configuration (AI_HAT_ENABLED=false)")
        elif not Path(self._device_path).exists():
            self._dummy = True
            log.warning(
                "AI HAT+ not found at %s – using dummy mode",
                self._device_path,
            )
        else:
            log.info(
                "AI HAT+ detected at %s (sample_rate=%d, lang=%s)",
                self._device_path,
                self._sample_rate,
                self._language,
            )

    # ── Lifecycle (called by SystemManager) ──────────────────────────

    def start(self) -> None:
        """Initialise the Hailo runtime (stub – no model loaded yet)."""
        self._running = True
        if self._dummy:
            log.info("[AI HAT+] Started (dummy mode – no inference available)")
        else:
            log.info(
                "[AI HAT+] Started (device=%s, sample_rate=%d, lang=%s)",
                self._device_path,
                self._sample_rate,
                self._language,
            )

    def stop(self) -> None:
        """Release the Hailo runtime resources."""
        self._running = False
        log.info("[AI HAT+] Stopped")

    # ── Public API (stubs for later stages) ──────────────────────────

    def is_speech_available(self) -> bool:
        """
        Check whether speech recognition is ready.

        Returns:
            ``False`` for now.  Will return ``True`` once the speech
            model is loaded in a later stage.
        """
        return not self._dummy and self._running

    def is_voice_id_available(self) -> bool:
        """
        Check whether voice identification is ready.

        Returns:
            ``False`` for now.  Will return ``True`` once the voice
            embedding model is loaded in a later stage.
        """
        return not self._dummy and self._running

    # ── Diagnostics ──────────────────────────────────────────────────

    @property
    def is_dummy(self) -> bool:
        """``True`` when running without the real AI HAT+ hardware."""
        return self._dummy

    @property
    def is_running(self) -> bool:
        """``True`` when the AI HAT+ manager has been started."""
        return self._running

    @property
    def is_available(self) -> bool:
        """``True`` when real hardware is present and the manager is running."""
        return not self._dummy and self._running

    def health(self) -> str:
        """Return a short health-check string."""
        if not self._enabled:
            return "disabled"
        mode = "dummy" if self._dummy else "hardware"
        state = "running" if self._running else "stopped"
        return f"ok ({mode}, {state})"
