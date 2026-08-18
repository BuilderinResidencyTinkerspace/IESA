"""
USB Camera Manager (Stub)
~~~~~~~~~~~~~~~~~~~~~~~~~
Manages the USB camera connected to the Raspberry Pi 5.  Used for video
input, face recognition, and visual interaction tracking.

Hardware path:
    Detects the camera at the device path configured in settings
    (default ``/dev/video0``).

Fallback path:
    If the camera device is not found, switches to *dummy mode* and logs
    actions to the console.  This allows development and testing on any
    machine without a camera attached.

.. note::
    Actual frame capture (OpenCV) will be added in a later stage.
    This stub provides the lifecycle hooks and health interface so the
    SystemManager can register it now.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from config import settings

log = logging.getLogger("iesa.camera")


class CameraManager:
    """
    Stub manager for the USB camera.

    Provides ``start()`` / ``stop()`` lifecycle hooks compatible with
    :class:`SystemManager`, and a ``health()`` method for diagnostics.
    """

    def __init__(self) -> None:
        self._dummy: bool = False
        self._running: bool = False
        self._device_path: str = settings.CAMERA_DEVICE
        self._resolution: tuple[int, int] = (settings.CAMERA_WIDTH, settings.CAMERA_HEIGHT)
        self._fps: int = settings.CAMERA_FPS

        # Probe for the camera device
        if not Path(self._device_path).exists():
            self._dummy = True
            log.warning(
                "USB camera not found at %s – using dummy mode",
                self._device_path,
            )
        else:
            log.info(
                "USB camera detected at %s (%dx%d @ %d fps)",
                self._device_path,
                self._resolution[0],
                self._resolution[1],
                self._fps,
            )

    # ── Lifecycle (called by SystemManager) ──────────────────────────

    def start(self) -> None:
        """Open the camera device (stub – does not capture yet)."""
        self._running = True
        if self._dummy:
            log.info("[Camera] Started (dummy mode – no frames captured)")
        else:
            log.info(
                "[Camera] Started on %s (%dx%d @ %d fps)",
                self._device_path,
                self._resolution[0],
                self._resolution[1],
                self._fps,
            )

    def stop(self) -> None:
        """Release the camera device."""
        self._running = False
        log.info("[Camera] Stopped")

    # ── Public API (stubs for later stages) ──────────────────────────

    def capture_frame(self) -> Optional[object]:
        """
        Capture a single frame from the camera.

        Returns:
            ``None`` for now.  Will return a NumPy array (BGR image)
            once OpenCV integration is added in a later stage.
        """
        if self._dummy:
            log.debug("[Camera] capture_frame() called (dummy – returning None)")
        return None

    # ── Diagnostics ──────────────────────────────────────────────────

    @property
    def is_dummy(self) -> bool:
        """``True`` when running without real camera hardware."""
        return self._dummy

    @property
    def is_running(self) -> bool:
        """``True`` when the camera has been started."""
        return self._running

    def health(self) -> str:
        """Return a short health-check string."""
        mode = "dummy" if self._dummy else "hardware"
        state = "running" if self._running else "stopped"
        return f"ok ({mode}, {state})"
