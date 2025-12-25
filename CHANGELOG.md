# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2025-12-25

### Added
- **Ollama External Server Support**: Connect to Ollama in multiple deployment modes
  - Docker mode: Use Ollama in Docker Compose (default)
  - Native mode: Use system-installed Ollama (brew/apt)
  - Remote mode: Connect to remote Ollama server
  - Auto mode: Automatically detect available Ollama
- **Ollama Configuration Commands**: New `ollama config` command group
  - `ollama config show`: Display current connection configuration
  - `ollama config set-mode`: Change connection mode (auto/docker/native/remote)
  - `ollama config set-url`: Set remote server URL
  - `ollama config test`: Test all connection modes
- **Connection Abstraction**: `OllamaConnection` class for unified Ollama access
- **API Client**: HTTP API client for remote Ollama servers
- **Documentation**: Comprehensive Ollama external setup guide

### Changed
- All `ollama` commands now display current connection mode in output
- All `ollama` commands work with any connection mode
- Ollama commands use connection abstraction instead of hardcoded docker-compose calls
- `ollama sync-litellm` intelligently configures API base URL based on connection mode

### Technical Details
- New module: `src/ai_dev_local/ollama_connection.py`
- New environment variables:
  - `OLLAMA_CONNECTION_MODE`: Connection mode selection
  - `OLLAMA_API_URL`: Remote/native API endpoint
  - `OLLAMA_DOCKER_COMPOSE_FILE`: Docker compose file path
  - `OLLAMA_DOCKER_SERVICE`: Docker service name

## [0.2.1] - 2025-12-25

### Added
- Initial release with core features
- Multiple AI services integration (Langfuse, FlowiseAI, Open WebUI, LiteLLM)
- Docker-based Ollama support
- MCP (Model Context Protocol) integration
- IDE integration support
- Unified CLI for service management
- Configuration management commands
- Docker image tracking and updates

[Unreleased]: https://github.com/brunseba/ai-dev-local/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/brunseba/ai-dev-local/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/brunseba/ai-dev-local/releases/tag/v0.2.1
