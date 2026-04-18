#!/bin/bash
# Quick Start Script - NFT Market Analytics Dashboard

set -e  # Exit on error

echo "🚀 NFT Market Analytics Dashboard - Quick Start"
echo "=================================================="

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Run this script from the project root."
    exit 1
fi

# Step 1: Activate virtual environment
echo ""
echo "1️⃣  Activating virtual environment..."
if [ ! -d ".venv" ]; then
    echo "   Creating new virtual environment..."
    python3 -m venv .venv
fi

source .venv/bin/activate
echo "   ✓ Virtual environment activated"

# Step 2: Install/verify dependencies
echo ""
echo "2️⃣  Installing dependencies..."
pip install -q -r requirements.txt
echo "   ✓ Dependencies installed"

# Step 3: Verify installation
echo ""
echo "3️⃣  Verifying setup..."
python -c "import streamlit; import pandas; import plotly; print('   ✓ All imports successful')"

# Step 4: Check data files
echo ""
echo "4️⃣  Checking data files..."
if [ -d "data" ] && [ -f "data/Level3_bayc_new.csv" ]; then
    count=$(ls data/*.csv 2>/dev/null | wc -l)
    echo "   ✓ Found $count CSV files"
else
    echo "   ⚠ Warning: Data files might be missing"
fi

# Step 5: Start the app
echo ""
echo "✅ Setup complete! Starting dashboard..."
echo ""
echo "📊 Dashboard URL: http://localhost:8501"
echo "Press CTRL+C to stop the server"
echo ""

streamlit run app.py
