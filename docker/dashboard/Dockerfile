# Use a minimal nginx image as parent image
FROM nginx:alpine

# Build arguments for versioning
ARG GIT_TAG=unknown
ARG BUILD_DATE=unknown

# Install git and envsubst for environment variable substitution
RUN apk add --no-cache gettext git

# Set working directory
WORKDIR /usr/share/nginx/html

# Create app directory for git repository
RUN mkdir -p /app

# Copy static website template to Nginx path
COPY ./index.html.template ./index.html.template

# Copy custom Nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy startup script and health script
COPY ./entrypoint.sh /entrypoint.sh
COPY ./health.sh /usr/share/nginx/html/health
RUN chmod +x /entrypoint.sh /usr/share/nginx/html/health

# Expose the listening port
EXPOSE 80

# Use custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
