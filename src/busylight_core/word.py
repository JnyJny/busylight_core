""" """

import array
import struct


class Word:
    def __init__(self, value: int = 0, length: int = 8) -> None:

        if length <= 0 or length % 8 != 0:
            raise ValueError("length must be a multiple of 8")

        self.initial_value = value
        self.length = length
        self.bits = array.array("B", [(value >> n) & 1 for n in self.range])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.hex})"

    def __str__(self) -> str:
        return self.hex

    @property
    def value(self) -> int:
        """Return the integer value of the word."""
        return sum([b << n for n, b in enumerate(self.bits)])

    @property
    def range(self) -> range:
        """Return the range of bit offsets for this word."""
        return range(0, self.length)

    @property
    def hex(self) -> str:
        return f"{self.value:#0{self.length // 4}x}"

    @property
    def bin(self) -> str:
        return "0b" + bin(self.value)[2:].zfill(self.length)

    def clear(self) -> None:
        """Clear all bits in the word."""
        self.bits = array.array("B", [0] * self.length)

    def __bytes__(self) -> bytes:
        return self.value.to_bytes(self.length // 8, byteorder="big")

    def __getitem__(self, key: int | slice) -> int:
        if isinstance(key, int):
            if key not in self.range:
                raise IndexError(f"Index out of range: {key}")
            return self.bits[key]
        return sum([b << n for n, b in enumerate(self.bits[key])])

    def __setitem__(self, key: int | slice, value: bool | int) -> None:
        if isinstance(key, int):
            if key not in self.range:
                raise IndexError(f"Index out of range: {key}")
            self.bits[key] = value & 1
            return
        length = len(self.bits[key])
        new_bits = array.array("B", [value >> n & 1 for n in range(length)])
        self.bits[key] = new_bits


class ReadOnlyBitField:
    def __init__(self, offset: int, width: int = 1) -> None:
        self.field = slice(offset, offset + width)

    def __get__(self, obj, type=None) -> int:
        return obj[self.field]

    def __set_name__(self, owner, name: str) -> None:
        self.name = name

    def __set__(self, obj, value: int) -> None:
        raise AttributeError(f"{self.name} attribute is read only")


class BitField(ReadOnlyBitField):
    def __set__(self, obj, value: int) -> None:
        obj[self.field] = value
