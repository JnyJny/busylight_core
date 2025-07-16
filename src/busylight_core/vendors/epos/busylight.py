"""EPOS Busylight Support"""

from functools import cached_property

from ...light import Light
from ._busylight import State


class Busylight(Light):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x1395, 0x0074): "Busylight",
    }

    @staticmethod
    def vendor() -> str:
        return "EPOS"

    @cached_property
    def state(self) -> State:
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        self.color = color
        with self.batch_update():
            self.state.set_color(color, led)

    def reset(self) -> None:
        self.state.reset()
        super().reset()
