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
5. **LiteLLM Warning Messages**: See [LiteLLM Troubleshooting](#litellm-troubleshooting) below

### LiteLLM Troubleshooting

If you see warning messages like `"Invalid HTTP request received."` in the LiteLLM logs, this is usually caused by API authentication issues during health checks.

#### Symptoms
- Log messages: `{"message": "Invalid HTTP request received.", "level": "WARNING"}`
- LiteLLM reports "unhealthy_endpoints" in health checks
- Models appear unavailable in the UI

#### Common Causes
1. **Placeholder API Keys**: Your `.env` file still contains example values
2. **Invalid API Keys**: API keys are incorrect or expired
3. **Missing API Keys**: Required keys are empty or not set

#### Diagnosis
Check LiteLLM health status:
```bash
# Check if LiteLLM is accessible
curl -H "Authorization: Bearer $(grep LITELLM_MASTER_KEY .env | cut -d'=' -f2)" \
     http://localhost:4000/health
```

This will show which endpoints are healthy/unhealthy and why.

#### Solutions

**1. Update Placeholder API Keys**
Replace example values in your `.env` file:
```bash
# BAD - placeholder values
OPENAI_API_KEY=*********************
ANTHROPIC_API_KEY=your-anthropic-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here

# GOOD - real API keys
OPENAI_API_KEY=sk-proj-abc123...
ANTHROPIC_API_KEY=sk-ant-api03-xyz789...
GEMINI_API_KEY=AIzaSy123...
```

**2. Get Valid API Keys**
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Google Gemini**: https://aistudio.google.com/app/apikey
- **Cohere**: https://dashboard.cohere.ai/api-keys

**3. Update and Restart Services**
```bash
# Update API keys
ai-dev-local config set OPENAI_API_KEY sk-proj-your-real-key
ai-dev-local config set ANTHROPIC_API_KEY sk-ant-your-real-key

# Restart LiteLLM to pick up new keys
docker-compose restart litellm

# Verify health
ai-dev-local status
```

**4. Disable Unused Providers**
If you don't plan to use certain providers, you can comment them out in `configs/litellm_config.yaml`:
```yaml
model_list:
  # OpenAI Models (keep these if you have OPENAI_API_KEY)
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: os.environ/OPENAI_API_KEY
  
  # Comment out unused providers to avoid health check failures
  # - model_name: claude-3-opus
  #   litellm_params:
  #     model: anthropic/claude-3-opus-20240229
  #     api_key: os.environ/ANTHROPIC_API_KEY
```

#### Expected Behavior After Fix
- No more "Invalid HTTP request received" warnings
- Health check shows `"healthy_endpoints"` instead of empty array
- Models become available in Open WebUI and other interfaces
- LiteLLM proxy responds correctly to API requests

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
