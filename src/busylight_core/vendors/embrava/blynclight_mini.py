""" """

from .blynclight import Blynclight


class Blynclight_Mini(Blynclight):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x2C0D, 0x000A): "Blynclight Mini",
        (0x0E53, 0x2517): "Blynclight Mini",
    }
