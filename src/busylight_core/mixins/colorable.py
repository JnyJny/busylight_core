"""
"""


class ColorableMixin:

    @property
    def red(self) -> int:
        """Red color value."""
        return getattr(self, "_red", 0)

    @red.setter
    def red(self, value: int):
        self._red = value

    @property
    def green(self) -> int:
        """Green color value."""
        return getattr(self, "_green", 0)

    @green.setter
    def green(self, value: int):
        self._green = value

    @property
    def blue(self) -> int:
        """Blue color value."""
        return getattr(self, "_blue", 0)

    @blue.setter
    def blue(self, value: int):
        self._blue = value

    @property
    def color(self) -> tuple[int, int, int]:
        """A tuple of red, green, and blue color values."""
        return self.red, self.green, self.blue

    @color.setter
    def color(self, value: tuple[int, int, int]):
        self.red, self.green, self.blue = value

    @property
    def is_lit(self) -> bool:
        """True if any color value is greater than 0."""
        return any(self.color)
