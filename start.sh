#!/bin/bash

# Wildlife Crime Dashboard Startup Script

echo "🚀 Starting Wildlife Crime Monitoring Dashboard..."
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip3 install -r requirements.txt

# Start the application
echo "🌐 Starting Flask application..."
echo "Dashboard will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo "================================================"

python3 app.py
