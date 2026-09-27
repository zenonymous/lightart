"""Relay for the LED power supply (Raspberry Pi GPIO, BCM numbering).

It does the same as ``gpio/gpio_on.py`` / ``gpio_off.py``: HIGH = power on.
"Off" drives the pin LOW explicitly, where the original fell back to a
floating input (``GPIO.cleanup()``). That is the same state for an
active-high relay module, but LOW doesn't depend on the pin's pull-down.
"""

from __future__ import annotations

DEFAULT_PIN = 23


def set_power(on: bool, pin: int = DEFAULT_PIN) -> None:
    try:
        import RPi.GPIO as GPIO  # type: ignore[import-not-found]
    except ImportError as exc:  # not on a Pi
        raise SystemExit(f"RPi.GPIO is not available ({exc}); run this on the Raspberry Pi") from exc
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH if on else GPIO.LOW)
    # No GPIO.cleanup(): that would turn the pin into an input and could drop the relay.
