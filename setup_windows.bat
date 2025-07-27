@echo off
echo 🔧 Starting setup on Windows...

REM Check Python
python --version
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found. Please install Python 3.10 manually:
    echo https://www.python.org/downloads/release/python-31013/
    pause
    exit /b
)

REM Create virtual environment
echo 📦 Creating virtual environment (.venv)...
python -m venv .venv

REM Activate virtual environment
call .venv\Scripts\activate

REM Install packages from requirements.txt
echo 📦 Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Setup complete. Activate with: call .venv\Scripts\activate
pause
