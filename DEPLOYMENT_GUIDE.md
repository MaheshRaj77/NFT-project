# 🚀 NFT Market Analytics - Deployment Guide

**Project Structure**:
- 🎨 **Frontend**: Streamlit Dashboard (`app.py`) 
- 🔧 **Backend API**: FastAPI (`api.py`)
- 🔐 **Config**: Environment & settings (`config.py`, `.env`)
- 🐳 **Container**: Docker support included

---

## 📊 Deployment Options Comparison

| Platform | Cost | Setup | Scaling | Best For |
|----------|------|-------|---------|----------|
| **Render.com** | Free tier + paid | ⭐⭐ Easy | Auto | 🟢 **Recommended** |
| **Railway** | Pay-as-you-go | ⭐⭐ Easy | Auto | 🟢 Good alternative |
| **Heroku** | Paid (free tier ended) | ⭐⭐ Easy | Manual | 🟡 Works but paid |
| **Streamlit Cloud** | Free | ⭐ Very easy | Limited | 🟡 Frontend only |
| **AWS/Digital Ocean** | Flexible | ⭐⭐⭐ Complex | Manual | 🔴 For experts |
| **Local VPS** | $5-20/mo | ⭐⭐ Moderate | Manual | 🔴 Technical |

---

## 🟢 OPTION 1: RENDER.COM (RECOMMENDED - FREE)

### Why Render?
- ✅ Free tier available
- ✅ Auto-deploys from GitHub
- ✅ Docker support built-in
- ✅ Health checks included
- ✅ Environment variables management
- ✅ Custom domains available

### Step 1: Prepare Repository

```bash
cd /Users/mahesh/github/NFT-project

# Verify files are ready
git add .
git commit -m "Ready for deployment to Render"
git push origin main
```

### Step 2: Update render.yaml

Edit `render.yaml` and update:

```yaml
repo: https://github.com/YOUR_GITHUB_USERNAME/NFT-project
# Change YOUR_GITHUB_USERNAME to your actual GitHub username
```

### Step 3: Create Render Account

1. Go to [render.com](https://render.com)
2. Click "Sign up" → Connect GitHub account
3. Authorize Render to access your repositories

### Step 4: Deploy Backend API

**Option A: Using render.yaml (Infrastructure as Code)**

```bash
# 1. Go to https://dashboard.render.com
# 2. Click "New +" → "Blueprint"
# 3. Paste your GitHub repo URL: https://github.com/YOUR_USERNAME/NFT-project
# 4. Select main branch
# 5. Click "Deploy"
```

**Option B: Manual deployment (if yaml doesn't work)**

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Click "New +" → "Web Service"
3. Select repository: `NFT-project`
4. Configure:
   - **Name**: `nft-market-analytics-api`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements_api.txt`
   - **Start Command**: `uvicorn api:app --host 0.0.0.0 --port 8000`
5. Select Plan: **Free**
6. Click "Create Web Service"

### Step 5: Set Environment Variables

1. Go to your service dashboard
2. Click "Environment" tab
3. Add variables:
   ```
   API_KEY_APP1 = c830a7c501571649da6563c4bf28c2f564ee0eef9b51c8e9ce534ad14cbea5ee
   API_KEY_APP2 = f5e8dd56e12121c78d5e88932e7709e97be5ff1643a4c98b3b874e94f0292c48
   ENV = production
   PORT = 8000
   ```
4. Also add Google Drive URLs (from your .env):
   ```
   DATA_URL_LEVEL3_CRYPTOPUNKS = https://drive.google.com/uc?export=download&id=...
   DATA_URL_LEVEL3_BAYC = ...
   [etc for all 10 CSV URLs]
   ```

### Step 6: Deploy Frontend Dashboard

Create a second service for Streamlit:

1. Click "New +" → "Web Service"
2. Configure:
   - **Name**: `nft-market-analytics-dashboard`
   - **Environment**: `Docker`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
3. Add environment variables (same as API service)
4. Click "Create Web Service"

### Step 7: Verify Deployment

```bash
# Check API is running
curl https://nft-market-analytics-api-XXX.onrender.com/api/health

# Check Frontend
# Visit: https://nft-market-analytics-dashboard-XXX.onrender.com
```

**Your URLs will be assigned automatically like:**
- API: `https://nft-market-analytics-api-abc123.onrender.com`
- Dashboard: `https://nft-market-analytics-dashboard-abc123.onrender.com`

---

## 🟡 OPTION 2: RAILWAY (FREE CREDITS)

### Why Railway?
- ✅ $5 free monthly credits
- ✅ Simpler deployment flow
- ✅ Auto-deploys from GitHub
- ✅ Good for quick testing

### Steps:

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select `NFT-project`
5. Railway auto-detects `Dockerfile` and deploys
6. Add environment variables in dashboard
7. Custom domain available in project settings

---

## 🟡 OPTION 3: STREAMLIT CLOUD (FREE, Frontend Only)

### Steps:

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Sign up with GitHub
3. Click "New App"
4. Connect your repository
5. Select:
   - Repo: `YOUR_USERNAME/NFT-project`
   - Branch: `main`
   - Main file path: `app.py`
6. Advanced settings → Environment variables:
   ```
   API_KEY_APP1=...
   API_URL=https://your-api.onrender.com  # Link to your API
   ```
7. Deploy!

⚠️ **Limitation**: You need API running separately (Render, Railway, etc.)

---

## 🔴 OPTION 4: AWS DEPLOYMENT (Production Scale)

### Services Needed:
- **ECS** (Elastic Container Service) for Docker containers
- **RDS** (Optional: if you add database)
- **ECR** (Elastic Container Registry) for Docker images
- **ALB** (Application Load Balancer)

### Estimated Cost:
- Free tier eligible first 12 months
- ~$15-50/month after

### Setup (Advanced):

```bash
# 1. Install AWS CLI
brew install awscli

# 2. Configure credentials
aws configure

# 3. Create ECR repository
aws ecr create-repository --repository-name nft-analytics

# 4. Build and push Docker image
docker build -t nft-analytics .
docker tag nft-analytics:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/nft-analytics
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/nft-analytics

# 5. Deploy via ECS (use AWS console or CDK)
```

---

## 🔴 OPTION 5: SELF-HOSTED (VPS)

### Services:
- **DigitalOcean** ($4-6/month)
- **Linode** ($5+/month)
- **Vultr** ($2.50+/month)

### Setup:

```bash
# 1. SSH into VPS
ssh root@YOUR_VPS_IP

# 2. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 3. Clone repository
git clone https://github.com/YOUR_USERNAME/NFT-project.git
cd NFT-project

# 4. Create .env file
cp .env.example .env
nano .env  # Add your API keys and Google Drive URLs

# 5. Run with Docker Compose
docker-compose up -d

# 6. Setup Nginx reverse proxy for SSL
sudo apt-get install nginx
# Configure SSL with Let's Encrypt (certbot)
```

---

## ✅ Quick Start: Deploy to Render (5 minutes)

### Prerequisites:
- GitHub account with NFT-project repository
- Render.com account

### Commands:

```bash
# 1. From your local machine, ensure everything is pushed
cd /Users/mahesh/github/NFT-project
git status
git add .
git commit -m "Deployment ready"
git push origin main

# 2. Go to https://render.com
# 3. Sign up / Log in
# 4. New Web Service → Select GitHub repo
# 5. Configure:
#    - Runtime: Docker
#    - Build Command: pip install -r requirements_api.txt
#    - Start Command: uvicorn api:app --host 0.0.0.0 --port 8000
# 6. Add environment variables (see below)
# 7. Deploy!

# 3. Test your API
curl https://YOUR_SERVICE_NAME.onrender.com/api/health
```

---

## 🔐 Environment Variables for Deployment

All platforms require these variables set:

### Required (API Authentication):
```
API_KEY_APP1 = c830a7c501571649da6563c4bf28c2f564ee0eef9b51c8e9ce534ad14cbea5ee
API_KEY_APP2 = f5e8dd56e12121c78d5e88932e7709e97be5ff1643a4c98b3b874e94f0292c48
```

### Required (Google Drive Data):
```
DATA_URL_LEVEL3_CRYPTOPUNKS = https://drive.google.com/uc?export=download&id=1Ic6TdqKjCazT3ORI4TjZ01XFaJxtKW16
DATA_URL_LEVEL3_BAYC = https://drive.google.com/uc?export=download&id=...
DATA_URL_LEVEL3_MAYC = ...
DATA_URL_LEVEL3_DOODLES = ...
DATA_URL_LEVEL3_PUDGY_PENGUINS = ...
DATA_URL_LEVEL4_CRYPTOPUNKS = ...
DATA_URL_LEVEL4_BAYC = ...
DATA_URL_LEVEL4_MAYC = ...
DATA_URL_LEVEL4_DOODLES = ...
DATA_URL_LEVEL4_PUDGYPENGUINS = ...
```

### Optional:
```
ENV = production
PORT = 8000
DATA_PATH = data
```

---

## 📋 Pre-Deployment Checklist

- [ ] All files committed to GitHub
- [ ] `.env` is in `.gitignore` (secrets not exposed)
- [ ] API keys are secure
- [ ] `requirements_api.txt` includes all dependencies
- [ ] `Dockerfile` is present
- [ ] Health check endpoint works locally (`/api/health`)
- [ ] Google Drive URLs are valid and accessible
- [ ] No hardcoded local paths in code

---

## 🔧 Post-Deployment Tasks

### 1. Update Frontend to Use Deployed API
Edit `app.py` to point to your deployed API:

```python
# In app.py, change:
# API_URL = "http://localhost:8000"  # Local
# to:
API_URL = "https://your-api-name.onrender.com"  # Production
```

### 2. Set Up Custom Domain (Optional)

In Render dashboard:
- Settings → Custom Domain
- Add your domain (e.g., `api.yoursite.com`)
- Configure DNS records (provided by Render)

### 3. Monitor & Logs

```bash
# Render: Dashboard → View Logs
# Railway: Dashboard → Logs tab
# Heroku: heroku logs --tail
```

### 4. Set Up Auto-Deploy

- Render: Check "Auto-deploy" in settings
- Railway: Automatic on main branch push
- Streamlit Cloud: Automatic

---

## ⚡ Performance Tips

1. **Cache data**: Google Drive calls cached in memory
2. **Pagination**: API supports limit/offset for large datasets
3. **Rate limiting**: Add to prevent abuse
4. **CDN**: Render/Railway include built-in caching
5. **Database**: Consider adding PostgreSQL for production

---

## 🆘 Troubleshooting

### API Won't Start
```bash
# Check logs
# Verify all environment variables are set
# Check if port 8000 is available
```

### Data Not Loading
```bash
# Verify Google Drive URLs are accessible
# Check DATA_URL_* environment variables
# Test CSV URLs in browser
```

### Slow Performance
```bash
# Render free tier: 0.5 vCPU (expected to be slower)
# Upgrade to paid tier for better performance
# Add caching headers
```

---

## 📞 Support & Resources

- **Render Docs**: https://docs.render.com
- **Railway Docs**: https://docs.railway.app
- **FastAPI**: https://fastapi.tiangolo.com
- **Streamlit**: https://docs.streamlit.io
- **Docker**: https://docs.docker.com

---

**Next Steps**:
1. Choose your preferred platform (Render recommended)
2. Create account and connect GitHub
3. Set environment variables
4. Deploy!
5. Test endpoints with provided API keys

**Questions?** Check the logs on your deployment platform for error details.

