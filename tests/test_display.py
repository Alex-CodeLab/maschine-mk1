#!/usr/bin/env python3
"""
Display Test Script for Maschine MK1
Tests screen primitives and shows animated patterns on both displays.
"""

import sys
import time
import math
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from maschine import MaschineLED


class DualDisplay:
    def __init__(self, client):
        self.d0 = None
        self.d1 = None
        if client.numDisplays() > 0:
            self.d0 = client.getDisplay(0)
        if client.numDisplays() > 1:
            self.d1 = client.getDisplay(1)

    def black(self):
        if self.d0:
            self.d0.black()
        if self.d1:
            self.d1.black()

    def setDirty(self):
        if self.d0:
            self.d0.setDirty()
        if self.d1:
            self.d1.setDirty()

    def putText(self, x, y, text, color):
        x = max(0, x)
        y = max(0, min(63, y))
        if self.d0:
            self.d0.putText(x, y, text, color)
        if self.d1:
            self.d1.putText(x, y, text, color)

    def line(self, x1, y1, x2, y2, color):
        if self.d0:
            self.d0.line(x1, y1, x2, y2, color)
        if self.d1:
            self.d1.line(x1, y1, x2, y2, color)

    def rectangle(self, x, y, w, h, color):
        if self.d0:
            self.d0.rectangle(x, y, w, h, color)
        if self.d1:
            self.d1.rectangle(x, y, w, h, color)

    def rectangleFilled(self, x, y, w, h, color):
        if self.d0:
            self.d0.rectangleFilled(x, y, w, h, color)
        if self.d1:
            self.d1.rectangleFilled(x, y, w, h, color)

    def circle(self, x, y, r, color):
        if self.d0:
            self.d0.circle(x, y, r, color)
        if self.d1:
            self.d1.circle(x, y, r, color)

    def circleFilled(self, x, y, r, color):
        if self.d0:
            self.d0.circleFilled(x, y, r, color)
        if self.d1:
            self.d1.circleFilled(x, y, r, color)

    def setPixel(self, x, y, color):
        if self.d0:
            self.d0.setPixel(x, y, color)
        if self.d1:
            self.d1.setPixel(x, y, color)

    def invert(self):
        if self.d0:
            self.d0.invert()
        if self.d1:
            self.d1.invert()


def demo_primitives(display):
    print("\n=== Testing Primitives ===")

    display.black()
    display.setDirty()

    for x in range(0, 254, 16):
        display.line(x, 10, x + 8, 10, 255)
    display.setDirty()
    print("Horizontal lines")
    time.sleep(1)

    display.black()
    for y in range(0, 64, 8):
        display.line(10, y, 10, y + 8, 255)
    display.setDirty()
    print("Vertical lines")
    time.sleep(1)

    display.black()
    for i in range(0, 200, 20):
        display.line(i, 5, i + 50, 50, 255)
    display.setDirty()
    print("Diagonal lines")
    time.sleep(1)

    display.black()
    display.rectangle(10, 10, 50, 30, 255)
    display.rectangle(80, 10, 50, 30, 0)
    display.setDirty()
    print("Rectangles")
    time.sleep(1)

    display.black()
    display.circle(40, 30, 15, 255)
    display.circle(100, 30, 12, 0)
    display.setDirty()
    print("Circles")
    time.sleep(1)


def demo_text(display):
    print("\n=== Testing Text ===")

    display.black()
    display.putText(5, 20, "HELLO WORLD", 255)
    display.putText(5, 40, "MASCHINE MK1", 255)
    display.setDirty()
    print("Text rendering")
    time.sleep(2)


def pattern_scanlines(display):
    print("\n=== Scanlines Pattern ===")

    for y in range(0, 64, 4):
        display.black()
        for ly in range(0, y + 1, 2):
            display.line(0, ly, 254, ly, 255)
        display.setDirty()
        time.sleep(0.15)


def pattern_checkerboard(display):
    print("\n=== Checkerboard Pattern ===")

    display.black()
    for y in range(0, 64, 8):
        for x in range(0, 255, 8):
            if ((x // 8) + (y // 8)) % 2 == 0:
                display.rectangleFilled(x, y, 8, 8, 255)
    display.setDirty()
    time.sleep(1)

    display.invert()
    display.setDirty()
    time.sleep(0.3)


def pattern_noise(display):
    print("\n=== Noise Pattern ===")

    import random

    for _ in range(6):
        display.black()
        for _ in range(150):
            x = random.randint(0, 254)
            y = random.randint(0, 63)
            display.setPixel(x, y, 255)
        display.setDirty()
        time.sleep(0.2)


def pattern_border(display):
    print("\n=== Border Animation ===")

    for size in range(1, 80, 4):
        display.black()
        x = max(0, 127 - size)
        y = max(0, 32 - size // 2)
        w = min(254 - x, size * 2)
        h = min(63 - y, size)
        display.rectangle(x, y, w, h, 255)
        display.setDirty()
        time.sleep(0.03)

    time.sleep(0.3)

    for size in range(80, 0, -4):
        display.black()
        x = max(0, 127 - size)
        y = max(0, 32 - size // 2)
        w = min(254 - x, size * 2)
        h = min(63 - y, size)
        display.rectangle(x, y, w, h, 255)
        display.setDirty()
        time.sleep(0.03)


def pattern_scroll_text(display):
    print("\n=== Scroll Text ===")

    text = "   MASCHINE MK1   "
    width = 255

    for offset in range(len(text) * 8 + width):
        display.black()
        x = max(0, width - offset)
        display.putText(x, 25, text, 255)
        display.setDirty()
        time.sleep(0.04)


def pattern_bouncing_ball(display):
    print("\n=== Bouncing Ball ===")

    x, y = 40, 20
    dx, dy = 4, 3

    for _ in range(50):
        display.black()
        display.circleFilled(int(x), int(y), 8, 255)
        display.setDirty()

        x += dx
        y += dy

        if x <= 10 or x >= 245:
            dx = -dx
        if y <= 10 or y >= 55:
            dy = -dy

        time.sleep(0.04)


def pattern_wave(display):
    print("\n=== Wave Pattern ===")

    for phase in range(0, 360, 8):
        display.black()
        for x in range(0, 250, 4):
            y = 32 + int(20 * math.sin(math.radians(phase + x)))
            display.setPixel(x, y, 255)
        display.setDirty()
        time.sleep(0.1)


def pattern_progress_bar(display):
    print("\n=== Progress Bar ===")

    display.black()
    display.rectangle(10, 20, 235, 24, 255)
    display.setDirty()
    time.sleep(0.5)

    for p in range(0, 225, 8):
        display.rectangleFilled(12, 22, p, 20, 255)
        display.setDirty()
        time.sleep(0.06)

    time.sleep(0.5)

    for p in range(225, 0, -8):
        display.rectangleFilled(12, 22, p, 20, 0)
        display.setDirty()
        time.sleep(0.06)


def pattern_grid(display):
    print("\n=== Grid Pattern ===")

    for offset in range(0, 16, 2):
        display.black()
        for x in range(0, 255, 16):
            display.line(x, 0, x + offset, 63, 255)
        for y in range(0, 64, 16):
            display.line(0, y, 254, y + offset, 255)
        display.setDirty()
        time.sleep(0.1)


def demo_complete(display):
    print("\n=== Complete ===")

    display.black()
    display.putText(50, 25, "DONE", 255)
    display.setDirty()
    time.sleep(1)


def main():
    led = MaschineLED()
    display = None
    try:
        if not led.init():
            print("Failed to connect to Maschine controller")
            print("Make sure the device is connected and you have USB permissions")
            return 1

        print("Maschine MK1 Display Test")
        print("=" * 40)

        client = led._client
        num_displays = client.numDisplays()
        print(f"Found {num_displays} display(s)")

        display = DualDisplay(client)
        if not display.d0:
            print("No displays available")
            led.close()
            return 1

        # Initial test - show something immediately
        display.black()
        display.putText(10, 25, "TESTING...", 255)
        display.setDirty()
        time.sleep(1)

        demo_primitives(display)
        demo_text(display)

        print("\n=== Patterns ===")
        pattern_scanlines(display)
        pattern_checkerboard(display)
        pattern_noise(display)
        pattern_wave(display)
        pattern_progress_bar(display)

        demo_complete(display)

        display.black()
        display.setDirty()
        print("\n=== Test Complete ===")

    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        if display and led.is_connected():
            display.black()
            display.setDirty()
        led.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())
