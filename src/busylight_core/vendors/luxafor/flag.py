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
        """Check if this class can handle the given hardware device.

        Args:
            hardware: Hardware device to check

        Returns:
            True if this class can handle the hardware

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
        """Get the device state manager for controlling LED patterns."""
        return State()

    def __bytes__(self) -> bytes:
        self.state.color = self.color
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the Luxafor Flag with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index (0 for all LEDs, or specific LED number)

        """
        with self.batch_update():
            try:
                self.state.leds = LEDS(led)
            except ValueError:
                self.state.leds = LEDS.All
            self.color = color
