"""Luxafor vendor base class."""

from typing import ClassVar

from loguru import logger

from busylight_core.hardware import Hardware
from busylight_core.light import Light


class LuxaforBase(Light):
    """Base class for Luxafor devices.
    
    Provides common functionality for all Luxafor devices including
    the Flag, Mute, Orb, Bluetooth, and BusyTag product lines.
    """

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for Luxafor devices."""
        return "Luxafor"

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Check if this class claims the given hardware device.

        This implementation handles Luxafor's device identification pattern
        by checking the product string against supported device names.

        :param hardware: A hardware instance
        """
        if not super().claims(hardware):
            return False

        try:
            product = hardware.product_string.split()[-1].casefold()
        except (KeyError, IndexError) as error:
            logger.debug(f"problem {error} processing {hardware}")
            return False

        return product in [
            value.casefold() for value in cls.supported_device_ids.values()
        ]