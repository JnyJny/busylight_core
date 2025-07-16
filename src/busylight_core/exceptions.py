"""raised by busylight_core.light.Light and subclasses"""


class _BaseHardwareError(Exception):
    """Base class for hardware-related errors."""


class _BaseLightError(Exception):
    """Base class for light-related errors."""


class LightUnavailableError(_BaseLightError):
    """Previously accessible light is now not accessible."""


class HardwareUnsupportedError(_BaseLightError):
    """The hardware supplied is not supported by this class."""


class NoLightsFoundError(_BaseLightError):
    """No lights were discovered by Light or a subclass of Light."""


class InvalidHardwareError(_BaseHardwareError):
    """The device dictionary is missing required key/value pairs."""


class HardwareAlreadyOpenError(_BaseHardwareError):
    """The hardware device is already open and cannot be opened again."""


class HardwareNotOpenError(_BaseHardwareError):
    """The hardware device is not open and cannot be used."""
