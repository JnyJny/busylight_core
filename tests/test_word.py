"""
"""

import pytest
from busylight_core.word import BitField, ReadOnlyBitField, Word


@pytest.mark.parametrize("length", [8, 16, 32, 64])
def test_word_init(length: int) -> None:

    value = 1 << length - 1
    result = Word(value, length)
    assert isinstance(result, Word)
    assert result.length == length
    assert result.value == value
    assert isinstance(result.hex, str)
    assert isinstance(result.bin, str)
    assert isinstance(bytes(result), bytes)


@pytest.mark.parametrize("length", [8, 16, 32, 64])
def test_word_init_initializer_too_long(length: int) -> None:

    value = 1 << length
    result = Word(value, length)
    assert isinstance(result, Word)
    assert result.length == length
    assert result.value == 0


@pytest.mark.parametrize("value", list(range(1, 256, 16)))
def test_word_method_clear(value) -> None:

    result = Word(value, 8)

    assert result.value == value

    result.clear()

    assert result.value == 0


@pytest.mark.parametrize("value", [0, 0xFF])
def test_word_dunder_bytes(value) -> None:

    results = Word(0, 8)

    assert isinstance(bytes(results), bytes)


@pytest.mark.parametrize("value, expected", [(0, 0), (0xFF, 1)])
def test_word_dunder_getitem(value, expected) -> None:

    result = Word(value, 8)

    for i in result.range:
        assert result[i] == expected


def test_word_dunder_setitem() -> None:

    result = Word(0, 8)

    assert result.value == 0

    for i in result.range:
        result[i] = 1
        assert result.value & 1 << i


def test_word_with_ReadOnlyBitField() -> None:

    class TestWord(Word):
        readonly = ReadOnlyBitField(0, 8)

    result = TestWord(0, 8)

    assert result.readonly == 0

    with pytest.raises(AttributeError):
        result.readonly = 1


@pytest.mark.parametrize("value, expected", [(0, 0), (0xFF, 0xFF)])
def test_word_with_BitField(value, expected) -> None:

    class TestWord(Word):
        field = BitField(0, 8)

    result = TestWord(value, 8)

    assert result.field == expected

    result.field = 1

    assert result.field == 1


def test_word_with_BitField_and_ReadOnlyBitField() -> None:

    class TestWord(Word):
        field = BitField(0, 4)
        readonly = ReadOnlyBitField(4, 4)

    result = TestWord(0, 8)

    assert result.field == 0
    assert result.readonly == 0

    result.field = 1

    assert result.field == 1

    with pytest.raises(AttributeError):
        result.readonly = 1


@pytest.mark.parametrize("length", [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12])
def test_word_with_invalid_length(length: int) -> None:

    with pytest.raises(ValueError):
        Word(0, length)
