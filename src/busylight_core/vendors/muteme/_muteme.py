"""MuteMe Implementation Details"""

from busylight_core.word import BitField, Word


class OneBitField(BitField):
    def __get__(self, instance: Word, owner: type | None = None) -> int:
        return 0xFF if super().__get__(instance, owner) else 0

    def __set__(self, instance: Word, value: int) -> None:
        super().__set__(instance, int(bool(value)))


class RedBit(OneBitField):
    """1-bit red color field"""

    def __init__(self) -> None:
        super().__init__(0, 1)


class GreenBit(OneBitField):
    """1-bit green color field"""

    def __init__(self) -> None:
        super().__init__(1, 1)


class BlueBit(OneBitField):
    """1-bit blue color field"""

    def __init__(self) -> None:
        super().__init__(2, 1)


class DimBit(OneBitField):
    """1-bit dim field"""

    def __init__(self) -> None:
        super().__init__(4, 1)


class BlinkBit(OneBitField):
    """1-bit blink field"""

    def __init__(self) -> None:
        super().__init__(5, 1)


class SleepBit(OneBitField):
    """1-bit sleep field"""

    def __init__(self) -> None:
        super().__init__(6, 1)


class State(Word):
    """MuteMe state word"""

    red = RedBit()
    green = GreenBit()
    blue = BlueBit()
    dim = DimBit()
    blink = BlinkBit()
    sleep = SleepBit()

    @property
    def color(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    @color.setter
    def color(self, values: tuple[int, int, int]) -> None:
        self.red, self.green, self.blue = values
