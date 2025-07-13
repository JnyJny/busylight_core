"""MuteMe Button & Light"""

import struct
from functools import cached_property

from loguru import logger

from ...light import Light
from ._muteme import State


class MuteMe(Light):
    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x16C0, 0x27DB): "MuteMe Original",
            (0x20A0, 0x42DA): "MuteMe Original",
        }

    @staticmethod
    def vendor() -> str:
        return "MuteMe"

    @cached_property
    def state(self) -> State():
        return State()

    @cached_property
    def struct(self) -> struct.Struct:
        return struct.Struct("!xB")

    def __bytes__(self) -> bytes:
        self.state.color = self.color
        return self.struct.pack(self.state.value)

    @property
    def is_pluggedin(self) -> bool:

        # EJO No reason for eight, just a power of two.
        try:
            nbytes = self.hardware.send_feature_report([0] * 8)
            return nbytes == 8
        except ValueError:
            pass
        return False

    @property
    def is_button(self) -> bool:
        return True

    @property
    def button_on(self) -> bool:
        raise NotImplementedError()
