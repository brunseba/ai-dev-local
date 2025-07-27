#!/usr/bin/env python3
"""
MCP Gateway - Central routing and management for MCP servers
"""

import os
import asyncio
import logging
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MCPServerInfo(BaseModel):
    name: str
    url: str
    status: str = "unknown"
    capabilities: List[str] = []

class MCPGateway:
    def __init__(self):
        self.servers: Dict[str, MCPServerInfo] = {}
        self.client = httpx.AsyncClient(timeout=30.0)
        self._load_servers()

    def _load_servers(self):
        """Load MCP servers from environment configuration"""
        servers_config = os.getenv("MCP_SERVERS", "")
        if not servers_config:
            logger.warning("No MCP_SERVERS configuration found")
            return

        for server_config in servers_config.split(","):
            if ":" not in server_config:
                continue
            
            name, url = server_config.split(":", 1)
            self.servers[name] = MCPServerInfo(name=name, url=url)
            logger.info(f"Registered MCP server: {name} -> {url}")

    async def health_check_server(self, server: MCPServerInfo) -> bool:
        """Check if an MCP server is healthy"""
        try:
            response = await self.client.get(f"{server.url}/health", timeout=5.0)
            server.status = "healthy" if response.status_code == 200 else "unhealthy"
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Health check failed for {server.name}: {e}")
            server.status = "unhealthy"
            return False

    async def discover_capabilities(self, server: MCPServerInfo):
        """Discover capabilities of an MCP server"""
        try:
            response = await self.client.get(f"{server.url}/capabilities")
            if response.status_code == 200:
                data = response.json()
                server.capabilities = data.get("capabilities", [])
        except Exception as e:
            logger.warning(f"Failed to discover capabilities for {server.name}: {e}")

    async def route_request(self, server_name: str, path: str, method: str, **kwargs) -> Dict[str, Any]:
        """Route a request to a specific MCP server"""
        if server_name not in self.servers:
            raise HTTPException(status_code=404, detail=f"MCP server '{server_name}' not found")

        server = self.servers[server_name]
        url = f"{server.url}/{path.lstrip('/')}"

        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            
            if response.headers.get("content-type", "").startswith("application/json"):
                return response.json()
            else:
                return {"content": response.text, "content_type": response.headers.get("content-type")}
                
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            logger.error(f"Request to {server_name} failed: {e}")
            raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    async def refresh_server_status(self):
        """Refresh status and capabilities for all servers"""
        tasks = []
        for server in self.servers.values():
            tasks.extend([
                self.health_check_server(server),
                self.discover_capabilities(server)
            ])
        
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)

# Initialize gateway
gateway = MCPGateway()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting MCP Gateway...")
    await gateway.refresh_server_status()
    
    # Background task for periodic health checks
    async def periodic_health_check():
        while True:
            await asyncio.sleep(60)  # Check every minute
            await gateway.refresh_server_status()
    
    task = asyncio.create_task(periodic_health_check())
    
    yield
    
    # Shutdown
    task.cancel()
    await gateway.client.aclose()
    logger.info("MCP Gateway stopped")

# FastAPI app
app = FastAPI(
    title="MCP Gateway",
    description="Central routing and management for Model Context Protocol servers",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health():
    """Gateway health check"""
    return {"status": "healthy", "gateway": "mcp-gateway", "version": "1.0.0"}

@app.get("/servers")
async def list_servers():
    """List all registered MCP servers"""
    return {
        "servers": {name: server.dict() for name, server in gateway.servers.items()},
        "total": len(gateway.servers)
    }

@app.get("/servers/{server_name}")
async def get_server_info(server_name: str):
    """Get information about a specific MCP server"""
    if server_name not in gateway.servers:
        raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
    
    return gateway.servers[server_name].dict()

@app.post("/servers/{server_name}/refresh")
async def refresh_server(server_name: str):
    """Refresh status and capabilities for a specific server"""
    if server_name not in gateway.servers:
        raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
    
    server = gateway.servers[server_name]
    await gateway.health_check_server(server)
    await gateway.discover_capabilities(server)
    
    return server.dict()

@app.api_route("/mcp/{server_name}/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_to_mcp_server(server_name: str, path: str, request: Request):
    """Proxy requests to MCP servers"""
    # Get request data
    query_params = dict(request.query_params)
    headers = dict(request.headers)
    
    # Remove hop-by-hop headers
    headers.pop("host", None)
    headers.pop("connection", None)
    
    kwargs = {
        "params": query_params,
        "headers": headers,
    }
    
    # Add body for POST/PUT/PATCH requests
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        if body:
            kwargs["content"] = body
    
    try:
        result = await gateway.route_request(
            server_name=server_name,
            path=path,
            method=request.method,
            **kwargs
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in proxy: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/")
async def root():
    """Gateway information"""
    return {
        "service": "MCP Gateway",
        "version": "1.0.0",
        "servers": len(gateway.servers),
        "endpoints": {
            "health": "/health",
            "servers": "/servers",
            "proxy": "/mcp/{server_name}/{path}"
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("GATEWAY_PORT", 8080))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        access_log=True
    )
