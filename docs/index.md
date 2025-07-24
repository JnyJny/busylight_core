# Busylight Core for Humans

A unified Python library for controlling USB status lights (busylights) from multiple vendors.

## Overview

Busylight Core provides a consistent interface to control various USB-connected status lights, commonly used for indicating availability, meeting status, or system notifications. The library abstracts away vendor-specific protocols and provides a clean, unified API for controlling lights from 9+ different manufacturers.

## Quick Start

Install busylight_core using pip:

```bash
pip install busylight_core
```

Then use it in your Python code:

```python
from busylight_core import Light

# Find all connected lights
lights = Light.available()
print(f"Found {len(lights)} device(s)")

# Control a light
if lights:
    light = lights[0]
    light.on((255, 0, 0))  # Turn on red
    light.off()           # Turn off
```

## Features

- **Multi-Vendor Support** - Control devices from 9+ vendors (Embrava, Kuando, Luxafor, ThingM, and more)
- **Multiple Connection Types** - HID, Serial, and Bluetooth device support
- **Rich Light Control** - Colors, brightness, flash patterns, fade effects
- **Audio Capabilities** - Sound playback and mute/unmute on supported devices
- **Input Detection** - Button press handling on interactive devices
- **Multi-LED Support** - Control devices with 1-192 individual LEDs
- **Async Task Management** - Built-in support for animations and effects
- **Extensible Architecture** - Easy to add support for new devices
- **Object-Oriented API** - Clean, intuitive programming interface

## Installation

For detailed installation instructions, see [Installation](getting-started/installation.md).

## Documentation

- [Getting Started](getting-started/quickstart.md) - Quick start guide
- [Features](user-guide/advanced-features.md) - Detailed feature documentation
- [API Reference](reference/index.md) - Complete API documentation
- [Contributing](contributing.md) - How to contribute to this project

## License

This project is licensed under the Apache-2.0 license.
## Support

- [GitHub Issues](https://github.com/JnyJny/busylight_core/issues)
