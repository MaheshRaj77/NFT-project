# NFT Market Analytics Dashboard

A comprehensive Streamlit-based analytics dashboard for analyzing NFT market data across 5 major collections: **CryptoPunks**, **BAYC** (Bored Ape Yacht Club), **MAYC** (Mutant Ape Yacht Club), **Doodles**, and **Pudgy Penguins**.

## 🎯 Project Overview

This dashboard provides real-time market insights into NFT trading activity, including sales trends, price analysis, volume metrics, and individual NFT rankings. The application uses Python with Streamlit for the frontend and Plotly for interactive visualizations.

### Collections Tracked
- **CryptoPunks** - Pioneering generative art NFTs
- **BAYC** - Bored Ape Yacht Club
- **MAYC** - Mutant Ape Yacht Club
- **Doodles** - Community-driven art collection
- **Pudgy Penguins** - Collectible penguin characters

## 📊 Dashboard Sections

1. **Sales & Revenue** - Total volume, transaction counts, average/highest sale prices by collection
2. **Market Trends** - Monthly trading volume, average prices, and sales count trends
3. **Event Analysis** - Breakdown of transaction types (sales, transfers, mints) with notable events
4. **Price Analysis** - Price distribution by collection (avg, max, min prices)
5. **Volume Analysis** - Trading volume metrics and trends across collections
6. **Top 10 Rankings** - Highest/lowest priced NFTs and most-traded NFTs

## 🚀 Quick Start

### Prerequisites
- Python 3.14+
- Virtual environment (venv)

### Installation & Setup

1. **Activate the virtual environment:**
   ```bash
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard:**
   Open your browser and navigate to `http://localhost:8501`

## 📁 Project Structure

```
NFT-project/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .venv/                          # Virtual environment (auto-created)
├── data/
│   ├── Level3_cryptopunks_new.csv  # Individual transaction data
│   ├── Level3_bayc_new.csv
│   ├── Level3_mayc_new.csv
│   ├── Level3_doodles_new.csv
│   ├── Level3_pudgy_penguins_new.csv
│   ├── Level4_cryptopunks_new.csv  # Aggregated NFT statistics
│   ├── Level4_bayc_new.csv
│   ├── Level4_mayc_new.csv
│   ├── Level4_doodles_new.csv
│   └── Level4_pudgypenguins_new.csv
└── docs/
    ├── README.md                   # This file
    ├── PROJECT_CONTEXT.md          # AI-agent context document
    ├── SETUP.md                    # Detailed setup guide
    └── ARCHITECTURE.md             # Technical architecture
```

## 🛠 Technologies Used

| Component | Library | Version |
|-----------|---------|---------|
| Dashboard Framework | Streamlit | 1.56.0 |
| Data Processing | Pandas | 3.0.2 |
| Visualization | Plotly | 6.7.0 |
| Numerical Computing | NumPy | 2.4.4 |
| Python Runtime | Python | 3.14.3 |

## 📊 Data Sources

### Level 3 Data (Transaction Records)
Raw transaction data with:
- NFT identifier and name
- Event types (mint, sale, transfer)
- Price in ETH
- Buyer/seller addresses
- Transaction timestamps
- Transaction hashes

### Level 4 Data (Aggregated Statistics)
Per-NFT aggregated metrics:
- Transaction count
- Average/Max/Min prices
- Total trading volume
- Unique buyer/seller counts

## 🎨 UI/UX Features

- **Dark Theme**: Professional dark color scheme (#0f0f1a background, #1a1a2e cards)
- **Collection Color Coding**: Unique colors for each collection
- **Responsive Layout**: Wide layout optimized for large screens
- **Interactive Charts**: Hover tooltips and zoom capabilities
- **Collection Filter**: Sidebar filter to focus on specific collections
- **Metric Cards**: Key metrics displayed prominently with proper formatting

## 🔧 Configuration

### Using Google Drive CSV Links (.env)

If you uploaded data to Google Drive, you can run the app/API without copying CSVs into `data/`:

1. Copy `.env.example` to `.env`
2. Fill `DATA_URL_*` variables with your Google Drive file links
3. Start the app/API normally

Supported link formats include:
- `https://drive.google.com/file/d/<FILE_ID>/view?...`
- `https://drive.google.com/open?id=<FILE_ID>`

The loader automatically converts these to direct-download URLs.

### Color Palette
```python
CryptoPunks: #534AB7 (Purple)
BAYC: #1D9E75 (Teal)
MAYC: #D85A30 (Orange)
Doodles: #BA7517 (Brown)
Pudgy Penguins: #D4537E (Pink)
```

### Styling
- Background: #0f0f1a
- Card Background: #1a1a2e
- Border: #2a2a3e
- Grid Lines: rgba(255,255,255,0.07)
- Text: #e0e0e0
- Subtext: #999999

## 📝 Usage Notes

- **Collection Filter**: Use the sidebar dropdown to filter dashboard data for specific collections or view "All" collections
- **Interactive Charts**: All Plotly charts support zoom, pan, and export functions (hover over chart for options)
- **Data Updates**: Add new CSV files to the `data/` folder and restart the app to load new data
- **Performance**: Data is cached using `@st.cache_data` for optimal performance on repeated views

## 🔄 Data Processing Pipeline

1. **CSV Loading**: Level 3 and Level 4 CSVs are loaded separately
2. **Data Concatenation**: Collection-specific dataframes are combined
3. **Type Conversion**: Timestamps and numeric values are properly parsed
4. **Filtering**: Data is filtered based on user-selected collection
5. **Aggregation**: Derived metrics are calculated (trends, rankings, statistics)
6. **Visualization**: Data is formatted and rendered through Plotly charts

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Virtual environment not found | Run `python -m venv .venv` to create it |
| Dependencies not installed | Run `.venv/bin/pip install -r requirements.txt` |
| Port 8501 already in use | Run `streamlit run app.py --server.port 8502` |
| Data files not found | Ensure CSV files are in the `data/` directory |
| Charts not displaying | Clear cache: delete `.streamlit/cache` folder |

## 📈 Future Enhancements

- Real-time data integration via APIs
- Additional NFT collections
- Advanced filtering options (date ranges, price ranges)
- Export functionality for reports
- User authentication for personalized dashboards
- Machine learning-based price predictions
- Portfolio tracking features

## 📄 License

This project is provided as-is for analytical purposes.

## 🤝 Support

For issues or questions, refer to the documentation in the `docs/` folder:
- Technical details: See `ARCHITECTURE.md`
- AI agent context: See `PROJECT_CONTEXT.md`
- Setup help: See `SETUP.md`
