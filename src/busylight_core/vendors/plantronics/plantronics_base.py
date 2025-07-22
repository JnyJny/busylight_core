"""Plantronics vendor base class."""

from busylight_core.vendors.embrava.embrava_base import EmbravaBase


class PlantronicsBase(EmbravaBase):
    """Base class for Plantronics devices.

    Plantronics devices are typically OEM versions of Embrava devices
    with the same functionality but different vendor branding.
    """

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for Plantronics devices."""
        return "Plantronics"
