""" Embrava Blynclight Implementation Details
"""

import struct

from ...word import BitField, Word


class OffBit(BitField):
    """1 bit field to turn light off, clear to turn light on."""

    def __init__(self) -> None:
        super().__init__(17, 1)


class DimBit(BitField):
    """1 bit field to dim light, clear to brighten light."""

    def __init__(self) -> None:
        super().__init__(18, 1)


class FlashBit(BitField):
    """1 bit field to flash light, clear to stop flashing."""

    def __init__(self) -> None:
        super().__init__(19, 1)


class SpeedField(BitField):
    """3 bit field to set flash speed: 1=slow, 2=medium, 4=fast."""

    def __init__(self) -> None:
        super().__init__(20, 3)


class RepeatBit(BitField):
    """1 bit field to repeat sound, clear to play sound once."""

    def __init__(self) -> None:
        super().__init__(13, 1)


class PlayBit(BitField):
    """1 bit field to play sound, clear to stop sound."""

    def __init__(self) -> None:
        super().__init__(12, 1)


class MusicField(BitField):
    """4 bit field to select music to play, ranges from 0 to 15."""

    def __init__(self) -> None:
        super().__init__(8, 4)


class VolumeField(BitField):
    """4 bit field to set volume level, ranges from 0 to 15."""

    def __init__(self) -> None:
        super().__init__(0, 4)


class MuteBit(BitField):
    """1 bit field to mute sound, clear to enable sound."""

    def __init__(self) -> None:
        super().__init__(4, 1)


class State(Word):

    def __init__(self) -> None:
        super().__init__(0, 24)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(0x{self!s})"

    def __str__(self) -> str:
        fields = [
            f"off:    {self.off}",
            f"dim:    {self.dim}",
            f"flash:  {self.flash}",
            f"speed:  {self.speed}",
            f"repeat: {self.repeat}",
            f"play:   {self.play}",
            f"music:  {self.music}",
            f"volume: {self.volume}",
            f"mute:   {self.mute}",
        ]
        return "\n".join(fields)

    off = OffBit()
    dim = DimBit()
    flash = FlashBit()
    speed = SpeedField()
    repeat = RepeatBit()
    play = PlayBit()
    music = MusicField()
    volume = VolumeField()
    mute = MuteBit()
