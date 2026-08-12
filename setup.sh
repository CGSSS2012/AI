#!/bin/bash

# Multi-Purpose Development Agent Setup Script for macOS/Linux

echo ""
echo "========================================================="
echo "  Multi-Purpose Development Agent - Setup"
echo "========================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ from https://www.python.org/downloads/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed or not in PATH"
    echo "Please install Node.js 14+ from https://nodejs.org/"
    exit 1
fi

echo "[✓] Python and Node.js are installed"
echo ""

# Setup Backend
echo "========================================================="
echo "Setting up Backend..."
echo "========================================================="
cd backend

echo "[1] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[2] Installing Python dependencies..."
pip install -r requirements.txt

echo "[3] Backend setup complete!"
echo ""
cd ..

# Setup Frontend
echo "========================================================="
echo "Setting up Frontend..."
echo "========================================================="
cd frontend

echo "[1] Installing Node dependencies..."
npm install

echo "[2] Frontend setup complete!"
echo ""
cd ..

echo "========================================================="
echo "  Setup Complete!"
echo "========================================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Terminal 1 - Start Backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python app.py"
echo ""
echo "2. Terminal 2 - Start Frontend:"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "The app will open at http://localhost:3000"
echo "Backend API: http://localhost:5000"
echo ""
echo "For more information, see QUICKSTART.md or README.md"
echo ""
