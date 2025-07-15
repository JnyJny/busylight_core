""" """

from busylight_core import Light
from busylight_core.hardware import ConnectionType, Hardware


def make_hardware(
    subclass: Light,
    template: dict[str, str | bytes | int],
) -> list[Hardware]:
    for (v, p), name in subclass.supported_device_ids.items():
        match template.get("device_type", ConnectionType.HID):
            case ConnectionType.HID:
                yield Hardware.from_hid({**template, "vendor_id": v, "product_id": p})
            case ConnectionType.SERIAL:
                yield Hardware(**{**template, "vendor_id": v, "product_id": p})
