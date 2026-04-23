# API Endpoint Testing Guide

Complete guide for testing all NFT Market Analytics API endpoints with detailed examples.

## 📋 Table of Contents

1. [Setup](#setup)
2. [Health Check](#health-check)
3. [Collections](#collections)
4. [Sales Data](#sales-data)
5. [Volume Metrics](#volume-metrics)
6. [Trends](#trends)
7. [Events](#events)
8. [Error Handling](#error-handling)
9. [Performance Tips](#performance-tips)

---

## 🔧 Setup

### Prerequisites

```bash
# Install dependencies
pip install requests

# For curl testing (usually pre-installed)
which curl

# For JSON formatting
brew install jq  # macOS
# or
sudo apt-get install jq  # Ubuntu
```

### Environment Setup

```bash
# Create .env file
cat > .env << 'EOF'
API_KEY_APP1=sk_test_key_app1_12345
API_KEY_APP2=sk_test_key_app2_67890
DATA_PATH=data
PORT=8000
HOST=0.0.0.0
ENV=development
EOF

# Start the API
uvicorn api:app --reload
```

### Helper Variables

```bash
# Save these in your shell session
export API_URL="http://localhost:8000"
export API_KEY="sk_test_key_app1_12345"

# Quick test
curl -s -H "X-API-Key: $API_KEY" $API_URL/api/health | jq .
```

---

## ✅ Health Check

**Endpoint:** `GET /api/health`  
**Auth Required:** No  
**Purpose:** Verify API is operational

### cURL

```bash
# Basic health check
curl -s $API_URL/api/health | jq .

# With response time
curl -w "\n@Response Time: %{time_total}s\n" \
     -s $API_URL/api/health | jq .
```

### Expected Response

```json
{
  "status": "operational",
  "timestamp": "2026-04-23T10:30:45Z",
  "version": "1.0.0"
}
```

### Python

```python
import requests

response = requests.get("http://localhost:8000/api/health")
assert response.status_code == 200
print(response.json())
```

---

## 🎨 Collections

**Endpoint:** `GET /api/collections`  
**Auth Required:** Yes (X-API-Key header)  
**Purpose:** List all available NFT collections

### cURL - Basic

```bash
curl -H "X-API-Key: $API_KEY" \
     $API_URL/api/collections | jq .
```

### cURL - Pretty Print

```bash
curl -s -H "X-API-Key: $API_KEY" \
     $API_URL/api/collections | jq '.data[] | {name, color}'
```

### cURL - Save to File

```bash
curl -s -H "X-API-Key: $API_KEY" \
     $API_URL/api/collections > collections.json
```

### Expected Response

```json
{
  "status": "success",
  "data": [
    {
      "name": "CryptoPunks",
      "color": "#534AB7"
    },
    {
      "name": "BAYC",
      "color": "#1D9E75"
    },
    {
      "name": "MAYC",
      "color": "#D85A30"
    },
    {
      "name": "Doodles",
      "color": "#BA7517"
    },
    {
      "name": "Pudgy Penguins",
      "color": "#D4537E"
    }
  ],
  "count": 5,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

### Python

```python
import requests

headers = {"X-API-Key": "sk_test_key"}
response = requests.get("http://localhost:8000/api/collections", headers=headers)
data = response.json()

print(f"Total Collections: {data['count']}")
for collection in data['data']:
    print(f"  • {collection['name']} - {collection['color']}")
```

---

## 💰 Sales Data

**Endpoint:** `GET /api/sales`  
**Auth Required:** Yes  
**Purpose:** Get individual sales/transaction records (Level 3 data)

### Query Parameters

| Parameter | Type | Required | Default | Range | Description |
|-----------|------|----------|---------|-------|-------------|
| `collection` | string | No | "all" | - | Collection name or "all" |
| `limit` | integer | No | 50 | 1-1000 | Results per page |
| `offset` | integer | No | 0 | ≥ 0 | Pagination offset |

### Test 1: Get First 10 Sales

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?limit=10" | jq '.data[0:2]'
```

### Test 2: Get BAYC Sales

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?collection=BAYC&limit=5" | jq '.data[] | {name, price_eth, timestamp}'
```

### Test 3: Pagination (Get items 20-30)

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?limit=10&offset=20" | jq '.count'
```

### Test 4: Count Total Records

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?limit=1" | jq '.count'
```

### Expected Response

```json
{
  "status": "success",
  "collection": "BAYC",
  "data": [
    {
      "identifier": 1,
      "name": "Bored Ape #1",
      "event_type": "sale",
      "price_eth": 125.5,
      "timestamp": "2024-01-15T14:32:00",
      "collection": "BAYC"
    },
    {
      "identifier": 2,
      "name": "Bored Ape #2",
      "event_type": "transfer",
      "price_eth": 0,
      "timestamp": "2024-01-16T09:15:00",
      "collection": "BAYC"
    }
  ],
  "count": 3456,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

### Python - Get All BAYC Sales (with pagination)

```python
import requests

def get_all_sales(collection, page_size=100):
    """Fetch all sales for a collection"""
    headers = {"X-API-Key": "sk_test_key"}
    all_items = []
    offset = 0
    
    while True:
        response = requests.get(
            "http://localhost:8000/api/sales",
            headers=headers,
            params={
                "collection": collection,
                "limit": page_size,
                "offset": offset
            }
        )
        
        data = response.json()
        all_items.extend(data['data'])
        
        if len(all_items) >= data['count']:
            break
        
        offset += page_size
    
    return all_items

bayc_sales = get_all_sales("BAYC")
print(f"Total BAYC sales: {len(bayc_sales)}")
```

---

## 📊 Volume Metrics

**Endpoint:** `GET /api/volume`  
**Auth Required:** Yes  
**Purpose:** Get aggregated volume statistics (Level 4 data)

### Test 1: All Collections Volume

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/volume" | jq '.data[] | {collection, total_volume, total_transactions}'
```

### Test 2: BAYC Volume Only

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/volume?collection=BAYC" | jq '.data[0]'
```

### Test 3: Compare Collections by Volume

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/volume" | \
     jq '.data | sort_by(-.total_volume) | .[] | {collection, total_volume}'
```

### Expected Response

```json
{
  "status": "success",
  "data": [
    {
      "collection": "CryptoPunks",
      "total_volume": 45234.5,
      "total_transactions": 5678,
      "average_price": 7.95,
      "total_unique_buyers": 1234,
      "total_unique_sellers": 890
    },
    {
      "collection": "BAYC",
      "total_volume": 32891.2,
      "total_transactions": 3456,
      "average_price": 9.51,
      "total_unique_buyers": 567,
      "total_unique_sellers": 445
    }
  ],
  "count": 5,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

### Python - Get Highest Volume Collection

```python
import requests

headers = {"X-API-Key": "sk_test_key"}
response = requests.get("http://localhost:8000/api/volume", headers=headers)
data = response.json()

# Find collection with highest volume
highest = max(data['data'], key=lambda x: x['total_volume'])
print(f"Highest volume: {highest['collection']} - {highest['total_volume']} ETH")
```

---

## 📈 Trends

**Endpoint:** `GET /api/trends`  
**Auth Required:** Yes  
**Purpose:** Get monthly trend data

### Test 1: Doodles Trends

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/trends?collection=Doodles" | \
     jq '.data[] | {month, total_volume, average_price, transaction_count}'
```

### Test 2: Latest Month Data

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/trends?collection=MAYC" | \
     jq '.data[-1]'
```

### Test 3: All Collections Latest Month

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/trends?collection=all" | \
     jq '.data[-5:] | .[] | {month, total_volume}'
```

### Expected Response

```json
{
  "status": "success",
  "collection": "Doodles",
  "data": [
    {
      "month": "2024-01",
      "total_volume": 5234.5,
      "average_price": 8.75,
      "transaction_count": 598
    },
    {
      "month": "2024-02",
      "total_volume": 4891.2,
      "average_price": 9.12,
      "transaction_count": 535
    }
  ],
  "count": 12,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

### Python - Chart Trends

```python
import requests
import json

headers = {"X-API-Key": "sk_test_key"}
response = requests.get(
    "http://localhost:8000/api/trends",
    headers=headers,
    params={"collection": "CryptoPunks"}
)

data = response.json()
print("CryptoPunks Monthly Trends")
print("-" * 60)
print(f"{'Month':<12} {'Volume':<15} {'Avg Price':<15} {'Transactions':<10}")
print("-" * 60)

for trend in data['data']:
    print(f"{trend['month']:<12} "
          f"{trend['total_volume']:<15.2f} "
          f"{trend['average_price']:<15.2f} "
          f"{trend['transaction_count']:<10}")
```

---

## 🎭 Events

**Endpoint:** `GET /api/events`  
**Auth Required:** Yes  
**Purpose:** Get event type breakdown (sales, transfers, mints)

### Test 1: Pudgy Penguins Events

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/events?collection=Pudgy%20Penguins" | jq '.'
```

### Test 2: Event Breakdown Table

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/events?collection=MAYC" | \
     jq '.data.event_breakdown | to_entries[] | {event_type: .key, count: .value.count, percentage: .value.percentage}'
```

### Test 3: Highest Event Type

```bash
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/events?collection=CryptoPunks" | \
     jq '.data.event_breakdown | to_entries | sort_by(-.value.percentage) | .[0]'
```

### Expected Response

```json
{
  "status": "success",
  "collection": "Pudgy Penguins",
  "data": {
    "total_events": 3456,
    "event_breakdown": {
      "sale": {
        "count": 2100,
        "percentage": 60.77
      },
      "transfer": {
        "count": 890,
        "percentage": 25.75
      },
      "mint": {
        "count": 466,
        "percentage": 13.48
      }
    }
  },
  "count": 1,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

### Python - Event Analysis

```python
import requests

headers = {"X-API-Key": "sk_test_key"}
response = requests.get(
    "http://localhost:8000/api/events",
    headers=headers,
    params={"collection": "BAYC"}
)

data = response.json()
events = data['data']['event_breakdown']

print(f"BAYC Event Analysis")
print(f"Total Events: {data['data']['total_events']}")
print("-" * 40)

for event_type, stats in sorted(events.items(), 
                                key=lambda x: x[1]['count'], 
                                reverse=True):
    print(f"{event_type:10} {stats['percentage']:6.2f}%  ({stats['count']:,})")
```

---

## ❌ Error Handling

### Test 1: Missing API Key

```bash
# Should return 401 Unauthorized
curl -s $API_URL/api/collections | jq .
```

**Response:**
```json
{
  "detail": "Invalid or missing API key. Provide valid X-API-Key header."
}
```

### Test 2: Invalid Collection

```bash
# Should return 404 Not Found
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?collection=NonExistent" | jq .
```

**Response:**
```json
{
  "detail": "Collection 'NonExistent' not found"
}
```

### Test 3: Invalid Limit (> 1000)

```bash
# Will be rejected by validation
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?limit=5000" | jq .
```

### Test 4: Database Error Handling

```python
import requests

def test_error_handling():
    headers = {"X-API-Key": "invalid_key"}
    
    tests = [
        ("Missing Auth", {}, "no_key"),
        ("Invalid Collection", {"collection": "Invalid"}, "invalid_collection"),
        ("Invalid Limit", {"limit": 9999}, "invalid_limit"),
    ]
    
    for name, params, test_type in tests:
        if test_type == "no_key":
            response = requests.get("http://localhost:8000/api/collections")
        else:
            headers = {"X-API-Key": "sk_test_key"}
            response = requests.get(
                "http://localhost:8000/api/sales",
                headers=headers,
                params=params
            )
        
        print(f"{name}: Status {response.status_code}")
        if response.status_code != 200:
            print(f"  Error: {response.json()['detail']}")
```

---

## ⚡ Performance Tips

### 1. Optimize Pagination

```bash
# ❌ Bad: Get all records one by one
for i in {0..1000}; do
  curl -s -H "X-API-Key: $API_KEY" \
       "$API_URL/api/sales?offset=$i&limit=1"
done

# ✅ Good: Batch request larger chunks
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?limit=100&offset=0"
```

### 2. Limit Response Size

```bash
# ❌ Bad: Get too much data
curl -s -H "X-API-Key: $API_KEY" "$API_URL/api/sales?limit=1000"

# ✅ Good: Get only what you need
curl -s -H "X-API-Key: $API_KEY" "$API_URL/api/sales?limit=50" | jq '.data[] | {name, price_eth}'
```

### 3. Cache Results

```python
from functools import lru_cache
import requests
from datetime import datetime, timedelta

class CachedAPI:
    def __init__(self, cache_ttl_seconds=300):
        self.cache_ttl = cache_ttl_seconds
        self.cache = {}
    
    def get_collections(self):
        """Get cached collections (5-minute cache)"""
        now = datetime.now()
        
        if 'collections' in self.cache:
            timestamp, data = self.cache['collections']
            if (now - timestamp).seconds < self.cache_ttl:
                return data
        
        headers = {"X-API-Key": "sk_test_key"}
        response = requests.get(
            "http://localhost:8000/api/collections",
            headers=headers
        )
        
        self.cache['collections'] = (now, response.json())
        return response.json()

api = CachedAPI()
collections = api.get_collections()  # First call: API request
collections = api.get_collections()  # Cached: no API request
```

### 4. Parallel Requests

```python
import requests
from concurrent.futures import ThreadPoolExecutor

def fetch_collection_data(collection):
    headers = {"X-API-Key": "sk_test_key"}
    
    sales = requests.get(
        "http://localhost:8000/api/sales",
        headers=headers,
        params={"collection": collection, "limit": 10}
    ).json()
    
    volume = requests.get(
        "http://localhost:8000/api/volume",
        headers=headers,
        params={"collection": collection}
    ).json()
    
    return {"sales": sales, "volume": volume}

# Fetch all collections in parallel
collections = ["CryptoPunks", "BAYC", "MAYC", "Doodles", "Pudgy Penguins"]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_collection_data, collections))

print(f"Fetched data for {len(results)} collections")
```

---

## 📝 Test Checklist

Before deploying to production, verify:

- [ ] Health check returns 200
- [ ] Collections endpoint lists all 5 collections
- [ ] Sales data includes required fields
- [ ] Volume metrics calculated correctly
- [ ] Trends show monthly progression
- [ ] Events breakdown totals 100%
- [ ] Pagination works correctly
- [ ] Invalid collection returns 404
- [ ] Missing API key returns 401
- [ ] Response times are acceptable
- [ ] API works from production environment

---

**Happy Testing! 🧪**
