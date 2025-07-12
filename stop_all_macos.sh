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
