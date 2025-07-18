"""Agile Innovative Blinkstick Square implementation details."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, ClassVar

from busylight_core.light import Light

if TYPE_CHECKING:
    from busylight_core.hardware import Hardware

from ._blinkstick import State


class BlinkStickSquare(Light):
    """Agile Innovative BlinkStick Square status light controller.

    The BlinkStick Square is a USB-connected RGB LED device with a square form factor
    that can be controlled to display various colors and patterns for status indication.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x41E5): "BlinkStick Square",
    }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Check if the hardware matches the BlinkStick Square device IDs."""
        claim = super().claims(hardware)

        try:
            major = hardware.serial_number[-3:][0]
        except (IndexError, TypeError):
            return False

        return claim and major == "3" and hardware.release_number == 0x200

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "Agile Innovative"

    @cached_property
    def state(self) -> State:
        """Get the current state of the BlinkStick Square."""
        return State.blinkstick_square()

    def __bytes__(self) -> bytes:
        """Return the byte representation of the BlinkStick Square state."""
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Activate the light with the given red, green, blue color tuple."""
        with self.batch_update():
            self.color = color
            if led == 0:
                self.state.color = self.color
            else:
                self.state.set_led(led - 1, color)
