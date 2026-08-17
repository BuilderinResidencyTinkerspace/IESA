# IESA - Intelligent Embodied Smart Assistant

A modular robot software stack for Raspberry Pi 5, built step by step.

## Current Stage

| Stage | Description | Status |
|-------|-------------|--------|
| 1 | Software Foundation | Done |
| 2 | OLED Emotive Display | Done |

## Project Structure

```
code/
  main.py                  # Entry point
  demo_oled.py             # Render all emotions & save previews
  requirements.txt         # Python dependencies
  .env.example             # Environment variable template
  config/
    settings.py            # Configuration loader (python-dotenv)
    gpio.py                # GPIO pin stubs (placeholders)
  core/
    logger.py              # Logging setup (console + rotating file)
    state_manager.py       # System state enum & state machine
    event_bus.py           # Publish-subscribe event bus
    system_manager.py      # Top-level orchestrator
  emotion/
    emotion_state.py       # Emotion enum (SLEEPING, IDLE, etc.)
    oled.py                # SSD1306 OLED renderer with dummy fallback
  tests/
    test_event_bus.py      # EventBus unit tests
    test_state_manager.py  # State enum & transition tests
    test_oled.py           # OLED rendering tests (all 6 emotions)
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

### Stage 1 - Software Foundation

- **Config** (`config/settings.py`): Loads `.env` via `python-dotenv`, exposes typed constants (`DATABASE_PATH`, `LOG_LEVEL`, `OLED_I2C_ADDRESS`, etc.).
- **Logger** (`core/logger.py`): Console + rotating file handler under `logs/`.
- **State Machine** (`core/state_manager.py`): 11-state enum (`BOOTING` -> `IDLE` -> ... -> `ERROR`). Transitions emit events via the bus.
- **Event Bus** (`core/event_bus.py`): `on(event, callback)` / `emit(event, data)` with exception-safe dispatch.
- **System Manager** (`core/system_manager.py`): Wires everything together. `startup()` walks `BOOTING -> INITIALIZING -> IDLE`. `shutdown()` tears down modules in reverse order. `health_status()` returns a diagnostic dict.

### Stage 2 - OLED Emotive Display

- **Emotions** (`emotion/emotion_state.py`): `SLEEPING`, `IDLE`, `LISTENING`, `THINKING`, `HAPPY`, `CURIOUS`.
- **OLED Renderer** (`emotion/oled.py`): Draws pixel-art eyes using Pillow for each emotion. Uses `luma.oled` on real hardware, falls back to console logging on desktop.
- **Previews**: Run `python demo_oled.py` to generate 4x-scaled PNG previews of each emotion.

## Testing

```bash
python -m pytest tests/ -v
```

39 tests covering:
- EventBus subscribe/emit/unsubscribe/clear/error isolation
- SystemState enum completeness and transition events
- OLED rendering for all 6 emotions (image size, non-blank, mode)
- Lifecycle methods (start/stop/clear/sleep)

## Hardware Notes

- **OLED**: SSD1306 128x64 I2C display at address `0x3C` (configurable via `.env`).
- **GPIO**: All motor/servo/sensor pins are stubs (`None`) in `config/gpio.py`. They will be assigned when wiring is finalised.
- **I2C**: SDA = BCM 2, SCL = BCM 3 (fixed on Pi 5).

## License

See [LICENSE](../LICENSE) in the project root.
