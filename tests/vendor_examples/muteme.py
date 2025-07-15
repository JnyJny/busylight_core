""" """

from busylight_core.vendors.muteme import MuteMe, MuteMe_Mini, MuteSync

from .utils import make_hardware

muteme_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "muteme.com",
    "product_string": "MuteMe",
    "usage_page": 9,
    "usage": 6,
    "interface_number": 0,
    "bus_type": 1,
}
muteme_mini_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "muteme.com",
    "product_string": "MuteMe Mini",
    "usage_page": 9,
    "usage": 6,
    "interface_number": 0,
    "bus_type": 1,
}

mutesync_template = {
    "device_type": ConnectionType.SERIAL,
    "path": b"/BOGUS/PATH",
    "serial_number": "S7GWBRO3JUH8AF",
    "manufacturer_string": "commutesync",
    "product_string": "MuteSync Button",
    "bus_type": 1,
}


MUTEME_HARDWARE = {
    MuteMe: make_hardware(MuteMe, muteme_template),
    MuteMe_Mini: make_hardware(MuteMe_Mini, muteme_mini_template),
    MuteSync: make_hardware(MuteSync, mutesync_template),
}
