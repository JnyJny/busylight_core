"""Plantronics Status Indicator"""

from typing import ClassVar

from busylight_core.vendors.embrava.blynclight import Blynclight


class Status_Indicator(Blynclight):
    """Plantronics Status Indicator status light controller.

    A Plantronics-branded version of the Blynclight device with
    identical functionality to the Embrava Blynclight.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x047F, 0xD005): "Status Indicator",
    }
