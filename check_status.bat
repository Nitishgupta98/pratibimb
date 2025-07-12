@echo off
REM ============================================================
REM 🔧 PRATIBIMB - Quick Setup Check
REM Verify deployment status and test connectivity
REM ============================================================

echo.
echo ============================================================
echo 🔍 PRATIBIMB - Deployment Status Check
echo ============================================================
echo.

set "PROJECT_ROOT=%~dp0"
set "API_DIR=%PROJECT_ROOT%API"
set "UI_DIR=%PROJECT_ROOT%UI"

REM Check if deployment files exist
echo 📋 Checking deployment files...
echo ============================================================

if exist "%PROJECT_ROOT%start_all_services.bat" (
    echo ✅ Service scripts found
) else (
    echo ❌ Service scripts missing - run deploy_vm.bat first
    goto :end
)

if exist "%API_DIR%\venv" (
    echo ✅ Python virtual environment found
) else (
    echo ❌ Python virtual environment missing
    goto :end
)

if exist "%UI_DIR%\build" (
    echo ✅ UI build files found
) else (
    echo ❌ UI build files missing
    goto :end
)

if exist "%UI_DIR%\.env" (
    echo ✅ Environment configuration found
    echo 📄 Current .env configuration:
    type "%UI_DIR%\.env"
) else (
    echo ❌ Environment configuration missing
)

echo.

REM Check running processes
echo 🔄 Checking running services...
echo ============================================================

tasklist /fi "imagename eq python.exe" 2>nul | find /i "python.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ Python processes running (API may be active)
) else (
    echo ⚠️  No Python processes found
)

tasklist /fi "imagename eq node.exe" 2>nul | find /i "node.exe" >nul
if %errorlevel% equ 0 (
    echo ✅ Node.js processes running (UI may be active)
) else (
    echo ⚠️  No Node.js processes found
)

echo.

REM Check network connectivity
echo 🌐 Checking network connectivity...
echo ============================================================

REM Test if ports are listening
netstat -an | find ":8000" >nul
if %errorlevel% equ 0 (
    echo ✅ Port 8000 is active (API Server)
) else (
    echo ⚠️  Port 8000 not active
)

netstat -an | find ":3000" >nul
if %errorlevel% equ 0 (
    echo ✅ Port 3000 is active (UI Server)
) else (
    echo ⚠️  Port 3000 not active
)

echo.

REM Show firewall rules
echo 🔥 Checking firewall rules...
echo ============================================================

netsh advfirewall firewall show rule name="Pratibimb API Server" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ API Server firewall rule active
) else (
    echo ⚠️  API Server firewall rule missing
)

netsh advfirewall firewall show rule name="Pratibimb UI Server" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ UI Server firewall rule active
) else (
    echo ⚠️  UI Server firewall rule missing
)

echo.

REM Get current IP
echo 📍 Current network information...
echo ============================================================
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "CURRENT_IP=%%i"
    set "CURRENT_IP=!CURRENT_IP: =!"
    echo 🌐 Current IP: !CURRENT_IP!
    echo 🔗 Expected UI URL: http://!CURRENT_IP!:3000
    echo 🔗 Expected API URL: http://!CURRENT_IP!:8000
    goto :show_commands
)

:show_commands
echo.
echo 🚀 Quick Commands:
echo ============================================================
echo 1. Start all services: start_all_services.bat
echo 2. Stop all services: stop_all_services.bat
echo 3. View API logs: cd API ^&^& type logs\pratibimb.log
echo 4. Rebuild UI: cd UI ^&^& npm run build
echo 5. Test API: curl http://localhost:8000/docs

:end
echo.
echo ============================================================
pause
