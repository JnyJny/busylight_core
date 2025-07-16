"""Luxafor Flag device implementation details."""

from enum import Enum

from loguru import logger


class Command(int, Enum):
    Color: int = 1
    Fade: int = 2
    Strobe: int = 3
    Wave: int = 4
    Pattern: int = 6


class LEDS(int, Enum):
    All: int = 0xFF
    Back: int = 0x41
    Front: int = 0x42
    LED1: int = 0x1
    LED2: int = 0x2
    LED3: int = 0x3
    LED4: int = 0x4
    LED5: int = 0x5
    LED6: int = 0x6


class Pattern(int, Enum):
    Off: int = 0
    TrafficLight: int = 1
    Random1: int = 2
    Random2: int = 3
    Random3: int = 4
    Police: int = 5
    Random4: int = 6
    Random5: int = 7
    Rainbow: int = 8


class Wave(int, Enum):
    Off: int = 0
    Short: int = 1
    Long: int = 2
    ShortOverLapping: int = 3
    LongOverlapping: int = 4
    WAVE5: int = 5


class State:
    def __init__(self) -> None:
        self.command = Command.Color
        self.leds = LEDS.All
        self.fade = 0
        self.repeat = 0
        self.pattern = Pattern.Off
        self.wave = Wave.Off
        self.color = (0, 0, 0)

    def __bytes__(self) -> bytes:
        match self.command:
            case Command.Color:
                return bytes([self.command, self.leds, *self.color])
            case Command.Fade:
                return bytes(
                    [self.command, self.leds, *self.color, self.fade, self.repeat]
                )
            case _:
                pass

        logger.debug(f"Unsupported command: {self.command}")
        msg = f"Unsupported command: {self.command}"
        raise ValueError(msg)
