"""Test configuration and shared fixtures."""

import pytest
from serial.tools.list_ports_common import ListPortInfo

from busylight_core.hardware import Hardware


@pytest.fixture
def serial_device_info() -> ListPortInfo:
    """Create a mock serial device info for testing."""
    info = ListPortInfo("/BOGUS/PATH")
    info.description = "Test Port"
    info.hwid = "USB VID:PID=9999:9999"
    info.manufacturer = "Test Manufacturer"
    info.product = "Test Product"
    info.vid = 0x9999
    info.pid = 0x9999
    info.serial_number = "12345678"
    return info


@pytest.fixture
def hid_device_info() -> dict:
    """Create a mock HID device info for testing."""
    return {
        "path": b"/BOGUS/PATH",
        "vendor_id": 0x9999,
        "product_id": 0x9999,
        "serial_number": "12345678",
        "manufacturer_string": "Test Manufacturer",
        "product_string": "Test Product",
        "usage_page": 0x01,
        "usage": 0x02,
        "interface_number": 0,
        "bus_type": 0,
    }


@pytest.fixture
def hardware_hid_device(hid_device_info) -> Hardware:
    """Create a mock HID hardware device for testing."""
    return Hardware.from_hid(hid_device_info)


@pytest.fixture
def hardware_serial_device(serial_device_info) -> Hardware:
    """Create a mock serial hardware device for testing."""
    return Hardware.from_portinfo(serial_device_info)


@pytest.fixture
def hardware_devices(hardware_hid_device, hardware_serial_device) -> list[Hardware]:
    """Create a list of mock hardware devices for testing."""
    return [hardware_hid_device, hardware_serial_device]
