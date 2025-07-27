# CLI Reference

AI Dev Local CLI provides various commands to manage and operate AI services effectively.

## Commands Overview

### Core Commands

#### `ai-dev-local start`

Starts all the AI services defined in your configuration.

```bash
ai-dev-local start
```

#### `ai-dev-local stop`

Stops all running AI services cleanly.

```bash
ai-dev-local stop
```

#### `ai-dev-local status`

Displays the current status of all AI services.

```bash
ai-dev-local status
```

### Configuration Commands

#### `ai-dev-local config init`

Initializes the configuration file with default settings.

```bash
ai-dev-local config init
```

#### `ai-dev-local config set <KEY> <VALUE>`

Updates the configuration with a specific key-value pair.

```bash
ai-dev-local config set OPENAI_API_KEY your-api-key
```

#### `ai-dev-local config validate`

Checks the current configuration for missing or incorrect settings.

```bash
ai-dev-local config validate
```

### Utility Commands

#### `ai-dev-local logs`

Fetches logs from running AI services for debugging and analysis.

```bash
ai-dev-local logs
```

#### `ai-dev-local version`

Displays the current version of AI Dev Local installed.

```bash
ai-dev-local version
```

## Additional Information

For more detailed CLI usage, use the `--help` flag with any command:

```bash
ai-dev-local --help
```
