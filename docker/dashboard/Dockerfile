# Use a minimal nginx image as parent image
FROM nginx:alpine

# Install envsubst for environment variable substitution
RUN apk add --no-cache gettext

# Set working directory
WORKDIR /usr/share/nginx/html

# Copy static website template to Nginx path
COPY ./index.html.template ./index.html.template

# Copy custom Nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy startup script
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the listening port
EXPOSE 80

# Use custom entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["nginx", "-g", "daemon off;"]
