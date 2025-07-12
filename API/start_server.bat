@echo off
echo ============================================================
echo 🌟 PRATIBIMB - True Reflection of Digital World 🌟
echo Starting API Server...
echo ============================================================

echo 🔧 Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ❌ Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo 📁 Creating output directory if needed...
if not exist "Output_files" mkdir Output_files

echo 🚀 Starting API server...
echo.
echo ============================================================
echo 📍 Server will be available at: http://localhost:8000
echo 📖 API Documentation: http://localhost:8000/docs
echo 🔧 Available endpoints:
echo    • POST /process_transcript - Complete processing
echo    • POST /get_raw_transcript - Get YouTube transcript
echo    • POST /get_enhance_transcript - Enhance for blind users
echo    • GET /api/reports/{name} - Get report file
echo    • GET /api/latest-report - Get latest report
echo    • GET /api/latest-report-data - Get latest report as JSON
echo ============================================================
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause
