"""ThingM Blink(1) device implementation details."""

from enum import Enum

from busylight_core.word import BitField, Word


class Action(int, Enum):
    FadeColor = ord("c")
    SetColor = ord("n")
    ReadColor = ord("r")
    ServerTickle = ord("D")
    PlayLoop = ord("p")
    PlayStateRead = ord("S")
    SetColorPattern = ord("P")
    SaveColorPatterns = ord("W")
    ReadColorPattern = ord("R")
    SetLEDn = ord("l")
    ReadEEPROM = ord("e")
    WriteEEPROM = ord("E")
    GetVersion = ord("v")
    TestCommand = ord("!")
    WriteNote = ord("F")
    ReadNote = ord("f")
    Bootloader = ord("G")
    LockBootLoader = ord("L")
    SetStartupParams = ord("B")
    GetStartupParams = ord("b")
    ServerModeTickle = ord("D")
    GetChipID = ord("U")


class LEDS(int, Enum):
    All = 0
    Top = 1
    Bottom = 2


class Report(int, Enum):
    One = 1
    Two = 2


class ReportField(BitField):
    """8-bit report field."""

    def __init__(self) -> None:
        super().__init__(56, 8)


class ActionField(BitField):
    """8-bit action field."""

    def __init__(self) -> None:
        super().__init__(48, 8)


class RedField(BitField):
    """8-bit red field."""

    def __init__(self) -> None:
        super().__init__(40, 8)


class GreenField(BitField):
    """8-bit green field."""

    def __init__(self) -> None:
        super().__init__(32, 8)


class BlueField(BitField):
    """8-bit blue field."""

    def __init__(self) -> None:
        super().__init__(24, 8)


class PlayField(BitField):
    """8-bit play field."""

    def __init__(self) -> None:
        super().__init__(40, 8)


class StartField(BitField):
    """8-bit start field."""

    def __init__(self) -> None:
        super().__init__(32, 8)


class StopField(BitField):
    """8-bit stop field."""

    def __init__(self) -> None:
        super().__init__(24, 8)


class CountField(BitField):
    """8-bit count field."""

    def __init__(self) -> None:
        super().__init__(16, 8)


class FadeField(BitField):
    """16-bit fade field."""

    def __init__(self) -> None:
        super().__init__(8, 16)


class LedsField(BitField):
    """8-bit led field."""

    def __init__(self) -> None:
        super().__init__(0, 8)


class LinesField(BitField):
    """8-bit line field."""

    def __init__(self) -> None:
        super().__init__(0, 8)


class State(Word):
    def __init__(self) -> None:
        super().__init__(0, 64)

    report = ReportField()
    action = ActionField()
    red = RedField()
    green = GreenField()
    blue = BlueField()
    play = PlayField()  # alias for red
    start = StartField()  # alias for green
    stop = StopField()  # alias for blue
    count = CountField()
    fade = FadeField()
    leds = LedsField()
    line = LinesField()  # alias for leds

    @property
    def color(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    @color.setter
    def color(self, values: tuple[int, int, int]) -> None:
        self.red, self.green, self.blue = values

    def fade_to_color(
        self,
        color: tuple[int, int, int],
        fade_ms: int = 10,
        leds: LEDS = LEDS.All,
    ) -> None:
        self.clear()
        self.report = Report.One
        self.action = Action.FadeColor
        self.color = color
        self.fade = fade_ms
        self.leds = leds

    def write_pattern_line(
        self,
        color: tuple[int, int, int],
        fade_ms: int,
        index: int,
    ) -> None:
        self.clear()
        self.report = Report.One
        self.action = Action.SetColorPattern
        self.color = color
        self.fade = fade_ms
        self.line = index

    def save_patterns(self) -> None:
        self.clear()
        self.report = Report.One
        self.action = Action.SaveColorPatterns
        self.color = (0xBE, 0xEF, 0xCA)
        self.count = 0xFE

    def play_loop(self, play: int, start: int, stop: int, count: int = 0) -> None:
        self.clear()
        self.report = Report.One
        self.action = Action.PlayLoop
        self.play = play
        self.start = start
        self.stop = stop
        self.count = count

    def clear_patterns(self, start: int = 0, count: int = 16) -> None:
        for index in range(start, start + count):
            self.write_pattern_line((0, 0, 0), 0, index)
