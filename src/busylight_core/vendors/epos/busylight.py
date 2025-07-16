"""EPOS Busylight Support"""

from functools import cached_property
from typing import ClassVar

from busylight_core.light import Light

from ._busylight import State


class Busylight(Light):
    """EPOS Busylight status light controller.

    The EPOS Busylight is a USB-connected RGB LED device that provides
    status indication with multiple LED control capabilities.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x1395, 0x0074): "Busylight",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "EPOS"

    @cached_property
    def state(self) -> State:
        """Get the device state manager for controlling LED patterns."""
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the EPOS Busylight with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index for targeting specific LEDs

        """
        self.color = color
        with self.batch_update():
            self.state.set_color(color, led)

    def reset(self) -> None:
        """Reset the device to its default state."""
        self.state.reset()
        super().reset()
