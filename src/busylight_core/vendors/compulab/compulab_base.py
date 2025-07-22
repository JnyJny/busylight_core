"""CompuLab vendor base class."""

from busylight_core.light import Light


class CompuLabBase(Light):
    """Base class for CompuLab devices.

    Provides common functionality for all CompuLab devices,
    primarily the fit-statUSB product line.
    """

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for CompuLab devices."""
        return "CompuLab"
