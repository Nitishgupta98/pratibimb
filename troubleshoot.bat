@echo off
setlocal enabledelayedexpansion
REM ============================================================
REM 🔧 PRATIBIMB - Troubleshooting & Repair Tool
REM Fix common deployment issues
REM ============================================================

echo.
echo ============================================================
echo 🔧 PRATIBIMB - Troubleshooting Tool
echo ============================================================
echo.

set "PROJECT_ROOT=%~dp0"
set "API_DIR=%PROJECT_ROOT%API"
set "UI_DIR=%PROJECT_ROOT%UI"

:menu
echo.
echo 📋 Select troubleshooting option:
echo ============================================================
echo 1. Fix firewall rules
echo 2. Rebuild Python environment
echo 3. Rebuild UI
echo 4. Fix permissions
echo 5. Reset environment configuration
echo 6. Clear all caches
echo 7. Test network connectivity
echo 8. View error logs
echo 9. Complete reset (re-run deployment)
echo 0. Exit
echo ============================================================
set /p "choice=Enter your choice (0-9): "

if "%choice%"=="1" goto :fix_firewall
if "%choice%"=="2" goto :rebuild_python
if "%choice%"=="3" goto :rebuild_ui
if "%choice%"=="4" goto :fix_permissions
if "%choice%"=="5" goto :reset_env
if "%choice%"=="6" goto :clear_cache
if "%choice%"=="7" goto :test_network
if "%choice%"=="8" goto :view_logs
if "%choice%"=="9" goto :complete_reset
if "%choice%"=="0" goto :exit
goto :menu

:fix_firewall
echo.
echo 🔥 Fixing firewall rules...
echo ============================================================
netsh advfirewall firewall delete rule name="Pratibimb API Server" >nul 2>&1
netsh advfirewall firewall delete rule name="Pratibimb UI Server" >nul 2>&1
netsh advfirewall firewall add rule name="Pratibimb API Server" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="Pratibimb UI Server" dir=in action=allow protocol=TCP localport=3000
echo ✅ Firewall rules updated
goto :menu

:rebuild_python
echo.
echo 🐍 Rebuilding Python environment...
echo ============================================================
cd /d "%API_DIR%"
if exist "venv" rmdir /s /q "venv"
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
echo ✅ Python environment rebuilt
goto :menu

:rebuild_ui
echo.
echo ⚛️ Rebuilding UI...
echo ============================================================
cd /d "%UI_DIR%"
if exist "build" rmdir /s /q "build"
if exist "node_modules" rmdir /s /q "node_modules"
npm install
npm run build
echo ✅ UI rebuilt
goto :menu

:fix_permissions
echo.
echo 🔐 Fixing file permissions...
echo ============================================================
icacls "%PROJECT_ROOT%" /grant:r "%USERNAME%":(OI)(CI)F /T >nul 2>&1
echo ✅ Permissions updated
goto :menu

:reset_env
echo.
echo 🔧 Resetting environment configuration...
echo ============================================================
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "NEW_IP=%%i"
    set "NEW_IP=!NEW_IP: =!"
    goto :found_new_ip
)
:found_new_ip
echo Current IP detected: !NEW_IP!
set /p "USER_IP=Enter VM IP address (or press Enter to use !NEW_IP!): "
if "%USER_IP%"=="" set "USER_IP=!NEW_IP!"

cd /d "%UI_DIR%"
(
echo # Pratibimb VM Deployment Configuration
echo REACT_APP_ENVIRONMENT=vm
echo REACT_APP_API_URL=http://!USER_IP!:8000
echo REACT_APP_VM_DEPLOYMENT=true
echo GENERATE_SOURCEMAP=false
) > .env
echo ✅ Environment configuration reset
echo 📍 New API URL: http://!USER_IP!:8000
goto :menu

:clear_cache
echo.
echo 🗑️ Clearing all caches...
echo ============================================================
cd /d "%UI_DIR%"
if exist ".next" rmdir /s /q ".next"
if exist "node_modules\.cache" rmdir /s /q "node_modules\.cache"
npm cache clean --force >nul 2>&1

cd /d "%API_DIR%"
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "*.pyc" del /q "*.pyc"
for /d %%d in (*) do (
    if exist "%%d\__pycache__" rmdir /s /q "%%d\__pycache__"
)
echo ✅ Caches cleared
goto :menu

:test_network
echo.
echo 🌐 Testing network connectivity...
echo ============================================================
echo Testing localhost connections...
curl -I http://localhost:8000 2>nul | find "200 OK" >nul
if %errorlevel% equ 0 (
    echo ✅ API responding on localhost:8000
) else (
    echo ❌ API not responding on localhost:8000
)

curl -I http://localhost:3000 2>nul | find "200" >nul
if %errorlevel% equ 0 (
    echo ✅ UI responding on localhost:3000
) else (
    echo ❌ UI not responding on localhost:3000
)

echo.
echo Testing external IP...
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /c:"IPv4 Address"') do (
    set "TEST_IP=%%i"
    set "TEST_IP=!TEST_IP: =!"
    echo Testing http://!TEST_IP!:8000...
    curl -I http://!TEST_IP!:8000 2>nul | find "200 OK" >nul
    if %errorlevel% equ 0 (
        echo ✅ API accessible via !TEST_IP!:8000
    ) else (
        echo ❌ API not accessible via !TEST_IP!:8000
    )
    goto :network_done
)
:network_done
goto :menu

:view_logs
echo.
echo 📄 Viewing error logs...
echo ============================================================
echo API Logs:
if exist "%API_DIR%\logs\pratibimb.log" (
    echo Last 20 lines of API log:
    powershell "Get-Content '%API_DIR%\logs\pratibimb.log' -Tail 20"
) else (
    echo ❌ No API log file found
)

echo.
echo Request Logs:
if exist "%API_DIR%\logs\requests" (
    echo Recent request logs:
    dir /b /o-d "%API_DIR%\logs\requests\*.log" 2>nul | head -5
) else (
    echo ❌ No request logs found
)

echo.
echo UI Build Logs:
if exist "%UI_DIR%\npm-debug.log" (
    echo Last 10 lines of npm debug log:
    powershell "Get-Content '%UI_DIR%\npm-debug.log' -Tail 10"
) else (
    echo ℹ️  No UI debug log found
)
goto :menu

:complete_reset
echo.
echo 🔄 Complete reset - this will re-run the full deployment...
echo ============================================================
set /p "confirm=Are you sure? This will rebuild everything (y/n): "
if /i not "%confirm%"=="y" goto :menu

echo Stopping all services...
taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im node.exe /t >nul 2>&1

echo Running deployment script...
call "%PROJECT_ROOT%deploy_vm.bat"
goto :exit

:exit
echo.
echo ============================================================
echo 🔧 Troubleshooting session ended
echo ============================================================
pause
exit /b 0
