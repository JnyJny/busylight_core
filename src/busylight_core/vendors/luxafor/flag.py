"""Luxafor Flag"""

from functools import cached_property
from typing import ClassVar

from loguru import logger

from busylight_core.hardware import Hardware
from busylight_core.light import Light

from ._flag import LEDS, State


class Flag(Light):
    """Luxafor Flag status light controller.

    The Luxafor Flag is a USB-connected RGB LED device with multiple
    individually controllable LEDs arranged in a flag pattern.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x4D8, 0xF372): "Flag",
    }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Check if this class claims the given hardware device.

        :param hardware: A hardware instance
        """
        if not super().claims(hardware):
            return False

        try:
            product = hardware.product_string.split()[-1].casefold()
        except (KeyError, IndexError) as error:
            logger.debug(f"problem {error} processing {hardware}")
            return False

        return product in [
            value.casefold() for value in cls.supported_device_ids.values()
        ]

    @cached_property
    def state(self) -> State:
        """The device state manager for controlling a Luxfor device."""
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on a Luxafor device with the specified color tuple.

        :param color: RGB color tuple (red, green, blue)
        """
        with self.batch_update():
            self.color = color
            try:
                self.state.leds = LEDS(led)
            except ValueError:
                self.state.leds = LEDS.All

    @property
    def color(self) -> tuple[int, int, int]:
        """The current RGB color of a Luxafor device."""
        return self.state.color

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        self.state.color = value
