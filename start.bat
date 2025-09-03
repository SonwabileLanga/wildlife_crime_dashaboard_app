@echo off
REM Wildlife Crime Dashboard Startup Script for Windows

echo 🚀 Starting Wildlife Crime Monitoring Dashboard...
echo ================================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.7 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Start the application
echo 🌐 Starting Flask application...
echo Dashboard will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo ================================================

python app.py

pause
