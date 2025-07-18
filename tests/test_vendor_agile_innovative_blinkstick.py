"""Tests for Agile Innovative BlinkStick implementation."""

from unittest.mock import Mock, patch

import pytest

from busylight_core.hardware import ConnectionType, Hardware
from busylight_core.vendors.agile_innovative import BlinkStickSquare
from busylight_core.vendors.agile_innovative._blinkstick import State


class TestBlinkStickState:
    """Test the BlinkStick State class."""

    def test_state_initialization(self) -> None:
        """Test State initializes with correct parameters."""
        state = State(1, 8)
        assert state.report == 1
        assert state.nleds == 8
        assert state.channel == 0
        assert state.colors == []

    def test_state_blinkstick_factory(self) -> None:
        """Test blinkstick() factory method."""
        state = State.blinkstick()
        assert state.report == 1
        assert state.nleds == 1
        assert state.channel == 0
        assert state.colors == []

    def test_state_blinkstick_pro_factory(self) -> None:
        """Test blinkstick_pro() factory method."""
        state = State.blinkstick_pro()
        assert state.report == 2
        assert state.nleds == 192
        assert state.channel == 0
        assert state.colors == []

    def test_state_blinkstick_square_factory(self) -> None:
        """Test blinkstick_square() factory method."""
        state = State.blinkstick_square()
        assert state.report == 6
        assert state.nleds == 8
        assert state.channel == 0
        assert state.colors == []

    def test_state_blinkstick_strip_factory(self) -> None:
        """Test blinkstick_strip() factory method."""
        state = State.blinkstick_strip()
        assert state.report == 6
        assert state.nleds == 8
        assert state.channel == 0
        assert state.colors == []

    def test_state_blinkstick_nano_factory(self) -> None:
        """Test blinkstick_nano() factory method."""
        state = State.blinkstick_nano()
        assert state.report == 6
        assert state.nleds == 2
        assert state.channel == 0
        assert state.colors == []

    def test_state_blinkstick_flex_factory(self) -> None:
        """Test blinkstick_flex() factory method."""
        state = State.blinkstick_flex()
        assert state.report == 6
        assert state.nleds == 32
        assert state.channel == 0
        assert state.colors == []

    def test_state_color_property_getter_empty(self) -> None:
        """Test color property getter with empty colors."""
        state = State(1, 4)
        assert state.color == (0, 0, 0)

    def test_state_color_property_getter_with_colors(self) -> None:
        """Test color property getter with colors set."""
        state = State(1, 4)
        # Set colors in GRB format internally
        state.colors = [(0, 0, 0), (128, 255, 64), (0, 0, 0), (0, 0, 0)]
        # Should return first non-zero color converted to RGB
        assert state.color == (255, 128, 64)  # GRB (128, 255, 64) -> RGB (255, 128, 64)

    def test_state_color_property_getter_all_zero(self) -> None:
        """Test color property getter with all zero colors."""
        state = State(1, 4)
        state.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        assert state.color == (0, 0, 0)

    def test_state_color_property_setter(self) -> None:
        """Test color property setter converts RGB to GRB."""
        state = State(1, 4)
        state.color = (255, 128, 64)  # RGB
        # Should be converted to GRB and set for all LEDs
        expected_grb = (128, 255, 64)  # GRB format
        assert state.colors == [expected_grb, expected_grb, expected_grb, expected_grb]

    def test_state_get_led_valid_index(self) -> None:
        """Test get_led() with valid index."""
        state = State(1, 4)
        state.colors = [(128, 255, 64), (0, 128, 255), (255, 0, 128), (64, 32, 16)]
        # Should return RGB format (converted from internal GRB)
        assert state.get_led(0) == (
            255,
            128,
            64,
        )  # GRB (128, 255, 64) -> RGB (255, 128, 64)
        assert state.get_led(1) == (
            128,
            0,
            255,
        )  # GRB (0, 128, 255) -> RGB (128, 0, 255)
        assert state.get_led(2) == (
            0,
            255,
            128,
        )  # GRB (255, 0, 128) -> RGB (0, 255, 128)
        assert state.get_led(3) == (32, 64, 16)  # GRB (64, 32, 16) -> RGB (32, 64, 16)

    def test_state_get_led_invalid_index(self) -> None:
        """Test get_led() with invalid index returns (0, 0, 0)."""
        state = State(1, 4)
        state.colors = [(128, 255, 64), (0, 128, 255)]
        assert state.get_led(5) == (0, 0, 0)  # Index out of range
        assert state.get_led(10) == (0, 0, 0)  # Index out of range

    def test_state_set_led_valid_index(self) -> None:
        """Test set_led() with valid index."""
        state = State(1, 4)
        state.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]
        state.set_led(1, (255, 128, 64))  # RGB input
        # Should be converted to GRB and set at index 1
        expected_grb = (128, 255, 64)
        assert state.colors[1] == expected_grb
        assert state.colors[0] == (0, 0, 0)  # Other LEDs unchanged
        assert state.colors[2] == (0, 0, 0)
        assert state.colors[3] == (0, 0, 0)

    def test_state_set_led_invalid_index(self) -> None:
        """Test set_led() with invalid index (should be suppressed)."""
        state = State(1, 2)
        state.colors = [(0, 0, 0), (0, 0, 0)]
        # Should not raise IndexError due to contextlib.suppress
        state.set_led(5, (255, 128, 64))
        # Colors should remain unchanged
        assert state.colors == [(0, 0, 0), (0, 0, 0)]

    def test_state_bytes_empty(self) -> None:
        """Test __bytes__() with empty colors."""
        state = State(1, 4)
        result = bytes(state)
        expected = bytes([1, 0])  # [report, channel]
        assert result == expected

    def test_state_bytes_with_colors(self) -> None:
        """Test __bytes__() with colors set."""
        state = State(6, 3)
        state.colors = [(128, 255, 64), (0, 128, 255), (255, 0, 128)]
        result = bytes(state)
        expected = bytes(
            [6, 0, 128, 255, 64, 0, 128, 255, 255, 0, 128]
        )  # [report, channel] + colors
        assert result == expected

    def test_state_bytes_single_led(self) -> None:
        """Test __bytes__() with single LED."""
        state = State(1, 1)
        state.colors = [(100, 200, 50)]
        result = bytes(state)
        expected = bytes([1, 0, 100, 200, 50])  # [report, channel] + single color
        assert result == expected

    def test_state_rgb_grb_conversion_consistency(self) -> None:
        """Test RGB to GRB conversion consistency."""
        state = State(1, 1)
        rgb_color = (255, 128, 64)
        state.color = rgb_color
        retrieved_color = state.color
        assert retrieved_color == rgb_color

    def test_state_multiple_led_operations(self) -> None:
        """Test operations with multiple LEDs."""
        state = State(6, 4)
        # Initialize colors array first
        state.colors = [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)]

        # Set individual LEDs
        state.set_led(0, (255, 0, 0))  # Red -> stored as (0, 255, 0) in GRB
        state.set_led(1, (0, 255, 0))  # Green -> stored as (255, 0, 0) in GRB
        state.set_led(2, (0, 0, 255))  # Blue -> stored as (0, 0, 255) in GRB
        state.set_led(3, (255, 255, 0))  # Yellow -> stored as (255, 255, 0) in GRB

        # Verify individual LEDs (returned in RGB format, converted from internal GRB)
        assert state.get_led(0) == (255, 0, 0)  # RGB format
        assert state.get_led(1) == (0, 255, 0)  # RGB format
        assert state.get_led(2) == (0, 0, 255)  # RGB format
        assert state.get_led(3) == (255, 255, 0)  # RGB format

        # Verify color property returns first non-zero converted to RGB
        assert state.color == (255, 0, 0)  # First LED returns RGB

    def test_state_color_property_overrides_individual_leds(self) -> None:
        """Test that setting color property overrides individual LED colors."""
        state = State(1, 4)
        # Set individual LEDs first
        state.set_led(0, (255, 0, 0))
        state.set_led(1, (0, 255, 0))
        state.set_led(2, (0, 0, 255))
        state.set_led(3, (255, 255, 0))

        # Set color property - should override all
        state.color = (128, 64, 32)
        expected_grb = (64, 128, 32)
        assert state.colors == [expected_grb, expected_grb, expected_grb, expected_grb]

    def test_state_rgb_to_grb_conversion(self) -> None:
        """Test rgb_to_grb() static method."""
        # Test various RGB colors
        assert State.rgb_to_grb((255, 128, 64)) == (128, 255, 64)  # RGB -> GRB
        assert State.rgb_to_grb((0, 255, 0)) == (255, 0, 0)  # Green -> GRB
        assert State.rgb_to_grb((255, 0, 0)) == (0, 255, 0)  # Red -> GRB
        assert State.rgb_to_grb((0, 0, 255)) == (0, 0, 255)  # Blue -> GRB
        assert State.rgb_to_grb((255, 255, 255)) == (255, 255, 255)  # White -> GRB
        assert State.rgb_to_grb((0, 0, 0)) == (0, 0, 0)  # Black -> GRB

    def test_state_grb_to_rgb_conversion(self) -> None:
        """Test grb_to_rgb() static method."""
        # Test various GRB colors
        assert State.grb_to_rgb((128, 255, 64)) == (255, 128, 64)  # GRB -> RGB
        assert State.grb_to_rgb((255, 0, 0)) == (0, 255, 0)  # GRB -> Green
        assert State.grb_to_rgb((0, 255, 0)) == (255, 0, 0)  # GRB -> Red
        assert State.grb_to_rgb((0, 0, 255)) == (0, 0, 255)  # GRB -> Blue
        assert State.grb_to_rgb((255, 255, 255)) == (255, 255, 255)  # GRB -> White
        assert State.grb_to_rgb((0, 0, 0)) == (0, 0, 0)  # GRB -> Black

    def test_state_color_conversion_roundtrip(self) -> None:
        """Test that RGB -> GRB -> RGB conversion is consistent."""
        test_colors = [
            (255, 128, 64),
            (0, 255, 0),
            (255, 0, 0),
            (0, 0, 255),
            (255, 255, 255),
            (0, 0, 0),
            (128, 64, 192),
        ]

        for rgb_color in test_colors:
            grb_color = State.rgb_to_grb(rgb_color)
            converted_back = State.grb_to_rgb(grb_color)
            assert converted_back == rgb_color


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
        hardware.release_number = 0x200
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware

    @pytest.fixture
    def blinkstick_square(self, mock_hardware) -> BlinkStickSquare:
        """Create a BlinkStickSquare instance for testing."""
        mock_hardware.handle = Mock()
        mock_hardware.handle.write = Mock(return_value=8)
        mock_hardware.handle.read = Mock(return_value=b"\x00" * 8)
        return BlinkStickSquare(mock_hardware, reset=False, exclusive=False)

    def test_vendor_method(self) -> None:
        """Test vendor() method returns correct vendor name."""
        assert BlinkStickSquare.vendor() == "Agile Innovative"

    def test_supported_device_ids(self) -> None:
        """Test supported_device_ids contains expected devices."""
        device_ids = BlinkStickSquare.supported_device_ids
        assert (0x20A0, 0x41E5) in device_ids
        assert device_ids[(0x20A0, 0x41E5)] == "BlinkStick Square"

    def test_claims_method_valid_hardware(self, mock_hardware) -> None:
        """Test claims() method with valid hardware."""
        mock_hardware.serial_number = "BS123456-3.0"
        mock_hardware.release_number = 0x200

        # Mock super().claims() to return True
        with patch.object(BlinkStickSquare.__bases__[0], "claims", return_value=True):
            assert BlinkStickSquare.claims(mock_hardware) is True

    def test_claims_method_invalid_serial_number(self, mock_hardware) -> None:
        """Test claims() method with invalid serial number."""
        mock_hardware.serial_number = "BS123456-2.0"  # Wrong major version
        mock_hardware.release_number = 0x200

        with patch.object(BlinkStickSquare.__bases__[0], "claims", return_value=True):
            assert BlinkStickSquare.claims(mock_hardware) is False

    def test_claims_method_invalid_release_number(self, mock_hardware) -> None:
        """Test claims() method with invalid release number."""
        mock_hardware.serial_number = "BS123456-3.0"
        mock_hardware.release_number = 0x100  # Wrong release number

        with patch.object(BlinkStickSquare.__bases__[0], "claims", return_value=True):
            assert BlinkStickSquare.claims(mock_hardware) is False

    def test_claims_method_index_error(self, mock_hardware) -> None:
        """Test claims() method with IndexError in serial number processing."""
        mock_hardware.serial_number = "12"  # Too short to access [-3:][0]
        mock_hardware.release_number = 0x200

        with patch.object(BlinkStickSquare.__bases__[0], "claims", return_value=True):
            assert BlinkStickSquare.claims(mock_hardware) is False

    def test_claims_method_type_error(self, mock_hardware) -> None:
        """Test claims() method with TypeError in serial number processing."""
        mock_hardware.serial_number = None  # None will cause TypeError
        mock_hardware.release_number = 0x200

        with patch.object(BlinkStickSquare.__bases__[0], "claims", return_value=True):
            assert BlinkStickSquare.claims(mock_hardware) is False

    def test_claims_method_super_false(self, mock_hardware) -> None:
        """Test claims() method when super().claims() returns False."""
        mock_hardware.serial_number = "BS123456-3.0"
        mock_hardware.release_number = 0x200

        with patch.object(BlinkStickSquare.__bases__[0], "claims", return_value=False):
            assert BlinkStickSquare.claims(mock_hardware) is False

    def test_state_property(self, blinkstick_square) -> None:
        """Test state property returns BlinkStick Square state."""
        state = blinkstick_square.state
        assert isinstance(state, State)
        assert state.report == 6
        assert state.nleds == 8
        # Should be cached
        assert blinkstick_square.state is state

    def test_bytes_method(self, blinkstick_square) -> None:
        """Test __bytes__ method returns state bytes."""
        state_bytes = bytes(blinkstick_square)
        expected_bytes = bytes(blinkstick_square.state)
        assert state_bytes == expected_bytes

    def test_on_method_all_leds(self, blinkstick_square) -> None:
        """Test on() method with LED=0 (all LEDs)."""
        color = (255, 128, 64)
        with patch.object(blinkstick_square, "batch_update") as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            blinkstick_square.on(color, led=0)

            assert blinkstick_square.color == color
            assert blinkstick_square.state.color == color
            mock_batch.assert_called_once()

    def test_on_method_specific_led(self, blinkstick_square) -> None:
        """Test on() method with specific LED."""
        color = (200, 100, 50)
        led = 3
        # Initialize colors array so set_led can work
        blinkstick_square.state.colors = [(0, 0, 0)] * 8

        with patch.object(blinkstick_square, "batch_update") as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            blinkstick_square.on(color, led=led)

            assert blinkstick_square.color == color
            # Should set specific LED (led-1 because method uses led-1)
            # get_led now returns RGB format (converted from internal GRB)
            assert blinkstick_square.state.get_led(led - 1) == color
            mock_batch.assert_called_once()

    def test_on_method_various_leds(self, blinkstick_square) -> None:
        """Test on() method with various LED indices."""
        color = (100, 200, 50)
        test_cases = [1, 2, 3, 4, 5, 6, 7, 8]

        for led in test_cases:
            # Initialize colors array so set_led can work
            blinkstick_square.state.colors = [(0, 0, 0)] * 8

            with patch.object(blinkstick_square, "batch_update") as mock_batch:
                mock_batch.return_value.__enter__ = Mock()
                mock_batch.return_value.__exit__ = Mock()

                blinkstick_square.on(color, led=led)

                assert blinkstick_square.color == color
                # Check that the correct LED index is set (led-1)
                # get_led now returns RGB format (converted from internal GRB)
                assert blinkstick_square.state.get_led(led - 1) == color
                mock_batch.assert_called_once()

    def test_on_method_batch_update_usage(self, blinkstick_square) -> None:
        """Test on() method uses batch_update correctly."""
        color = (150, 75, 25)
        with patch.object(blinkstick_square, "batch_update") as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            blinkstick_square.on(color)

            mock_batch.assert_called_once()
            mock_batch.return_value.__enter__.assert_called_once()
            mock_batch.return_value.__exit__.assert_called_once()

    def test_bytes_integration_with_state(self, blinkstick_square) -> None:
        """Test bytes() integration with state after on() calls."""
        color = (255, 128, 64)
        blinkstick_square.on(color, led=0)

        result = bytes(blinkstick_square)
        expected = bytes(blinkstick_square.state)
        assert result == expected

        # Should contain the color data
        assert len(result) >= 2  # At least report and channel

    def test_state_persistence_across_operations(self, blinkstick_square) -> None:
        """Test that state persists across multiple operations."""
        color1 = (255, 0, 0)
        color2 = (0, 255, 0)

        # Initialize colors array so set_led can work
        blinkstick_square.state.colors = [(0, 0, 0)] * 8

        # Set first color
        blinkstick_square.on(color1, led=1)
        led1_color = blinkstick_square.state.get_led(0)

        # Set second color on different LED
        blinkstick_square.on(color2, led=2)
        led2_color = blinkstick_square.state.get_led(1)

        # LEDs should have colors in RGB format (converted from internal GRB)
        assert led1_color == color1
        assert led2_color == color2

    def test_color_property_integration(self, blinkstick_square) -> None:
        """Test color property integration with BlinkStick Square."""
        color = (128, 64, 32)
        blinkstick_square.on(color, led=0)

        # Both device and state should have the same color
        assert blinkstick_square.color == color
        assert blinkstick_square.state.color == color
