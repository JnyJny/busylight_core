# Configuration

Busylight Core for Humans uses Pydantic Settings for configuration management, which allows you to configure the application using environment variables, configuration files, or both.

## Environment Variables

You can configure busylight_core using environment variables:

```bash
export BUSYLIGHT_CORE_SETTING_NAME=value
busylight_core [command]
```

## Configuration File

You can also use a configuration file. Create a `.env` file in your project directory:

```bash
# .env
BUSYLIGHT_CORE_SETTING_NAME=value
```

## Available Settings

The following settings are available:

### Logging Settings

- `BUSYLIGHT_CORE_LOG_LEVEL`: Set the logging level (default: INFO)
- `BUSYLIGHT_CORE_LOG_FILE`: Path to log file (default: busylight_core.log)
### Application Settings

Add your application-specific settings here.

## Priority Order

Settings are loaded in the following priority order (highest to lowest):

1. Environment variables
2. Configuration file (`.env`)
3. Default values

## Example

```bash
# Set log level to DEBUG
export BUSYLIGHT_CORE_LOG_LEVEL=DEBUG

# Run the CLI
busylight_core [command]
```

