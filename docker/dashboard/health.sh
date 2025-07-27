#!/bin/sh

# Health check endpoint that returns version information
echo "Content-Type: application/json"
echo ""

# Get version from environment or git
if [ -d "/app/.git" ]; then
    cd /app
    VERSION=$(git describe --tags --always 2>/dev/null || echo "${APP_VERSION:-v0.2.0}")
else
    VERSION="${APP_VERSION:-v0.2.0}"
fi

BUILD_DATE="${BUILD_DATE:-$(date -u +"%Y-%m-%dT%H:%M:%SZ")}"

cat << EOF
{
  "status": "healthy",
  "version": "$VERSION",
  "build_date": "$BUILD_DATE",
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
}
EOF
