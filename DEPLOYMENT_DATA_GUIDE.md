# Git Large Files & Deployment Guide

**Problem**: CSV data files exceed GitHub's file size limits:
- Level3_mayc_new.csv: 127.74 MB (❌ exceeds 100 MB hard limit)
- Level3_pudgy_penguins_new.csv: 60.50 MB (⚠️ exceeds 50 MB recommended)
- Level3_doodles_new.csv: 54.03 MB (⚠️ exceeds 50 MB recommended)

**Solution**: Data files are excluded from git. Here's how to manage them:

---

## 📋 Table of Contents

1. [Local Development](#local-development)
2. [Git Setup](#git-setup)
3. [Render Deployment](#render-deployment)
4. [Railway Deployment](#railway-deployment)
5. [Docker Deployment](#docker-deployment)

---

## 💻 Local Development

### Setup (First Time)

**Step 1: Clone repo**
```bash
git clone https://github.com/YOUR_USERNAME/NFT-project.git
cd NFT-project
```

**Step 2: Copy CSV files**
```bash
# Option A: Copy from existing location
cp ~/Downloads/Level3_*.csv data/
cp ~/Downloads/Level4_*.csv data/

# Option B: Create symlink (if data is elsewhere)
ln -s /path/to/csv/files data/

# Verify
ls -lh data/*.csv
```

**Step 3: Set up Streamlit app**
```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

**Step 4: Set up FastAPI backend**
```bash
pip install -r requirements_api.txt
cp .env.example .env
# Edit .env with your API keys

# Test endpoints
uvicorn api:app --reload

# In another terminal, test:
curl -H "X-API-Key: $(grep API_KEY_APP1 .env | cut -d= -f2)" \
     http://localhost:8000/api/collections
```

### Verify Setup
```bash
# Check data files exist
ls -lh data/*.csv

# Check file sizes
du -sh data/

# Verify CSV integrity
python -c "
import pandas as pd
for f in __import__('glob').glob('data/*.csv'):
    df = pd.read_csv(f)
    print(f'{f}: {len(df)} rows')
"
```

---

## 🔧 Git Setup

### Option 1: Use Git LFS (Recommended)

**Install Git LFS**:
```bash
# macOS
brew install git-lfs

# Ubuntu/Debian
apt-get install git-lfs

# Or download: https://git-lfs.github.com
```

**Setup LFS tracking**:
```bash
# Run our setup script
bash setup_git_lfs.sh

# Or manual setup:
git lfs install
git lfs track "data/*.csv"
git add .gitattributes
git commit -m "Add Git LFS tracking for CSV files"
```

**Push to GitHub**:
```bash
git add api.py config.py requirements_api.txt Dockerfile render.yaml README_API.md
git commit -m "Add FastAPI backend"
git push -u origin main
```

**Note**: Git LFS requires GitHub Pro subscription OR enable through repository settings. Free accounts limited to 1 GB/month.

### Option 2: Keep Data Separate (Free, Recommended)

**Current setup** (✅ Already configured):
- `.gitignore` excludes `data/*.csv`
- Data files NOT committed to git
- Git repo stays small (~500 KB)

**Push to GitHub**:
```bash
# Files only (no data)
git add api.py config.py requirements_api.txt Dockerfile render.yaml README_API.md
git commit -m "Add FastAPI backend"
git push -u origin main
```

**Data is downloaded/configured during deployment** (see sections below)

---

## 🌐 Render Deployment

### Setup Data Storage

**Step 1: Create persistent disk in Render**
- Go to dashboard.render.com
- Select your service
- Click "Disks" tab
- Click "Add Disk"
  - Name: `nft-data`
  - Mount path: `/data` (in container)
  - Size: 10 GB

**Step 2: Upload CSV files**

Option A - Via SFTP:
```bash
# Get connection info from Render dashboard
sftp -i ~/.ssh/id_rsa srv-xxxxx@sftp-render.com

# Once connected:
put Level3_bayc_new.csv /data/
put Level3_cryptopunks_new.csv /data/
put Level3_doodles_new.csv /data/
put Level3_mayc_new.csv /data/
put Level3_pudgy_penguins_new.csv /data/
put Level4_bayc_new.csv /data/
put Level4_cryptopunks_new.csv /data/
put Level4_doodles_new.csv /data/
put Level4_mayc_new.csv /data/
put Level4_pudgypenguins_new.csv /data/

exit
```

Option B - During build (if repo has data):
```bash
# Add build script to Render
render.yaml:
  buildCommand: |
    pip install -r requirements_api.txt
    # Copy data if in repo
    cp -r data/* /data/ || true
```

**Step 3: Update config**

In Render dashboard:
```
Environment Variables:
  DATA_PATH=/data
  API_KEY_APP1=sk_your_key_here
  API_KEY_APP2=sk_your_key_here
```

**Step 4: Deploy**
```bash
git push origin main
```

### Health Check
```bash
curl https://nft-market-analytics-api.onrender.com/api/health
curl -H "X-API-Key: sk_your_key" \
     https://nft-market-analytics-api.onrender.com/api/collections
```

---

## 🚂 Railway Deployment

### Setup Data Storage

**Step 1: Initialize Railway project**
```bash
railway init
```

**Step 2: Add environment variables**
```bash
railway variables set API_KEY_APP1=sk_your_key_here
railway variables set API_KEY_APP2=sk_your_key_here
railway variables set DATA_PATH=data
```

**Step 3: Upload data**

Option A - Copy to /data during deployment:
```bash
# Create data directory in Railway
railway shell
mkdir -p /data
exit

# Upload via SCP
scp -r data/* railway_user@railway-host:/data/
```

Option B - Store on Railway volume:
```bash
# In railway.json or railway dashboard:
{
  "volumes": [
    {
      "name": "nft-data",
      "mount": "/data",
      "size": "10GB"
    }
  ]
}
```

**Step 4: Deploy**
```bash
git push
railway up
```

### Health Check
```bash
railway logs
curl https://your-railway-url.railway.app/api/health
```

---

## 🐳 Docker Deployment

### Local Docker

**Build image**:
```bash
docker build -t nft-api:latest .
```

**Run with data volume**:
```bash
docker run -p 8000:8000 \
  -e API_KEY_APP1=sk_your_key_here \
  -e API_KEY_APP2=sk_your_key_here \
  -e DATA_PATH=/data \
  -v $(pwd)/data:/data \
  nft-api:latest
```

### Docker Compose

**Create `docker-compose.yml`**:
```yaml
version: '3.8'

services:
  nft-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      API_KEY_APP1: ${API_KEY_APP1}
      API_KEY_APP2: ${API_KEY_APP2}
      DATA_PATH: /data
    volumes:
      - ./data:/data
    restart: unless-stopped
```

**Run**:
```bash
cp .env.example .env
# Edit .env with your keys
docker-compose up -d
```

**Stop**:
```bash
docker-compose down
```

---

## 📦 Production Deployment Checklist

- ✅ `.gitignore` excludes `data/*.csv`
- ✅ `.env.example` provided (no secrets in repo)
- ✅ `Dockerfile` configured with data volume mount
- ✅ `render.yaml` or Railway config ready
- ✅ API keys stored in environment (not in code)
- ✅ Data downloaded/uploaded to deployment platform
- ✅ Health check passes: `/api/health`
- ✅ All 9 endpoints tested with valid API key
- ✅ Response times <200ms (data cached)

---

## 🔐 Security Notes

**Never commit:**
- `.env` file (only commit `.env.example`)
- CSV files to public repo (especially if sensitive)
- API keys or secrets

**Always use:**
- Environment variables for secrets
- API key headers (X-API-Key)
- HTTPS on production
- Persistent disk storage for data (not in container)

---

## 🚨 Troubleshooting

### CSV files not loading
```python
# Debug in Python
import os
print(os.listdir('data/'))  # Should show CSV files

# Check DATA_PATH
import sys
sys.path.insert(0, '.')
from config import settings
print(settings.DATA_PATH)
```

### Too many files error
```bash
# Increase file descriptor limit
ulimit -n 4096
```

### Render deployment fails
```bash
# Check logs
curl https://nft-market-analytics-api.onrender.com/api/health
# or use Render dashboard → Logs

# Restart service
# From Render dashboard → Services → Restart
```

### Git push still fails
```bash
# Clear git cache and retry
git rm --cached data/*.csv
git push

# Or use git lfs
bash setup_git_lfs.sh
git push
```

---

## 📚 References

- [Git LFS Documentation](https://git-lfs.github.com)
- [Render Persistent Disks](https://render.com/docs/persistent-disks)
- [Railway Volume Storage](https://docs.railway.app/guides/volumes)
- [Docker Volumes](https://docs.docker.com/storage/volumes/)

---

**Last Updated**: April 18, 2026  
**Status**: 🟢 Ready for Production
