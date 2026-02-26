#!/usr/bin/env python3
"""
Maschine MK1 Controller - Input via cabl
"""

import contextlib
import sys
import time
import os

os.environ.setdefault("LD_LIBRARY_PATH", "/usr/lib/x86_64-linux-gnu:/usr/local/lib")

from maschine import cablpy
from maschine.led_control import MaschineLED
from maschine.startup import run_startup


def set_pad_led(client, idx, brightness):
    if 0 <= idx < 16:
        client.setKeyLed(idx, cablpy.Color(brightness))


# Button names from cabl Device.h
BUTTON_NAMES = {
    0: "Control",
    1: "Step",
    2: "Browse",
    3: "Sampling",
    8: "DisplayButton1",
    9: "DisplayButton2",
    10: "DisplayButton3",
    11: "DisplayButton4",
    12: "DisplayButton5",
    13: "DisplayButton6",
    14: "DisplayButton7",
    15: "DisplayButton8",
    62: "Scene",
    63: "Pattern",
    64: "PadMode",
    68: "Duplicate",
    69: "Select",
    70: "Solo",
    71: "Mute",
    81: "GroupA",
    82: "GroupB",
    83: "GroupC",
    84: "GroupD",
    85: "GroupE",
    86: "GroupF",
    87: "GroupG",
    88: "GroupH",
    93: "Grid",
    94: "Play",
    95: "Rec",
    96: "Erase",
    97: "Shift",
}


def main():
    print("=== Maschine MK1 Controller ===", flush=True)
    print(f"cabl version: {cablpy.getVersion()}", flush=True)

    client = cablpy.MaschineClient()
    client.init()

    if not client.isConnected():
        print("Failed!", flush=True)
        return 1

    print(f"Connected: {client.isConnected()}", flush=True)

    led = MaschineLED()
    led._client = client
    led._connected = True
    if client.numDisplays() > 0:
        led._display0 = client.getDisplay(0)
    if client.numDisplays() > 1:
        led._display1 = client.getDisplay(1)

    print("Running startup sequence...", flush=True)
    run_startup(led)

    if client.numDisplays() > 0:
        display = client.getDisplay(0)
        if display:
            print(f"Display: {display.width()}x{display.height()}", flush=True)
            display.black()
            display.putText(10, 10, "Maschine MK1", 0xFF)
            display.setDirty()

    def on_button(btn, pressed, shift):
        name = BUTTON_NAMES.get(btn, f"Btn{btn}")
        state = "pressed" if pressed else "released"
        print(f"{name}: {state}", flush=True)

        # All buttons use setButtonLed
        with contextlib.suppress(Exception):
            btn_enum = cablpy.Button(btn)
            client.setButtonLed(btn_enum, cablpy.Color(255 if pressed else 0))

    def on_encoder(enc, inc, shift):
        print(f"Encoder {enc}: {'+' if inc else '-'}", flush=True)

    def on_key(key, value, shift):
        print(f"Key {key}: {value:.2f}", flush=True)
        if 0 <= key < 16:
            set_pad_led(client, key, int(value * 255))

    client.setButtonCallback(on_button)
    client.setEncoderCallback(on_encoder)
    client.setKeyCallback(on_key)

    print("Callbacks registered", flush=True)
    print("Running. Press Ctrl+C", flush=True)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExit", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
