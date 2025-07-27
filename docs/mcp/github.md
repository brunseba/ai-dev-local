# GitHub MCP Server

The GitHub MCP Server provides integration with GitHub for repository management, issue tracking, pull request management, and more.

## Features

- **Repository Operations**: Create, list, fork, and manage repositories on GitHub.
- **Issue Management**: Create, list, and manage GitHub issues with ease.
- **Pull Requests**: Open, list, and manage pull requests across repositories.
- **Code Security**: Integrate with GitHub's code scanning and security features.

## HTTP Wrapper

To enable HTTP transport compatibility, the GitHub MCP server uses a Node.js based HTTP wrapper that bridges HTTP requests to the server's stdio communication model. This allows seamless integration with other MCP servers and clients using standard web technologies.

### Key Advantages:
- **HTTP Compatibility**: Provides a RESTful API, making it easier to integrate with web-based applications and services.
- **Toolset Expansion**: Access to 70+ GitHub tools and resources via HTTP endpoints.

### Wrapper Details:
- Built using Express.js for lightweight and performant communication.
- Provides endpoints for core GitHub operations, including repository, issue, and pull request management.
- Supports dynamic tool execution and real-time response streaming.
- Includes comprehensive logging and error handling.

## Configuration

Ensure you have configured the following environment variables:

- `GITHUB_PERSONAL_ACCESS_TOKEN`: Your personal access token for authenticating with GitHub's API.
- `GITHUB_TOOLSETS`: A comma-separated list of toolsets to enable (e.g., `repos,issues,pull_requests`).
- `GITHUB_READ_ONLY`: Option to set the server in read-only mode (default: `false`).

## Usage Examples

### Listing Repositories

```bash
mcp-call list_repositories
```

### Creating an Issue

```bash
mcp-call create_issue --title "Bug Report" --body "Description" --repo "owner/repo"
```

### Managing Pull Requests

```bash
mcp-call create_pull_request --base "main" --head "feature" --title "New Feature"
```

## Security Considerations

- **Token Security**: Keep your GitHub personal access token confidential.
- **Minimal Permissions**: Use permissions scopes closely matching your requirements.

## Further Reading

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [Creating a personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---
