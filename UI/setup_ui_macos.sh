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
echo "Setting up UI Environment on macOS..."
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
print_step "🔍 Checking Node.js installation..."
if ! command_exists node; then
    print_error "Node.js is not installed!"
    echo -e "${YELLOW}Please install Node.js using one of the following methods:${NC}"
    echo "1. Download from https://nodejs.org/"
    echo "2. Install via Homebrew: brew install node"
    echo "3. Install via nvm: nvm install --lts"
    echo "4. Install via fnm: fnm install --lts"
    exit 1
fi

NODE_VERSION=$(node --version 2>&1)
print_success "Found Node.js $NODE_VERSION"

# Check Node.js version (should be >= 16)
NODE_MAJOR_VERSION=$(node --version | cut -d'.' -f1 | sed 's/v//')
if [ "$NODE_MAJOR_VERSION" -lt 16 ]; then
    print_warning "Node.js version $NODE_VERSION is quite old. Recommended: >= 16.0.0"
    echo "Consider upgrading for better compatibility"
fi

# Check if npm is available
print_step "🔍 Checking npm installation..."
if ! command_exists npm; then
    print_error "npm is not available!"
    echo "npm should come with Node.js. Please reinstall Node.js"
    exit 1
fi

NPM_VERSION=$(npm --version 2>&1)
print_success "Found npm $NPM_VERSION"

# Clean previous installations
print_step "🧹 Cleaning previous installations..."
if [ -d "node_modules" ]; then
    print_warning "Removing existing node_modules..."
    rm -rf node_modules
fi

if [ -f "package-lock.json" ]; then
    print_warning "Removing existing package-lock.json..."
    rm package-lock.json
fi

# Clear npm cache
print_step "🗑️  Clearing npm cache..."
npm cache clean --force

# Install dependencies
print_step "📥 Installing React dependencies..."
npm install
if [ $? -ne 0 ]; then
    print_error "Failed to install dependencies with npm"
    print_step "Trying with npm install --legacy-peer-deps..."
    npm install --legacy-peer-deps
    if [ $? -ne 0 ]; then
        print_error "Failed to install dependencies"
        print_step "Trying manual installation of core packages..."
        npm install react@^18.2.0 react-dom@^18.2.0 react-scripts@5.0.1 lucide-react@^0.263.1
        if [ $? -ne 0 ]; then
            print_error "Manual package installation failed"
            exit 1
        fi
    fi
fi
print_success "Dependencies installed successfully"

# Create public directory if it doesn't exist
print_step "📁 Setting up public directory..."
if [ ! -d "public" ]; then
    mkdir -p public
fi

# Create index.html if it doesn't exist
if [ ! -f "public/index.html" ]; then
    print_step "📄 Creating index.html..."
    cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <link rel="icon" href="%PUBLIC_URL%/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#000000" />
    <meta
      name="description"
      content="Pratibimb - True Reflection of Digital World - AI-powered Braille conversion system"
    />
    <title>Pratibimb - Braille Converter</title>
  </head>
  <body>
    <noscript>You need to enable JavaScript to run this app.</noscript>
    <div id="root"></div>
  </body>
</html>
EOF
    print_success "Created index.html"
fi

# Create favicon if it doesn't exist
if [ ! -f "public/favicon.ico" ]; then
    print_step "🎨 Creating favicon..."
    # Create a simple text-based favicon placeholder
    echo "Creating simple favicon placeholder..."
    touch public/favicon.ico
    print_success "Created favicon placeholder"
fi

# Make the start script executable
if [ -f "start_dev_macos.sh" ]; then
    chmod +x start_dev_macos.sh
    print_success "start_dev_macos.sh made executable"
fi

# Check if src directory exists
if [ ! -d "src" ]; then
    print_error "src directory not found!"
    echo "Please ensure you're in the correct UI directory"
    exit 1
fi

# Verify React components exist
print_step "🔍 Verifying React components..."
if [ ! -f "src/App.js" ]; then
    print_error "src/App.js not found!"
    exit 1
fi

if [ ! -f "src/index.js" ]; then
    print_error "src/index.js not found!"
    exit 1
fi

print_success "React components verified"

echo "============================================================"
print_success "UI Setup completed successfully!"
echo ""
echo -e "${BLUE}📝 Next steps:${NC}"
echo "1. Ensure the API server is running (in ../API directory)"
echo "2. Run: ${GREEN}./start_dev_macos.sh${NC} to start the development server"
echo "3. Or run: ${GREEN}npm start${NC}"
echo ""
echo -e "${BLUE}🔧 Development server will be available at:${NC} http://localhost:3000"
echo -e "${BLUE}📱 The app will automatically reload when you make changes${NC}"
echo "============================================================"
