"""Embrava Blynclight Support"""

import struct
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

    @cached_property
    def struct(self) -> struct.Struct:
        """Get the binary struct formatter for device communication."""
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

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        """Turn on the Blynclight with the specified color.

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            led: LED index (unused for Blynclight)

        """
        with self.batch_update():
            self.color = color

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

        Args:
            music: Sound ID to play (0-9)
            volume: Volume level (1-10)
            repeat: Whether to repeat the sound continuously

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

        Args:
            color: RGB color tuple (red, green, blue) with values 0-255
            speed: Flash speed (slow, medium, fast) - defaults to slow

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
        self.color = (0, 0, 0)
        self.update()
