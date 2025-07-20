"""Base class for USB connected lights.

While not intended to be instantiated directly, this class provides a
common interface for all USB connected lights and a mechanism for
discovering available lights on the system.

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
from typing import TYPE_CHECKING, ClassVar

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
from .mixins import TaskableMixin


class Light(abc.ABC, TaskableMixin):
    """Base class for USB connected lights.

    This base class provides a common interface for USB connected lights.

    Subclasses should inherit from this class, implement the abstract
    methods, and populate the `supported_device_ids` class variable
    with supported device IDs and their product names. The key for
    support_device_ids should be a tuple composed of the vendor ID and
    product ID, while the value should be the human-readable marketing
    name of the device.

    Note: If a subclass inherits from Light, but does not directly
          implement support for any specific hardware, it should leave
          the `supported_device_ids` class variable *empty*. This
          allows the base class to identify subclasses which do not
          support any specific hardware and act appropriately.

    The Light class has been designed to be helpful for discovering
    and managing USB connected lights without having to know aprori
    details of the hardware present.

    - Light.available_lights() lists devices discovered
    - Light.all_lights() returns all discovered lights ready for use
    - Light.first_light() returns the first available light

    If you know what devices you have connected and want to access
    them directly, you can use the Light subclasses directly.

    ```python
    from busylight_core.vendors.embrava import Blynclight
    from busylight_core.vendors.luxafor import Flag

    blynclight = Blynclight.first_light()
    flag = Flag.first_light()
    ```
    """

    supported_device_ids: ClassVar[dict[tuple[int, int], str]] = {}

    @classmethod
    @lru_cache(maxsize=1)
    def vendor(cls) -> str:
        """Return the vendor name in title case."""
        # EJO this is a low-effort way to get the vendor
        #     name from the module name. Subclasses can
        #     and should override this method to provide
        #     a more accurate vendor name.
        return cls.__module__.split(".")[-2].title()

    @classmethod
    @lru_cache(maxsize=1)
    def unique_device_names(cls) -> list[str]:
        """Return a list of unique device names."""
        return sorted(set(cls.supported_device_ids.values()))

    @classmethod
    @lru_cache(maxsize=1)
    def unique_device_ids(cls) -> list[tuple[int, int]]:
        """Return a list of unique device IDs."""
        return sorted(set(cls.supported_device_ids.keys()))

    @classmethod
    def claims(cls, hardware: Hardware) -> bool:
        """Return True if the hardware is claimed by this class."""
        return hardware.device_id in cls.supported_device_ids

    @classmethod
    @cache
    def subclasses(cls) -> list[type[Light]]:
        """Return a list of all subclasses of this class."""
        subclasses = []

        if cls != Light and cls.supported_device_ids:
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

        The Hardware instances are a record of light devices that were
        discovered during the enumeration process and were claimed by
        a Light subclass. The hardware device may be in use by another
        process, which will be reported when attempting to acquire the
        device during Light subclass initialization.
        """
        available_lights: dict[type[Light], list[Hardware]] = {}

        for hardware in Hardware.enumerate():
            if cls.supported_device_ids:
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
        """Return a list of all lights ready for use.

        All the lights in the list have been initialized with the
        given reset and exclusive parameters. Lights acquired with
        exclusive=True can only be used by the current process and
        will block other processes from using the same hardware until
        the light is released.

        If no lights are found, an empty list is returned.

        :param: reset - bool - reset the hardware to a known state
        :param: exclusive - bool - acquire exclusive access to the hardware
        """
        lights: list[Light] = []

        for subclass, devices in cls.available_lights().items():
            for device in devices:
                try:
                    lights.append(subclass(device, reset=reset, exclusive=exclusive))
                except Exception as error:
                    logger.info(f"Failed to acquire {device}: {error}")

        return lights

    @classmethod
    def first_light(cls, *, reset: bool = True, exclusive: bool = True) -> Light:
        """Return the first unused light ready for use.

        The light returned has been initialized with the given reset
        and exclusive parameters. If exclusive=True, the light can
        only be used by the current process and will block other
        processes from using the light until it is released.

        Raises:
        - NoLightsFoundError

        """
        for subclass, devices in cls.available_lights().items():
            for device in devices:
                try:
                    return subclass(device, reset=reset, exclusive=exclusive)
                except Exception as error:
                    logger.info(f"Failed to acquire {device}: {error}")
                    raise

        raise NoLightsFoundError(cls)

    @classmethod
    def udev_rules(cls, mode: int = 0o666) -> dict[tuple[int, int], list[str]]:
        """Return a dictionary of udev rules for the light subclass.

        The keys of the dictionary are device ID tuples, while the
        values are lists of udev rules for a particular light.  If
        duplicate device IDs are encountered, the first device ID
        wins and subsequent device IDs are ignored.

        :param mode: int - file permissions for the device, defaults to 0o666
        """
        rules = {}

        rule_formats = [
            'SUBSYSTEMS=="usb", ATTRS{{idVendor}}=="{vid:04x}", ATTRS{{idProduct}}=="{pid:04x}", MODE="{mode:04o}"',  # noqa: E501
            'KERNEL=="hidraw*", ATTRS{{idVendor}}=="{vid:04x}", ATTRS{{idProduct}}=="{pid:04x}", MODE="{mode:04o}"',  # noqa: E501
        ]

        if cls.supported_device_ids:
            for vid, pid in cls.unique_device_ids():
                content = rules.setdefault((vid, pid), [])
                content.append(f"# {cls.vendor()} {cls.__name__} udev rules")
                for rule_format in rule_formats:
                    content.append(rule_format.format(vid=vid, pid=pid, mode=mode))
        else:
            for subclass in cls.subclasses():
                subclass_rules = subclass.udev_rules(mode=mode)
                for key, value in subclass_rules.items():
                    if key not in rules:
                        rules[key] = value

        return rules

    def __init__(
        self,
        hardware: Hardware,
        *,
        reset: bool = False,
        exclusive: bool = True,
    ) -> None:
        """Initialize a Light with the given hardware information.

        The hardware argument is an instance of the Hardware class
        usually obtained from the Hardware.enumerate method. Due to
        vagaries in vendor USB implementations, the supplied hardware
        can contain incomplete information compared to other vendors
        and it's up to the Light subclass to fill in some of the
        blanks.

        The reset keyword-only parameter controls whether the hardware
        is reset to a known state using the Light.reset method.

        The exclusive keyword-only parameter controls whether the
        process creating this light has exclusive access to the
        hardware.

        :param: hardware  - Hardware
        :param: reset     - bool
        :param: exclusive - bool

        Raises:
        - HardwareUnsupportedError

        """
        if not self.__class__.claims(hardware):
            raise HardwareUnsupportedError(hardware, self.__class__)

        self.hardware = hardware
        self._reset = reset
        self._exclusive = exclusive

        if exclusive:
            self.hardware.acquire()

        if reset:
            self.reset()

    def __repr__(self) -> str:
        repr_fmt = "{n}({h!r}, *, reset={r}, exclusive={e}"
        return repr_fmt.format(
            n=self.__class__.__name__,
            h=self.hardware,
            r=self._reset,
            e=self._exclusive,
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
    def was_reset(self) -> bool:
        """Return True if the light was reset when the hardware was initialized."""
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
        """Return a hash value for the light based on its sort key."""
        try:
            return self._hash
        except AttributeError:
            self._hash = hash(self.sort_key)
            return self._hash

    @cached_property
    def name(self) -> str:
        """The human-readable marketing name of this light."""
        return self.supported_device_ids[self.hardware.device_id]

    @property
    def hex(self) -> str:
        """The hexadecimal representation of the light's state."""
        return bytes(self).hex(":")

    @property
    def read_strategy(self) -> Callable[[int, int | None], bytes]:
        """The read method used by this light."""
        return self.hardware.handle.read

    @property
    def write_strategy(self) -> Callable[[bytes], None]:
        """The write method used by this light."""
        return self.hardware.handle.write

    @contextlib.contextmanager
    def exclusive_access(self) -> Generator[None, None, None]:
        """Manage exclusive access to the light.

        If the device is not acquired in exclusive mode, it will be
        acquired and released automatically.

        No actions are taken if the light is already acquired
        in exclusive mode.
        """
        if not self._exclusive:
            self.hardware.acquire()

        yield

        if not self._exclusive:
            self.hardware.release()

    def update(self) -> None:
        """Obtain the current state of the light and write it to the device.

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
        """Update the software state of the light on exit.

        This context manager is convenience for updating multiple
        light attribute values at once and write the new state to the
        hardware on exit. This approach reduces the number of writes
        to the hardware, which is beneficial for performance.
        """
        yield
        self.update()

    @abc.abstractmethod
    def on(
        self,
        color: tuple[int, int, int],
        led: int = 0,
    ) -> None:
        """Activate the light with the given red, green, blue color tuple.

        If a subclass supports multiple LEDs, the `led` parameter
        specifies which LED to activate. If `led` is 0, all LEDs
        are activated with the specified color. If a subclasss
        does not support multiple LEDs, the `led` parameter
        is ignored and defaults to 0.

        Color tuple values should be in the range of 0-255.

        :param: color: tuple[int, int, int] - RGB color tuple
        :param: led: int - LED index, 0 for all LEDs
        """
        raise NotImplementedError

    def off(self, led: int = 0) -> None:
        """Deactivate the light.

        If a subclass supports multiple LEDs, the `led` parameter
        specifies which LED to deactivate. If `led` is 0, all LEDs
        are deactivated. If a subclass does not support multiple LEDs,
        the `led` parameter is ignored and defaults to 0.

        :param: led: int - LED index, 0 for all LEDs
        """
        self.on((0, 0, 0), led)

    def reset(self) -> None:
        """Turn the light off and cancel associated asynchronous tasks."""
        self.off()
        self.cancel_tasks()

    @abc.abstractmethod
    def __bytes__(self) -> bytes:
        """Return the light's state suitable for writing to the device."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def color(self) -> tuple[int, int, int]:
        """Get the current RGB color of the light."""
        raise NotImplementedError

    @color.setter
    @abc.abstractmethod
    def color(self, value: tuple[int, int, int]) -> None:
        """Set the RGB color of the light.

        :param: value: tuple[int, int, int] - RGB color tuple
        """
        raise NotImplementedError

    @property
    def is_lit(self) -> bool:
        """Check if the light is currently lit."""
        return any(self.color)
