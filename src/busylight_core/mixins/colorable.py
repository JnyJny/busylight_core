"""Color manipulation mixin for Light classes."""


class ColorableMixin:
    """Mixin providing color properties."""

    red = property(
        lambda self: getattr(self, "_red", 0),
        lambda self, value: setattr(self, "_red", value),
        doc="Red color value.",
    )

    green = property(
        lambda self: getattr(self, "_green", 0),
        lambda self, value: setattr(self, "_green", value),
        doc="Green color value.",
    )

    blue = property(
        lambda self: getattr(self, "_blue", 0),
        lambda self, value: setattr(self, "_blue", value),
        doc="Blue color value.",
    )

    @property
    def color(self) -> tuple[int, int, int]:
        """Tuple of RGB color values."""
        return (self.red, self.green, self.blue)

    @color.setter
    def color(self, value: tuple[int, int, int]) -> None:
        self.red, self.green, self.blue = value
