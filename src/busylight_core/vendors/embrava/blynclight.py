"""Embrava Blynclight Support"""

from functools import cached_property
from typing import ClassVar

from busylight_core.light import Light

from ._blynclight import FlashSpeed, State


class Blynclight(Light):
    """Embrava Blynclight status light controller.

    The Blynclight is a USB-connected RGB LED device with additional features
    like sound playback, volume control, and flashing patterns.
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {
        (0x2C0D, 0x0001): "Blynclight",
        (0x2C0D, 0x000C): "Blynclight",
        (0x0E53, 0x2516): "Blynclight",
    }

    @cached_property
    def state(self) -> State:
        """Get the device state manager for controlling light behavior."""
        return State()

    def __bytes__(self) -> bytes:
        if not self.is_lit:
            self.state.off = True
            self.state.flash = False
            self.state.dim = False

        return bytes([0, *bytes(self.state), 0xFF, 0x22])

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the Blynclight with the specified color.

        :param value: RGB color tuple (red, green, blue)
        """
        with self.batch_update():
            self.color = color

    @property
    def color(self) -> tuple[int, int, int]:
        """Get the current RGB color of the Blynclight."""
        return (self.state.red, self.state.green, self.state.blue)

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        self.state.red, self.state.green, self.state.blue = value

    def dim(self) -> None:
        """Set the light to dim mode (reduced brightness)."""
        with self.batch_update():
            self.state.dim = True

    def bright(self) -> None:
        """Set the light to bright mode (full brightness)."""
        with self.batch_update():
            self.state.dim = False

    def play_sound(
        self,
        music: int = 0,
        volume: int = 1,
        repeat: bool = False,
    ) -> None:
        """Play a sound on the Blynclight device.

        :param music: Music track number to play (0-7)
        :param volume: Volume level (0-3)
        :param repeat: Whether the music repeats
        """
        with self.batch_update():
            self.state.repeat = repeat
            self.state.play = True
            self.state.music = music
            self.state.mute = False
            self.state.volume = volume

    def stop_sound(self) -> None:
        """Stop playing any currently playing sound."""
        with self.batch_update():
            self.state.play = False

    def mute(self) -> None:
        """Mute the device sound output."""
        with self.batch_update():
            self.state.mute = True

    def unmute(self) -> None:
        """Unmute the device sound output."""
        with self.batch_update():
            self.state.mute = False

    def flash(self, color: tuple[int, int, int], speed: FlashSpeed = None) -> None:
        """Flash the light with the specified color and speed.

        :param color: RGB color tuple to flash
        :param speed: Flashing speed (default is slow)

        """
        speed = speed or FlashSpeed.slow

        with self.batch_update():
            self.color = color
            self.state.flash = True
            self.state.speed = speed.value

    def stop_flashing(self) -> None:
        """Stop the flashing pattern and return to solid color."""
        with self.batch_update():
            self.state.flash = False

    def reset(self) -> None:
        """Reset the device to its default state (off, no sound)."""
        self.state.reset()
        self.update()
