"""ThingM blink(1) Support"""

from collections.abc import Callable
from functools import cached_property
from typing import ClassVar

from busylight_core.light import Light

from ._blink1 import LEDS, State


class Blink1(Light):
    """ThingM Blink(1) status light controller.

    The Blink(1) is a USB-connected RGB LED device that uses
    feature reports for communication and supports various effects.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x27B8, 0x01ED): "Blink(1)",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "ThingM"

    @cached_property
    def state(self) -> State:
        """Get the device state manager for controlling LED patterns."""
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the Blink(1) with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index for targeting specific LEDs

        """
        self.color = color
        with self.batch_update():
            self.state.fade_to_color(self.color, leds=LEDS(led))

    @property
    def write_strategy(self) -> Callable:
        """Get the write strategy for communicating with the device.

        Returns:
            The hardware's send_feature_report method

        """
        return self.hardware.handle.send_feature_report
