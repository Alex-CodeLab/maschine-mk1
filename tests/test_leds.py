#!/usr/bin/env python3
"""
LED Test Script for Maschine MK1
Tests each LED and shows flashy patterns.
"""

import sys
import time
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maschine import MaschineLED
from maschine.led_control import BUTTON_NAME_TO_ENUM


def demo_pads(led):
    """Demo all 16 pads."""
    print("\n=== Testing Pads ===")
    for i in range(16):
        led.set_pad_led(i, 255)
        print(f"Pad {i + 1} ON")
        time.sleep(0.05)

    time.sleep(0.3)

    for i in range(16):
        led.set_pad_led(i, 0)

    print("All pads OFF")
    time.sleep(0.2)


def demo_buttons(led):
    """Demo all buttons."""
    print("\n=== Testing Buttons ===")
    buttons = list(BUTTON_NAME_TO_ENUM.keys())

    for btn in buttons:
        led.set_button_led(btn, 255)
        print(f"{btn} LED ON")
        time.sleep(0.15)
        led.set_button_led(btn, 0)

    print("All buttons OFF")
    time.sleep(0.2)


def pattern_wave(led):
    """Wave pattern across pads."""
    print("\n=== Wave Pattern ===")
    for _ in range(3):
        for i in range(16):
            led.set_pad_led(i, 255)
            time.sleep(0.03)
            led.set_pad_led(i, 0)

        for i in range(15, -1, -1):
            led.set_pad_led(i, 255)
            time.sleep(0.03)
            led.set_pad_led(i, 0)


def pattern_rain(led):
    """Rain drops falling."""
    print("\n=== Rain Pattern ===")
    import random

    for _ in range(30):
        pad = random.randint(0, 15)
        led.set_pad_led(pad, 255)
        time.sleep(0.05)
        led.set_pad_led(pad, 0)


def pattern_snake(led):
    """Snake pattern across all LEDs."""
    print("\n=== Snake Pattern ===")

    pads = list(range(16))
    buttons = list(BUTTON_NAME_TO_ENUM.keys())

    leds = pads + buttons[:8]

    positions = []
    for i in range(5):
        positions.extend(leds)

    for pos in positions:
        if isinstance(pos, int):
            led.set_pad_led(pos, 255)
        else:
            led.set_button_led(pos, 255)
        time.sleep(0.04)
        if isinstance(pos, int):
            led.set_pad_led(pos, 0)
        else:
            led.set_button_led(pos, 0)


def pattern_flash_all(led):
    """Flash all LEDs."""
    print("\n=== Flash All Pattern ===")

    for _ in range(5):
        for i in range(16):
            led.set_pad_led(i, 255)
        for btn in BUTTON_NAME_TO_ENUM.keys():
            led.set_button_led(btn, 255)

        time.sleep(0.2)

        for i in range(16):
            led.set_pad_led(i, 0)
        for btn in BUTTON_NAME_TO_ENUM.keys():
            led.set_button_led(btn, 0)

        time.sleep(0.1)


def pattern_bounce(led):
    """Bounce outer to inner."""
    print("\n=== Bounce Pattern ===")

    outer = [0, 1, 2, 3, 7, 11, 15, 14, 13, 12, 8, 4]
    inner = [5, 6, 9, 10]

    for _ in range(4):
        for p in outer:
            led.set_pad_led(p, 255)
        time.sleep(0.15)
        for p in outer:
            led.set_pad_led(p, 0)

        for p in inner:
            led.set_pad_led(p, 255)
        time.sleep(0.15)
        for p in inner:
            led.set_pad_led(p, 0)


def pattern_sine(led):
    """Sine wave brightness on pads."""
    print("\n=== Sine Wave Pattern ===")
    import math

    for phase in range(720):
        for i in range(16):
            brightness = int(128 + 127 * math.sin(math.radians(phase + i * 45)))
            led.set_pad_led(i, brightness)
        time.sleep(0.01)


def main():
    led = MaschineLED()
    if not led.init():
        print("Failed to connect to Maschine controller")
        print("Make sure the device is connected and you have USB permissions")
        return 1

    print("Maschine MK1 LED Test")
    print("=" * 40)

    led.clear_all_leds()
    time.sleep(0.3)

    demo_pads(led)
    demo_buttons(led)

    print("\n=== Flashy Patterns ===")
    pattern_wave(led)
    pattern_rain(led)
    pattern_snake(led)
    pattern_bounce(led)
    pattern_flash_all(led)
    pattern_sine(led)

    led.clear_all_leds()
    print("\n=== Test Complete ===")

    led.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
