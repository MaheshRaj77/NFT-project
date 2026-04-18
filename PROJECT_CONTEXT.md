# NFT Market Analytics Dashboard - Complete Project Context

**Last Updated**: April 2026  
**Python Version**: 3.14.3  
**Environment**: macOS (Virtual Environment)

---

## 📋 Executive Summary

This document serves as a comprehensive context guide for AI agents working on the NFT Market Analytics Dashboard project. It contains all necessary information to understand, modify, and extend the application.

### Project Goals
- Analyze historical NFT trading data across 5 major collections
- Provide interactive visualizations of market trends
- Enable data-driven insights into NFT market behavior
- Support collection-specific and cross-collection analysis

### Key Stakeholders
- Data Analysts: Use dashboard for market insights
- Researchers: Extract trends and patterns
- Developers: Extend functionality

---

## 🏗️ Technical Architecture

### Technology Stack
```
Frontend:        Streamlit 1.56.0 (Python web framework)
Data Processing: Pandas 3.0.2 (Data manipulation)
Visualization:   Plotly 6.7.0 (Interactive charts)
Numeric Ops:     NumPy 2.4.4 (Array operations)
Python:          3.14.3 (Latest version)
Environment:     Virtual Environment (.venv)
OS:              macOS
```

### Project Location
```
/Users/mahesh/github/NFT-project/
```

### Directory Structure
```
NFT-project/
├── .venv/                          # Python virtual environment
├── app.py                          # Main application (700+ lines)
├── requirements.txt                # 4 dependencies
├── data/                           # 10 CSV data files
│   ├── Level3_*_new.csv           # Transaction-level data
│   └── Level4_*_new.csv           # Aggregated NFT data
└── docs/
    ├── README.md                   # User guide
    ├── PROJECT_CONTEXT.md          # This file
    ├── SETUP.md                    # Installation guide
    └── ARCHITECTURE.md             # Technical details
```

---

## 📊 Data Architecture

### Data Layers

#### Level 3: Transaction Records
**Purpose**: Individual sales/transfer/mint events  
**Files**: `Level3_{collection}_new.csv`  
**Collections**: CryptoPunks, BAYC, MAYC, Doodles, Pudgy Penguins

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| identifier | int | NFT token ID |
| name | string | Human-readable NFT name |
| raw_event_type | string | Original event type |
| event_type | string | Normalized event (sale, transfer, mint) |
| order_type | string | Order type (nullable) |
| price_eth | float | Price in ETH (0.0 for non-sales) |
| from | string | Sender wallet address |
| to | string | Receiver wallet address |
| timestamp | datetime | Event timestamp (UTC) |
| tx_hash | string | Blockchain transaction hash |
| collection | string | Collection name (auto-added) |

**Data Volume**: ~50-200 rows per collection (sample data)

#### Level 4: Aggregated NFT Statistics
**Purpose**: Per-NFT summary metrics  
**Files**: `Level4_{collection}_new.csv`  
**Collections**: Same 5 collections

**Schema:**
| Column | Type | Description |
|--------|------|-------------|
| identifier | int | NFT token ID (primary key) |
| transaction_count | int | Total transactions for this NFT |
| avg_price_eth | float | Average price across transactions |
| max_price_eth | float | Highest price paid |
| min_price_eth | float | Lowest price paid |
| total_volume_eth | float | Sum of all prices paid |
| unique_buyers | int | Count of distinct buyers |
| unique_sellers | int | Count of distinct sellers |
| collection | string | Collection name (auto-added) |

**Data Volume**: ~100-1000 rows per collection (sample data)

### Data Processing Pipeline

```python
load_data()
├── Read CSV Files
│   ├── Load Level 3 (5 files)
│   ├── Load Level 4 (5 files)
│   └── Auto-assign collection names
├── Type Conversion
│   ├── Convert price_eth to numeric
│   ├── Convert timestamp to datetime
│   └── Convert numeric columns
├── Concatenation
│   ├── Combine all Level 3 files → sales_df
│   └── Combine all Level 4 files → agg_df
└── Cache Results (for performance)
    └── Reuse across session
```

### Data Flow Through Dashboard

```
CSV Files
    ↓
load_data() [cached]
    ↓
sales_df (Level 3) + agg_df (Level 4)
    ↓
Collection Filter (Sidebar)
    ↓
Derived DataFrames:
├── coll_data (collection summaries)
├── trends (monthly metrics)
├── top_vol (top 10 by volume)
├── top_tx (top 10 by transactions)
├── top_high (highest prices)
├── top_low (lowest prices)
└── event_counts (event types)
    ↓
Tab Views (6 sections)
    ↓
Visualizations + Metric Cards
```

---

## 🎨 UI/UX Architecture

### Global Styling (CSS)
- **Framework Integration**: Custom Streamlit CSS applied via `st.markdown(..., unsafe_allow_html=True)`
- **Color Variables**: All colors defined as Python constants for consistency
- **Dark Theme**: Professional dark scheme with accent colors per collection
- **Responsive**: Uses Streamlit columns and grid system

### Color Constants
```python
COLLS = ["CryptoPunks", "BAYC", "MAYC", "Doodles", "Pudgy Penguins"]
CKEYS = ["#534AB7", "#1D9E75", "#D85A30", "#BA7517", "#D4537E"]
CMAP = dict(zip(COLLS, CKEYS))  # Maps collection → color

# Theme colors
BG = "#0f0f1a"              # Main background
CARD_BG = "#1a1a2e"         # Card backgrounds
BORDER = "#2a2a3e"          # Borders
TICK = "#666666"            # Axis ticks
GRID = "rgba(255,255,255,0.07)"  # Grid lines
TEXT = "#e0e0e0"            # Primary text
SUBTEXT = "#999999"         # Secondary text
```

### Component Types

#### 1. Metric Cards
**HTML Template**: Custom styled div with label/value/unit  
**Usage**: Display key numbers (volume, count, price)  
**Function**: `metric_card(label, value, unit="")`

#### 2. Chart Cards
**Framework**: Plotly graphs with dark styling  
**Standard Settings**:
- Height: 240-280px
- Margins: 10px all sides
- Legend: Bottom center, transparent background
- Grid: Horizontal only, light gray
- Axes: Dark styling, 45° angle for x-labels

#### 3. Styled Tables
**HTML Template**: Dark-themed HTML tables  
**Features**: Rank styling, badge colors, right-aligned numbers  
**Function**: Custom HTML with CSS classes

### Tab Structure
```
Dashboard Header (Logo + Title)
    ↓
6 Tabs:
├── Tab 1: Sales & Revenue
│   ├── 4 metric cards (volume, sales, avg price, highest)
│   └── 3 charts (volume by collection, avg price, max price)
├── Tab 2: Market Trends
│   ├── 3 metric cards (peak month, avg sales, peak price)
│   └── 2 line charts (volume, avg price)
├── Tab 3: Event Analysis
│   ├── 4 metric cards (total events, sales, transfers, mints)
│   ├── 2 pie charts (event breakdown)
│   └── Notable events table
├── Tab 4: Price Analysis
│   ├── 4 metric cards (global avg, max, min, volume)
│   └── 3 bar charts (price comparison, distribution)
├── Tab 5: Volume Analysis
│   ├── Metrics and charts (volume trends)
│   └── Volume distribution
└── Tab 6: Top 10 Rankings
    ├── Top by volume
    ├── Top by transactions
    ├── Highest priced
    └── Lowest priced
```

---

## 🔧 Core Functions

### Main Application Entry Point

**File**: `app.py`  
**Lines**: ~700+ (partially shown in context)

### Key Functions

#### 1. `load_data()` [Lines 190-230]
```python
@st.cache_data
def load_data():
    """
    Load and combine Level 3 & Level 4 CSV files
    Returns: (sales_df, agg_df)
    """
```
- Caches results for performance
- Handles multiple CSV files
- Type conversion for dates and numerics
- Returns two main dataframes

#### 2. `hex_to_rgba(hex_color, alpha=0.1)` [Lines ~330]
```python
def hex_to_rgba(hex_color, alpha=0.1):
    """Convert hex color to RGBA string for transparency"""
```
- Used for chart background colors
- Supports custom alpha values

#### 3. `dark_layout(fig, height=260)` [Lines ~340]
```python
def dark_layout(fig, height=260):
    """Apply dark theme to Plotly figure"""
```
- Consistent chart styling
- Updates layout, axes, legend
- Sets grid, borders, fonts

#### 4. `bar_fig(x, y, colors, height=240)` [Lines ~375]
```python
def bar_fig(x, y, colors, height=240):
    """Create dark-themed bar chart"""
```
- Shorthand for common bar charts
- Auto-applies dark layout

#### 5. `line_fig(x, ys_dict, height=260)` [Lines ~380-420]
```python
def line_fig(x, ys_dict, height=260):
    """Create multi-line chart
    ys_dict format: {label: (values, colour)}
    """
```
- Supports multiple lines
- Custom colors per line
- Smooth curves (mode='lines+markers')

#### 6. `metric_card(label, value, unit="")` [Lines ~425]
```python
def metric_card(label, value, unit=""):
    """Return HTML for styled metric card"""
```
- Returns HTML string
- Used with `st.markdown(..., unsafe_allow_html=True)`

#### 7. Helper Functions [Lines ~430-450]
```python
card(content_html)      # Wrap content in card div
chart_title(t)          # Create chart title HTML
badge(collection)       # Create colored badge for collection
```

### Data Derivation Functions

#### Collection Summaries
```python
coll_data = (
    agg_df.groupby("collection")
    .agg({
        "total_volume_eth": "sum",
        "avg_price_eth": "mean",
        "max_price_eth": "max",
        "min_price_eth": "min",
        "transaction_count": "mean"
    })
)
```

#### Monthly Trends
```python
sales["month"] = sales["timestamp"].dt.to_period("M").astype(str)
trends = pd.DataFrame({
    "month": monthly_grp["price_eth"].sum().index,
    "volume": monthly_grp["price_eth"].sum().values,
    "avg_price": monthly_grp["price_eth"].mean().values,
    "sales_count": monthly_grp["price_eth"].count().values,
})
```

#### Top Rankings (Top 10 by various metrics)
```python
top_vol = agg_df.sort_values("total_volume_eth", ascending=False).head(10)
top_high = agg_df.sort_values("max_price_eth", ascending=False).head(10)
# ... and more
```

---

## 🎯 Tab-by-Tab Breakdown

### Tab 1: Sales & Revenue
**Purpose**: Overview of sales activity  
**Metrics**:
- Total Volume (ETH sum)
- Total Sales (count)
- Average Sale Price
- Highest Sale Price

**Charts**:
1. Volume by Collection (bar chart)
2. Average Price by Collection (bar chart)
3. Maximum Price by Collection (bar chart)

**Data Source**: Level 3 sales events

### Tab 2: Market Trends
**Purpose**: Historical trends over time  
**Metrics**:
- Peak Volume Month (best month)
- Average Monthly Sales (transactions/month)
- Peak Average Price (month + value)

**Charts**:
1. Monthly Trading Volume (line chart)
2. Monthly Average Price (line chart)
3. Monthly Sales Count (line chart)

**Data Source**: Level 3 sales with monthly aggregation

### Tab 3: Event Analysis
**Purpose**: Breakdown of transaction types  
**Event Types**:
- Sales (actual trades)
- Transfers (wallet-to-wallet)
- Mints (creation/initial distribution)

**Metrics**:
- Total Events (count)
- Sales Events (count + %)
- Transfer Events (count + %)
- Mint Events (count + %)

**Charts**:
1. Event Type Distribution (pie chart)
2. Event Type Breakdown (pie chart)

**Notable Events**:
- Highest Sale (NFT name + price)
- Most Recent Transfer (NFT name + date)
- Most Recent Mint (NFT name + date)
- Collections Tracked (count)

**Data Source**: Level 3 all events + statistics

### Tab 4: Price Analysis
**Purpose**: Price distribution analysis  
**Metrics**:
- Global Average Price (across collections)
- Global Maximum Price
- Global Minimum Price
- Total Volume (sum)

**Charts**:
1. Price by Collection - Avg vs Max÷10 vs Min (grouped bar chart)
2. Price Distribution (histogram or box plot)
3. Price Trends Over Time (line chart)

**Data Source**: Level 4 aggregated prices

### Tab 5: Volume Analysis
**Purpose**: Volume metrics and trends  
**Metrics**:
- Total Volume (ETH sum)
- Average Volume (per NFT)
- Peak Volume
- Volume by Collection

**Charts**:
1. Volume by Collection (bar chart)
2. Volume Trends (line chart)
3. Volume Distribution (histogram)

**Data Source**: Level 4 volume metrics

### Tab 6: Top 10 Rankings
**Purpose**: Identify leading NFTs  
**Rankings**:
1. Top 10 by Total Volume
2. Top 10 by Transaction Count
3. Top 10 Highest Priced
4. Top 10 Lowest Priced

**Table Format**:
- NFT ID/Name
- Collection (with color badge)
- Key Metric (volume, tx count, price)

**Data Source**: Level 4 sorted by different metrics

---

## 🔄 Sidebar Functionality

### Collection Filter
```python
with st.sidebar:
    st.markdown("COLLECTION FILTER", unsafe_allow_html=True)
    sel = st.selectbox("", ["All"] + available_colls, label_visibility="collapsed")
```

**Behavior**:
- Default: "All" collections
- Options: Each collection individually
- Effect: Filters all charts and metrics in dashboard

**Implementation**:
```python
filt = coll_data if sel == "All" else coll_data[coll_data["collection"] == sel]
filt_sales = sales if sel == "All" else sales[sales["collection"] == sel]
```

---

## 💾 Data Management

### Data Loading Strategy
- **Lazy Loading**: Data loads only on app start
- **Caching**: `@st.cache_data` decorator prevents reloading
- **In-Memory**: All data kept in memory for fast filtering

### Data Paths
```python
"data/Level3_cryptopunks_new.csv"
"data/Level3_bayc_new.csv"
"data/Level3_mayc_new.csv"
"data/Level3_doodles_new.csv"
"data/Level3_pudgy_penguins_new.csv"
"data/Level4_cryptopunks_new.csv"
"data/Level4_bayc_new.csv"
"data/Level4_mayc_new.csv"
"data/Level4_doodles_new.csv"
"data/Level4_pudgypenguins_new.csv"
```

### Data Validation
- Type conversion with `pd.to_numeric(..., errors="coerce")`
- Timestamp parsing with `pd.to_datetime(..., errors="coerce")`
- Missing values handled gracefully

---

## 🚀 Running the Application

### Prerequisites
- Python 3.14+
- Virtual environment activated
- All dependencies installed

### Command to Run
```bash
source .venv/bin/activate
streamlit run app.py
```

### Default Behavior
- Listens on `http://localhost:8501`
- Loads all data on startup
- Caches data for session
- Hot-reloads on file changes (development mode)

### Configuration
- `page_title`: "NFT Market Analytics"
- `page_icon`: "📊"
- `layout`: "wide" (full-screen columns)
- `initial_sidebar_state`: "collapsed"

---

## 🐛 Known Issues & Limitations

### Current Limitations
1. **Sample Data Only**: Current CSV files contain sample data
2. **No Real-Time**: Data doesn't update without manual reload
3. **No Persistence**: No database backend for historical tracking
4. **Manual Scaling**: Adding collections requires code changes
5. **No Authentication**: No user login/permissions
6. **No Export**: Limited data export functionality

### Potential Issues
1. **Large Datasets**: Performance may degrade with millions of records
2. **Timestamp Issues**: Assumes UTC timestamps in data
3. **Missing Data**: Handles null values but may skip calculations
4. **Collection Names**: Case-sensitive string matching required

---

## 📈 Extension Points

### Easy Additions
1. New metric cards (add calculation + `metric_card()` call)
2. New chart types (add Plotly figure + `dark_layout()`)
3. Additional collections (add CSV files + column update)
4. New time periods (modify `dt.to_period()` call)

### Complex Additions
1. Real API integration (modify `load_data()`)
2. Database backend (add SQLAlchemy queries)
3. User authentication (add `streamlit_authenticator`)
4. Export functionality (add `pd.to_excel()` or similar)
5. Machine learning (add scikit-learn predictions)

---

## 📋 Checklist for AI Agents

When working on this project, verify:

- [ ] Virtual environment is activated: `.venv/bin/python`
- [ ] All dependencies installed: `pip list | grep -E "streamlit|pandas|plotly"`
- [ ] Data files exist in `data/` folder
- [ ] CSV schema matches code expectations
- [ ] Dates parsed correctly as datetime objects
- [ ] Color constants are hex format
- [ ] Charts render in dark theme
- [ ] Collection filter works correctly
- [ ] Metric calculations are accurate
- [ ] No console errors when running

---

## 🔗 Related Documentation

- **SETUP.md**: Detailed environment setup instructions
- **ARCHITECTURE.md**: Low-level technical architecture
- **README.md**: User-facing documentation

---

## 📞 Quick Reference

| Task | Command/Function |
|------|------------------|
| Run app | `streamlit run app.py` |
| Activate venv | `source .venv/bin/activate` |
| Install deps | `pip install -r requirements.txt` |
| Add metric card | `st.markdown(metric_card(...), unsafe_allow_html=True)` |
| Create bar chart | `fig = bar_fig(x, y, colors); st.plotly_chart(fig)` |
| Create line chart | `fig = line_fig(x, ys_dict); st.plotly_chart(fig)` |
| Apply dark theme | `dark_layout(fig, height=260)` |
| Filter by collection | `df[df["collection"] == selected_collection]` |
| Format ETH amount | `_fmt_vol(value)` helper function |
| Create tab section | `with tabs[n]: ...` |
| Cache function results | `@st.cache_data` decorator |

---

**Document Version**: 1.0  
**Last Updated**: April 2026  
**Maintained By**: Development Team
