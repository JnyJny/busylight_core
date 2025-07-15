""" """

import pytest
from busylight_core import Light, NoLightsFound
from busylight_core.hardware import Hardware


def test_light_init_fails(hardware_devices: list[Hardware]) -> None:
    for device in hardware_devices:
        with pytest.raises(TypeError):
            result = Light(device)


def test_light_abstractclassmethod_supported_device_ids() -> None:
    assert Light.supported_device_ids == {}


def test_light_classmethod_vendor() -> None:
    result = Light.vendor()
    assert isinstance(result, str)


def test_light_classmethod_unique_device_names() -> None:
    results = Light.unique_device_names()

    for result in results:
        assert isinstance(result, str)


def test_light_classmethod_claims_bogus_device(
    hardware_devices: list[Hardware],
) -> None:
    for device in hardware_devices:
        result = Light.claims(device)
        assert not result


def test_light_classmethod_subclasses() -> None:
    results = Light.subclasses()

    assert isinstance(results, list)

    for item in results:
        assert issubclass(item, Light)


def test_light_classmethod_supported_lights() -> None:
    results = Light.supported_lights()

    assert isinstance(results, dict)

    for vendor, product_names in results.items():
        assert isinstance(vendor, str)
        assert isinstance(product_names, list)

        for product_name in product_names:
            assert isinstance(product_name, str)


def test_light_classmethod_available_lights() -> None:
    results = Light.available_lights()

    assert isinstance(results, dict)

    for subclass, devices in results.items():
        assert issubclass(subclass, Light)
        assert isinstance(devices, list)

        for device in devices:
            assert isinstance(device, Hardware)


def test_light_classmethod_all_lights() -> None:
    results = Light.all_lights(reset=False, exclusive=False)

    assert isinstance(results, list)

    for item in results:
        assert isinstance(item, Light)


def test_light_classmethod_first_light() -> None:
    try:
        result = Light.first_light(reset=False, exclusive=False)
        assert isinstance(result, Light)
    except NoLightsFound:
        pass
