"""Kuando Busylight device implementation details."""

from __future__ import annotations

import struct
from enum import Enum

from busylight_core.word import BitField, Word


class Ring(int, Enum):
    Off: int = 0
    OpenOffice: int = 136
    Quiet: int = 144
    Funky: int = 152
    FairyTale: int = 160
    KuandoTrain: int = 168
    TelephoneNordic: int = 176
    TelephoneOriginal: int = 184
    TelephonePickMeUp: int = 192
    Buzz: int = 216


class OpCode(int, Enum):
    Jump: int = 0x1
    Reset: int = 0x2
    Boot: int = 0x4
    KeepAlive: int = 0x8


class OpCodeField(BitField):
    """4-bit opcode"""

    def __init__(self) -> None:
        super().__init__(60, 4)


class OperandField(BitField):
    """4-bit operand"""

    def __init__(self) -> None:
        super().__init__(56, 4)


class BodyField(BitField):
    """56-bit body"""

    def __init__(self) -> None:
        super().__init__(0, 56)


class RepeatField(BitField):
    """8-bit repeat"""

    def __init__(self) -> None:
        super().__init__(48, 8)


class ScaledColorField(BitField):
    """A scaled color field."""

    def __get__(self, instance: Word | None, owner: type | None = None) -> int:
        if instance is None:
            return self
        return (instance[self.field] / 100) * 0xFF

    def __set__(self, instance: Word, value: int) -> None:
        instance[self.field] = int((value / 0xFF) * 100)


class RedField(ScaledColorField):
    """8-bit red color."""

    def __init__(self) -> None:
        super().__init__(40, 8)


class GreenField(ScaledColorField):
    """8-bit green color."""

    def __init__(self) -> None:
        super().__init__(32, 8)


class BlueField(ScaledColorField):
    """8-bit blue color."""

    def __init__(self) -> None:
        super().__init__(24, 8)


class DutyCycleOnField(BitField):
    """8-bit duty cycle on"""

    def __init__(self) -> None:
        super().__init__(16, 8)


class DutyCycleOffField(BitField):
    """8-bit duty cycle off"""

    def __init__(self) -> None:
        super().__init__(8, 8)


class UpdateBit(BitField):
    """1-bit update"""

    def __init__(self) -> None:
        super().__init__(7, 1)


class RingtoneField(BitField):
    """4-bit ringtone"""

    def __init__(self) -> None:
        super().__init__(3, 4)


class VolumeField(BitField):
    """3-bit volume"""

    def __init__(self) -> None:
        super().__init__(0, 3)


class Step(Word):
    def __init__(self) -> None:
        super().__init__(0, 64)

    def keep_alive(self, timeout: int) -> None:
        """Configure the step as a KeepAlive with timeout in seconds."""
        self.opcode = OpCode.KeepAlive
        self.operand = timeout & 0xF
        self.body = 0

    def boot(self) -> None:
        """Configure the step as a Boot instruction."""
        self.opcode = OpCode.Boot
        self.operand = 0
        self.body = 0

    def reset(self) -> None:
        """Configure the step as a Reset instruction."""
        self.opcode = OpCode.Reset
        self.operand = 0
        self.body = 0

    def jump(
        self,
        color: tuple[int, int, int],
        target: int = 0,
        repeat: int = 0,
        on_time: int = 0,
        off_time: int = 0,
        update: int = 0,
        ringtone: Ring = Ring.Off,
        volume: int = 0,
    ) -> None:
        """Configure the step as a Jump instruction."""
        self.opcode = OpCode.Jump
        self.operand = target & 0xF
        self.repeat = repeat & 0xFF
        self.color = color
        self.duty_cycle_on = on_time & 0xFF
        self.duty_cycle_off = off_time & 0xFF
        self.update = update & 0x1
        self.ringtone = ringtone & 0xF
        self.volume = volume & 0x3

    @property
    def color(self) -> tuple[int, int, int]:
        return (self.red, self.green, self.blue)

    @color.setter
    def color(self, color: tuple[int, int, int]) -> None:
        self.red, self.green, self.blue = color

    opcode = OpCodeField()
    operand = OperandField()
    body = BodyField()
    repeat = RepeatField()
    red = RedField()
    green = GreenField()
    blue = BlueField()
    duty_cycle_on = DutyCycleOnField()
    duty_cycle_off = DutyCycleOffField()
    update = UpdateBit()
    ringtone = RingtoneField()
    volume = VolumeField()


class SensitivityField(BitField):
    """8-bit sensitivity"""

    def __init__(self) -> None:
        super().__init__(56, 8)


class TimeoutField(BitField):
    """8-bit timeout"""

    def __init__(self) -> None:
        super().__init__(48, 8)


class TriggerField(BitField):
    """8-bit trigger"""

    def __init__(self) -> None:
        super().__init__(40, 8)


class ChecksumField(BitField):
    """16-bit checksum"""

    def __init__(self) -> None:
        super().__init__(0, 16)


class Footer(Step):
    def __init__(self) -> None:
        super().__init__()
        self.checksum = 0
        self.pad = 0xFFF

    sensitivity = SensitivityField()
    timeout = TimeoutField()
    trigger = TriggerField()
    pad = BitField(16, 24)
    checksum = ChecksumField()


class State:
    def __init__(self) -> None:
        self.steps = [Step() for _ in range(7)]
        self.footer = Footer()
        self.struct = struct.Struct("!8Q")

    def __bytes__(self) -> bytes:
        self.footer.checksum = sum(bytes(self.footer)[:-2])
        for step in self.steps:
            self.footer.checksum += sum(bytes(step))

        return self.struct.pack(
            *[step.value for step in self.steps],
            self.footer.value,
        )
