# Examples

This page provides practical examples of using Busylight Core for Humans.

## Basic Usage

### Getting Help

```bash
# Show main help
busylight_core --help

# Show help for a specific command
busylight_core [command] --help
```

### Check Version

```bash
busylight_core --version
```

## Advanced Usage

### Using with Different Log Levels

```bash
# Run with debug logging
busylight_core --log-level DEBUG [command]

# Run with minimal logging
busylight_core --log-level ERROR [command]
```

### Using with Configuration

```bash
# Set configuration via environment variables
export BUSYLIGHT_CORE_SETTING_NAME=value
busylight_core [command]

# Or create a .env file
echo "BUSYLIGHT_CORE_SETTING_NAME=value" > .env
busylight_core [command]
```
## Common Workflows

### Example Workflow 1

```bash
# Step 1: Initialize
busylight_core init

# Step 2: Process
busylight_core process --input file.txt

# Step 3: Output
busylight_core output --format json
```

### Example Workflow 2

```bash
# One-liner example
busylight_core process --input file.txt --output result.txt --verbose
```

## Error Handling Examples

### Common Errors

```bash
# File not found
busylight_core process --input nonexistent.txt
# Error: Input file 'nonexistent.txt' not found

# Invalid option
busylight_core --invalid-option
# Error: No such option: --invalid-option
```

### Debugging

```bash
# Run with debug logging to troubleshoot
busylight_core --log-level DEBUG process --input file.txt
```

## Integration Examples

### Use in Scripts

```bash
#!/bin/bash
set -e

# Check if busylight_core is installed
if ! command -v busylight_core &> /dev/null; then
    echo "busylight_core is not installed"
    exit 1
fi

# Run the command
busylight_core process --input "$1" --output "$2"
echo "Processing complete"
```

### Use with Make

```makefile
.PHONY: process
process:
	busylight_core process --input input.txt --output output.txt

.PHONY: clean
clean:
	rm -f output.txt busylight_core.log
```

## Performance Tips

- Use appropriate log levels in production
- Process files in batches when possible
- Use configuration files for repeated settings

## Next Steps

- Learn more about the [API Reference](../reference/)
- Check out the [Contributing Guide](../contributing.md)
- Visit the [GitHub repository](https://github.com/JnyJny/busylight_core)