# Quick Start

This guide will help you get started with Busylight Core quickly.

## Installation

First, install busylight_core using pip:

```bash
pip install busylight_core
```

Or with uv:

```bash
uv add busylight_core
```

## Basic Usage

After [installing](installation.md) busylight_core, you can start controlling lights in your Python code:

**Option 1: Any compatible device (recommended for simple use cases)**
```python
from busylight_core import Light

# Find all connected lights
lights = Light.all_lights()
print(f"Found {len(lights)} device(s)")

# Control the first light found
if lights:
    light = lights[0]
    light.on((255, 0, 0))  # Turn on red
    light.off()           # Turn off
else:
    print("No compatible lights found. Check your device connection.")
```

**Option 2: Vendor-specific devices (recommended for production)**
```python
from busylight_core import EmbravaLights, LuxaforLights

# Get devices from specific vendors
embrava_lights = EmbravaLights.all_lights()
luxafor_lights = LuxaforLights.all_lights()

# Use Embrava devices if available
if embrava_lights:
    light = embrava_lights[0]
    light.on((255, 0, 0), sound=True)  # Red with audio (Embrava-specific)
    light.dim()  # Reduce brightness
elif luxafor_lights:
    light = luxafor_lights[0] 
    light.on((255, 0, 0))  # Red light
    # Check for multi-LED support
    if hasattr(light, 'on') and 'led' in light.on.__annotations__:
        for i in range(6):  # Flag has 6 LEDs
            light.on((0, 255, 0), led=i)  # Green on each LED
else:
    print("No Embrava or Luxafor devices found")
```

## Discovering Your Device

**Check all connected devices:**
```python
from busylight_core import Light

# Get all available lights
lights = Light.all_lights()

if lights:
    for i, light in enumerate(lights):
        print(f"Light {i}: {light.vendor()} {light.name}")
        print(f"  Device ID: {light.device_id}")
        print(f"  Hardware: {light.hardware.manufacturer_string}")
else:
    print("No lights found. Try:")
    print("1. Check USB connection")
    print("2. On Linux, ensure udev rules are configured")
    print("3. Try running with sudo (not recommended for production)")
```

**Check devices by vendor:**
```python
from busylight_core import (
    EmbravaLights, KuandoLights, LuxaforLights, 
    AgileInnovativeLights, ThingMLights, MuteMeLights
)

# Check what vendors you have connected
vendors = [
    ("Embrava", EmbravaLights),
    ("Kuando", KuandoLights), 
    ("Luxafor", LuxaforLights),
    ("BlinkStick", AgileInnovativeLights),
    ("ThingM", ThingMLights),
    ("MuteMe", MuteMeLights),
]

for vendor_name, vendor_class in vendors:
    devices = vendor_class.all_lights()
    if devices:
        print(f"{vendor_name}: {len(devices)} device(s)")
        for device in devices:
            print(f"  - {device.name}")
    else:
        print(f"{vendor_name}: No devices found")
```

## Basic Light Control

### Colors

**Universal approach (works with any device):**
```python
from busylight_core import Light, NoLightsFoundError

try:
    light = Light.first_light()  # Get the first available light
    
    # Basic colors (RGB tuples, values 0-255)
    light.on((255, 0, 0))    # Red
    light.on((0, 255, 0))    # Green  
    light.on((0, 0, 255))    # Blue
    light.on((255, 255, 0))  # Yellow
    light.on((255, 0, 255))  # Magenta
    light.on((0, 255, 255))  # Cyan
    light.on((255, 255, 255)) # White
    
    # Turn off
    light.off()
    
except NoLightsFoundError:
    print("No lights available")
```

**Vendor-specific approach (recommended for specific features):**
```python
from busylight_core import EmbravaLights, KuandoLights, NoLightsFoundError

# Embrava devices with audio
try:
    light = EmbravaLights.first_light()
    light.on((255, 0, 0), sound=True)  # Red with sound
    light.dim()  # Reduce brightness
    light.bright()  # Restore brightness
except NoLightsFoundError:
    print("No Embrava devices found")

# Kuando devices with keepalive
try:
    light = KuandoLights.first_light()
    light.on((0, 255, 0))
    light.keepalive()  # Required for Kuando devices
except NoLightsFoundError:
    print("No Kuando devices found")
```

### Flash Patterns

**Universal approach with fallback:**
```python
from busylight_core import Light, NoLightsFoundError
import time

# Flash patterns work on devices with hardware flash support
try:
    light = Light.first_light()
    
    # Check if device supports flashing
    if hasattr(light, 'flash'):
        light.flash((255, 0, 0))  # Flash red (device-specific timing)
        print("Device supports hardware flash")
    else:
        # Software flash fallback
        for _ in range(3):
            light.on((255, 0, 0))
            time.sleep(0.5)
            light.off()
            time.sleep(0.5)
        print("Using software flash fallback")
        
except NoLightsFoundError:
    print("No lights available")
```

**Vendor-specific flash patterns:**
```python
from busylight_core import EmbravaLights, KuandoLights

# Embrava devices have configurable flash speeds
try:
    light = EmbravaLights.first_light()
    light.flash((255, 165, 0))  # Orange flash with default speed
    # Some Embrava devices support speed control
    # light.flash((255, 0, 0), speed="fast")
except NoLightsFoundError:
    print("No Embrava devices found")

# Kuando devices have built-in flash patterns  
try:
    light = KuandoLights.first_light()
    light.flash((255, 0, 255))  # Magenta flash
    light.keepalive()  # Don't forget keepalive for Kuando
except NoLightsFoundError:
    print("No Kuando devices found")
```


## Device Compatibility

Different devices have different capabilities. Use the [Device Capabilities](../user-guide/device-capabilities.md) guide to understand what features your hardware supports.

## Configuration

Busylight Core can be configured using environment variables or a configuration file. See [Configuration](configuration.md) for details.

## Next Steps

- Learn about specific device capabilities: [Device Capabilities](../user-guide/device-capabilities.md)
- See comprehensive examples: [Examples](../user-guide/examples.md) 
- Check out the [API Reference](../reference/index.md)
- Read the [Contributing Guide](../contributing.md) if you want to contribute
