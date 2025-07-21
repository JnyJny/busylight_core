"""Embrava Blynclight Mini Support"""

from typing import ClassVar

from .embrava_base import EmbravaBase


class BlynclightMini(EmbravaBase):
    """Embrava Blynclight Mini status light controller.

    A smaller version of the Blynclight with the same functionality
    as the standard Blynclight device.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x2C0D, 0x000A): "Blynclight Mini",
        (0x0E53, 0x2517): "Blynclight Mini",
    }
