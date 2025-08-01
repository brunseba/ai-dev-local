# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

## [0.2.1] - 2025-01-27

### Added
- **Comprehensive Installation Guide** (`docs/getting-started/installation.md`):
  - Multiple installation methods (pipx, pip, development)
  - System setup instructions for Docker and prerequisites
  - Platform-specific guidance (macOS, Ubuntu/Debian, Windows)
  - Post-installation verification and troubleshooting
- **Quick Start Tutorial** (`docs/getting-started/quick-start.md`):
  - Step-by-step tutorial for new users
  - Basic configuration and service launch
  - Overview of key features and services
- **Service Documentation**:
  - Langfuse service guide (`docs/services/langfuse.md`)
  - FlowiseAI service guide (`docs/services/flowiseai.md`)
  - Open WebUI service guide (`docs/services/open-webui.md`)
  - LiteLLM Proxy service guide (`docs/services/litellm.md`)
- **LiteLLM Troubleshooting Section**:
  - Detailed troubleshooting for "Invalid HTTP request" warnings
  - API key configuration and validation steps
  - Health check diagnostics and solutions
  - Common issues and their resolutions

### Changed
- Updated main documentation index with troubleshooting references
- Improved navigation structure in documentation
- Enhanced user experience with better cross-references

## [0.2.0] - 2024-07-27

### Added
- Initial project structure with Python 3.10+ support
- CLI framework with Click
- Pre-commit hooks for code quality
- MkDocs documentation with Material theme
- GitHub Actions workflows for CI/CD
- Docker support preparation
- Unit testing framework with pytest
- **IDE MCP Configuration Files**:
  - VS Code/Codium workspace MCP configuration (`.vscode/mcp.json`)
  - Global IDE MCP configuration template (`configs/ide-mcp/vscode-mcp.json`)
  - Support for GitHub, GitLab, and SonarQube MCP servers
- **Comprehensive IDE MCP Setup Guide** (`docs/IDE_MCP_SETUP.md`):
  - Step-by-step setup instructions for multiple IDEs
  - Token configuration and security guidelines
  - Troubleshooting and debugging information
  - Usage examples and best practices
- **Enhanced MCP Integration Documentation**:
  - Updated Phase 3 MCP integration plan
  - Architecture diagrams and implementation roadmap
  - Security considerations and deployment options

### Changed

### Deprecated

### Removed

### Fixed

### Security

## [0.1.0] - 2024-07-27

### Added
- Initial project setup
- Basic CLI structure
- Documentation framework
- Development tooling

[Unreleased]: https://github.com/brunseba/ai-dev-local/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/brunseba/ai-dev-local/releases/tag/v0.2.1
[0.2.0]: https://github.com/brunseba/ai-dev-local/releases/tag/v0.2.0
[0.1.0]: https://github.com/brunseba/ai-dev-local/releases/tag/v0.1.0
