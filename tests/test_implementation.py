""" """

from collections.abc import Callable

import pytest

from busylight_core import LightUnsupported, NoLightsFound
from busylight_core.hardware import Hardware

from .vendor_examples import HardwareCatalog as VENDOR_HARDWARE

VENDOR_SUBCLASSES = VENDOR_HARDWARE.keys()


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_supported_device_ids(subclass) -> None:
    result = subclass.supported_device_ids
    assert isinstance(result, dict)

    for key, value in result.items():
        assert isinstance(key, tuple)
        for item in key:
            assert isinstance(item, int)
        assert isinstance(value, str)


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_vendor(subclass) -> None:
    result = subclass.vendor()
    assert isinstance(result, str)


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_unique_device_names(subclass) -> None:
    result = subclass.unique_device_names()
    assert isinstance(result, list)

    for item in result:
        assert isinstance(item, str)


@pytest.mark.parametrize("subclass,devices", list(VENDOR_HARDWARE.items()))
def test_implementation_classmethod_claims(subclass, devices) -> None:
    for device in devices:
        result = subclass.claims(device)
        assert isinstance(result, bool)
        assert result is True


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_does_not_claim_bogus(
    subclass,
    hardware_devices,
) -> None:
    for device in hardware_devices:
        result = subclass.claims(device)
        assert isinstance(result, bool)
        assert result is False


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_subclasses(subclass) -> None:
    results = subclass.subclasses()
    assert isinstance(results, list)
    for item in results:
        assert issubclass(item, subclass)


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_supported_lights(subclass) -> None:
    results = subclass.supported_lights()
    assert isinstance(results, dict)
    for key, value in results.items():
        assert isinstance(key, str)
        for item in value:
            assert isinstance(item, str)


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_available_lights(subclass) -> None:
    results = subclass.available_lights()
    assert isinstance(results, dict)
    for subclasses, devices in results.items():
        assert issubclass(subclasses, subclass)
        assert isinstance(devices, list)
        for device in devices:
            assert isinstance(device, Hardware)


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_all_lights(subclass) -> None:
    results = subclass.all_lights()
    assert isinstance(results, list)
    for item in results:
        assert isinstance(item, subclass)


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_classmethod_first_light(subclass) -> None:
    try:
        result = subclass.first_light()
        assert isinstance(result, subclass)
    except NoLightsFound:
        pass


@pytest.mark.parametrize("subclass", VENDOR_SUBCLASSES)
def test_implementation_init_with_bogus_hardware(subclass, hardware_devices) -> None:
    for device in hardware_devices:
        with pytest.raises(LightUnsupported):
            result = subclass(device, reset=False, exclusive=False)


@pytest.mark.parametrize("subclass,devices", list(VENDOR_HARDWARE.items()))
def test_implementation_init(subclass, devices) -> None:
    for device in devices:
        ## EJO The aquire and release methods are monkey patched here to
        ##     to avoid really trying to acquire/release potentially bogus
        ##     hardware devices.  Additionally, the write and read strategy
        ##     methods are monkey patched to avoid any real I/O operations.

        device.acquire = lambda: None
        device.release = lambda: None

        class TestSubclass(subclass):
            @property
            def write_strategy(self) -> Callable[[bytes], int]:
                return lambda buf: None

            @property
            def read_strategy(self) -> Callable[[int, int | None], bytes]:
                return lambda nbytes: b""

        result = TestSubclass(device, reset=False, exclusive=False)

        assert isinstance(result, subclass)

        assert isinstance(result.hardware, Hardware)
        assert result.hardware == device
        assert result._reset is False
        assert result._exclusive is False

        assert isinstance(result._sort_key, tuple)
        for item in result._sort_key:
            assert isinstance(item, str)

        assert isinstance(result.name, str)
        assert isinstance(result.hex, str)
        assert isinstance(result.read_strategy, Callable)
        assert isinstance(result.write_strategy, Callable)

        assert isinstance(bytes(result), bytes)

        assert isinstance(result.red, int)
        assert result.red == 0
        assert isinstance(result.green, int)
        assert result.green == 0
        assert isinstance(result.blue, int)
        assert result.blue == 0

        assert isinstance(result.color, tuple)
        assert all(c == 0 for c in result.color)

        color = (255, 255, 255)

        result.on(color)

        assert all(c == 0xFF for c in result.color)
        assert result.red == 0xFF
        assert result.green == 0xFF
        assert result.blue == 0xFF

        result.off()

        assert all(c == 0x00 for c in result.color)
        assert result.red == 0x00
        assert result.green == 0x00
        assert result.blue == 0x00
