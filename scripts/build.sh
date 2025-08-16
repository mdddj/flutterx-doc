#!/bin/bash

# Build script for FlutterX MkDocs documentation

echo "Building FlutterX Documentation..."

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

# Build the documentation
echo "Building documentation..."
mkdocs build

echo "Build complete! Output is in the 'site' directory."
echo "To serve locally, run: mkdocs serve"