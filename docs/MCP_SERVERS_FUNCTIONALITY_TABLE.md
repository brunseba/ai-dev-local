# MCP Servers Functionality Table

This table provides a comprehensive overview of all MCP servers configured in `docker-compose.mcp.yml`, including their functionalities, configurations, and available primitives (tools/resources).

## MCP Servers Overview

| Server Name | Description | Image | Port | Key Environment Variables | Available Primitives |
|-------------|-------------|-------|------|---------------------------|---------------------|
| **Git Server** | Git repository operations | `mcp/git:latest` | 9001:8000 | `GIT_AUTHOR_NAME`, `GIT_AUTHOR_EMAIL`, `GIT_COMMITTER_NAME`, `GIT_COMMITTER_EMAIL` | **Tools:** `git_add`, `git_commit`, `git_push`, `git_pull`, `git_clone`, `git_status`, `git_diff`, `git_log`, `git_branch`, `git_checkout`, `git_merge`, `git_reset`, `git_stash`<br>**Resources:** `repository_info`, `commit_history`, `branch_list`, `file_changes` |
| **Filesystem** | Secure file operations | `mcp/filesystem:latest` | 9002:8000 | `ALLOWED_DIRECTORIES`, `READ_ONLY_DIRECTORIES` | **Tools:** `read_file`, `write_file`, `create_directory`, `list_directory`, `move_file`, `copy_file`, `delete_file`, `get_file_info`, `search_files`<br>**Resources:** `file_tree`, `directory_structure`, `file_metadata` |
| **Fetch Server** | Web content retrieval | `mcp/fetch:latest` | 9003:8000 | `USER_AGENT`, `MAX_RESPONSE_SIZE`, `TIMEOUT` | **Tools:** `fetch`, `fetch_html`, `fetch_text`, `fetch_json`, `fetch_pdf`<br>**Resources:** `web_content`, `html_structure`, `extracted_text`, `page_metadata` |
| **Memory Server** | Persistent knowledge graph | `mcp/memory:latest` | 9004:8000 | `MEMORY_STORE_PATH`, `MAX_MEMORY_SIZE` | **Tools:** `create_entities`, `create_relations`, `add_observations`, `delete_entities`, `delete_relations`, `delete_observations`, `read_graph`, `search_nodes`, `open_nodes`<br>**Resources:** `knowledge_graph`, `entity_relations`, `observation_history` |
| **Time Server** | Time and timezone utilities | `mcp/time:latest` | 9005:8000 | `DEFAULT_TIMEZONE` | **Tools:** `get_current_time`, `convert_timezone`, `format_datetime`, `parse_datetime`, `add_time`, `subtract_time`, `get_timezone_info`<br>**Resources:** `current_time`, `timezone_list`, `time_formats` |
| **PostgreSQL** | Database operations | `postgres:15-alpine` + MCP wrapper | 9006:8000 | `DATABASE_URL`, `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` | **Tools:** `query`, `execute`, `list_tables`, `describe_table`, `create_table`, `drop_table`, `insert`, `update`, `delete`<br>**Resources:** `schema_info`, `table_structure`, `query_results`, `database_stats` |
| **Everything** | Reference/test server | `mcp/everything:latest` | 9007:8000 | `DEMO_MODE` | **Tools:** `echo`, `add`, `longRunningOperation`, `get_prompt`, `sampleLLM`<br>**Resources:** `demo_resource`, `sample_data`, `test_endpoints` |
|| **GitHub** | Official GitHub integration with HTTP wrapper | Custom build (`./docker/mcp-github`) + `ghcr.io/github/github-mcp-server:latest` | 9008:8000 | `GITHUB_PERSONAL_ACCESS_TOKEN`, `GITHUB_TOOLSETS`, `GITHUB_READ_ONLY` | **Tools:** 70+ tools including `create_repository`, `get_repository`, `list_repositories`, `create_issue`, `get_issue`, `list_issues`, `create_pull_request`, `get_pull_request`, `list_pull_requests`, `merge_pull_request`, `create_comment`, `get_file_contents`, `create_or_update_file`, `delete_file`, `search_repositories`, `search_code`, `search_issues`, `get_me`, `list_commits`, `get_commit`, `fork_repository`, `create_branch`, `list_branches`, `get_workflow_run`, `list_workflows`, `run_workflow`, `cancel_workflow_run`, `assign_copilot_to_issue`, `request_copilot_review`, `get_code_scanning_alert`, `list_code_scanning_alerts`, `create_pending_pull_request_review`, `submit_pending_pull_request_review`, `add_comment_to_pending_review`, `get_pull_request_diff`, `get_pull_request_files`, `get_pull_request_reviews`, `list_tags`, `get_tag`, `push_files`<br>**Resources:** `repository_info`, `issue_details`, `pull_request_details`, `file_contents`, `commit_details`, `user_profile`, `organization_info`, `workflow_details`, `security_alerts`, `code_scanning_results` |
| **GitLab** | GitLab integration | `zereight/gitlab-mcp:latest` | 9009:8000 | `GITLAB_TOKEN`, `GITLAB_URL`, `GITLAB_API_VERSION` | **Tools:** `get_project`, `list_projects`, `create_project`, `get_issue`, `list_issues`, `create_issue`, `get_merge_request`, `list_merge_requests`, `create_merge_request`, `get_pipeline`, `list_pipelines`, `create_branch`, `list_branches`, `get_file`, `create_file`, `update_file`, `delete_file`, `get_user`, `list_users`<br>**Resources:** `project_info`, `issue_details`, `merge_request_details`, `pipeline_status`, `file_contents`, `user_profile` |
| **SonarQube** | Code quality analysis | `sonarsource/sonarqube-mcp-server:latest` | 9010:8000 | `SONARQUBE_URL`, `SONARQUBE_TOKEN`, `SONARQUBE_ORGANIZATION` | **Tools:** `get_project`, `list_projects`, `get_issues`, `search_issues`, `get_measures`, `get_metrics`, `get_hotspots`, `get_duplications`, `get_coverage`, `get_tests`, `get_components`, `search_components`, `get_rules`, `search_rules`<br>**Resources:** `project_metrics`, `code_issues`, `security_hotspots`, `code_coverage`, `duplications`, `test_results`, `quality_gate_status` |
| **MCP Gateway** | Central routing and management | Custom build (`./docker/mcp-gateway`) | 9000:8080 | `MCP_SERVERS`, `GATEWAY_PORT` | **Tools:** `route_request`, `list_servers`, `get_server_status`, `proxy_call`<br>**Resources:** `server_registry`, `routing_table`, `health_status` |

## Server Categories

### 🔧 **Core Development Tools**
- **Git Server**: Version control operations
- **Filesystem Server**: File system operations with security controls
- **Fetch Server**: External content retrieval

### 💾 **Data & Storage**
- **Memory Server**: Knowledge graph and persistent memory
- **PostgreSQL Server**: Database operations and queries
- **Time Server**: Temporal utilities and timezone handling

### 🏢 **Platform Integration**
- **GitHub Server**: Complete GitHub ecosystem integration
- **GitLab Server**: GitLab repository and CI/CD management
- **SonarQube Server**: Code quality and security analysis

### 🛠️ **Infrastructure**
- **Everything Server**: Testing and reference implementation
- **MCP Gateway**: Central routing and server management

## GitHub Server Toolsets

The GitHub server supports modular toolsets that can be configured via `GITHUB_TOOLSETS`:

| Toolset | Description | Key Tools |
|---------|-------------|-----------|
| `context` | User context and GitHub info | `get_user`, `get_authenticated_user` |
| `repos` | Repository operations | `create_repository`, `get_repository`, `list_repositories`, `fork_repository` |
| `issues` | Issue management | `create_issue`, `get_issue`, `list_issues`, `update_issue`, `create_comment` |
| `pull_requests` | PR management | `create_pull_request`, `get_pull_request`, `list_pull_requests`, `merge_pull_request` |
| `actions` | GitHub Actions/CI-CD | `list_workflows`, `get_workflow_run`, `trigger_workflow` |
| `code_security` | Security scanning | `list_security_alerts`, `get_vulnerability_alert`, `list_dependabot_alerts` |
| `discussions` | GitHub Discussions | `create_discussion`, `get_discussion`, `list_discussions` |
| `notifications` | Notification management | `list_notifications`, `mark_as_read` |
| `orgs` | Organization management | `get_organization`, `list_org_members`, `list_org_repositories` |
| `users` | User operations | `get_user`, `list_users`, `follow_user` |

## Configuration Notes

### Volume Mounts
- **Git Server**: Read-only workspace access, Git config, SSH keys
- **Filesystem Server**: Full workspace access with security controls
- **Memory Server**: Persistent data volume (`mcp_memory_data`)
- **PostgreSQL**: Configuration directory mount

### Network Configuration
- All servers run on the `ai-dev-mcp` bridge network
- Subnet: `172.20.0.0/16` (masked for security)
- Internal communication on port 8000
- External access via mapped ports (9001-9010, 9000 for gateway)

### Health Checks
- **Core MCP Servers**: Python module import tests
- **External Services**: HTTP health endpoint checks (`/health`)
- **PostgreSQL**: Database readiness checks (`pg_isready`)

### Security Considerations
- **Filesystem Server**: Directory access controls and read-only restrictions
- **GitHub/GitLab/SonarQube**: Token-based authentication
- **Memory Server**: Size limits (1GB default)
- **Fetch Server**: Response size limits (10MB default)

## Usage Examples

### Git Operations
```bash
# Via MCP client
mcp-call git_status
mcp-call git_commit --message "Update documentation"
```

### File Operations
```bash
# Via MCP client
mcp-call read_file --path "/workspace/README.md"
mcp-call list_directory --path "/workspace"
```

### GitHub Integration
```bash
# Via MCP client
mcp-call create_issue --title "Bug Report" --body "Description"
mcp-call list_pull_requests --repository "owner/repo"
```

### Knowledge Graph
```bash
# Via MCP client
mcp-call create_entities --entities '[{"name": "project", "entityType": "software"}]'
mcp-call add_observations --observations '[{"content": "Project uses Python"}]'
```

This comprehensive table provides all the necessary information to understand and utilize the MCP servers configured in your Docker Compose setup.
