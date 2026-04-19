# 🚀 QUICK DEPLOYMENT REFERENCE

## Where Can You Deploy?

### ✅ BEST OPTIONS (Free or Very Cheap)

```
┌─────────────────────────────────────────────────────────────────┐
│ 🥇 RENDER.COM (RECOMMENDED - FREE)                              │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Free tier available                                           │
│ ✅ Easy GitHub integration                                       │
│ ✅ Docker support built-in                                       │
│ ✅ Auto-deploy on git push                                       │
│ ⏱️  Setup: 5 minutes                                             │
│                                                                  │
│ 🔗 Visit: https://render.com                                    │
│ 📝 Your Files: render.yaml (already configured!)                │
│ 🐳 Your Docker: Dockerfile (already configured!)                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 🥈 RAILWAY (Pay as you go - $5 free credits)                   │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Free $5 monthly credits                                       │
│ ✅ Simpler deployment                                            │
│ ✅ Auto-detects Docker setup                                     │
│ ⏱️  Setup: 3 minutes                                             │
│                                                                  │
│ 🔗 Visit: https://railway.app                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ 🥉 STREAMLIT CLOUD (Free - Frontend Only)                       │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Completely free                                               │
│ ✅ Perfect for Streamlit apps                                    │
│ ⚠️  Requires API running elsewhere                               │
│ ⏱️  Setup: 2 minutes                                             │
│                                                                  │
│ 🔗 Visit: https://streamlit.io/cloud                            │
│ 📝 Link to your API running on Render/Railway                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 RECOMMENDED SETUP

### Deploy Both Components (Frontend + API)

```
Your GitHub Repository
    ↓
Render.com (or Railway)
    ↓
    ├─ Backend API (api.py)
    │  └─ https://your-api.onrender.com
    │
    └─ Frontend Dashboard (app.py)
       └─ https://your-dashboard.onrender.com
             ↓
             (connects to API)
             ↓
        Google Drive Data
```

---

## ⚡ FASTEST DEPLOYMENT (Render - 5 Steps)

### Step 1: Prepare
```bash
cd /Users/mahesh/github/NFT-project
git push origin main  # Ensure code is pushed
```

### Step 2: Create Render Account
Visit: https://render.com → Sign up with GitHub

### Step 3: Deploy API
- Click "New +" → "Web Service"
- Select your NFT-project repository
- Settings auto-fill from render.yaml
- Click "Create Web Service"

### Step 4: Deploy Dashboard
- Click "New +" → "Web Service" again
- Same repo, but change:
  - Start Command: `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
- Click "Create Web Service"

### Step 5: Configure Environment Variables
In both services:
- Go to "Environment" tab
- Add:
  ```
  API_KEY_APP1=c830a7c501571649da6563c4bf28c2f564ee0eef9b51c8e9ce534ad14cbea5ee
  API_KEY_APP2=f5e8dd56e12121c78d5e88932e7709e97be5ff1643a4c98b3b874e94f0292c48
  DATA_URL_LEVEL3_CRYPTOPUNKS=https://drive.google.com/uc?export=download&id=1Ic6TdqKjCazT3ORI4TjZ01XFaJxtKW16
  [add all other DATA_URL_* variables]
  ```

✅ **Done! Your app is live!**

---

## 📊 COST COMPARISON

| Platform | API | Dashboard | Total/Month |
|----------|-----|-----------|------------|
| **Render Free** | Free | Free* | $0 |
| **Railway** | Free credits | Free credits | $0-5 |
| **Streamlit Cloud** | N/A | Free | $0 (API elsewhere) |
| **Heroku** | Paid | Paid | $20+ |
| **AWS** | Flexible | Flexible | $10-50+ |
| **VPS** | N/A | N/A | $4-10 |

*Render free tier includes 750 hours/month per service (unlimited projects)

---

## 🔐 What You Need

- ✅ **GitHub Account** (repo already committed)
- ✅ **API Keys** (stored in .env)
  - APP1: `c830a7c501571649da6563c4bf28c2f564ee0eef9b51c8e9ce534ad14cbea5ee`
  - APP2: `f5e8dd56e12121c78d5e88932e7709e97be5ff1643a4c98b3b874e94f0292c48`
- ✅ **Google Drive URLs** (10 CSV links in .env)
- ✅ **Docker file** (already included: `Dockerfile`)
- ✅ **Config** (already included: `render.yaml`)

---

## 🧪 VERIFY DEPLOYMENT

After deploying, test your endpoints:

```bash
# Test API (replace with your Render URL)
curl https://your-service.onrender.com/api/health

# Expected response:
# {"status":"operational","timestamp":"...","version":"1.0.0"}

# Test with API key
curl -H "X-API-Key: c830a7c501571649da6563c4bf28c2f564ee0eef9b51c8e9ce534ad14cbea5ee" \
     https://your-service.onrender.com/api/collections

# Visit Dashboard
# https://your-dashboard.onrender.com
```

---

## 📋 FILE REFERENCES

- 📄 **DEPLOYMENT_GUIDE.md** - Full guide with all options
- 📄 **render.yaml** - Render configuration (ready to use)
- 🐳 **Dockerfile** - Container setup (ready to use)
- 📄 **requirements_api.txt** - API dependencies
- 📄 **requirements.txt** - Dashboard dependencies

---

## ❓ FAQ

**Q: Should I deploy both frontend and backend?**  
A: Yes! Frontend + Backend together gives full functionality.

**Q: Can I use Streamlit Cloud?**  
A: Yes, but you need API running separately (use Render for API).

**Q: How much will it cost?**  
A: Free for both on Render! (750 hours/month per service)

**Q: Can I use my own domain?**  
A: Yes, all platforms support custom domains.

**Q: What if API is slow?**  
A: Render free tier is slower. Upgrade to Starter ($7/month) for better performance.

---

**Next Steps:**
1. Go to https://render.com
2. Sign up with GitHub
3. Deploy NFT-project
4. Share your deployed URLs! 🎉

