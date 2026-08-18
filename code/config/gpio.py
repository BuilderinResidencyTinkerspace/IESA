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

# ---------------------------------------------------------------------------
# USB Camera (no GPIO – connected via USB bus)
# ---------------------------------------------------------------------------
# The USB camera is enumerated as /dev/video0 (configurable in settings.py).
# No GPIO pins are required; this section is for documentation only.
USB_CAMERA_PORT: str = "USB"  # physical USB port (document when wired)

# ---------------------------------------------------------------------------
# Raspberry Pi AI HAT+ (no GPIO – connected via M.2 PCIe slot)
# ---------------------------------------------------------------------------
# The AI HAT+ (Hailo-8L) connects through the Pi 5's PCIe interface.
# It appears as /dev/hailo0 when the HailoRT driver is installed.
# No GPIO pins are required; this section is for documentation only.
AI_HAT_INTERFACE: str = "PCIe_M2"  # M.2 key M slot on Pi 5

# ---------------------------------------------------------------------------
# Audio I/O – microphone & speaker (placeholder)
# ---------------------------------------------------------------------------
# Assign real BCM pins once the mic/amp wiring is finalised.
# If using a USB microphone, no GPIO is needed.
I2S_BCLK: int | None = None    # I²S bit clock
I2S_LRCLK: int | None = None   # I²S left/right (word) clock
I2S_DATA_IN: int | None = None  # I²S data from microphone
I2S_DATA_OUT: int | None = None # I²S data to speaker/amp

