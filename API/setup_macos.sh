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
echo "Setting up API Environment on macOS..."
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

# Check if Python is installed
print_step "🔍 Checking Python installation..."
if ! command_exists python3; then
    print_error "Python 3 is not installed!"
    echo -e "${YELLOW}Please install Python 3 using one of the following methods:${NC}"
    echo "1. Download from https://www.python.org/downloads/"
    echo "2. Install via Homebrew: brew install python"
    echo "3. Install via pyenv: pyenv install 3.11.0"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1)
print_success "Found $PYTHON_VERSION"

# Check if pip is available
print_step "🔍 Checking pip installation..."
if ! command_exists pip3; then
    print_error "pip3 is not available!"
    echo "Installing pip..."
    python3 -m ensurepip --upgrade
    if [ $? -ne 0 ]; then
        print_error "Failed to install pip"
        exit 1
    fi
fi
print_success "pip3 is available"

# Create virtual environment
print_step "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Removing..."
    rm -rf venv
fi

python3 -m venv venv
if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment"
    exit 1
fi
print_success "Virtual environment created"

# Activate virtual environment
print_step "🔧 Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    print_error "Failed to activate virtual environment"
    exit 1
fi
print_success "Virtual environment activated"

# Upgrade pip
print_step "⬆️  Upgrading pip..."
pip install --upgrade pip
if [ $? -ne 0 ]; then
    print_warning "Failed to upgrade pip, continuing anyway..."
fi

# Install dependencies from requirements.txt
print_step "📥 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies from requirements.txt"
        print_step "Trying manual installation..."
        pip install fastapi uvicorn[standard] pydantic youtube-transcript-api google-generativeai requests python-dotenv python-multipart
        if [ $? -ne 0 ]; then
            print_error "Manual package installation failed"
            exit 1
        fi
    fi
else
    print_warning "requirements.txt not found, installing packages manually..."
    pip install fastapi uvicorn[standard] pydantic youtube-transcript-api google-generativeai requests python-dotenv python-multipart
    if [ $? -ne 0 ]; then
        print_error "Package installation failed"
        exit 1
    fi
fi
print_success "Dependencies installed successfully"

# Create necessary directories
print_step "📁 Creating output directories..."
mkdir -p Output_files
mkdir -p output
mkdir -p logs/requests
mkdir -p reports
print_success "Directories created"

# Check if config.json exists
print_step "⚙️  Checking configuration..."
if [ ! -f "config.json" ]; then
    print_warning "config.json not found. Creating default configuration..."
    cat > config.json << 'EOF'
{
  "google": {
    "api_key": "YOUR_GOOGLE_API_KEY_HERE"
  },
  "output": {
    "folder": "Output_files",
    "raw_transcript_file": "raw_transcript.txt",
    "enhanced_transcript_file": "enhanced_transcript_for_braille.txt"
  },
  "logging_settings": {
    "log_file": "logs/pratibimb.log"
  }
}
EOF
    print_warning "Please update config.json with your Google API key!"
fi

# Make the start script executable
if [ -f "start_server.sh" ]; then
    chmod +x start_server.sh
    print_success "start_server.sh made executable"
fi

echo "============================================================"
print_success "Setup completed successfully!"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo "1. Update config.json with your Google API key"
echo "2. Run: ${GREEN}./start_server.sh${NC} to start the API server"
echo "3. Or run: ${GREEN}source venv/bin/activate && python main.py${NC}"
echo ""
echo -e "${BLUE}🔧 Server will be available at:${NC} http://localhost:8000"
echo -e "${BLUE}📖 API Documentation:${NC} http://localhost:8000/docs"
echo "============================================================"
