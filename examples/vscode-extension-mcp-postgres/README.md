# AI Dev Local - MCP Integration

A VS Code extension for interacting with AI Dev Local MCP (Model Context Protocol) servers, specifically designed to work with the PostgreSQL MCP server.

## Features

- **Database Explorer**: Browse database tables and their schemas directly in VS Code
- **Table Operations**: List tables, describe table structures, and execute SQL queries
- **MCP Integration**: Connect to MCP servers via HTTP wrapper
- **Real-time Updates**: Refresh database information dynamically

## Prerequisites

- VS Code 1.74.0 or higher
- AI Dev Local MCP PostgreSQL server running on port 9006 (default)
- Node.js and npm for development

## Installation

1. Clone or download the extension files
2. Open the `vscode-extension` folder in VS Code
3. Run `npm install` to install dependencies
4. Press `F5` to run the extension in a new Extension Development Host window

## Configuration

The extension can be configured through VS Code settings:

```json
{
  "ai-dev-local.mcpServer.host": "localhost",
  "ai-dev-local.mcpServer.port": 9006,
  "ai-dev-local.mcpServer.autoConnect": true
}
```

### Settings

- `ai-dev-local.mcpServer.host`: MCP server hostname (default: "localhost")
- `ai-dev-local.mcpServer.port`: MCP server port (default: 9006)
- `ai-dev-local.mcpServer.autoConnect`: Auto-connect on startup (default: true)

## Usage

### MCP Database Explorer

The extension adds an "MCP Database Explorer" view to the VS Code Explorer panel:

- **Connection Status**: Shows if connected to the MCP server
- **Database Tables**: Lists all available tables
- **Table Details**: Expand tables to see column information

### Commands

Access these commands via the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`):

- `AI Dev Local: List Database Tables` - Show all tables in the database
- `AI Dev Local: Describe Table` - Get detailed schema information for a table
- `AI Dev Local: Query Database` - Execute custom SQL queries
- `AI Dev Local: Connect to MCP Server` - Manually connect to the MCP server

### Context Menu Actions

Right-click on tables in the MCP Database Explorer for quick actions:

- **Describe Table**: View table schema and column details

## Example Workflow

1. **Start the MCP Server**: Ensure your AI Dev Local PostgreSQL MCP server is running
2. **Open VS Code**: The extension will auto-connect if enabled
3. **Browse Tables**: Use the MCP Database Explorer to see available tables
4. **Explore Schema**: Click on tables to see their column structure
5. **Run Queries**: Use the "Query Database" command to execute SQL

## API Integration

The extension communicates with the MCP server via HTTP endpoints:

- `GET /health` - Check server health
- `GET /tools` - List available MCP tools
- `POST /tools/list_tables` - Get database tables
- `POST /tools/describe_table` - Get table schema
- `POST /tools/execute_query` - Run SQL queries

## Development

To develop or modify the extension:

1. Clone the repository
2. Run `npm install` to install dependencies
3. Make your changes to the TypeScript files in `src/`
4. Run `npm run compile` to build the extension
5. Press `F5` to test in a new VS Code window

### Project Structure

```
vscode-extension/
├── src/
│   ├── extension.ts          # Main extension entry point
│   ├── mcpClient.ts          # HTTP client for MCP communication
│   └── mcpExplorerProvider.ts # Tree view provider for database explorer
├── package.json              # Extension manifest and dependencies
├── tsconfig.json            # TypeScript configuration
└── README.md               # This file
```

## Troubleshooting

### Connection Issues

- Ensure the MCP PostgreSQL server is running on the configured port
- Check that the server health endpoint returns "healthy" status
- Verify network connectivity and firewall settings

### Extension Not Loading

- Check the VS Code Developer Console for error messages
- Ensure all dependencies are installed (`npm install`)
- Verify TypeScript compilation succeeded (`npm run compile`)

### Database Queries Failing

- Confirm the PostgreSQL database is accessible
- Check database credentials and connection settings
- Review MCP server logs for detailed error information

## License

MIT License - see the project's main LICENSE file for details.

## Contributing

Contributions are welcome! Please follow the project's coding standards and include tests for new features.
