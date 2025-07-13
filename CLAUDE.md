# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is `busylight_core`, a Python library for controlling USB-connected status lights (busylights) from various vendors. The project provides a unified interface for controlling different hardware devices through a plugin-style architecture where each vendor implements the abstract `Light` class.

## Development Commands

The project uses [Poe the Poet](https://poethepoet.natn.io) for task automation. Run `poe` without arguments to see all available tasks.

### Essential Commands
- `poe test` - Run test suite with pytest
- `poe ruff` - Run code formatting and linting (check + format)
- `poe mypy` - Run mypy type checking
- `poe ty` - Run ty type checking  
- `poe qc` - Run all quality checks (test + ruff + mypy + ty)
- `poe coverage` - Generate and open HTML coverage report

### Development Setup
- `uv sync` - Install dependencies and create virtual environment
- `direnv allow` - Enable automatic venv activation (optional but recommended)

### Documentation
- `poe docs-serve` - Serve MkDocs documentation locally
- `poe docs-build` - Build documentation
- `poe docs-deploy` - Deploy to GitHub Pages

## Architecture

### Core Components

1. **Abstract Base Classes**
   - `Light` (src/busylight_core/light.py) - Main abstract class that all device implementations inherit from
   - `Hardware` (src/busylight_core/hardware.py) - Represents hardware device information and connection handling

2. **Mixins** (src/busylight_core/mixins/)
   - `ColorableMixin` - Provides color manipulation functionality
   - `TaskableMixin` - Provides task scheduling and management

3. **Vendor Implementations** (src/busylight_core/vendors/)
   - Each vendor has its own package (e.g., embrava/, luxafor/, kuando/)
   - Vendors implement device-specific `Light` subclasses
   - All vendor classes must be imported in `__init__.py` for discovery

### Device Support Pattern

To add a new device:
1. Create vendor package in `src/busylight_core/vendors/` if needed
2. Implement `Light` subclass with required abstract methods
3. Import the class in vendor's `__init__.py` and add to `__all__`
4. Import in main `__init__.py` and add to main `__all__`

The discovery mechanism relies on `abc.ABC.__subclasses__()` so all implementations must be imported.

### Connection Types

The library supports multiple connection types defined in `hardware.py`:
- HID (Human Interface Device) - Most common for USB devices
- Serial - For serial port devices  
- Bluetooth - For wireless devices

### CLI Interface

- Main CLI entry point: `src/busylight_core/__main__.py`
- Uses Typer for command-line interface
- CLI command is registered as `blc` in pyproject.toml
- Includes self-management subcommands

## Key Dependencies

- `typer` - CLI framework
- `loguru` - Logging
- `pydantic_settings` - Configuration management
- `hidapi` - HID device communication
- `pyserial` - Serial port communication

## Testing

Tests are located in `tests/` directory with vendor-specific examples in `tests/vendor_examples/`. The project uses pytest with coverage reporting.