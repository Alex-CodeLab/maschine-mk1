# controller

Python library for controlling the Native Instruments Maschine MK1 controller on Linux.

## Features

- Full LED control for all 16 pads + transport buttons + group buttons
- 255x64 pixel LCD display support
- Input handling for pads, buttons, knobs, and encoders
- Startup animation sequences
- MIDI support

## Installation

```bash
pip install -e .
```

## Testing

```bash
# Test LEDs
python -m tests.test_leds

# Test display
python -m tests.test_display

# Simple demo
python main.py
```

## Usage

```python
from maschine import MaschineLED, run_startup

led = MaschineLED()
led.init()

# Run startup animation
run_startup(led)

# Control LEDs
led.set_pad_led(0, 255)  # Pad 1 at full brightness
led.set_button_led("Play", 128)

led.close()
```

## Requirements

- Linux
- Python 3.13+
- Native Instruments Maschine MK1 controller
- libusb (via hidapi-libusb)

## Auto-start on device connect

Create a udev rule to automatically run the script when the Maschine MK1 is connected via USB:

1. Find the device vendor/product ID:
   ```bash
   lsusb | grep -i maschine
   ```
   The Maschine MK1 typically shows as `17cc:__` (Vendor ID: 17cc, Product ID: varies)

2. Create a udev rule file:
   ```bash
   sudo nano /etc/udev/rules.d/99-maschine.rules
   ```

3. Add the following rule (replace `17cc:____` with your device ID):
   ```
   SUBSYSTEM=="usb", ATTR{idVendor}=="17cc", ATTR{idProduct}=="____", MODE="0666", GROUP="plugdev", ACTION=="add", RUN+="/usr/bin/su -c '/projects/pushb/controller/main.py' - username"
   ```

   Or use a systemd service for better reliability:
   ```
   SUBSYSTEM=="usb", ATTR{idVendor}=="17cc", ATTR{idProduct}=="____", TAG+="systemd", ENV{SYSTEMD_WANTS}="maschine.service"
   ```

4. Create the systemd service:
   ```bash
   sudo nano /etc/systemd/system/maschine.service
   ```

   ```ini
   [Unit]
   Description=Maschine MK1 Controller
   After=local-fs.target
   
   [Service]
   Type=simple
   User=username
   WorkingDirectory=/projects/pushb/controller
   ExecStart=/usr/bin/python3 /projects/pushb/controller/main.py
   Restart=on-failure
   
   [Install]
   WantedBy=multi-user.target
   ```

5. Reload udev and enable the service:
   ```bash
   sudo udevadm control --reload-rules
   sudo systemctl daemon-reload
   sudo systemctl enable maschine.service
   ```

6. Plug in the Maschine device - the script should start automatically.

## Compatibility:
- cablpy.so was built for Linux x86-64 with Python 3.13
- It will work on any Linux x86_64 system with Python 3.13 and the required system libraries


## License

MIT
