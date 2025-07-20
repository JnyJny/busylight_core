"""Tests for Kuando Busylight Alpha device-specific functionality."""

from unittest.mock import Mock

import pytest

from busylight_core.hardware import ConnectionType, Hardware
from busylight_core.vendors.kuando import Busylight_Alpha


class TestKuandoBusylightAlpha:
    """Test the Busylight Alpha device-specific functionality."""

    @pytest.fixture
    def mock_hardware(self) -> Hardware:
        """Create mock hardware for testing Alpha-specific device IDs."""
        hardware = Mock(spec=Hardware)
        hardware.vendor_id = 0x04D8
        hardware.product_id = 0xF848
        hardware.device_id = (0x04D8, 0xF848)
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware

    @pytest.fixture
    def busylight(self, mock_hardware) -> Busylight_Alpha:
        """Create a Busylight_Alpha instance for testing."""
        # Mock the hardware handle methods
        mock_hardware.handle = Mock()
        mock_hardware.handle.write = Mock(return_value=64)
        mock_hardware.handle.read = Mock(return_value=b"\x00" * 64)

        return Busylight_Alpha(mock_hardware, reset=False, exclusive=False)

    def test_supported_device_ids(self) -> None:
        """Test Alpha supported_device_ids contains expected devices."""
        device_ids = Busylight_Alpha.supported_device_ids
        assert (0x04D8, 0xF848) in device_ids
        assert (0x27BB, 0x3BCA) in device_ids
        assert (0x27BB, 0x3BCB) in device_ids
        assert (0x27BB, 0x3BCE) in device_ids
        assert all("Busylight Alpha" in name for name in device_ids.values())
        # Ensure these are Alpha-specific and not Omega IDs
        assert (0x27BB, 0x3BCD) not in device_ids  # Omega ID
        assert (0x27BB, 0x3BCF) not in device_ids  # Omega ID

    def test_vendor_method(self, busylight) -> None:
        """Test vendor() method returns correct vendor name."""
        assert busylight.vendor() == "Kuando"

    def test_claims_method_with_alpha_hardware(self, mock_hardware) -> None:
        """Test claims() method with Alpha-specific hardware."""
        # Test with Alpha device ID
        mock_hardware.device_id = (0x04D8, 0xF848)
        assert Busylight_Alpha.claims(mock_hardware) is True

        # Test with another Alpha device ID
        mock_hardware.device_id = (0x27BB, 0x3BCA)
        assert Busylight_Alpha.claims(mock_hardware) is True

        # Test with Omega device ID (should not claim)
        mock_hardware.device_id = (0x27BB, 0x3BCD)
        assert Busylight_Alpha.claims(mock_hardware) is False

        # Test with unknown device ID
        mock_hardware.device_id = (0x1234, 0x5678)
        assert Busylight_Alpha.claims(mock_hardware) is False
