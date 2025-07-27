import axios, { AxiosInstance } from 'axios';
import * as vscode from 'vscode';

export class McpClient {
    private httpClient: AxiosInstance;
    private baseUrl: string;
    private connected: boolean = false;

    constructor() {
        const config = vscode.workspace.getConfiguration('ai-dev-local');
        const host = config.get<string>('mcpServer.host', 'localhost');
        const port = config.get<number>('mcpServer.port', 9006);
        
        this.baseUrl = `http://${host}:${port}`;
        this.httpClient = axios.create({
            baseURL: this.baseUrl,
            timeout: 10000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }

    async connect(): Promise<boolean> {
        try {
            // Check health endpoint
            const healthResponse = await this.httpClient.get('/health');
            if (healthResponse.data.status === 'healthy') {
                this.connected = true;
                console.log('Connected to MCP PostgreSQL server');
                return true;
            }
        } catch (error) {
            console.error('Failed to connect to MCP server:', error);
            this.connected = false;
        }
        return false;
    }

    disconnect(): void {
        this.connected = false;
        console.log('Disconnected from MCP server');
    }

    isConnected(): boolean {
        return this.connected;
    }

    async listTables(): Promise<any[]> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await this.httpClient.post('/tools/list_tables', {});
            
            if (response.data.jsonrpc && response.data.result) {
                const content = response.data.result.content;
                if (content && content.length > 0) {
                    const tableData = JSON.parse(content[0].text);
                    return tableData.tables || [];
                }
            }
            return [];
        } catch (error) {
            console.error('Error listing tables:', error);
            throw error;
        }
    }

    async describeTable(tableName: string): Promise<any> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await this.httpClient.post('/tools/describe_table', {
                arguments: {
                    table_name: tableName
                }
            });

            if (response.data.jsonrpc && response.data.result) {
                const content = response.data.result.content;
                if (content && content.length > 0) {
                    return JSON.parse(content[0].text);
                }
            }
            return null;
        } catch (error) {
            console.error('Error describing table:', error);
            throw error;
        }
    }

    async executeQuery(query: string): Promise<any> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await this.httpClient.post('/tools/execute_query', {
                arguments: {
                    query: query
                }
            });

            if (response.data.jsonrpc && response.data.result) {
                const content = response.data.result.content;
                if (content && content.length > 0) {
                    return JSON.parse(content[0].text);
                }
            }
            return null;
        } catch (error) {
            console.error('Error executing query:', error);
            throw error;
        }
    }

    async getAvailableTools(): Promise<any[]> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await this.httpClient.get('/tools');
            
            if (response.data.jsonrpc && response.data.result) {
                return response.data.result.tools || [];
            }
            return [];
        } catch (error) {
            console.error('Error getting available tools:', error);
            throw error;
        }
    }

    async callTool(toolName: string, args: any = {}): Promise<any> {
        if (!this.connected) {
            throw new Error('Not connected to MCP server');
        }

        try {
            const response = await this.httpClient.post(`/tools/${toolName}`, {
                arguments: args
            });

            if (response.data.jsonrpc && response.data.result) {
                const content = response.data.result.content;
                if (content && content.length > 0) {
                    return JSON.parse(content[0].text);
                }
            }
            return null;
        } catch (error) {
            console.error(`Error calling tool ${toolName}:`, error);
            throw error;
        }
    }
}
