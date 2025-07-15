"""BusyTag Light Support"""

from functools import cached_property
from ...light import Light
from ._busytag import Command


class BusyTag(Light):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x303A, 0x81DF): "Busy Tag",
    }

    @staticmethod
    def vendor() -> str:
        return "Busy Tag"

    @property
    def command(self) -> str:
        return getattr(self, "_command", "")

    @command.setter
    def command(self, value: str) -> None:
        self._command = value

    def __bytes__(self) -> bytes:
        return self.command.encode()

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        with self.batch_update():
            self.color = color
            self.command = Command.solid_color(color, led)
