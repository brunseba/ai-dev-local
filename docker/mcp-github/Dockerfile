# Extract binary from official GitHub MCP server image
FROM ghcr.io/github/github-mcp-server:latest as mcp-server

# Main Node.js application
FROM node:18-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the GitHub MCP server binary from the official image
COPY --from=mcp-server /server/github-mcp-server /usr/local/bin/github-mcp-server
RUN chmod +x /usr/local/bin/github-mcp-server

# Create app directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install Node.js dependencies
RUN npm install

# Copy application files
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the HTTP wrapper
CMD ["node", "wrapper.js"]
