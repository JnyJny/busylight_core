"""
"""

from busylight_core.hardware import ConnectionType
from busylight_core.vendors.compulab import Fit_StatUSB

from .utils import make_hardware

fit_statusb_template = {
    "device_type": ConnectionType.SERIAL,
    "path": b"/BOGUS/PATH",
    "serial_number": "193F914722000800",
    "manufacturer_string": "Compulab LTD",
    "product_string": "fit_StatUSB",
    "bus_type": 1,
}


COMPULAB_HARDWARE = {
    Fit_StatUSB: make_hardware(Fit_StatUSB, fit_statusb_template),
}
