"""USB Hardware Description"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from typing import TYPE_CHECKING

import serial
from loguru import logger
from serial.tools import list_ports

if TYPE_CHECKING:
    from serial.tools.list_ports_common import ListPortInfo

from . import hid


class ConnectionType(int, Enum):
    """USB Harddware connection types."""

    ANY: int = -1
    UNKNOWN: int = 0
    HID: int = 1
    SERIAL: int = 2
    BLUETOOTH: int = 3


HardwareHandle = hid.Device | serial.Serial


@dataclass
class Hardware:
    """USB Hardware description."""

    device_type: ConnectionType
    path: bytes
    vendor_id: int
    product_id: int
    serial_number: str
    manufacturer_string: str
    product_string: str | None = None
    release_number: str | None = None
    usage: int | None = None
    usage_page: int | None = None
    interface_number: int | None = None
    bus_type: int | None = None
    is_acquired: bool = False

    @classmethod
    def enumerate(cls, by_type: ConnectionType = ConnectionType.ANY) -> list[Hardware]:
        """List of all connected hardware devices."""
        hardware_info = []

        match by_type:
            case ConnectionType.ANY:
                for connection_type in ConnectionType:
                    if connection_type <= 0:
                        continue
                    with contextlib.suppress(NotImplementedError):
                        hardware_info.extend(cls.enumerate(connection_type))
            case ConnectionType.HID:
                hardware_info.extend(
                    cls.from_hid(device_dict) for device_dict in hid.enumerate()
                )
            case ConnectionType.SERIAL:
                hardware_info.extend(
                    cls.from_portinfo(port_info) for port_info in list_ports.comports()
                )

            case _:
                msg = f"Device type {by_type} not implemented"
                raise NotImplementedError(msg)

        return hardware_info

    @classmethod
    def from_portinfo(cls, port_info: ListPortInfo) -> Hardware:
        """Create a Hardware object from a serial port info object."""
        return cls(
            device_type=ConnectionType.SERIAL,
            vendor_id=port_info.vid,
            product_id=port_info.pid,
            path=port_info.device.encode("utf-8"),
            serial_number=port_info.serial_number,
            manufacturer_string=port_info.manufacturer,
            product_string=port_info.product,
            bus_type=1,
        )

    @classmethod
    def from_hid(cls, device: dict) -> Hardware:
        """Create a Hardware object from a HID dictionary."""
        return cls(device_type=ConnectionType.HID, **device)

    @cached_property
    def device_id(self) -> tuple[int, int]:
        """A tuple of the vendor and product identifiers."""
        return (self.vendor_id, self.product_id)

    def __str__(self) -> str:
        fields = [
            f"{self.vendor_id:04x}:{self.product_id:04x}",
            self.manufacturer_string,
            self.product_string,
            self.serial_number,
            self.path.decode("utf-8"),
        ]
        return " ".join([field for field in fields if field])

    @cached_property
    def handle(self) -> HardwareHandle:
        """An I/O handle for this hardware device."""
        handle: HardwareHandle

        match self.device_type:
            case ConnectionType.HID:
                handle = hid.Device()
            case ConnectionType.SERIAL:
                handle = serial.Serial(timeout=1)
                handle.port = self.path.decode("utf-8")
            case _:
                msg = f"Device type {self.device_type} not implemented"
                raise NotImplementedError(msg)
        return handle

    def acquire(self) -> None:
        """Open the hardware device."""
        if self.is_acquired:
            logger.debug(f"{self} already acquired")
            return

        match self.device_type:
            case ConnectionType.HID:
                self.handle.open_path(self.path)
                self.is_acquired = True
            case ConnectionType.SERIAL:
                self.handle.open()
                self.is_acquired = True
            case _:
                msg = f"{self.device_type.value.title()} hardware not implemented"
                raise NotImplementedError(msg)

    def release(self) -> None:
        """Close the hardware device."""
        if not self.is_acquired:
            logger.debug(f"{self} already released")
            return

        match self.device_type:
            case ConnectionType.HID | ConnectionType.SERIAL:
                self.handle.close()
                self.is_acquired = False
            case _:
                msg = f"{self.device_type.value.title()} hardware not implemented"
                raise NotImplementedError(msg)
