"""
Emotion State Definitions
~~~~~~~~~~~~~~~~~~~~~~~~~
Each variant maps to a distinct set of "eyes" drawn on the OLED display.
"""

from __future__ import annotations

from enum import Enum, auto


class Emotion(Enum):
    """Emotions the robot can visually express on its OLED face."""

    SLEEPING = auto()
    IDLE = auto()
    LISTENING = auto()
    THINKING = auto()
    HAPPY = auto()
    CURIOUS = auto()
