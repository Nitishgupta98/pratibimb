# Pratibimb Development Server Startup Script
# Starts both FastAPI back    Write-Host "🎉 Pratibimb is ready!" -ForegroundColor Green
    Write-Host "📱 UI: http://localhost:$port" -ForegroundColor Cyan
    Write-Host "🔌 API: http://localhost:8001" -ForegroundColor Cyan
    Write-Host "📚 Docs: http://localhost:8001/docs" -ForegroundColor Cyanand UI server

Write-Host "🔤 Pratibimb Development Environment" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Gray

# Check if required files exist
if (-not (Test-Path "api.py")) {
    Write-Host "❌ api.py not found. Please run from the project root directory." -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "ui\index.html")) {
    Write-Host "❌ UI files not found. Please ensure ui\index.html exists." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Project files found" -ForegroundColor Green

# Install dependencies if requirements file exists
if (Test-Path "requirements-api.txt") {
    Write-Host "📦 Installing API dependencies..." -ForegroundColor Yellow
    python -m pip install -r requirements-api.txt
}

Write-Host "🚀 Starting servers..." -ForegroundColor Cyan

# Start FastAPI server in background
Write-Host "🔧 Starting FastAPI server on http://localhost:8001" -ForegroundColor Green
Start-Process python -ArgumentList "-m", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001", "--reload" -WindowStyle Hidden

# Wait a moment for the API server to start
Start-Sleep -Seconds 3

# Start UI server
Write-Host "🌐 Starting UI server..." -ForegroundColor Green
Set-Location ui

# Find available port starting from 3000
$port = 3000
$maxAttempts = 5
$serverStarted = $false

for ($attempt = 0; $attempt -lt $maxAttempts; $attempt++) {
    try {
        Write-Host "🔍 Trying port $port..." -ForegroundColor Yellow
        Start-Process python -ArgumentList "-m", "http.server", $port -NoNewWindow
        
        Start-Sleep -Seconds 2
        
        # Test if server is responding
        $response = Invoke-WebRequest -Uri "http://localhost:$port" -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($response.StatusCode -eq 200) {
            Write-Host "✅ UI server running at http://localhost:$port" -ForegroundColor Green
            Write-Host "📖 API docs available at http://localhost:8001/docs" -ForegroundColor Cyan
            
            # Open browser
            Start-Process "http://localhost:$port"
            
            $serverStarted = $true
            break
        }
    }
    catch {
        $port++
        if ($attempt -eq ($maxAttempts - 1)) {
            Write-Host "❌ Could not find available port for UI server" -ForegroundColor Red
            exit 1
        }
    }
}

if ($serverStarted) {
    Write-Host "`n🎉 Pratibimb is ready!" -ForegroundColor Green
    Write-Host "📱 UI: http://localhost:$port" -ForegroundColor Cyan
    Write-Host "🔌 API: http://localhost:8000" -ForegroundColor Cyan
    Write-Host "📚 Docs: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "`nPress Ctrl+C to stop the servers" -ForegroundColor Yellow
    
    # Keep script running
    try {
        while ($true) {
            Start-Sleep -Seconds 1
        }
    }
    catch {
        Write-Host "`n🛑 Shutting down servers..." -ForegroundColor Yellow
        Write-Host "👋 Goodbye!" -ForegroundColor Green
    }
}
