#!/bin/bash
# Quick verification script for NFT Project
# Checks that everything is ready before pushing to GitHub

set -e

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "NFT Project - Pre-Push Verification"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Check Streamlit app
echo "📊 Checking Streamlit Application..."
if [ -f "app.py" ]; then
    echo "  ✓ app.py found ($(wc -l < app.py) lines)"
else
    echo "  ✗ app.py not found"
    exit 1
fi

# Check FastAPI backend
echo "🔧 Checking FastAPI Backend..."
if [ -f "api.py" ]; then
    echo "  ✓ api.py found ($(wc -l < api.py) lines)"
else
    echo "  ✗ api.py not found"
    exit 1
fi

if [ -f "config.py" ]; then
    echo "  ✓ config.py found"
else
    echo "  ✗ config.py not found"
    exit 1
fi

if [ -f "requirements_api.txt" ]; then
    echo "  ✓ requirements_api.txt found"
else
    echo "  ✗ requirements_api.txt not found"
    exit 1
fi

# Check deployment configs
echo "🌐 Checking Deployment Configurations..."
if [ -f "Dockerfile" ]; then
    echo "  ✓ Dockerfile found"
else
    echo "  ✗ Dockerfile not found"
    exit 1
fi

if [ -f "render.yaml" ]; then
    echo "  ✓ render.yaml found"
else
    echo "  ✗ render.yaml not found"
    exit 1
fi

# Check documentation
echo "📚 Checking Documentation..."
docs=("README.md" "README_API.md" "QUICK_START.md" "SETUP.md" "ARCHITECTURE.md" "PROJECT_CONTEXT.md" "AI_AGENT_COMPLETE_CONTEXT.md" "DEPLOYMENT_DATA_GUIDE.md")
found=0
for doc in "${docs[@]}"; do
    if [ -f "$doc" ]; then
        echo "  ✓ $doc"
        ((found++))
    fi
done
echo "  Found $found/8 documentation files"

# Check .gitignore
echo "🔒 Checking .gitignore..."
if grep -q "data/" .gitignore; then
    echo "  ✓ data/ excluded from git"
else
    echo "  ⚠ data/ not excluded (add to .gitignore)"
fi

# Check .env
echo "🔐 Checking Environment Files..."
if [ -f ".env.example" ]; then
    echo "  ✓ .env.example found"
else
    echo "  ✗ .env.example not found"
    exit 1
fi

if [ -f ".env" ]; then
    echo "  ⚠ .env file exists (make sure it's in .gitignore)"
else
    echo "  ✓ .env not in repo (good)"
fi

# Check data folder
echo "📁 Checking Data Folder..."
if [ -d "data" ]; then
    csv_count=$(find data -name "*.csv" 2>/dev/null | wc -l)
    if [ $csv_count -gt 0 ]; then
        echo "  ✓ data/ folder exists with $csv_count CSV files"
        # Check if CSVs would be committed
        if git check-ignore data/*.csv &>/dev/null; then
            echo "  ✓ CSV files are ignored by git"
        else
            echo "  ⚠ CSV files might be committed (check .gitignore)"
        fi
    else
        echo "  ℹ data/ folder exists but is empty (expected for deployment)"
    fi
else
    echo "  ℹ data/ folder doesn't exist (will be created on deployment)"
fi

# Check git status
echo "📊 Checking Git Status..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "  ✓ Git repository initialized"
    
    # Count files that would be committed
    file_count=$(git status --porcelain | wc -l)
    echo "  ℹ Files to commit: $file_count"
    
    # Show what would be committed (first 10 lines)
    echo ""
    echo "Files ready to commit:"
    git status --porcelain | head -10
    if [ $file_count -gt 10 ]; then
        echo "... and $((file_count - 10)) more"
    fi
else
    echo "  ✗ Not a git repository"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ VERIFICATION COMPLETE"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📋 NEXT STEPS:"
echo ""
echo "1. Review changes:"
echo "   git status"
echo ""
echo "2. Stage files:"
echo "   git add api.py config.py requirements_api.txt Dockerfile render.yaml"
echo "   git add README_API.md DEPLOYMENT_DATA_GUIDE.md .env.example"
echo ""
echo "3. Commit:"
echo "   git commit -m \"Add production-ready FastAPI backend with deployment configs\""
echo ""
echo "4. Push to GitHub:"
echo "   git push -u origin main"
echo ""
echo "✅ That's it! CSV data files are excluded from git."
echo "   Handle data upload during deployment (see DEPLOYMENT_DATA_GUIDE.md)"
echo ""
