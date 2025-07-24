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

## Discovering Your Device

Check what lights are connected to your system:

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

## Basic Light Control

### Colors

Control your light with RGB colors:

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

### Flash Patterns

Create attention-getting flash patterns (device-dependent):

```python
# Flash patterns work on devices with hardware flash support
try:
    light = Light.first_light()
    
    # Check if device supports flashing
    if hasattr(light, 'flash'):
        light.flash((255, 0, 0))  # Flash red (device-specific timing)
        print("Device supports hardware flash")
    else:
        # Software flash fallback
        import time
        for _ in range(3):
            light.on((255, 0, 0))
            time.sleep(0.5)
            light.off()
            time.sleep(0.5)
        print("Using software flash fallback")
        
except NoLightsFoundError:
    print("No lights available")
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
