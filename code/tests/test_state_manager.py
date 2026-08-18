"""
Tests for core.state_manager.StateManager and SystemState transitions.
"""

import pytest
from core.event_bus import EventBus
from core.state_manager import StateManager, SystemState


class TestSystemState:
    """Verify the enum has all expected members."""

    def test_all_states_present(self):
        expected = {
            "BOOTING", "INITIALIZING", "IDLE", "SLEEPING",
            "LISTENING", "THINKING", "RESPONDING", "RECOGNIZING",
            "MOVING", "FOLLOWING", "SAFETY_STOP", "ERROR",
        }
        actual = {s.name for s in SystemState}
        assert actual == expected


class TestStateManager:
    """State transitions and event integration."""

    def test_initial_state_is_booting(self):
        sm = StateManager()
        assert sm.state == SystemState.BOOTING

    def test_transition_changes_state(self):
        sm = StateManager()
        sm.transition(SystemState.INITIALIZING)
        assert sm.state == SystemState.INITIALIZING

    def test_full_startup_sequence(self):
        sm = StateManager()
        sm.transition(SystemState.INITIALIZING)
        sm.transition(SystemState.IDLE)
        assert sm.state == SystemState.IDLE

    def test_transition_emits_event(self):
        bus = EventBus()
        sm = StateManager(event_bus=bus)
        events = []
        bus.on("state_changed", lambda data: events.append(data))

        sm.transition(SystemState.IDLE)

        assert len(events) == 1
        assert events[0]["old"] == SystemState.BOOTING
        assert events[0]["new"] == SystemState.IDLE

    def test_transition_without_bus_is_safe(self):
        sm = StateManager(event_bus=None)
        sm.transition(SystemState.ERROR)  # should not raise
        assert sm.state == SystemState.ERROR

    def test_multiple_transitions_emit_correct_events(self):
        bus = EventBus()
        sm = StateManager(event_bus=bus)
        transitions = []
        bus.on("state_changed", lambda d: transitions.append(
            (d["old"].name, d["new"].name)
        ))

        sm.transition(SystemState.INITIALIZING)
        sm.transition(SystemState.IDLE)
        sm.transition(SystemState.LISTENING)

        assert transitions == [
            ("BOOTING", "INITIALIZING"),
            ("INITIALIZING", "IDLE"),
            ("IDLE", "LISTENING"),
        ]
