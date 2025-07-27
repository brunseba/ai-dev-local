# AI Dev Local

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-github%20pages-blue.svg)](https://yourusername.github.io/ai-dev-local/)

A comprehensive AI lab for local development with various AI services and Model Context Protocol (MCP) integrations.

## 🚀 Features

- **Multiple AI Services**: Langfuse, FlowiseAI, Open WebUI, and LiteLLM Proxy
- **MCP Integration**: GitLab, GitHub, and SonarQube MCP servers
- **Unified CLI**: Manage all services from a single command-line interface
- **Docker Orchestration**: Easy deployment with Docker Compose
- **Development Tools**: Pre-commit hooks, testing, and documentation

## 📦 Installation

### Using pipx (Recommended)

```bash
pipx install ai-dev-local
```

### From Source

```bash
git clone https://github.com/yourusername/ai-dev-local.git
cd ai-dev-local
uv sync --extra dev
```

## 🏁 Quick Start

1. **Start all services**:
   ```bash
   ai-dev-local start
   ```

2. **Check service status**:
   ```bash
   ai-dev-local status
   ```

3. **Access web interfaces**:
   - Langfuse: http://localhost:3000
   - FlowiseAI: http://localhost:3001
   - Open WebUI: http://localhost:8080
   - LiteLLM Proxy: http://localhost:4000

## 🛠️ Services

### Server Services

| Service | Description | Port | Documentation |
|---------|-------------|------|---------------|
| **Langfuse** | LLM observability and analytics | 3000 | [docs](https://langfuse.com/) |
| **FlowiseAI** | Visual AI workflow builder | 3001 | [docs](https://docs.flowiseai.com/) |
| **Open WebUI** | Chat interface for LLMs | 8080 | [docs](https://docs.openwebui.com/) |
| **LiteLLM Proxy** | Unified API for multiple LLM providers | 4000 | [docs](https://docs.litellm.ai/) |

### MCP Services

| Service | Description | Repository |
|---------|-------------|------------|
| **GitLab MCP** | GitLab integration | [gitlab-mcp](https://github.com/zereight/gitlab-mcp) |
| **GitHub MCP** | GitHub integration | [github-mcp-server](https://github.com/github/github-mcp-server) |
| **SonarQube MCP** | Code quality analysis | [sonarqube-mcp-server](https://github.com/SonarSource/sonarqube-mcp-server) |

## 🔧 Development

### Prerequisites

- Python 3.10+
- UV package manager
- Docker and Docker Compose
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-dev-local.git
cd ai-dev-local

# Install dependencies
uv sync --extra dev --extra docs

# Install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Run tests
pytest

# Format code
black src tests
```

### Project Structure

```
ai-dev-local/
├── src/ai_dev_local/     # Main package
├── tests/                # Unit tests
├── docs/                 # Documentation
├── docker/               # Docker configurations
├── scripts/              # Utility scripts
├── pyproject.toml        # Project configuration
├── mkdocs.yml           # Documentation configuration
└── README.md            # This file
```

## 📚 Documentation

Full documentation is available at [yourusername.github.io/ai-dev-local](https://yourusername.github.io/ai-dev-local/).

### Building Documentation Locally

```bash
# Install docs dependencies
uv sync --extra docs

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

## 🤝 Contributing

We welcome contributions! Please see our [contributing guidelines](CONTRIBUTING.md) for details.

### Commit Convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions or modifications
- `chore:` Maintenance tasks

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Langfuse](https://langfuse.com/) for LLM observability
- [FlowiseAI](https://flowiseai.com/) for visual AI workflows
- [Open WebUI](https://openwebui.com/) for the chat interface
- [LiteLLM](https://litellm.ai/) for LLM proxy capabilities
- The MCP community for protocol development

---

**Version**: 0.1.0
