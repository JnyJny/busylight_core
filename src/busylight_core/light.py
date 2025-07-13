""" """

from __future__ import annotations

import abc
import contextlib
import functools
import platform
from functools import cached_property
from typing import Callable, Generator

from loguru import logger

from .exceptions import LightUnavailable, LightUnsupported, NoLightsFound
from .hardware import Hardware
from .mixins import ColorableMixin, TaskableMixin


class Light(abc.ABC, ColorableMixin, TaskableMixin):

    @abc.abstractclassmethod
    @functools.lru_cache(maxsize=1)
    def supported_device_ids(cls) -> dict[tuple[int, int], str]:
        """A dictionary of supported device id tuples and names."""
        raise NotImplementedError

    @classmethod
    @functools.lru_cache(maxsize=1)
    def vendor(cls) -> str:
        """The vendor name in title case."""
        return cls.__module__.split(".")[-2].title()

    @classmethod
    @functools.lru_cache(maxsize=1)
    def unique_device_names(cls) -> list[str]:
        """Returns a list of unique device names."""
        return sorted(set(cls.supported_device_ids().values()))

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Returns True if the hardware is claimed by this class."""
        return hardware.device_id in cls.supported_device_ids()

    @classmethod
    @functools.lru_cache(maxsize=None)
    def subclasses(cls) -> list[type[Light]]:
        """Returns a list of all light subclasses of this class."""
        subclasses = []

        if cls != Light:
            subclasses.append(cls)

        for subclass in cls.__subclasses__():
            subclasses.extend(subclass.subclasses())

        return sorted(subclasses, key=lambda s: s.__module__)

    @classmethod
    @functools.lru_cache(maxsize=1)
    def supported_lights(cls) -> dict[str, list[str]]:
        """A dictionary of supported lights by vendor."""
        supported_lights: dict[str, list[str]] = {}

        for subclass in cls.subclasses():
            names = supported_lights.setdefault(subclass.vendor(), [])
            names.extend(subclass.unique_device_names())

        return supported_lights

    @classmethod
    def available_lights(cls) -> dict[type[Light], list[Hardware]]:
        """Returns a dictionary of available hardware by type."""

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
    def all_lights(cls, reset: bool = True, exclusive: bool = True) -> list[Light]:
        """Returns a list of all lights ready for use."""

        lights: list[Light] = []

        for subclass, devices in cls.available_lights().items():
            for device in devices:
                lights.append(subclass(device, reset, exclusive))

        return lights

    @classmethod
    def first_light(cls, reset: bool = True, exclusive: bool = True) -> Light:
        """Returns the first unused light ready for use.

        Raises:
        - NoLightsFound: if no lights are available.
        """

        for subclass, devices in cls.available_lights().items():
            for device in devices:
                try:
                    return subclass(device, reset, exclusive)
                except Exception as error:
                    logger.info(f"Failed to acquire {device}: {error}")
                    raise

        raise NoLightsFound()

    def __init__(
        self,
        hardware: Hardware,
        reset: bool = False,
        exclusive: bool = True,
    ):

        if not self.__class__.claims(hardware):
            raise LightUnsupported(hardware)

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
        system = platform.system()
        match system:
            case "Windows":
                return f"{system}_{platform.release()}"
            case _:
                return system

    @cached_property
    def _sort_key(self) -> tuple[str, str, str]:
        return (self.vendor().lower(), self.name.lower(), self.path)

    def __eq__(self, other: object) -> bool:
        try:
            return self._sort_key == other._sort_key
        except AttributeError:
            raise NotImplemented from None

    def __lt__(self, other: Light) -> bool:

        if not isinstance(other, Light):
            return NotImplemented

        for self_value, other_value in zip(self._sort_key, other._sort_key):
            if self_value != other_value:
                return self_value < other_value

        return False

    def __hash__(self) -> int:
        try:
            return self._hash
        except AttributeError:
            pass
        self._hash = hash(self._sort_key)
        return self._hash

    @cached_property
    def name(self) -> str:
        """The marketing name of this light."""
        return self.supported_device_ids()[self.hardware.device_id]

    @property
    def hex(self) -> str:
        """The hexadecimal representation of the light's state."""
        return bytes(self).hex(":")

    @property
    def read_strategy(self) -> Callable[[int, int | None], bytes]:
        """Returns the read method used by this light."""
        return self.hardware.handle.read

    @property
    def write_strategy(self) -> Callable[[bytes], None]:
        """Returns the write method used by this light."""
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
        """Obtains the current state of the light and writes it to the device."""

        data = bytes(self)

        match self.platform:
            case "Windows_10":
                data = bytes([0]) + data
            case "Darwin" | "Linux" | "Windows_11":
                pass
            case _:
                logger.info(f"Unsupported OS {self.platform}, hoping for the best.")

        with self.exclusive_access():

            logger.debug(f"{self.name} payload {data.hex(':')}")

            try:
                self.write_strategy(data)
            except Exception as error:
                logger.error(f"{self}: {error}")
                raise LightUnavailable(self) from None

    @contextlib.contextmanager
    def batch_update(self) -> Generator[None, None, None]:
        """A context manager for updating the software state of the
        light and updating the hardware automatically on exit.
        """

        yield
        self.update()

    def on(self, color: tuple[int, int, int]) -> None:
        """Activate the light with the given red, green, blue color tuple."""
        with self.batch_update():
            self.color = color

    def off(self) -> None:
        """Deactivate the light."""
        self.on((0, 0, 0))

    def reset(self) -> None:
        """Quiesce the light and associated asynchronous tasks."""
        self.off()
        self.cancel_tasks()

    @abc.abstractmethod
    def __bytes__(self) -> bytes:
        """The byte representation of the light's state."""
