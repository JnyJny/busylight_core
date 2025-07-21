"""Hardware examples for Embrava busylight devices.

This module provides mock hardware definitions for testing Embrava
busylight devices, including the Blynclight product line.
"""

from busylight_core.vendors.embrava import Blynclight, BlynclightMini, BlynclightPlus

from .utils import make_hardware

blynclight_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "",
    "product_string": "Blynclight",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}

blynclight_mini_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "",
    "product_string": "Blynclight Mini",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}

blynclight_plus_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "",
    "product_string": "Blynclight Plus",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}


EMBRAVA_HARDWARE = {
    Blynclight: make_hardware(Blynclight, blynclight_template),
    BlynclightMini: make_hardware(BlynclightMini, blynclight_mini_template),
    BlynclightPlus: make_hardware(BlynclightPlus, blynclight_plus_template),
}
