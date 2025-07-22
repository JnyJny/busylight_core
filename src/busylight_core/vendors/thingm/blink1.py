"""ThingM blink(1) Support"""

from collections.abc import Callable
from functools import cached_property
from typing import ClassVar

from ._blink1 import LEDS, Action, Report, State
from .thingm_base import ThingMBase


class Blink1(ThingMBase):
    """ThingM Blink(1) USB RGB LED with feature report control.

    The Blink(1) uses HID feature reports for communication and supports
    advanced effects like fading and pattern playback. Use this class to
    control Blink(1) devices for sophisticated status indication with
    smooth color transitions and custom effects.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x27B8, 0x01ED): "Blink(1)",
    }

    @cached_property
    def state(self) -> State:
        """Device state manager for Blink(1) control.

        Returns a State instance that manages color, timing, and effect
        settings for the Blink(1). Use this to configure device behavior
        before calling update() to apply changes.

        :return: State instance for managing device properties
        """
        return State()

    def __bytes__(self) -> bytes:
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the Blink(1) with the specified color.

        :param color: RGB color tuple (red, green, blue) with values 0-255
        :param led: LED index (0 for the first LED, 1 for the second, etc.)
        """
        with self.batch_update():
            self.state.clear()
            self.state.report = Report.One
            self.state.action = Action.FadeColor
            self.state.color = color
            self.state.fade = 10  # Default fade time in milliseconds
            self.state.leds = LEDS(led)

    @property
    def color(self) -> tuple[int, int, int]:
        """Tuple of RGB color values."""
        return self.state.color

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        self.state.color = value

    @property
    def write_strategy(self) -> Callable:
        """The write strategy for communicating with the device."""
        return self.hardware.handle.send_feature_report
