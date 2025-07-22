"""Agile Innovative Blinkstick Nano implementation details."""

from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from busylight_core.hardware import Hardware

from ._blinkstick import State
from .blinkstick_base import BlinkStickBase


class BlinkStickNano(BlinkStickBase):
    """Agile Innovative BlinkStick Nano status light controller.

    The BlinkStick Nano is a USB-connected RGB LED device with a nano form factor
    that can be controlled to display various colors and patterns for status indication.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x20A0, 0x41E5): "BlinkStick Nano",
    }

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Return True if the hardware describes a BlinkStick Nano."""
        return cls._claims(hardware, 3, 0x202)

    @cached_property
    def state(self) -> State:
        """The state of the BlinkStick Nano."""
        return State.blinkstick_nano()
