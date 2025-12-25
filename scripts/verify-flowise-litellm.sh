#!/bin/bash
# Verification script for Flowise + LiteLLM integration
# Tests connectivity, authentication, and configuration

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Load environment variables from .env file
if [ -f .env ]; then
    LITELLM_MASTER_KEY=$(grep "^LITELLM_MASTER_KEY=" .env | cut -d= -f2)
    LITELLM_PORT=$(grep "^LITELLM_PORT=" .env | cut -d= -f2)
    FLOWISE_PORT=$(grep "^FLOWISE_PORT=" .env | cut -d= -f2)
    HOST=$(grep "^HOST=" .env | cut -d= -f2)
fi

# Set defaults if not found
LITELLM_MASTER_KEY=${LITELLM_MASTER_KEY:-"*******************"}
LITELLM_PORT=${LITELLM_PORT:-4000}
FLOWISE_PORT=${FLOWISE_PORT:-3001}
HOST=${HOST:-localhost}

echo "========================================"
echo "Flowise + LiteLLM Integration Verification"
echo "========================================"
echo ""

# Test 1: Check if LiteLLM is running
echo -e "${YELLOW}[1/7] Checking if LiteLLM is running...${NC}"
if docker compose ps litellm | grep -q "Up"; then
    echo -e "${GREEN}✓ LiteLLM container is running${NC}"
else
    echo -e "${RED}✗ LiteLLM container is not running${NC}"
    echo "Start it with: docker compose up -d litellm"
    exit 1
fi
echo ""

# Test 2: Check LiteLLM health (requires authentication)
echo -e "${YELLOW}[2/7] Testing LiteLLM health endpoint...${NC}"
HEALTH_CHECK=$(curl --connect-timeout 5 --max-time 10 -s -w "\n%{http_code}" \
    -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
    "http://${HOST}:${LITELLM_PORT}/health" 2>&1)

HTTP_CODE=$(echo "$HEALTH_CHECK" | tail -1)
RESPONSE_BODY=$(echo "$HEALTH_CHECK" | sed '$ d')

if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ LiteLLM health check passed${NC}"
    # Show summary of endpoints
    HEALTHY_COUNT=$(echo "$RESPONSE_BODY" | grep -o '"healthy_endpoints":[0-9]*' | cut -d: -f2)
    if [ -n "$HEALTHY_COUNT" ]; then
        echo "  Healthy endpoints: $HEALTHY_COUNT"
    fi
else
    echo -e "${RED}✗ LiteLLM health check failed (HTTP $HTTP_CODE)${NC}"
    echo "Check logs: docker compose logs litellm"
    exit 1
fi
echo ""

# Test 3: Test LiteLLM authentication
echo -e "${YELLOW}[3/7] Testing LiteLLM authentication...${NC}"
AUTH_RESPONSE=$(curl --connect-timeout 5 --max-time 10 -sf \
    -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
    "http://${HOST}:${LITELLM_PORT}/v1/models" 2>&1 || echo "FAILED")

if echo "$AUTH_RESPONSE" | grep -q "data"; then
    echo -e "${GREEN}✓ LiteLLM authentication successful${NC}"
else
    echo -e "${RED}✗ LiteLLM authentication failed${NC}"
    echo "Response: $AUTH_RESPONSE"
    echo "Check your LITELLM_MASTER_KEY in .env"
    exit 1
fi
echo ""

# Test 4: List available models
echo -e "${YELLOW}[4/7] Listing available models through LiteLLM...${NC}"
MODELS=$(curl --connect-timeout 5 --max-time 10 -sf \
    -H "Authorization: Bearer ${LITELLM_MASTER_KEY}" \
    "http://${HOST}:${LITELLM_PORT}/v1/models" | grep -o '"id":"[^"]*"' | cut -d'"' -f4 | head -10)

if [ -n "$MODELS" ]; then
    echo -e "${GREEN}✓ Available models:${NC}"
    echo "$MODELS" | while read -r model; do
        echo "  - $model"
    done
else
    echo -e "${RED}✗ Could not retrieve models${NC}"
    exit 1
fi
echo ""

# Test 5: Check if Flowise is running
echo -e "${YELLOW}[5/7] Checking if Flowise is running...${NC}"
if docker compose ps flowise | grep -q "Up"; then
    echo -e "${GREEN}✓ Flowise container is running${NC}"
else
    echo -e "${RED}✗ Flowise container is not running${NC}"
    echo "Start it with: docker compose up -d flowise"
    exit 1
fi
echo ""

# Test 6: Check Flowise environment variables
echo -e "${YELLOW}[6/7] Checking Flowise environment variables...${NC}"
FLOWISE_ENV=$(docker compose exec -T flowise env | grep -E "^OPENAI_API")

OPENAI_KEY=$(echo "$FLOWISE_ENV" | grep "OPENAI_API_KEY=" | cut -d'=' -f2)
OPENAI_BASE=$(echo "$FLOWISE_ENV" | grep "OPENAI_API_BASE=" | cut -d'=' -f2)

echo "  OPENAI_API_KEY: ${OPENAI_KEY:0:20}..."
echo "  OPENAI_API_BASE: $OPENAI_BASE"

if [ "$OPENAI_BASE" = "http://litellm:4000/v1" ]; then
    echo -e "${GREEN}✓ OPENAI_API_BASE is correctly configured${NC}"
else
    echo -e "${YELLOW}⚠ OPENAI_API_BASE should be: http://litellm:4000/v1${NC}"
    echo -e "${YELLOW}  Current value: $OPENAI_BASE${NC}"
fi

if [ "$OPENAI_KEY" = "$LITELLM_MASTER_KEY" ]; then
    echo -e "${GREEN}✓ OPENAI_API_KEY matches LITELLM_MASTER_KEY${NC}"
else
    echo -e "${YELLOW}⚠ OPENAI_API_KEY does not match LITELLM_MASTER_KEY${NC}"
fi
echo ""

# Test 7: Test connectivity from Flowise to LiteLLM
echo -e "${YELLOW}[7/7] Testing connectivity from Flowise to LiteLLM...${NC}"
FLOWISE_CURL=$(docker compose exec -T flowise curl --connect-timeout 5 --max-time 10 -sf http://litellm:4000/health 2>&1 || echo "FAILED")

if echo "$FLOWISE_CURL" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Flowise can reach LiteLLM proxy${NC}"
else
    echo -e "${RED}✗ Flowise cannot reach LiteLLM${NC}"
    echo "Response: $FLOWISE_CURL"
    echo "Check Docker network: docker network inspect ai-dev-local"
    exit 1
fi
echo ""

# Summary
echo "========================================"
echo -e "${GREEN}All checks passed!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Access Flowise: http://${HOST}:${FLOWISE_PORT}"
echo "2. Login with: admin / admin123"
echo "3. Create credential:"
echo "   - Name: LiteLLM Proxy"
echo "   - API Key: ${LITELLM_MASTER_KEY:0:20}..."
echo "4. In OpenAI nodes, set:"
echo "   - BasePath: http://litellm:4000"
echo "   - Model: gpt-3.5-turbo (or any model from the list above)"
echo ""
echo "For detailed setup instructions, see:"
echo "  docs/flowise-litellm-setup.md"
echo ""
