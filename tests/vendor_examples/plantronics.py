""" """

from busylight_core.vendors.plantronics import Status_Indicator

from .utils import make_hardware

status_indicator_template = {
    "path": b"/BOGUS/PATH",
    "serial_number": "",
    "release_number": 1,
    "manufacturer_string": "",
    "product_string": "Plantronics Status Indicator",
    "usage_page": 65280,
    "usage": 1,
    "interface_number": 0,
    "bus_type": 1,
}

PLANTRONICS_HARDWARE = {
    Status_Indicator: make_hardware(Status_Indicator, status_indicator_template),
}
