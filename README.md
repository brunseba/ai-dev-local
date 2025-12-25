# AI Dev Local

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-github%20pages-blue.svg)](https://brunseba.github.io/ai-dev-local/)

A comprehensive AI lab for local development with various AI services and Model Context Protocol (MCP) integrations.

## 🚀 Features

- **Multiple AI Services**: Langfuse, FlowiseAI, Open WebUI, and LiteLLM Proxy
- **Local LLMs with Ollama**: Run AI models locally with flexible deployment options
- **Ollama Multi-Mode Support**: Connect to Docker, native, or remote Ollama servers
- **Vector Store**: OpenAI-compatible vector store API with PGVector for RAG workflows
- **MCP Integration**: GitLab, GitHub, and SonarQube MCP servers
- **IDE Integration**: Direct MCP server integration with VS Code, Codium, Cursor, and other editors
- **Unified CLI**: Manage all services from a single command-line interface
- **Docker Orchestration**: Easy deployment with Docker Compose
- **Docker Image Tracking**: Monitor and update Docker image versions
- **Development Tools**: Pre-commit hooks, testing, and documentation

## 📦 Installation

### Using pipx (Recommended)

```bash
pipx install ai-dev-local
```

### From Source

```bash
git clone https://github.com/brunseba/ai-dev-local.git
cd ai-dev-local
uv sync --extra dev
```

## 🏁 Quick Start

### Option 1: Full Stack Deployment

1. **Start all services**:
   ```bash
   ai-dev-local start
   ```

2. **Check service status**:
   ```bash
   ai-dev-local status
   ```

3. **Access web interfaces**:
   - Dashboard: http://localhost:3002
   - Langfuse: http://localhost:3000
   - FlowiseAI: http://localhost:3001
   - Open WebUI: http://localhost:8081
   - LiteLLM Proxy: http://localhost:4000
   - Vector Store API: http://localhost:8000

4. **Manage local AI models** (optional):
   ```bash
   # Start with local Ollama server (Docker mode)
   ai-dev-local start --ollama
   
   # Or use native/remote Ollama
   ai-dev-local ollama config set-mode native  # Use system Ollama
   ai-dev-local ollama config set-mode remote  # Use remote server
   
   # Browse and install AI models
   ai-dev-local ollama list-available --category code
   ai-dev-local ollama pull codellama:7b
   
   # View connection status
   ai-dev-local ollama config show
   
   # Sync models to unified API
   ai-dev-local ollama sync-litellm
   ```
   
   📖 **Ollama Setup Guide**: See [docs/ollama-external-setup.md](docs/ollama-external-setup.md)

5. **Track Docker image versions**:
   ```bash
   # List all Docker images used in the project
   ai-dev-local docker track-versions
   
   # Check for available updates on Docker Hub
   ai-dev-local docker track-versions --check-updates
   
   # Update a specific service image
   ai-dev-local docker update-image postgres --version 16
   ```

### Option 2: IDE MCP Integration (Recommended for Development)

1. **Configure your IDE** with the provided MCP settings:
   - **VS Code/Codium**: Use `.vscode/mcp.json` (workspace-specific)
   - **Global Setup**: Use `configs/ide-mcp/vscode-mcp.json`

2. **Set up access tokens**:
   - GitHub Personal Access Token
   - GitLab Token (optional)
   - SonarQube Token (optional)

3. **Start using MCP features** directly in your AI assistant within the IDE

📖 **Detailed Setup Guide**: See [docs/IDE_MCP_SETUP.md](docs/IDE_MCP_SETUP.md)

## 🛠️ Services

### Server Services

| Service | Description | Port | Documentation |
|---------|-------------|------|---------------|
| **Langfuse** | LLM observability and analytics | 3000 | [docs](https://langfuse.com/) |
| **FlowiseAI** | Visual AI workflow builder | 3001 | [docs](https://docs.flowiseai.com/) |
| **Open WebUI** | Chat interface for LLMs | 8080 | [docs](https://docs.openwebui.com/) |
| **LiteLLM Proxy** | Unified API for multiple LLM providers | 4000 | [docs](https://docs.litellm.ai/) |
| **Vector Store** | OpenAI-compatible vector store with pgvector | 8000 | [docs](docs/VECTOR_STORE.md) |

### MCP Services

| Service | Description | Repository | IDE Support |
|---------|-------------|------------|-------------|
| **GitLab MCP** | GitLab integration | [gitlab-mcp](https://github.com/zereight/gitlab-mcp) | ✅ Configured |
| **GitHub MCP** | GitHub integration | [github-mcp-server](https://github.com/github/github-mcp-server) | ✅ Configured |
| **SonarQube MCP** | Code quality analysis | [sonarqube-mcp-server](https://github.com/SonarSource/sonarqube-mcp-server) | ✅ Configured |

**IDE Integration**: Pre-configured for VS Code, Codium, Cursor, and other MCP-compatible editors. See [IDE MCP Setup Guide](docs/IDE_MCP_SETUP.md) for details.

## 🔧 Development

### Prerequisites

- Python 3.10+
- UV package manager
- Docker and Docker Compose
- Git

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/brunseba/ai-dev-local.git
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
├── src/ai_dev_local/          # Main package
├── tests/                     # Unit tests
├── docs/                      # Documentation
│   ├── IDE_MCP_SETUP.md      # IDE MCP integration guide
│   └── PHASE_3_MCP_INTEGRATION.md # MCP implementation plan
├── configs/                   # Configuration files
│   └── ide-mcp/              # IDE MCP configurations
│       └── vscode-mcp.json   # Global VS Code/Codium MCP config
├── .vscode/                   # VS Code workspace settings
│   └── mcp.json              # Workspace MCP configuration
├── docker/                    # Docker configurations
├── scripts/                   # Utility scripts
├── pyproject.toml            # Project configuration
├── mkdocs.yml               # Documentation configuration
└── README.md                # This file
```

## 📚 Documentation

Full documentation is available at [brunseba.github.io/ai-dev-local](https://brunseba.github.io/ai-dev-local/).

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
