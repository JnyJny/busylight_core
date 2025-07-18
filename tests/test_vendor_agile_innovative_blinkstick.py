"""Tests for Agile Innovative BlinkStick implementation."""

from unittest.mock import Mock

import pytest

from busylight_core.hardware import ConnectionType, Hardware
from busylight_core.vendors.agile_innovative import BlinkStickSquare


class TestBlinkStickSquare:
    """Test the BlinkStickSquare class."""

    @pytest.fixture
    def mock_hardware(self) -> Hardware:
        """Create mock hardware for BlinkStick Square"""
        hardware = Mock(spec=Hardware)
        hardware.vendor_id = 0x20A0
        hardware.product_id = 0x41E5
        hardware.device_id = (0x20A0, 0x41E5)
        hardware.serial_number = "BS123456-3.0"
        hardware.release_number = 0x100
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware

    def test_vendor_method(self) -> None:
        """Test vendor() method returns correct vendor name."""
        assert BlinkStickSquare.vendor() == "Agile Innovative"

    def test_supported_device_ids(self) -> None:
        """Test supported_device_ids contains expected devices."""
        device_ids = BlinkStickSquare.supported_device_ids
        assert (0x20A0, 0x41E5) in device_ids
        assert device_ids[(0x20A0, 0x41E5)] == "BlinkStick Square"
