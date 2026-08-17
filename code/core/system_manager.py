"""
System Manager
~~~~~~~~~~~~~~
Top-level orchestrator that wires together configuration, logging,
the event bus, and the state machine.  All subsystems (OLED, audio,
motors …) will register themselves here in later stages.
"""

from __future__ import annotations

import logging
from typing import Any

from config import settings
from core.event_bus import EventBus
from core.logger import setup_logging
from core.state_manager import StateManager, SystemState

log = logging.getLogger("iesa.system")


class SystemManager:
    """
    Central orchestrator for the IESA robot.

    Responsibilities:
        * Loads configuration.
        * Sets up logging.
        * Manages the startup / shutdown lifecycle.
        * Exposes health status for diagnostics.
    """

    def __init__(self) -> None:
        # ── Bootstrap logging first so everything else can log ───────
        self.logger = setup_logging()

        log.info("=" * 60)
        log.info("  IESA - Intelligent Embodied Smart Assistant")
        log.info("=" * 60)

        # ── Configuration ────────────────────────────────────────────
        self.config = settings.as_dict()
        log.info("Configuration loaded: %s", self.config)

        # ── Event bus ────────────────────────────────────────────────
        self.event_bus = EventBus()

        # ── State machine ────────────────────────────────────────────
        self.state_manager = StateManager(event_bus=self.event_bus)

        # ── Subsystem registry (populated by later stages) ───────────
        self._modules: dict[str, Any] = {}

    # ── Lifecycle ────────────────────────────────────────────────────

    def startup(self) -> None:
        """
        Run the startup sequence:
            BOOTING → INITIALIZING → IDLE
        """
        log.info("Starting up ...")

        # State is already BOOTING from StateManager.__init__
        self.state_manager.transition(SystemState.INITIALIZING)

        # (Future stages will initialise subsystems here)
        for name, module in self._modules.items():
            try:
                if hasattr(module, "start"):
                    module.start()
                    log.info("Module '%s' started", name)
            except Exception:
                log.exception("Failed to start module '%s'", name)

        self.state_manager.transition(SystemState.IDLE)
        log.info("Startup complete")

    def shutdown(self) -> None:
        """Gracefully stop all subsystems and clear the event bus."""
        log.info("Shutting down ...")

        # Stop modules in reverse registration order
        for name in reversed(list(self._modules)):
            try:
                module = self._modules[name]
                if hasattr(module, "stop"):
                    module.stop()
                    log.info("Module '%s' stopped", name)
            except Exception:
                log.exception("Error stopping module '%s'", name)

        self.event_bus.clear()
        self.state_manager.transition(SystemState.BOOTING)  # back to initial
        log.info("Shutdown complete")

    # ── Module registration ──────────────────────────────────────────

    def register_module(self, name: str, module: Any) -> None:
        """
        Register a subsystem so it participates in startup/shutdown.

        Args:
            name:   Human-readable module name (e.g. ``"oled"``).
            module: Any object; if it has ``start()`` / ``stop()`` methods
                    they will be called during the lifecycle.
        """
        self._modules[name] = module
        log.info("Module registered: %s", name)

    # ── Diagnostics ──────────────────────────────────────────────────

    def health_status(self) -> dict:
        """
        Return a snapshot of the system health.

        Returns:
            A dict containing the current state and per-module status.
        """
        module_health: dict[str, str] = {}
        for name, module in self._modules.items():
            if hasattr(module, "health"):
                try:
                    module_health[name] = module.health()
                except Exception:
                    module_health[name] = "error"
            else:
                module_health[name] = "registered"

        return {
            "state": self.state_manager.state.name,
            "modules": module_health,
        }
