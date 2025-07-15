"""BusyTag Light Support"""

from ...light import Light

# https://luxafor.helpscoutdocs.com/article/47-busy-tag-usb-cdc-command-reference-guide


class BusyTag(Light):

    @staticmethod
    def supported_device_ids() -> dict[tuple[int, int], str]:
        return {
            (0x303A, 0x81DF): "Busy Tag",
        }

    @staticmethod
    def vendor() -> str:
        return "Busy Tag"

    def __bytes__(self) -> bytes:

        cmd = f"AT+SC=127,{self.red:02x}{self.green:02x}{self.blue:02x}"

        return buf.encode()
