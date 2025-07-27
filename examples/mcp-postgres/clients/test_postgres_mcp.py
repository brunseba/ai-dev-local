#!/usr/bin/env python3

import json
import requests
import time

def test_postgres_mcp():
    """Test PostgreSQL MCP server by listing tables"""
    
    # First, get a session ID from the SSE endpoint
    print("Connecting to PostgreSQL MCP server...")
    
    try:
        # Connect to SSE endpoint to get session ID
        response = requests.get(
            'http://localhost:9006/sse',
            headers={'Accept': 'text/event-stream'},
            stream=True,
            timeout=10
        )
        
        session_id = None
        for line in response.iter_lines(decode_unicode=True):
            if line and 'session_id=' in line:
                session_id = line.split('session_id=')[1]
                break
        
        if not session_id:
            print("Could not get session ID")
            return
            
        print(f"Got session ID: {session_id}")
        
        # Initialize the MCP connection
        init_message = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "resources": {},
                    "tools": {}
                },
                "clientInfo": {
                    "name": "ai-dev-local",
                    "version": "1.0.0"
                }
            }
        }
        
        print("Initializing MCP connection...")
        init_response = requests.post(
            f'http://localhost:9006/messages/?session_id={session_id}',
            headers={'Content-Type': 'application/json'},
            json=init_message,
            timeout=10
        )
        
        print(f"Initialization response: {init_response.status_code}")
        if init_response.status_code == 200:
            print(f"Response: {init_response.text}")
        
        # List available tools
        tools_message = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("Getting available tools...")
        tools_response = requests.post(
            f'http://localhost:9006/messages/?session_id={session_id}',
            headers={'Content-Type': 'application/json'},
            json=tools_message,
            timeout=10
        )
        
        print(f"Tools response: {tools_response.status_code}")
        if tools_response.status_code == 200:
            print(f"Available tools: {tools_response.text}")
        
        # Call list_tables tool
        list_tables_message = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "list_tables",
                "arguments": {}
            }
        }
        
        print("Calling list_tables tool...")
        tables_response = requests.post(
            f'http://localhost:9006/messages/?session_id={session_id}',
            headers={'Content-Type': 'application/json'},
            json=list_tables_message,
            timeout=10
        )
        
        print(f"List tables response: {tables_response.status_code}")
        if tables_response.status_code == 200:
            result = tables_response.json()
            print(f"Tables result: {json.dumps(result, indent=2)}")
        else:
            print(f"Error: {tables_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_postgres_mcp()
