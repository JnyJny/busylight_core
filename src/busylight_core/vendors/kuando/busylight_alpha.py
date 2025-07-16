"""Busylight Alpha Support"""

import asyncio
from functools import cached_property

from ...light import Light
from ._busylight import State


class Busylight_Alpha(Light):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x04D8, 0xF848): "Busylight Alpha",
        (0x27BB, 0x3BCA): "Busylight Alpha",
        (0x27BB, 0x3BCB): "Busylight Alpha",
        (0x27BB, 0x3BCE): "Busylight Alpha",
    }

    @cached_property
    def state(self) -> State:
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        self.color = color
        with self.batch_update():
            self.state.steps[0].jump(self.color)
        self.add_task("keepalive", _keepalive)

    def off(self, led: int = 0) -> None:
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
        raise ValueError("Keepalive interval must be between 0 and 15 seconds.")

    sleep_interval = round(interval / 2)

    while True:
        with light.batch_update():
            light.state.steps[0].keepalive(interval)
        await asyncio.sleep(sleep_interval)
