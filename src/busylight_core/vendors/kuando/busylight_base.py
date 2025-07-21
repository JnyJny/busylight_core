"""Kuando Busylight Base Implementation"""

import asyncio
from functools import cached_property

from busylight_core.mixins import ColorableMixin

from ._busylight import State
from .kuando_base import KuandoBase


class BusylightBase(ColorableMixin, KuandoBase):
    """Base Busylight implementation."""

    @cached_property
    def state(self) -> State:
        """The device state manager."""
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the Busylight with the specified color.

        :param color: RGB color tuple (red, green, blue) with values 0-255
        :param led: LED index (unused for Busylight Alpha)
        """
        self.color = color
        with self.batch_update():
            self.state.steps[0].jump(self.color)
        self.add_task("keepalive", _keepalive)

    def off(self, led: int = 0) -> None:
        """Turn off the Busylight.

        :param led: LED index (unused for Busylight Alpha)
        """
        self.color = (0, 0, 0)
        with self.batch_update():
            self.state.steps[0].jump(self.color)
        self.cancel_task("keepalive")


async def _keepalive(light: BusylightBase, interval: int = 15) -> None:
    """Send a keep alive packet to a Busylight.

    The hardware will be configured for a keep alive interval of
    `interval` seconds, and an asyncio sleep for half that time will
    be used to schedule the next keep alive packet update.
    """
    if interval not in range(16):
        msg = "Keepalive interval must be between 0 and 15 seconds."
        raise ValueError(msg)

    sleep_interval = round(interval / 2)

    while True:
        with light.batch_update():
            light.state.steps[0].keep_alive(interval)
        await asyncio.sleep(sleep_interval)
