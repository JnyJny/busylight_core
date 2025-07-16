"""Agile Innovative BlinkStick"""

from functools import cached_property
from typing import ClassVar

from busylight_core.light import Light

from ._blinkstick import BlinkStickVariant


class BlinkStick(Light):
    """Agile Innovative BlinkStick status light controller.

    The BlinkStick is a USB-connected RGB LED device that can be controlled
    to display various colors and patterns for status indication.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x41E5): "BlinkStick",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "Agile Innovative"

    @property
    def channel(self) -> int:
        """Get the current channel number for multi-channel BlinkStick devices."""
        return getattr(self, "_channel", 0)

    @channel.setter
    def channel(self, value: int) -> None:
        self._channel = value

    @property
    def index(self) -> int:
        """Get the current LED index for addressing individual LEDs."""
        return getattr(self, "_index", 0)

    @index.setter
    def index(self, value: int) -> None:
        self._index = value

    @cached_property
    def variant(self) -> BlinkStickVariant:
        """Get the BlinkStick variant information based on hardware detection."""
        return BlinkStickVariant.from_hardware(self.hardware)

    @property
    def name(self) -> str:
        """Get the device name from the variant information."""
        return self.variant.name

    def __bytes__(self) -> bytes:
        match self.variant.report:
            case 1:
                buf = [self.variant.report, self.green, self.red, self.blue]
            case _:
                buf = [self.variant.report, self.channel]
                buf.extend([self.green, self.red, self.blue] * self.variant.nleds)

        return bytes(buf)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the BlinkStick with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index (unused for BlinkStick)

        """
        with self.batch_update():
            self.color = color
