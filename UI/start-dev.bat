@echo off
echo Starting Pratibimb UI Development Server...
echo.
echo Make sure you have:
echo 1. Node.js installed
echo 2. API server running on http://localhost:8000
echo.

echo Installing dependencies...
call npm install

echo.
echo Starting development server...
echo The application will open at http://localhost:3000
echo.

call npm start

pause
