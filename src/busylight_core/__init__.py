"""Support for USB Connected Lights

Developers, adding support for a new device will entail:

- Optionally create a new vendor package in the vendors directory.
- Create a new subclass of busylight_core.light.Light.
- Implement all the missing abstract methods.
- Make sure the vendor package imports all the new subclasses.
- Make sure the vendor package appends the new subclasses to __all__.
- Import the new subclasses in busylight_core.__init__.
- Add the new subclasses to busylight_core.__init__.__all__.

Refer to any of the existing vendor packages as an example.

Please note, if the subclasses are not imported here, the
abc.ABC.__subclasses__ machinery will not find them and your
new lights will not be recognized.

"""

from loguru import logger

from .exceptions import (
    HardwareUnsupportedError,
    InvalidHardwareError,
    LightUnavailableError,
    NoLightsFoundError,
)
from .hardware import Hardware
from .light import Light
from .vendors.agile_innovative import BlinkStick
from .vendors.compulab import Fit_StatUSB
from .vendors.embrava import Blynclight, Blynclight_Mini, Blynclight_Plus
from .vendors.epos import Busylight
from .vendors.kuando import Busylight_Alpha, Busylight_Omega
from .vendors.luxafor import Bluetooth, BusyTag, Flag, Mute, Orb
from .vendors.muteme import MuteMe, MuteMe_Mini, MuteSync
from .vendors.plantronics import Status_Indicator
from .vendors.thingm import Blink1

__all__ = [
    "Blink1",
    "BlinkStick",
    "Bluetooth",
    "Blynclight",
    "Blynclight_Mini",
    "Blynclight_Plus",
    "BusyTag",
    "Busylight",
    "Busylight_Alpha",
    "Busylight_Omega",
    "Fit_StatUSB",
    "Flag",
    "Hardware",
    "HardwareUnsupportedError",
    "InvalidHardwareError",
    "Light",
    "LightUnavailableError",
    "Mute",
    "MuteMe",
    "MuteMe_Mini",
    "MuteSync",
    "NoLightsFoundError",
    "Orb",
    "Status_Indicator",
]

logger.disable("busylight_core")
