"""Tests for EPOS Busylight implementation."""

from unittest.mock import Mock, patch

import pytest

from busylight_core.hardware import ConnectionType, Hardware
from busylight_core.vendors.epos import Busylight
from busylight_core.vendors.epos._busylight import Action, Report, State


class TestEPOSBusylightState:
    """Test the State class for EPOS Busylight."""

    def test_state_initialization(self):
        """Test that State initializes with correct default values."""
        state = State()
        assert state.report == 0
        assert state.action == 0
        assert state.red0 == 0
        assert state.green0 == 0
        assert state.blue0 == 0
        assert state.red1 == 0
        assert state.green1 == 0
        assert state.blue1 == 0
        assert state.on == 0
        assert state.color0 == (0, 0, 0)
        assert state.color1 == (0, 0, 0)
        assert state.color == (0, 0, 0)

    def test_state_color0_property(self):
        """Test color0 property getter and setter."""
        state = State()
        color = (255, 128, 64)
        state.color0 = color
        assert state.color0 == color
        assert state.red0 == 255
        assert state.green0 == 128
        assert state.blue0 == 64

    def test_state_color1_property(self):
        """Test color1 property getter and setter."""
        state = State()
        color = (128, 255, 32)
        state.color1 = color
        assert state.color1 == color
        assert state.red1 == 128
        assert state.green1 == 255
        assert state.blue1 == 32

    def test_state_color_property(self):
        """Test color property getter and setter."""
        state = State()
        color = (200, 100, 50)
        state.color = color
        # Setting color should set both color0 and color1
        assert state.color == color
        assert state.color0 == color
        assert state.color1 == color

    def test_state_set_color_led_0(self):
        """Test set_color with LED 0 (default)."""
        state = State()
        color = (255, 0, 128)
        state.set_color(color, led=0)
        assert state.report == Report.ONE
        assert state.action == Action.SetColor
        assert state.color0 == color
        assert state.color1 == color  # color property sets both

    def test_state_set_color_led_1(self):
        """Test set_color with LED 1."""
        state = State()
        color = (128, 255, 0)
        state.set_color(color, led=1)
        assert state.report == Report.ONE
        assert state.action == Action.SetColor
        assert state.color0 == color
        assert state.color1 == (0, 0, 0)  # color0 property only affects first LED

    def test_state_set_color_led_2(self):
        """Test set_color with LED 2."""
        state = State()
        color = (0, 128, 255)
        state.set_color(color, led=2)
        assert state.report == Report.ONE
        assert state.action == Action.SetColor
        assert state.color0 == (0, 0, 0)  # color1 property only affects second LED
        assert state.color1 == color

    def test_state_reset(self):
        """Test state reset functionality."""
        state = State()
        # Set some values
        state.report = Report.ONE
        state.action = Action.SetColor
        state.color0 = (255, 255, 255)
        state.color1 = (128, 128, 128)
        state.on = 1

        # Reset should clear all fields
        state.reset()
        assert state.report == 0
        assert state.action == 0
        assert state.red0 == 0
        assert state.green0 == 0
        assert state.blue0 == 0
        assert state.red1 == 0
        assert state.green1 == 0
        assert state.blue1 == 0
        assert state.on == 0
        assert state.color0 == (0, 0, 0)
        assert state.color1 == (0, 0, 0)


class TestEPOSBusylight:
    """Test the main Busylight class."""

    @pytest.fixture
    def mock_hardware(self):
        """Create mock hardware for testing."""
        hardware = Mock(spec=Hardware)
        hardware.vendor_id = 0x1395
        hardware.product_id = 0x0074
        hardware.device_id = (0x1395, 0x0074)  # Add device_id property
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware

    @pytest.fixture
    def busylight(self, mock_hardware):
        """Create a Busylight instance for testing."""
        # Mock the hardware handle methods
        mock_hardware.handle = Mock()
        mock_hardware.handle.write = Mock(return_value=10)
        mock_hardware.handle.read = Mock(return_value=b"\x00" * 10)

        return Busylight(mock_hardware, reset=False, exclusive=False)

    def test_vendor_method(self):
        """Test vendor() method returns correct vendor name."""
        assert Busylight.vendor() == "EPOS"

    def test_supported_device_ids(self):
        """Test supported_device_ids contains expected devices."""
        device_ids = Busylight.supported_device_ids
        assert (0x1395, 0x0074) in device_ids
        assert device_ids[(0x1395, 0x0074)] == "Busylight"

    def test_state_property(self, busylight):
        """Test state property returns State instance."""
        assert isinstance(busylight.state, State)
        # Should be cached
        assert busylight.state is busylight.state

    def test_bytes_method(self, busylight):
        """Test __bytes__ method returns state bytes."""
        # Test that __bytes__ returns the state as bytes
        state_bytes = bytes(busylight)
        expected_bytes = bytes(busylight.state)
        assert state_bytes == expected_bytes
        assert len(state_bytes) == 10  # State should be 80 bits / 8 = 10 bytes

    def test_on_method_default_led(self, busylight):
        """Test on() method with default LED."""
        color = (255, 128, 64)
        with (
            patch.object(busylight, "batch_update") as mock_batch,
            patch.object(busylight.state, "set_color") as mock_set_color,
        ):
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            busylight.on(color)

            assert busylight.color == color
            mock_set_color.assert_called_once_with(color, 0)
            mock_batch.assert_called_once()

    def test_on_method_specific_led(self, busylight):
        """Test on() method with specific LED."""
        color = (128, 255, 32)
        led = 1
        with (
            patch.object(busylight, "batch_update") as mock_batch,
            patch.object(busylight.state, "set_color") as mock_set_color,
        ):
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            busylight.on(color, led=led)

            assert busylight.color == color
            mock_set_color.assert_called_once_with(color, led)
            mock_batch.assert_called_once()

    def test_reset_method(self, busylight):
        """Test reset() method calls state.reset() and super().reset()."""
        with (
            patch.object(busylight.state, "reset") as mock_state_reset,
            patch.object(busylight.__class__.__bases__[0], "reset") as mock_super_reset,
        ):
            busylight.reset()

            mock_state_reset.assert_called_once()
            mock_super_reset.assert_called_once()

    def test_on_method_updates_internal_color(self, busylight):
        """Test that on() method updates the internal color state."""
        color = (200, 100, 50)
        with patch.object(busylight, "batch_update") as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            busylight.on(color)

            # Check that the state was properly updated
            assert busylight.state.color == color
            assert busylight.state.report == Report.ONE
            assert busylight.state.action == Action.SetColor

    def test_different_led_targets(self, busylight):
        """Test that different LED targets affect the correct color fields."""
        color1 = (255, 0, 0)
        color2 = (0, 255, 0)
        color3 = (0, 0, 255)

        with patch.object(busylight, "batch_update") as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            # Test LED 0 (should set both color0 and color1)
            busylight.on(color1, led=0)
            assert busylight.state.color0 == color1
            assert busylight.state.color1 == color1

            # Reset state
            busylight.state.reset()

            # Test LED 1 (should set only color0)
            busylight.on(color2, led=1)
            assert busylight.state.color0 == color2
            assert busylight.state.color1 == (0, 0, 0)

            # Reset state
            busylight.state.reset()

            # Test LED 2 (should set only color1)
            busylight.on(color3, led=2)
            assert busylight.state.color0 == (0, 0, 0)
            assert busylight.state.color1 == color3
