# Multi-Purpose Development Agent - Complete Startup Script
# This script starts both the Flask backend and React frontend

Write-Host "Multi-Purpose Development Agent - Startup" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# ============================================
# Step 1: Set up PATH for Node.js on Windows
# ============================================
Write-Host "Setting up Node.js PATH..." -ForegroundColor Yellow
$env:Path = "C:\Program Files\nodejs;$env:Path"

# Verify Node.js and npm
try {
    $nodeVersion = node --version
    $npmVersion = npm --version
    Write-Host "[OK] Node.js: $nodeVersion" -ForegroundColor Green
    Write-Host "[OK] npm: $npmVersion" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Node.js or npm not found. Please install Node.js 14+" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================
# Step 2: Setup and Start Backend
# ============================================
Write-Host "Setting up Backend..." -ForegroundColor Yellow

$backendPath = Join-Path $scriptDir "backend"
$venvPath = Join-Path $backendPath "venv"

# Check if venv exists
if (-not (Test-Path $venvPath)) {
    Write-Host "Creating Python virtual environment..." -ForegroundColor Cyan
    cd $backendPath
    python -m venv venv
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to create virtual environment" -ForegroundColor Red
        exit 1
    }
}

# Activate venv and install dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Cyan
cd $backendPath
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip and install requirements
pip install --upgrade pip setuptools wheel -q
pip install -r requirements.txt -q

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install backend dependencies" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Backend ready" -ForegroundColor Green
Write-Host ""

# ============================================
# Step 3: Start Backend in Background
# ============================================
Write-Host "Starting Backend (Flask)..." -ForegroundColor Yellow

$backendProcess = Start-Process `
    -FilePath "python" `
    -ArgumentList "app.py" `
    -WorkingDirectory $backendPath `
    -WindowStyle Minimized `
    -PassThru

Write-Host "[OK] Backend started (PID: $($backendProcess.Id))" -ForegroundColor Green
Write-Host "   Running on: http://127.0.0.1:5000" -ForegroundColor Cyan

# Wait for backend to be ready
Write-Host "Waiting for backend to be ready..." -ForegroundColor Yellow
$backendReady = $false
$maxAttempts = 30
$attempt = 0

while (-not $backendReady -and $attempt -lt $maxAttempts) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000" -ErrorAction SilentlyContinue
        $backendReady = $true
        Write-Host "[OK] Backend is ready!" -ForegroundColor Green
    }
    catch {
        $attempt++
        Start-Sleep -Milliseconds 500
    }
}

if (-not $backendReady) {
    Write-Host "[WARNING] Backend took a while to start, continuing anyway..." -ForegroundColor Yellow
}

Write-Host ""

# ============================================
# Step 4: Setup and Start Frontend
# ============================================
Write-Host "Setting up Frontend..." -ForegroundColor Yellow

$frontendPath = Join-Path $scriptDir "frontend"

# Install dependencies if node_modules doesn't exist
if (-not (Test-Path (Join-Path $frontendPath "node_modules"))) {
    Write-Host "Installing frontend dependencies (this may take 1-2 minutes)..." -ForegroundColor Cyan
    cd $frontendPath
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install frontend dependencies" -ForegroundColor Red
        # Kill backend process before exiting
        Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
        exit 1
    }
}
else {
    Write-Host "[OK] Frontend dependencies already installed" -ForegroundColor Green
}

Write-Host ""

# ============================================
# Step 5: Start Frontend
# ============================================
Write-Host "Starting Frontend (React)..." -ForegroundColor Yellow

cd $frontendPath

# Start npm start in a new terminal window
$frontendProcess = Start-Process `
    -FilePath "npm" `
    -ArgumentList "start" `
    -WorkingDirectory $frontendPath `
    -PassThru

Write-Host "[OK] Frontend started" -ForegroundColor Green
Write-Host "   Opening at: http://localhost:3000" -ForegroundColor Cyan

Write-Host ""
Write-Host "SUCCESS! Multi-Purpose Development Agent is Running!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Backend: http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Follow the QUICKSTART.md guide to get started!" -ForegroundColor Yellow
Write-Host ""
Write-Host "To stop the agent:" -ForegroundColor Yellow
Write-Host "   - Close the React window, or" -ForegroundColor Yellow
Write-Host "   - Close this PowerShell window" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop..." -ForegroundColor Yellow

# Wait for either process to exit
Wait-Process -Id $backendProcess.Id -ErrorAction SilentlyContinue
Wait-Process -Id $frontendProcess.Id -ErrorAction SilentlyContinue

# Cleanup
Write-Host ""
Write-Host "Stopping processes..." -ForegroundColor Yellow
Stop-Process -Id $backendProcess.Id -Force -ErrorAction SilentlyContinue
Stop-Process -Id $frontendProcess.Id -Force -ErrorAction SilentlyContinue

Write-Host "[OK] Agent stopped" -ForegroundColor Green
