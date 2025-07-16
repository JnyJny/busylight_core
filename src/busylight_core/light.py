"""Base class for USB connected lights.

While not intended to be instantiated directly, this class provides a common
interface for all USB connected lights and a mechanism for discovering
available lights on the system.

```python
from busylight_core import Light

all_lights = Light.all_lights()

for light in all_lights:
    light.on((255, 0, 0))  # Turn on the light with red color

for light in all_lights:
    light.off()  # Turn off all lights
````

"""

from __future__ import annotations

import abc
import contextlib
import platform
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

from functools import cache, cached_property, lru_cache

from loguru import logger

from .exceptions import (
    HardwareUnsupportedError,
    LightUnavailableError,
    NoLightsFoundError,
)
from .hardware import Hardware
from .mixins import ColorableMixin, TaskableMixin


class Light(abc.ABC, ColorableMixin, TaskableMixin):
    """Base class for USB connected lights.

    This base class provides a common interface for all USB connected lights.
    """

    supported_device_ids: dict[tuple[int, int], str] | None = None

    @classmethod
    @lru_cache(maxsize=1)
    def vendor(cls) -> str:
        """Return the vendor name in title case."""
        return cls.__module__.split(".")[-2].title()

    @classmethod
    @lru_cache(maxsize=1)
    def unique_device_names(cls) -> list[str]:
        """Return a list of unique device names."""
        try:
            return sorted(set(cls.supported_device_ids.values()))
        except AttributeError:
            return []

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Return True if the hardware is claimed by this class."""
        try:
            return hardware.device_id in cls.supported_device_ids
        except TypeError:
            return False

    @classmethod
    @cache
    def subclasses(cls) -> list[type[Light]]:
        """Return a list of all subclasses of this class."""
        subclasses = []

        if cls != Light:
            subclasses.append(cls)

        for subclass in cls.__subclasses__():
            subclasses.extend(subclass.subclasses())

        return sorted(subclasses, key=lambda s: s.__module__)

    @classmethod
    @lru_cache(maxsize=1)
    def supported_lights(cls) -> dict[str, list[str]]:
        """Return a dictionary of supported lights by vendor.

        Keys are vendor names, values are a list of product names.
        """
        supported_lights: dict[str, list[str]] = {}

        for subclass in cls.subclasses():
            names = supported_lights.setdefault(subclass.vendor(), [])
            names.extend(subclass.unique_device_names())

        return supported_lights

    @classmethod
    def available_lights(cls) -> dict[type[Light], list[Hardware]]:
        """Return a dictionary of available hardware by type.

        Keys are Light subclasses, values are a list of Hardware instances.
        """
        available_lights: dict[type[Light], list[Hardware]] = {}

        for hardware in Hardware.enumerate():
            if cls != Light:
                if cls.claims(hardware):
                    logger.debug(f"{cls.__name__} claims {hardware}")
                    claimed = available_lights.setdefault(cls, [])
                    claimed.append(hardware)
            else:
                for subclass in cls.subclasses():
                    if subclass.claims(hardware):
                        logger.debug(f"{subclass.__name__} claims {hardware}")
                        claimed = available_lights.setdefault(subclass, [])
                        claimed.append(hardware)

        return available_lights

    @classmethod
    def all_lights(cls, *, reset: bool = True, exclusive: bool = True) -> list[Light]:
        """Return a list of all lights ready for use."""
        lights: list[Light] = []

        for subclass, devices in cls.available_lights().items():
            lights.extend(
                [
                    subclass(device, reset=reset, exclusive=exclusive)
                    for device in devices
                ]
            )

        return lights

    @classmethod
    def first_light(cls, *, reset: bool = True, exclusive: bool = True) -> Light:
        """Return the first unused light ready for use.

        Raises:
        - NoLightsFoundError: if no lights are available.

        """
        for subclass, devices in cls.available_lights().items():
            for device in devices:
                try:
                    return subclass(device, reset=reset, exclusive=exclusive)
                except Exception as error:
                    logger.info(f"Failed to acquire {device}: {error}")
                    raise

        raise NoLightsFoundError

    def __init__(
        self,
        hardware: Hardware,
        *,
        reset: bool = False,
        exclusive: bool = True,
    ) -> None:
        """Initialize a Light with the given hardware information.

        :param: reset - bool - reset the hardware to a known state
        :param: exclusive - bool - acquire exclusive access to the hardware

        Raises:
        - HardwareUnsupportedError: if the given Hardware is not supported by this
          class.

        """
        if not self.__class__.claims(hardware):
            raise HardwareUnsupportedError(hardware)

        self.hardware = hardware
        self._reset = reset
        self._exclusive = exclusive

        if exclusive:
            self.hardware.acquire()

        if reset:
            self.reset()

    def __repr__(self) -> str:
        return "".join(
            [
                f"{self.__class__.__name__}(",
                f"{self.hardware!r}, reset={self._reset},",
                f"exclusive={self._exclusive})",
            ]
        )

    @cached_property
    def path(self) -> str:
        """The path to the hardware device."""
        return self.hardware.path.decode("utf-8")

    @cached_property
    def platform(self) -> str:
        """The discovered operating system platform name."""
        system = platform.system()
        match system:
            case "Windows":
                return f"{system}_{platform.release()}"
            case _:
                return system

    @property
    def exclusive(self) -> bool:
        """Return True if the light has exclusive access to the hardware."""
        return self._exclusive

    @property
    def reset(self) -> bool:
        """Return True if the light resets the hardware to a known state."""
        return self._reset

    @cached_property
    def sort_key(self) -> tuple[str, str, str]:
        """Return a tuple used for sorting lights.

        The tuple consists of:
        - vendor name in lowercase
        - device name in lowercase
        - hardware path
        """
        return (self.vendor().lower(), self.name.lower(), self.path)

    def __eq__(self, other: object) -> bool:
        try:
            return self.sort_key == other.sort_key
        except AttributeError:
            raise TypeError from None

    def __lt__(self, other: Light) -> bool:
        if not isinstance(other, Light):
            return NotImplemented

        for self_value, other_value in zip(self.sort_key, other.sort_key, strict=False):
            if self_value != other_value:
                return self_value < other_value

        return False

    def __hash__(self) -> int:
        try:
            return self._hash
        except AttributeError:
            self._hash = hash(self.sort_key)
            return self._hash

    @cached_property
    def name(self) -> str:
        """Return the marketing name of this light."""
        return self.supported_device_ids[self.hardware.device_id]

    @property
    def hex(self) -> str:
        """Return the hexadecimal representation of the light's state."""
        return bytes(self).hex(":")

    @property
    def read_strategy(self) -> Callable[[int, int | None], bytes]:
        """Return the read method used by this light."""
        return self.hardware.handle.read

    @property
    def write_strategy(self) -> Callable[[bytes], None]:
        """Return the write method used by this light."""
        return self.hardware.handle.write

    @contextlib.contextmanager
    def exclusive_access(self) -> Generator[None, None, None]:
        """Manage exclusive access to the light.

        If the device is not acquired in exclusive mode, it will be
        acquired and released automatically.
        """
        if not self._exclusive:
            self.hardware.acquire()

        yield

        if not self._exclusive:
            self.hardware.release()

    def update(self) -> None:
        """Obtain the current state of the light and writes it to the device.

        Raises:
        - LightUnavailableError

        """
        state = bytes(self)

        match self.platform:
            case "Windows_10":
                state = bytes([0]) + state
            case "Darwin" | "Linux" | "Windows_11":
                pass
            case _:
                logger.info(f"Unsupported OS {self.platform}, hoping for the best.")

        with self.exclusive_access():
            logger.debug(f"{self.name} payload {state.hex(':')}")

            try:
                self.write_strategy(state)
            except Exception as error:
                logger.error(f"{self}: {error}")
                raise LightUnavailableError(self) from None

    @contextlib.contextmanager
    def batch_update(self) -> Generator[None, None, None]:
        """Update the software state of the light on exit."""
        yield
        self.update()

    @abc.abstractmethod
    def on(
        self,
        color: tuple[int, int, int],
        led: int = 0,
    ) -> None:
        """Activate the light with the given red, green, blue color tuple."""
        raise NotImplementedError

    def off(self, led: int = 0) -> None:
        """Deactivate the light."""
        self.on((0, 0, 0), led)

    def reset(self) -> None:
        """Turn the light off and cancel associated asynchronous tasks."""
        self.off()
        self.cancel_tasks()

    @abc.abstractmethod
    def __bytes__(self) -> bytes:
        """Return the byte representation of the light's state."""
