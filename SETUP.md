# Setup Guide - NFT Market Analytics Dashboard

Complete step-by-step instructions for setting up and running the NFT Market Analytics Dashboard.

## 📋 Prerequisites

- **OS**: macOS (tested), Linux, or Windows with WSL
- **Python**: 3.14+ (currently using Python 3.14.3)
- **pip**: Python package manager (included with Python)
- **Terminal**: bash or zsh shell

## 🔧 Environment Setup

### Step 1: Verify Python Installation

Check your Python version:
```bash
python3 --version
```

Expected output: `Python 3.14.3` or higher

### Step 2: Navigate to Project Directory

```bash
cd /Users/mahesh/github/NFT-project
```

### Step 3: Activate Virtual Environment

The project includes a pre-configured virtual environment (`.venv`).

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

**On Windows (with WSL):**
```bash
source .venv/Scripts/activate
```

**Verify activation** - Your terminal should show `(.venv)` prefix:
```
(.venv) user@machine project %
```

### Step 4: Verify Python Executable

Confirm you're using the virtual environment's Python:
```bash
which python
```

Expected output: `/Users/mahesh/github/NFT-project/.venv/bin/python`

### Step 5: Install Dependencies

All required packages are listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

**Expected packages** (auto-installed):
- `streamlit==1.56.0` - Web framework
- `pandas==3.0.2` - Data manipulation
- `plotly==6.7.0` - Interactive charts
- `numpy==2.4.4` - Numerical computing
- Plus all transitive dependencies

**Verify installation:**
```bash
pip list
```

You should see all 4 main packages + ~40 dependencies.

## ✅ Verification Checks

### Test Python Imports

```bash
python -c "import streamlit; import pandas; import plotly; print('✓ All imports successful')"
```

Expected output:
```
✓ All imports successful
```

### Test Streamlit

```bash
streamlit --version
```

Expected output:
```
Streamlit, version 1.56.0
```

### Check Data Files

```bash
ls -la data/
```

You should see 10 CSV files:
```
Level3_bayc_new.csv
Level3_cryptopunks_new.csv
Level3_doodles_new.csv
Level3_mayc_new.csv
Level3_pudgy_penguins_new.csv
Level4_bayc_new.csv
Level4_cryptopunks_new.csv
Level4_doodles_new.csv
Level4_mayc_new.csv
Level4_pudgypenguins_new.csv
```

## 🚀 Running the Application

### Start the Dashboard

```bash
streamlit run app.py
```

You should see output similar to:
```
  You can now view your Streamlit app in your browser.

  URL: http://localhost:8501

  Press CTRL+C anytime to stop the server
```

### Access the Dashboard

Open your web browser and navigate to:
```
http://localhost:8501
```

### Stop the Server

Press `CTRL+C` in the terminal where Streamlit is running.

## 🔄 Development Workflow

### Making Code Changes

When you modify `app.py`:
1. Save the file in your editor
2. Streamlit automatically detects changes
3. Click "Rerun" button in the browser, or
4. Press `R` to rerun

### Adding New CSV Data

To add new data:
1. Place new CSV files in the `data/` folder
2. Update `load_data()` function in `app.py` to include them
3. Restart Streamlit with `CTRL+C` then `streamlit run app.py`

### Debugging

**Enable debug output:**
```bash
streamlit run app.py --logger.level=debug
```

**View Streamlit logs:**
```bash
# macOS/Linux
cat ~/.streamlit/logs/2026-*.log

# Or monitor in real-time
tail -f ~/.streamlit/logs/2026-*.log
```

## 🔧 Configuration

### Custom Port

If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Custom Host

To run on a specific IP:
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Configuration File

Create `.streamlit/config.toml` for persistent settings:
```toml
[theme]
primaryColor = "#534AB7"
backgroundColor = "#0f0f1a"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#e0e0e0"

[server]
port = 8501
headless = false
runOnSave = true
```

## 🛠️ Troubleshooting

### Issue: Virtual Environment Not Found

**Error**: `command not found: .venv/bin/python`

**Solution**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Issue: Dependencies Not Installed

**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
# Verify venv is activated
which python
# Should show: /Users/mahesh/github/NFT-project/.venv/bin/python

# Install dependencies
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Error**: `streamlit.errors.StreamlitAPIException: Port 8501 is already in use.`

**Solution** (option 1):
```bash
# Find and kill process on port 8501
lsof -i :8501
kill -9 <PID>
```

**Solution** (option 2):
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Data Files Not Found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'data/Level3_bayc_new.csv'`

**Solution**:
```bash
# Verify you're in the correct directory
pwd
# Should output: /Users/mahesh/github/NFT-project

# Check data folder exists
ls -la data/

# If empty, restore data files
# (files should be provided with the project)
```

### Issue: Charts Not Displaying

**Error**: Blank areas where charts should be

**Solution**:
```bash
# Clear Streamlit cache
rm -rf .streamlit/cache/

# Restart Streamlit
streamlit run app.py
```

### Issue: Slow Performance

**Cause**: Large CSV files or first-time data loading

**Solution**:
- First run will be slower as data loads
- Subsequent views use cache (very fast)
- For large datasets, consider data filtering or database

## 📦 Dependency Details

### Required Packages

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.56.0 | Web framework for dashboard |
| pandas | 3.0.2 | Data loading & manipulation |
| plotly | 6.7.0 | Interactive charts |
| numpy | 2.4.4 | Numerical operations |

### Auto-Installed Dependencies

Streamlit installs many dependencies automatically:
- `altair` - Alternative charting
- `pillow` - Image handling
- `requests` - HTTP requests
- `click` - CLI utilities
- `tornado` - Web server
- And ~35+ more...

### Version Constraints

All package versions are pinned in `requirements.txt` to ensure reproducibility. Do not upgrade individual packages unless testing compatibility.

## 🔐 Security Notes

### Data Privacy

- **Local Storage**: All data is stored locally in `data/` folder
- **No Cloud Upload**: No data is sent to external services
- **Browser Cache**: Clear browser cache if sharing the machine

### Environment Variables

No secrets required for this project. If adding external API integrations:
```bash
# Create .env file (not in version control)
echo "API_KEY=your_key_here" > .env

# Load in Python
from dotenv import load_dotenv
load_dotenv()
import os
api_key = os.getenv("API_KEY")
```

## 📝 Common Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# List installed packages
pip list

# Deactivate virtual environment
deactivate

# Create new venv (if needed)
python3 -m venv .venv

# Update pip
pip install --upgrade pip

# Check Python version
python --version

# Find which Python is running
which python

# Show Python info
python -c "import sys; print(sys.prefix)"
```

## 🚨 Emergency Reset

If everything breaks, do a complete fresh setup:

```bash
# 1. Deactivate current venv
deactivate 2>/dev/null

# 2. Remove old venv
rm -rf .venv

# 3. Create fresh venv
python3 -m venv .venv

# 4. Activate new venv
source .venv/bin/activate

# 5. Upgrade pip
pip install --upgrade pip

# 6. Install dependencies
pip install -r requirements.txt

# 7. Verify
python -c "import streamlit; print('Ready!')"

# 8. Run app
streamlit run app.py
```

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org)
- [Plotly Documentation](https://plotly.com/python)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)

## ✅ Setup Verification Checklist

Before considering setup complete:

- [ ] Python 3.14+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed from requirements.txt
- [ ] Data files present in `data/` folder
- [ ] `app.py` file exists and is readable
- [ ] Documentation files present (README, SETUP, etc.)
- [ ] Streamlit runs without errors
- [ ] Dashboard accessible at http://localhost:8501
- [ ] All 6 tabs visible and functional
- [ ] Collection filter works in sidebar
- [ ] Charts render without errors
- [ ] No console errors in terminal

---

**Last Updated**: April 2026  
**Platform**: macOS (also tested: Linux)  
**Python**: 3.14.3
