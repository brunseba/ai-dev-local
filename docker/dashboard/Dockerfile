# Use a minimal nginx image as parent image
FROM nginx:alpine

# Set working directory
WORKDIR /usr/share/nginx/html

# Copy static website to Nginx path
COPY ./index.html .

# Copy custom Nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose the listening port
EXPOSE 80

# Start Nginx service
CMD ["nginx", "-g", "daemon off;"]
