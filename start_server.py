#!/usr/bin/env python3
"""
🚀 Pratibimb Development Server
Starts both the FastAPI backend and serves the UI

Usage:
    python start_server.py

This will start:
- FastAPI server on http://localhost:8001
- UI served on http://localhost:3000 (or available port)
"""

import os
import sys
import time
import subprocess
import threading
import webbrowser
from pathlib import Path

def start_fastapi_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        # Install requirements if needed
        requirements_file = "requirements-api.txt"
        if os.path.exists(requirements_file):
            print("📦 Installing API dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], 
                         check=True, capture_output=True)
        
        # Start the FastAPI server
        subprocess.run([sys.executable, "-m", "uvicorn", "api:app", 
                       "--host", "0.0.0.0", "--port", "8001", "--reload"], 
                      check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start FastAPI server: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ uvicorn not found. Please install: pip install uvicorn fastapi")
        sys.exit(1)

def start_ui_server():
    """Start a simple HTTP server for the UI"""
    print("🌐 Starting UI server...")
    time.sleep(3)  # Wait for FastAPI to start
    
    try:
        ui_dir = Path("ui")
        if not ui_dir.exists():
            print("❌ UI directory not found")
            return
        
        os.chdir(ui_dir)
        
        # Try to use Python's built-in HTTP server
        import http.server
        import socketserver
        
        port = 3000
        max_attempts = 5
        
        for attempt in range(max_attempts):
            try:
                with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
                    print(f"✅ UI server running at http://localhost:{port}")
                    print(f"📖 API docs available at http://localhost:8001/docs")
                    
                    # Open browser
                    webbrowser.open(f"http://localhost:{port}")
                    
                    httpd.serve_forever()
                break
            except OSError:
                port += 1
                if attempt == max_attempts - 1:
                    print("❌ Could not find available port for UI server")
                    return
                
    except Exception as e:
        print(f"❌ Failed to start UI server: {e}")

def main():
    """Main function to coordinate server startup"""
    print("🔤 Pratibimb Development Environment")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("api.py"):
        print("❌ api.py not found. Please run from the project root directory.")
        sys.exit(1)
    
    if not os.path.exists("ui/index.html"):
        print("❌ UI files not found. Please ensure ui/index.html exists.")
        sys.exit(1)
    
    print("✅ Project files found")
    print("🔄 Starting servers...")
    
    try:
        # Start FastAPI server in a separate thread
        api_thread = threading.Thread(target=start_fastapi_server, daemon=True)
        api_thread.start()
        
        # Start UI server in main thread
        start_ui_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down servers...")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
