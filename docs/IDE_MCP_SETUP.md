# IDE-Side MCP Setup Guide

This guide explains how to use MCP servers directly within your IDE (VS Code, Codium, Cursor, etc.) rather than running them as containerized services.

## Overview

Instead of running MCP servers in Docker containers as part of your development stack, you can configure your IDE to run MCP servers on-demand. This approach provides:

- **Direct IDE integration** with GitHub, GitLab, and SonarQube
- **Per-project configuration** flexibility
- **Resource efficiency** (servers only run when needed)
- **Easier debugging** and development workflow

## MCP Servers from inputs/README.md

Based on your `inputs/README.md`, we'll set up these MCP servers:

1. **GitHub MCP Server** - Official GitHub integration
2. **GitLab MCP Server** - GitLab repository management  
3. **SonarQube MCP Server** - Code quality analysis

## Prerequisites

### 1. IDE Requirements
- **VS Code**: Version 1.101+ (for MCP support)
- **Codium**: Latest version with MCP extension support
- **Cursor**: Latest version with MCP support
- **Windsurf**: Latest version

### 2. Docker
All MCP servers run in Docker containers, so you need:
- Docker Desktop installed and running
- Access to pull public Docker images

### 3. Access Tokens

#### GitHub Personal Access Token
1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/personal-access-tokens/new)
2. Create a fine-grained personal access token with these permissions:
   - **Repository permissions**: Read access to code, issues, pull requests, actions
   - **Account permissions**: Read access to user profile
3. Save the token securely

#### GitLab Personal Access Token (Optional)
1. Go to [GitLab Settings > Access Tokens](https://gitlab.com/-/profile/personal_access_tokens)
2. Create a token with these scopes:
   - `read_api`, `read_repository`, `read_user`
3. Save the token securely

#### SonarQube Token (Optional)
1. In your SonarQube instance, go to **User > My Account > Security**
2. Generate a new token with appropriate permissions
3. Save the token securely

## Setup Instructions

### Method 1: Workspace-Specific Configuration (Recommended)

This method configures MCP servers for a specific project/workspace.

1. **Copy the workspace MCP configuration**:
   ```bash
   # The .vscode/mcp.json file is already created in your project
   # You can customize it for your specific needs
   ```

2. **Open your project in VS Code/Codium**

3. **Enable GitHub Copilot Agent Mode** (if using VS Code with Copilot):
   - Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
   - Type "Copilot: Toggle Agent Mode"
   - Enable Agent Mode

4. **The IDE will prompt for tokens** when first using MCP features

### Method 2: Global User Configuration

This method configures MCP servers globally for all projects.

#### For VS Code:
1. **Open VS Code Settings** (`Ctrl+,` / `Cmd+,`)
2. **Open Settings JSON** (click the `{}` icon in the top right)
3. **Add the MCP configuration** from `configs/ide-mcp/vscode-mcp.json`
4. **Save and restart VS Code**

#### For Codium:
1. **Open Codium Settings** (`Ctrl+,` / `Cmd+,`)
2. **Open Settings JSON**
3. **Add the same MCP configuration** (Codium follows VS Code's format)
4. **Save and restart Codium**

### Method 3: Using GitHub Copilot in Other IDEs

For **JetBrains IDEs**, **Visual Studio**, **Eclipse**, etc. with GitHub Copilot:

1. **Add MCP configuration** to your IDE's Copilot settings
2. **Use the format** from `configs/ide-mcp/vscode-mcp.json` (adapt syntax as needed)
3. **Restart your IDE**

## Usage Examples

### GitHub MCP Server Capabilities

Once configured, you can ask your AI assistant to:

```
# Repository Management
"Show me the recent commits in this repository"
"Create a new issue for the bug we just found"
"List all open pull requests"

# Code Analysis
"Analyze the security findings in this repo"
"Show me all Dependabot alerts"
"Check the status of GitHub Actions workflows"

# Project Management
"Create a pull request for my current branch"
"Add a comment to issue #123"
"Merge pull request #456"
```

### GitLab MCP Server Capabilities

```
# Repository Operations
"Show me merge requests for this project"
"Create a new issue in GitLab"
"Check pipeline status"

# Project Management
"List project milestones"
"Show recent activity"
"Create a merge request"
```

### SonarQube MCP Server Capabilities

```
# Code Quality
"Show code quality metrics for this project"
"List all security vulnerabilities"
"Analyze code coverage reports"

# Issue Management
"Show critical issues in the codebase"
"Generate a quality gate report"
"List technical debt items"
```

## Configuration Options

### GitHub Server Options

You can customize the GitHub MCP server by modifying the environment variables:

```json
{
  "env": {
    "GITHUB_PERSONAL_ACCESS_TOKEN": "${input:github_token}",
    "GITHUB_TOOLSETS": "repos,issues,pull_requests,actions,code_security,context",
    "GITHUB_READ_ONLY": "false",
    "GITHUB_HOST": "https://github.com"  // For GitHub Enterprise
  }
}
```

Available toolsets:
- `context` - User context and GitHub info (recommended)
- `repos` - Repository operations  
- `issues` - Issue management
- `pull_requests` - PR management
- `actions` - GitHub Actions/CI-CD
- `code_security` - Security scanning
- `discussions` - GitHub Discussions
- `notifications` - Notification management
- `orgs` - Organization management
- `users` - User operations

### GitLab Server Options

```json
{
  "env": {
    "GITLAB_TOKEN": "${input:gitlab_token}",
    "GITLAB_URL": "https://gitlab.com",  // Change for self-hosted
    "GITLAB_API_VERSION": "v4"
  }
}
```

### SonarQube Server Options

```json
{
  "env": {
    "SONARQUBE_TOKEN": "${input:sonarqube_token}", 
    "SONARQUBE_URL": "http://localhost:9000",  // Your SonarQube instance
    "SONARQUBE_ORGANIZATION": "your-org"       // For SonarCloud
  }
}
```

## Troubleshooting

### Common Issues

1. **"Docker image not found"**
   - Ensure Docker is running
   - Pull images manually: `docker pull ghcr.io/github/github-mcp-server`

2. **"Authentication failed"**
   - Verify your access tokens are correct and not expired
   - Check token permissions match requirements

3. **"MCP server not responding"**
   - Check Docker logs: `docker logs <container-id>`
   - Verify network connectivity to GitHub/GitLab/SonarQube

4. **"VS Code not recognizing MCP configuration"**
   - Ensure VS Code version is 1.101+
   - Restart VS Code after configuration changes
   - Check the JSON syntax is valid

### Debug Mode

Enable debug logging by adding to your MCP server configuration:

```json
{
  "env": {
    "DEBUG": "true",
    "LOG_LEVEL": "debug"
  }
}
```

### Testing MCP Connection

You can test MCP servers directly:

```bash
# Test GitHub MCP server
docker run -it --rm -e GITHUB_PERSONAL_ACCESS_TOKEN=your_token ghcr.io/github/github-mcp-server

# Test GitLab MCP server  
docker run -it --rm -e GITLAB_TOKEN=your_token zereight/gitlab-mcp

# Test SonarQube MCP server
docker run -it --rm -e SONARQUBE_TOKEN=your_token sonarsource/sonarqube-mcp-server
```

## Security Considerations

1. **Token Storage**: IDE configurations store tokens securely, but avoid committing them to version control
2. **Workspace Isolation**: Use workspace-specific configurations for sensitive projects
3. **Read-Only Mode**: Enable read-only mode for GitHub server in production environments
4. **Network Access**: MCP servers run in containers with network access to external services

## Alternative: Remote MCP Servers

For GitHub, you can also use the hosted remote MCP server:

```json
{
  "servers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

This doesn't require running Docker containers locally but requires GitHub Copilot subscription.

## Next Steps

1. **Choose your setup method** (workspace-specific recommended)
2. **Configure your IDE** with the appropriate MCP settings
3. **Obtain required access tokens** for the services you want to use
4. **Test the integration** by asking your AI assistant to interact with GitHub/GitLab/SonarQube
5. **Explore advanced features** like automated issue creation, PR management, and code quality analysis

The IDE-side MCP integration provides powerful capabilities for AI-assisted development workflows while keeping the setup flexible and resource-efficient.
