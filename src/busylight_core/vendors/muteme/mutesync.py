"""
"""

from loguru import logger

from ...hardware import Hardware
from ...light import Light


class MuteSync(Light):
    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x10C4, 0xEA60): "MuteSync Button",
        }

    @staticmethod
    def vendor() -> str:
        return "MuteSync"

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Returns True if the hardware describes a MuteSync Button."""

        # Addresses issue #356 where MuteSync claims another hardware with
        # a SiliconLabs CP2102 USB to Serial controller that is not a MuteSync
        # hardware.

        claim = super().claims(hardware)

        vendor = cls.vendor().lower()

        try:
            manufacturer = vendor in hardware.manufacturer_string.lower()
        except AttributeError:
            manufacturer = False

        try:
            product = vendor in hardware.product_string.lower()
        except AttributeError:
            product = False

        return claim and (product or manufacturer)

    def __bytes__(self) -> bytes:

        buf = [65] + [*self.color] * 4

        return bytes(buf)

    @property
    def is_button(self) -> bool:
        return True

    @property
    def button_on(self) -> bool:
        return False
