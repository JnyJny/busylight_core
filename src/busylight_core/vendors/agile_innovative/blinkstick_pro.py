"""Agile Innovative Blinkstick Pro implementation details."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from busylight_core.hardware import Hardware

from ._blinkstick import BaseBlinkStick, State


class BlinkStickPro(BaseBlinkStick):
    """Agile Innovative BlinkStick Pro status light controller.

    The BlinkStick Pro is a USB-connected RGB LED device with a pro form factor
    that can be controlled to display various colors and patterns for status indication.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x41E5): "BlinkStick Pro",
    }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Check if the hardware describes a BlinkStick Pro."""
        claim = super().claims(hardware)

        try:
            major, _ = cls.get_version(hardware.serial_number)
        except ValueError:
            return False

        return claim and major == 2

    @cached_property
    def state(self) -> State:
        """Get the current state of the BlinkStick Pro."""
        return State.blinkstick_pro()
