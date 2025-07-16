""" """

from ...light import Light


class Fit_StatUSB(Light):
    supported_device_ids: dict[tuple[int, int], str] = {
        (0x2047, 0x03DF): "fit-statUSB",
    }

    @staticmethod
    def vendor() -> str:
        return "CompuLab"

    def __bytes__(self) -> bytes:
        buf = f"B#{self.red:02x}{self.green:02x}{self.blue:02x}\n"

        return buf.encode()

    def on(self, color: tuple[int, int, int], led: int = 0) -> None:
        with self.batch_update():
            self.color = color
