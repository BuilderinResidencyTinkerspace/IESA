"""
Tests for core.event_bus.EventBus
"""

import pytest
from core.event_bus import EventBus


class TestEventBusBasics:
    """Subscribe, emit, and unsubscribe."""

    def test_listener_receives_data(self):
        bus = EventBus()
        received = []
        bus.on("ping", lambda data: received.append(data))
        bus.emit("ping", {"msg": "hello"})
        assert received == [{"msg": "hello"}]

    def test_multiple_listeners(self):
        bus = EventBus()
        calls = []
        bus.on("evt", lambda d: calls.append("a"))
        bus.on("evt", lambda d: calls.append("b"))
        bus.emit("evt")
        assert calls == ["a", "b"]

    def test_emit_without_listeners_is_safe(self):
        bus = EventBus()
        bus.emit("nonexistent")  # should not raise

    def test_off_removes_listener(self):
        bus = EventBus()
        calls = []

        def handler(data):
            calls.append(data)

        bus.on("evt", handler)
        bus.emit("evt", 1)
        bus.off("evt", handler)
        bus.emit("evt", 2)
        assert calls == [1]

    def test_off_nonexistent_is_safe(self):
        bus = EventBus()
        bus.off("evt", lambda d: None)  # should not raise

    def test_clear_removes_all(self):
        bus = EventBus()
        bus.on("a", lambda d: None)
        bus.on("b", lambda d: None)
        bus.clear()
        assert bus.event_names == []

    def test_event_names(self):
        bus = EventBus()
        bus.on("x", lambda d: None)
        bus.on("y", lambda d: None)
        names = sorted(bus.event_names)
        assert names == ["x", "y"]

    def test_listener_exception_does_not_break_others(self):
        bus = EventBus()
        results = []

        def bad_handler(data):
            raise ValueError("boom")

        def good_handler(data):
            results.append("ok")

        bus.on("evt", bad_handler)
        bus.on("evt", good_handler)
        bus.emit("evt")  # bad_handler raises, but good_handler still runs
        assert results == ["ok"]
