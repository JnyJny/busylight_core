# Examples

This page provides comprehensive examples of using Busylight Core for various scenarios.

## Basic Device Control

### Finding and Connecting to Lights

```python
from busylight_core import Light, NoLightsFoundError

# Get all available lights
lights = Light.all_lights()
print(f"Found {len(lights)} light(s)")

# Get the first available light
try:
    light = Light.first_light()
    print(f"Using: {light.vendor()} {light.name}")
except NoLightsFoundError:
    print("No lights found")
    light = None

# Find lights by vendor  
embrava_lights = [l for l in lights if l.vendor() == "Embrava"]
```

### Basic Light Operations

```python
from busylight_core import Light, NoLightsFoundError

try:
    light = Light.first_light()
    
    # Turn on with different colors
    light.on((255, 0, 0))    # Red
    light.on((0, 255, 0))    # Green
    light.on((0, 0, 255))    # Blue
    light.on((255, 255, 0))  # Yellow
    
    # Turn off
    light.off()
    
    # Check if light is on
    if light.is_on:
        print("Light is currently on")
        
except NoLightsFoundError:
    print("No lights found")
```

## Advanced Light Control

### Flash Patterns and Effects

```python
# Flash patterns
light.flash((255, 0, 0), count=3)           # Flash red 3 times
light.flash((0, 255, 0), duration=0.5)      # Custom flash duration
light.flash((255, 255, 0), count=5, delay=0.2)  # Custom count and delay

# Fade effects (for supported devices like Blink(1))
if hasattr(light, 'fade'):
    light.fade((255, 0, 0), duration=2.0)   # Fade to red over 2 seconds
```

### Multi-LED Device Control

```python
from busylight_core import BlinkStick

# Find BlinkStick devices (support multiple LEDs)
blinksticks = [l for l in Light.available() if isinstance(l, BlinkStick)]

if blinksticks:
    stick = blinksticks[0]
    
    # Control individual LEDs
    stick.set_led(0, (255, 0, 0))    # First LED red
    stick.set_led(1, (0, 255, 0))    # Second LED green
    stick.set_led(2, (0, 0, 255))    # Third LED blue
    
    # Set all LEDs to same color
    stick.set_all((255, 255, 255))   # All white
```

### Audio-Enabled Devices

```python
from busylight_core import Blynclight

# Find Blynclight devices (support audio)
blynclights = [l for l in Light.available() if isinstance(l, Blynclight)]

if blynclights:
    blight = blynclights[0]
    
    # Control with sound
    blight.on((255, 0, 0), sound=True)      # Red with sound
    blight.flash((255, 255, 0), sound=True)  # Flash yellow with sound
    
    # Mute/unmute functions
    blight.mute()
    blight.unmute()
```

## Async Programming

### Using Built-in Task Management

```python
import asyncio
from busylight_core import Light, NoLightsFoundError

try:
    light = Light.first_light()
    
    # Use the built-in TaskableMixin for animations
    async def pulse_animation():
        """Custom pulse animation"""
        for _ in range(10):
            light.on((255, 0, 0))
            await asyncio.sleep(0.5)
            light.off()
            await asyncio.sleep(0.5)
    
    # Add and manage tasks
    task = light.add_task("pulse", pulse_animation)
    print(f"Started task: {task}")
    
    # Cancel task later
    light.cancel_task("pulse")
    
    # Cancel all tasks
    light.cancel_tasks()
    
except NoLightsFoundError:
    print("No lights found")
```


## Device-Specific Features

### Button Input Handling

```python
from busylight_core import MuteMe, Luxafor

# For devices with button input (MuteMe, Luxafor Mute)
devices_with_buttons = []
for light in Light.available():
    if isinstance(light, (MuteMe, Luxafor)) and hasattr(light, 'button_pressed'):
        devices_with_buttons.append(light)

if devices_with_buttons:
    device = devices_with_buttons[0]
    
    # Check button state
    if device.button_pressed():
        print("Button is currently pressed")
        device.on((255, 0, 0))  # Red when pressed
    else:
        device.on((0, 255, 0))  # Green when not pressed
```

### Vendor-Specific Optimizations

```python
from busylight_core import Light, Kuando

# Some devices have vendor-specific features
for light in Light.available():
    if isinstance(light, Kuando):
        # Kuando devices support keepalive
        light.keepalive()
    
    # Check device capabilities
    if hasattr(light, 'dim'):
        light.dim()  # Dim the light
    
    if hasattr(light, 'bright'):
        light.bright()  # Brighten the light
```

## Error Handling and Debugging

### Robust Error Handling

```python
from busylight_core import Light, LightUnavailableError, NoLightsFoundError

try:
    # Try to get a light
    light = Light.first_light()
    
    # Try to control the light
    light.on((255, 0, 0))
    
except NoLightsFoundError:
    print("No busylights found. Please connect a device.")
except LightUnavailableError as error:
    print(f"Light unavailable: {error}")
except Exception as error:
    print(f"Unexpected error: {error}")
```

### Debugging Device Issues

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
- Check out [Device Capabilities](device-capabilities.md) for device-specific features
- Read the [Contributing Guide](../contributing.md) to add support for new devices
- Visit the [GitHub repository](https://github.com/JnyJny/busylight_core) for the latest updates
