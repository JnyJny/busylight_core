"""EPOS Busylight Implementation Details"""

from enum import Enum

from busylight_core.word import BitField, Word


class Action(int, Enum):
    SetColor = 0x1202


class Report(int, Enum):
    ONE: int = 1


class ReportField(BitField):
    """An 8-bit report field."""


class ActionField(BitField):
    """An 8-bit action."""


class ColorField(BitField):
    """An 8-bit color value."""


class OnField(BitField):
    """A 1-bit field that toggles the light on."""


class State(Word):
    def __init__(self) -> None:
        super().__init__(0, 80)

    report = ReportField(72, 8)
    action = ActionField(56, 16)

    red0 = ColorField(48, 8)
    green0 = ColorField(40, 8)
    blue0 = ColorField(32, 8)

    red1 = ColorField(24, 8)
    green1 = ColorField(16, 8)
    blue1 = ColorField(8, 8)

    on = OnField(0, 8)

    def set_color(
        self,
        color: tuple[int, int, int],
        led: int = 0,
    ) -> None:
        """Set color for the specified LED."""
        self.report = Report.ONE
        self.action = Action.SetColor
        match led:
            case 0:
                self.color = color
            case 1:
                self.color0 = color
            case 2:
                self.color1 = color

    @property
    def color0(self) -> tuple[int, int, int]:
        """Return the first color as a tuple of RGB values."""
        return (self.red0, self.green0, self.blue0)

    @color0.setter
    def color0(self, color: tuple[int, int, int]) -> None:
        self.red0, self.green0, self.blue0 = color

    @property
    def color1(self) -> tuple[int, int, int]:
        """Return the second color as a tuple of RGB values."""
        return (self.red1, self.green1, self.blue1)

    @color1.setter
    def color1(self, color: tuple[int, int, int]) -> None:
        self.red1, self.green1, self.blue1 = color

    @property
    def color(self) -> tuple[int, int, int]:
        return self.color0

    @color.setter
    def color(self, color: tuple[int, int, int]) -> None:
        self.color0 = color
        self.color1 = color

    def reset(self) -> None:
        """Reset state to default value."""
        self.report = 0
        self.action = 0
        self.red0 = 0
        self.green0 = 0
        self.blue0 = 0
        self.red1 = 0
        self.green1 = 0
        self.blue1 = 0
        self.on = 0
