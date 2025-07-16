"""Bitwise operations on a word of bits."""

import array


class Word:
    """A class representing a word of bits, with methods for bit manipulation."""

    def __init__(self, value: int = 0, length: int = 8) -> None:
        """Initialize a Word of length bits with the given value."""
        if length <= 0 or length % 8 != 0:
            msg = "length must be a multiple of 8"
            raise ValueError(msg)

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
        return range(self.length)

    @property
    def hex(self) -> str:
        """Return a string hexadecimal representation of the word."""
        return f"{self.value:#0{self.length // 4}x}"

    @property
    def bin(self) -> str:
        """Return a string binary representation of the word."""
        return "0b" + bin(self.value)[2:].zfill(self.length)

    def clear(self) -> None:
        """Clear all bits in the word."""
        self.bits = array.array("B", [0] * self.length)

    def __bytes__(self) -> bytes:
        return self.value.to_bytes(self.length // 8, byteorder="big")

    def __getitem__(self, key: int | slice) -> int:
        if isinstance(key, int):
            if key not in self.range:
                msg = f"Index out of range: {key}"
                raise IndexError(msg)
            return self.bits[key]
        return sum([b << n for n, b in enumerate(self.bits[key])])

    def __setitem__(self, key: int | slice, value: bool | int) -> None:
        if isinstance(key, int):
            if key not in self.range:
                msg = f"Index out of range: {key}"
                raise IndexError(msg)
            self.bits[key] = value & 1
            return
        length = len(self.bits[key])
        new_bits = array.array("B", [value >> n & 1 for n in range(length)])
        self.bits[key] = new_bits


class ReadOnlyBitField:
    """A class representing a read-only bit field within a word."""

    def __init__(self, offset: int, width: int = 1) -> None:
        """Initialize a bitfield with the given offset and width."""
        self.field = slice(offset, offset + width)

    def __get__(self, instance: Word, owner: type | None = None) -> int:
        return instance[self.field]

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = name

    def __set__(self, instance: Word, value: int) -> None:
        msg = f"{self.name} attribute is read only"
        raise AttributeError(msg)


class BitField(ReadOnlyBitField):
    """A class representing a mutable bit field within a word."""

    def __set__(self, instance: Word, value: int) -> None:
        instance[self.field] = value
