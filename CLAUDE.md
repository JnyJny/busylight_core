# CLAUDE.md

Python library for controlling USB status lights from various vendors using a plugin architecture.

## Commands
- `poe test` - Run tests
- `poe ruff` - Format and lint
- `poe coverage` - Coverage report
- `poe docs-serve` - Serve docs locally

## Architecture
- **Light** (src/busylight_core/light.py) - Base class for all devices
- **Hardware** (src/busylight_core/hardware.py) - Device connection handling
- **Vendors** (src/busylight_core/vendors/) - Device-specific implementations
- **Mixins** - ColorableMixin, TaskableMixin for shared functionality

### Adding Devices
1. Create vendor package in vendors/ if needed  
2. Implement Light subclass
3. Import in vendor __init__.py and main __init__.py
4. Discovery uses abc.ABC.__subclasses__()

## Code Guidelines

**Architecture**: **DO NOT** consolidate vendor classes - this breaks plugin discovery and type safety.

**Docstrings**: Use Sphinx format focusing on programmer intent:
```python
def method(self, param: str) -> bool:
    """Brief summary.
    
    :param param: What user provides
    :return: How to use result
    """
```

**Patterns**: Three device types - simple (ColorableMixin), complex (Word/BitField), multi-LED (arrays). Preserve these patterns.

**Quality**: Run `poe ruff` before commits.