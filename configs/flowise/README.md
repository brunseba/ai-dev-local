# Flowise Silent Setup Configuration

This directory contains configuration files for Flowise silent setup in the AI Dev Local environment.

## Overview

Flowise is configured for **silent, automated setup** with the following features:

- 🔐 **Pre-configured Authentication**: Default admin user with secure JWT tokens
- 🗄️ **Automatic Database Setup**: PostgreSQL integration with automatic schema creation
- ⚡ **Performance Optimized**: Configured timeouts and upload limits
- 🛡️ **Security Hardened**: Telemetry disabled, secure defaults
- 🎯 **Ready-to-Use**: No manual setup required after startup

## Files

### `flowise.json`
Main configuration file containing:
- Authentication settings (username/password/JWT)
- Database connection parameters
- Server configuration (CORS, ports, proxies)
- Feature flags and telemetry settings
- Storage paths and performance tuning
- Default credentials for API integrations

### `init.js`
Initialization script that:
- Creates required directory structure
- Loads configuration from JSON file
- Sets up environment variables
- Configures authentication and database
- Prepares default credentials

## Default Settings

| Setting | Value | Description |
|---------|-------|-------------|
| **Username** | `admin` | Default admin username |
| **Password** | `admin123` | Default admin password (change in production!) |
| **Port** | `3001` | Internal Flowise port (mapped via docker-compose) |
| **Database** | PostgreSQL | Using shared postgres service |
| **Authentication** | JWT | Token-based authentication enabled |
| **Telemetry** | Disabled | Privacy-focused configuration |
| **CORS** | `*` | Allow all origins (development setup) |

## Environment Variables

The following environment variables are automatically configured:

### Authentication
```bash
FLOWISE_USERNAME=admin
FLOWISE_PASSWORD=admin123
JWT_AUTH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDD
JWT_REFRESH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDD
```

### Database
```bash
DATABASE_TYPE=postgres
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=flowise
OVERRIDE_DATABASE=true
```

### Performance
```bash
CHATFLOW_WORKER_TIMEOUT=30000
DEPLOY_TIMEOUT=120000
MAX_UPLOAD_SIZE=50mb
```

### Security
```bash
DISABLE_FLOWISE_TELEMETRY=true
LANGCHAIN_TRACING_V2=false
NUMBER_OF_PROXIES=1
```

## Usage

The configuration is automatically applied when you start Flowise with AI Dev Local:

```bash
# Start all services including Flowise
ai-dev-local start

# Or start just Flowise with dependencies
docker compose up flowise postgres
```

## Accessing Flowise

Once started, access Flowise at:
- **URL**: http://localhost:3001
- **Username**: admin
- **Password**: admin123

## Customization

To customize the configuration:

1. **Edit Configuration**: Modify `flowise.json` with your preferred settings
2. **Update Environment**: Change values in `.env` file
3. **Restart Service**: `docker compose restart flowise`

### Example Customizations

```bash
# Change default credentials
FLOWISE_USERNAME=myuser
FLOWISE_PASSWORD=mysecurepassword

# Adjust performance settings
CHATFLOW_WORKER_TIMEOUT=60000
MAX_UPLOAD_SIZE=100mb

# Enable debugging
DEBUG=true
LOG_LEVEL=debug
```

## Security Notes

⚠️ **Important Security Considerations**:

1. **Change Default Password**: The default password `admin123` should be changed in production
2. **Secure JWT Secrets**: Generate new JWT secrets for production use
3. **Network Security**: Configure appropriate CORS origins for production
4. **Database Security**: Use strong database credentials in production

## Troubleshooting

### Common Issues

1. **Cannot Login**: Check if username/password match environment variables
2. **Database Connection**: Ensure PostgreSQL service is healthy
3. **Port Conflicts**: Verify port 3001 is available
4. **Permission Issues**: Check Docker volume permissions

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# In .env file
DEBUG=true
LOG_LEVEL=debug

# Restart Flowise
docker compose restart flowise
```

### Logs

View Flowise logs:

```bash
# Follow logs
docker compose logs -f flowise

# View recent logs
docker compose logs --tail=50 flowise
```

## Integration

Flowise integrates seamlessly with other AI Dev Local services:

- **LiteLLM**: Access unified LLM APIs
- **Langfuse**: Automatic observability and analytics
- **Open WebUI**: Share models and configurations
- **PostgreSQL**: Shared database for persistence

## API Access

Flowise provides REST APIs for programmatic access:

- **Base URL**: http://localhost:3001/api/v1
- **Authentication**: JWT tokens or API keys
- **Documentation**: Available in Flowise UI under API section

For API integration examples, see the main AI Dev Local documentation.
