"""Agile Innovative Blinkstick Flex implementation details."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from busylight_core.hardware import Hardware

from ._blinkstick import BaseBlinkStick, State


class BlinkStickFlex(BaseBlinkStick):
    """Agile Innovative BlinkStick Flex status light controller.

    The BlinkStick Flex is a USB-connected RGB LED device with a flex form factor
    that can be controlled to display various colors and patterns for status indication.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x41E5): "BlinkStick Flex",
    }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Check if the hardware describes a BlinkStick Flex."""
        claim = super().claims(hardware)

        try:
            major, _ = cls.get_version(hardware.serial_number)
        except ValueError:
            return False

        return claim and major == 3 and hardware.release_number == 0x203

    @cached_property
    def state(self) -> State:
        """Get the current state of the BlinkStick Flex."""
        return State.blinkstick_flex()
