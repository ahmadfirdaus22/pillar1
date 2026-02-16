#!/bin/bash
# Launch script for Pillar 1 Streamlit UI

echo "🚀 Launching Pillar 1 Streamlit UI..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first to install dependencies."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo "Installing streamlit..."
    pip install streamlit>=1.30.0
fi

echo "✅ Starting Streamlit app..."
echo ""
echo "The UI will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
streamlit run ui_app.py --server.port 8501
