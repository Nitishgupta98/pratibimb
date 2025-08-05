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
echo "Starting API Server on macOS..."
echo "============================================================"

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

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found!"
    echo "Please run setup_macos.sh first"
    exit 1
fi

# Activate virtual environment
print_step "🔧 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi
print_success "Virtual environment activated"

# Create output directories if needed
print_step "📁 Ensuring output directories exist..."
mkdir -p Output_files
mkdir -p output
mkdir -p logs/requests
mkdir -p reports

# Check if config.json exists and has API key
print_step "⚙️  Checking configuration..."
if [ ! -f "config.json" ]; then
    print_error "config.json not found!"
    echo "Please run setup_macos.sh first"
    exit 1
fi

# Check if API key is configured
if grep -q "YOUR_GOOGLE_API_KEY_HERE" config.json; then
    print_warning "Google API key not configured in config.json"
    echo "Please update config.json with your actual Google API key"
    echo "The server will start but AI features may not work without a valid API key"
    echo ""
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi


# Check if main.py exists
if [ ! -f "main.py" ]; then
    print_error "main.py not found!"
    echo "Please ensure you're in the correct API directory"
    exit 1
fi


print_step "🚀 Starting Modular Pipeline API server..."
echo ""
echo "============================================================"
echo -e "${GREEN}📍 Modular Pipeline API will be available at: http://localhost:8001${NC}"
echo -e "${GREEN}📖 API Documentation: http://localhost:8001/docs${NC}"
echo -e "${BLUE}🔧 Modular endpoints: See main.py for full list${NC}"
echo "============================================================"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

# Start the modular pipeline server
uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4

# Deactivate virtual environment when done
deactivate
