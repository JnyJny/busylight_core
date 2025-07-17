"""Tests for Agile Innovative BlinkStick implementation."""

import pytest
from unittest.mock import Mock, patch

from busylight_core.vendors.agile_innovative import BlinkStick
from busylight_core.vendors.agile_innovative._blinkstick import BlinkStickVariant
from busylight_core.hardware import Hardware, ConnectionType
from busylight_core.exceptions import HardwareUnsupportedError


class TestBlinkStickVariant:
    """Test the BlinkStickVariant class."""
    
    def test_variants_class_method(self):
        """Test variants() class method returns expected variants."""
        variants = BlinkStickVariant.variants()
        
        expected_variants = {
            "BlinkStick": BlinkStickVariant(1, "BlinkStick", 1, 1),
            "BlinkStick Pro": BlinkStickVariant(2, "BlinkStick Pro", 192, 4),
            "BlinkStick Square": BlinkStickVariant(0x200, "BlinkStick Square", 8, 6),
            "BlinkStick Strip": BlinkStickVariant(0x201, "BlinkStick Strip", 8, 6),
            "BlinkStick Nano": BlinkStickVariant(0x202, "BlinkStick Nano", 2, 6),
            "BlinkStick Flex": BlinkStickVariant(0x203, "BlinkStick Flex", 32, 6),
        }
        
        assert len(variants) == len(expected_variants)
        for name, expected in expected_variants.items():
            assert name in variants
            actual = variants[name]
            assert actual.variant == expected.variant
            assert actual.name == expected.name
            assert actual.nleds == expected.nleds
            assert actual.report == expected.report
    
    def test_from_hardware_blinkstick_v1(self):
        """Test from_hardware with BlinkStick v1."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS123456-1.0"
        hardware.release_number = 0x100
        
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.variant == 1
        assert variant.name == "BlinkStick"
        assert variant.nleds == 1
        assert variant.report == 1
    
    def test_from_hardware_blinkstick_pro_v2(self):
        """Test from_hardware with BlinkStick Pro v2."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS789012-2.0"
        hardware.release_number = 0x200
        
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.variant == 2
        assert variant.name == "BlinkStick Pro"
        assert variant.nleds == 192
        assert variant.report == 4
    
    def test_from_hardware_blinkstick_square_v3(self):
        """Test from_hardware with BlinkStick Square v3."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS345678-3.0"
        hardware.release_number = 0x200
        
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.variant == 0x200
        assert variant.name == "BlinkStick Square"
        assert variant.nleds == 8
        assert variant.report == 6
    
    def test_from_hardware_blinkstick_strip_v3(self):
        """Test from_hardware with BlinkStick Strip v3."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS456789-3.0"
        hardware.release_number = 0x201
        
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.variant == 0x201
        assert variant.name == "BlinkStick Strip"
        assert variant.nleds == 8
        assert variant.report == 6
    
    def test_from_hardware_blinkstick_nano_v3(self):
        """Test from_hardware with BlinkStick Nano v3."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS567890-3.0"
        hardware.release_number = 0x202
        
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.variant == 0x202
        assert variant.name == "BlinkStick Nano"
        assert variant.nleds == 2
        assert variant.report == 6
    
    def test_from_hardware_blinkstick_flex_v3(self):
        """Test from_hardware with BlinkStick Flex v3."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS678901-3.0"
        hardware.release_number = 0x203
        
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.variant == 0x203
        assert variant.name == "BlinkStick Flex"
        assert variant.nleds == 32
        assert variant.report == 6
    
    def test_from_hardware_unknown_v3_release(self):
        """Test from_hardware with unknown v3 release number."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS789012-3.0"
        hardware.release_number = 0x999  # Unknown release
        hardware.release = 0x999
        
        with patch('busylight_core.vendors.agile_innovative._blinkstick.logger') as mock_logger:
            with pytest.raises(HardwareUnsupportedError):
                BlinkStickVariant.from_hardware(hardware)
            mock_logger.error.assert_called_with("unknown release 2457")  # 0x999 in decimal
    
    def test_from_hardware_unknown_major_version(self):
        """Test from_hardware with unknown major version."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS890123-9.0"  # Unknown major version
        hardware.release_number = 0x200
        
        with patch('busylight_core.vendors.agile_innovative._blinkstick.logger') as mock_logger:
            with pytest.raises(HardwareUnsupportedError):
                BlinkStickVariant.from_hardware(hardware)
            mock_logger.error.assert_called_with("unknown major 9")
    
    def test_from_hardware_serial_parsing(self):
        """Test serial number parsing edge cases."""
        hardware = Mock(spec=Hardware)
        hardware.serial_number = "BS123456-1.5"  # Minor version should be ignored
        hardware.release_number = 0x100
        
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.name == "BlinkStick"
        
        # Test with different BS prefix
        hardware.serial_number = "BS999999-2.7"
        variant = BlinkStickVariant.from_hardware(hardware)
        assert variant.name == "BlinkStick Pro"


class TestBlinkStick:
    """Test the main BlinkStick class."""
    
    @pytest.fixture
    def mock_hardware_v1(self):
        """Create mock hardware for BlinkStick v1."""
        hardware = Mock(spec=Hardware)
        hardware.vendor_id = 0x20A0
        hardware.product_id = 0x41E5
        hardware.device_id = (0x20A0, 0x41E5)
        hardware.serial_number = "BS123456-1.0"
        hardware.release_number = 0x100
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware
    
    @pytest.fixture
    def mock_hardware_v2(self):
        """Create mock hardware for BlinkStick Pro v2."""
        hardware = Mock(spec=Hardware)
        hardware.vendor_id = 0x20A0
        hardware.product_id = 0x41E5
        hardware.device_id = (0x20A0, 0x41E5)
        hardware.serial_number = "BS789012-2.0"
        hardware.release_number = 0x200
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware
    
    @pytest.fixture
    def mock_hardware_v3_strip(self):
        """Create mock hardware for BlinkStick Strip v3."""
        hardware = Mock(spec=Hardware)
        hardware.vendor_id = 0x20A0
        hardware.product_id = 0x41E5
        hardware.device_id = (0x20A0, 0x41E5)
        hardware.serial_number = "BS456789-3.0"
        hardware.release_number = 0x201
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware
    
    @pytest.fixture
    def blinkstick_v1(self, mock_hardware_v1):
        """Create a BlinkStick v1 instance for testing."""
        mock_hardware_v1.handle = Mock()
        mock_hardware_v1.handle.write = Mock(return_value=4)
        mock_hardware_v1.handle.read = Mock(return_value=b'\x00' * 4)
        return BlinkStick(mock_hardware_v1, reset=False, exclusive=False)
    
    @pytest.fixture
    def blinkstick_v2(self, mock_hardware_v2):
        """Create a BlinkStick Pro v2 instance for testing."""
        mock_hardware_v2.handle = Mock()
        mock_hardware_v2.handle.write = Mock(return_value=386)  # 2 + 192*2
        mock_hardware_v2.handle.read = Mock(return_value=b'\x00' * 386)
        return BlinkStick(mock_hardware_v2, reset=False, exclusive=False)
    
    @pytest.fixture
    def blinkstick_v3_strip(self, mock_hardware_v3_strip):
        """Create a BlinkStick Strip v3 instance for testing."""
        mock_hardware_v3_strip.handle = Mock()
        mock_hardware_v3_strip.handle.write = Mock(return_value=26)  # 2 + 8*3
        mock_hardware_v3_strip.handle.read = Mock(return_value=b'\x00' * 26)
        return BlinkStick(mock_hardware_v3_strip, reset=False, exclusive=False)
    
    def test_vendor_method(self):
        """Test vendor() method returns correct vendor name."""
        assert BlinkStick.vendor() == "Agile Innovative"
    
    def test_supported_device_ids(self):
        """Test supported_device_ids contains expected devices."""
        device_ids = BlinkStick.supported_device_ids
        assert (0x20A0, 0x41E5) in device_ids
        assert device_ids[(0x20A0, 0x41E5)] == "BlinkStick"
    
    def test_channel_property_default(self, blinkstick_v1):
        """Test channel property default value."""
        assert blinkstick_v1.channel == 0
    
    def test_channel_property_setter(self, blinkstick_v1):
        """Test channel property setter."""
        blinkstick_v1.channel = 5
        assert blinkstick_v1.channel == 5
        assert blinkstick_v1._channel == 5
    
    def test_index_property_default(self, blinkstick_v1):
        """Test index property default value."""
        assert blinkstick_v1.index == 0
    
    def test_index_property_setter(self, blinkstick_v1):
        """Test index property setter."""
        blinkstick_v1.index = 3
        assert blinkstick_v1.index == 3
        assert blinkstick_v1._index == 3
    
    def test_variant_property_v1(self, blinkstick_v1):
        """Test variant property for v1 BlinkStick."""
        variant = blinkstick_v1.variant
        assert variant.variant == 1
        assert variant.name == "BlinkStick"
        assert variant.nleds == 1
        assert variant.report == 1
        # Should be cached
        assert blinkstick_v1.variant is variant
    
    def test_variant_property_v2(self, blinkstick_v2):
        """Test variant property for v2 BlinkStick Pro."""
        variant = blinkstick_v2.variant
        assert variant.variant == 2
        assert variant.name == "BlinkStick Pro"
        assert variant.nleds == 192
        assert variant.report == 4
    
    def test_variant_property_v3_strip(self, blinkstick_v3_strip):
        """Test variant property for v3 BlinkStick Strip."""
        variant = blinkstick_v3_strip.variant
        assert variant.variant == 0x201
        assert variant.name == "BlinkStick Strip"
        assert variant.nleds == 8
        assert variant.report == 6
    
    def test_name_property(self, blinkstick_v1):
        """Test name property returns variant name."""
        assert blinkstick_v1.name == "BlinkStick"
    
    def test_name_property_v2(self, blinkstick_v2):
        """Test name property for v2 returns variant name."""
        assert blinkstick_v2.name == "BlinkStick Pro"
    
    def test_bytes_method_v1(self, blinkstick_v1):
        """Test __bytes__ method for v1 BlinkStick."""
        blinkstick_v1.color = (255, 128, 64)
        result = bytes(blinkstick_v1)
        # v1 format: [report=1, green, red, blue]
        expected = bytes([1, 128, 255, 64])
        assert result == expected
    
    def test_bytes_method_v2(self, blinkstick_v2):
        """Test __bytes__ method for v2 BlinkStick Pro."""
        blinkstick_v2.color = (200, 100, 50)
        blinkstick_v2.channel = 2
        result = bytes(blinkstick_v2)
        # v2 format: [report=4, channel, green, red, blue repeated for nleds]
        expected = [4, 2]
        color_pattern = [100, 200, 50]  # green, red, blue
        expected.extend(color_pattern * 192)  # repeated for 192 LEDs
        assert result == bytes(expected)
    
    def test_bytes_method_v3_strip(self, blinkstick_v3_strip):
        """Test __bytes__ method for v3 BlinkStick Strip."""
        blinkstick_v3_strip.color = (128, 64, 32)
        blinkstick_v3_strip.channel = 1
        result = bytes(blinkstick_v3_strip)
        # v3 format: [report=6, channel, green, red, blue repeated for nleds]
        expected = [6, 1]
        color_pattern = [64, 128, 32]  # green, red, blue
        expected.extend(color_pattern * 8)  # repeated for 8 LEDs
        assert result == bytes(expected)
    
    def test_bytes_method_different_channels(self, blinkstick_v2):
        """Test __bytes__ method with different channel values."""
        blinkstick_v2.color = (255, 255, 255)
        
        # Test channel 0
        blinkstick_v2.channel = 0
        result = bytes(blinkstick_v2)
        assert result[0] == 4  # report
        assert result[1] == 0  # channel
        
        # Test channel 7
        blinkstick_v2.channel = 7
        result = bytes(blinkstick_v2)
        assert result[0] == 4  # report
        assert result[1] == 7  # channel
    
    def test_on_method_v1(self, blinkstick_v1):
        """Test on() method for v1 BlinkStick."""
        color = (255, 128, 64)
        with patch.object(blinkstick_v1, 'batch_update') as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()
            
            blinkstick_v1.on(color)
            
            assert blinkstick_v1.color == color
            mock_batch.assert_called_once()
    
    def test_on_method_v2(self, blinkstick_v2):
        """Test on() method for v2 BlinkStick Pro."""
        color = (200, 150, 100)
        with patch.object(blinkstick_v2, 'batch_update') as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()
            
            blinkstick_v2.on(color)
            
            assert blinkstick_v2.color == color
            mock_batch.assert_called_once()
    
    def test_on_method_with_led_parameter(self, blinkstick_v1):
        """Test on() method with led parameter (should be ignored)."""
        color = (128, 255, 32)
        with patch.object(blinkstick_v1, 'batch_update') as mock_batch:
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()
            
            blinkstick_v1.on(color, led=5)  # LED parameter should be ignored
            
            assert blinkstick_v1.color == color
            mock_batch.assert_called_once()
    
    def test_channel_and_index_independent(self, blinkstick_v2):
        """Test that channel and index properties are independent."""
        blinkstick_v2.channel = 3
        blinkstick_v2.index = 7
        
        assert blinkstick_v2.channel == 3
        assert blinkstick_v2.index == 7
        
        # Changing one shouldn't affect the other
        blinkstick_v2.channel = 5
        assert blinkstick_v2.channel == 5
        assert blinkstick_v2.index == 7
    
    def test_bytes_length_consistency(self, blinkstick_v1, blinkstick_v2, blinkstick_v3_strip):
        """Test that bytes output length is consistent with variant specs."""
        # v1: report(1) + green(1) + red(1) + blue(1) = 4 bytes
        assert len(bytes(blinkstick_v1)) == 4
        
        # v2: report(1) + channel(1) + (green+red+blue)*192 = 2 + 576 = 578 bytes
        assert len(bytes(blinkstick_v2)) == 2 + (3 * 192)
        
        # v3 Strip: report(1) + channel(1) + (green+red+blue)*8 = 2 + 24 = 26 bytes
        assert len(bytes(blinkstick_v3_strip)) == 2 + (3 * 8)
    
    def test_color_persistence_across_bytes_calls(self, blinkstick_v1):
        """Test that color persists across multiple bytes() calls."""
        color = (100, 200, 50)
        blinkstick_v1.color = color
        
        result1 = bytes(blinkstick_v1)
        result2 = bytes(blinkstick_v1)
        
        assert result1 == result2
        assert blinkstick_v1.color == color
    
    def test_variant_detection_error_handling(self, mock_hardware_v1):
        """Test error handling in variant detection."""
        # Test with invalid hardware that causes variant detection to fail
        mock_hardware_v1.serial_number = "INVALID-FORMAT"
        mock_hardware_v1.handle = Mock()
        mock_hardware_v1.handle.write = Mock(return_value=4)
        mock_hardware_v1.handle.read = Mock(return_value=b'\x00' * 4)
        
        blinkstick = BlinkStick(mock_hardware_v1, reset=False, exclusive=False)
        
        # This should raise an error when trying to access variant
        with pytest.raises(Exception):  # Could be ValueError, IndexError, etc.
            _ = blinkstick.variant