"""Luxafor Flag"""

from functools import cached_property

from loguru import logger

from ...hardware import Hardware
from ...light import Light
from ._flag import LEDS, Command, Pattern, State, Wave


class Flag(Light):
    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x4D8, 0xF372): "Flag",
        }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:

        if not super().claims(hardware):
            return False

        try:
            product = hardware.product_string.split()[-1].casefold()
        except (KeyError, IndexError) as error:
            logger.debug(f"problem {error} processing {hardware}")
            return False

        return product in [
            value.casefold() for value in cls.supported_device_ids().values()
        ]

    @cached_property
    def state(self) -> State:
        return State()

    def __bytes__(self) -> bytes:

        self.state.color = self.color

        return bytes(self.state)
