# LiteLLM Proxy Service

LiteLLM Proxy serves as a unified API gateway that provides a standardized OpenAI-compatible interface for 100+ large language model providers. It enables seamless switching between different LLM providers while maintaining consistent API contracts and adding enterprise features like load balancing, rate limiting, and cost tracking.

## Architecture Overview

```mermaid
graph TB
    A[Client Applications] -->|OpenAI Format| B[LiteLLM Proxy]
    B -->|Route & Transform| C[Request Router]
    C -->|Load Balance| D[Provider Pool]
    D --> E[OpenAI GPT-4]
    D --> F[Anthropic Claude]
    D --> G[Google Gemini]
    D --> H[Cohere Command]
    D --> I[Local Ollama]
    B -->|Log & Monitor| J[Analytics DB]
    B -->|Cache Responses| K[Redis Cache]
    B -->|Rate Limit| L[Rate Limiter]
```

## Key Features

### Unified API Interface
- **OpenAI-compatible endpoints** for all supported providers
- **Consistent request/response format** across different models
- **Automatic parameter translation** between provider schemas
- **Streaming support** for real-time responses

### Enterprise-Grade Functionality
- **Load balancing** across multiple model instances
- **Intelligent failover** when providers are unavailable
- **Rate limiting** per user, API key, or model
- **Cost tracking** and budget enforcement
- **Request/response caching** for improved performance

### Multi-Provider Support
- **100+ LLM providers** supported out of the box
- **Custom endpoint configuration** for proprietary models
- **Model routing strategies** (cost-based, performance-based)
- **Provider-specific optimizations** and retry logic

### Observability & Analytics
- **Real-time usage dashboards** with Langfuse integration
- **Detailed cost breakdowns** per model and user
- **Performance metrics** (latency, throughput, error rates)
- **Audit logs** for compliance and debugging

## Configuration Schema

### Environment Variables
```bash
# Core Settings
LITELLM_MASTER_KEY=sk-your-master-key-here
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/litellm

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# UI Authentication
UI_USERNAME=admin
UI_PASSWORD=admin123

# Provider API Keys
OPENAI_API_KEY=sk-proj-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GEMINI_API_KEY=your-gemini-key
COHERE_API_KEY=your-cohere-key

# Langfuse Integration
LANGFUSE_PUBLIC_KEY=pk-your-langfuse-public-key
LANGFUSE_SECRET_KEY=sk-your-langfuse-secret-key
LANGFUSE_HOST=http://langfuse:3000

# Logging
LITELLM_LOG=INFO
LITELLM_DEBUG=false
```

### Model Configuration (litellm_config.yaml)
```yaml
model_list:
  # OpenAI Models
  - model_name: gpt-4
    litellm_params:
      model: openai/gpt-4
      api_key: os.environ/OPENAI_API_KEY
      max_tokens: 4096
      temperature: 0.7
  
  - model_name: gpt-3.5-turbo
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
      max_tokens: 2048
  
  # Anthropic Models
  - model_name: claude-3-sonnet
    litellm_params:
      model: anthropic/claude-3-sonnet-20240229
      api_key: os.environ/ANTHROPIC_API_KEY
      max_tokens: 2048
  
  # Google Models
  - model_name: gemini-pro
    litellm_params:
      model: gemini/gemini-pro
      api_key: os.environ/GEMINI_API_KEY
  
  # Local Ollama Models
  - model_name: llama2
    litellm_params:
      model: ollama/llama2
      api_base: http://host.docker.internal:11434

# Router Configuration
router_settings:
  routing_strategy: usage-based-routing
  model_group_alias:
    gpt-4-group: ["gpt-4", "gpt-4-turbo"]
    claude-group: ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
  fallbacks:
    - gpt-4: ["gpt-3.5-turbo"]
    - claude-3-opus: ["claude-3-sonnet", "gpt-4"]

# General Settings
general_settings:
  master_key: os.environ/LITELLM_MASTER_KEY
  database_url: os.environ/DATABASE_URL
  
  # Cost & Budget Controls
  track_cost_per_model: true
  max_budget: 100.0
  budget_duration: 30d
  
  # Caching
  cache: true
  cache_params:
    type: redis
    host: os.environ/REDIS_HOST
    port: os.environ/REDIS_PORT
    ttl: 600
  
  # Rate Limiting
  tpm_limit: 10000  # tokens per minute
  rpm_limit: 100    # requests per minute
  
  # Callbacks for Observability
  success_callback: ["langfuse"]
  failure_callback: ["langfuse"]
  
  # Security
  allowed_ips: ["*"]
  blocked_ips: []
```

### API Request Schema
```json
{
  "model": "gpt-4",
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Hello, how are you?"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1000,
  "stream": false
}
```

### API Response Schema
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! I'm doing well, thank you for asking."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 20,
    "completion_tokens": 12,
    "total_tokens": 32
  }
}
```

## Default Credentials

- **UI Username:** admin
- **UI Password:** admin123
- **Master Key:** Required for API access

!!! warning "Security"
    Change default credentials and set a strong master key in production.

## Access

LiteLLM Proxy is accessible at:

```
http://localhost:4000/
```

### Key Endpoints

- **Chat Completions:** `POST /v1/chat/completions`
- **Completions:** `POST /v1/completions`
- **Models List:** `GET /v1/models`
- **Health Check:** `GET /health`
- **UI Dashboard:** `GET /ui` (admin interface)
- **Metrics:** `GET /metrics` (Prometheus format)

## Supported Providers

### Major Cloud Providers
- **OpenAI:** GPT-3.5, GPT-4, GPT-4 Vision, DALL-E
- **Anthropic:** Claude 3 (Haiku, Sonnet, Opus)
- **Google:** Gemini Pro, Gemini Pro Vision, PaLM
- **Cohere:** Command, Command-Light, Embed
- **Azure OpenAI:** All OpenAI models via Azure
- **AWS Bedrock:** Titan, Claude, Llama models

### Open Source & Local
- **Ollama:** Local model serving
- **Hugging Face:** Transformers models
- **vLLM:** High-performance inference
- **Together AI:** Open source models
- **Replicate:** Community-hosted models

### Specialized Providers
- **Stability AI:** Stable Diffusion models
- **Mistral AI:** Mistral 7B, Mixtral 8x7B
- **AI21:** Jurassic models
- **Aleph Alpha:** Luminous models

## Advanced Features

### Load Balancing Strategies
```yaml
router_settings:
  routing_strategy: "usage-based-routing"  # or "simple-shuffle", "least-busy", "latency-based"
  cooldown_time: 1  # seconds between retries
  retry_policy:
    max_retries: 3
    base_delay: 1
    max_delay: 10
```

### Cost Controls
```yaml
general_settings:
  max_budget: 100.0
  budget_duration: "30d"
  budget_reset_at: "00:00"
  cost_per_token:
    gpt-4: 0.00006  # per token
    gpt-3.5-turbo: 0.000002
```

### Rate Limiting
```yaml
general_settings:
  tpm_limit: 10000  # tokens per minute
  rpm_limit: 100    # requests per minute
  max_parallel_requests: 10
  user_rate_limit:
    "user-1": {"tpm": 5000, "rpm": 50}
```

## Monitoring & Observability

### Health Check Response
```json
{
  "status": "healthy",
  "healthy_endpoints": [
    {
      "model": "gpt-4",
      "status": "healthy",
      "latency_ms": 245
    }
  ],
  "unhealthy_endpoints": [],
  "version": "1.0.0",
  "uptime": "2h 15m 30s"
}
```

### Usage Analytics
- **Request volume** per model and time period
- **Cost analysis** with breakdown by user/model
- **Performance metrics** (P95, P99 latency)
- **Error rate tracking** with categorization
- **Token usage patterns** and optimization insights

## Troubleshooting

### Common Issues

1. **"Invalid HTTP request received" warnings**
   - Usually caused by invalid API keys or authentication issues
   - See [LiteLLM Troubleshooting](../CONFIGURATION.md#litellm-troubleshooting) guide

2. **Model unavailable errors**
   - Check provider API key configuration
   - Verify model name spelling and availability
   - Review rate limiting settings

3. **High latency issues**
   - Enable response caching
   - Implement load balancing
   - Check provider geographic regions

### Debug Commands
```bash
# Check health status
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://localhost:4000/health

# List available models
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://localhost:4000/v1/models

# View metrics
curl http://localhost:4000/metrics
```

## Online Resources

- **GitHub Repository:** [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- **Official Website:** [LiteLLM.ai](https://litellm.ai)
- **Documentation:** [LiteLLM Docs](https://docs.litellm.ai)
- **API Reference:** [API Docs](https://docs.litellm.ai/docs/proxy/api_reference)
- **Community:** [Discord Server](https://discord.gg/wuPM9dRgDw)
- **Docker Hub:** [LiteLLM Images](https://hub.docker.com/r/berriaiofficial/litellm)

## Use Cases

- **Multi-Provider Abstraction:** Single API for multiple LLM providers
- **Cost Optimization:** Automatic routing to cost-effective models
- **High Availability:** Failover between providers for reliability
- **Development & Testing:** Easy model comparison and A/B testing
- **Enterprise Deployment:** Centralized LLM access with governance
- **Microservices Architecture:** Unified LLM gateway for distributed systems

## Performance Optimizations

- **Response Caching:** Redis-based caching for repeated queries
- **Connection Pooling:** Efficient HTTP connection management
- **Batch Processing:** Support for batch API requests
- **Streaming Responses:** Real-time response streaming
- **Geographic Routing:** Route to nearest provider endpoints

LiteLLM Proxy is essential for organizations requiring a robust, scalable, and cost-effective solution for managing multiple LLM providers through a single, standardized interface.
