"""
NFT Market Analytics Dashboard - FastAPI Backend
================================================

Production-ready REST API with:
- CSV data loading & caching
- API key authentication
- CORS support
- Pagination
- Proper error handling
- JSON responses with metadata

Usage:
    uvicorn api:app --reload          # Development
    uvicorn api:app --host 0.0.0.0   # Production
"""

from fastapi import FastAPI, Header, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from functools import lru_cache
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path
import pandas as pd
import numpy as np
from pydantic import BaseModel
import json
import os
import re
from urllib.parse import parse_qs, urlparse

from config import settings, validate_api_key

# ═══════════════════════════════════════════════════════════════════════════════
# RESPONSE MODELS (Pydantic)
# ═══════════════════════════════════════════════════════════════════════════════

class APIResponse(BaseModel):
    """Standard API response wrapper"""
    status: str
    collection: Optional[str] = None
    data: Any
    count: Optional[int] = None
    timestamp: str


class CollectionInfo(BaseModel):
    """Collection metadata"""
    name: str
    color: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str = "1.0.0"


# ═══════════════════════════════════════════════════════════════════════════════
# FASTAPI APP SETUP
# ═══════════════════════════════════════════════════════════════════════════════

app = FastAPI(
    title="NFT Market Analytics API",
    description="REST API for NFT market data across 5 collections",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware - allow mobile apps to make requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_URL_ENV_MAP = {
    "Level3_cryptopunks_new.csv": "DATA_URL_LEVEL3_CRYPTOPUNKS",
    "Level3_bayc_new.csv": "DATA_URL_LEVEL3_BAYC",
    "Level3_mayc_new.csv": "DATA_URL_LEVEL3_MAYC",
    "Level3_doodles_new.csv": "DATA_URL_LEVEL3_DOODLES",
    "Level3_pudgy_penguins_new.csv": "DATA_URL_LEVEL3_PUDGY_PENGUINS",
    "Level4_cryptopunks_new.csv": "DATA_URL_LEVEL4_CRYPTOPUNKS",
    "Level4_bayc_new.csv": "DATA_URL_LEVEL4_BAYC",
    "Level4_mayc_new.csv": "DATA_URL_LEVEL4_MAYC",
    "Level4_doodles_new.csv": "DATA_URL_LEVEL4_DOODLES",
    "Level4_pudgypenguins_new.csv": "DATA_URL_LEVEL4_PUDGYPENGUINS",
}


def _gdrive_to_direct_download(url: str) -> str:
    if not url:
        return url

    if "drive.google.com" not in url:
        return url

    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    file_id = None

    if "id" in qs and qs["id"]:
        file_id = qs["id"][0]
    else:
        match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
        if match:
            file_id = match.group(1)

    if not file_id:
        return url

    return f"https://drive.google.com/uc?export=download&id={file_id}"


def _resolve_csv_source(filename: str) -> tuple[str, str]:
    local_path = Path(settings.DATA_PATH) / filename
    if local_path.exists():
        return str(local_path), "local"

    env_name = CSV_URL_ENV_MAP.get(filename, "")
    raw_url = os.getenv(env_name, "").strip() if env_name else ""
    if not raw_url:
        raise FileNotFoundError(filename)

    return _gdrive_to_direct_download(raw_url), f"env:{env_name}"


# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING WITH CACHING
# ═══════════════════════════════════════════════════════════════════════════════

@lru_cache(maxsize=1)
def load_data() -> tuple:
    """
    Load all CSV files once and cache in memory.
    
    Returns:
        tuple: (sales_df, agg_df) - Level 3 and Level 4 dataframes
    
    Performance:
        - Cold load: ~1-2 seconds
        - Cached: ~0ms (in-memory)
    """
    level3_specs = [
        ("Level3_cryptopunks_new.csv", "CryptoPunks"),
        ("Level3_bayc_new.csv", "BAYC"),
        ("Level3_mayc_new.csv", "MAYC"),
        ("Level3_doodles_new.csv", "Doodles"),
        ("Level3_pudgy_penguins_new.csv", "Pudgy Penguins"),
    ]
    level4_specs = [
        ("Level4_cryptopunks_new.csv", "CryptoPunks"),
        ("Level4_bayc_new.csv", "BAYC"),
        ("Level4_mayc_new.csv", "MAYC"),
        ("Level4_doodles_new.csv", "Doodles"),
        ("Level4_pudgypenguins_new.csv", "Pudgy Penguins"),
    ]

    missing_files = []
    load_errors = []
    sales_frames = []
    agg_frames = []

    for filename, collection in level3_specs:
        source_name = "unknown"
        try:
            source, source_name = _resolve_csv_source(filename)
            df = pd.read_csv(source)
            df["collection"] = collection
            sales_frames.append(df)
        except FileNotFoundError:
            missing_files.append(filename)
        except Exception as exc:
            load_errors.append(f"{filename} ({source_name}): {exc}")

    for filename, collection in level4_specs:
        source_name = "unknown"
        try:
            source, source_name = _resolve_csv_source(filename)
            df = pd.read_csv(source)
            df["collection"] = collection
            agg_frames.append(df)
        except FileNotFoundError:
            missing_files.append(filename)
        except Exception as exc:
            load_errors.append(f"{filename} ({source_name}): {exc}")

    if missing_files or load_errors:
        missing_hints = []
        for filename in sorted(set(missing_files)):
            env_name = CSV_URL_ENV_MAP.get(filename, "DATA_URL_<FILE>")
            missing_hints.append(
                f"{filename}: add local file under {settings.DATA_PATH}/ or set {env_name}"
            )

        details = []
        if missing_hints:
            details.append("Missing files -> " + " | ".join(missing_hints))
        if load_errors:
            details.append("Load errors -> " + " | ".join(load_errors))

        raise HTTPException(
            status_code=500,
            detail="Data loading error. " + " ; ".join(details),
        )

    sales_df = pd.concat(sales_frames, ignore_index=True)
    agg_df = pd.concat(agg_frames, ignore_index=True)

    # Type conversion
    if "timestamp" in sales_df.columns:
        sales_df["timestamp"] = pd.to_datetime(sales_df["timestamp"], errors="coerce")
    if "price_eth" in sales_df.columns:
        sales_df["price_eth"] = pd.to_numeric(sales_df["price_eth"], errors="coerce")

    for col in ["avg_price_eth", "total_volume_eth", "max_price_eth", "min_price_eth"]:
        if col in agg_df.columns:
            agg_df[col] = pd.to_numeric(agg_df[col], errors="coerce")

    return sales_df, agg_df


def nan_to_none(obj):
    """
    Recursively convert NaN/NaT values to None for JSON serialization.
    """
    if isinstance(obj, dict):
        return {k: nan_to_none(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [nan_to_none(item) for item in obj]
    elif pd.isna(obj):
        return None
    elif isinstance(obj, (pd.Timestamp, np.datetime64)):
        return str(obj)
    elif isinstance(obj, (np.integer, np.floating)):
        return float(obj) if isinstance(obj, np.floating) else int(obj)
    return obj


def get_timestamp() -> str:
    """Get current UTC timestamp in ISO format"""
    return datetime.utcnow().isoformat() + "Z"


# ═══════════════════════════════════════════════════════════════════════════════
# API KEY AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

async def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    Middleware to verify API key from X-API-Key header.
    
    Args:
        x_api_key: API key from request header
    
    Returns:
        str: The API key if valid
    
    Raises:
        HTTPException: 401 if key is invalid
    """
    if not validate_api_key(x_api_key):
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key. Provide valid X-API-Key header."
        )
    return x_api_key


# ═══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════════

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint - no auth required.
    
    Returns:
        HealthResponse: Server status
    """
    return HealthResponse(
        status="operational",
        timestamp=get_timestamp()
    )


@app.get("/api/collections", response_model=APIResponse)
async def get_collections(api_key: str = Depends(verify_api_key)):
    """
    List all NFT collections with metadata.
    
    Args:
        api_key: Validated API key
    
    Returns:
        APIResponse: List of collections with color codes
    """
    collections = [
        {"name": "CryptoPunks", "color": "#534AB7"},
        {"name": "BAYC", "color": "#1D9E75"},
        {"name": "MAYC", "color": "#D85A30"},
        {"name": "Doodles", "color": "#BA7517"},
        {"name": "Pudgy Penguins", "color": "#D4537E"},
    ]
    
    return APIResponse(
        status="success",
        data=collections,
        count=len(collections),
        timestamp=get_timestamp()
    )


@app.get("/api/sales", response_model=APIResponse)
async def get_sales(
    collection: str = Query("all", description="Collection name or 'all'"),
    limit: int = Query(50, ge=1, le=1000, description="Results per page"),
    offset: int = Query(0, ge=0, description="Results offset"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get sales/transaction records (Level 3 data) with pagination.
    
    Args:
        collection: Filter by collection name or "all"
        limit: Max results (1-1000, default 50)
        offset: Pagination offset
        api_key: Validated API key
    
    Returns:
        APIResponse: Paginated Level 3 data
    """
    sales_df, _ = load_data()
    
    # Filter by collection
    if collection.lower() != "all":
        sales_df = sales_df[sales_df['collection'] == collection]
        if sales_df.empty:
            raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    
    # Pagination
    total = len(sales_df)
    sales_df = sales_df.iloc[offset:offset + limit]
    
    # Convert to dict and handle NaN values
    data = sales_df.to_dict('records')
    data = nan_to_none(data)
    
    return APIResponse(
        status="success",
        collection=collection if collection.lower() != "all" else None,
        data=data,
        count=total,
        timestamp=get_timestamp()
    )


@app.get("/api/volume", response_model=APIResponse)
async def get_volume(
    collection: str = Query("all", description="Collection name or 'all'"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get volume metrics by collection (Level 4 data aggregation).
    
    Args:
        collection: Filter by collection or "all"
        api_key: Validated API key
    
    Returns:
        APIResponse: Volume statistics per collection
    """
    _, agg_df = load_data()
    
    # Filter by collection if specified
    if collection.lower() != "all":
        agg_df = agg_df[agg_df['collection'] == collection]
        if agg_df.empty:
            raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    
    # Aggregate by collection
    volume_data = agg_df.groupby('collection').agg({
        'total_volume_eth': 'sum',
        'transaction_count': 'sum',
        'avg_price_eth': 'mean',
        'unique_buyers': 'sum',
        'unique_sellers': 'sum',
    }).reset_index()
    
    volume_data.columns = [
        'collection', 'total_volume', 'total_transactions', 
        'average_price', 'total_unique_buyers', 'total_unique_sellers'
    ]
    
    data = volume_data.to_dict('records')
    data = nan_to_none(data)
    
    return APIResponse(
        status="success",
        collection=collection if collection.lower() != "all" else None,
        data=data,
        count=len(data),
        timestamp=get_timestamp()
    )


@app.get("/api/trends", response_model=APIResponse)
async def get_trends(
    collection: str = Query("all", description="Collection name or 'all'"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get monthly trend data (volume, avg price, transaction count).
    
    Args:
        collection: Filter by collection or "all"
        api_key: Validated API key
    
    Returns:
        APIResponse: Monthly aggregated trends
    """
    sales_df, _ = load_data()
    
    # Filter by collection
    if collection.lower() != "all":
        sales_df = sales_df[sales_df['collection'] == collection]
        if sales_df.empty:
            raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    
    # Add month column for grouping
    sales_df['month'] = sales_df['timestamp'].dt.to_period('M')
    
    # Aggregate by month
    trends = sales_df.groupby('month').agg({
        'price_eth': ['sum', 'mean', 'count']
    }).reset_index()
    
    trends.columns = ['month', 'total_volume', 'average_price', 'transaction_count']
    trends['month'] = trends['month'].astype(str)
    
    data = trends.to_dict('records')
    data = nan_to_none(data)
    
    return APIResponse(
        status="success",
        collection=collection if collection.lower() != "all" else None,
        data=data,
        count=len(data),
        timestamp=get_timestamp()
    )


@app.get("/api/events", response_model=APIResponse)
async def get_events(
    collection: str = Query("all", description="Collection name or 'all'"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get event type breakdown (sale/transfer/mint percentages).
    
    Args:
        collection: Filter by collection or "all"
        api_key: Validated API key
    
    Returns:
        APIResponse: Event type statistics
    """
    sales_df, _ = load_data()
    
    # Filter by collection
    if collection.lower() != "all":
        sales_df = sales_df[sales_df['collection'] == collection]
        if sales_df.empty:
            raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    
    # Count events by type
    total_events = len(sales_df)
    event_counts = sales_df['event_type'].value_counts().to_dict()
    
    # Calculate percentages
    event_data = {
        'total_events': int(total_events),
        'event_breakdown': {},
    }
    
    for event_type, count in event_counts.items():
        event_data['event_breakdown'][event_type] = {
            'count': int(count),
            'percentage': round((count / total_events) * 100, 2) if total_events > 0 else 0
        }
    
    return APIResponse(
        status="success",
        collection=collection if collection.lower() != "all" else None,
        data=event_data,
        count=total_events,
        timestamp=get_timestamp()
    )


@app.get("/api/price-analysis", response_model=APIResponse)
async def get_price_analysis(
    collection: str = Query("all", description="Collection name or 'all'"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get price statistics (avg, max, min, median) per collection.
    
    Args:
        collection: Filter by collection or "all"
        api_key: Validated API key
    
    Returns:
        APIResponse: Price analysis metrics
    """
    _, agg_df = load_data()
    
    # Filter by collection
    if collection.lower() != "all":
        agg_df = agg_df[agg_df['collection'] == collection]
        if agg_df.empty:
            raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    
    # Aggregate by collection
    price_analysis = agg_df.groupby('collection').agg({
        'avg_price_eth': ['mean', 'median'],
        'max_price_eth': 'max',
        'min_price_eth': 'min',
        'total_volume_eth': 'sum',
    }).reset_index()
    
    price_analysis.columns = [
        'collection', 'average_price', 'median_price', 
        'maximum_price', 'minimum_price', 'total_volume'
    ]
    
    data = price_analysis.to_dict('records')
    data = nan_to_none(data)
    
    return APIResponse(
        status="success",
        collection=collection if collection.lower() != "all" else None,
        data=data,
        count=len(data),
        timestamp=get_timestamp()
    )


@app.get("/api/top10", response_model=APIResponse)
async def get_top10(
    metric: str = Query("total_volume_eth", description="Metric to rank by"),
    collection: str = Query("all", description="Collection name or 'all'"),
    limit: int = Query(10, ge=1, le=100, description="Number of top items"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get top N NFTs ranked by chosen metric.
    
    Args:
        metric: Metric name (total_volume_eth, transaction_count, max_price_eth, etc.)
        collection: Filter by collection or "all"
        limit: How many top items to return (1-100)
        api_key: Validated API key
    
    Returns:
        APIResponse: Top ranked NFTs
    """
    _, agg_df = load_data()
    
    # Validate metric exists
    if metric not in agg_df.columns:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid metric '{metric}'. Must be one of: {', '.join(agg_df.columns)}"
        )
    
    # Filter by collection
    if collection.lower() != "all":
        agg_df = agg_df[agg_df['collection'] == collection]
        if agg_df.empty:
            raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    
    # Sort and get top N
    top_nfts = agg_df.nlargest(limit, metric)[
        ['identifier', 'collection', metric, 'avg_price_eth', 'transaction_count']
    ].reset_index(drop=True)
    
    # Add rank column
    top_nfts['rank'] = range(1, len(top_nfts) + 1)
    
    data = top_nfts.to_dict('records')
    data = nan_to_none(data)
    
    return APIResponse(
        status="success",
        collection=collection if collection.lower() != "all" else None,
        data=data,
        count=len(data),
        timestamp=get_timestamp()
    )


@app.get("/api/summary", response_model=APIResponse)
async def get_summary(
    collection: str = Query("all", description="Collection name or 'all'"),
    api_key: str = Depends(verify_api_key)
):
    """
    Get comprehensive summary with all key metrics for app home screen.
    
    Args:
        collection: Filter by collection or "all"
        api_key: Validated API key
    
    Returns:
        APIResponse: Complete summary with all major metrics
    """
    sales_df, agg_df = load_data()
    
    # Filter by collection
    if collection.lower() != "all":
        sales_df = sales_df[sales_df['collection'] == collection]
        agg_df = agg_df[agg_df['collection'] == collection]
        if agg_df.empty:
            raise HTTPException(status_code=404, detail=f"Collection '{collection}' not found")
    
    # Calculate summary metrics
    summary = {
        'total_volume_eth': float(agg_df['total_volume_eth'].sum()),
        'total_transactions': int(agg_df['transaction_count'].sum()),
        'total_unique_nfts': len(agg_df),
        'average_price_eth': float(agg_df['avg_price_eth'].mean()),
        'highest_price_eth': float(agg_df['max_price_eth'].max()),
        'lowest_price_eth': float(agg_df['min_price_eth'].min()),
        'total_events': len(sales_df),
        'event_breakdown': sales_df['event_type'].value_counts().to_dict(),
        'total_unique_buyers': int(agg_df['unique_buyers'].sum()),
        'total_unique_sellers': int(agg_df['unique_sellers'].sum()),
    }
    
    # Convert event counts to integers
    summary['event_breakdown'] = {k: int(v) for k, v in summary['event_breakdown'].items()}
    
    # Handle NaN values
    summary = nan_to_none(summary)
    
    return APIResponse(
        status="success",
        collection=collection if collection.lower() != "all" else None,
        data=summary,
        count=1,
        timestamp=get_timestamp()
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom error response format"""
    return {
        "status": "error",
        "message": exc.detail,
        "timestamp": get_timestamp()
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Catch-all error handler"""
    return {
        "status": "error",
        "message": "Internal server error",
        "timestamp": get_timestamp()
    }


# ═══════════════════════════════════════════════════════════════════════════════
# APP STARTUP/SHUTDOWN
# ═══════════════════════════════════════════════════════════════════════════════

@app.on_event("startup")
async def startup_event():
    """Pre-load data on startup for faster first request"""
    try:
        load_data()
        print("✓ Data loaded and cached successfully")
    except Exception as e:
        print(f"✗ Error loading data: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=settings.PORT,
        log_level="info"
    )
