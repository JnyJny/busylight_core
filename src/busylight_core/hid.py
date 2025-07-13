"""USB Human Interface Device (HID) Porcelain.

Why This File Exists.

The 'apmorton/pyhidapi' package and 'trezor/cython-hidapi' packages
both occupy the namespace hid when installed. Regardless of install
order, apmorton/pyhidapi wins and overwrites cython-hidapi in the
directory */lib/python3*/site-packages/hid. The two packages provide
similar support for performing IO to USB human interface devices with
small but significant differences. Since I cannot control which
package is installed first, I've provided a wrapper around the two
packages that allows either to be used without changing the consumer
code.

I originally picked the trezor/cython-hidapi package for HID support
because it does not require the user to install additional non-Python
software.  The pyhidapi package is a ctypes interface to the hidapi
shared object which the user must install in an operation separate
from the `pip install`.

Both cython-hidapi and pyhidapi support a function `enumerate` which
returns a list of dictionaries, each dictionary describing discovered
USB devices.

The Device class in this module wallpapers over the differences
between cython-hidapi::hid.device and pyhidapi::hid.Device, favoring
the open() semantics of hid.device since it requires fewer changes to
the consumer in this package.

Hopefully at some point in the future the two projects can come to an
agreement and remove the namespace collision.

"""

from functools import cached_property

from loguru import logger

import hid


def enumerate() -> list[dict]:
    """Return a list of dictionaries, each describing a USB device."""

    return [dict(**d) for d in hid.enumerate()]


class Device:
    def __init__(self) -> None:
        try:
            self._handle = hid.device()
        except AttributeError:
            self._handle = None
        self._is_open = False

    @property
    def is_open(self) -> bool:
        """Return True if the device is open."""
        return self._is_open

    @property
    def error(self) -> str:
        """Return the last error message."""
        try:
            return self._handle.error()
        except IOError as error:
            return str(error)

    def open(
        self,
        vendor_id: int,
        product_id: int,
        serial_number: str | None = None,
    ) -> None:
        """Open the first device matching vendor_id and product_id or
        serial number.

        If the device is already open, raises IOError.
        """

        if self.is_open:
            raise IOError("device already open")

        if self._handle:
            self._handle.open(vendor_id, product_id, serial_number)
        else:
            self._handle = hid.Device(
                vid=vendor_id,
                pid=product_id,
                serial=serial_number,
            )
        self._is_open = True

    def open_path(self, path: bytes | str) -> None:
        """Open the device specified by path.

        If the device is already open, raises IOError.
        """

        if self.is_open:
            raise IOError("device already open")

        if isinstance(path, str):
            path = path.encode("utf-8")

        logger.debug(f"opening device at path {path!r}")

        if self._handle:
            # hidapi
            self._handle.open_path(path)
        else:
            # pyhidapi
            self._handle = hid.Device(path=path)
        self._is_open = True

    def close(self) -> None:
        """Close this device."""
        try:
            self._handle.close()
            self._is_open = False
        except AttributeError:
            raise IOError("device not open") from None

    def read(self, nbytes: int, timeout_ms: int | None = None) -> list[int]:
        """Read nbytes from the device, returns a list of ints."""

        if not self.is_open:
            raise IOError("device not open")

        return self._handle.read(nbytes, timeout_ms)

    def write(self, buf: bytes) -> int:
        """Write bytes in buf to the device."""

        if not self.is_open:
            raise IOError("device not open")

        return self._handle.write(buf)

    def get_feature_report(self, report: int, nbytes: int) -> list[int]:
        """Read a nbytes feature report from the device."""

        if not self.is_open:
            raise IOError("device not open")

        return self._handle.get_feature_report(report, nbytes)

    def send_feature_report(self, buf: bytes) -> int:
        """Write bytes in buf using device feature report."""

        if not self.is_open:
            raise IOError("device not open")

        return self._handle.send_feature_report(buf)
