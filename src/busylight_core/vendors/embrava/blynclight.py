"""Embrava Blynclight Support"""

from typing import ClassVar

from .embrava_base import EmbravaBase


class Blynclight(EmbravaBase):
    """Embrava Blynclight USB status light with audio capabilities.

    The Blynclight combines RGB LED status indication with built-in
    audio playback, volume control, and flashing patterns. Use this
    class to control standard Blynclight devices for comprehensive
    audiovisual status notifications.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x2C0D, 0x0001): "Blynclight",
        (0x2C0D, 0x000C): "Blynclight",
        (0x0E53, 0x2516): "Blynclight",
    }
