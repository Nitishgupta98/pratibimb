#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m'

echo "============================================================"
echo -e "${PURPLE}🌟 PRATIBIMB - Starting Complete Application 🌟${NC}"
echo "============================================================"

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Function to cleanup background processes
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    if [ ! -z "$API_PID" ]; then
        kill $API_PID 2>/dev/null
        echo -e "${GREEN}✅ API server stopped${NC}"
    fi
    if [ ! -z "$UI_PID" ]; then
        kill $UI_PID 2>/dev/null
        echo -e "${GREEN}✅ UI server stopped${NC}"
    fi
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo -e "${BLUE}🔧 Starting API server in background...${NC}"
cd "$SCRIPT_DIR/API"
./start_server_macos.sh > api.log 2>&1 &
API_PID=$!

echo -e "${BLUE}⏳ Waiting for API server to start...${NC}"
sleep 10

# Check if API server is running
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${GREEN}✅ API server is running at http://localhost:8000${NC}"
else
    echo -e "${RED}❌ API server failed to start${NC}"
    echo "Check api.log for details"
    cleanup
fi

echo -e "${BLUE}🎨 Starting UI development server...${NC}"
cd "$SCRIPT_DIR/UI"
./start_dev_macos.sh

# This will run when UI server stops
cleanup
