# CLI Usage

Busylight Core for Humans provides a command-line interface built with Typer.

## Basic Syntax

```bash
busylight_core [OPTIONS] [COMMAND] [ARGS]...
```

## Global Options

The following options are available for all commands:

- `--help`: Show help message and exit
- `--version`: Show version and exit

## Commands

### Help

Get help for the CLI or any specific command:

```bash
busylight_core --help
busylight_core [command] --help
```

### Version

Display the version:

```bash
busylight_core --version
```

## Self-Subcommands

Busylight Core for Humans uses a self-subcommand pattern, where the main command can also act as a subcommand. This provides a clean and intuitive interface.

## Logging

The CLI uses structured logging with Loguru. You can control the log level using:

```bash
busylight_core --log-level DEBUG [command]
```

## Log Files

By default, logs are also written to `busylight_core.log` in the current directory.
## Examples

For specific usage examples, see the [Examples](examples.md) page.

## Error Handling

The CLI provides clear error messages and appropriate exit codes:

- `0`: Success
- `1`: General error
- `2`: Command line usage error

## Shell Completion

Busylight Core for Humans supports shell completion for bash, zsh, and fish. To enable it:

### Bash

```bash
eval "$(_BUSYLIGHT_CORE_COMPLETE=bash_source busylight_core)"
```

### Zsh

```bash
eval "$(_BUSYLIGHT_CORE_COMPLETE=zsh_source busylight_core)"
```

### Fish

```bash
eval "$(_BUSYLIGHT_CORE_COMPLETE=fish_source busylight_core)"
```