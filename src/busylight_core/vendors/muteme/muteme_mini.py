"""MuteMe Mini Support"""

from typing import ClassVar

from .muteme import MuteMe


class MuteMe_Mini(MuteMe):
    """MuteMe Mini status light and button controller.

    A smaller version of the MuteMe device with the same button
    and LED functionality as the original MuteMe.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x42DB): "MuteMe Mini",
    }
