"""Agile Innovative BlinkStick"""

from functools import cached_property

from loguru import logger

from ...light import Light
from ._blinkstick import BlinkStickVariant


class BlinkStick(Light):
    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x20A0, 0x41E5): "BlinkStick",
        }

    @staticmethod
    def vendor() -> str:
        return "Agile Innovative"

    @property
    def channel(self) -> int:
        return getattr(self, "_channel", 0)

    @channel.setter
    def channel(self, value: int) -> None:
        self._channel = value

    @property
    def index(self) -> int:
        return getattr(self, "_index", 0)

    @index.setter
    def index(self, value: int) -> None:
        self._index = value

    @cached_property
    def variant(self) -> BlinkStickVariant:
        return BlinkStickVariant.from_hardware(self.hardware)


    @property
    def name(self) -> str:
        return self.variant.name

    def __bytes__(self) -> bytes:

        match self.variant.report:
            case 1:
                buf = [self.variant.report, self.green, self.red, self.blue]
            case _:
                buf = [self.variant.report, self.channel]
                buf.extend([self.green, self.red, self.blue] * self.variant.nleds)

        return bytes(buf)
