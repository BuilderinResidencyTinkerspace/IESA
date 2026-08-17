#!/usr/bin/env python3
"""
IESA - main entry point
~~~~~~~~~~~~~~~~~~~~~~~~
Creates the SystemManager, registers subsystems, starts the robot software,
and waits for a keyboard interrupt before shutting down cleanly.
"""

from __future__ import annotations

import sys

from core.system_manager import SystemManager
from emotion.oled import OLEDDisplay


def main() -> None:
    """Boot IESA and block until Ctrl+C."""
    manager = SystemManager()

    # ── Register subsystems ──────────────────────────────────────
    oled = OLEDDisplay()
    manager.register_module("oled", oled)

    try:
        manager.startup()
        status = manager.health_status()
        print(f"\nIESA running, state: {status['state']}")
        print(f"    modules: {status['modules']}")
        print("    Press Ctrl+C to stop.\n")

        # Block until the user presses Ctrl+C
        while True:
            pass

    except KeyboardInterrupt:
        print("\n⏎  Interrupt received – shutting down …")

    except Exception as exc:
        print(f"\n❌  Unexpected error: {exc}", file=sys.stderr)

    finally:
        manager.shutdown()


if __name__ == "__main__":
    main()
