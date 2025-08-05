@echo off
setlocal enabledelayedexpansion

echo ============================================================
echo 🌟 PRATIBIMB API SERVER 🌟
echo Starting Pratibimb Modular Pipeline API...
echo ============================================================

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo 📁 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Using system Python.
    echo 💡 Run setup_windows.bat first to set up the environment properly.
)

REM Check if requirements are installed
echo 📦 Checking dependencies...
python -c "import fastapi, uvicorn" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing dependencies...
    pip install -r requirements.txt
)

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  No .env file found. Creating from template...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo 💡 Please edit .env file with your API keys before proceeding.
    )
)

REM Start the API server
echo 🚀 Starting API server on http://localhost:8000
echo 📖 API Documentation: http://localhost:8000/docs
echo ============================================================

uvicorn main:app --host 0.0.0.0 --port 8000 --reload
