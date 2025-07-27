# SonarQube MCP Server

The SonarQube MCP Server provides integration with SonarQube for code quality analysis, security scanning, and technical debt management.

## Features

- **Code Quality Analysis**: Access comprehensive code quality metrics and reports.
- **Security Scanning**: Identify security vulnerabilities and hotspots in your codebase.
- **Technical Debt Management**: Track and manage technical debt across projects.
- **Quality Gates**: Monitor quality gates and compliance status.

## Configuration

Ensure you have configured the following environment variables:

- `SONARQUBE_URL`: The URL of your SonarQube instance (default: `http://localhost:9000`).
- `SONARQUBE_TOKEN`: Your authentication token for accessing the SonarQube API.
- `SONARQUBE_ORGANIZATION`: Your organization key (required for SonarCloud).

## Usage Examples

### Listing Projects

```bash
mcp-call list_projects
```

### Getting Project Metrics

```bash
mcp-call get_measures --project_key "my-project" --metrics "coverage,bugs,vulnerabilities"
```

### Searching for Issues

```bash
mcp-call search_issues --project_key "my-project" --types "BUG,VULNERABILITY"
```

### Getting Security Hotspots

```bash
mcp-call get_hotspots --project_key "my-project"
```

## Available Metrics

SonarQube provides numerous metrics for code analysis:

- **Reliability**: `bugs`, `reliability_rating`
- **Security**: `vulnerabilities`, `security_rating`, `security_hotspots`
- **Maintainability**: `code_smells`, `sqale_rating`, `technical_debt`
- **Coverage**: `coverage`, `line_coverage`, `branch_coverage`
- **Duplications**: `duplicated_lines_density`, `duplicated_blocks`
- **Size**: `lines`, `ncloc`, `classes`, `functions`

## Quality Gate Status

Monitor your project's quality gate status:

```bash
mcp-call get_project --project_key "my-project"
```

The quality gate status indicates whether your project meets the defined quality criteria.

## Security Considerations

- **Token Security**: Keep your SonarQube token secure and limit its permissions.
- **Network Access**: Ensure proper network security between your application and SonarQube instance.
- **Data Privacy**: Be mindful of code analysis data being transmitted to external SonarQube instances.

## Integration with CI/CD

The SonarQube MCP server works well with CI/CD pipelines:

1. **Analysis Results**: Retrieve analysis results after code scans
2. **Quality Gates**: Check quality gate status before deployment
3. **Issue Tracking**: Monitor new issues introduced in recent commits

## Further Reading

- [SonarQube Documentation](https://docs.sonarqube.org/)
- [SonarQube Web API](https://docs.sonarqube.org/latest/extend/web-api/)
- [SonarQube Authentication](https://docs.sonarqube.org/latest/instance-administration/security/)

---
