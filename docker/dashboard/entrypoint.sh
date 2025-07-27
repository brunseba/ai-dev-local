#!/bin/sh

# Function to get git version
get_git_version() {
    if [ -d "/app/.git" ]; then
        cd /app
        # Try to get exact tag first
        if git describe --tags --exact-match 2>/dev/null; then
            return
        fi
        # Fallback to latest tag with commits
        if git describe --tags --always 2>/dev/null; then
            return
        fi
    fi
    # Final fallback
    echo "${APP_VERSION:-v0.2.0}"
}

# Set default values for environment variables
export DASHBOARD_TITLE="${DASHBOARD_TITLE:-AI Dev Local Dashboard}"
export LANGFUSE_URL="${LANGFUSE_URL:-http://localhost:3000}"
export FLOWISE_URL="${FLOWISE_URL:-http://localhost:3001}"
export OPENWEBUI_URL="${OPENWEBUI_URL:-http://localhost:8080}"
export LITELLM_URL="${LITELLM_URL:-http://localhost:4000}"
export OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"

# Get version information
export APP_VERSION="$(get_git_version)"

# Set build date with fallback
if [ -z "$BUILD_DATE" ] || [ "$BUILD_DATE" = "unknown" ]; then
    export BUILD_DATE="$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || echo "$(date -u +"%Y-%m-%d %H:%M:%S UTC" 2>/dev/null)")"
fi

echo "Dashboard starting with version: $APP_VERSION (built: $BUILD_DATE)"

# Substitute environment variables in the HTML template
envsubst < /usr/share/nginx/html/index.html.template > /usr/share/nginx/html/index.html

# Start the original command
exec "$@"
