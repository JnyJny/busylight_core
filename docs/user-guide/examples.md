# Examples

This page provides comprehensive examples of using Busylight Core for various scenarios.

## Basic Device Control

### Finding and Connecting to Lights

```python
from busylight_core import Light

# Get all available lights
lights = Light.available()
print(f"Found {len(lights)} light(s)")

# Get the first available light
light = Light.first_light()
if light:
    print(f"Using: {light.vendor} {light.name}")
else:
    print("No lights found")

# Find lights by vendor
embrava_lights = [l for l in lights if l.vendor == "Embrava"]
```

### Basic Light Operations

```python
from busylight_core import Light

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

### Using Async Tasks for Animations

```python
import asyncio
from busylight_core import Light

async def breathing_effect(light, color, duration=2.0):
    """Create a breathing effect by fading in and out"""
    while True:
        # Fade in
        for brightness in range(0, 256, 5):
            scaled_color = tuple(int(c * brightness / 255) for c in color)
            light.on(scaled_color)
            await asyncio.sleep(duration / 102)  # 51 steps * 2 directions
        
        # Fade out
        for brightness in range(255, -1, -5):
            scaled_color = tuple(int(c * brightness / 255) for c in color)
            light.on(scaled_color)
            await asyncio.sleep(duration / 102)

async def rainbow_cycle(light):
    """Cycle through rainbow colors"""
    colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211),  # Violet
    ]
    
    for color in colors:
        light.on(color)
        await asyncio.sleep(1.0)

# Run async animations
async def main():
    light = Light.first_light()
    if light:
        # Run breathing effect for 10 seconds
        breathing_task = asyncio.create_task(breathing_effect(light, (0, 255, 0)))
        await asyncio.sleep(10)
        breathing_task.cancel()
        
        # Run rainbow cycle
        await rainbow_cycle(light)
        light.off()

# Run the example
asyncio.run(main())
```

### Using Built-in Task Management

```python
from busylight_core import Light

light = Light.first_light()

# Use the built-in TaskableMixin for animations
async def pulse_animation(light_instance):
    """Custom pulse animation"""
    for _ in range(10):
        light_instance.on((255, 0, 0))
        await asyncio.sleep(0.5)
        light_instance.off()
        await asyncio.sleep(0.5)

# Add and manage tasks
task = light.add_task("pulse", pulse_animation)
print(f"Started task: {task}")

# Cancel task later
light.cancel_task("pulse")

# Cancel all tasks
light.cancel_tasks()
```

## Real-World Applications

### Meeting Status Indicator

```python
from busylight_core import Light
import time

class MeetingStatusLight:
    def __init__(self):
        self.light = Light.first_light()
        
    def available(self):
        """Green light - available for meetings"""
        if self.light:
            self.light.on((0, 255, 0))
    
    def busy(self):
        """Red light - in meeting, do not disturb"""
        if self.light:
            self.light.on((255, 0, 0))
    
    def away(self):
        """Yellow light - away from desk"""
        if self.light:
            self.light.on((255, 255, 0))
    
    def offline(self):
        """No light - offline/unavailable"""
        if self.light:
            self.light.off()

# Usage
status = MeetingStatusLight()
status.busy()        # Set to busy
time.sleep(3600)     # Stay busy for an hour
status.available()   # Back to available
```

### Build Status Monitor

```python
import subprocess
from busylight_core import Light

class BuildMonitor:
    def __init__(self):
        self.light = Light.first_light()
    
    def check_build_status(self):
        """Check build status and update light accordingly"""
        try:
            # Run your build command
            result = subprocess.run(['your-build-command'], 
                                  capture_output=True, check=True)
            
            # Success - green flash
            if self.light:
                self.light.flash((0, 255, 0), count=3)
                self.light.on((0, 255, 0))  # Stay green
            
        except subprocess.CalledProcessError:
            # Failure - red flash then solid red
            if self.light:
                self.light.flash((255, 0, 0), count=5)
                self.light.on((255, 0, 0))  # Stay red

# Usage
monitor = BuildMonitor()
monitor.check_build_status()
```

### Notification System

```python
from busylight_core import Light
import json

class NotificationLight:
    def __init__(self):
        self.light = Light.first_light()
        
        # Define notification colors
        self.colors = {
            'email': (0, 0, 255),      # Blue
            'calendar': (255, 255, 0),  # Yellow
            'alert': (255, 0, 0),      # Red
            'success': (0, 255, 0),    # Green
            'info': (0, 255, 255),     # Cyan
        }
    
    def notify(self, notification_type, flash=True):
        """Show notification on light"""
        color = self.colors.get(notification_type, (255, 255, 255))
        
        if self.light:
            if flash:
                self.light.flash(color, count=2)
            self.light.on(color)
    
    def clear(self):
        """Clear all notifications"""
        if self.light:
            self.light.off()

# Usage
notifier = NotificationLight()
notifier.notify('email')     # Blue flash for new email
notifier.notify('alert')     # Red flash for alert
notifier.clear()             # Turn off
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
from busylight_core import Light, LightUnavailable, NoLightsFound

try:
    # Try to get a light
    light = Light.first_light()
    if not light:
        raise NoLightsFound("No lights connected")
    
    # Try to control the light
    light.on((255, 0, 0))
    
except NoLightsFound:
    print("No busylights found. Please connect a device.")
except LightUnavailable as e:
    print(f"Light unavailable: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
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
lights = Light.available()
print(f"Recognized {len(lights)} as lights:")

for light in lights:
    print(f"  {light.vendor} {light.name}")
    print(f"    Claimed by: {light.__class__.__name__}")
```

## Configuration and Settings

### Environment Variables

```python
import os
from busylight_core import Light

# Configure via environment variables
os.environ['BUSYLIGHT_CORE_DEBUG'] = 'true'
os.environ['BUSYLIGHT_CORE_DEFAULT_COLOR'] = '255,0,0'  # Default red

# Use configured settings
light = Light.first_light()
if light:
    # Settings are automatically applied
    light.on()  # Uses default color from environment
```

## Next Steps

- Learn more about the [API Reference](../reference/)
- Check out device-specific documentation for advanced features
- Read the [Contributing Guide](../contributing.md) to add support for new devices
- Visit the [GitHub repository](https://github.com/JnyJny/busylight_core) for the latest updates