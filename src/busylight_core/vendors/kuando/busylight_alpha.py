"""Busylight Alpha Support"""

import asyncio
from functools import cached_property
from typing import ClassVar

from busylight_core.light import Light

from ._busylight import State


class Busylight_Alpha(Light):
    """Kuando Busylight Alpha status light controller.

    The Busylight Alpha is a USB-connected RGB LED device that requires
    periodic keepalive messages to maintain its connection state.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x04D8, 0xF848): "Busylight Alpha",
        (0x27BB, 0x3BCA): "Busylight Alpha",
        (0x27BB, 0x3BCB): "Busylight Alpha",
        (0x27BB, 0x3BCE): "Busylight Alpha",
    }

    @cached_property
    def state(self) -> State:
        """Get the device state manager for controlling light patterns."""
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the Busylight Alpha with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index (unused for Busylight Alpha)

        """
        self.color = color
        with self.batch_update():
            self.state.steps[0].jump(self.color)
        self.add_task("keepalive", _keepalive)

    def off(self, led: int = 0) -> None:
        """Turn off the Busylight Alpha.

        Args:
            led: LED index (unused for Busylight Alpha)

        """
        self.color = (0, 0, 0)
        with self.batch_update():
            self.state.steps[0].jump(self.color)
        self.cancel_task("keepalive")


async def _keepalive(light: Busylight_Alpha, interval: int = 15) -> None:
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
