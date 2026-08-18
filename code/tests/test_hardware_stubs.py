"""
Tests for hardware.camera.CameraManager and hardware.ai_hat.AIHatManager

On a development machine without the physical hardware, both managers
fall back to dummy mode.  These tests verify that the stubs work
correctly and integrate with the SystemManager lifecycle.
"""

import pytest

from hardware.camera import CameraManager
from hardware.ai_hat import AIHatManager


# ── CameraManager ────────────────────────────────────────────────────


class TestCameraManagerDummy:
    """Verify dummy-mode behaviour on machines without a USB camera."""

    @pytest.fixture
    def camera(self):
        return CameraManager()

    def test_is_dummy_on_desktop(self, camera: CameraManager):
        # /dev/video0 won't exist on a macOS/Windows dev machine
        assert camera.is_dummy is True

    def test_health_reports_dummy(self, camera: CameraManager):
        assert "dummy" in camera.health()

    def test_start_stop_lifecycle(self, camera: CameraManager):
        assert camera.is_running is False
        camera.start()
        assert camera.is_running is True
        assert "running" in camera.health()
        camera.stop()
        assert camera.is_running is False
        assert "stopped" in camera.health()

    def test_capture_frame_returns_none(self, camera: CameraManager):
        assert camera.capture_frame() is None

    def test_health_format(self, camera: CameraManager):
        camera.start()
        health = camera.health()
        assert health == "ok (dummy, running)"
        camera.stop()
        assert camera.health() == "ok (dummy, stopped)"


# ── AIHatManager ─────────────────────────────────────────────────────


class TestAIHatManagerDummy:
    """Verify dummy-mode behaviour on machines without the AI HAT+."""

    @pytest.fixture
    def ai_hat(self):
        return AIHatManager()

    def test_is_dummy_on_desktop(self, ai_hat: AIHatManager):
        # /dev/hailo0 won't exist on a dev machine
        assert ai_hat.is_dummy is True

    def test_health_reports_dummy(self, ai_hat: AIHatManager):
        assert "dummy" in ai_hat.health()

    def test_start_stop_lifecycle(self, ai_hat: AIHatManager):
        assert ai_hat.is_running is False
        ai_hat.start()
        assert ai_hat.is_running is True
        assert "running" in ai_hat.health()
        ai_hat.stop()
        assert ai_hat.is_running is False
        assert "stopped" in ai_hat.health()

    def test_is_available_false_in_dummy(self, ai_hat: AIHatManager):
        ai_hat.start()
        # Even when started, is_available should be False in dummy mode
        assert ai_hat.is_available is False

    def test_speech_not_available_in_dummy(self, ai_hat: AIHatManager):
        ai_hat.start()
        assert ai_hat.is_speech_available() is False

    def test_voice_id_not_available_in_dummy(self, ai_hat: AIHatManager):
        ai_hat.start()
        assert ai_hat.is_voice_id_available() is False

    def test_health_format(self, ai_hat: AIHatManager):
        ai_hat.start()
        assert ai_hat.health() == "ok (dummy, running)"
        ai_hat.stop()
        assert ai_hat.health() == "ok (dummy, stopped)"
