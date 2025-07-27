#!/usr/bin/env python3

import json
import subprocess
import sys

def send_mcp_message(message):
    """Send a JSON-RPC message to the MCP PostgreSQL server"""
    try:
        # Start the MCP server process
        process = subprocess.Popen(
            ['docker', 'exec', '-i', 'ai-dev-mcp-mcp-postgres-1', 'postgres-mcp', '--access-mode=restricted'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the message
        stdout, stderr = process.communicate(input=json.dumps(message) + '\n')
        
        if stderr:
            print(f"Error: {stderr}", file=sys.stderr)
        
        if stdout:
            try:
                return json.loads(stdout.strip())
            except json.JSONDecodeError:
                print(f"Raw output: {stdout}")
                return None
                
    except Exception as e:
        print(f"Exception: {e}", file=sys.stderr)
        return None

def main():
    print("Connecting to PostgreSQL MCP server...")
    
    # 1. Initialize the connection
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "clientInfo": {
                "name": "ai-dev-local",
                "version": "1.0.0"
            }
        }
    }
    
    print("Initializing connection...")
    response = send_mcp_message(init_message)
    if response:
        print(f"Initialize response: {json.dumps(response, indent=2)}")
    
    # 2. List available tools
    tools_message = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list"
    }
    
    print("\nListing available tools...")
    response = send_mcp_message(tools_message)
    if response:
        print(f"Tools response: {json.dumps(response, indent=2)}")
    
    # 3. Call list_tables tool
    list_tables_message = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "list_tables",
            "arguments": {}
        }
    }
    
    print("\nCalling list_tables tool...")
    response = send_mcp_message(list_tables_message)
    if response:
        print(f"List tables response: {json.dumps(response, indent=2)}")

if __name__ == "__main__":
    main()
