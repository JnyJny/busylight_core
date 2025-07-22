"""Kuando vendor base class."""

from busylight_core.light import Light


class KuandoBase(Light):
    """Base class for Kuando devices.

    Provides common functionality for all Kuando devices,
    primarily the Busylight product line.
    """

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for Kuando devices."""
        return "Kuando"
