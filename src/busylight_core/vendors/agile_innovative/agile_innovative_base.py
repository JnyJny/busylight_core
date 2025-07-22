"""Agile Innovative vendor base class."""

from busylight_core.light import Light


class AgileInnovativeBase(Light):
    """Base class for Agile Innovative devices.

    Provides common functionality for all Agile Innovative devices,
    primarily the BlinkStick product line.
    """

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for Agile Innovative devices."""
        return "Agile Innovative"
