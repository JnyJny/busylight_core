"""ThingM blink(1) Support"""

from functools import cached_property
from typing import Callable

from loguru import logger

from ...light import Light
from ._blink1 import LEDS, State


class Blink1(Light):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x27B8, 0x01ED): "Blink(1)",
    }

    @staticmethod
    def vendor() -> str:
        return "ThingM"

    @cached_property
    def state(self) -> State:
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        self.color = color
        with self.batch_update():
            self.state.fade_to_color(self.color, leds=LEDS(led))

    @property
    def write_strategy(self) -> Callable:
        return self.hardware.handle.send_feature_report
