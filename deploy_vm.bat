@echo off
setlocal enabledelayedexpansion

REM ============================================================
REM 🌟 PRATIBIMB - True Reflection of Digital World 🌟
REM Complete Windows VM Deployment Script
REM ============================================================

echo.
echo ============================================================
echo 🌟 PRATIBIMB - VM Deployment Starting...
echo ============================================================
echo.

REM Get the directory where this batch file is located
set "PROJECT_ROOT=%~dp0"
set "API_DIR=%PROJECT_ROOT%API"
set "UI_DIR=%PROJECT_ROOT%UI"

echo 📁 Project Root: %PROJECT_ROOT%
echo 📁 API Directory: %API_DIR%
echo 📁 UI Directory: %UI_DIR%
echo.

REM ============================================================
REM Step 1: Check Prerequisites
REM ============================================================
echo 🔍 Step 1: Checking Prerequisites...
echo ============================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)
echo ✅ Python is installed

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and add it to PATH
    pause
    exit /b 1
)
echo ✅ Node.js is installed

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed or not in PATH
    pause
    exit /b 1
)
echo ✅ npm is installed

echo.

REM ============================================================
REM Step 2: Get VM Network Configuration
REM ============================================================
echo 🌐 Step 2: Network Configuration
echo ============================================================

REM Get local IP address
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "VM_IP=%%i"
    goto :found_ip
)

:found_ip
REM Clean up the IP (remove spaces)
set "VM_IP=%VM_IP: =%"

if "%VM_IP%"=="" (
    echo ⚠️  Could not auto-detect IP address
    set /p VM_IP="Enter your VM IP address (e.g., 192.168.1.100): "
) else (
    echo 🔍 Auto-detected VM IP: %VM_IP%
    set /p "USER_IP=Is this correct? Press Enter to use %VM_IP% or type a different IP: "
    if not "%USER_IP%"=="" set "VM_IP=%USER_IP%"
)

echo ✅ Using VM IP: %VM_IP%
echo.

REM ============================================================
REM Step 3: Configure Windows Firewall
REM ============================================================
echo 🔥 Step 3: Configuring Windows Firewall...
echo ============================================================

echo 🔓 Adding firewall rules for ports 8000 (API) and 3000 (UI)...

REM Remove existing rules (if any)
netsh advfirewall firewall delete rule name="Pratibimb API Server" >nul 2>&1
netsh advfirewall firewall delete rule name="Pratibimb UI Server" >nul 2>&1

REM Add new firewall rules
netsh advfirewall firewall add rule name="Pratibimb API Server" dir=in action=allow protocol=TCP localport=8000
if %errorlevel% neq 0 (
    echo ⚠️  Failed to add firewall rule for port 8000. You may need to run as Administrator.
) else (
    echo ✅ Firewall rule added for port 8000
)

netsh advfirewall firewall add rule name="Pratibimb UI Server" dir=in action=allow protocol=TCP localport=3000
if %errorlevel% neq 0 (
    echo ⚠️  Failed to add firewall rule for port 3000. You may need to run as Administrator.
) else (
    echo ✅ Firewall rule added for port 3000
)

echo.

REM ============================================================
REM Step 4: Setup Python Virtual Environment and API
REM ============================================================
echo 🐍 Step 4: Setting up Python API...
echo ============================================================

cd /d "%API_DIR%"
if %errorlevel% neq 0 (
    echo ❌ Could not find API directory: %API_DIR%
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating Python virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install Python dependencies
echo 📥 Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)
echo ✅ Python dependencies installed

REM Create necessary directories
echo 📁 Creating output directories...
if not exist "logs\requests" mkdir "logs\requests"
if not exist "output" mkdir "output"
if not exist "Output_files" mkdir "Output_files"
if not exist "reports" mkdir "reports"
echo ✅ Output directories created

echo.

REM ============================================================
REM Step 5: Setup Node.js UI
REM ============================================================
echo ⚛️ Step 5: Setting up React UI...
echo ============================================================

cd /d "%UI_DIR%"
if %errorlevel% neq 0 (
    echo ❌ Could not find UI directory: %UI_DIR%
    pause
    exit /b 1
)

REM Install Node.js dependencies
echo 📥 Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)
echo ✅ Node.js dependencies installed

REM Create environment configuration
echo 🔧 Creating environment configuration...
(
echo # Pratibimb VM Deployment Configuration
echo REACT_APP_ENVIRONMENT=vm
echo REACT_APP_API_URL=http://%VM_IP%:8000
echo REACT_APP_VM_DEPLOYMENT=true
echo GENERATE_SOURCEMAP=false
) > .env

echo ✅ Environment configuration created (.env^)
echo 📍 API URL configured as: http://%VM_IP%:8000

echo.

REM ============================================================
REM Step 6: Build UI for Production
REM ============================================================
echo 🏗️ Step 6: Building React UI for production...
echo ============================================================

npm run build
if %errorlevel% neq 0 (
    echo ❌ Failed to build React UI
    pause
    exit /b 1
)
echo ✅ React UI built successfully

echo.

REM ============================================================
REM Step 7: Create Service Scripts
REM ============================================================
echo 🛠️ Step 7: Creating service scripts...
echo ============================================================

cd /d "%PROJECT_ROOT%"

REM Create API service script
(
echo @echo off
echo echo ============================================================
echo echo 🌟 PRATIBIMB API Server - Starting...
echo echo ============================================================
echo echo 📍 Server URL: http://%VM_IP%:8000
echo echo 📖 API Documentation: http://%VM_IP%:8000/docs
echo echo ============================================================
echo echo.
echo cd /d "%API_DIR%"
echo call venv\Scripts\activate.bat
echo python main.py
echo pause
) > start_api.bat

REM Create UI service script
(
echo @echo off
echo echo ============================================================
echo echo ⚛️ PRATIBIMB UI Server - Starting...
echo echo ============================================================
echo echo 📍 UI URL: http://%VM_IP%:3000
echo echo 🔗 API URL: http://%VM_IP%:8000
echo echo ============================================================
echo echo.
echo cd /d "%UI_DIR%"
echo npm start
echo pause
) > start_ui.bat

REM Create production UI service script
(
echo @echo off
echo echo ============================================================
echo echo ⚛️ PRATIBIMB UI Production Server - Starting...
echo echo ============================================================
echo echo 📍 UI URL: http://%VM_IP%:3000
echo echo 🔗 API URL: http://%VM_IP%:8000
echo echo ============================================================
echo echo.
echo cd /d "%UI_DIR%"
echo npx serve -s build -l 3000
echo pause
) > start_ui_production.bat

REM Create combined service script
(
echo @echo off
echo setlocal
echo echo ============================================================
echo echo 🌟 PRATIBIMB - Starting All Services
echo echo ============================================================
echo echo 🚀 Starting API Server in background...
echo start "Pratibimb API" "%PROJECT_ROOT%start_api.bat"
echo echo ⏳ Waiting 5 seconds for API to start...
echo timeout /t 5 /nobreak ^>nul
echo echo 🚀 Starting UI Production Server...
echo start "Pratibimb UI" "%PROJECT_ROOT%start_ui_production.bat"
echo echo.
echo echo ============================================================
echo echo ✅ Both services are starting...
echo echo 📍 UI: http://%VM_IP%:3000
echo echo 📍 API: http://%VM_IP%:8000
echo echo 📖 API Docs: http://%VM_IP%:8000/docs
echo echo ============================================================
echo echo.
echo echo Press any key to exit...
echo pause ^>nul
) > start_all_services.bat

REM Create stop services script
(
echo @echo off
echo echo ============================================================
echo echo 🛑 PRATIBIMB - Stopping All Services
echo echo ============================================================
echo taskkill /f /im python.exe /t ^>nul 2^>^&1
echo taskkill /f /im node.exe /t ^>nul 2^>^&1
echo taskkill /f /im npm.exe /t ^>nul 2^>^&1
echo echo ✅ All services stopped
echo echo ============================================================
echo pause
) > stop_all_services.bat

echo ✅ Service scripts created:
echo    - start_api.bat (API server only)
echo    - start_ui.bat (UI development server)
echo    - start_ui_production.bat (UI production server)
echo    - start_all_services.bat (both services)
echo    - stop_all_services.bat (stop all services)

echo.

REM ============================================================
REM Step 8: Test Deployment
REM ============================================================
echo 🧪 Step 8: Testing deployment...
echo ============================================================

echo 🔍 Testing if all files are in place...

if not exist "%API_DIR%\main.py" (
    echo ❌ main.py not found in API directory
    goto :deployment_failed
)

if not exist "%UI_DIR%\build\index.html" (
    echo ❌ Built UI files not found
    goto :deployment_failed
)

if not exist "%API_DIR%\venv\Scripts\python.exe" (
    echo ❌ Python virtual environment not properly set up
    goto :deployment_failed
)

echo ✅ All files are in place

echo.

REM ============================================================
REM Deployment Complete
REM ============================================================
echo ============================================================
echo 🎉 PRATIBIMB VM DEPLOYMENT COMPLETED SUCCESSFULLY!
echo ============================================================
echo.
echo 📋 DEPLOYMENT SUMMARY:
echo ============================================================
echo 📍 VM IP Address: %VM_IP%
echo 🔗 UI URL: http://%VM_IP%:3000
echo 🔗 API URL: http://%VM_IP%:8000
echo 📖 API Documentation: http://%VM_IP%:8000/docs
echo.
echo 🚀 QUICK START COMMANDS:
echo ============================================================
echo 1. Start all services: start_all_services.bat
echo 2. Start API only: start_api.bat
echo 3. Start UI only: start_ui_production.bat
echo 4. Stop all services: stop_all_services.bat
echo.
echo 🔥 FIREWALL RULES ADDED:
echo ============================================================
echo - Port 8000 (API Server): Allowed
echo - Port 3000 (UI Server): Allowed
echo.
echo 📝 NEXT STEPS:
echo ============================================================
echo 1. Run 'start_all_services.bat' to start both services
echo 2. Open http://%VM_IP%:3000 in your browser
echo 3. Test the Braille conversion with a YouTube URL
echo 4. Check real-time progress and file downloads
echo.
echo ⚠️  IMPORTANT NOTES:
echo ============================================================
echo - Make sure this VM is accessible from your network
echo - For external access, configure your router/firewall
echo - The services will run until you close the command windows
echo - Use 'stop_all_services.bat' to stop all services
echo.
echo ============================================================

REM Ask if user wants to start services now
set /p "START_NOW=Start all services now? (y/n): "
if /i "%START_NOW%"=="y" (
    echo.
    echo 🚀 Starting all services...
    call start_all_services.bat
)

echo.
echo ✅ Deployment script completed!
pause
exit /b 0

:deployment_failed
echo.
echo ============================================================
echo ❌ DEPLOYMENT FAILED
echo ============================================================
echo Please check the error messages above and try again.
echo You may need to:
echo - Run as Administrator
echo - Check Python and Node.js installations
echo - Verify all source files are present
echo ============================================================
pause
exit /b 1
