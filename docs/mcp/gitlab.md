# GitLab MCP Server

The GitLab MCP Server provides integration with GitLab for managing repositories, issues, merge requests, and CI/CD operations.

## Features

- **Repository Management**: Create, list, and manage GitLab repositories.
- **Issue Tracking**: Create, list, and track issues across projects.
- **Merge Requests**: Manage merge requests across branches and projects.
- **CI/CD**: Access pipeline and job information directly from GitLab.

## Configuration

Ensure you have the following environment variables configured:

- `GITLAB_TOKEN`: Your personal access token for authenticating with the GitLab API.
- `GITLAB_URL`: The base URL for the GitLab instance (default: `https://gitlab.com`).
- `GITLAB_API_VERSION`: API version to use (default: `v4`).

## Usage Examples

### Listing Repositories

```bash
mcp-call list_projects
```

### Creating an Issue

```bash
mcp-call create_issue --title "New Bug Report" --project_id 123 --description "Bug details..."
```

### Handling Merge Requests

```bash
mcp-call create_merge_request --source_branch "feature" --target_branch "main" --title "Feature Addition"
```

## Security Considerations

- **Token Security**: Keep your GitLab token secure and do not share it.
- **Read-Only Mode**: Use read-only tokens or permissions for safer operations if write access is not needed.

## Further Reading

- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [GitLab Personal Access Tokens](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html)

---

