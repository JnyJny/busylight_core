"""
"""

import pytest
from busylight_core.hardware import ConnectionType, Hardware
from serial.tools import list_ports_common

# test enumerate classmethod


def test_hardware_classmethod_enumerate_without_args() -> None:

    results = Hardware.enumerate()

    assert isinstance(results, list)
    for item in results:
        assert isinstance(item, Hardware)


@pytest.mark.parametrize(
    "connection, implemented",
    [
        (ConnectionType.ANY, True),
        (ConnectionType.UNKNOWN, False),
        (ConnectionType.HID, True),
        (ConnectionType.SERIAL, True),
        (ConnectionType.BLUETOOTH, False),
    ],
)
def test_hardware_classmethod_enumerate_by_connection_type(
    connection,
    implemented,
) -> None:

    if not implemented:
        with pytest.raises(NotImplementedError):
            results = Hardware.enumerate(connection)
    else:
        results = Hardware.enumerate(connection)

        assert isinstance(results, list)
        for item in results:
            assert isinstance(item, Hardware)
            assert item.device_type in ConnectionType


def test_hardware_classmethod_from_portinfo(hardware_serial_device) -> None:

    assert isinstance(hardware_serial_device, Hardware)
    assert hardware_serial_device.vendor_id == 0x9999
    assert hardware_serial_device.product_id == 0x9999
    assert hardware_serial_device.serial_number == "12345678"
    assert hardware_serial_device.device_type == ConnectionType.SERIAL
    assert hardware_serial_device.bus_type == 1
    assert "test" in hardware_serial_device.manufacturer_string.lower()
    assert isinstance(hardware_serial_device.path, bytes)
    assert hardware_serial_device.device_id == (
        hardware_serial_device.vendor_id,
        hardware_serial_device.product_id,
    )


def test_hardware_classmethod_from_hid(hardware_hid_device) -> None:

    assert isinstance(hardware_hid_device, Hardware)
    assert hardware_hid_device.vendor_id == 0x9999
    assert hardware_hid_device.product_id == 0x9999
    assert hardware_hid_device.serial_number == "12345678"
    assert hardware_hid_device.device_type == ConnectionType.HID
    assert hardware_hid_device.bus_type == 0
    assert "test" in hardware_hid_device.manufacturer_string.lower()
    assert "test" in hardware_hid_device.product_string.lower()
    assert isinstance(hardware_hid_device.path, bytes)
    assert hardware_hid_device.device_id == (
        hardware_hid_device.vendor_id,
        hardware_hid_device.product_id,
    )


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.parametrize("hardware", [None])
def test_hardware_property_handle(hardware: Hardware) -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.parametrize("hardware", [None])
def test_hardware_method_acquire(hardware: Hardware) -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
@pytest.mark.parametrize("hardware", [None])
def test_hardware_method_release(hardware: Hardware) -> None:
    pass
