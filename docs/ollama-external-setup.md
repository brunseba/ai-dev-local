# Ollama External Server Support

The `ai-dev-local` CLI supports connecting to Ollama in multiple deployment modes, giving you flexibility to use Ollama however you prefer.

## Connection Modes

### 1. Docker Mode (Default)
Uses the Ollama service running in Docker Compose.

**When to use:**
- Default setup for ai-dev-local
- Self-contained environment
- Easy to start/stop

**Setup:**
```bash
# Start Ollama with other services
ai-dev-local start --ollama

# Verify it's running
docker-compose ps ollama
```

### 2. Native Mode
Uses Ollama installed directly on your system via Homebrew, apt, or binary installation.

**When to use:**
- Already have Ollama installed locally
- Want faster performance without Docker overhead
- Prefer system-level installation

**Setup:**
```bash
# Install via Homebrew (macOS)
brew install ollama

# Start Ollama service
ollama serve

# Configure CLI to use native mode
ai-dev-local ollama config set-mode native
```

### 3. Remote Mode
Connects to an Ollama server running on another machine or network.

**When to use:**
- Share Ollama server across team
- Use remote GPU-enabled machine
- Centralized model management
- Multiple developers using same models

**Setup:**
```bash
# Configure remote server
ai-dev-local ollama config set-mode remote
ai-dev-local ollama config set-url http://ollama-server.local:11434

# Test connection
ai-dev-local ollama config test
```

### 4. Auto Mode
Automatically detects and uses the best available Ollama installation.

**Detection order:**
1. Docker Compose service (if running)
2. Native Ollama (if installed)
3. Remote server (if configured)

**Setup:**
```bash
# Enable auto-detection
ai-dev-local ollama config set-mode auto
```

## Configuration

### View Current Configuration

```bash
ai-dev-local ollama config show
```

**Example output:**
```
🔧 Ollama Connection Configuration:
==================================================
  Mode: docker
  API URL: http://localhost:11434
  Available: ✅ Yes
  Docker Service: ollama
  Compose File: docker-compose.yml

💡 Configuration from .env file:
  OLLAMA_CONNECTION_MODE=auto
  OLLAMA_API_URL=http://localhost:11434
```

### Change Connection Mode

```bash
# Use Docker mode
ai-dev-local ollama config set-mode docker

# Use native mode
ai-dev-local ollama config set-mode native

# Use remote mode
ai-dev-local ollama config set-mode remote

# Use auto-detection
ai-dev-local ollama config set-mode auto
```

### Set Remote Server URL

```bash
# Set remote server address
ai-dev-local ollama config set-url http://192.168.1.100:11434

# Or use hostname
ai-dev-local ollama config set-url http://ollama.example.com:11434
```

### Test All Connection Modes

```bash
ai-dev-local ollama config test
```

**Example output:**
```
🔍 Testing Ollama connection...

Docker Mode:
  ✅ Docker Ollama is running
     5 models available

Native Mode:
  ❌ Native Ollama not available
     💡 Install with: brew install ollama

Remote Mode:
  ✅ Remote Ollama accessible at http://localhost:11434
     5 models available

💡 Use 'ai-dev-local ollama config show' to see current settings
💡 Use 'ai-dev-local ollama config set-mode <mode>' to change mode
```

## Environment Variables

All configuration is stored in the `.env` file:

```bash
# Connection mode: auto, docker, native, remote
OLLAMA_CONNECTION_MODE=auto

# API URL for remote/native modes
OLLAMA_API_URL=http://localhost:11434

# Docker-specific settings
OLLAMA_DOCKER_COMPOSE_FILE=docker-compose.yml
OLLAMA_DOCKER_SERVICE=ollama
```

## Usage Examples

### Example 1: Using Native Ollama

```bash
# Install Ollama locally
brew install ollama

# Start Ollama service
ollama serve &

# Configure CLI
ai-dev-local ollama config set-mode native

# Use normally
ai-dev-local ollama pull llama3:8b
ai-dev-local ollama models
ai-dev-local ollama ps
```

### Example 2: Remote Team Server

**On the server (with GPU):**
```bash
# Install and start Ollama
curl https://ollama.ai/install.sh | sh
ollama serve

# Pull models for the team
ollama pull llama3:8b
ollama pull codellama
ollama pull nomic-embed-text
```

**On developer machines:**
```bash
# Configure to use remote server
ai-dev-local ollama config set-mode remote
ai-dev-local ollama config set-url http://team-ollama:11434

# Verify connection
ai-dev-local ollama config test

# Use remote models
ai-dev-local ollama models
ai-dev-local ollama pull mistral:7b
```

### Example 3: Multiple Environments

```bash
# Development: use Docker
export OLLAMA_CONNECTION_MODE=docker
ai-dev-local start --ollama
ai-dev-local ollama pull phi:2.7b

# Production: use dedicated server
export OLLAMA_CONNECTION_MODE=remote
export OLLAMA_API_URL=http://prod-ollama:11434
ai-dev-local ollama models

# Personal: use native installation
export OLLAMA_CONNECTION_MODE=native
ai-dev-local ollama pull llama3:8b
```

## Command Reference

All ollama commands automatically use the configured connection mode:

| Command | Description | Works with all modes |
|---------|-------------|---------------------|
| `ollama models` | List downloaded models | ✅ |
| `ollama ps` | Show active models | ✅ |
| `ollama pull <model>` | Download model | ✅ |
| `ollama remove <model>` | Delete model | ✅ |
| `ollama init` | Pull default models | ✅ |
| `ollama config show` | Show configuration | ✅ |
| `ollama config test` | Test all modes | ✅ |
| `ollama config set-mode` | Change mode | ✅ |
| `ollama config set-url` | Set remote URL | ✅ |

The current mode is displayed in command output:
```bash
$ ai-dev-local ollama models
📦 Downloaded Ollama models (docker mode):
...

$ ai-dev-local ollama ps
🔍 Active Ollama models (remote mode):
...
```

## Troubleshooting

### Docker Mode Issues

**Problem:** "Docker Ollama not available"

**Solutions:**
```bash
# Check if Docker is running
docker ps

# Start Ollama service
ai-dev-local start --ollama

# Check service status
docker-compose ps ollama

# View logs
docker-compose logs ollama
```

### Native Mode Issues

**Problem:** "Native Ollama not available"

**Solutions:**
```bash
# Check if ollama is installed
which ollama

# Install Ollama
brew install ollama  # macOS
# or download from https://ollama.ai

# Start Ollama service
ollama serve

# Verify it's running
ollama list
```

### Remote Mode Issues

**Problem:** "Remote Ollama not accessible"

**Solutions:**
```bash
# Check network connectivity
ping ollama-server.local

# Test API directly
curl http://ollama-server.local:11434/api/tags

# Verify URL is correct
ai-dev-local ollama config show

# Update URL if needed
ai-dev-local ollama config set-url http://correct-url:11434

# Check firewall rules on server
# Port 11434 must be accessible
```

**Problem:** Connection timeout

**Solutions:**
- Check if Ollama server is running
- Verify network connectivity
- Check firewall settings
- Ensure port 11434 is open

### Auto Mode Issues

**Problem:** Wrong mode detected

**Solutions:**
```bash
# Check what's available
ai-dev-local ollama config test

# Manually set preferred mode
ai-dev-local ollama config set-mode docker
# or
ai-dev-local ollama config set-mode native
```

## Performance Considerations

### Docker Mode
- **Pros:** Easy setup, isolated environment
- **Cons:** Slight overhead from Docker networking
- **Best for:** Development, testing, demo environments

### Native Mode
- **Pros:** Best performance, direct system access
- **Cons:** Requires system installation
- **Best for:** Production use, performance-critical applications

### Remote Mode
- **Pros:** Centralized management, shared resources, can use powerful remote GPU
- **Cons:** Network latency, requires network access
- **Best for:** Team environments, shared infrastructure

## Security Considerations

### Docker Mode
- Models stored in Docker volumes
- Isolated from host system
- Standard Docker security applies

### Native Mode
- Models stored in `~/.ollama/models`
- Direct system access
- Standard filesystem permissions apply

### Remote Mode
- **Important:** Ollama does not have built-in authentication
- Secure your network:
  - Use VPN or private network
  - Implement firewall rules
  - Use SSH tunneling for external access
  - Consider reverse proxy with authentication

**SSH Tunnel Example:**
```bash
# Create SSH tunnel to remote Ollama
ssh -L 11434:localhost:11434 user@ollama-server

# Configure CLI to use localhost (which tunnels to remote)
ai-dev-local ollama config set-mode remote
ai-dev-local ollama config set-url http://localhost:11434
```

## Integration with Other Services

The Ollama connection mode affects how other ai-dev-local services connect:

### Open WebUI
Update `docker-compose.yml` to match your Ollama setup:

```yaml
# For Docker Ollama
OLLAMA_BASE_URL: http://ollama:11434

# For Native Ollama
OLLAMA_BASE_URL: http://host.docker.internal:11434

# For Remote Ollama
OLLAMA_BASE_URL: http://remote-server:11434
```

### LiteLLM
Update `configs/litellm_config.yaml`:

```yaml
# For Docker Ollama
- model_name: llama3
  litellm_params:
    model: ollama/llama3:8b
    api_base: http://ollama:11434

# For Native/Remote Ollama
- model_name: llama3
  litellm_params:
    model: ollama/llama3:8b
    api_base: http://host.docker.internal:11434  # or remote URL
```

### Flowise
Configure in Flowise UI:
- **Ollama Base URL:** Set to match your Ollama location
- Docker: `http://ollama:11434`
- Native/Remote: `http://host.docker.internal:11434` or remote URL

## Best Practices

1. **Use auto mode** for most cases - it automatically picks the best option
2. **Use Docker mode** for development and testing
3. **Use native mode** when you need maximum performance
4. **Use remote mode** for team collaboration
5. **Test configuration** after changes with `ai-dev-local ollama config test`
6. **Keep .env in version control** (with sensitive values redacted) to share team configuration
7. **Document your team's setup** so everyone uses the same mode

## FAQ

**Q: Can I switch modes without restarting services?**  
A: Yes, just change the mode and run commands. No restart needed.

**Q: Do I need to pull models separately for each mode?**  
A: Yes, each Ollama instance (Docker, native, remote) has its own model storage.

**Q: Can I use multiple modes simultaneously?**  
A: No, but you can quickly switch between modes with `ollama config set-mode`.

**Q: How do I share models with my team?**  
A: Set up a remote Ollama server and configure everyone to use it.

**Q: Does the mode affect model performance?**  
A: Docker has minimal overhead. Native mode may be slightly faster. Remote mode depends on network speed.

**Q: Can I use Ollama with GPU in Docker?**  
A: Yes, see [Ollama Docker GPU setup](https://github.com/ollama/ollama/blob/main/docs/docker.md)

**Q: How do I backup my models?**  
A: Models are stored in:
- Docker: Docker volume `ollama_data`
- Native: `~/.ollama/models`
- Remote: On the remote server

## Additional Resources

- [Ollama Official Documentation](https://github.com/ollama/ollama)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [Ollama Model Library](https://ollama.ai/library)
- [ai-dev-local Documentation](../README.md)
