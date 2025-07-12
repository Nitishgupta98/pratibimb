# 🌟 PRATIBIMB - macOS Setup Guide

**True Reflection of Digital World** - AI-powered Braille conversion system

## 🚀 Quick Start (One-Command Setup)

```bash
# Make setup script executable and run
chmod +x setup_complete_macos.sh
./setup_complete_macos.sh
```

## 📋 Prerequisites

### Required Software
- **macOS 10.15+** (Catalina or later)
- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)

### Installation Options

#### Python Installation:
```bash
# Option 1: Official installer
# Download from https://www.python.org/downloads/

# Option 2: Homebrew
brew install python

# Option 3: pyenv (recommended for multiple versions)
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0
```

#### Node.js Installation:
```bash
# Option 1: Official installer
# Download from https://nodejs.org/

# Option 2: Homebrew
brew install node

# Option 3: nvm (recommended for multiple versions)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
nvm use --lts
```

## 🔧 Manual Setup (Step by Step)

### 1. Setup API Backend
```bash
cd API
chmod +x setup_macos.sh
./setup_macos.sh
```

### 2. Setup UI Frontend
```bash
cd UI
chmod +x setup_ui_macos.sh
./setup_ui_macos.sh
```

### 3. Configure Google API Key
```bash
cd API
nano config.json
# Update the "api_key" field with your actual Google API key
```

## 🚀 Running the Application

### Option A: Start Everything Together
```bash
./start_all_macos.sh
```

### Option B: Start Servers Separately
```bash
# Terminal 1 (API Server)
cd API
./start_server_macos.sh

# Terminal 2 (UI Development Server)
cd UI
./start_dev_macos.sh
```

## 🌐 Access URLs

- **Frontend Application**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **API Interactive Docs**: http://localhost:8000/redoc

## 🛑 Stopping the Application

```bash
# Stop all services
./stop_all_macos.sh

# Or press Ctrl+C in the terminal running the servers
```

## 📁 Project Structure

```
pratibimb-main/
├── API/                          # Backend Python FastAPI
│   ├── setup_macos.sh           # API setup script
│   ├── start_server_macos.sh    # API start script
│   ├── main.py                  # Main API server
│   ├── pratibimb.py            # Braille conversion engine
│   ├── config.json             # Configuration file
│   ├── requirements.txt        # Python dependencies
│   └── ...
├── UI/                          # Frontend React
│   ├── setup_ui_macos.sh       # UI setup script
│   ├── start_dev_macos.sh      # UI start script
│   ├── package.json            # Node.js dependencies
│   ├── src/                    # React source code
│   └── ...
├── setup_complete_macos.sh     # Complete setup script
├── start_all_macos.sh          # Start all services
├── stop_all_macos.sh           # Stop all services
└── README_MACOS.md             # This file
```

## 🔧 Configuration

### Google API Key Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Generative AI API
4. Create an API key
5. Update `API/config.json`:
```json
{
  "google": {
    "api_key": "YOUR_ACTUAL_API_KEY_HERE"
  }
}
```

## 🐛 Troubleshooting

### Common Issues

#### Permission Denied
```bash
chmod +x *.sh
```

#### Python Not Found
```bash
# Check Python installation
python3 --version
which python3

# If not found, install Python
brew install python
```

#### Node.js/npm Not Found
```bash
# Check Node.js installation
node --version
npm --version

# If not found, install Node.js
brew install node
```

#### Port Already in Use
```bash
# Kill processes using ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

#### React Dependencies Issues
```bash
cd UI
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --legacy-peer-deps
```

#### Python Dependencies Issues
```bash
cd API
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Log Files
- API logs: `API/logs/pratibimb.log`
- API request logs: `API/logs/requests/`
- Startup logs: `api.log` (when using start_all_macos.sh)

## 🆘 Getting Help

1. **Check logs** in the respective directories
2. **Verify prerequisites** are installed correctly
3. **Ensure ports 3000 and 8000** are available
4. **Check Google API key** is valid and has proper permissions

## 🌟 Features

- **YouTube Video Processing**: Extract and enhance transcripts
- **AI-Powered Enhancement**: Optimize content for blind users
- **Braille Conversion**: Generate Grade 1 Braille output
- **Real-time Progress**: Live progress tracking with animations
- **Multiple Formats**: Unicode Braille and embosser-ready BRF files
- **Responsive UI**: Works on all screen sizes

## 📱 Browser Compatibility

- **Chrome 90+** ✅
- **Firefox 88+** ✅
- **Safari 14+** ✅
- **Edge 90+** ✅

---

🌟 **Pratibimb** - Making digital content accessible for everyone!
