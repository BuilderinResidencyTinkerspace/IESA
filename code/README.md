# IESA - Intelligent Embodied Smart Assistant

A modular robot software stack for Raspberry Pi 5, built step by step.

## Current Stage

| Stage | Description | Status |
|-------|-------------|--------|
| 1 | Software Foundation | ✅ Done |
| 2 | OLED Emotive Display | ✅ Done |

## Hardware Overview

| Component | Interface | Device Path | Notes |
|-----------|-----------|-------------|-------|
| SSD1306 OLED 128×64 | I²C | — | Address `0x3C` (BCM 2/3) |
| USB Camera | USB | `/dev/video0` | Video input, face recognition |
| AI HAT+ (Hailo-8L) | PCIe M.2 | `/dev/hailo0` | Speech & voice recognition |
| Microphone | TBD | — | USB or I²S (placeholder) |
| Speaker / Amp | TBD | — | USB, I²S, or 3.5mm (placeholder) |

## Project Structure

```
code/
  main.py                  # Entry point
  demo_oled.py             # Render all emotions & save previews
  requirements.txt         # Python dependencies
  .env.example             # Environment variable template
  config/
    settings.py            # Configuration loader (python-dotenv)
    gpio.py                # GPIO pin stubs & hardware bus docs
  core/
    logger.py              # Logging setup (console + rotating file)
    state_manager.py       # System state enum & state machine
    event_bus.py           # Publish-subscribe event bus
    system_manager.py      # Top-level orchestrator
  emotion/
    emotion_state.py       # Emotion enum (SLEEPING, IDLE, etc.)
    oled.py                # SSD1306 OLED renderer with dummy fallback
  hardware/
    camera.py              # USB camera manager (stub, dummy fallback)
    ai_hat.py              # AI HAT+ manager (stub, dummy fallback)
  tests/
    test_event_bus.py      # EventBus unit tests
    test_state_manager.py  # State enum & transition tests
    test_oled.py           # OLED rendering tests (all 6 emotions)
    test_hardware_stubs.py # Camera & AI HAT+ stub tests
  previews/                # Generated emotion preview images
```

## Quick Start

```bash
cd code

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux / Pi)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment config (optional)
cp .env.example .env

# Run IESA
python main.py

# Run tests
python -m pytest tests/ -v

# Generate OLED emotion previews
python demo_oled.py
```

## How It Works

### Stage 1 — Software Foundation

- **Config** (`config/settings.py`): Loads `.env` via `python-dotenv`, exposes typed constants (`DATABASE_PATH`, `LOG_LEVEL`, `OLED_I2C_ADDRESS`, `CAMERA_DEVICE`, `AI_HAT_DEVICE`, etc.).
- **Logger** (`core/logger.py`): Console + rotating file handler under `logs/`.
- **State Machine** (`core/state_manager.py`): 12-state enum (`BOOTING` → `IDLE` → … → `ERROR`), including `RECOGNIZING` for AI HAT+ inference. Transitions emit events via the bus.
- **Event Bus** (`core/event_bus.py`): `on(event, callback)` / `emit(event, data)` with exception-safe dispatch.
- **System Manager** (`core/system_manager.py`): Wires everything together. `startup()` walks `BOOTING → INITIALIZING → IDLE`. `shutdown()` tears down modules in reverse order. `health_status()` returns a diagnostic dict.

### Stage 2 — OLED Emotive Display

- **Emotions** (`emotion/emotion_state.py`): `SLEEPING`, `IDLE`, `LISTENING`, `THINKING`, `HAPPY`, `CURIOUS`.
- **OLED Renderer** (`emotion/oled.py`): Draws pixel-art eyes using Pillow for each emotion. Uses `luma.oled` on real hardware, falls back to console logging on desktop.
- **Previews**: Run `python demo_oled.py` to generate 4×-scaled PNG previews of each emotion.

### Hardware Stubs

- **Camera** (`hardware/camera.py`): Detects USB camera at `/dev/video0`. Falls back to dummy mode on dev machines. Provides lifecycle hooks (`start`/`stop`) and `health()` for SystemManager. Actual frame capture (OpenCV) will be added in a later stage.
- **AI HAT+** (`hardware/ai_hat.py`): Detects Hailo-8L at `/dev/hailo0`. Falls back to dummy mode. Provides `is_speech_available()` / `is_voice_id_available()` stubs. Actual model loading (HailoRT) will be added in a later stage.

## Testing

```bash
python -m pytest tests/ -v
```

Tests cover:
- EventBus subscribe/emit/unsubscribe/clear/error isolation
- SystemState enum completeness (12 states incl. RECOGNIZING) and transition events
- OLED rendering for all 6 emotions (image size, non-blank, mode)
- OLED lifecycle methods (start/stop/clear/sleep)
- CameraManager dummy mode, lifecycle, health reporting
- AIHatManager dummy mode, lifecycle, availability checks, health reporting

## Hardware Notes

- **OLED**: SSD1306 128×64 I²C display at address `0x3C` (configurable via `.env`).
- **USB Camera**: Standard UVC camera at `/dev/video0`. Resolution and FPS configurable via `.env`.
- **AI HAT+**: Hailo-8L accelerator via PCIe M.2 slot. Requires HailoRT driver. Device path configurable via `.env`.
- **GPIO**: All motor/servo/sensor pins are stubs (`None`) in `config/gpio.py`. Audio I/O pins (I²S) are also placeholders.
- **I²C**: SDA = BCM 2, SCL = BCM 3 (fixed on Pi 5).

## License

See [LICENSE](../LICENSE) in the project root.
