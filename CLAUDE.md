# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when
working with code in this repository.

## Project Overview

This is `busylight_core`, a Python library for controlling
USB-connected status lights (busylights) from various vendors. The
project provides a unified interface for controlling different
hardware devices through a plugin-style architecture where each vendor
implements the abstract `Light` class.

## Development Commands

The project uses [Poe the Poet](https://poethepoet.natn.io) for task
automation. Run `poe` without arguments to see all available tasks.

### Essential Commands
- `poe test` - Run test suite with pytest
- `poe ruff-format` - Run ruff format on src and tests
- `poe ruff-check` - Run ruff check on src and tests
- `poe ruff` - Run code formatting and linting (check + format)
- `poe coverage` - Generate and open HTML coverage report

### Development Setup
- `uv sync --all-groups` - Install dependencies and create virtual environment
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

Tests are located in `tests/` directory with vendor-specific examples
in `tests/vendor_examples/`. The project uses pytest with coverage
reporting.

## Code Quality and Architecture Notes

<!-- EJO claude's evaluation take with a grain of salt -->
### Excellent Architecture - Avoid Over-Engineering

This codebase demonstrates **exemplary software architecture** with minimal
code duplication. What may initially appear as "duplicate code" across vendor
implementations is typically one of:

1. **Necessary device-specific configuration** (device IDs, hardware detection)
2. **Well-designed inheritance patterns** that properly share functionality
3. **Type-safe plugin architecture** where separate classes enable discovery

**True code duplication is minimal (~5-10%)** and consists primarily of:
- BlinkStick `claims()` methods (~50 lines total)
- Vendor base class `vendor()` methods (~15 lines total)

### Design Principles Prioritized

The current architecture correctly prioritizes:
- ✅ **Clarity**: Each device class is self-contained and obvious
- ✅ **Type safety**: Static analysis works well with separate classes
- ✅ **Maintainability**: Device-specific issues are isolated
- ✅ **Plugin architecture**: Discovery mechanism relies on separate classes
- ✅ **Hardware abstraction**: Complex device differences are properly
  encapsulated

### What NOT to do

**Avoid template/mixin consolidation efforts** that would:
- Make inheritance hierarchies confusing
- Compromise type safety for marginal code savings
- Create complex abstractions for naturally device-specific logic
- Break the plugin discovery mechanism

The apparent "duplication" serves important architectural purposes.
Device-specific classes should remain separate even when they share similar
patterns.

### Successful Refactorings Completed

- ✅ Enhanced `Word.__str__()` with BitField introspection for better debugging
- ✅ Consistent naming across vendor classes (removed underscores)
- ✅ Complete vendor base class hierarchy for all vendors
- ✅ Enhanced async task management with prioritization and error handling

### Docstring Format

Use **Sphinx reStructuredText format** focusing on programmer intent:

```python
def method(self, param: str) -> bool:
    """Single-line summary of what this does.

    Explain the programmer's intent - how and why other code should use
    this. Focus on expected inputs, actions taken, exceptions that might
    be raised, and how to use returned values.

    :param param: What the user should provide (not the type)
    :raises SomeError: When this might fail and why
    :return: How the returned value should be used
    """
```

**Key principles:**
- Document programmer intent, not implementation details
- Explain expected inputs and return value usage
- Type hints handle type information - don't duplicate in docstrings
- Use compact `:param name: description` format
- Always document exceptions that callers should handle

### Vendor Implementation Patterns

The codebase uses three main device implementation patterns, each appropriate
for different hardware complexity:

1. **Simple devices** (CompuLab): ColorableMixin + simple protocol
2. **Complex devices** (Embrava, Kuando): Word/BitField state management
3. **Multi-LED devices** (BlinkStick, Luxafor): Array-based LED management

These patterns should be preserved rather than consolidated.

## TODO and Reminders

- Review `.github/workflows/release.yaml` for auto-generate-changelog task and TYPE variable describing the tags used to recognize important commit messages and use those tags in commits.