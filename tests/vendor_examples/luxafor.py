"""
"""

from busylight_core.vendors.luxafor import Bluetooth, Flag, Mute, Orb

from .utils import make_hardware

bluetooth_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "",
    "product_string": "LUXAFOR BT",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}


flag_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "",
    "product_string": "LUXAFOR FLAG",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}


mute_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "",
    "product_string": "LUXAFOR MUTE",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}


orb_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "",
    "product_string": "LUXAFOR ORB",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}

LUXAFOR_HARDWARE = {
    Bluetooth: make_hardware(Bluetooth, bluetooth_template),
    Flag: make_hardware(Flag, flag_template),
    Mute: make_hardware(Mute, mute_template),
    Orb: make_hardware(Orb, orb_template),
}
