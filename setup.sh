#!/bin/bash
# Setup script for Pillar 1 system

echo "Setting up Pillar 1: Narrative Genesis Input Processor..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.9 or higher."
    exit 1
fi

echo "Python version:"
python3 --version
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

echo ""
echo "Activating virtual environment and installing dependencies..."
echo "Running: source venv/bin/activate && pip install -r requirements.txt"
echo ""

# Activate and install
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Setup complete!"
    echo ""
    echo "To use the system:"
    echo "  1. Activate virtual environment: source venv/bin/activate"
    echo "  2. Edit input_master.json with your data"
    echo "  3. Run: python process_narrative.py"
    echo ""
else
    echo ""
    echo "✗ Installation failed. Please check the error messages above."
    exit 1
fi
