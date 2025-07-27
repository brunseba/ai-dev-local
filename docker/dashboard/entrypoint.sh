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

# Function to get Ollama models
get_ollama_models() {
    local ollama_url="${OLLAMA_URL:-http://localhost:11434}"
    local models_json="[]"
    local model_count="0"
    
    # Try to fetch models from Ollama API
    if models_response=$(curl -s --connect-timeout 5 --max-time 10 "${ollama_url}/api/tags" 2>/dev/null); then
        if echo "$models_response" | grep -q '"models"'; then
            models_json="$models_response"
            model_count=$(echo "$models_response" | grep -o '"name"' | wc -l | tr -d ' ')
        fi
    fi
    
    export OLLAMA_MODELS_JSON="$models_json"
    export OLLAMA_MODEL_COUNT="$model_count"
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

# Get Ollama models information
get_ollama_models

echo "Dashboard starting with version: $APP_VERSION (built: $BUILD_DATE)"
echo "Ollama models found: $OLLAMA_MODEL_COUNT"

# Substitute environment variables in the HTML template
envsubst < /usr/share/nginx/html/index.html.template > /usr/share/nginx/html/index.html

# Start the original command
exec "$@"
