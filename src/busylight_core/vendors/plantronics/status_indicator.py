"""Plantronics Status Indicator"""

from typing import ClassVar

from busylight_core.vendors.embrava.embrava_base import EmbravaBase


class StatusIndicator(EmbravaBase):
    """Plantronics Status Indicator status light controller.

    A Plantronics-branded version of the Blynclight device with
    identical functionality to the Embrava Blynclight.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x047F, 0xD005): "Status Indicator",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "Plantronics"
