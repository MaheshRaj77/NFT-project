# Technical Architecture - NFT Market Analytics Dashboard

Low-level technical architecture, design patterns, and implementation details.

## 🏗️ Overall System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Web Browser (Client)                      │
│  - Displays Streamlit UI                                    │
│  - Renders Plotly interactive charts                        │
│  - Sends user interactions                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP (WebSocket)
┌──────────────────────▼──────────────────────────────────────┐
│              Streamlit Server (Python)                       │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Session 1: User A                                   │   │
│  │ - Loads data into memory                            │   │
│  │ - Caches results                                    │   │
│  │ - Renders UI components                            │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Session 2: User B                                   │   │
│  │ - Independent data & caches                         │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────┘
                       │ File I/O
┌──────────────────────▼──────────────────────────────────────┐
│                    File System                               │
│  - data/Level3_*.csv (transaction records)                  │
│  - data/Level4_*.csv (aggregated metrics)                   │
│  - app.py (main application)                                │
│  - .streamlit/config.toml (configuration)                   │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Architecture

### Data Models (Dataframes)

#### Primary Dataframes

```python
# Level 3: Transaction Records
sales_df: DataFrame
├── identifier: int64 (NFT token ID)
├── name: object (NFT name)
├── raw_event_type: object (original type)
├── event_type: object (normalized)
├── order_type: object (nullable)
├── price_eth: float64 (in ETH)
├── from: object (hex address)
├── to: object (hex address)
├── timestamp: datetime64[ns] (UTC)
├── tx_hash: object (0x... hash)
└── collection: object (collection name)

# Level 4: Aggregated Statistics
agg_df: DataFrame
├── identifier: int64 (NFT token ID)
├── transaction_count: int64
├── avg_price_eth: float64
├── max_price_eth: float64
├── min_price_eth: float64
├── total_volume_eth: float64
├── unique_buyers: int64
├── unique_sellers: int64
└── collection: object (collection name)
```

#### Derived Dataframes

```python
# Collection Summary (Tab 1, 4, 5)
coll_data: DataFrame
├── collection: object (index)
├── total_volume: float64
├── avg_price: float64
├── max_price: float64
├── min_price: float64
└── avg_tx: float64

# Market Trends (Tab 2)
trends: DataFrame
├── month: object (YYYY-MM)
├── volume: float64 (sum of prices)
├── avg_price: float64 (mean price)
└── sales_count: int64 (transaction count)

# Top Rankings (Tab 6)
top_vol: DataFrame          # Top 10 by volume
top_tx: DataFrame           # Top 10 by transactions (alias: top_tx_nfts)
top_high: DataFrame         # Top 10 highest prices
top_low: DataFrame          # Top 10 lowest prices
```

### Memory Usage

```
sales_df:      ~5-20 MB (5000-50000 rows)
agg_df:        ~2-10 MB (1000-10000 rows)
coll_data:     ~1 KB (5 rows)
trends:        ~5-50 KB (12-100 rows)
top_vol/tx...: ~50 KB (10 rows each)
────────────────────────
Total:         ~10-50 MB per session
```

## 🔄 Data Flow

### Initialization Phase

```
1. User visits http://localhost:8501
   ↓
2. Streamlit creates new session
   ↓
3. @st.cache_data decorator checks cache
   - If miss: Execute load_data()
   - If hit: Return cached (sales_df, agg_df)
   ↓
4. load_data() executes:
   ├── Read 5 Level 3 CSVs
   ├── Read 5 Level 4 CSVs
   ├── Assign collection names
   ├── Type conversion
   └── Concatenate into sales_df, agg_df
   ↓
5. Derive downstream dataframes:
   ├── coll_data (groupby + agg)
   ├── trends (monthly groupby)
   ├── top_vol, top_tx, etc. (sort + head)
   ├── event_counts (value_counts)
   └── notable_rows (idxmax, iloc, sort)
   ↓
6. Render UI (no caching, runs every interaction)
   ├── Read coll_data, trends, etc.
   ├── Apply sidebar collection filter
   ├── Generate metric cards
   ├── Create Plotly figures
   └── Display in tabs
```

### User Interaction Phase

```
User selects collection from sidebar
   ↓
On Change Trigger:
   ├── filtered_sales = sales[sales["collection"] == selected]
   ├── filtered_coll_data = coll_data[coll_data["collection"] == selected]
   ├── Recalculate trends for selected collection
   └── Regenerate all charts & metrics
   ↓
Streamlit re-renders affected components
   ↓
Plotly sends new data to browser
   ↓
Browser updates charts with animation
```

### Session Cache Strategy

```
@st.cache_data persists:
├── sales_df (reused across all user interactions in session)
├── agg_df (reused across all user interactions in session)
└── By default: Invalidated when file changes

NOT cached (regenerated on each interaction):
├── coll_data
├── trends
├── top_vol, top_tx, top_high, top_low
├── event_counts
└── All UI components (tabs, charts, cards)
```

## 🎨 UI Rendering Pipeline

### Streamlit Component Hierarchy

```
st.set_page_config(...)
   ↓
Global CSS (st.markdown with <style> tag)
   ├── App background colors
   ├── Tab styling
   ├── Metric cards
   ├── Chart containers
   └── Tables
   ↓
Dashboard Header (HTML custom div)
   ├── Logo: "📊"
   ├── Title: "NFT Market Analytics"
   └── Subtitle: Collection names
   ↓
st.tabs() creates 6 tab panels
   ├── Tab 0: Sales & Revenue
   │  ├── st.columns(4)
   │  │  ├── metric_card() → HTML → st.markdown()
   │  │  ├── metric_card() → HTML → st.markdown()
   │  │  ├── metric_card() → HTML → st.markdown()
   │  │  └── metric_card() → HTML → st.markdown()
   │  ├── st.markdown("<br>")  # Spacing
   │  ├── st.columns(2)
   │  │  ├── bar_fig() → Figure → st.plotly_chart()
   │  │  └── bar_fig() → Figure → st.plotly_chart()
   │  └── bar_fig() → Figure → st.plotly_chart()
   ├── Tab 1: Market Trends
   │  ├── [Similar structure]
   │  └── line_fig() → Figure → st.plotly_chart()
   ├── Tab 2: Event Analysis
   │  ├── [Metric cards + pie charts]
   │  └── HTML table → st.markdown()
   ├── Tab 3: Price Analysis
   │  ├── [Metric cards]
   │  └── bar_fig() + custom Figure
   ├── Tab 4: Volume Analysis
   │  ├── [Metrics + bar charts]
   │  └── [Volume distribution]
   └── Tab 5: Top 10 Rankings
      ├── Top volume table
      ├── Top transactions table
      ├── Top high prices table
      └── Top low prices table
```

### Sidebar Rendering

```
with st.sidebar:
   ├── st.markdown() for label
   └── st.selectbox()
       ├── Options: ["All", "CryptoPunks", "BAYC", "MAYC", "Doodles", "Pudgy Penguins"]
       └── Triggers immediate re-render of all tabs with filtered data
```

## 🖼️ Chart Rendering

### Plotly Figure Creation Flow

```
Chart Function (bar_fig, line_fig, etc.)
   │
   ├── 1. Create go.Figure()
   ├── 2. Add traces (Bar, Line, Scatter, etc.)
   │   ├── Set x, y data
   │   ├── Set colors (from CMAP or explicit)
   │   ├── Set hover info
   │   └── Set marker/line properties
   │
   ├── 3. Call dark_layout(fig)
   │   ├── Set paper_bgcolor="rgba(0,0,0,0)" (transparent)
   │   ├── Set plot_bgcolor="rgba(0,0,0,0)"
   │   ├── Set font_color=TEXT
   │   ├── Set legend position & background
   │   ├── Update xaxes (grid off, line color)
   │   ├── Update yaxes (grid on, light)
   │   └── Set height
   │
   └── 4. Return figure
       │
       └── st.plotly_chart(fig, use_container_width=True)
           ├── Sends figure JSON to browser
           ├── Browser renders using Plotly.js
           └── Enables hover, click, zoom interactions
```

### Color Management

```python
# Centralized Color Definitions
COLLS = ["CryptoPunks", "BAYC", "MAYC", "Doodles", "Pudgy Penguins"]
CKEYS = ["#534AB7", "#1D9E75", "#D85A30", "#BA7517", "#D4537E"]
CMAP = dict(zip(COLLS, CKEYS))

# Usage in Charts
colors = [CMAP.get(coll, "#888") for coll in collection_list]
fig = bar_fig(x, y, colors)

# Usage in Badges
badge = f'<span style="background:{CMAP[collection]}22;color:{CMAP[collection]}">'

# Usage in hex_to_rgba
rgba_bg = hex_to_rgba(CMAP[collection], alpha=0.1)
```

## 📈 Calculation Patterns

### Groupby Aggregations

#### Collection Summary
```python
coll_data = (
    agg_df.groupby("collection", as_index=False)
    .agg({
        "total_volume_eth": "sum",      # Total across all NFTs
        "avg_price_eth": "mean",        # Average of NFT averages
        "max_price_eth": "max",         # Global max
        "min_price_eth": "min",         # Global min
        "transaction_count": "mean",    # Average transactions per NFT
    })
    .round({"avg_price": 2, "avg_tx": 1})
)
```

#### Monthly Trends
```python
sales["month"] = sales["timestamp"].dt.to_period("M").astype(str)
monthly_grp = sales.groupby("month")
trends = pd.DataFrame({
    "month": monthly_grp["price_eth"].sum().index,
    "volume": monthly_grp["price_eth"].sum().values,       # Sum = volume
    "avg_price": monthly_grp["price_eth"].mean().values,   # Mean price
    "sales_count": monthly_grp["price_eth"].count().values # Count = sales
})
```

#### Top Rankings
```python
top_vol = (
    agg_df[[_id_col, "collection", "total_volume_eth", "avg_price_eth"]]
    .dropna(subset=["total_volume_eth"])
    .sort_values("total_volume_eth", ascending=False)
    .head(10)
    .reset_index(drop=True)
    .rename(columns={...})
)
```

### Filtering Patterns

#### Single Collection
```python
filt_sales = sales[sales["collection"] == sel] if sel != "All" else sales
```

#### Value Conditions
```python
sales_only = sales_df[sales_df["event_type"].fillna("").str.lower() == "sale"]
```

#### Nullability Handling
```python
.dropna(subset=["total_volume_eth"])      # Drop rows where column is null
.fillna(0)                                 # Fill nulls with 0
.query("min_price_eth > 0")               # Filter with query string
```

## 🔐 Code Organization

### File Structure

```
app.py (700+ lines)
├── Imports (lines 1-20)
├── Page Config (lines ~25-30)
├── Color Constants (lines ~33-45)
├── Global CSS (lines ~47-170)
├── Data Loading (lines ~175-230)
│   └── load_data() function
├── Main Data Pipeline (lines ~235-280)
│   ├── Sales derivation
│   ├── Collection data aggregation
│   ├── Trends calculation
│   └── Top rankings creation
├── Sidebar Filter (lines ~320-340)
├── Helper Functions (lines ~350-450)
│   ├── hex_to_rgba()
│   ├── dark_layout()
│   ├── bar_fig()
│   ├── line_fig()
│   ├── metric_card()
│   ├── card()
│   ├── chart_title()
│   └── badge()
├── Dashboard Header (lines ~460-470)
├── Tab Creation (lines ~475-485)
└── Tab 0-5 Content (lines ~490-700)
    ├── Tab 0: Sales & Revenue
    ├── Tab 1: Market Trends
    ├── Tab 2: Event Analysis
    ├── Tab 3: Price Analysis
    ├── Tab 4: Volume Analysis
    └── Tab 5: Top 10 Rankings
```

## 🔄 Rendering Lifecycle

### Single Page Refresh

```
Trigger: 
  - User interacts (click, select, scroll)
  - File saved (development mode)
  - Browser refresh
  ↓
State Restoration:
  - Load session cache (load_data cached)
  - Restore sidebar selection
  ↓
Render:
  - Re-execute app.py from top to bottom
  - Rebuild all UI components
  - Apply current filter to data
  ↓
Diff:
  - Streamlit computes delta
  - Only changed elements are updated
  ↓
Display:
  - Browser receives updates
  - DOM is patched with new content
  - Charts re-render with animation
```

### Performance Optimization

```
Cached (does not re-run):
  ├── load_data() function
  │   └── CSV I/O (slower)
  └── Results stored in Pandas DataFrames

Not Cached (re-runs every interaction):
  ├── Collection filtering
  ├── Metric calculations (fast, in-memory)
  ├── UI rendering
  └── All st.* calls
```

## 🔗 External Dependencies

### Streamlit Ecosystem

```
streamlit (main)
├── tornado (web server)
├── click (CLI)
├── cachetools (caching)
├── altair (charting alternative)
└── pydeck (map visualization)
```

### Data Processing

```
pandas (primary)
├── numpy (underneath)
├── python-dateutil (timestamp parsing)
└── pyarrow (performance)
```

### Visualization

```
plotly (primary)
├── plotly-orca (static export)
└── kaleido (image generation)
```

## 🚀 Deployment Considerations

### Scalability Limits

| Metric | Current | Limit | Note |
|--------|---------|-------|------|
| CSV Records | ~50-200 | 10M | Memory dependent |
| Collection Filter Speed | <100ms | N/A | In-memory filtering |
| Chart Render | <1s | <5s | Browser dependent |
| Session Memory | ~50 MB | 500 MB | Per user |
| Concurrent Users | 1-10 | 100+ | Server dependent |

### Optimization Opportunities

```
Current Approach:
├── All data in memory
├── Per-request filtering
├── Client-side rendering (Plotly)
└── Streamlit manages state

For 10M+ Records:
├── Switch to database (SQLite/PostgreSQL)
├── Server-side aggregation
├── Pagination
└── Progressive loading
```

## 🔐 Security

### Input Validation

```python
# Collection filter
sel = st.selectbox("", ["All"] + available_colls)
# Safe: Only predefined options available

# No user-supplied SQL/code execution
# All file paths hardcoded
```

### Data Handling

```
CSV Files:
├── Read as pandas (safe, typed)
├── No eval() or exec()
└── Type conversion with error handling

No external API calls:
├── No data exfiltration
├── Fully local
└── No network traffic
```

## 📊 Testing Patterns

### Manual Testing Checklist

```
Initialization:
  □ App starts without errors
  □ All 10 CSVs loaded
  □ Data types correct
  □ No null values in critical fields

Functionality:
  □ Sidebar filter works
  □ All 6 tabs visible
  □ Metrics display correctly
  □ Charts render
  □ Colors apply correctly

Performance:
  □ Initial load < 3 seconds
  □ Filter change < 500ms
  □ Smooth scrolling
  □ No memory leaks
```

## 📝 Code Standards

### Naming Conventions

```python
Constants:      UPPER_SNAKE_CASE (COLLS, CMAP, BG)
Variables:      lower_snake_case (sales_df, coll_data)
Functions:      lower_snake_case (load_data, bar_fig)
Classes:        PascalCase (not used in this project)
Private:        _leading_underscore (_fmt_vol, _fmt_id)
```

### Documentation

```python
# Functions have docstrings
def metric_card(label, value, unit=""):
    """Return HTML for styled metric card"""
    
# Complex logic has comments
# ── Derive all downstream frames from real data ───────────────

# TODO/FIXME format
# TODO: Add real-time data updates
# FIXME: Handle timezone issues
```

---

**Document Version**: 1.0  
**Last Updated**: April 2026  
**Target Audience**: Developers, ML Engineers, DevOps
