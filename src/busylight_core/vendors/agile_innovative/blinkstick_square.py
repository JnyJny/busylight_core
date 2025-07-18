"""Agile Innovative Blinkstick Square implementation details."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from busylight_core.hardware import Hardware


from ._blinkstick import BaseBlinkStick, State


class BlinkStickSquare(BaseBlinkStick):
    """Agile Innovative BlinkStick Square status light controller.

    The BlinkStick Square is a USB-connected RGB LED device with a square form factor
    that can be controlled to display various colors and patterns for status indication.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x41E5): "BlinkStick Square",
    }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Return True if the hardware describes a BlinkStick Square."""
        claim = super().claims(hardware)

        try:
            major, _ = cls.get_version(hardware.serial_number)
        except ValueError:
            return False

        return claim and major == 3 and hardware.release_number == 0x200

    @cached_property
    def state(self) -> State:
        """Get the current state of the BlinkStick Square."""
        return State.blinkstick_square()
