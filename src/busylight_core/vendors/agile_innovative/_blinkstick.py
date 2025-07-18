"""Agile Innovative BlinkStick implementation details."""

from __future__ import annotations

import contextlib

from busylight_core import Light


class BaseBlinkStick(Light):
    """Base BlinkStick Implementation

    Subclasses should provide a claims classmethod and a state
    instance property that provides a properly initialized State
    instance for the specific BlinkStick variant.
    """

    @staticmethod
    def get_version(serial_number: str) -> tuple[int, int]:
        """Extract the major and minor version from the hardware serial number.

        Raises:
        - ValueError: If the serial number does not contain a valid version.

        """
        if not serial_number or not serial_number.startswith("BS"):
            msg = "Invalid BlinkStick serial number"
            raise ValueError(msg)

        try:
            return map(int, serial_number[-3:].split("."))
        except (IndexError, TypeError, ValueError):
            raise ValueError from None

    @staticmethod
    def vendor() -> str:
        """Return the vendor name for this device."""
        return "Agile Innovative"

    @property
    def name(self) -> str:
        return self.state.name

    def __bytes__(self) -> bytes:
        """Return the byte representation of the BlinkStick Square state."""
        return bytes(self.state)

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Activate the light with the given red, green, blue color tuple."""
        with self.batch_update():
            self.color = color
            if led == 0:
                self.state.color = self.color
            else:
                self.state.set_led(led - 1, color)


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
        return cls(1, 1, "BlinkStick")

    @classmethod
    def blinkstick_pro(cls) -> State:
        """Return the BlinkStick Pro state variant."""
        return cls(2, 192, "BlinkStick Pro")

    @classmethod
    def blinkstick_square(cls) -> State:
        """Return the BlinkStick Square state variant."""
        return cls(6, 8, "BlinkStick Square")

    @classmethod
    def blinkstick_strip(cls) -> State:
        """Return the BlinkStick Strip state variant."""
        return cls(6, 8, "BlinkStick Strip")

    @classmethod
    def blinkstick_nano(cls) -> State:
        """Return the BlinkStick Nano state variant."""
        return cls(6, 2, "BlinkStick Nano")

    @classmethod
    def blinkstick_flex(cls) -> State:
        """Return BlinkStick Flex state variant."""
        return cls(6, 32, "BlinkStick Flex")

    def __init__(self, report: int, nleds: int, name: str) -> None:
        self.report = report
        self.nleds = nleds
        self.name = name
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
