#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo "============================================================"
echo -e "${PURPLE}🌟 PRATIBIMB - True Reflection of Digital World 🌟${NC}"
echo -e "${CYAN}Complete macOS Setup Script${NC}"
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

print_header() {
    echo ""
    echo "============================================================"
    echo -e "${CYAN}$1${NC}"
    echo "============================================================"
}

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR"

print_step "📍 Project root: $PROJECT_ROOT"

# Setup API
print_header "🔧 Setting up API Backend"

if [ -d "$PROJECT_ROOT/API" ]; then
    cd "$PROJECT_ROOT/API"
    
    if [ -f "setup_macos.sh" ]; then
        chmod +x setup_macos.sh
        print_step "🚀 Running API setup..."
        ./setup_macos.sh
        API_SETUP_STATUS=$?
        
        if [ $API_SETUP_STATUS -eq 0 ]; then
            print_success "API setup completed successfully"
            
            # Make start script executable
            if [ -f "start_server_macos.sh" ]; then
                chmod +x start_server_macos.sh
            fi
        else
            print_error "API setup failed"
            exit 1
        fi
    else
        print_error "API setup script not found"
        exit 1
    fi
else
    print_error "API directory not found"
    exit 1
fi

# Setup UI
print_header "🎨 Setting up UI Frontend"

if [ -d "$PROJECT_ROOT/UI" ]; then
    cd "$PROJECT_ROOT/UI"
    
    if [ -f "setup_ui_macos.sh" ]; then
        chmod +x setup_ui_macos.sh
        print_step "🚀 Running UI setup..."
        ./setup_ui_macos.sh
        UI_SETUP_STATUS=$?
        
        if [ $UI_SETUP_STATUS -eq 0 ]; then
            print_success "UI setup completed successfully"
            
            # Make start script executable
            if [ -f "start_dev_macos.sh" ]; then
                chmod +x start_dev_macos.sh
            fi
        else
            print_error "UI setup failed"
            exit 1
        fi
    else
        print_error "UI setup script not found"
        exit 1
    fi
else
    print_error "UI directory not found"
    exit 1
fi

# Create convenience scripts
print_header "📝 Creating convenience scripts"

cd "$PROJECT_ROOT"

# Create start-all script
print_step "📝 Creating start-all script..."
cat > start_all_macos.sh << 'EOF'
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
EOF

chmod +x start_all_macos.sh
print_success "Created start_all_macos.sh"

# Create stop-all script
print_step "📝 Creating stop-all script..."
cat > stop_all_macos.sh << 'EOF'
#!/bin/bash

echo "🛑 Stopping all Pratibimb services..."

# Kill processes by port
echo "Stopping API server (port 8000)..."
lsof -ti:8000 | xargs kill -9 2>/dev/null

echo "Stopping UI server (port 3000)..."
lsof -ti:3000 | xargs kill -9 2>/dev/null

# Kill by process name
pkill -f "uvicorn main:app" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null

echo "✅ All services stopped"
EOF

chmod +x stop_all_macos.sh
print_success "Created stop_all_macos.sh"

# Final instructions
print_header "🎉 Setup Complete!"

echo -e "${GREEN}✅ API Backend setup completed${NC}"
echo -e "${GREEN}✅ UI Frontend setup completed${NC}"
echo -e "${GREEN}✅ Convenience scripts created${NC}"
echo ""
echo -e "${BLUE}📝 Next Steps:${NC}"
echo ""
echo -e "${YELLOW}1. Configure Google API Key:${NC}"
echo "   cd API"
echo "   nano config.json"
echo "   # Update the api_key field with your actual Google API key"
echo ""
echo -e "${YELLOW}2. Start the application:${NC}"
echo -e "   ${GREEN}Option A - Start everything together:${NC}"
echo "   ./start_all_macos.sh"
echo ""
echo -e "   ${GREEN}Option B - Start servers separately:${NC}"
echo "   # Terminal 1 (API):"
echo "   cd API && ./start_server_macos.sh"
echo "   # Terminal 2 (UI):"
echo "   cd UI && ./start_dev_macos.sh"
echo ""
echo -e "${YELLOW}3. Access the application:${NC}"
echo -e "   ${GREEN}🌐 Frontend:${NC} http://localhost:3000"
echo -e "   ${GREEN}🔧 Backend API:${NC} http://localhost:8000"
echo -e "   ${GREEN}📖 API Docs:${NC} http://localhost:8000/docs"
echo ""
echo -e "${YELLOW}4. Stop the application:${NC}"
echo "   ./stop_all_macos.sh"
echo "   # Or press Ctrl+C in the terminal running the servers"
echo ""
echo "============================================================"
echo -e "${PURPLE}🌟 Pratibimb is ready to bring digital accessibility! 🌟${NC}"
echo "============================================================"
