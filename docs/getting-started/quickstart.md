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
lights = Light.available()
print(f"Found {len(lights)} device(s)")

# Control the first light found
if lights:
    light = lights[0]
    light.on((255, 0, 0))  # Turn on red
    light.off()           # Turn off
```

## Discovering Your Device

Check what lights are connected to your system:

```python
from busylight_core import Light

# Get all available lights
lights = Light.available()

for i, light in enumerate(lights):
    print(f"Light {i}: {light.vendor} {light.name}")
    print(f"  Device ID: {light.device_id}")
    print(f"  Connection: {light.hardware.device_type}")
```

## Basic Light Control

### Colors

Control your light with RGB colors:

```python
from busylight_core import Light

light = Light.first_light()  # Get the first available light

# Basic colors (RGB tuples)
light.on((255, 0, 0))    # Red
light.on((0, 255, 0))    # Green  
light.on((0, 0, 255))    # Blue
light.on((255, 255, 0))  # Yellow
light.on((255, 0, 255))  # Magenta
light.on((0, 255, 255))  # Cyan
light.on((255, 255, 255)) # White

# Turn off
light.off()
```

### Flash Patterns

Create attention-getting flash patterns:

```python
light.flash((255, 0, 0), count=3)        # Flash red 3 times
light.flash((0, 255, 0), duration=0.5)   # Flash green with custom timing
```

## Configuration

Busylight Core can be configured using environment variables or a configuration file. See [Configuration](configuration.md) for details.

## Examples

For more detailed examples including async usage, multi-device control, and advanced features, see the [Examples](../user-guide/examples.md) page.

## Next Steps

- Learn about [Advanced Features](../user-guide/examples.md)
- Check out the [API Reference](../reference/index.md)
- Read the [Contributing Guide](../contributing.md) if you want to contribute
