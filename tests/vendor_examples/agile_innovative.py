"""
"""

from busylight_core.vendors.agile_innovative import BlinkStick

from .utils import make_hardware

blinkstick_square_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "BS032974-3.0",
    "release_number": 512,
    "manufacturer_string": "Agile Innovative Ltd",
    "product_string": "BlinkStick",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}

AGILE_INNOVATIVE_HARDWARE = {
    BlinkStick: make_hardware(BlinkStick, blinkstick_square_template),
}
