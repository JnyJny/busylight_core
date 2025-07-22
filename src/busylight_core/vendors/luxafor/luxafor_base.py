"""Luxafor vendor base class."""

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
    def claims(cls, hardware: Hardware, product_check: bool = True) -> bool:
        """Return True if the hardware matches Luxafor criteria.

        The product_check argument will short-circuit checking
        the hardware product string for Luxafor device names.
        This is used primarily by the busytag implementation
        which does not require the product string check.

        :param hardware: The Hardware instance to check.
        :product_check: Whether to check the product string.
        """
        result = super().claims(hardware)

        if not product_check:
            return result

        if not result:
            return False

        try:
            product = hardware.product_string.split()[-1].casefold()
        except (KeyError, IndexError) as error:
            logger.debug(f"problem {error} processing {hardware}")
            return False

        return product in [
            value.casefold() for value in cls.supported_device_ids.values()
        ]
