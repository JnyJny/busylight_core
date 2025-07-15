"""Luxafor Orb"""

from .flag import Flag


class Orb(Flag):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x4D8, 0xF372): "Orb",
    }
