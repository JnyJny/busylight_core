"""Agile Innovative BlinkStick implementation details."""

from __future__ import annotations

import contextlib


class State:
    """BlinkStick State

    These devices store their colors as Green, Red, Blue tuples
    rather than the more common Red, Green, Blue tuples. Colors
    are transposed automatically if you use the color property
    or the set_led() method.
    """

    @classmethod
    def blinkstick(cls) -> State:
        """Return the BlinkStick state variant."""
        return cls(report=1, nleds=1)

    @classmethod
    def blinkstick_pro(cls) -> State:
        """Return the BlinkStick Pro state variant."""
        return cls(report=2, nleds=192)

    @classmethod
    def blinkstick_square(cls) -> State:
        """Return the BlinkStick Square state variant."""
        return cls(report=6, nleds=8)

    @classmethod
    def blinkstick_strip(cls) -> State:
        """Return the BlinkStick Strip state variant."""
        return cls(report=6, nleds=8)

    @classmethod
    def blinkstick_nano(cls) -> State:
        """Return the BlinkStick Nano state variant."""
        return cls(report=6, nleds=2)

    @classmethod
    def blinkstick_flex(cls) -> State:
        """Return BlinkStick Flex state variant."""
        return cls(report=6, nleds=32)

    def __init__(self, *, report: int, nleds: int) -> None:
        self.report = report
        self.nleds = nleds
        self.channel = 0
        self.colors: list[tuple[int, int, int]] = [(0, 0, 0)] * nleds

    def __bytes__(self) -> bytes:
        # EJO there is a bug here WRT versions of BlinkStick that
        #     don't require the channel in the command word. Also,
        #     I don't have a solid understanding of what channel
        #     controls. This works for BlinkStick Square which I
        #     can test.
        buf = [self.report, self.channel]
        for color in self.colors:
            buf.extend(color)
        return bytes(buf)

    @property
    def color(self) -> tuple[int, int, int]:
        """Get the current color of the BlinkStick."""
        for color in self.colors:
            if sum(color) > 0:
                g, r, b = color
                return (r, g, b)
        return (0, 0, 0)

    @staticmethod
    def rgb_to_grb(color: tuple[int, int, int]) -> tuple[int, int, int]:
        """Convert a RGB color tuple to an internal GRB representation."""
        r, g, b = color
        return (g, r, b)

    @staticmethod
    def grb_to_rgb(color: tuple[int, int, int]) -> tuple[int, int, int]:
        """Convert an internal GRB color tuple to RGB representation."""
        g, r, b = color
        return (r, g, b)

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        self.colors = [self.rgb_to_grb(value)] * self.nleds

    def get_led(self, index: int) -> tuple[int, int, int]:
        """Get the RGB color of a specific LED."""
        try:
            return self.grb_to_rgb(self.colors[index])
        except IndexError:
            return (0, 0, 0)

    def set_led(self, index: int, color: tuple[int, int, int]) -> None:
        """Set the RGB color of a specific LED."""
        with contextlib.suppress(IndexError):
            self.colors[index] = self.rgb_to_grb(color)
