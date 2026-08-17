"""
Tests for emotion.oled.OLEDDisplay

On a machine without an SSD1306, the display falls back to dummy mode.
These tests verify that every emotion renders without error and produces
a valid PIL Image of the correct size.
"""

import pytest
from PIL import Image

from emotion.emotion_state import Emotion
from emotion.oled import OLEDDisplay


@pytest.fixture
def display():
    """Create an OLEDDisplay (will be in dummy mode on dev machines)."""
    return OLEDDisplay()


class TestOLEDFallback:
    """Verify dummy-mode behaviour on machines without hardware."""

    def test_is_dummy_on_desktop(self, display: OLEDDisplay):
        # On a desktop without I2C, this should always be True
        assert display.is_dummy is True

    def test_health_reports_dummy(self, display: OLEDDisplay):
        assert "dummy" in display.health()


class TestEmotionRendering:
    """Each emotion should produce a 128x64 monochrome image."""

    @pytest.mark.parametrize("emotion", list(Emotion))
    def test_render_returns_valid_image(self, display: OLEDDisplay, emotion: Emotion):
        img = display.render(emotion)
        assert isinstance(img, Image.Image)
        assert img.size == (128, 64)
        assert img.mode == "1"  # monochrome

    @pytest.mark.parametrize("emotion", list(Emotion))
    def test_render_produces_non_blank_image(self, display: OLEDDisplay, emotion: Emotion):
        """Every emotion should draw *something* (not a fully black image)."""
        img = display.render(emotion)
        # At least some pixels should be white
        assert img.getbbox() is not None, f"{emotion.name} rendered a blank image"

    @pytest.mark.parametrize("emotion", list(Emotion))
    def test_current_emotion_tracks(self, display: OLEDDisplay, emotion: Emotion):
        display.render(emotion)
        assert display.current_emotion == emotion


class TestClearAndSleep:
    """Verify clear() and sleep()/wake() don't crash in dummy mode."""

    def test_clear(self, display: OLEDDisplay):
        display.clear()  # should not raise

    def test_sleep_and_wake(self, display: OLEDDisplay):
        display.sleep()
        display.wake()


class TestLifecycle:
    """start() and stop() integration."""

    def test_start_renders_idle(self, display: OLEDDisplay):
        display.start()
        assert display.current_emotion == Emotion.IDLE

    def test_stop_does_not_crash(self, display: OLEDDisplay):
        display.stop()  # clear + sleep
