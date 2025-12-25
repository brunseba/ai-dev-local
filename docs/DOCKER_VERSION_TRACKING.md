# Docker Image Version Tracking

The AI Dev Local CLI includes built-in Docker image version tracking to help you monitor and manage the Docker images used in your project.

## Features

- **Track all Docker images** from docker-compose files
- **Check for updates** on Docker Hub
- **Update specific services** to new image versions
- **Automatic backups** before making changes
- **Export tracking data** in multiple formats (table, list, JSON)

## Commands

### Track Versions

List all Docker images used in the project:

```bash
ai-dev-local docker track-versions
```

This command scans both `docker-compose.yml` and `docker-compose.mcp.yml` files and displays:
- Service name
- Image name
- Current version/tag
- Source compose file

#### Check for Updates

To check for available updates on Docker Hub:

```bash
ai-dev-local docker track-versions --check-updates
```

This will:
- Query Docker Hub API for the latest versions
- Compare current versions with available versions
- Display which services have updates available
- Skip pre-release tags (alpha, beta, rc, dev, etc.)

#### Output Formats

Choose your preferred output format:

```bash
# Table format (default)
ai-dev-local docker track-versions

# List format
ai-dev-local docker track-versions --format list

# JSON format
ai-dev-local docker track-versions --format json
```

### Update Image

Update a specific service to a new Docker image version:

```bash
ai-dev-local docker update-image <service-name> [--version <tag>]
```

**Examples:**

```bash
# Update postgres to version 16
ai-dev-local docker update-image postgres --version 16

# Update to latest version
ai-dev-local docker update-image redis
```

The command will:
1. Show current and new image versions
2. Ask for confirmation before proceeding
3. Create a backup of the docker-compose file
4. Update the image version in the compose file
5. Optionally pull the new image
6. Optionally restart the service with the new image

## Tracking File

Version tracking data is automatically saved to `.docker-versions.json` in your project root. This file contains:
- Timestamp of last check
- All discovered images with their versions
- Latest available versions (if checked)

The tracking file is excluded from git by default (added to `.gitignore`).

## Use Cases

### Regular Maintenance

Check for updates monthly:

```bash
ai-dev-local docker track-versions --check-updates
```

### Security Updates

Quickly identify which services need security updates:

```bash
ai-dev-local docker track-versions --check-updates --format json | jq '.images | to_entries[] | select(.value.latest_version != .value.current_version and .value.latest_version != "N/A")'
```

### Documentation

Generate a report of all images for documentation:

```bash
ai-dev-local docker track-versions --format json > docker-images-report.json
```

### CI/CD Integration

Integrate version tracking into your CI/CD pipeline to ensure images are up-to-date:

```bash
# In your CI script
ai-dev-local docker track-versions --check-updates --format json > versions.json
# Parse versions.json to fail build if critical updates are available
```

## Supported Registries

Currently, the update check feature works with:
- Docker Hub official images (e.g., `postgres:15`)
- Docker Hub user/org images (e.g., `flowiseai/flowise:latest`)

Images from other registries (e.g., `ghcr.io`, `gcr.io`) are tracked but update checks may not be available.

## Best Practices

1. **Backup First**: The `update-image` command automatically creates backups, but consider committing your current compose files before making changes.

2. **Test Updates**: Always test image updates in a development environment before applying to production.

3. **Version Pinning**: Avoid using `latest` tags in production. Pin to specific versions for reproducibility.

4. **Regular Checks**: Run `track-versions --check-updates` regularly to stay informed about available updates.

5. **Review Release Notes**: Before updating, review the release notes for breaking changes.

## Troubleshooting

### Docker Hub Rate Limits

If you encounter rate limit errors when checking for updates, you may need to:
- Wait before retrying
- Use a Docker Hub account and authenticate
- Check less frequently

### Update Check Fails

If the update check fails for specific images:
- Verify the image exists on Docker Hub
- Check your internet connection
- The image may be from a private registry or different registry

### Service Not Found

If the `update-image` command can't find your service:
- Verify the service name matches exactly (case-sensitive)
- Ensure the service is defined in one of the compose files
- Check that the service has an `image` field (not just `build`)

## Related Commands

- `ai-dev-local status` - Check running services
- `ai-dev-local start` - Start all services
- `ai-dev-local stop` - Stop all services
- `ai-dev-local logs <service>` - View service logs

---

**See Also:**
- [Main README](../README.md)
- [Development Guide](../CONTRIBUTING.md)
