"""MuteSync status light and button implementation."""

from typing import ClassVar

from busylight_core.hardware import Hardware
from busylight_core.light import Light


class MuteSync(Light):
    """MuteSync status light and button controller.

    The MuteSync is a USB-connected device that combines button
    functionality with status light capabilities for meeting control.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x10C4, 0xEA60): "MuteSync Button",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "MuteSync"

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Return True if the hardware describes a MuteSync Button."""
        # Addresses issue #356 where MuteSync claims another hardware with
        # a SiliconLabs CP2102 USB to Serial controller that is not a MuteSync
        # hardware.

        claim = super().claims(hardware)

        vendor = cls.vendor().lower()

        try:
            manufacturer = vendor in hardware.manufacturer_string.lower()
        except AttributeError:
            manufacturer = False

        try:
            product = vendor in hardware.product_string.lower()
        except AttributeError:
            product = False

        return claim and (product or manufacturer)

    def __bytes__(self) -> bytes:
        buf = [65] + [*self.color] * 4

        return bytes(buf)

    @property
    def is_button(self) -> bool:
        """Check if this device has button functionality.

        Returns:
            True, as the MuteSync device has a button

        """
        return True

    @property
    def button_on(self) -> bool:
        """Check if the mute button is currently pressed.

        Returns:
            Always False in current implementation

        """
        return False

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the MuteSync with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index (unused for MuteSync)

        """
        with self.batch_update():
            self.color = color
