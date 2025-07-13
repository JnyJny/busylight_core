"""
"""

from busylight_core.hardware import ConnectionType
from busylight_core.vendors.mutesync import MuteSync

from .utils import make_hardware

mutesync_template = {
    "device_type": ConnectionType.SERIAL,
    "path": b"/BOGUS/PATH",
    "serial_number": "S7GWBRO3JUH8AF",
    "manufacturer_string": "commutesync",
    "product_string": "MuteSync Button",
    "bus_type": 1,
}


MUTESYNC_HARDWARE = {
    MuteSync: make_hardware(MuteSync, mutesync_template),
}
