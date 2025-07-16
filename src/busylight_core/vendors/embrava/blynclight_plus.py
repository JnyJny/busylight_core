"""Embrava Blynclight Plus Support"""

from typing import ClassVar

from .blynclight import Blynclight


class Blynclight_Plus(Blynclight):
    """Embrava Blynclight Plus status light controller.

    An enhanced version of the Blynclight with additional features
    while maintaining the same basic functionality.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x2C0D, 0x0002): "Blynclight Plus",
        (0x2C0D, 0x0010): "Blynclight Plus",
    }
