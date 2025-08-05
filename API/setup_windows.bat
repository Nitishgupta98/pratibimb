@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo 🌟 PRATIBIMB - True Reflection of Digital World 🌟
echo Complete Windows Setup for Pratibimb API
echo ============================================================

echo 📋 Starting Windows setup process...
echo.

REM Step 1: Check for Python
echo 📋 Step 1: Checking Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Python not found. Please install Python 3.11+ from python.org
    echo Opening Python download page...
    start https://www.python.org/downloads/
    echo Please install Python and run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Python is already installed
)

REM Step 2: Check for pip and upgrade
echo 📋 Step 2: Upgrading pip
python -m pip install --upgrade pip
echo ✅ Pip upgraded

REM Step 3: Install Git (if not present)
echo 📋 Step 3: Checking Git installation
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Git not found. Please install Git from git-scm.com
    start https://git-scm.com/download/win
    echo Please install Git and run this script again.
    pause
    exit /b 1
) else (
    echo ✅ Git is already installed
)

REM Step 4: Check FFmpeg
echo 📋 Step 4: Checking FFmpeg installation
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  FFmpeg not found. Please install FFmpeg:
    echo 1. Download from: https://www.gyan.dev/ffmpeg/builds/
    echo 2. Extract to C:\ffmpeg
    echo 3. Add C:\ffmpeg\bin to your PATH
    start https://www.gyan.dev/ffmpeg/builds/
    echo Please install FFmpeg and run this script again.
    pause
    exit /b 1
) else (
    echo ✅ FFmpeg is already installed
)

REM Step 5: Create virtual environment
echo 📋 Step 5: Creating Python virtual environment
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Step 6: Install Python dependencies
echo 📋 Step 6: Installing Python dependencies
if exist "requirements.txt" (
    pip install -r requirements.txt
    echo ✅ Python dependencies installed
) else (
    echo ❌ requirements.txt not found!
    pause
    exit /b 1
)

REM Step 7: Install PyTorch
echo 📋 Step 7: Installing PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
echo ✅ PyTorch installed for CPU

REM Step 8: Setup environment file
echo 📋 Step 8: Setting up environment configuration
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo ✅ Environment file created from template
        echo ⚠️  Please edit .env file with your API keys
    ) else (
        echo # Pratibimb API Environment Variables > .env
        echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
        echo API_HOST=0.0.0.0 >> .env
        echo API_PORT=8000 >> .env
        echo ✅ Basic .env file created
        echo ⚠️  Please edit .env file with your actual API keys
    )
) else (
    echo ✅ Environment file already exists
)

REM Step 9: Create necessary directories
echo 📋 Step 9: Creating necessary directories
if not exist "logs" mkdir logs
if not exist "output" mkdir output
if not exist "reports" mkdir reports
if not exist "rai_reports" mkdir rai_reports
echo ✅ Directories created

REM Step 10: Test installation
echo 📋 Step 10: Testing installation
python -c "
import sys
print('Python version:', sys.version.split()[0])
try:
    import fastapi; print('✅ FastAPI: OK')
except: print('❌ FastAPI: Failed')
try:
    import uvicorn; print('✅ Uvicorn: OK')
except: print('❌ Uvicorn: Failed')
try:
    import torch; print('✅ PyTorch: OK')
except: print('❌ PyTorch: Failed')
try:
    import cv2; print('✅ OpenCV: OK')
except: print('❌ OpenCV: Failed')
"

echo.
echo ============================================================
echo 🎉 SETUP COMPLETE! 🎉
echo ============================================================
echo 📋 What was set up:
echo    • Python virtual environment
echo    • All Python dependencies
echo    • PyTorch for AI/ML capabilities
echo    • Environment configuration
echo.
echo 🚀 To start the API server:
echo    start_api.bat
echo.
echo 📖 To view API documentation:
echo    http://localhost:8000/docs (after starting server)
echo.
echo ⚙️  Important:
echo    • Edit .env file with your API keys
echo    • GEMINI_API_KEY is required for AI features
echo.
echo 🌟 Pratibimb API is ready to use! 🌟
echo ============================================================

pause
