# NFT Market Analytics Dashboard - Quick Reference

## 🚀 Getting Started (60 seconds)

```bash
# 1. Navigate to project
cd /Users/mahesh/github/NFT-project

# 2. Activate environment
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py

# 5. Open browser
# http://localhost:8501
```

**Or use the quick start script:**
```bash
bash run.sh
```

## 📊 Dashboard Features

| Tab | Content | Purpose |
|-----|---------|---------|
| 📈 Sales & Revenue | Volume, counts, prices by collection | Overview |
| 📉 Market Trends | Monthly trends over time | Historical patterns |
| 🔔 Event Analysis | Sales/transfers/mints breakdown | Event classification |
| 💰 Price Analysis | Price distribution by collection | Price insights |
| 📦 Volume Analysis | Trading volume metrics | Volume patterns |
| 🏆 Top 10 Rankings | Top NFTs by various metrics | Leaderboards |

## 🎮 User Interactions

```
Sidebar (Left):
  ┌─────────────────────────────┐
  │ Collection Filter           │
  │ ┌─────────────────────────┐ │
  │ │ ▼ All                   │ │  Click to filter by:
  │ │ CryptoPunks             │ │  - All
  │ │ BAYC                    │ │  - Individual collections
  │ │ MAYC                    │ │
  │ │ Doodles                 │ │
  │ │ Pudgy Penguins          │ │
  │ └─────────────────────────┘ │
  └─────────────────────────────┘
        ↓
     All charts update instantly
```

## 📁 Project Files

```
NFT-project/
├── app.py                  # Main application (700+ lines)
├── requirements.txt        # Python dependencies
├── run.sh                  # Quick start script
├── .venv/                  # Virtual environment
└── docs/
    ├── README.md          # User guide
    ├── PROJECT_CONTEXT.md # Complete context for AI agents
    ├── SETUP.md           # Detailed setup instructions
    ├── ARCHITECTURE.md    # Technical architecture
    └── QUICK_START.md     # This file
```

## 🐛 Common Issues

| Issue | Solution |
|-------|----------|
| Port 8501 in use | `streamlit run app.py --server.port 8502` |
| Module not found | `pip install -r requirements.txt` |
| Data not loading | Check `data/` folder has 10 CSV files |
| Slow performance | Clear cache: `rm -rf .streamlit/cache/` |

## 🔧 Commands

```bash
# Run app
streamlit run app.py

# Run on different port
streamlit run app.py --server.port 8502

# Run with debug logging
streamlit run app.py --logger.level=debug

# Check installed packages
pip list

# Update single package
pip install --upgrade streamlit

# Deactivate environment
deactivate

# View Streamlit config
cat ~/.streamlit/config.toml
```

## 📊 Collections Analyzed

- **CryptoPunks** - #534AB7 (Purple)
- **BAYC** - #1D9E75 (Teal)
- **MAYC** - #D85A30 (Orange)
- **Doodles** - #BA7517 (Brown)
- **Pudgy Penguins** - #D4537E (Pink)

## 📚 Full Documentation

- **User Guide**: [README.md](README.md)
- **Setup Help**: [SETUP.md](SETUP.md)
- **AI Context**: [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md)
- **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md)

## 🆘 Need Help?

1. Check [SETUP.md](SETUP.md) for troubleshooting
2. See [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md) for technical details
3. Read [ARCHITECTURE.md](ARCHITECTURE.md) for low-level design

---

**Ready?** Run `streamlit run app.py` and open http://localhost:8501
