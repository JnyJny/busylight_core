"""ThingM vendor base class."""

from busylight_core.light import Light


class ThingMBase(Light):
    """Base class for ThingM devices.

    Provides common functionality for all ThingM devices,
    primarily the Blink(1) product line.
    """

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for ThingM devices."""
        return "ThingM"
