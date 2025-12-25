# Configuring Flowise to Use LiteLLM

This guide explains how to configure Flowise to consume LiteLLM's OpenAI-compatible API, giving you unified access to multiple LLM providers (OpenAI, Anthropic, Google, Ollama, etc.) through a single interface.

## Overview

Flowise integrates with LiteLLM using **node-level configuration** in the Flowise UI. This is the recommended approach from [Flowise's official documentation](https://docs.flowiseai.com/integrations/litellm).

### Configuration Methods (Priority Order)

1. **Node-level configuration** (Highest Priority) - Set BasePath directly in OpenAI nodes
2. **Credential configuration** - Create credentials in Flowise UI with custom settings
3. **Environment variables** (Lowest Priority) - Fallback for nodes that don't specify BasePath

### Environment Configuration (Fallback Only)

Your Flowise container has these environment variables as a fallback:

```bash
OPENAI_API_KEY=D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB  # LiteLLM master key
OPENAI_API_BASE=http://litellm:4000/v1                   # LiteLLM proxy endpoint
```

**Important**: Node-level configuration in chatflows will override these environment variables. For best results, explicitly configure each OpenAI node to use LiteLLM.

## Creating Credentials in Flowise UI

When building chatflows, you need to create OpenAI credentials in the Flowise UI:

### Step 1: Access Flowise

Navigate to: http://localhost:3001

Login credentials:
- **Username**: `admin`
- **Password**: `admin123`

### Step 2: Create OpenAI Credential

1. Click on **"Credentials"** in the left sidebar
2. Click **"+ Add New Credential"**
3. Select **"OpenAI API"** from the list
4. Fill in the credential details:

   ```
   Credential Name: LiteLLM Proxy
   API Key: D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB
   ```

5. Click **"Add"** to save

**Note**: Do not add the `sk-` prefix. Use the LiteLLM master key exactly as shown.

### Step 3: Configure OpenAI Nodes in Chatflows

When creating a chatflow with OpenAI components, follow the official Flowise approach:

1. **Add Node** → **Chat Models** → Select **"ChatOpenAI"** (use standard OpenAI nodes, NOT Azure OpenAI)

2. **Configure the node**:
   - **Model Name**: Enter one of the available models:
     - `gpt-4` - GPT-4 via OpenAI
     - `gpt-3.5-turbo` - GPT-3.5 Turbo via OpenAI
     - `claude-3-opus` - Claude 3 Opus via Anthropic
     - `claude-3-sonnet` - Claude 3 Sonnet via Anthropic
     - `claude-3-haiku` - Claude 3 Haiku via Anthropic
     - `llama3:8b` - LLaMA 3 8B via local Ollama
     - `codegemma` - CodeGemma via local Ollama
   - **Connect Credential**: Select "LiteLLM Proxy" (the credential you created)
   - **BasePath** (Optional but Recommended): `http://litellm:4000`
   - **Headers** (if BasePath is set): Add custom header
     - Key: `Authorization`
     - Value: `Bearer D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB`

3. **For Embeddings**: Use **"OpenAI Embeddings"** node with same configuration:
   - Model: `text-embedding-3-small` or `text-embedding-3-large`
   - Credential: "LiteLLM Proxy"
   - BasePath: `http://litellm:4000` (if setting explicitly)

### Step 4: Test Your Chatflow

1. Configure your chatflow with the desired model
2. Click **"Save Chatflow"**
3. Use the chat interface to test
4. All requests will route through LiteLLM automatically

## Available Models

Through LiteLLM, you have access to:

### OpenAI Models
- `gpt-4` - Most capable GPT-4
- `gpt-4-turbo` - Faster GPT-4 variant
- `gpt-3.5-turbo` - Fast and cost-effective

### Anthropic Models (via LiteLLM)
- `claude-3-opus` - Most capable Claude
- `claude-3-sonnet` - Balanced performance
- `claude-3-haiku` - Fastest Claude

### Google Models (via LiteLLM)
- `gemini-pro` - Google's Gemini Pro

### Ollama Models (Local)
- `llama3:8b` - Meta LLaMA 3 8B
- `codegemma` - Google CodeGemma 2B
- `nomic-embed-text` - Embeddings model

### Embeddings
- `text-embedding-ada-002` - OpenAI embeddings
- `text-embedding-3-small` - OpenAI small embeddings
- `text-embedding-3-large` - OpenAI large embeddings
- `nomic-embed-text` - Local embeddings via Ollama

## Advanced Configuration

### Using Different Models in Same Workflow

You can mix and match models in a single chatflow:
1. Create multiple chat model nodes
2. Each can use a different model (e.g., `gpt-4` for reasoning, `llama3:8b` for generation)
3. All use the same LiteLLM credential

### Method 1: Node-Level Configuration (Recommended)

Configure BasePath directly in each OpenAI node for explicit control:

1. In the node configuration panel, look for **"BasePath"** or **"Base URL"** field
2. Set it to: `http://litellm:4000`
3. Add Authorization header:
   - Click **"Add Additional Parameters"** or **"Headers"**
   - Key: `Authorization`
   - Value: `Bearer D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB`

### Method 2: Environment Variables (Automatic)

If you don't set BasePath in the node, Flowise will use the environment variable:
- `OPENAI_API_BASE=http://litellm:4000/v1`

This works for most nodes but may not cover all cases. Node-level configuration is more reliable.

### Testing Connectivity

To verify LiteLLM is accessible from Flowise:

```bash
# From your host machine
docker compose exec flowise curl -s http://litellm:4000/health

# Should return: {"status":"healthy"}
```

## Troubleshooting

### "Authentication Error" or "Invalid API Key"

**Problem**: Flowise can't authenticate with LiteLLM

**Solution**:
1. Verify the credential in Flowise uses: `D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB`
2. Do NOT add `sk-` prefix to the key
3. Check environment variables:
   ```bash
   docker compose exec flowise env | grep OPENAI_API
   ```

### "Model Not Found" Error

**Problem**: The model you selected isn't available in LiteLLM

**Solution**:
1. Check available models:
   ```bash
   curl -H "Authorization: Bearer D3NCfoEhE07v0ka5GRvw1MGNXIxewrxBb1GZzjsB" \
        http://localhost:4000/v1/models
   ```
2. For Ollama models, ensure they're pulled:
   ```bash
   ollama list
   ```
3. Update `configs/litellm_config.yaml` if needed

### "Connection Refused" Error

**Problem**: Flowise can't reach LiteLLM

**Solution**:
1. Verify LiteLLM is running:
   ```bash
   docker compose ps litellm
   ```
2. Check Docker network:
   ```bash
   docker network inspect ai-dev-local
   ```
3. Restart both services:
   ```bash
   docker compose restart litellm flowise
   ```

## Configuration Files Reference

### LiteLLM Config
Location: `configs/litellm_config.yaml`

Add new models here and restart LiteLLM:
```bash
docker compose restart litellm
```

### Flowise Config
Location: `configs/flowise/flowise.json`

Contains default credential templates (for reference only).

## API Usage Example

If using Flowise's API directly with LiteLLM models:

```bash
curl -X POST http://localhost:3001/api/v1/prediction/{chatflowId} \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Hello, how are you?",
    "overrideConfig": {
      "modelName": "llama3:8b"
    }
  }'
```

## Best Practices

1. **Use descriptive credential names** - e.g., "LiteLLM - GPT-4", "LiteLLM - Claude"
2. **Test with cheaper models first** - Use `gpt-3.5-turbo` or `llama3:8b` for testing
3. **Monitor costs** - LiteLLM tracks usage in its database
4. **Use local models when possible** - Ollama models are free and private
5. **Keep credentials secure** - Don't commit API keys to git

## Integration with Langfuse

All LLM calls through LiteLLM are automatically logged to Langfuse for observability:

- View at: http://localhost:3000
- Login: First user to sign up becomes admin
- See model usage, costs, and traces

## Summary

✅ Flowise is pre-configured to use LiteLLM
✅ Create "OpenAI API" credential with LiteLLM master key
✅ Select any model from the unified model list
✅ All API calls route through LiteLLM automatically
✅ Access to 15+ models from multiple providers
✅ Full observability via Langfuse integration

For more details, see:
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Flowise Documentation](https://docs.flowiseai.com/)
- [AI Dev Local README](../README.md)
