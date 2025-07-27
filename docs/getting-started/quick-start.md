# Quick Start Tutorial

Welcome to the Quick Start Tutorial for AI Dev Local, your local development environment for powerful AI integrations.

## Objective

In this tutorial, you'll:

- **Install** AI Dev Local
- **Configure** your environment
- **Launch** services to get started fast

## Step 1: Installation

### Prerequisites

1. Python 3.10+
2. Docker
3. pipx (for package installation)

### Install AI Dev Local

```bash
# Install with pipx
pipx install ai-dev-local

# Verify installation
ai-dev-local --version
```

## Step 2: Configuration

### Initialize Configuration

Initialize the default settings:

```bash
ai-dev-local config init
```

### Set API Keys

For OpenAI models:

```bash
ai-dev-local config set OPENAI_API_KEY your-openai-api-key
```

(Optional) For other LLM providers:

```bash
ai-dev-local config set ANTHROPIC_API_KEY your-anthropic-api-key
```

Validate the setup:

```bash
ai-dev-local config validate
```

## Step 3: Launch Services

### Start the Environment

Launch the services:

```bash
ai-dev-local start
```

### Verify Running Services

Check that services are running smoothly:

```bash
ai-dev-local status
```

Navigate to the Dashboard:

```text
Open in browser: http://localhost:3002/
```

## Step 4: Explore Features

### Dashboard

Use the Dashboard to monitor and control your services.

- URL: [Dashboard](http://localhost:3002/)

### Open WebUI

Chat with AI models via Open WebUI.

- Open WebUI: [Chat Interface](http://localhost:8081/)

### FlowiseAI

Build AI workflows visually with FlowiseAI.

- FlowiseAI: [Visual Builder](http://localhost:3001/)

### Langfuse

Track and debug LLM interactions using Langfuse.

- Langfuse: [Observability](http://localhost:3000/)

### LiteLLM

Access the unified API proxy for LLMs.

- LiteLLM: [API Proxy](http://localhost:4000/)

## Useful Commands

- **Stop Services**: `ai-dev-local stop`
- **View Logs**: `ai-dev-local logs`
- **Update Configuration**: `ai-dev-local config set <KEY> <VALUE>`

## Next Steps

Once you're familiar with the basics, check out:

- **[Configuration Guide](../CONFIGURATION.md)** for advanced settings.
- **[IDE MCP Setup](../IDE_MCP_SETUP.md)** to integrate with your development environment.
