"""Busylight Omega Support"""

from .busylight_alpha import Busylight_Alpha


class Busylight_Omega(Busylight_Alpha):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x27BB, 0x3BCD): "Busylight Omega",
        (0x27BB, 0x3BCF): "Busylight Omega",
    }
