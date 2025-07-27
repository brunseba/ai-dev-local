#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration
MCP_COMPOSE_FILE="$PROJECT_ROOT/docker-compose.mcp.yml"
ENV_FILE="$PROJECT_ROOT/.env"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
}

# Function to check if environment file exists
check_env_file() {
    if [[ ! -f "$ENV_FILE" ]]; then
        print_warning "Environment file not found. Creating from template..."
        cp "$PROJECT_ROOT/.env.example" "$ENV_FILE"
        print_status "Please edit $ENV_FILE with your configuration"
    fi
}

# Function to start MCP servers
start_mcp() {
    print_status "Starting MCP servers..."
    
    check_docker
    check_env_file
    
    # Start MCP services
    docker-compose -f "$MCP_COMPOSE_FILE" --env-file "$ENV_FILE" up -d
    
    print_success "MCP servers started successfully!"
    print_status "MCP Gateway available at: http://localhost:9000"
    print_status "Individual servers:"
    print_status "  - Git Server: http://localhost:9001"
    print_status "  - Filesystem Server: http://localhost:9002" 
    print_status "  - Fetch Server: http://localhost:9003"
    print_status "  - Memory Server: http://localhost:9004"
    print_status "  - Time Server: http://localhost:9005"
    print_status "  - Everything Server: http://localhost:9007"
    print_status "  - GitHub Server: http://localhost:9008"
    print_status "  - GitLab Server: http://localhost:9009"
    print_status "  - SonarQube Server: http://localhost:9010"
}

# Function to stop MCP servers
stop_mcp() {
    print_status "Stopping MCP servers..."
    
    docker-compose -f "$MCP_COMPOSE_FILE" down
    
    print_success "MCP servers stopped successfully!"
}

# Function to restart MCP servers
restart_mcp() {
    print_status "Restarting MCP servers..."
    stop_mcp
    start_mcp
}

# Function to show MCP server status
status_mcp() {
    print_status "MCP Server Status:"
    echo
    
    # Check if MCP Gateway is accessible
    if curl -s http://localhost:9000/health >/dev/null 2>&1; then
        print_success "MCP Gateway: Online"
        
        # Get server list from gateway
        echo
        print_status "MCP Servers:"
        curl -s http://localhost:9000/servers | python3 -m json.tool 2>/dev/null || echo "Unable to fetch server list"
    else
        print_warning "MCP Gateway: Offline"
    fi
    
    echo
    print_status "Docker Container Status:"
    docker-compose -f "$MCP_COMPOSE_FILE" ps
}

# Function to view MCP server logs
logs_mcp() {
    local service=${1:-}
    
    if [[ -n "$service" ]]; then
        print_status "Showing logs for MCP service: $service"
        docker-compose -f "$MCP_COMPOSE_FILE" logs -f "$service"
    else
        print_status "Showing logs for all MCP services:"
        docker-compose -f "$MCP_COMPOSE_FILE" logs -f
    fi
}

# Function to test MCP servers
test_mcp() {
    print_status "Testing MCP servers..."
    
    # Test MCP Gateway
    print_status "Testing MCP Gateway..."
    if curl -s http://localhost:9000/health | grep -q "healthy"; then
        print_success "MCP Gateway: OK"
    else
        print_error "MCP Gateway: FAILED"
    fi
    
    # Test individual servers through gateway
    local servers=("git" "filesystem" "fetch" "memory" "time")
    
    for server in "${servers[@]}"; do
        print_status "Testing $server server..."
        if curl -s "http://localhost:9000/servers/$server" | grep -q "name"; then
            print_success "$server server: OK"
        else
            print_warning "$server server: May not be ready yet"
        fi
    done
}

# Function to build MCP server images
build_mcp() {
    print_status "Building MCP server images..."
    
    check_docker
    
    docker-compose -f "$MCP_COMPOSE_FILE" build --no-cache
    
    print_success "MCP server images built successfully!"
}

# Function to clean up MCP resources
clean_mcp() {
    print_status "Cleaning up MCP resources..."
    
    # Stop and remove containers
    docker-compose -f "$MCP_COMPOSE_FILE" down -v --remove-orphans
    
    # Remove images
    local images=$(docker images --filter=reference="mcp/*" -q)
    if [[ -n "$images" ]]; then
        print_status "Removing MCP images..."
        docker rmi $images 2>/dev/null || true
    fi
    
    print_success "MCP resources cleaned up!"
}

# Function to show usage help
show_help() {
    echo "MCP Manager - Manage Model Context Protocol servers"
    echo
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo
    echo "Commands:"
    echo "  start          Start MCP servers"
    echo "  stop           Stop MCP servers"
    echo "  restart        Restart MCP servers"
    echo "  status         Show MCP server status"
    echo "  logs [SERVICE] Show logs (optionally for specific service)"
    echo "  test           Test MCP server connectivity"
    echo "  build          Build MCP server images"
    echo "  clean          Clean up MCP resources"
    echo "  help           Show this help message"
    echo
    echo "Examples:"
    echo "  $0 start                    # Start all MCP servers"
    echo "  $0 logs mcp-git            # Show logs for Git server"
    echo "  $0 status                  # Check server status"
    echo "  $0 test                    # Test all servers"
    echo
}

# Main command handler
main() {
    local command=${1:-help}
    
    case $command in
        start)
            start_mcp
            ;;
        stop)
            stop_mcp
            ;;
        restart)
            restart_mcp
            ;;
        status)
            status_mcp
            ;;
        logs)
            logs_mcp "$2"
            ;;
        test)
            test_mcp
            ;;
        build)
            build_mcp
            ;;
        clean)
            clean_mcp
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $command"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
