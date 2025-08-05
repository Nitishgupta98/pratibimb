#!/bin/bash

# Pratibimb RAI Integration - Quick Start Guide
# This script helps you get started with the RAI-integrated pipeline

echo "🌟 Pratibimb RAI Integration - Quick Start"
echo "=========================================="

# Check if we're in the right directory
if [ ! -f "modular_pipeline.py" ]; then
    echo "❌ Please run this script from the API directory"
    echo "   cd /path/to/pratibimb/API"
    exit 1
fi

# Check Python version
echo "🐍 Checking Python version..."
python3 --version

# Check dependencies
echo "📦 Checking dependencies..."
if python3 -c "import fastapi, uvicorn" 2>/dev/null; then
    echo "✅ FastAPI and Uvicorn available"
else
    echo "❌ FastAPI/Uvicorn not available"
    echo "   Install with: pip3 install fastapi uvicorn"
    exit 1
fi

# Test module import
echo "🔧 Testing module import..."
python3 -c "import modular_pipeline; print('✅ Pipeline module imports successfully')"

# Check RAI availability
echo "🛡️  Checking RAI availability..."
if python3 -c "from RAI.rai_middleware import RAIContentAnalyzer" 2>/dev/null; then
    echo "✅ RAI modules available"
    RAI_STATUS="available"
else
    echo "⚠️  RAI modules not fully available (will use fallback mode)"
    RAI_STATUS="fallback"
fi

echo ""
echo "📋 Setup Summary:"
echo "   ✅ Python 3.x installed"
echo "   ✅ FastAPI/Uvicorn available"
echo "   ✅ Pipeline module ready"
echo "   ${RAI_STATUS} RAI modules ${RAI_STATUS}"

echo ""
echo "🚀 Starting the modular pipeline server..."
echo "   URL: http://localhost:8001"
echo "   API Docs: http://localhost:8001/docs"
echo ""

# Start server
echo "💡 Press Ctrl+C to stop the server"
echo ""

uvicorn modular_pipeline:app --host 0.0.0.0 --port 8001 --reload
