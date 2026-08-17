"""
OLED Emotive Display
~~~~~~~~~~~~~~~~~~~~
Drives an SSD1306 128x64 I2C OLED to render expressive robot eyes.

Hardware path:
    Uses ``luma.oled`` to talk to a real SSD1306 over I2C.

Fallback path:
    If the hardware is not found (ImportError, OSError, etc.) the class
    switches to *dummy mode* and prints the emotion to the console instead.
    This allows full development and testing on a desktop machine.
"""

from __future__ import annotations

import logging
from typing import Optional

from PIL import Image, ImageDraw

from config import settings
from emotion.emotion_state import Emotion

log = logging.getLogger("iesa.oled")

# Display dimensions (from settings, default 128x64)
WIDTH = settings.OLED_WIDTH
HEIGHT = settings.OLED_HEIGHT


class OLEDDisplay:
    """
    Render robot-eye emotions on an SSD1306 128x64 OLED.

    Falls back to console logging when the hardware is absent.
    """

    def __init__(self) -> None:
        self._device: Optional[object] = None
        self._dummy = False
        self._current_emotion: Optional[Emotion] = None

        try:
            from luma.core.interface.serial import i2c
            from luma.oled.device import ssd1306

            serial = i2c(port=1, address=settings.OLED_I2C_ADDRESS)
            self._device = ssd1306(serial, width=WIDTH, height=HEIGHT)
            log.info(
                "OLED hardware initialised (addr=0x%02X, %dx%d)",
                settings.OLED_I2C_ADDRESS, WIDTH, HEIGHT,
            )
        except Exception as exc:
            self._dummy = True
            log.warning("OLED hardware not available (%s) - using dummy mode", exc)

    # ── Public API ───────────────────────────────────────────────────

    def render(self, emotion: Emotion) -> Image.Image:
        """
        Draw the eyes for *emotion* and push to the display (or console).

        Args:
            emotion: The :class:`Emotion` to render.

        Returns:
            The PIL Image that was rendered (useful for testing / saving).
        """
        self._current_emotion = emotion
        image = self._draw_emotion(emotion)

        if self._dummy:
            log.info("[OLED] Emotion: %s", emotion.name)
        else:
            self._device.display(image)  # type: ignore[union-attr]
            log.debug("OLED rendered: %s", emotion.name)

        return image

    def clear(self) -> None:
        """Blank the display."""
        image = Image.new("1", (WIDTH, HEIGHT), 0)
        if not self._dummy:
            self._device.display(image)  # type: ignore[union-attr]
        log.debug("OLED cleared")

    def sleep(self) -> None:
        """Turn the OLED panel off to save power."""
        if not self._dummy:
            self._device.hide()  # type: ignore[union-attr]
        log.info("OLED entering sleep")

    def wake(self) -> None:
        """Turn the OLED panel back on."""
        if not self._dummy:
            self._device.show()  # type: ignore[union-attr]
        log.info("OLED waking up")

    @property
    def is_dummy(self) -> bool:
        """``True`` when running without real hardware."""
        return self._dummy

    @property
    def current_emotion(self) -> Optional[Emotion]:
        """The last emotion rendered, or ``None``."""
        return self._current_emotion

    def health(self) -> str:
        """Return a short health-check string."""
        mode = "dummy" if self._dummy else "hardware"
        return f"ok ({mode})"

    # ── Module lifecycle (called by SystemManager) ───────────────────

    def start(self) -> None:
        """Render the default IDLE face on startup."""
        self.render(Emotion.IDLE)

    def stop(self) -> None:
        """Clear and sleep on shutdown."""
        self.clear()
        self.sleep()

    # ── Eye rendering ────────────────────────────────────────────────

    def _draw_emotion(self, emotion: Emotion) -> Image.Image:
        """Dispatch to the correct eye-drawing method."""
        image = Image.new("1", (WIDTH, HEIGHT), 0)
        draw = ImageDraw.Draw(image)

        renderer = {
            Emotion.SLEEPING: self._draw_sleeping,
            Emotion.IDLE: self._draw_idle,
            Emotion.LISTENING: self._draw_listening,
            Emotion.THINKING: self._draw_thinking,
            Emotion.HAPPY: self._draw_happy,
            Emotion.CURIOUS: self._draw_curious,
        }.get(emotion, self._draw_idle)

        renderer(draw)
        return image

    # ── Individual emotion renderers ─────────────────────────────────
    # All coordinates are tuned for a 128x64 display.
    # Left eye centre ~ (32, 32), right eye centre ~ (96, 32).

    @staticmethod
    def _draw_sleeping(draw: ImageDraw.ImageDraw) -> None:
        """Two thin horizontal lines (closed eyes) with small 'z' marks."""
        # Left eye - horizontal line
        draw.line([(16, 32), (48, 32)], fill=1, width=2)
        # Right eye - horizontal line
        draw.line([(80, 32), (112, 32)], fill=1, width=2)

        # Small "zzz" marks above right eye
        for i, (x, y, size) in enumerate([(105, 14, 5), (112, 8, 7), (120, 2, 9)]):
            # Each 'z' is two horizontal lines connected by a diagonal
            draw.line([(x, y), (x + size, y)], fill=1, width=1)
            draw.line([(x + size, y), (x, y + size)], fill=1, width=1)
            draw.line([(x, y + size), (x + size, y + size)], fill=1, width=1)

    @staticmethod
    def _draw_idle(draw: ImageDraw.ImageDraw) -> None:
        """Two round open eyes - the default resting face."""
        # Left eye - filled circle
        draw.ellipse([(18, 18), (46, 46)], outline=1, fill=0, width=2)
        # Pupil
        draw.ellipse([(27, 27), (37, 37)], fill=1)

        # Right eye - filled circle
        draw.ellipse([(82, 18), (110, 46)], outline=1, fill=0, width=2)
        # Pupil
        draw.ellipse([(91, 27), (101, 37)], fill=1)

    @staticmethod
    def _draw_listening(draw: ImageDraw.ImageDraw) -> None:
        """Wide open eyes (larger circles) - attentive look."""
        # Left eye - large circle
        draw.ellipse([(14, 12), (50, 48)], outline=1, fill=0, width=2)
        # Larger pupil
        draw.ellipse([(26, 24), (38, 36)], fill=1)

        # Right eye - large circle
        draw.ellipse([(78, 12), (114, 48)], outline=1, fill=0, width=2)
        # Larger pupil
        draw.ellipse([(90, 24), (102, 36)], fill=1)

        # Small arcs above eyes (raised eyebrows)
        draw.arc([(18, 4), (46, 18)], start=200, end=340, fill=1, width=2)
        draw.arc([(82, 4), (110, 18)], start=200, end=340, fill=1, width=2)

    @staticmethod
    def _draw_thinking(draw: ImageDraw.ImageDraw) -> None:
        """One eye normal, one squinted; pupils looking up-right."""
        # Left eye - normal
        draw.ellipse([(18, 18), (46, 46)], outline=1, fill=0, width=2)
        # Pupil looking up-right
        draw.ellipse([(32, 20), (42, 30)], fill=1)

        # Right eye - squinted (narrower ellipse)
        draw.ellipse([(82, 24), (110, 40)], outline=1, fill=0, width=2)
        # Pupil looking up-right
        draw.ellipse([(94, 26), (104, 36)], fill=1)

        # Thinking dots (ellipsis) below right side
        for x in (90, 102, 114):
            draw.ellipse([(x, 52), (x + 4, 56)], fill=1)

    @staticmethod
    def _draw_happy(draw: ImageDraw.ImageDraw) -> None:
        """Upward-curved arcs (smiling eyes) with small sparkle marks."""
        # Left eye - happy arc (upside-down U)
        draw.arc([(18, 14), (46, 46)], start=200, end=340, fill=1, width=3)

        # Right eye - happy arc
        draw.arc([(82, 14), (110, 46)], start=200, end=340, fill=1, width=3)

        # Sparkle marks around eyes
        # Left sparkle
        draw.line([(8, 16), (14, 22)], fill=1, width=1)
        draw.line([(8, 22), (14, 16)], fill=1, width=1)
        # Right sparkle
        draw.line([(114, 16), (120, 22)], fill=1, width=1)
        draw.line([(114, 22), (120, 16)], fill=1, width=1)

    @staticmethod
    def _draw_curious(draw: ImageDraw.ImageDraw) -> None:
        """One eye larger than the other; a tilted, inquisitive look."""
        # Left eye - small
        draw.ellipse([(22, 22), (44, 44)], outline=1, fill=0, width=2)
        draw.ellipse([(29, 29), (37, 37)], fill=1)

        # Right eye - large (curious / intrigued)
        draw.ellipse([(76, 10), (116, 50)], outline=1, fill=0, width=2)
        draw.ellipse([(89, 23), (103, 37)], fill=1)

        # Raised eyebrow over the large eye
        draw.arc([(78, 2), (114, 18)], start=200, end=340, fill=1, width=2)
