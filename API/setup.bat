@echo off
echo ============================================================
echo 🌟 PRATIBIMB - True Reflection of Digital World 🌟
echo Setting up API Environment...
echo ============================================================

echo 📦 Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment
    echo Please ensure Python is installed and added to PATH
    pause
    exit /b 1
)

echo 🔧 Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo 📥 Installing dependencies...
pip install fastapi uvicorn youtube-transcript-api google-generativeai requests python-dotenv
if %errorlevel% neq 0 (
    echo ❌ Failed to install packages
    echo Trying alternative installation...
    pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org fastapi uvicorn youtube-transcript-api google-generativeai requests python-dotenv
    if %errorlevel% neq 0 (
        echo ❌ Package installation failed
        pause
        exit /b 1
    )
)

echo 📁 Creating output directory...
if not exist "Output_files" mkdir Output_files

echo ============================================================
echo ✅ Setup completed successfully!
echo 🚀 Run start_server.bat to start the API server
echo ============================================================
pause
