import * as vscode from 'vscode';
import { McpClient } from './mcpClient';
import { McpExplorerProvider } from './mcpExplorerProvider';

let mcpClient: McpClient;
let mcpExplorerProvider: McpExplorerProvider;

export function activate(context: vscode.ExtensionContext) {
    console.log('AI Dev Local MCP extension is now active');

    // Initialize MCP client
    mcpClient = new McpClient();
    mcpExplorerProvider = new McpExplorerProvider(mcpClient);

    // Register the tree data provider
    vscode.window.registerTreeDataProvider('mcpExplorer', mcpExplorerProvider);

    // Register commands
    const listTablesCommand = vscode.commands.registerCommand('ai-dev-local.listTables', async () => {
        try {
            const tables = await mcpClient.listTables();
            if (tables && tables.length > 0) {
                const tableNames = tables.map((table: any) => table.name || table).join(', ');
                vscode.window.showInformationMessage(`Tables found: ${tableNames}`);
            } else {
                vscode.window.showInformationMessage('No tables found in the database');
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error listing tables: ${error}`);
        }
    });

    const describeTableCommand = vscode.commands.registerCommand('ai-dev-local.describeTable', async (tableItem?: any) => {
        try {
            let tableName: string | undefined;
            
            if (tableItem && tableItem.label) {
                tableName = tableItem.label;
            } else {
                // Show input box to get table name
                tableName = await vscode.window.showInputBox({
                    prompt: 'Enter table name to describe',
                    placeHolder: 'table_name'
                });
            }

            if (!tableName) {
                return;
            }

            const schema = await mcpClient.describeTable(tableName);
            if (schema) {
                // Create a new document to show the table schema
                const doc = await vscode.workspace.openTextDocument({
                    content: JSON.stringify(schema, null, 2),
                    language: 'json'
                });
                await vscode.window.showTextDocument(doc);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error describing table: ${error}`);
        }
    });

    const queryDatabaseCommand = vscode.commands.registerCommand('ai-dev-local.queryDatabase', async () => {
        try {
            const query = await vscode.window.showInputBox({
                prompt: 'Enter SQL query',
                placeHolder: 'SELECT * FROM table_name LIMIT 10;'
            });

            if (!query) {
                return;
            }

            const result = await mcpClient.executeQuery(query);
            if (result) {
                // Create a new document to show the query results
                const doc = await vscode.workspace.openTextDocument({
                    content: JSON.stringify(result, null, 2),
                    language: 'json'
                });
                await vscode.window.showTextDocument(doc);
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error executing query: ${error}`);
        }
    });

    const refreshExplorerCommand = vscode.commands.registerCommand('ai-dev-local.refreshMcpExplorer', () => {
        mcpExplorerProvider.refresh();
    });

    const connectMcpCommand = vscode.commands.registerCommand('ai-dev-local.connectMcp', async () => {
        try {
            const connected = await mcpClient.connect();
            if (connected) {
                vscode.window.showInformationMessage('Connected to MCP server successfully');
                mcpExplorerProvider.refresh();
            } else {
                vscode.window.showErrorMessage('Failed to connect to MCP server');
            }
        } catch (error) {
            vscode.window.showErrorMessage(`Error connecting to MCP server: ${error}`);
        }
    });

    // Add commands to disposables
    context.subscriptions.push(
        listTablesCommand,
        describeTableCommand,
        queryDatabaseCommand,
        refreshExplorerCommand,
        connectMcpCommand
    );

    // Auto-connect if enabled
    const config = vscode.workspace.getConfiguration('ai-dev-local');
    if (config.get('mcpServer.autoConnect')) {
        mcpClient.connect().then((connected) => {
            if (connected) {
                mcpExplorerProvider.refresh();
            }
        }).catch((error) => {
            console.error('Auto-connect failed:', error);
        });
    }
}

export function deactivate() {
    if (mcpClient) {
        mcpClient.disconnect();
    }
}
