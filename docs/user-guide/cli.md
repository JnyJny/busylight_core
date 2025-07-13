# Advanced Features

Busylight Core provides extensive functionality for controlling USB status lights programmatically.

## Device Discovery and Management

### Automatic Device Detection

Busylight Core automatically detects and recognizes supported devices:

```python
from busylight_core import Light, Hardware

# Low-level hardware discovery
hardware_devices = Hardware.enumerate()
print(f"Found {len(hardware_devices)} hardware devices")

# High-level light discovery
lights = Light.available()
print(f"Recognized {len(lights)} busylights")
```

### Device Information

Get detailed information about connected devices:

```python
for light in Light.available():
    print(f"Vendor: {light.vendor}")
    print(f"Model: {light.name}")
    print(f"Device ID: {light.device_id}")
    print(f"Connection Type: {light.hardware.device_type}")
    print(f"USB Path: {light.hardware.path}")
```

## Color Management

### Color Formats

Busylight Core supports multiple color formats:

```python
light = Light.first_light()

# RGB tuples (0-255)
light.on((255, 0, 0))      # Red
light.on((0, 255, 0))      # Green
light.on((0, 0, 255))      # Blue

# Hexadecimal strings
light.on("#FF0000")        # Red
light.on("#00FF00")        # Green
light.on("#0000FF")        # Blue

# Named colors (if supported)
light.on("red")
light.on("green")
light.on("blue")
```

### Color Utilities

Use built-in color utilities for advanced color manipulation:

```python
from busylight_core.mixins import ColorableMixin

# Color interpolation
start_color = (255, 0, 0)    # Red
end_color = (0, 0, 255)      # Blue
steps = 10

for i in range(steps):
    ratio = i / (steps - 1)
    interpolated = ColorableMixin.interpolate_color(start_color, end_color, ratio)
    light.on(interpolated)
    time.sleep(0.1)
```

## Advanced Device Features

### Multi-LED Devices

Control devices with multiple LEDs individually:

```python
from busylight_core import BlinkStick

blinksticks = [l for l in Light.available() if isinstance(l, BlinkStick)]
if blinksticks:
    stick = blinksticks[0]
    
    # Set individual LEDs
    for i in range(8):  # BlinkStick Strip has 8 LEDs
        color = (255 * i // 7, 0, 255 - (255 * i // 7))  # Red to blue gradient
        stick.set_led(i, color)
    
    # Set all LEDs at once
    stick.set_all((255, 255, 255))  # All white
```

### Audio-Enabled Devices

Control sound features on supported devices:

```python
from busylight_core import Blynclight

blynclights = [l for l in Light.available() if isinstance(l, Blynclight)]
if blynclights:
    blight = blynclights[0]
    
    # Play sound with light
    blight.on((255, 0, 0), sound=True)
    
    # Sound-only operations
    blight.play_sound()
    blight.mute()
    blight.unmute()
    
    # Check mute status
    if blight.is_muted():
        print("Device is muted")
```

### Button Input Devices

Handle button input on interactive devices:

```python
from busylight_core import MuteMe, Luxafor

# Find devices with button input
input_devices = []
for light in Light.available():
    if isinstance(light, (MuteMe, Luxafor)) and hasattr(light, 'button_pressed'):
        input_devices.append(light)

if input_devices:
    device = input_devices[0]
    
    # Poll button state
    while True:
        if device.button_pressed():
            device.on((255, 0, 0))  # Red when pressed
        else:
            device.on((0, 255, 0))  # Green when not pressed
        time.sleep(0.1)
```

## Asynchronous Programming

### Built-in Task Management

Every Light instance includes async task management:

```python
import asyncio
from busylight_core import Light

async def breathing_animation(light_instance):
    """Breathing effect animation"""
    while True:
        # Fade in
        for brightness in range(0, 256, 5):
            color = (brightness, 0, 0)  # Red
            light_instance.on(color)
            await asyncio.sleep(0.02)
        
        # Fade out
        for brightness in range(255, -1, -5):
            color = (brightness, 0, 0)
            light_instance.on(color)
            await asyncio.sleep(0.02)

# Use task management
light = Light.first_light()
if light:
    # Start animation task
    task = light.add_task("breathing", breathing_animation)
    
    # Let it run for 10 seconds
    await asyncio.sleep(10)
    
    # Stop the animation
    light.cancel_task("breathing")
    light.off()
```

### Custom Async Patterns

Create complex lighting patterns with async/await:

```python
async def police_lights(light):
    """Police car style red/blue flashing"""
    while True:
        # Red flash
        for _ in range(3):
            light.on((255, 0, 0))
            await asyncio.sleep(0.1)
            light.off()
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(0.2)
        
        # Blue flash
        for _ in range(3):
            light.on((0, 0, 255))
            await asyncio.sleep(0.1)
            light.off()
            await asyncio.sleep(0.1)
        
        await asyncio.sleep(0.5)

# Run the pattern
light = Light.first_light()
if light:
    await police_lights(light)
```

## Configuration and Settings

### Environment Variables

Configure Busylight Core behavior via environment variables:

```python
import os

# Set default behavior
os.environ['BUSYLIGHT_CORE_DEBUG'] = 'true'
os.environ['BUSYLIGHT_CORE_DEFAULT_BRIGHTNESS'] = '128'
os.environ['BUSYLIGHT_CORE_AUTO_DISCOVER'] = 'true'

# Use configuration
from busylight_core import Light
lights = Light.available()  # Uses configured settings
```

### Programmatic Configuration

Configure devices programmatically:

```python
from busylight_core.settings import Settings

# Access global settings
settings = Settings()
settings.debug = True
settings.default_color = (255, 255, 0)  # Yellow

# Device-specific configuration
light = Light.first_light()
if light:
    light.brightness = 0.5  # 50% brightness
    light.default_flash_count = 5
```

## Error Handling and Debugging

### Exception Hierarchy

Busylight Core provides specific exceptions for different error conditions:

```python
from busylight_core import (
    Light, 
    NoLightsFound, 
    LightUnavailable, 
    LightUnsupported,
    InvalidHardwareInfo
)

try:
    light = Light.first_light()
    if not light:
        raise NoLightsFound("No devices found")
    
    light.on((255, 0, 0))
    
except NoLightsFound:
    print("Please connect a busylight device")
except LightUnavailable as e:
    print(f"Device unavailable: {e}")
except LightUnsupported as e:
    print(f"Device not supported: {e}")
except InvalidHardwareInfo as e:
    print(f"Hardware error: {e}")
```

### Debug Logging

Enable comprehensive debug logging:

```python
import logging
from loguru import logger

# Enable debug logging
logger.remove()
logger.add(lambda msg: print(msg), level="DEBUG")

# Now all operations will show debug information
from busylight_core import Light
lights = Light.available()  # Will show detailed discovery process
```

### Hardware Troubleshooting

Diagnose hardware detection issues:

```python
from busylight_core import Hardware, Light

def diagnose_hardware():
    """Comprehensive hardware diagnosis"""
    print("=== Hardware Diagnosis ===")
    
    # Check raw hardware detection
    hardware = Hardware.enumerate()
    print(f"Found {len(hardware)} hardware devices:")
    
    for hw in hardware:
        print(f"  VID:PID = {hw.vendor_id:04x}:{hw.product_id:04x}")
        print(f"  Manufacturer: {hw.manufacturer_string}")
        print(f"  Product: {hw.product_string}")
        print(f"  Serial: {hw.serial_number}")
        print(f"  Path: {hw.path}")
        print()
    
    # Check light recognition
    lights = Light.available()
    print(f"Recognized {len(lights)} as busylights:")
    
    for light in lights:
        print(f"  {light.vendor} {light.name}")
        print(f"  Class: {light.__class__.__name__}")
        print(f"  Supports: {', '.join(light.capabilities())}")
        print()
    
    # Check for unrecognized devices
    light_hardware = {light.hardware for light in lights}
    unrecognized = [hw for hw in hardware if hw not in light_hardware]
    
    if unrecognized:
        print(f"Unrecognized devices ({len(unrecognized)}):")
        for hw in unrecognized:
            print(f"  {hw.vendor_id:04x}:{hw.product_id:04x} - {hw.product_string}")

# Run diagnosis
diagnose_hardware()
```

## Performance Optimization

### Efficient Device Access

Optimize performance for applications that frequently access devices:

```python
from busylight_core import Light

class LightManager:
    def __init__(self):
        self._lights_cache = None
        self._last_scan = 0
        self.scan_interval = 5.0  # Rescan every 5 seconds
    
    @property
    def lights(self):
        import time
        now = time.time()
        
        if (self._lights_cache is None or 
            now - self._last_scan > self.scan_interval):
            self._lights_cache = Light.available()
            self._last_scan = now
        
        return self._lights_cache
    
    def refresh(self):
        """Force refresh of device list"""
        self._lights_cache = None

# Usage
manager = LightManager()
for light in manager.lights:  # Cached access
    light.on((255, 0, 0))
```

### Batch Operations

Perform batch operations efficiently:

```python
def set_all_lights(color, flash=False):
    """Set all connected lights to the same color"""
    lights = Light.available()
    
    for light in lights:
        try:
            if flash:
                light.flash(color, count=2)
            else:
                light.on(color)
        except Exception as e:
            print(f"Failed to control {light.name}: {e}")

# Set all lights to green
set_all_lights((0, 255, 0))

# Flash all lights red
set_all_lights((255, 0, 0), flash=True)
```

## Examples

For complete usage examples and real-world scenarios, see the [Examples](examples.md) page.

## Next Steps

- Explore the [API Reference](../reference/) for detailed method documentation
- Check out [Real-World Examples](examples.md) for practical applications
- Read the [Contributing Guide](../contributing.md) to add support for new devices