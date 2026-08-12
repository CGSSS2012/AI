@echo off
REM Multi-Purpose Development Agent Setup Script for Windows

echo.
echo =========================================================
echo   Multi-Purpose Development Agent - Windows Setup
echo =========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 14+ from https://nodejs.org/
    pause
    exit /b 1
)

echo [✓] Python and Node.js are installed
echo.

REM Setup Backend
echo =========================================================
echo Setting up Backend...
echo =========================================================
cd backend

echo [1] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2] Installing Python dependencies...
pip install -r requirements.txt

echo [3] Backend setup complete!
echo.
cd ..

REM Setup Frontend
echo =========================================================
echo Setting up Frontend...
echo =========================================================
cd frontend

echo [1] Installing Node dependencies...
call npm install

echo [2] Frontend setup complete!
echo.
cd ..

echo =========================================================
echo   Setup Complete!
echo =========================================================
echo.
echo To start the application:
echo.
echo 1. Terminal 1 - Start Backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 2. Terminal 2 - Start Frontend:
echo    cd frontend
echo    npm start
echo.
echo The app will open at http://localhost:3000
echo Backend API: http://localhost:5000
echo.
echo For more information, see QUICKSTART.md or README.md
echo.
pause
