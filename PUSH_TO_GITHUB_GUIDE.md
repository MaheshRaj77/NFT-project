# 🚀 PUSH TO GITHUB - Step by Step Guide

**Problem You Encountered**: CSV files are too large for GitHub
**Solution**: Exclude data files from git, push only code and configs

---

## ✅ What's Already Done

- ✓ `.gitignore` updated to exclude `data/` folder
- ✓ Created `.env.example` (no secrets)
- ✓ Created `DEPLOYMENT_DATA_GUIDE.md` (how to handle data on deployment)
- ✓ All code files ready (`api.py`, `config.py`, etc.)

---

## 🔴 IMPORTANT: undo previous attempt

First, remove the failed push attempt:

```bash
# Reset to before the push attempt
git reset --hard HEAD~1

# Or if you already pushed:
git push --force-with-lease origin main
```

---

## ✅ STEP 1: Verify Nothing Bad Gets Committed

```bash
cd /Users/mahesh/github/NFT-project

# Run verification script
bash verify_before_push.sh
```

**Expected output:**
```
✓ api.py found
✓ config.py found
✓ requirements_api.txt found
✓ Dockerfile found
✓ render.yaml found
✓ CSV files are ignored by git ← THIS IS IMPORTANT
```

---

## ✅ STEP 2: Check Git Status

```bash
git status
```

**Expected**: Shows code files, NOT CSV files
```
On branch main
Your branch is ahead of 'origin/main' by 1 commit.

Changes not staged for commit:
    modified:   .gitignore
    new file:   api.py
    new file:   config.py
    new file:   requirements_api.txt
    new file:   Dockerfile
    new file:   render.yaml
    new file:   README_API.md
    new file:   DEPLOYMENT_DATA_GUIDE.md
    modified:   .env.example

Untracked files:
    setup_git_lfs.sh
    verify_before_push.sh
```

**NOT expected**: No `data/Level3_*.csv` or `data/Level4_*.csv` here!

---

## ✅ STEP 3: Stage Files

```bash
# Stage backend files
git add api.py config.py requirements_api.txt

# Stage deployment configs
git add Dockerfile render.yaml

# Stage documentation
git add README_API.md DEPLOYMENT_DATA_GUIDE.md

# Stage scripts
git add setup_git_lfs.sh verify_before_push.sh

# Stage .gitignore update
git add .gitignore

# Stage .env.example
git add .env.example

# Verify what's staged
git status
```

---

## ✅ STEP 4: Commit

```bash
git commit -m "Add production-ready FastAPI backend with deployment configs

- Add api.py with 9 REST endpoints
- Add config.py for environment management
- Add Dockerfile for containerization
- Add render.yaml for Render deployment
- Add requirements_api.txt with pinned versions
- Add comprehensive documentation
- Update .gitignore to exclude large CSV files
- Data files are handled separately during deployment"
```

---

## ✅ STEP 5: Push to GitHub

```bash
git push -u origin main
```

**Expected**: 
- ✓ Upload succeeds
- ✓ No file size limit errors
- ✓ Code is on GitHub

**If it fails with file size error:**
```bash
# Find what's trying to be committed
git diff --cached --name-only

# Should NOT include data/*.csv
# If it does:
git reset HEAD data/*.csv
git push
```

---

## ✅ STEP 6: Verify on GitHub

Go to: https://github.com/YOUR_USERNAME/NFT-project

Check:
- ✓ All code files are there (`api.py`, `config.py`, etc.)
- ✓ Documentation files are there (`README_API.md`, etc.)
- ✓ `data/` folder exists (with `.gitkeep`, but NO CSV files)
- ✓ `.gitignore` excludes `data/`

---

## 📊 Repository Size

**Before (with data files)**: ~500 MB ❌
**After (code only)**: ~2 MB ✅

---

## 📝 What About the Data Files?

**Local development**: Keep them in `data/` folder
**GitHub**: NOT committed (excluded by `.gitignore`)
**Deployment**: Handle separately:
  - Option 1: Upload via SFTP to deployment platform
  - Option 2: Use Git LFS (requires GitHub Pro or workaround)
  - Option 3: Provide download script for deployment

See `DEPLOYMENT_DATA_GUIDE.md` for detailed instructions.

---

## 🔐 No Secrets in Repo?

Check what you're committing:

```bash
# View staged changes
git diff --cached

# Should NOT contain:
# - API keys
# - Database passwords
# - Private URLs
# - .env file (only .env.example)

# If you see secrets:
# 1. Don't commit
# 2. Add to .gitignore
# 3. Use environment variables instead
```

---

## ✅ FINAL CHECKLIST

Before pushing:
- ✓ Ran `bash verify_before_push.sh`
- ✓ Ran `git status` and confirmed no CSV files
- ✓ Created commit message
- ✓ Reviewed `.gitignore` excludes `data/`
- ✓ No secrets or API keys in commit
- ✓ Ready to push

---

## 🚀 YOU'RE READY!

```bash
# One last check
git status

# If everything looks good:
git push -u origin main

# You should see:
# Enumerating objects: XX, done.
# Counting objects: 100% (XX/XX), done.
# ...
# To https://github.com/YOUR_USERNAME/NFT-project.git
#    1234567..890abcd  main -> main
# Branch 'main' set to track remote branch 'main' from 'origin'.
```

✅ **Done! Your code is now on GitHub!**

---

## 🆘 TROUBLESHOOTING

### Still getting file size error?
```bash
# Check what's in the commit
git ls-files --stage | grep "data/"

# If CSV files are listed:
git rm --cached data/*.csv
git commit --amend
git push
```

### Can't push after reset?
```bash
# See what happened
git log --oneline -5

# Try again
git push -f origin main
```

### Git says "everything up-to-date"
```bash
# You already pushed successfully!
# Check GitHub: https://github.com/YOUR_USERNAME/NFT-project

# Or check local changes
git status
```

---

**Status**: 🟢 Ready to push  
**CSV Files**: Safely excluded from git  
**Code**: All production-ready  
**Deployment**: Documented in DEPLOYMENT_DATA_GUIDE.md
