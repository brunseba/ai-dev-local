# PostgreSQL MCP Server

The PostgreSQL MCP Server provides robust integration for database operations within the MCP ecosystem, allowing secure and efficient access to PostgreSQL databases through Server-Sent Events (SSE) transport.

## Features

- **Database Queries**: Execute SQL queries and transactions with ease
- **Schema Exploration**: Inspect and explore database schemas and structures
- **Data Management**: Perform CRUD operations on PostgreSQL data
- **Event Streaming**: Leverage Server-Sent Events (SSE) for real-time data updates
- **Restricted Access**: Runs in restricted mode for enhanced security
- **Multi-Network**: Connected to both MCP network and main AI Dev Local network

## Server Configuration

**Image**: `crystaldba/postgres-mcp:latest`  
**Port**: 9006  
**Transport**: Server-Sent Events (SSE)  
**Access Mode**: Restricted

### Docker Compose Configuration

```yaml
mcp-postgres:
  image: crystaldba/postgres-mcp:latest
  restart: unless-stopped
  command: ["--access-mode=restricted", "--transport=sse"]
  environment:
    - DATABASE_URI=postgresql://postgres:postgres@postgres:5432/postgres
    - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/postgres
    - POSTGRES_HOST=postgres
    - POSTGRES_PORT=5432
    - POSTGRES_DB=postgres
    - POSTGRES_USER=postgres
    - POSTGRES_PASSWORD=postgres
  ports:
    - "${MCP_POSTGRES_PORT:-9006}:8000"
  networks:
    - mcp-network
    - ai-dev-local
```

## Environment Variables

Ensure you have configured the following environment variables:

- `DATABASE_URI`: URI connection string for PostgreSQL (default: `postgresql://postgres:postgres@postgres:5432/postgres`)
- `DATABASE_URL`: Alternative connection string format
- `POSTGRES_HOST`: The hostname of the PostgreSQL server (default: `postgres`)
- `POSTGRES_PORT`: Port on which the PostgreSQL server is running (default: `5432`)
- `POSTGRES_DB`: Database name (default: `postgres`)
- `POSTGRES_USER`: Database username (default: `postgres`)
- `POSTGRES_PASSWORD`: Database password (default: `postgres`)

## Available Tools

The PostgreSQL MCP server provides the following tools for database operations:

### Core Database Operations
- **`query`**: Execute SQL SELECT queries
- **`execute`**: Execute SQL statements (INSERT, UPDATE, DELETE)
- **`list_tables`**: List all tables in the database
- **`describe_table`**: Get table schema and column information

### Schema Management
- **`create_table`**: Create new database tables
- **`drop_table`**: Delete existing tables
- **`get_schema_info`**: Retrieve database schema information

### Data Operations
- **`insert`**: Insert new records into tables
- **`update`**: Update existing records
- **`delete`**: Remove records from tables

## Usage Examples

### Running a Query

```bash
# Via HTTP endpoint
curl -X POST http://localhost:9006/tools/query \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"sql": "SELECT * FROM users LIMIT 10"}}'

# Via MCP client
mcp-call query --sql "SELECT * FROM users WHERE active = true"
```

### Describe a Table

```bash
# Get table structure
curl -X POST http://localhost:9006/tools/describe_table \
  -H "Content-Type: application/json" \
  -d '{"arguments": {"table_name": "users"}}'

# Via MCP client
mcp-call describe_table --table "users"
```

### List All Tables

```bash
# Get all tables in database
curl -X POST http://localhost:9006/tools/list_tables \
  -H "Content-Type: application/json" \
  -d '{}'

# Via MCP client
mcp-call list_tables
```

### Insert Data

```bash
# Insert new record
curl -X POST http://localhost:9006/tools/insert \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "table": "users",
      "data": {
        "name": "John Doe",
        "email": "john@example.com",
        "active": true
      }
    }
  }'
```

### Create a New Table

```bash
# Create table with schema
curl -X POST http://localhost:9006/tools/create_table \
  -H "Content-Type: application/json" \
  -d '{
    "arguments": {
      "name": "projects",
      "schema": "CREATE TABLE projects (id SERIAL PRIMARY KEY, name VARCHAR(255) NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    }
  }'
```

## Health Monitoring

### Health Check

```bash
# Check PostgreSQL MCP server health
curl http://localhost:9006/health

# Check PostgreSQL database connectivity
docker-compose -f docker-compose.mcp.yml exec mcp-postgres pg_isready -h postgres -U postgres
```

### Service Status

```bash
# Check service status
ai-dev-local mcp status | grep postgres

# View service logs
docker-compose -f docker-compose.mcp.yml logs -f mcp-postgres
```

## Network Configuration

The PostgreSQL MCP server is connected to two networks:

1. **`mcp-network`**: For communication with other MCP servers
2. **`ai-dev-local`**: For connection to the main PostgreSQL database

This dual-network setup ensures secure database access while maintaining MCP ecosystem connectivity.

## Security Considerations

### Access Control
- **Restricted Mode**: Server runs with `--access-mode=restricted` for enhanced security
- **Network Isolation**: Runs on isolated Docker networks
- **Connection Security**: Uses internal Docker networking for database connections

### Database Security
- **Credentials**: Database credentials are managed via environment variables
- **Network Access**: Database accessible only within Docker network
- **Least Privilege**: Grant minimal necessary permissions to database users

### Best Practices
- **Environment Variables**: Never hardcode database credentials
- **TLS Connections**: Enable SSL/TLS for database connections in production
- **Regular Updates**: Keep PostgreSQL and MCP server images updated
- **Monitoring**: Monitor database performance and access patterns

## Troubleshooting

### Common Issues

1. **Connection Failures**
   ```bash
   # Test database connectivity
   docker-compose -f docker-compose.mcp.yml exec mcp-postgres \
     psql postgresql://postgres:postgres@postgres:5432/postgres -c "SELECT 1;"
   ```

2. **Service Not Starting**
   ```bash
   # Check logs for errors
   docker-compose -f docker-compose.mcp.yml logs mcp-postgres
   
   # Restart service
   docker-compose -f docker-compose.mcp.yml restart mcp-postgres
   ```

3. **SSE Transport Issues**
   ```bash
   # Verify SSE endpoint
   curl -H "Accept: text/event-stream" http://localhost:9006/sse
   ```

## Integration Examples

### FlowiseAI Integration

```javascript
// FlowiseAI Custom Database Node
const executeQuery = async (sql, params = {}) => {
  const response = await fetch('http://mcp-postgres:8000/tools/query', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ arguments: { sql, params } })
  });
  return response.json();
};

// Example: Get user analytics
const analytics = await executeQuery(
  'SELECT COUNT(*) as total_users, AVG(age) as avg_age FROM users WHERE active = $1',
  [true]
);
```

### LiteLLM Integration

```python
# Custom database tool for LiteLLM
import requests

def db_query_tool(sql, **params):
    """Execute database query via MCP"""
    response = requests.post(
        'http://localhost:9006/tools/query',
        json={'arguments': {'sql': sql, 'params': params}}
    )
    return response.json()

# Usage example
result = db_query_tool(
    'SELECT * FROM projects WHERE status = %(status)s',
    status='active'
)
```

## Further Reading

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [PostgreSQL MCP Server Repository](https://github.com/crystaldba/postgres-mcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/docs/)
- [pgAdmin Tool](https://www.pgadmin.org/) for database management and visualization
- [Docker PostgreSQL Official Image](https://hub.docker.com/_/postgres)

