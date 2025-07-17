"""Tests for Kuando Busylight Alpha implementation."""

import asyncio
from unittest.mock import Mock, patch

import pytest

from busylight_core.hardware import ConnectionType, Hardware
from busylight_core.vendors.kuando import Busylight_Alpha
from busylight_core.vendors.kuando._busylight import OpCode, Ring, State, Step
from busylight_core.vendors.kuando.busylight_alpha import _keepalive


class TestKuandoBusylightStep:
    """Test the Step class for Kuando Busylight."""

    def test_step_initialization(self):
        """Test that Step initializes with correct default values."""
        step = Step()
        assert step.opcode == 0
        assert step.operand == 0
        assert step.body == 0
        assert step.color == (0, 0, 0)
        assert step.repeat == 0
        assert step.duty_cycle_on == 0
        assert step.duty_cycle_off == 0
        assert step.update == 0
        assert step.ringtone == 0
        assert step.volume == 0

    def test_step_keep_alive(self):
        """Test keep_alive method configuration."""
        step = Step()
        timeout = 10
        step.keep_alive(timeout)
        assert step.opcode == OpCode.KeepAlive
        assert step.operand == timeout
        assert step.body == 0

    def test_step_keep_alive_timeout_mask(self):
        """Test keep_alive method with timeout masking."""
        step = Step()
        timeout = 0x1F  # 31, should be masked to 0xF (15)
        step.keep_alive(timeout)
        assert step.opcode == OpCode.KeepAlive
        assert step.operand == 0xF  # Masked to 4 bits
        assert step.body == 0

    def test_step_boot(self):
        """Test boot method configuration."""
        step = Step()
        step.boot()
        assert step.opcode == OpCode.Boot
        assert step.operand == 0
        assert step.body == 0

    def test_step_reset(self):
        """Test reset method configuration."""
        step = Step()
        step.reset()
        assert step.opcode == OpCode.Reset
        assert step.operand == 0
        assert step.body == 0

    def test_step_jump_basic(self):
        """Test jump method with basic color."""
        step = Step()
        color = (255, 128, 64)
        step.jump(color)
        assert step.opcode == OpCode.Jump
        assert step.operand == 0  # default target
        # Color conversion has rounding - check approximately
        retrieved_color = step.color
        assert all(abs(retrieved_color[i] - color[i]) <= 2 for i in range(3))
        assert step.repeat == 0
        assert step.duty_cycle_on == 0
        assert step.duty_cycle_off == 0
        assert step.update == 0
        assert step.ringtone == Ring.Off
        assert step.volume == 0

    def test_step_jump_full_parameters(self):
        """Test jump method with all parameters."""
        step = Step()
        color = (200, 150, 100)
        target = 3
        repeat = 5
        on_time = 10
        off_time = 20
        update = 1
        ringtone = Ring.Buzz
        volume = 7

        step.jump(color, target, repeat, on_time, off_time, update, ringtone, volume)

        assert step.opcode == OpCode.Jump
        assert step.operand == target
        # Color conversion has rounding - check approximately
        retrieved_color = step.color
        assert all(
            abs(retrieved_color[i] - color[i]) <= 5 for i in range(3)
        )  # Allow larger tolerance
        assert step.repeat == repeat
        assert step.duty_cycle_on == on_time
        assert step.duty_cycle_off == off_time
        assert step.update == update
        assert step.ringtone == ringtone & 0xF  # Ringtone is masked to 4 bits
        assert step.volume == volume & 0x3  # Volume is masked to 3 bits

    def test_step_jump_parameter_masking(self):
        """Test jump method with parameter masking."""
        step = Step()
        color = (255, 255, 255)
        target = 0x1F  # Should be masked to 0xF
        repeat = 0x1FF  # Should be masked to 0xFF
        on_time = 0x1FF  # Should be masked to 0xFF
        off_time = 0x1FF  # Should be masked to 0xFF
        update = 0x3  # Should be masked to 0x1
        ringtone = 0x1F  # Should be masked to 0xF
        volume = 0x7  # Should be masked to 0x3

        step.jump(color, target, repeat, on_time, off_time, update, ringtone, volume)

        assert step.operand == 0xF
        assert step.repeat == 0xFF
        assert step.duty_cycle_on == 0xFF
        assert step.duty_cycle_off == 0xFF
        assert step.update == 0x1
        assert step.ringtone == 0xF
        assert step.volume == 0x3

    def test_step_color_property(self):
        """Test color property getter and setter."""
        step = Step()
        color = (128, 64, 32)
        step.color = color
        # Color conversion has rounding - check approximately
        retrieved_color = step.color
        assert all(abs(retrieved_color[i] - color[i]) <= 2 for i in range(3))

    def test_step_color_conversion(self):
        """Test color conversion from 0-255 to 0-100 range."""
        step = Step()
        # Test full range colors
        step.color = (255, 255, 255)
        # Colors should be converted and stored in 0-100 range internally
        # but retrieved as 0-255 range
        assert step.color == (255, 255, 255)

        step.color = (0, 0, 0)
        assert step.color == (0, 0, 0)

        # Test mid-range color
        step.color = (128, 128, 128)
        retrieved_color = step.color
        # Should be approximately 128 after conversion round-trip
        assert all(
            abs(c - 128) <= 2 for c in retrieved_color
        )  # Allow small rounding error


class TestKuandoBusylightState:
    """Test the State class for Kuando Busylight."""

    def test_state_initialization(self):
        """Test that State initializes with steps."""
        state = State()
        assert hasattr(state, "steps")
        assert len(state.steps) == 7  # State should have 7 steps
        for step in state.steps:
            assert isinstance(step, Step)
        assert hasattr(state, "footer")
        assert hasattr(state, "struct")


class TestKuandoBusylightAlpha:
    """Test the main Busylight_Alpha class."""

    @pytest.fixture
    def mock_hardware(self):
        """Create mock hardware for testing."""
        hardware = Mock(spec=Hardware)
        hardware.vendor_id = 0x04D8
        hardware.product_id = 0xF848
        hardware.device_id = (0x04D8, 0xF848)
        hardware.connection_type = ConnectionType.HID
        hardware.acquire = Mock()
        hardware.release = Mock()
        return hardware

    @pytest.fixture
    def busylight(self, mock_hardware):
        """Create a Busylight_Alpha instance for testing."""
        # Mock the hardware handle methods
        mock_hardware.handle = Mock()
        mock_hardware.handle.write = Mock(return_value=64)
        mock_hardware.handle.read = Mock(return_value=b"\x00" * 64)

        return Busylight_Alpha(mock_hardware, reset=False, exclusive=False)

    def test_supported_device_ids(self):
        """Test supported_device_ids contains expected devices."""
        device_ids = Busylight_Alpha.supported_device_ids
        assert (0x04D8, 0xF848) in device_ids
        assert (0x27BB, 0x3BCA) in device_ids
        assert (0x27BB, 0x3BCB) in device_ids
        assert (0x27BB, 0x3BCE) in device_ids
        assert all("Busylight Alpha" in name for name in device_ids.values())

    def test_state_property(self, busylight):
        """Test state property returns State instance."""
        assert isinstance(busylight.state, State)
        # Should be cached
        assert busylight.state is busylight.state

    def test_bytes_method(self, busylight):
        """Test __bytes__ method returns state bytes."""
        state_bytes = bytes(busylight)
        expected_bytes = bytes(busylight.state)
        assert state_bytes == expected_bytes
        assert (
            len(state_bytes) == 64
        )  # State should be 7 steps + 1 footer * 8 bytes each

    def test_on_method(self, busylight):
        """Test on() method with color."""
        color = (255, 128, 64)
        with (
            patch.object(busylight, "batch_update") as mock_batch,
            patch.object(busylight, "add_task") as mock_add_task,
        ):
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            busylight.on(color)

            assert busylight.color == color
            # Color conversion has rounding - check approximately
            retrieved_color = busylight.state.steps[0].color
            assert all(abs(retrieved_color[i] - color[i]) <= 2 for i in range(3))
            assert busylight.state.steps[0].opcode == OpCode.Jump
            mock_batch.assert_called_once()
            mock_add_task.assert_called_once_with("keepalive", _keepalive)

    def test_off_method(self, busylight):
        """Test off() method."""
        # First turn on
        busylight.on((255, 0, 0))

        with (
            patch.object(busylight, "batch_update") as mock_batch,
            patch.object(busylight, "cancel_task") as mock_cancel_task,
        ):
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            busylight.off()

            assert busylight.color == (0, 0, 0)
            assert busylight.state.steps[0].color == (0, 0, 0)
            assert busylight.state.steps[0].opcode == OpCode.Jump
            mock_batch.assert_called_once()
            mock_cancel_task.assert_called_once_with("keepalive")

    def test_on_method_with_led_parameter(self, busylight):
        """Test on() method with led parameter (should be ignored)."""
        color = (128, 255, 32)
        with (
            patch.object(busylight, "batch_update") as mock_batch,
            patch.object(busylight, "add_task") as mock_add_task,
        ):
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            busylight.on(color, led=5)  # LED parameter should be ignored

            assert busylight.color == color
            # Color conversion has rounding - check approximately
            retrieved_color = busylight.state.steps[0].color
            assert all(abs(retrieved_color[i] - color[i]) <= 2 for i in range(3))
            mock_batch.assert_called_once()
            mock_add_task.assert_called_once_with("keepalive", _keepalive)

    def test_off_method_with_led_parameter(self, busylight):
        """Test off() method with led parameter (should be ignored)."""
        with (
            patch.object(busylight, "batch_update") as mock_batch,
            patch.object(busylight, "cancel_task") as mock_cancel_task,
        ):
            mock_batch.return_value.__enter__ = Mock()
            mock_batch.return_value.__exit__ = Mock()

            busylight.off(led=3)  # LED parameter should be ignored

            assert busylight.color == (0, 0, 0)
            mock_batch.assert_called_once()
            mock_cancel_task.assert_called_once_with("keepalive")


class TestKuandoBusylightKeepAlive:
    """Test the keepalive functionality."""

    @pytest.fixture
    def mock_light(self):
        """Create mock light for testing."""
        light = Mock(spec=Busylight_Alpha)
        light.state = Mock()
        light.state.steps = [Mock(spec=Step) for _ in range(16)]
        light.batch_update = Mock()
        light.batch_update.return_value.__enter__ = Mock()
        light.batch_update.return_value.__exit__ = Mock()
        return light

    @pytest.mark.asyncio
    async def test_keepalive_default_interval(self, mock_light):
        """Test keepalive with default interval."""
        with patch("asyncio.sleep") as mock_sleep:
            mock_sleep.side_effect = [
                None,
                asyncio.CancelledError(),
            ]  # Stop after one iteration

            with pytest.raises(asyncio.CancelledError):
                await _keepalive(mock_light)

            # Should call keep_alive with default interval of 15
            mock_light.state.steps[0].keep_alive.assert_called_with(15)
            mock_sleep.assert_called_with(
                8
            )  # Should sleep for interval/2 rounded: round(15/2) = 8

    @pytest.mark.asyncio
    async def test_keepalive_custom_interval(self, mock_light):
        """Test keepalive with custom interval."""
        interval = 10
        with patch("asyncio.sleep") as mock_sleep:
            mock_sleep.side_effect = [
                None,
                asyncio.CancelledError(),
            ]  # Stop after one iteration

            with pytest.raises(asyncio.CancelledError):
                await _keepalive(mock_light, interval)

            mock_light.state.steps[0].keep_alive.assert_called_with(interval)
            mock_sleep.assert_called_with(5)  # Should sleep for interval/2

    @pytest.mark.asyncio
    async def test_keepalive_interval_validation(self, mock_light):
        """Test keepalive interval validation."""
        # Test invalid intervals
        with pytest.raises(
            ValueError, match="Keepalive interval must be between 0 and 15 seconds"
        ):
            await _keepalive(mock_light, -1)

        with pytest.raises(
            ValueError, match="Keepalive interval must be between 0 and 15 seconds"
        ):
            await _keepalive(mock_light, 16)

        # Test valid boundary values
        with patch("asyncio.sleep") as mock_sleep:
            # Test interval 0
            mock_sleep.side_effect = [asyncio.CancelledError()]  # Stop immediately

            with pytest.raises(asyncio.CancelledError):
                await _keepalive(mock_light, 0)
            mock_light.state.steps[0].keep_alive.assert_called_with(0)

            # Reset mock for next test
            mock_light.state.steps[0].keep_alive.reset_mock()

            # Test interval 15
            mock_sleep.side_effect = [asyncio.CancelledError()]  # Stop immediately

            with pytest.raises(asyncio.CancelledError):
                await _keepalive(mock_light, 15)
            mock_light.state.steps[0].keep_alive.assert_called_with(15)

    @pytest.mark.asyncio
    async def test_keepalive_sleep_calculation(self, mock_light):
        """Test keepalive sleep interval calculation."""
        test_cases = [
            (1, 0),  # round(1/2) = 0
            (2, 1),  # round(2/2) = 1
            (3, 2),  # round(3/2) = 2
            (9, 4),  # round(9/2) = 4
            (10, 5),  # round(10/2) = 5
            (15, 8),  # round(15/2) = 8
        ]

        for interval, expected_sleep in test_cases:
            with patch("asyncio.sleep") as mock_sleep:
                mock_sleep.side_effect = [asyncio.CancelledError()]  # Stop immediately

                with pytest.raises(asyncio.CancelledError):
                    await _keepalive(mock_light, interval)

                mock_sleep.assert_called_with(expected_sleep)

    @pytest.mark.asyncio
    async def test_keepalive_continuous_operation(self, mock_light):
        """Test keepalive continuous operation."""
        with patch("asyncio.sleep") as mock_sleep:
            # Allow 3 iterations then cancel
            mock_sleep.side_effect = [None, None, None, asyncio.CancelledError()]

            with pytest.raises(asyncio.CancelledError):
                await _keepalive(mock_light, 8)

            # Should have called keep_alive 4 times (once per iteration)
            assert mock_light.state.steps[0].keep_alive.call_count == 4
            # Should have called sleep 4 times (once per iteration)
            assert mock_sleep.call_count == 4
            # Each sleep should be with interval/2
            for call in mock_sleep.call_args_list:
                assert call[0][0] == 4  # round(8/2) = 4

    @pytest.mark.asyncio
    async def test_keepalive_batch_update_usage(self, mock_light):
        """Test keepalive uses batch_update correctly."""
        with patch("asyncio.sleep") as mock_sleep:
            mock_sleep.side_effect = [
                None,
                asyncio.CancelledError(),
            ]  # Stop after one iteration

            with pytest.raises(asyncio.CancelledError):
                await _keepalive(mock_light)

            # Should use batch_update for each keepalive call
            mock_light.batch_update.assert_called()
            mock_light.batch_update.return_value.__enter__.assert_called()
            mock_light.batch_update.return_value.__exit__.assert_called()
