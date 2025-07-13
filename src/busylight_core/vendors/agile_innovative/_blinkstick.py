""" Agile Innovative BlinkStick implementation details.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from loguru import logger

from ...exceptions import LightUnsupported
from ...hardware import Hardware


@dataclass
class BlinkStickVariant:
    variant: int
    name: str
    nleds: int
    report: int

    @classmethod
    def variants(cls) -> dict[str, BlinkStickVariant]:
        return {
            "BlinkStick": BlinkStickVariant(1, "BlinkStick", 1, 1),
            "BlinkStick Pro": BlinkStickVariant(2, "BlinkStick Pro", 192, 4),
            "BlinkStick Square": BlinkStickVariant(0x200, "BlinkStick Square", 8, 6),
            "BlinkStick Strip": BlinkStickVariant(0x201, "BlinkStick Strip", 8, 6),
            "BlinkStick Nano": BlinkStickVariant(0x202, "BlinkStick Nano", 2, 6),
            "BlinkStick Flex": BlinkStickVariant(0x203, "BlinkStick Flex", 32, 6),
        }

    @classmethod
    def from_hardware(cls, hardware: Hardware) -> BlinkStickVariant:

        bs_serial, version = hardware.serial_number.split("-")
        bs_serial = bs_serial[2:]
        major, minor = version.split(".")

        variants = cls.variants()

        match major:
            case "1":
                return variants["BlinkStick"]
            case "2":
                return variants["BlinkStick Pro"]
            case "3":
                match hardware.release_number:
                    case 0x200:
                        return variants["BlinkStick Square"]
                    case 0x201:
                        return variants["BlinkStick Strip"]
                    case 0x202:
                        return variants["BlinkStick Nano"]
                    case 0x203:
                        return variants["BlinkStick Flex"]
                    case _:
                        logger.error(f"unknown release {hardware.release}")
            case _:
                logger.error(f"unknown major {major}")

        raise LightUnsupported(Hardware)
