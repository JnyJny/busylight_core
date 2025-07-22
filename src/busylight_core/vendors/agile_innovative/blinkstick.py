"""Agile Innovative BlinkStick"""

from functools import cached_property
from typing import ClassVar

from busylight_core import Hardware

from ._blinkstick import State
from .blinkstick_base import BlinkStickBase


class BlinkStick(BlinkStickBase):
    """Agile Innovative BlinkStick status light controller.

    The BlinkStick is a USB-connected RGB LED device that can be controlled
    to display various colors and patterns for status indication.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x41E5): "BlinkStick",
    }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Return True if the hardware matches a BlinkStick."""
        if not super().claims(hardware):
            return False
        try:
            major, _ = cls.get_version(hardware.serial_number)
        except ValueError:
            return False
        return major == 1

    @cached_property
    def state(self) -> State:
        """Get the current state of the BlinkStick."""
        return State.blinkstick()
