# Installation

Busylight Core for Humans requires Python 3.8 or later.

## Install from PyPI

The easiest way to install busylight_core is from PyPI:

```bash
pip install busylight_core
```

## Install from Source

You can also install from source:

```bash
git clone https://github.com/JnyJny/busylight_core.git
cd busylight_core
pip install -e .
```

## Development Installation

For development, we recommend using `uv`:

```bash
git clone https://github.com/JnyJny/busylight_core.git
cd busylight_core
uv sync
```

This will install all dependencies including development tools.

## Verify Installation

After installation, verify that busylight_core is working:

```bash
busylight_core --version
```

You should see the version number displayed.

## Next Steps

Now that you have busylight_core installed, check out the [Quick Start](quickstart.md) guide to learn how to use it.