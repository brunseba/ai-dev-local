# Configuration Guide

This guide explains how to configure AI Dev Local for your specific needs.

## Quick Start

1. **Initialize configuration:**
   ```bash
   ai-dev-local config init
   ```

2. **Set your OpenAI API key:**
   ```bash
   ai-dev-local config set OPENAI_API_KEY your-actual-api-key-here
   ```

3. **Validate configuration:**
   ```bash
   ai-dev-local config validate
   ```

4. **Start services:**
   ```bash
   ai-dev-local start
   ```

## Configuration Management Commands

### Initialize Configuration
```bash
ai-dev-local config init
```
Creates `.env` file from `.env.example` template.

### Set Configuration Values
```bash
ai-dev-local config set KEY VALUE
```
Updates a specific configuration value.

### View Configuration
```bash
ai-dev-local config show           # Show all settings
ai-dev-local config show API_KEY   # Show specific setting
```

### Validate Configuration
```bash
ai-dev-local config validate
```
Checks if required settings are configured.

### Edit Configuration
```bash
ai-dev-local config edit
```
Opens `.env` file in your default editor.

## Required Configuration

### OpenAI API Key (Required)
```bash
OPENAI_API_KEY=your-openai-api-key
```
- Get from: https://platform.openai.com/api-keys
- Used for: GPT models (gpt-3.5-turbo, gpt-4, etc.)

### Security Keys (Required)
```bash
WEBUI_SECRET_KEY=your-secure-secret-key
WEBUI_JWT_SECRET_KEY=your-jwt-secret-key
LITELLM_MASTER_KEY=your-litellm-master-key
```
- Change default values for security
- Use random, strong keys

## Optional LLM Provider API Keys

### Anthropic (Claude Models)
```bash
ANTHROPIC_API_KEY=your-anthropic-api-key
```
- Get from: https://console.anthropic.com/
- Enables: Claude models (claude-3-sonnet, claude-3-haiku, etc.)

### Google Gemini
```bash
GEMINI_API_KEY=your-gemini-api-key
```
- Get from: https://aistudio.google.com/app/apikey
- Enables: Gemini models (gemini-pro, gemini-pro-vision, etc.)

### Cohere
```bash
COHERE_API_KEY=your-cohere-api-key
```
- Get from: https://dashboard.cohere.ai/api-keys
- Enables: Cohere models (command, command-light, etc.)

## Port Configuration

All service ports can be customized:

```bash
POSTGRES_PORT=5432     # PostgreSQL database
REDIS_PORT=6379        # Redis cache/queue
LANGFUSE_PORT=3000     # Langfuse analytics
FLOWISE_PORT=3001      # FlowiseAI workflows
OPENWEBUI_PORT=8081    # Open WebUI chat
LITELLM_PORT=4000      # LiteLLM proxy
OLLAMA_PORT=11434      # Ollama local LLM
DASHBOARD_PORT=3002    # Main dashboard
MKDOCS_PORT=8000       # Documentation
```

### Handling Port Conflicts

If you have port conflicts, update the relevant port:

```bash
ai-dev-local config set LANGFUSE_PORT 3030
ai-dev-local config set FLOWISE_PORT 3031
```

## Service-Specific Configuration

### Ollama (Local LLMs)

Configure local LLM models:

```bash
OLLAMA_AUTO_PULL_MODELS=llama2:7b,codellama:7b,mistral:7b,phi:2.7b
OLLAMA_GPU=false  # Set to true for NVIDIA GPU support
```

Start with Ollama:
```bash
ai-dev-local start --ollama
ai-dev-local ollama init  # Pull configured models
```

### Langfuse Analytics

Configure observability for your LLM applications:

```bash
LANGFUSE_PUBLIC_KEY=pk-your-public-key
LANGFUSE_SECRET_KEY=sk-your-secret-key
TELEMETRY_ENABLED=true
```

### FlowiseAI Workflows

Configure visual AI workflow builder:

```bash
DEBUG=false
LOG_LEVEL=info
DISABLE_FLOWISE_TELEMETRY=false
```

## Advanced Configuration

### MCP (Model Context Protocol)

Configure advanced AI agent integrations:

```bash
# GitHub integration
GITHUB_PERSONAL_ACCESS_TOKEN=your-github-pat
GITHUB_TOOLSETS=repos,issues,pull_requests,actions

# GitLab integration
GITLAB_TOKEN=your-gitlab-token
GITLAB_URL=https://gitlab.com

# Git configuration
GIT_AUTHOR_NAME=Your Name
GIT_AUTHOR_EMAIL=your@email.com
```

### Database Settings

Usually don't need to change:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

## Environment-Specific Configurations

### Development Environment
```bash
DEBUG=true
LOG_LEVEL=debug
TELEMETRY_ENABLED=false
```

### Production Environment
```bash
DEBUG=false
LOG_LEVEL=info
TELEMETRY_ENABLED=true
# Use strong, unique secrets
```

## Troubleshooting Configuration

### Check Current Configuration
```bash
ai-dev-local config show
```

### Validate Setup
```bash
ai-dev-local config validate
```

### Reset Configuration
```bash
rm .env
ai-dev-local config init
```

### Common Issues

1. **Missing API Keys**: Run `ai-dev-local config validate`
2. **Port Conflicts**: Change conflicting ports in `.env`
3. **Permission Issues**: Check file permissions on `.env`
4. **Invalid Values**: Use `ai-dev-local config set` to fix

## Security Best Practices

1. **Never commit `.env` to version control**
2. **Use strong, unique secrets for all keys**
3. **Regularly rotate API keys**
4. **Limit API key permissions where possible**
5. **Use environment-specific configurations**

## Configuration Templates

### Minimal Setup (OpenAI only)
```bash
OPENAI_API_KEY=your-openai-key
WEBUI_SECRET_KEY=your-secret-key
LITellm_MASTER_KEY=your-master-key
```

### Full Setup (All Providers)
```bash
OPENAI_API_KEY=your-openai-key
ANTHROPIC_API_KEY=your-anthropic-key
GEMINI_API_KEY=your-gemini-key
COHERE_API_KEY=your-cohere-key
WEBUI_SECRET_KEY=your-secret-key
LITELLM_MASTER_KEY=your-master-key
LANGFUSE_PUBLIC_KEY=your-langfuse-public-key
LANGFUSE_SECRET_KEY=your-langfuse-secret-key
```

### Local-Only Setup (with Ollama)
```bash
WEBUI_SECRET_KEY=your-secret-key
LITELLM_MASTER_KEY=your-master-key
OLLAMA_AUTO_PULL_MODELS=llama2:7b,codellama:7b
OLLAMA_GPU=true  # if you have NVIDIA GPU
```

For more help, run `ai-dev-local --help` or check the main documentation.
