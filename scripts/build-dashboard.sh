#!/bin/bash

# Build script for dashboard with git versioning
set -e

# Get current git tag/version
GIT_TAG=$(git describe --tags --always 2>/dev/null || echo "v0.2.0")
BUILD_DATE=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || python3 -c "import datetime; print(datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'))")

echo "🏷️  Building dashboard with version: $GIT_TAG"
echo "📅 Build date: $BUILD_DATE"

# Export environment variables for docker-compose
export GIT_TAG="$GIT_TAG"
export BUILD_DATE="$BUILD_DATE"

# Build the dashboard service
docker-compose build dashboard

echo "✅ Dashboard built successfully with version $GIT_TAG"
