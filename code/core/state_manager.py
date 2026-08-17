"""
System State Manager
~~~~~~~~~~~~~~~~~~~~
Defines all valid system states as an Enum and provides a small state-machine
wrapper that enforces transitions and emits events on change.
"""

from __future__ import annotations

import logging
from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.event_bus import EventBus

log = logging.getLogger("iesa.state")


class SystemState(Enum):
    """All possible high-level states the robot can be in."""

    BOOTING = auto()
    INITIALIZING = auto()
    IDLE = auto()
    SLEEPING = auto()
    LISTENING = auto()
    THINKING = auto()
    RESPONDING = auto()
    MOVING = auto()
    FOLLOWING = auto()
    SAFETY_STOP = auto()
    ERROR = auto()


class StateManager:
    """
    Tracks the current system state, logs transitions, and optionally
    broadcasts ``state_changed`` events on an :class:`EventBus`.
    """

    def __init__(self, event_bus: EventBus | None = None) -> None:
        self._state = SystemState.BOOTING
        self._event_bus = event_bus
        log.info("StateManager created  (initial state: %s)", self._state.name)

    # ── Properties ───────────────────────────────────────────────────

    @property
    def state(self) -> SystemState:
        """Return the current state."""
        return self._state

    # ── Transitions ──────────────────────────────────────────────────

    def transition(self, new_state: SystemState) -> None:
        """
        Move to *new_state*, log the change, and emit an event.

        Args:
            new_state: The target :class:`SystemState`.
        """
        old = self._state
        self._state = new_state
        log.info("State transition: %s -> %s", old.name, new_state.name)

        if self._event_bus is not None:
            self._event_bus.emit(
                "state_changed",
                {"old": old, "new": new_state},
            )
