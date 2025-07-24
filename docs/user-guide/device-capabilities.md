# Device Capabilities Reference

This guide provides detailed information about each supported device's capabilities, helping you choose the right device and understand what features are available for your specific hardware.

## Capability Overview

| Feature | Devices | Description |
|---------|---------|-------------|
| **Basic RGB Color** | All 26 devices | Standard 0-255 RGB color control |
| **Hardware Flash** | 13 devices | Built-in flash patterns with configurable speed |
| **Multi-LED Control** | 7 device variants | Control individual LEDs (2-192 LEDs) |
| **Audio/Sound** | 5 devices | Built-in speaker with configurable sounds |
| **Button Input** | 4 devices | Physical button state detection |
| **Advanced Programming** | 3 devices | Pattern storage and custom sequences |

## Vendor Summary

### Embrava (3 devices)
Professional meeting status lights with audio capabilities.

| Device | LEDs | Flash | Audio | Special Features |
|--------|------|-------|-------|------------------|
| **Blynclight** | 1 | ✓ | ✓ | Industry standard |
| **Blynclight Mini** | 1 | ✓ | ✓ | Compact form |
| **Blynclight Plus** | 1 | ✓ | ✓ | Enhanced brightness |

**Usage Example:**
```python
from busylight_core import Blynclight

# Find Blynclight devices
blynclights = Blynclight.all_lights()
if blynclights:
    light = blynclights[0]
    light.on((255, 0, 0), sound=True)  # Red with audio alert
    light.flash((255, 255, 0))         # Flash yellow
```

### Kuando (2 devices)
High-quality Nordic design with keepalive requirements.

| Device | LEDs | Flash | Audio | Special Features |
|--------|------|-------|-------|------------------|
| **Busylight Alpha** | 1 | ✓ | ✗ | Multiple USB IDs |
| **Busylight Omega** | 1 | ✓ | ✗ | Premium model |

**Usage Example:**
```python
from busylight_core import BusylightAlpha, BusylightOmega

# Kuando devices need keepalive
alpha_lights = BusylightAlpha.all_lights()
omega_lights = BusylightOmega.all_lights()

for light in alpha_lights + omega_lights:
    light.on((0, 255, 0))
    light.keepalive()  # Required for Kuando devices
```

### Luxafor (5 devices)
Versatile devices with multi-LED support and button input.

| Device | LEDs | Flash | Audio | Special Features |
|--------|------|-------|-------|------------------|
| **Flag** | 6 | ✓ | ✗ | Multi-zone control |
| **Orb** | 1 | ✓ | ✗ | Spherical design |
| **Bluetooth** | 1 | ✓ | ✗ | Wireless capable |
| **Mute** | 1 | ✓ | ✗ | Button input |
| **Busy Tag** | 1 | ✗ | ✗ | ASCII text protocol |

**Usage Example:**
```python
from busylight_core import Flag

# Multi-LED control with Flag
flags = Flag.all_lights()
if flags:
    flag = flags[0]
    # Control individual LEDs
    for i in range(6):
        flag.on((255, 0, 0), led=i)  # Individual LED control
```

### Agile Innovative BlinkStick (6 variants)
Flexible multi-LED strips and matrices for creative applications.

| Device | LEDs | Flash | Audio | Special Features |
|--------|------|-------|-------|------------------|
| **BlinkStick** | 1 | ✗ | ✗ | Basic model |
| **BlinkStick Nano** | 2 | ✗ | ✗ | Dual LED |
| **BlinkStick Square** | 8 | ✗ | ✗ | 8-LED matrix |
| **BlinkStick Strip** | 8 | ✗ | ✗ | LED strip |
| **BlinkStick Flex** | 32 | ✗ | ✗ | Flexible strip |
| **BlinkStick Pro** | 64 | ✗ | ✗ | Professional strip |

**Usage Example:**
```python
from busylight_core import BlinkStickPro

# Multi-LED animations
strips = BlinkStickPro.all_lights()
if strips:
    strip = strips[0]
    # Create rainbow effect
    colors = [(255,0,0), (255,127,0), (255,255,0), (0,255,0), (0,0,255)]
    for i, color in enumerate(colors):
        strip.on(color, led=i)
```

### ThingM (1 device)
Popular maker-friendly device with advanced programming.

| Device | LEDs | Flash | Audio | Special Features |
|--------|------|-------|-------|------------------|
| **Blink(1)** | 2 | ✗ | ✗ | Pattern storage, fade effects |

**Usage Example:**
```python
from busylight_core import Blink1

# Advanced fade effects
blink1s = Blink1.all_lights()
if blink1s:
    blink = blink1s[0]
    # Hardware fade (if supported)
    if hasattr(blink, 'fade'):
        blink.fade((255, 0, 0), duration=2.0)
```

### MuteMe (3 devices)
Specialized mute button devices with status indication.

| Device | LEDs | Flash | Audio | Special Features |
|--------|------|-------|-------|------------------|
| **MuteMe Original** | 1 | ✗ | ✗ | Button input, status LED |
| **MuteMe Mini** | 1 | ✗ | ✗ | Compact button |
| **MuteSync Button** | 1 | ✗ | ✗ | Sync-enabled |

**Usage Example:**
```python
from busylight_core import MuteMe

# Button state monitoring
muteme_devices = MuteMe.all_lights()
if muteme_devices:
    mute = muteme_devices[0]
    if mute.is_button and mute.button_pressed():
        mute.on((255, 0, 0))  # Red when muted
    else:
        mute.on((0, 255, 0))  # Green when unmuted
```

### Other Vendors

**EPOS Busylight** - Professional conferencing light
**Plantronics Status Indicator** - Call center indicator  
**CompuLab fit-statUSB** - Industrial status indicator

## Common Usage Patterns

### Device Detection and Selection
```python
from busylight_core import Light

# Get all devices with audio support
audio_devices = []
for light in Light.all_lights():
    if hasattr(light, 'on') and 'sound' in light.on.__annotations__:
        audio_devices.append(light)

# Get multi-LED devices
multi_led_devices = []
for light in Light.all_lights():
    if hasattr(light, 'on') and 'led' in light.on.__annotations__:
        multi_led_devices.append(light)
```

### Capability Testing
```python
# Check device capabilities at runtime
def get_device_features(light):
    features = {
        'basic_color': True,  # All devices support this
        'flash': hasattr(light, 'flash'),
        'multi_led': 'led' in getattr(light.on, '__annotations__', {}),
        'audio': 'sound' in getattr(light.on, '__annotations__', {}),
        'button': light.is_button,
        'fade': hasattr(light, 'fade'),
    }
    return features

# Use features to adapt behavior
for light in Light.all_lights():
    features = get_device_features(light)
    
    if features['audio']:
        light.on((255, 0, 0), sound=True)
    elif features['flash']:
        light.flash((255, 0, 0))
    else:
        light.on((255, 0, 0))
```

## Hardware Notes

### USB Device IDs
Each device type uses specific USB vendor/product ID combinations. Some vendors use the same USB ID for multiple products (differentiated by firmware or physical design).

### Color Ordering
Devices use different internal color formats, but the library automatically handles all conversions:
- Most devices: RGB (0-255)
- BlinkStick devices: GRB ordering internally
- Blynclight devices: RBG ordering internally  
- Kuando Busylight devices: RGB with 0-100 scaling internally

### Power Requirements
All supported devices are USB bus-powered and require no external power supply.

### Platform Compatibility
All devices work on Windows, macOS, and Linux. Linux users need udev rules for non-root access (see [Installation Guide](../getting-started/installation.md#linux-setup-udev-rules)).

## Next Steps

- Check the [Examples](examples.md) for device-specific usage patterns
- Review the [API Reference](../reference/index.md) for complete method documentation
- See [Installation Guide](../getting-started/installation.md) for setup instructions