#!/usr/bin/env python3
"""
OLED Emotion Demo
~~~~~~~~~~~~~~~~~
Renders every emotion and saves preview images to ``previews/``.
On real hardware, each emotion is also shown on the OLED for 2 seconds.
"""

from __future__ import annotations

import time
from pathlib import Path

from emotion.emotion_state import Emotion
from emotion.oled import OLEDDisplay


def main() -> None:
    display = OLEDDisplay()

    preview_dir = Path(__file__).parent / "previews"
    preview_dir.mkdir(exist_ok=True)

    print(f"OLED mode: {'DUMMY (no hardware)' if display.is_dummy else 'HARDWARE'}")
    print(f"Saving previews to: {preview_dir}\n")

    for emotion in Emotion:
        print(f"  Rendering: {emotion.name} ...", end=" ")
        img = display.render(emotion)

        # Save a scaled-up PNG for easy viewing (4x scale)
        preview = img.resize((128 * 4, 64 * 4), resample=0)  # nearest-neighbour
        path = preview_dir / f"{emotion.name.lower()}.png"
        preview.save(path)
        print(f"saved to {path}")

        if not display.is_dummy:
            time.sleep(2)

    print("\nDone!  Check the previews/ folder for rendered images.")
    display.clear()


if __name__ == "__main__":
    main()
