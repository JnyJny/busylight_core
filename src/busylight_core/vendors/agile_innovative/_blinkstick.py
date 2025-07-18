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
        """BlinkStick State"""
        return cls(1, 1)

    @classmethod
    def blinkstick_pro(cls) -> State:
        """BlinkStick Pro State"""
        return cls(2, 192)

    @classmethod
    def blinkstick_square(cls) -> State:
        """Return the BlinkStick Square variant."""
        return cls(6, 8)

    @classmethod
    def blinkstick_strip(cls) -> State:
        """BlinkStick Strip State"""
        return cls(6, 8)

    @classmethod
    def blinkstick_nano(cls) -> State:
        """BlinkStick Nano State"""
        return cls(6, 2)

    @classmethod
    def blinkstick_flex(cls) -> State:
        """BlinkStick Flex State"""
        return cls(6, 32)

    def __init__(self, report: int, nleds: int) -> None:
        self.report = report
        self.nleds = nleds
        self.channel = 0
        self.colors: list[tuple[int, int, int]] = []

    def __bytes__(self) -> bytes:
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

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        r, g, b = value
        value = (g, r, b)
        self.colors = [value] * self.nleds

    def get_led(self, index: int) -> tuple[int, int, int]:
        """Get the color of a specific LED."""
        try:
            r, g, b = self.colors[index]
        except IndexError:
            r, g, b = (0, 0, 0)

        return (r, g, b)

    def set_led(self, index: int, color: tuple[int, int, int]) -> None:
        """Set the color of a specific LED."""
        r, g, b = color
        with contextlib.suppress(IndexError):
            self.colors[index] = (g, r, b)
