"""
GPIO Pin Definitions (Stubs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Placeholder pin assignments for the Raspberry Pi 5.  These will be replaced
with real BCM numbers once the hardware wiring is finalised.

Convention:
    - All values use BCM numbering.
    - Set a pin to ``None`` to indicate "not yet assigned".
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Motor driver (placeholder)
# ---------------------------------------------------------------------------
MOTOR_LEFT_FWD: int | None = None
MOTOR_LEFT_BWD: int | None = None
MOTOR_RIGHT_FWD: int | None = None
MOTOR_RIGHT_BWD: int | None = None
MOTOR_PWM_LEFT: int | None = None
MOTOR_PWM_RIGHT: int | None = None

# ---------------------------------------------------------------------------
# Servo (placeholder)
# ---------------------------------------------------------------------------
SERVO_PAN: int | None = None
SERVO_TILT: int | None = None

# ---------------------------------------------------------------------------
# Ultrasonic distance sensor (placeholder)
# ---------------------------------------------------------------------------
ULTRASONIC_TRIG: int | None = None
ULTRASONIC_ECHO: int | None = None

# ---------------------------------------------------------------------------
# Status LED / indicator (placeholder)
# ---------------------------------------------------------------------------
STATUS_LED: int | None = None

# ---------------------------------------------------------------------------
# I²C (used by OLED – fixed on Pi 5, listed here for documentation)
# ---------------------------------------------------------------------------
I2C_SDA: int = 2   # BCM 2 – GPIO header pin 3
I2C_SCL: int = 3   # BCM 3 – GPIO header pin 5
