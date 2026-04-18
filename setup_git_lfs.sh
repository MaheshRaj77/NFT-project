# Git Large File Storage Setup Script
# Use this to enable Git LFS for large CSV files

#!/bin/bash

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "NFT Project - Git LFS Setup"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Check if git lfs is installed
if ! command -v git-lfs &> /dev/null; then
    echo "❌ Git LFS is not installed"
    echo ""
    echo "Install Git LFS:"
    echo "  macOS: brew install git-lfs"
    echo "  Ubuntu: apt-get install git-lfs"
    echo "  Or: https://git-lfs.github.com"
    exit 1
fi

echo "✓ Git LFS found: $(git lfs version)"
echo ""

# Initialize Git LFS
echo "📦 Initializing Git LFS..."
git lfs install

# Track CSV files with LFS
echo "📝 Tracking CSV files with LFS..."
git lfs track "data/*.csv"

# Update .gitattributes
if [ -f ".gitattributes" ]; then
    echo "✓ .gitattributes updated"
else
    echo "✓ .gitattributes created"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ Git LFS Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Commit changes: git add .gitattributes && git commit -m 'Add Git LFS tracking'"
echo "2. Push to GitHub: git push -u origin main"
echo "3. Data files will be stored with Git LFS (uses bandwidth, but allows large files)"
echo ""
echo "Alternative: Download data separately during deployment"
echo "═══════════════════════════════════════════════════════════════════════════════"
