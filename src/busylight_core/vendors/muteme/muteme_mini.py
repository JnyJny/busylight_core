""" MuteMe Mini Support
"""

from .muteme import MuteMe


class MuteMe_Mini(MuteMe):
    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x20A0, 0x42DB): "MuteMe Mini",
        }
