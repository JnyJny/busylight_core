""" """

from .blynclight import Blynclight


class Blynclight_Plus(Blynclight):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x2C0D, 0x0002): "Blynclight Plus",
        (0x2C0D, 0x0010): "Blynclight Plus",
    }
