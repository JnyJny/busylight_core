"""MuteMe Button & Light"""

import struct
from functools import cached_property
from typing import ClassVar

from busylight_core.light import Light

from ._muteme import State


class MuteMe(Light):
    """MuteMe status light and button controller.

    The MuteMe is a USB-connected RGB LED device with integrated button
    functionality for mute control in video conferencing applications.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x16C0, 0x27DB): "MuteMe Original",
        (0x20A0, 0x42DA): "MuteMe Original",
    }

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "MuteMe"

    @cached_property
    def state(self) -> State():
        """Get the device state manager for controlling light behavior."""
        return State()

    @cached_property
    def struct(self) -> struct.Struct:
        """Get the binary struct formatter for device communication."""
        return struct.Struct("!xB")

    def __bytes__(self) -> bytes:
        self.state.color = self.color
        return self.struct.pack(self.state.value)

    @property
    def is_pluggedin(self) -> bool:
        """Check if the device is plugged in and responsive.

        Returns:
            True if device responds to feature report, False otherwise

        """
        # EJO No reason for eight, just a power of two.
        try:
            nbytes = self.hardware.send_feature_report([0] * 8)
        except ValueError:
            pass
        else:
            return nbytes == 8
        return False

    @property
    def is_button(self) -> bool:
        """Check if this device has button functionality.

        Returns:
            True, as the MuteMe device has a button

        """
        return True

    @property
    def button_on(self) -> bool:
        """Check if the mute button is currently pressed.

        Returns:
            True if the button is pressed, False otherwise

        Raises:
            NotImplementedError: Button state reading not implemented

        """
        raise NotImplementedError

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the MuteMe with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index (unused for MuteMe)

        """
        with self.batch_update():
            self.color = color
