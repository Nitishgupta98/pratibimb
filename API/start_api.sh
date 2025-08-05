#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "============================================================"
echo -e "${PURPLE}🌟 PRATIBIMB API SERVER 🌟${NC}"
echo "Starting Pratibimb Modular Pipeline API..."
echo "============================================================"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${BLUE}📁 Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️  No virtual environment found. Using system Python.${NC}"
    echo -e "${BLUE}💡 Run ./setup_macos.sh first to set up the environment properly.${NC}"
fi

# Check if requirements are installed
echo -e "${BLUE}📦 Checking dependencies...${NC}"
python3 -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    pip install -r requirements.txt
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  No .env file found. Creating from template...${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${YELLOW}💡 Please edit .env file with your API keys before proceeding.${NC}"
    fi
fi

# Start the API server
echo -e "${GREEN}🚀 Starting API server on http://localhost:8000${NC}"
echo -e "${GREEN}📖 API Documentation: http://localhost:8000/docs${NC}"
echo "============================================================"

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
