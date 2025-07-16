""" """

from busylight_core.vendors.kuando import Busylight_Alpha, Busylight_Omega

from .utils import make_hardware

busylight_alpha_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "PLENOM APS",
    "product_string": "BUSYLIGHT ALPHA",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}

busylight_omega_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 256,
    "manufacturer_string": "PLENOM APS",
    "product_string": "BUSYLIGHT OMEGA",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}

KUANDO_HARDWARE = {
    Busylight_Alpha: make_hardware(Busylight_Alpha, busylight_alpha_template),
    Busylight_Omega: make_hardware(Busylight_Omega, busylight_omega_template),
}
