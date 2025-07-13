"""ThingM blink(1) Support"""

from functools import cached_property
from typing import Callable

from loguru import logger

from ...light import Light
from ._blink1 import LEDS, Action, Report, State


class Blink1(Light):
    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x27B8, 0x01ED): "Blink(1)",
        }

    @staticmethod
    def vendor() -> str:
        return "ThingM"

    @cached_property
    def state(self) -> State:
        return State()

    @property
    def action(self) -> Action:
        return getattr(self, "_action", Action.FadeColor)

    @action.setter
    def action(self, action: Action) -> None:
        self._action = action

    def __bytes__(self) -> bytes:

        match self.action:
            case Action.FadeColor:
                self.state.fade_to_color(self.color)
            case _:
                raise NotImplementedError(f"Action {self.action} not implemented")
        return bytes(self.state)

    def on(self, color: tuple[int, int, int]) -> None:

        self.action = Action.FadeColor
        super().on(color)

    @property
    def write_strategy(self) -> Callable:
        return self.hardware.handle.send_feature_report
