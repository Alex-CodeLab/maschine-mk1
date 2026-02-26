#!/usr/bin/env python3
"""
Maschine MK1 LED Control via cablpy
Reusable library for controlling Maschine MK1 LEDs using the cabl library.
"""

import os
import sys

_pkg_dir = os.path.dirname(os.path.abspath(__file__))
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)

os.environ.setdefault("LD_LIBRARY_PATH", "/usr/lib/x86_64-linux-gnu:/usr/local/lib")

import cablpy  # noqa: E402 - needs to be in path

PAD_COUNT = 16
GROUP_COUNT = 8

BUTTON_NAME_TO_ENUM = {
    # Top row buttons (direct button enum - these work for LED too)
    "Control": cablpy.Button.Control,
    "Step": cablpy.Button.Step,
    "Browse": cablpy.Button.Browse,
    "Sampling": cablpy.Button.Sampling,
    # Display buttons (above the screens)
    "DisplayButton1": cablpy.Button.DisplayButton1,
    "DisplayButton2": cablpy.Button.DisplayButton2,
    "DisplayButton3": cablpy.Button.DisplayButton3,
    "DisplayButton4": cablpy.Button.DisplayButton4,
    "DisplayButton5": cablpy.Button.DisplayButton5,
    "DisplayButton6": cablpy.Button.DisplayButton6,
    "DisplayButton7": cablpy.Button.DisplayButton7,
    "DisplayButton8": cablpy.Button.DisplayButton8,
    # Function buttons
    "PadMode": cablpy.Button.PadMode,
    "Scene": cablpy.Button.Scene,
    "Pattern": cablpy.Button.Pattern,
    "Navigate": cablpy.Button.Navigate,
    "Duplicate": cablpy.Button.Duplicate,
    "Select": cablpy.Button.Select,
    "Solo": cablpy.Button.Solo,
    "Mute": cablpy.Button.Mute,
    # Transport buttons
    "Grid": cablpy.Button.Grid,
    "Play": cablpy.Button.Play,
    "Rec": cablpy.Button.Rec,
    "Erase": cablpy.Button.Erase,
    "Shift": cablpy.Button.Shift,
    "Loop": cablpy.Button.Loop,
    "TransportRight": cablpy.Button.TransportRight,
    "TransportLeft": cablpy.Button.TransportLeft,
    # Right side buttons
    "AutoWrite": cablpy.Button.AutoWrite,
    "Snap": cablpy.Button.Snap,
    "BrowseRight": cablpy.Button.BrowseRight,
    "BrowseLeft": cablpy.Button.BrowseLeft,
    "NoteRepeat": cablpy.Button.NoteRepeat,
    # Group buttons
    "GroupA": cablpy.Button.GroupA,
    "GroupB": cablpy.Button.GroupB,
    "GroupC": cablpy.Button.GroupC,
    "GroupD": cablpy.Button.GroupD,
    "GroupE": cablpy.Button.GroupE,
    "GroupF": cablpy.Button.GroupF,
    "GroupG": cablpy.Button.GroupG,
    "GroupH": cablpy.Button.GroupH,
}

BUTTON_ALIASES = {
    # Group aliases (number and letter)
    "Group A": cablpy.Button.GroupA,
    "Group B": cablpy.Button.GroupB,
    "Group C": cablpy.Button.GroupC,
    "Group D": cablpy.Button.GroupD,
    "Group E": cablpy.Button.GroupE,
    "Group F": cablpy.Button.GroupF,
    "Group G": cablpy.Button.GroupG,
    "Group H": cablpy.Button.GroupH,
    "Group 1": cablpy.Button.GroupA,
    "Group 2": cablpy.Button.GroupB,
    "Group 3": cablpy.Button.GroupC,
    "Group 4": cablpy.Button.GroupD,
    "Group 5": cablpy.Button.GroupE,
    "Group 6": cablpy.Button.GroupF,
    "Group 7": cablpy.Button.GroupG,
    "Group 8": cablpy.Button.GroupH,
}

BUTTON_ALIASES = {
    # Groups (A-H mapped to Pad17-24)
    "Group A": cablpy.Button.Pad17,
    "Group B": cablpy.Button.Pad18,
    "Group C": cablpy.Button.Pad19,
    "Group D": cablpy.Button.Pad20,
    "Group E": cablpy.Button.Pad21,
    "Group F": cablpy.Button.Pad22,
    "Group G": cablpy.Button.Pad23,
    "Group H": cablpy.Button.Pad24,
    "Group 1": cablpy.Button.Pad17,
    "Group 2": cablpy.Button.Pad18,
    "Group 3": cablpy.Button.Pad19,
    "Group 4": cablpy.Button.Pad20,
    "Group 5": cablpy.Button.Pad21,
    "Group 6": cablpy.Button.Pad22,
    "Group 7": cablpy.Button.Pad23,
    "Group 8": cablpy.Button.Pad24,
}


class MaschineLED:
    def __init__(self):
        self._client = None
        self._display0 = None
        self._display1 = None
        self._connected = False

    @property
    def display(self):
        """Get primary display object (Display0)."""
        return self._display0

    @property
    def display1(self):
        """Get secondary display object (Display1)."""
        return self._display1

    @property
    def num_displays(self):
        """Number of displays available."""
        if self._client:
            return self._client.numDisplays()
        return 0

    def init(self):
        """Initialize connection to Maschine controller."""
        if self._connected:
            return True

        self._client = cablpy.MaschineClient()
        self._client.init()

        if self._client.isConnected():
            self._connected = True
            if self._client.numDisplays() > 0:
                self._display0 = self._client.getDisplay(0)
            if self._client.numDisplays() > 1:
                self._display1 = self._client.getDisplay(1)
            return True

        self._client = None
        return False

    def is_connected(self):
        """Check if Maschine is connected."""
        return self._connected

    def close(self):
        """Close connection."""
        self._client = None
        self._display = None
        self._connected = False

    def set_pad_led(self, pad, brightness):
        """Set pad LED (0-15, or 1-16). Brightness: 0-255."""
        if self._client is None:
            return False

        if pad < 0 or pad >= PAD_COUNT:
            return False

        brightness = max(0, min(255, int(brightness)))
        self._client.setKeyLed(pad, cablpy.Color(brightness))
        return True

    def set_button_led(self, button_name, brightness):
        """Set button LED by name. Brightness: 0-255."""
        if self._client is None:
            return False

        button_name = button_name.strip()
        brightness = max(0, min(255, int(brightness)))

        if button_name in BUTTON_ALIASES:
            btn_enum = BUTTON_ALIASES[button_name]
            self._client.setButtonLed(btn_enum, cablpy.Color(brightness))
            return True

        if button_name not in BUTTON_NAME_TO_ENUM:
            return False

        btn_enum = BUTTON_NAME_TO_ENUM[button_name]
        self._client.setButtonLed(btn_enum, cablpy.Color(brightness))
        return True

        if button_name not in BUTTON_NAME_TO_ENUM:
            return False

        btn_enum = BUTTON_NAME_TO_ENUM[button_name]
        self._client.setButtonLed(
            btn_enum, cablpy.Color(max(0, min(255, int(brightness))))
        )
        return True

    def set_led(self, name, brightness):
        """Set LED by name (handles both pads and buttons)."""
        name = name.strip()

        if name.lower().startswith("pad "):
            try:
                pad_num = int(name.split()[1]) - 1
                return self.set_pad_led(pad_num, brightness)
            except (ValueError, IndexError):
                return False

        try:
            pad_num = int(name) - 1
            if 0 <= pad_num < PAD_COUNT:
                return self.set_pad_led(pad_num, brightness)
        except ValueError:
            pass

        return self.set_button_led(name, brightness)

    def clear_all_leds(self):
        """Turn off all LEDs."""
        for i in range(PAD_COUNT):
            self.set_pad_led(i, 0)

        for btn_name in BUTTON_NAME_TO_ENUM:
            self.set_button_led(btn_name, 0)

    def clear_pad_leds(self):
        """Turn off all pad LEDs."""
        for i in range(PAD_COUNT):
            self.set_pad_led(i, 0)

    def clear_button_leds(self):
        """Turn off all button LEDs."""
        for btn_name in BUTTON_NAME_TO_ENUM:
            self.set_button_led(btn_name, 0)


_client = None


def get_client():
    """Get global MaschineLED instance."""
    global _client
    if _client is None:
        _client = MaschineLED()
        _client.init()
    return _client


def set_pad_led(pad, brightness):
    """Set pad LED (0-15, or 1-16). Brightness: 0-255."""
    return get_client().set_pad_led(pad, brightness)


def set_button_led(button_name, brightness):
    """Set button LED by name. Brightness: 0-255."""
    return get_client().set_button_led(button_name, brightness)


def set_led(name, brightness):
    """(handles bothSet LED by name pads and buttons)."""
    return get_client().set_led(name, brightness)


def clear_all_leds():
    """Turn off all LEDs."""
    return get_client().clear_all_leds()


def clear_pad_leds():
    """Turn off all pad LEDs."""
    return get_client().clear_pad_leds()


def clear_button_leds():
    """Turn off all button LEDs."""
    return get_client().clear_button_leds()


def is_connected():
    """Check if Maschine is connected."""
    return get_client().is_connected()


def demo():
    """Demo sequence."""
    led = MaschineLED()
    if not led.init():
        print("Failed to connect to Maschine controller")
        return False

    print("Maschine MK1 LED Demo")
    print("=" * 30)

    led.clear_all_leds()
    print("Cleared all LEDs")

    for i in range(PAD_COUNT):
        led.set_pad_led(i, 255)
        print(f"Pad {i + 1} ON")
        import time

        time.sleep(0.05)

    import time

    time.sleep(0.3)

    led.clear_all_leds()
    print("All LEDs off")

    for btn in ["Play", "Rec", "Mute", "Solo"]:
        led.set_button_led(btn, 255)
        print(f"LED {btn} ON")
        time.sleep(0.2)

    time.sleep(0.3)
    led.clear_all_leds()
    print("Demo complete")

    led.close()
    return True


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            demo()
        elif sys.argv[1] == "clear":
            led = MaschineLED()
            if led.init():
                led.clear_all_leds()
                print("Cleared all LEDs")
                led.close()
            else:
                print("Failed to connect")
        elif sys.argv[1] == "list":
            print("Available buttons:")
            for name in sorted(BUTTON_NAME_TO_ENUM.keys()):
                print(f"  {name}")
            print("\nAvailable pads: 1-16 (or 0-15)")
        else:
            name = " ".join(sys.argv[1:-1]) if len(sys.argv) > 2 else sys.argv[1]
            value = int(sys.argv[-1]) if len(sys.argv) > 2 else 255
            led = MaschineLED()
            if led.init():
                if led.set_led(name, value):
                    print(f"Set {name} to {value}")
                else:
                    print(f"Unknown LED: {name}")
                led.close()
            else:
                print("Failed to connect")
    else:
        print("Usage:")
        print("  python led_control.py <name> [value]")
        print("  python led_control.py clear")
        print("  python led_control.py list")
        print("  python led_control.py demo")
        print()
        print("Examples:")
        print("  python led_control.py Pad 1 255")
        print("  python led_control.py Play 128")
        print("  python led_control.py 1 255  # pad 1")
        print("  python led_control.py GroupA 255")
