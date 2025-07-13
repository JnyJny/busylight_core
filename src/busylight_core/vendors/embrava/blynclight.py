""" """

import struct
from enum import Enum
from functools import cached_property

from loguru import logger

from ...light import Light
from ._blynclight import State


class FlashSpeed(int, Enum):
    slow: int = 1
    medium: int = 2
    fast: int = 4


class Blynclight(Light):

    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x2C0D, 0x0001): "Blynclight",
            (0x2C0D, 0x000C): "Blynclight",
            (0x0E53, 0x2516): "Blynclight",
        }

    @cached_property
    def state(self) -> State:
        return State()

    @cached_property
    def struct(self) -> struct.Struct:
        return struct.Struct("!xBBBBBBH")

    def __bytes__(self) -> bytes:

        self.state.off = not self.is_lit

        if self.state.flash and self.state.off:
            self.state.flash = False

        if self.state.dim and self.state.off:
            self.state.dim = False

        return self.struct.pack(
            self.red,
            self.blue,
            self.green,
            *bytes(self.state),
            0xFF22,
        )

    def dim(self) -> None:

        with self.batch_update():
            self.state.dim = True

    def bright(self) -> None:

        with self.batch_update():
            self.state.dim = False

    def play_sound(
        self,
        music: int = 0,
        volume: int = 1,
        repeat: bool = False,
    ) -> None:

        with self.batch_update():
            self.state.repeat = repeat
            self.state.play = True
            self.state.music = music
            self.state.mute = False

    def stop_sound(self) -> None:

        with self.batch_update():
            self.state.play = False

    def mute(self) -> None:

        with self.batch_update():
            self.state.mute = True

    def unmute(self) -> None:

        with self.batch_update():
            self.state.mute = False

    def flash(self, color: tuple[int, int, int], speed: FlashSpeed = None) -> None:

        speed = speed or FlashSpeed.slow

        with self.batch_update():
            self.color = color
            self.state.flash = True
            self.state.speed = speed.value

    def stop_flashing(self) -> None:

        with self.batch_update():
            self.state.flash = False

    def reset(self) -> None:

        with self.batch_update():
            self.state.off = True
            self.state.dim = False
            self.state.flash = False
            self.state.speed = FlashSpeed.slow.value
            self.state.play = False
            self.state.mute = False
            self.state.repeat = False
            self.state.music = 0
            self.state.volume = 0

        super().reset()
