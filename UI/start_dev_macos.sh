#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo "============================================================"
echo -e "${PURPLE}🌟 PRATIBIMB - True Reflection of Digital World 🌟${NC}"
echo "Starting UI Development Server on macOS..."
echo "============================================================"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print colored output
print_step() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check if Node.js is installed
if ! command_exists node; then
    print_error "Node.js is not installed!"
    echo "Please run setup_ui_macos.sh first"
    exit 1
fi

# Check if npm is available
if ! command_exists npm; then
    print_error "npm is not available!"
    echo "Please run setup_ui_macos.sh first"
    exit 1
fi

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    print_error "node_modules directory not found!"
    echo "Please run setup_ui_macos.sh first to install dependencies"
    exit 1
fi

# Check if package.json exists
if [ ! -f "package.json" ]; then
    print_error "package.json not found!"
    echo "Please ensure you're in the correct UI directory"
    exit 1
fi

# Verify React components exist
print_step "🔍 Verifying React application..."
if [ ! -f "src/App.js" ]; then
    print_error "src/App.js not found!"
    exit 1
fi

if [ ! -f "src/index.js" ]; then
    print_error "src/index.js not found!"
    exit 1
fi

print_success "React application verified"

# Check if API server is running
print_step "🔍 Checking if API server is running..."
if curl -s http://localhost:8000 > /dev/null 2>&1; then
    print_success "API server is running at http://localhost:8000"
else
    print_warning "API server is not running at http://localhost:8000"
    echo "Please start the API server first:"
    echo "  cd ../API"
    echo "  ./start_server_macos.sh"
    echo ""
    echo "The UI will still start, but API calls will fail until the server is running."
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

print_step "🚀 Starting React development server..."
echo ""
echo "============================================================"
echo -e "${GREEN}📍 Development server will be available at: http://localhost:3000${NC}"
echo -e "${GREEN}🔗 API server should be running at: http://localhost:8000${NC}"
echo -e "${BLUE}🔧 Features:${NC}"
echo "   • Hot reload - changes automatically refresh the browser"
echo "   • Error overlay - compilation errors shown in browser"
echo "   • Proxy to API - API calls automatically forwarded to :8000"
echo "============================================================"
echo ""
echo -e "${YELLOW}The browser will automatically open. Press Ctrl+C to stop.${NC}"
echo ""

# Set environment variable to suppress React warnings in development
export GENERATE_SOURCEMAP=false

# Start the development server
npm start

print_step "🛑 Development server stopped"
