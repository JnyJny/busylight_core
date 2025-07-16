"""CompuLab fit-statUSB status light implementation."""

from typing import ClassVar

from busylight_core.light import Light


class Fit_StatUSB(Light):
    """CompuLab fit-statUSB status light controller.

    The fit-statUSB is a USB-connected RGB LED device that communicates
    using text-based commands for color control.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x2047, 0x03DF): "fit-statUSB",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "CompuLab"

    def __bytes__(self) -> bytes:
        buf = f"B#{self.red:02x}{self.green:02x}{self.blue:02x}\n"

        return buf.encode()

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the fit-statUSB with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index (unused for fit-statUSB)

        """
        with self.batch_update():
            self.color = color
