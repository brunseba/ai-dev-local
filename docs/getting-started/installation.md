# Installation Guide

This guide will help you install and set up AI Dev Local on your system.

## Prerequisites

Before installing AI Dev Local, ensure you have the following prerequisites:

### Required
- **Python 3.10+** - AI Dev Local requires Python 3.10 or higher
- **Docker & Docker Compose** - For running the containerized services
- **pipx** - For isolated Python package installation

### Recommended
- **Git** - For version control integration
- **curl** - For API testing and health checks

## Installation Methods

### Method 1: pipx (Recommended)

pipx installs Python packages in isolated environments, preventing dependency conflicts:

```bash
# Install pipx if you haven't already
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# Install AI Dev Local
pipx install ai-dev-local

# Verify installation
ai-dev-local --version
```

### Method 2: pip (Global Installation)

!!! warning "Not Recommended"
    Global pip installation can cause dependency conflicts. Use pipx instead.

```bash
pip install ai-dev-local
```

### Method 3: Development Installation

For development or contributing to the project:

```bash
# Clone the repository
git clone https://github.com/brunseba/ai-dev-local.git
cd ai-dev-local

# Install in development mode
pip install -e .

# Or using uv (faster)
uv pip install -e .
```

## System Setup

### Docker Installation

AI Dev Local requires Docker and Docker Compose:

=== "macOS"
    ```bash
    # Install Docker Desktop
    brew install --cask docker
    
    # Start Docker Desktop
    open /Applications/Docker.app
    ```

=== "Ubuntu/Debian"
    ```bash
    # Install Docker
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    
    # Install Docker Compose
    sudo apt-get update
    sudo apt-get install docker-compose-plugin
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    newgrp docker
    ```

=== "Windows"
    1. Download and install [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
    2. Ensure WSL2 is enabled
    3. Restart your system after installation

### Verify Docker Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker installation
docker run hello-world
```

## Initial Setup

### 1. Initialize Configuration

```bash
# Create initial configuration
ai-dev-local config init
```

This creates a `.env` file from the template with default values.

### 2. Configure API Keys

Set your OpenAI API key (required):

```bash
ai-dev-local config set OPENAI_API_KEY your-actual-api-key-here
```

Optional: Configure additional LLM providers:

```bash
ai-dev-local config set ANTHROPIC_API_KEY your-anthropic-key
ai-dev-local config set GEMINI_API_KEY your-gemini-key
ai-dev-local config set COHERE_API_KEY your-cohere-key
```

### 3. Validate Configuration

```bash
ai-dev-local config validate
```

### 4. Start Services

```bash
# Start all core services
ai-dev-local start

# Or start with Ollama for local models
ai-dev-local start --ollama
```

### 5. Verify Installation

```bash
# Check service status
ai-dev-local status

# Access the dashboard
open http://localhost:3002
```

## Post-Installation

### Access Services

After successful installation, you can access:

| Service | URL | Purpose |
|---------|-----|---------|
| **Dashboard** | http://localhost:3002 | Main control panel |
| **Open WebUI** | http://localhost:8081 | Chat interface |
| **FlowiseAI** | http://localhost:3001 | Visual workflows |
| **Langfuse** | http://localhost:3000 | LLM observability |
| **LiteLLM** | http://localhost:4000 | API gateway |
| **Documentation** | http://localhost:8000 | This documentation |

### Default Credentials

Some services require login credentials:

| Service | Username | Password |
|---------|----------|----------|
| **FlowiseAI** | admin | admin123 |
| **LiteLLM UI** | admin | admin123 |

!!! warning "Security"
    Change default passwords in production environments using the [Configuration Guide](../CONFIGURATION.md).

## Troubleshooting

### Common Installation Issues

#### Permission Denied Errors
```bash
# Fix Docker permissions (Linux/macOS)
sudo usermod -aG docker $USER
newgrp docker

# Fix file permissions
sudo chown -R $USER:$USER ~/.local/share/pipx
```

#### Port Conflicts
```bash
# Check what's using a port
lsof -i :3000

# Change conflicting ports
ai-dev-local config set LANGFUSE_PORT 3030
```

#### Docker Issues
```bash
# Restart Docker daemon
sudo systemctl restart docker  # Linux
# Or restart Docker Desktop on macOS/Windows

# Clean Docker system
docker system prune -a
```

#### Python Version Issues
```bash
# Check Python version
python3 --version

# Install Python 3.10+ using pyenv
curl https://pyenv.run | bash
pyenv install 3.11.0
pyenv global 3.11.0
```

### Getting Help

If you encounter issues:

1. **Check the logs**: `ai-dev-local logs`
2. **Validate configuration**: `ai-dev-local config validate`
3. **Review documentation**: [Configuration Guide](../CONFIGURATION.md)
4. **Search existing issues**: [GitHub Issues](https://github.com/brunseba/ai-dev-local/issues)
5. **Report new issues**: [Create Issue](https://github.com/brunseba/ai-dev-local/issues/new)

## Next Steps

After successful installation:

1. **[Quick Start Tutorial](quick-start.md)** - Learn the basics
2. **[Configuration Guide](../CONFIGURATION.md)** - Customize your setup
3. **[IDE MCP Setup](../IDE_MCP_SETUP.md)** - Integrate with your editor

## Uninstallation

To completely remove AI Dev Local:

```bash
# Stop and remove all services
ai-dev-local stop
ai-dev-local down --volumes

# Remove the CLI tool
pipx uninstall ai-dev-local

# Clean up Docker resources
docker system prune -a

# Remove configuration (optional)
rm -rf .env .ai-dev-local/
```
