"""BusyTag Light Support"""

from typing import ClassVar

from busylight_core.light import Light

from ._busytag import Command


class BusyTag(Light):
    """BusyTag status light controller.

    The BusyTag is a wireless status light that uses command strings
    for communication and supports various lighting patterns.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x303A, 0x81DF): "Busy Tag",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "Busy Tag"

    @property
    def command(self) -> str:
        """Get the current command string for device communication."""
        return getattr(self, "_command", "")

    @command.setter
    def command(self, value: str) -> None:
        self._command = value

    def __bytes__(self) -> bytes:
        return self.command.encode()

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the BusyTag with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index for specific LED targeting

        """
        with self.batch_update():
            self.color = color
            self.command = Command.solid_color(color, led)
