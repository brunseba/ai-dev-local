# Flowise Silent Setup Configuration

This directory contains configuration files for Flowise silent setup in the AI Dev Local environment.

## Overview

Flowise is configured using the **v3.0.1+ Email/Password Authentication System** with the following features:

- 🔐 **Modern Authentication**: Passport.js-based system with JWT tokens in secure HTTP-only cookies
- 🗄️ **Automatic Database Setup**: PostgreSQL integration with automatic schema creation
- ⚡ **Performance Optimized**: Configured timeouts and upload limits
- 🛡️ **Security Hardened**: bcrypt password hashing, secure token management
- 🎯 **Ready-to-Use**: Legacy username/password enables initial admin account creation

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
| **Legacy Username** | `admin` | Required for initial admin account setup |
| **Legacy Password** | `admin123` | Required for initial admin account setup (change in production!) |
| **Port** | `3001` | Internal Flowise port (mapped via docker-compose) |
| **Database** | PostgreSQL | Using shared postgres service |
| **Authentication** | Email/Password + JWT | v3.0.1+ Passport.js system with secure cookies |
| **Access Token Expiry** | 60 minutes | Short-lived access tokens |
| **Refresh Token Expiry** | 90 days | Long-lived refresh tokens |
| **Password Hashing** | bcrypt (12 rounds) | Secure password storage |
| **CORS** | `*` | Allow all origins (development setup) |

## Environment Variables

The following environment variables are automatically configured:

### Authentication (v3.0.1+ System)
```bash
# Legacy credentials (required for initial admin account setup)
FLOWISE_USERNAME=admin
FLOWISE_PASSWORD=admin123

# JWT Configuration
JWT_AUTH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDD
JWT_REFRESH_TOKEN_SECRET=AABBCCDDAABBCCDDAABBCCDDAABBCCDDAABBCCDD
JWT_TOKEN_EXPIRY_IN_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRY_IN_MINUTES=129600
EXPRESS_SESSION_SECRET=flowise-ai-dev-local

# Application URL
APP_URL=http://localhost:3001
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
# Password Security
PASSWORD_RESET_TOKEN_EXPIRY_IN_MINS=15
PASSWORD_SALT_HASH_ROUNDS=12
TOKEN_HASH_SECRET=ai-dev-local-token-hash-secret-key

# Privacy
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

### Initial Setup (First Time)
1. **URL**: http://localhost:3001
2. **Authentication**: Use legacy credentials to set up admin account
   - **Username**: admin
   - **Password**: admin123
3. **Create Admin Account**: Follow the setup wizard to create your email/password account

### Subsequent Access
- **URL**: http://localhost:3001
- **Login**: Use the email/password you created during initial setup
- **Authentication**: Secure JWT tokens in HTTP-only cookies

## Customization

To customize the configuration:

1. **Edit Configuration**: Modify `flowise.json` with your preferred settings
2. **Update Environment**: Change values in `.env` file
3. **Restart Service**: `docker compose restart flowise`

### Example Customizations

```bash
# Enhanced security for production
PASSWORD_SALT_HASH_ROUNDS=15
TOKEN_HASH_SECRET=your-super-secure-random-string
JWT_TOKEN_EXPIRY_IN_MINUTES=30

# Adjust performance settings
CHATFLOW_WORKER_TIMEOUT=60000
MAX_UPLOAD_SIZE=100mb

# Enable debugging
DEBUG=true
LOG_LEVEL=debug
```

## Security Notes

⚠️ **Important Security Considerations**:

1. **Complete Initial Setup**: Use legacy credentials only for initial admin account creation
2. **Strong Admin Credentials**: Create a strong email/password combination during setup
3. **Secure JWT Secrets**: Generate new JWT secrets for production use
4. **Password Security**: Configure higher `PASSWORD_SALT_HASH_ROUNDS` (12-15) for production
5. **Token Secrets**: Use strong, unique `TOKEN_HASH_SECRET` values
6. **Network Security**: Configure appropriate CORS origins for production
7. **Database Security**: Use strong database credentials in production

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
