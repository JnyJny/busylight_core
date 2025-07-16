"""Busylight Omega Support"""

from typing import ClassVar

from .busylight_alpha import Busylight_Alpha


class Busylight_Omega(Busylight_Alpha):
    """Kuando Busylight Omega status light controller.

    The Busylight Omega is an enhanced version of the Busylight Alpha
    with the same functionality and keepalive requirements.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x27BB, 0x3BCD): "Busylight Omega",
        (0x27BB, 0x3BCF): "Busylight Omega",
    }
