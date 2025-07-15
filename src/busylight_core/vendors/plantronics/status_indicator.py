"""Plantronics Status Indicator"""

from ..embrava.blynclight import Blynclight


class Status_Indicator(Blynclight):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x047F, 0xD005): "Status Indicator",
    }
