"""Embrava Blynclight Support"""

from typing import ClassVar

from .embrava_base import EmbravaBase


class Blynclight(EmbravaBase):
    """Embrava Blynclight status light controller.

    The Blynclight is a USB-connected RGB LED device with additional features
    like sound playback, volume control, and flashing patterns.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x2C0D, 0x0001): "Blynclight",
        (0x2C0D, 0x000C): "Blynclight",
        (0x0E53, 0x2516): "Blynclight",
    }
