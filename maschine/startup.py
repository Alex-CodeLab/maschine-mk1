#!/usr/bin/env python3
"""
Startup sequence for Maschine MK1 controller.
Provides animated LED patterns and display welcome messages on boot.
"""


import contextlib
import time
import math


class StartupSequence:
    """Animated startup sequence for Maschine MK1."""

    def __init__(self, led):
        """Initialize with MaschineLED instance."""
        self.led = led
        self._client = led._client if led else None
        self._display0 = led._display0 if led else None
        self._display1 = led._display1 if led else None

    def run(self):
        """Run the complete startup sequence."""
        if not self.led or not self.led.is_connected():
            return

        self._clear_displays()
        self._led_welcome()
        self._display_welcome()
        self._led_cascade()
        self._display_ready()
        self._final_leds()

    def _clear_displays(self):
        """Clear both displays."""
        if self._display0:
            self._display0.black()
            self._display0.setDirty()
        if self._display1:
            self._display1.black()
            self._display1.setDirty()
        time.sleep(0.1)

    def _led_welcome(self):
        """Initial LED flash to show system is alive."""
        for i in range(16):
            self.led.set_pad_led(i, 255)
        time.sleep(0.15)
        for i in range(16):
            self.led.set_pad_led(i, 0)
        time.sleep(0.1)

    def _display_welcome(self):
        """Show welcome message on display."""
        if not self._display0:
            return

        self._display0.black()
        self._display0.putText(20, 15, "OpenCode", 255)
        self._display0.putText(20, 30, "Maschine MK1", 255)
        self._display0.setDirty()
        time.sleep(0.8)

    def _led_cascade(self):
        """Cascade wave pattern across pads."""
        for round_num in range(2):
            for i in range(16):
                self.led.set_pad_led(i, 200)
                time.sleep(0.03)
            for i in range(16):
                self.led.set_pad_led(i, 0)
                time.sleep(0.02)

            for i in range(15, -1, -1):
                self.led.set_pad_led(i, 200)
                time.sleep(0.03)
            for i in range(16):
                self.led.set_pad_led(i, 0)
                time.sleep(0.02)

    def _display_ready(self):
        """Show ready status."""
        if not self._display0:
            return

        self._display0.black()
        self._display0.putText(30, 15, "Ready", 255)
        self._display0.putText(10, 35, "Press any key", 128)
        self._display0.setDirty()
        time.sleep(0.5)

    def _final_leds(self):
        """Light up group buttons as final flourish."""
        groups = [
            "GroupA",
            "GroupB",
            "GroupC",
            "GroupD",
            "GroupE",
            "GroupF",
            "GroupG",
            "GroupH",
        ]

        for group in groups:
            with contextlib.suppress(Exception):
                self.led.set_button_led(group, 150)
                time.sleep(0.08)
        time.sleep(0.3)

        for group in groups:
            with contextlib.suppress(Exception):
                self.led.set_button_led(group, 0)


class StartupDemo:
    """Quick demo startup for testing."""

    def __init__(self, led):
        self.led = led

    def run(self):
        """Run quick startup animation."""
        if not self.led or not self.led.is_connected():
            return

        if self.led._display0:
            self.led._display0.black()
            self.led._display0.putText(50, 25, "STARTING", 255)
            self.led._display0.setDirty()

        for i in range(16):
            self.led.set_pad_led(i, 255)
            time.sleep(0.04)

        for i in range(16):
            self.led.set_pad_led(i, 0)
            time.sleep(0.04)


def run_startup(led):
    """Convenience function to run startup sequence."""
    sequence = StartupSequence(led)
    sequence.run()


def run_demo(led):
    """Convenience function to run quick demo."""
    demo = StartupDemo(led)
    demo.run()
