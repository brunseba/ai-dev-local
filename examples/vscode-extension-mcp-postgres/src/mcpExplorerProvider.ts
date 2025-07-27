import * as vscode from 'vscode';
import { McpClient } from './mcpClient';

export class McpExplorerProvider implements vscode.TreeDataProvider<McpItem> {
    private _onDidChangeTreeData: vscode.EventEmitter<McpItem | undefined | null | void> = new vscode.EventEmitter<McpItem | undefined | null | void>();
    readonly onDidChangeTreeData: vscode.Event<McpItem | undefined | null | void> = this._onDidChangeTreeData.event;

    constructor(private mcpClient: McpClient) {}

    refresh(): void {
        this._onDidChangeTreeData.fire();
    }

    getTreeItem(element: McpItem): vscode.TreeItem {
        return element;
    }

    async getChildren(element?: McpItem): Promise<McpItem[]> {
        if (!this.mcpClient.isConnected()) {
            return [new McpItem('Not connected to MCP server', vscode.TreeItemCollapsibleState.None, 'disconnected')];
        }

        if (!element) {
            // Root level - show server status and tables
            try {
                const tables = await this.mcpClient.listTables();
                const items: McpItem[] = [];

                // Add server status
                items.push(new McpItem('✅ MCP Server Connected', vscode.TreeItemCollapsibleState.None, 'status'));

                // Add tables
                if (tables && tables.length > 0) {
                    const tablesItem = new McpItem('📊 Database Tables', vscode.TreeItemCollapsibleState.Expanded, 'tables-group');
                    items.push(tablesItem);

                    // Add individual tables
                    for (const table of tables) {
                        const tableName = typeof table === 'string' ? table : table.name || table.table_name;
                        if (tableName) {
                            const tableItem = new McpItem(`🗂️ ${tableName}`, vscode.TreeItemCollapsibleState.Collapsible, 'table');
                            tableItem.tooltip = `Table: ${tableName}`;
                            tableItem.command = {
                                command: 'ai-dev-local.describeTable',
                                title: 'Describe Table',
                                arguments: [tableItem]
                            };
                            items.push(tableItem);
                        }
                    }
                } else {
                    items.push(new McpItem('No tables found', vscode.TreeItemCollapsibleState.None, 'empty'));
                }

                return items;
            } catch (error) {
                return [new McpItem(`Error: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
            }
        } else if (element.contextValue === 'table') {
            // Show table details
            try {
                const tableName = element.label?.toString().replace('🗂️ ', '') || '';
                const schema = await this.mcpClient.describeTable(tableName);
                
                const items: McpItem[] = [];
                
                if (schema && schema.columns) {
                    items.push(new McpItem('📋 Columns', vscode.TreeItemCollapsibleState.Expanded, 'columns-group'));
                    
                    for (const column of schema.columns) {
                        const columnName = column.column_name || column.name;
                        const columnType = column.data_type || column.type;
                        const nullable = column.is_nullable === 'YES' || column.nullable ? '(nullable)' : '(not null)';
                        
                        const columnItem = new McpItem(
                            `📝 ${columnName}: ${columnType} ${nullable}`,
                            vscode.TreeItemCollapsibleState.None,
                            'column'
                        );
                        columnItem.tooltip = `Column: ${columnName}\nType: ${columnType}\nNullable: ${column.is_nullable === 'YES' || column.nullable ? 'Yes' : 'No'}`;
                        items.push(columnItem);
                    }
                }

                if (schema && schema.row_count !== undefined) {
                    items.push(new McpItem(`📊 Row Count: ${schema.row_count}`, vscode.TreeItemCollapsibleState.None, 'info'));
                }

                return items;
            } catch (error) {
                return [new McpItem(`Error loading table details: ${error}`, vscode.TreeItemCollapsibleState.None, 'error')];
            }
        }

        return [];
    }
}

class McpItem extends vscode.TreeItem {
    constructor(
        public readonly label: string,
        public readonly collapsibleState: vscode.TreeItemCollapsibleState,
        public readonly contextValue: string
    ) {
        super(label, collapsibleState);
        this.contextValue = contextValue;

        // Set icons based on context
        switch (contextValue) {
            case 'status':
                this.iconPath = new vscode.ThemeIcon('server-process');
                break;
            case 'tables-group':
                this.iconPath = new vscode.ThemeIcon('database');
                break;
            case 'table':
                this.iconPath = new vscode.ThemeIcon('table');
                break;
            case 'columns-group':
                this.iconPath = new vscode.ThemeIcon('list-unordered');
                break;
            case 'column':
                this.iconPath = new vscode.ThemeIcon('symbol-field');
                break;
            case 'info':
                this.iconPath = new vscode.ThemeIcon('info');
                break;
            case 'error':
                this.iconPath = new vscode.ThemeIcon('error');
                break;
            case 'disconnected':
                this.iconPath = new vscode.ThemeIcon('debug-disconnect');
                break;
            default:
                this.iconPath = new vscode.ThemeIcon('circle-outline');
        }
    }
}
