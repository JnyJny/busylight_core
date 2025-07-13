""" """

from pathlib import Path
import toml
import pytest
from busylight_core.hardware import ConnectionType, Hardware
from serial.tools.list_ports_common import ListPortInfo


@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the root path of the project."""
    yield Path.cwd()


@pytest.fixture(scope="session")
def pyproject_path(project_root: Path) -> Path:
    """Return the path to the pyproject.toml file."""
    yield project_root / "pyproject.toml"


@pytest.fixture(scope="session")
def pyproject_toml(pyproject_path: Path) -> dict:
    """Return the contents of the pyproject.toml file."""
    yield toml.load(pyproject_path.open("rb"))


@pytest.fixture(scope="session")
def project_version(pyproject_toml: dict) -> str:
    """Return the project version from pyproject.toml."""
    return pyproject_toml["project"]["version"]


@pytest.fixture
def serial_device_info() -> ListPortInfo:
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
    return Hardware.from_hid(hid_device_info)


@pytest.fixture
def hardware_serial_device(serial_device_info) -> Hardware:
    return Hardware.from_PortInfo(serial_device_info)


@pytest.fixture
def hardware_devices(hardware_hid_device, hardware_serial_device) -> list[Hardware]:
    return [hardware_hid_device, hardware_serial_device]
