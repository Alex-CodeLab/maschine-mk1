"""
Python library for controlling Native Instruments Maschine MK1 controller.
"""

import sys
import os

_pkg_dir = os.path.dirname(os.path.abspath(__file__))
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

os.environ.setdefault("LD_LIBRARY_PATH", "/usr/lib/x86_64-linux-gnu:/usr/local/lib")

import cablpy

from .led_control import (
    MaschineLED,
    set_pad_led,
    set_button_led,
    set_led,
    clear_all_leds,
    clear_pad_leds,
    clear_button_leds,
    is_connected,
    BUTTON_NAME_TO_ENUM,
    BUTTON_ALIASES,
)

from .startup import run_startup, run_demo

_pkg_dir = os.path.dirname(os.path.abspath(__file__))
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

_library_path = os.environ.get(
    "LD_LIBRARY_PATH", "/usr/lib/x86_64-linux-gnu:/usr/local/lib"
)
os.environ.setdefault("LD_LIBRARY_PATH", _library_path)

__all__ = [
    "MaschineLED",
    "set_pad_led",
    "set_button_led",
    "set_led",
    "clear_all_leds",
    "clear_pad_leds",
    "clear_button_leds",
    "is_connected",
    "BUTTON_NAME_TO_ENUM",
    "BUTTON_ALIASES",
    "cablpy",
    "run_startup",
    "run_demo",
]

__version__ = "0.1.0"
