const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
const port = 8000;

// Middleware
app.use(cors());
app.use(express.json());

// PostgreSQL MCP Server process
let mcpProcess = null;
let isReady = false;

// Start the PostgreSQL MCP server
function startMCPServer() {
    if (mcpProcess) {
        mcpProcess.kill();
    }

    console.log('Starting PostgreSQL MCP server...');
    
    mcpProcess = spawn('postgres-mcp', ['--access-mode=restricted'], {
        env: {
            ...process.env
        }
    });

    mcpProcess.stdout.on('data', (data) => {
        console.log('MCP Server stdout:', data.toString());
    });

    mcpProcess.stderr.on('data', (data) => {
        console.error('MCP Server stderr:', data.toString());
    });

    mcpProcess.on('close', (code) => {
        console.log(`MCP Server process exited with code ${code}`);
        isReady = false;
        // Restart after a delay
        setTimeout(startMCPServer, 5000);
    });

    mcpProcess.on('error', (error) => {
        console.error('Failed to start MCP Server:', error);
        isReady = false;
    });

    // Give the server time to start
    setTimeout(() => {
        isReady = true;
        console.log('PostgreSQL MCP server is ready');
    }, 2000);
}

// Send MCP message and get response
function sendMCPMessage(message) {
    return new Promise((resolve, reject) => {
        if (!mcpProcess || !isReady) {
            reject(new Error('MCP Server not ready'));
            return;
        }

        const messageStr = JSON.stringify(message) + '\n';
        console.log('Sending MCP message:', messageStr.trim());
        
        // Set up response handler
        const responseHandler = (data) => {
            try {
                const dataStr = data.toString().trim();
                console.log('Received MCP response:', dataStr);
                const response = JSON.parse(dataStr);
                mcpProcess.stdout.removeListener('data', responseHandler);
                resolve(response);
            } catch (error) {
                console.error('Failed to parse MCP response:', error.message);
                reject(new Error('Invalid JSON response from MCP server'));
            }
        };

        mcpProcess.stdout.once('data', responseHandler);
        
        try {
            mcpProcess.stdin.write(messageStr);
        } catch (error) {
            console.error('Failed to write to MCP server:', error.message);
            reject(new Error('Failed to communicate with MCP server'));
            return;
        }

        // Increase timeout to 15 seconds
        setTimeout(() => {
            mcpProcess.stdout.removeListener('data', responseHandler);
            reject(new Error('MCP Server response timeout'));
        }, 15000);
    });
}

// Health check endpoint
app.get('/health', (req, res) => {
    if (isReady && mcpProcess && !mcpProcess.killed) {
        res.json({ status: 'healthy', service: 'postgres-mcp-wrapper' });
    } else {
        res.status(503).json({ status: 'unhealthy', service: 'postgres-mcp-wrapper' });
    }
});

// MCP initialize endpoint
app.post('/initialize', async (req, res) => {
    try {
        const response = await sendMCPMessage({
            jsonrpc: '2.0',
            id: 1,
            method: 'initialize',
            params: {
                protocolVersion: '2024-11-05',
                capabilities: {
                    resources: {},
                    tools: {},
                    prompts: {}
                },
                clientInfo: {
                    name: 'ai-dev-local',
                    version: '1.0.0'
                }
            }
        });
        res.json(response);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// MCP resources list endpoint
app.get('/resources', async (req, res) => {
    try {
        const response = await sendMCPMessage({
            jsonrpc: '2.0',
            id: 2,
            method: 'resources/list'
        });
        res.json(response);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// MCP tools list endpoint
app.get('/tools', async (req, res) => {
    try {
        const response = await sendMCPMessage({
            jsonrpc: '2.0',
            id: 3,
            method: 'tools/list'
        });
        res.json(response);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// MCP tool call endpoint
app.post('/tools/:toolName', async (req, res) => {
    try {
        const { toolName } = req.params;
        const { arguments: toolArgs = {} } = req.body;
        
        const response = await sendMCPMessage({
            jsonrpc: '2.0',
            id: Date.now(),
            method: 'tools/call',
            params: {
                name: toolName,
                arguments: toolArgs
            }
        });
        res.json(response);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Generic MCP message endpoint
app.post('/message', async (req, res) => {
    try {
        const response = await sendMCPMessage(req.body);
        res.json(response);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Error handling middleware
app.use((error, req, res, next) => {
    console.error('Express error:', error);
    res.status(500).json({ error: 'Internal server error' });
});

// Start server
app.listen(port, () => {
    console.log(`PostgreSQL MCP HTTP wrapper listening on port ${port}`);
});

// Start the MCP server process
startMCPServer();

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('Received SIGTERM, shutting down gracefully');
    if (mcpProcess) {
        mcpProcess.kill();
    }
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('Received SIGINT, shutting down gracefully');
    if (mcpProcess) {
        mcpProcess.kill();
    }
    process.exit(0);
});

