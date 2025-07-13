"""
"""

from busylight_core.vendors.embrava import Blynclight, Blynclight_Mini, Blynclight_Plus

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
    Blynclight_Mini: make_hardware(Blynclight_Mini, blynclight_mini_template),
    Blynclight_Plus: make_hardware(Blynclight_Plus, blynclight_plus_template),
}
