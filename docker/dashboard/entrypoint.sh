#!/bin/sh

# Set default values for environment variables
export DASHBOARD_TITLE="${DASHBOARD_TITLE:-AI Dev Local Dashboard}"
export LANGFUSE_URL="${LANGFUSE_URL:-http://localhost:3000}"
export FLOWISE_URL="${FLOWISE_URL:-http://localhost:3001}"
export OPENWEBUI_URL="${OPENWEBUI_URL:-http://localhost:8080}"
export LITELLM_URL="${LITELLM_URL:-http://localhost:4000}"
export OLLAMA_URL="${OLLAMA_URL:-http://localhost:11434}"

# Substitute environment variables in the HTML template
envsubst < /usr/share/nginx/html/index.html.template > /usr/share/nginx/html/index.html

# Start the original command
exec "$@"
