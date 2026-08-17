"""
Publish–Subscribe Event Bus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A lightweight, synchronous event bus.  Components register callbacks with
:meth:`on` and trigger them with :meth:`emit`.

Thread safety is *not* required at this stage (single-threaded RPi app),
but could be added later with a ``threading.Lock``.
"""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import Any, Callable

log = logging.getLogger("iesa.events")

# Type alias for readability
Callback = Callable[..., Any]


class EventBus:
    """A minimal publish-subscribe event bus."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callback]] = defaultdict(list)
        log.debug("EventBus created")

    # ── Public API ───────────────────────────────────────────────────

    def on(self, event_name: str, callback: Callback) -> None:
        """
        Register *callback* to be invoked whenever *event_name* is emitted.

        Args:
            event_name: A string key (e.g. ``"state_changed"``).
            callback:   Any callable; will receive ``(data)`` as its argument.
        """
        self._listeners[event_name].append(callback)
        log.debug("Listener registered for '%s': %s", event_name, callback.__name__)

    def off(self, event_name: str, callback: Callback) -> None:
        """
        Remove a previously registered *callback* for *event_name*.

        Silently does nothing if the callback was not registered.
        """
        try:
            self._listeners[event_name].remove(callback)
            log.debug("Listener removed for '%s': %s", event_name, callback.__name__)
        except ValueError:
            pass

    def emit(self, event_name: str, data: Any = None) -> None:
        """
        Invoke every callback registered for *event_name*.

        Args:
            event_name: The event key.
            data:       Arbitrary payload forwarded to each callback.
        """
        callbacks = self._listeners.get(event_name, [])
        log.debug("Emitting '%s' to %d listener(s)", event_name, len(callbacks))
        for cb in callbacks:
            try:
                cb(data)
            except Exception:
                log.exception(
                    "Error in listener %s for event '%s'", cb.__name__, event_name
                )

    def clear(self) -> None:
        """Remove **all** listeners for every event."""
        self._listeners.clear()
        log.debug("All listeners cleared")

    # ── Introspection ────────────────────────────────────────────────

    @property
    def event_names(self) -> list[str]:
        """Return the names of all events that have at least one listener."""
        return [k for k, v in self._listeners.items() if v]
