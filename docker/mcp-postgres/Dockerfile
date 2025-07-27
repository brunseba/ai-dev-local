# Use the official PostgreSQL MCP server image as base
FROM crystaldba/postgres-mcp:latest

# Install Node.js and npm for the HTTP wrapper
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create wrapper app directory
WORKDIR /wrapper

# Copy package.json and install dependencies
COPY package.json ./
RUN npm install

# Copy wrapper source
COPY wrapper.js ./

# Expose port 8000 for the HTTP wrapper
EXPOSE 8000

# Set environment variables
ENV NODE_ENV=production

# Override the entrypoint and start the HTTP wrapper
ENTRYPOINT []
CMD ["node", "wrapper.js"]
