# MCP Deployment and Management Guide

This guide provides comprehensive information about deploying, managing, and integrating Model Context Protocol (MCP) servers in the AI Dev Local environment.

## Overview

The MCP ecosystem in AI Dev Local consists of multiple specialized servers that provide different capabilities to AI agents and applications. Each server runs in its own containerized environment with proper isolation and networking.

## Architecture

### MCP Network Topology

```mermaid
graph TB
    subgraph "Client Applications"
        Claude[🤖 Claude Desktop]
        VSCode[📝 VS Code/Codium]
        FlowiseAI[🌊 FlowiseAI]
        OpenWebUI[🌐 Open WebUI]
        LiteLLM[⚡ LiteLLM Proxy]
    end
    
    subgraph "MCP Gateway Layer"
        Gateway[🚪 MCP Gateway<br/>Port 9000]
    end
    
    subgraph "Core Development Servers"
        Git[📂 Git Server<br/>Port 9001]
        FS[📁 Filesystem<br/>Port 9002]
        Fetch[🌐 Fetch Server<br/>Port 9003]
    end
    
    subgraph "Data & Storage Servers"
        Memory[🧠 Memory Server<br/>Port 9004]
        Time[⏰ Time Server<br/>Port 9005]
        PostgreSQL[🐘 PostgreSQL<br/>Port 9006]
    end
    
    subgraph "Platform Integration Servers"
        Everything[🛠️ Everything<br/>Port 9007]
        GitHub[🐙 GitHub<br/>Port 9008]
        GitLab[🦊 GitLab<br/>Port 9009]
        SonarQube[🔍 SonarQube<br/>Port 9010]
    end
    
    subgraph "External Services"
        GitHubAPI[GitHub.com API]
        GitLabAPI[GitLab.com API]
        SonarQubeAPI[SonarQube Instance]
        Database[(PostgreSQL DB)]
    end
    
    Claude -.-> Gateway
    VSCode -.-> Gateway
    FlowiseAI --> Gateway
    OpenWebUI --> Gateway
    LiteLLM --> Gateway
    
    Gateway --> Git
    Gateway --> FS
    Gateway --> Fetch
    Gateway --> Memory
    Gateway --> Time
    Gateway --> PostgreSQL
    Gateway --> Everything
    Gateway --> GitHub
    Gateway --> GitLab
    Gateway --> SonarQube
    
    GitHub <--> GitHubAPI
    GitLab <--> GitLabAPI
    SonarQube <--> SonarQubeAPI
    PostgreSQL <--> Database
```

### Transport Protocols

MCP servers support multiple transport protocols:

1. **HTTP/REST**: Standard web API for most servers
2. **Server-Sent Events (SSE)**: Real-time streaming for compatible servers
3. **stdio**: Direct process communication (bridged to HTTP via wrappers)

## Deployment Commands

### Start All MCP Services

```bash
# Start the complete MCP stack
ai-dev-local mcp start

# Start specific services
docker-compose -f docker-compose.mcp.yml up -d mcp-github mcp-gitlab
```

### Check Service Status

```bash
# View all MCP service status
ai-dev-local mcp status

# Check specific service logs
docker-compose -f docker-compose.mcp.yml logs -f mcp-github
```

### Stop Services

```bash
# Stop all MCP services
ai-dev-local mcp stop

# Stop specific service
docker-compose -f docker-compose.mcp.yml stop mcp-github
```

## Individual Server Configurations

### GitHub MCP Server

**Image**: Custom HTTP wrapper + `ghcr.io/github/github-mcp-server:latest`  
**Port**: 9008  
**Transport**: HTTP (via stdio bridge)

```yaml
environment:
  - GITHUB_PERSONAL_ACCESS_TOKEN=${GITHUB_PERSONAL_ACCESS_TOKEN}
  - GITHUB_TOOLSETS=repos,issues,pull_requests,actions,code_security,context
  - GITHUB_READ_ONLY=false
```

**Key Features**:
- 70+ GitHub tools for comprehensive repository management
- HTTP wrapper enables seamless integration with other services
- Support for GitHub Actions, code security, and Copilot integration

### GitLab MCP Server

**Image**: Built from `https://github.com/zereight/gitlab-mcp.git`  
**Port**: 9009  
**Transport**: HTTP

```yaml
environment:
  - GITLAB_PERSONAL_ACCESS_TOKEN=${GITLAB_TOKEN}
  - GITLAB_API_URL=https://gitlab.com/api/v4
  - GITLAB_READ_ONLY_MODE=false
```

### PostgreSQL MCP Server

**Image**: `crystaldba/postgres-mcp:latest`  
**Port**: 9006  
**Transport**: SSE

```yaml
command: ["--access-mode=restricted", "--transport=sse"]
environment:
  - DATABASE_URI=postgresql://postgres:postgres@postgres:5432/postgres
```

### Git Server

**Image**: `mcp/git:latest`  
**Port**: 9001  
**Transport**: HTTP

**Volume Mounts**:
- Workspace (read-only): `.:/workspace:ro`
- Git config: `~/.gitconfig:/root/.gitconfig:ro`
- SSH keys: `~/.ssh:/root/.ssh:ro`

### Filesystem Server

**Image**: `mcp/filesystem:latest`  
**Port**: 9002  
**Transport**: HTTP

**Security Configuration**:
```yaml
environment:
  - ALLOWED_DIRECTORIES=/workspace,/tmp/mcp-fs
  - READ_ONLY_DIRECTORIES=/workspace/.git
```

### Memory Server

**Image**: `mcp/memory:latest`  
**Port**: 9004  
**Transport**: HTTP

**Persistent Storage**:
```yaml
volumes:
  - mcp_memory_data:/data
environment:
  - MEMORY_STORE_PATH=/data/memory.db
  - MAX_MEMORY_SIZE=1073741824  # 1GB
```

## Network Configuration

### Docker Networks

- **Primary Network**: `ai-dev-mcp` (bridge)
- **External Network**: `ai-dev-local` (connects to main services)
- **Subnet**: `192.168.100.0/24`

### Port Mapping

| Service | Internal Port | External Port | Protocol |
|---------|---------------|---------------|----------|
| Gateway | 8080 | 9000 | HTTP |
| Git | 8000 | 9001 | HTTP |
| Filesystem | 8000 | 9002 | HTTP |
| Fetch | 8000 | 9003 | HTTP |
| Memory | 8000 | 9004 | HTTP |
| Time | 8000 | 9005 | HTTP |
| PostgreSQL | 8000 | 9006 | SSE |
| Everything | 8000 | 9007 | HTTP |
| GitHub | 8000 | 9008 | HTTP |
| GitLab | 8000 | 9009 | HTTP |
| SonarQube | 8000 | 9010 | HTTP |

## Health Monitoring

### Health Check Endpoints

All HTTP-based servers provide health endpoints:

```bash
# Check individual server health
curl http://localhost:9008/health  # GitHub
curl http://localhost:9009/health  # GitLab
curl http://localhost:9010/health  # SonarQube
```

### Monitoring Commands

```bash
# View real-time logs
docker-compose -f docker-compose.mcp.yml logs -f

# Check resource usage
docker stats $(docker-compose -f docker-compose.mcp.yml ps -q)

# Restart unhealthy services
docker-compose -f docker-compose.mcp.yml restart mcp-github
```

## Troubleshooting

### Common Issues

1. **Service Not Starting**
   ```bash
   # Check logs for errors
   docker-compose -f docker-compose.mcp.yml logs mcp-github
   
   # Rebuild if needed
   docker-compose -f docker-compose.mcp.yml build --no-cache mcp-github
   ```

2. **Authentication Failures**
   ```bash
   # Verify environment variables
   docker-compose -f docker-compose.mcp.yml exec mcp-github env | grep GITHUB
   
   # Test token validity
   curl -H "Authorization: token $GITHUB_PERSONAL_ACCESS_TOKEN" https://api.github.com/user
   ```

3. **Network Connectivity Issues**
   ```bash
   # Check network configuration
   docker network inspect ai-dev-mcp
   
   # Verify inter-service communication
   docker-compose -f docker-compose.mcp.yml exec mcp-github curl http://mcp-gitlab:8000/health
   ```

### Debug Mode

Enable debug logging for specific services:

```yaml
# Add to service environment
environment:
  - DEBUG=mcp*
  - LOG_LEVEL=debug
```

## Security Best Practices

### Token Management

1. **Use Environment Variables**: Never hardcode tokens in configuration files
2. **Minimal Permissions**: Grant only necessary scopes to API tokens
3. **Token Rotation**: Regularly rotate access tokens
4. **Secret Management**: Use Docker secrets for production deployments

### Network Security

1. **Isolated Networks**: MCP servers run on separate network from main services
2. **Access Controls**: Filesystem server has directory-based access restrictions
3. **Health Checks**: Regular health monitoring to detect compromised services

### Container Security

1. **Non-root Users**: Containers run with non-privileged users where possible
2. **Read-only Mounts**: Sensitive directories mounted as read-only
3. **Resource Limits**: Memory and CPU limits prevent resource exhaustion

## Integration Examples

### FlowiseAI Integration

```javascript
// FlowiseAI Custom Tool Node
const mcpCall = async (serverUrl, tool, params) => {
  const response = await fetch(`${serverUrl}/tools/${tool}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ arguments: params })
  });
  return response.json();
};

// Example: Create GitHub issue from FlowiseAI
const result = await mcpCall('http://mcp-github:8000', 'create_issue', {
  owner: 'user',
  repo: 'project',
  title: 'Automated Issue',
  body: 'Created from FlowiseAI workflow'
});
```

### LiteLLM Proxy Integration

```python
# Custom MCP tool integration
import requests

def github_mcp_tool(action, **params):
    """Call GitHub MCP server from LiteLLM"""
    response = requests.post(
        f'http://localhost:9008/tools/{action}',
        json={'arguments': params}
    )
    return response.json()

# Usage in LiteLLM proxy
result = github_mcp_tool('list_repositories', owner='username')
```

## Performance Optimization

### Resource Allocation

- **Memory**: 512MB per server (adjust based on usage)
- **CPU**: 0.5 cores per server for normal workloads
- **Storage**: SSD recommended for Memory server persistence

### Scaling Considerations

- **Horizontal**: Deploy multiple instances behind load balancer
- **Vertical**: Increase container resources for high-traffic servers
- **Caching**: Implement Redis caching for frequently accessed data

This deployment guide ensures proper setup, monitoring, and maintenance of the MCP ecosystem within AI Dev Local.
