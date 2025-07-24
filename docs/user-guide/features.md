# Features

Busylight Core provides functionality for controlling USB status lights programmatically.

## Device Discovery and Management

### Automatic Device Detection

Busylight Core automatically detects and recognizes supported devices:

```python
from busylight_core import Light, Hardware, NoLightsFoundError

# Low-level hardware discovery
hardware_devices = Hardware.enumerate()
print(f"Found {len(hardware_devices)} hardware devices")

# High-level light discovery
lights = Light.all_lights()
print(f"Recognized {len(lights)} busylights")
```

### Device Information

Get detailed information about connected devices:

```python
for light in Light.all_lights():
    print(f"Vendor: {light.vendor()}")
    print(f"Model: {light.name}")
    print(f"Device ID: {light.device_id}")
    print(f"Connection Type: {light.hardware.device_type}")
    print(f"USB Path: {light.hardware.path}")
```

## Color Management

### Color Format

Busylight Core uses RGB color tuples with integer values from 0-255:

```python
try:
    light = Light.first_light()
    
    # RGB tuples (0-255) - only supported format
    light.on((255, 0, 0))      # Red
    light.on((0, 255, 0))      # Green
    light.on((0, 0, 255))      # Blue
    light.on((255, 255, 0))    # Yellow
    light.on((255, 0, 255))    # Magenta
    light.on((0, 255, 255))    # Cyan
    light.on((255, 255, 255))  # White
    light.on((128, 128, 128))  # Gray (50% brightness)
    
    # Turn off
    light.off()
    
except NoLightsFoundError:
    print("No lights available")
```

## Advanced Device Features

### Multi-LED Devices

Control devices with multiple LEDs individually:

```python
from busylight_core import BlinkStick, Light

# Find multi-LED devices
multi_led_devices = []
for light in Light.all_lights():
    if hasattr(light, 'on') and 'led' in light.on.__annotations__:
        multi_led_devices.append(light)

if multi_led_devices:
    device = multi_led_devices[0]
    
    # Control individual LEDs (if supported)
    device.on((255, 0, 0), led=0)    # First LED red
    device.on((0, 255, 0), led=1)    # Second LED green
    device.on((0, 0, 255), led=2)    # Third LED blue
```

### Audio-Enabled Devices

Control devices with built-in audio:

```python
from busylight_core import Blynclight, Light

# Find audio-capable devices
audio_devices = []
for light in Light.all_lights():
    if hasattr(light, 'on') and 'sound' in light.on.__annotations__:
        audio_devices.append(light)

if audio_devices:
    device = audio_devices[0]
    
    # Control with sound (if supported)
    device.on((255, 0, 0), sound=True)      # Red with sound
    
    # Mute/unmute functions (if available)
    if hasattr(device, 'mute'):
        device.mute()
    if hasattr(device, 'unmute'):
        device.unmute()
```

### Flash Patterns

Use hardware flash capabilities:

```python
# Check for flash support
try:
    light = Light.first_light()
    
    if hasattr(light, 'flash'):
        light.flash((255, 0, 0))  # Flash red (device-specific timing)
        print("Device supports hardware flash")
    else:
        print("Device does not support hardware flash")
        
except NoLightsFoundError:
    print("No lights available")
```

### Button Input Devices

Handle button input on interactive devices:

```python
from busylight_core import MuteMe

# Find devices with button input
button_devices = []
for light in Light.all_lights():
    if hasattr(light, 'button_pressed'):
        button_devices.append(light)

if button_devices:
    device = button_devices[0]
    
    # Check button state
    if device.button_pressed():
        print("Button is currently pressed")
        device.on((255, 0, 0))  # Red when pressed
    else:
        device.on((0, 255, 0))  # Green when not pressed
```

## Asynchronous Programming

### Built-in Task Management

Every Light instance includes async task management:

```python
import asyncio
from busylight_core import Light, NoLightsFoundError

try:
    light = Light.first_light()
    
    # Define a simple async task
    async def blink_task():
        for _ in range(5):
            light.on((255, 0, 0))
            await asyncio.sleep(0.5)
            light.off()
            await asyncio.sleep(0.5)
    
    # Add the task to the light's task manager
    task = light.add_task("blink", blink_task)
    print(f"Started blink task: {task}")
    
    # Cancel specific task
    light.cancel_task("blink")
    
    # Cancel all tasks
    light.cancel_tasks()
    
except NoLightsFoundError:
    print("No lights found")
```

## Error Handling

### Exception Types

Busylight Core provides specific exceptions:

```python
from busylight_core import Light, LightUnavailableError, NoLightsFoundError

try:
    # Try to get a light
    light = Light.first_light()
    light.on((255, 0, 0))
    
except NoLightsFoundError:
    print("No busylights found. Please connect a device.")
except LightUnavailableError as error:
    print(f"Light unavailable: {error}")
except Exception as error:
    print(f"Unexpected error: {error}")
```

### Hardware Debugging

Debug hardware detection issues:

```python
import logging
from busylight_core import Light, Hardware

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Check hardware detection
hardware_devices = Hardware.enumerate()
print(f"Found {len(hardware_devices)} hardware devices:")

for hw in hardware_devices:
    print(f"  {hw.manufacturer_string} {hw.product_string}")
    print(f"    VID:PID = {hw.vendor_id:04x}:{hw.product_id:04x}")
    print(f"    Path: {hw.path}")

# Check light recognition
lights = Light.all_lights()
print(f"Recognized {len(lights)} as lights:")

for light in lights:
    print(f"  {light.vendor()} {light.name}")
    print(f"    Claimed by: {light.__class__.__name__}")
```

## Next Steps

- Learn more about the [API Reference](../reference/index.md)
- Check out device-specific capabilities in [Device Capabilities](device-capabilities.md)
- Visit the [GitHub repository](https://github.com/JnyJny/busylight_core) for the latest updates