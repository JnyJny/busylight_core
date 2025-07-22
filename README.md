
[![Release][badge-release]][release]
![Version][badge-pypi-version]
![Release Date][badge-release-date]
![Python Version][badge-python-version]
![License][badge-license]
![Monthly Downloads][badge-monthly-downloads]
# Busylight Core for Humans™

> A unified Python library for controlling USB status lights (busylights) from multiple vendors

**busylight-core** provides a consistent interface to control various
USB-connected status lights, commonly used for indicating
availability, meeting status, or system notifications. Were you
looking for a command-line interface to control your lights? Check out
[Busylight for Humans™][busylight-for-humans]!

## Features

- **Multi-Vendor Support** - Control devices from nine vendors.
- **Multiple Connection Types** - HID and Serial device support.
- **Python Library** - Clean, object-oriented API for easy integration.
- **Input Detection** - Button press handling on interactive devices.
- **Multi-LED Support** - Control devices with 1-192 individual LEDs.
- **Extensible Architecture** - Easy to add support for new devices.

## Supported Hardware

| Vendor | Device Models |
|--------|---------------|
| **Agile Innovative** | BlinkStick, BlinkStick Pro, BlinkStick Flex, BlickStick Nano, BlinkStick Strip, BlinkStick Square |
| **CompuLab** | fit-statUSB |
| **EPOS** | Busylight |
| **Embrava** | Blynclight, Blynclight Mini, Blynclight Plus |
| **Kuando** | Busylight Alpha, Busylight Omega, Mute |
| **Luxafor** | Flag, Mute, Orb, Bluetooth |
| **MuteMe** | MuteMe, MuteMe Mini, MuteSync |
| **Plantronics** | Status Indicator |
| **ThingM** | Blink(1) |


## Installation

### Install with uv
```console
uv add busylight_core
```

### Install with pip
```console
python3 -m pip install busylight_core
```

## Usage

```python
from busylight_core import Light

lights = Light.all_lights()

print(f"Found {len(lights)} light(s)")

for light in lights:
    light.on((255, 0, 0))  # Turn on red
    light.off()            # Turn off
```

### Common Use Cases

**Meeting Status Indicator:**
```python
from busylight_core import Light

red = (255, 0, 0)
green = (0, 128, 0)
yellow = (255, 255, 0)

light = Light.first_light()

# Available
light.on(green)

# In meeting
light.on(red)

# Away
light.on(yellow)

light.off()
```


## Documentation

For detailed documentation including API reference, advanced usage examples, and device-specific information:

- **Full Documentation**: [https://JnyJny.github.io/busylight_core/](https://JnyJny.github.io/busylight_core/)
- **Quick Start Guide**: [Getting Started](https://JnyJny.github.io/busylight_core/getting-started/quickstart/)
- **Examples**: [Usage Examples](https://JnyJny.github.io/busylight_core/user-guide/examples/)
- **API Reference**: [API Docs](https://JnyJny.github.io/busylight_core/reference/)

## Development

This project and it's virtual environment is managed using [uv][uv] and
is configured to support automatic activation of virtual environments
using [direnv][direnv]. Development activites such as linting and testing
are automated via [Poe The Poet][poethepoet], run `poe` after cloning
this repo for a list of tasks.

### Clone
```console
git clone https://github.com/JnyJny/busylight_core
cd busylight_core
```
### Allow Direnv _optional_ but recommended
```console
direnv allow
```

### Install Dependencies
```console
uv sync --all-groups
```
### Run `poe`
```console
poe --help
```

### Release Management

This project uses automated release management with GitHub Actions:

#### Version Bumping
- `poe publish_patch` - Bump patch version, commit, tag, and push
- `poe publish_minor` - Bump minor version, commit, tag, and push
- `poe publish_major` - Bump major version, commit, tag, and push

Any of the publish tasks will trigger testing, publishing to PyPi, and
a GitHub release.

#### Release Notes
- `poe changelog` - Generate changelog since last tag
- `poe release-notes` - Generate release notes file

#### Automatic Releases
When you push a version tag (e.g., `v1.0.0`), the unified GitHub Actions workflow will:
1. **Test** - Run tests across all supported Python versions and OS combinations
2. **Publish** - Build and publish to PyPI (only if tests pass)
3. **GitHub Release** - Create GitHub release with auto-generated notes and artifacts (only if PyPI publish succeeds)

This ensures a complete release pipeline where each step depends on
the previous step's success.

#### MkDocs Documentation
- `poe docs-serve` - Serve documentation locally
- `poe docs-build` - Build documentation
- `poe docs-deploy` - Deploy to GitHub Pages


<hr>

[![gh:JnyJny/python-package-cookiecutter][python-package-cookiecutter-badge]][python-package-cookiecutter]

<!-- End Links -->
[busylight-for-humans]: https://github.com/JnyJny/busylight
[python-package-cookiecutter-badge]: https://img.shields.io/badge/Made_With_Cookiecutter-python--package--cookiecutter-green?style=for-the-badge
[python-package-cookiecutter]: https://github.com/JnyJny/python-package-cookiecutter
[badge-release]: https://github.com/JnyJny/busylight_core/actions/workflows/release.yaml/badge.svg
[release]: https://github.com/JnyJny/busylight_core/actions/workflows/release.yaml
[badge-pypi-version]: https://img.shields.io/pypi/v/busylight_core
[badge-release-date]: https://img.shields.io/github/release-date/JnyJny/busylight_core
[badge-python-version]: https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2FJnyJny%2Fbusylight_core%2Fmain%2Fpyproject.toml
[badge-license]: https://img.shields.io/github/license/JnyJny/busylight_core
[badge-monthly-downloads]: https://img.shields.io/pypi/dm/busylight_core
[poe]: https://poethepoet.natn.io
[uv]: https://docs.astral.sh/uv/
[direnv]: https://direnv.net
