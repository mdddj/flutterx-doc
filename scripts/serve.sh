#!/bin/bash

# Development server script for FlutterX MkDocs documentation

echo "Starting FlutterX Documentation development server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start development server
echo "Starting development server..."
echo "Documentation will be available at: http://127.0.0.1:8000"
mkdocs serve