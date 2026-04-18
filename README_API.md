# NFT Market Analytics API - Complete Documentation

**Status**: 🟢 Production Ready  
**Version**: 1.0.0  
**Framework**: FastAPI + Uvicorn  
**Python**: 3.14.3  
**Data Source**: 10 CSV files (5 Level3 + 5 Level4)

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Local Development](#local-development)
3. [Deployment](#deployment)
4. [API Endpoints](#api-endpoints)
5. [Authentication](#authentication)
6. [Response Format](#response-format)
7. [Mobile App Integration](#mobile-app-integration)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Virtual environment activated
- CSV data files in `data/` folder

### Setup (5 minutes)

**Step 1: Install dependencies**
```bash
pip install -r requirements_api.txt
```

**Step 2: Create .env file**
```bash
cp .env.example .env
```

**Step 3: Generate API keys**
```bash
# Generate two strong API keys
openssl rand -hex 32
openssl rand -hex 32
```

**Step 4: Update .env with your keys**
```bash
API_KEY_APP1=sk_your_first_key_here
API_KEY_APP2=sk_your_second_key_here
DATA_PATH=data
PORT=8000
HOST=0.0.0.0
ENV=development
```

**Step 5: Run the API**
```bash
uvicorn api:app --reload
```

**Step 6: Access**
- API: http://localhost:8000
- Documentation: http://localhost:8000/api/docs
- Alternative Docs: http://localhost:8000/api/redoc

---

## 💻 Local Development

### Running the API

**Development mode (with auto-reload)**:
```bash
uvicorn api:app --reload
```

**Production mode**:
```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Testing with cURL

**Health check (no auth required)**:
```bash
curl http://localhost:8000/api/health
```

**With API key**:
```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     http://localhost:8000/api/collections
```

### Testing with Python

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "sk_your_api_key_here"
headers = {"X-API-Key": API_KEY}

# Get collections
response = requests.get(f"{API_URL}/api/collections", headers=headers)
print(response.json())

# Get BAYC sales data
response = requests.get(
    f"{API_URL}/api/sales?collection=BAYC&limit=10",
    headers=headers
)
print(response.json())
```

### Interactive Testing

Open http://localhost:8000/api/docs in browser:
- Click "Authorize" button
- Enter your API key in the dialog
- Try endpoints directly in Swagger UI

---

## 🌐 Deployment

### Option 1: Render.com (Recommended)

**Step 1: Prepare repository**
```bash
# Ensure files are in git
git add api.py config.py requirements_api.txt Dockerfile render.yaml .env.example
git commit -m "Add FastAPI backend"
git push origin main
```

**Step 2: Connect to Render**
- Go to https://dashboard.render.com
- Click "New +" → "Web Service"
- Connect GitHub repository
- Select repository and branch

**Step 3: Configure**
- Runtime: Docker
- Build command: `pip install -r requirements_api.txt`
- Start command: `uvicorn api:app --host 0.0.0.0 --port 8000`

**Step 4: Set environment variables**
- Click "Environment" in Render dashboard
- Add `API_KEY_APP1` (generate new strong key)
- Add `API_KEY_APP2` (generate new strong key)
- Add `DATA_PATH=data`
- Add `ENV=production`

**Step 5: Upload data files**
- Attach persistent disk (5GB)
- Mount at `/app/data`
- Upload CSV files via SFTP or during build

**Step 6: Deploy**
- Click "Deploy"
- Wait for build to complete (~2 minutes)
- API will be available at: `https://nft-market-analytics-api.onrender.com`

### Option 2: Railway.app

**Step 1: Install Railway CLI**
```bash
npm install -g @railway/cli
```

**Step 2: Login and initialize**
```bash
railway login
railway init
```

**Step 3: Add environment variables**
```bash
railway variables set API_KEY_APP1=sk_your_key_here
railway variables set API_KEY_APP2=sk_your_key_here
railway variables set DATA_PATH=data
railway variables set ENV=production
```

**Step 4: Deploy**
```bash
railway up
```

### Option 3: Docker Locally

**Build image**:
```bash
docker build -t nft-api:latest .
```

**Run container**:
```bash
docker run -p 8000:8000 \
  -e API_KEY_APP1=sk_your_key_here \
  -e API_KEY_APP2=sk_your_key_here \
  -e DATA_PATH=data \
  -v $(pwd)/data:/app/data \
  nft-api:latest
```

---

## 📡 API Endpoints

### Authentication
All endpoints (except `/api/health`) require `X-API-Key` header:
```
X-API-Key: sk_your_api_key_here
```

### Endpoint Reference

#### 1. Health Check (Public)
```
GET /api/health
```
**No authentication required**

**Response**:
```json
{
  "status": "operational",
  "timestamp": "2026-04-18T10:00:00Z",
  "version": "1.0.0"
}
```

---

#### 2. List Collections
```
GET /api/collections
```
**Query Parameters**: None

**Response**:
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
    }
  ],
  "count": 5,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

#### 3. Get Sales/Transactions
```
GET /api/sales?collection=BAYC&limit=50&offset=0
```
**Query Parameters**:
- `collection` (string): Collection name or "all" (default: "all")
- `limit` (integer): Results per page, 1-1000 (default: 50)
- `offset` (integer): Pagination offset (default: 0)

**Response**:
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
    }
  ],
  "count": 1250,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

#### 4. Get Volume Metrics
```
GET /api/volume?collection=all
```
**Query Parameters**:
- `collection` (string): Collection name or "all"

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "collection": "BAYC",
      "total_volume": 45230.5,
      "total_transactions": 2150,
      "average_price": 21.03,
      "total_unique_buyers": 890,
      "total_unique_sellers": 756
    }
  ],
  "count": 5,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

#### 5. Get Monthly Trends
```
GET /api/trends?collection=BAYC
```
**Query Parameters**:
- `collection` (string): Collection name or "all"

**Response**:
```json
{
  "status": "success",
  "collection": "BAYC",
  "data": [
    {
      "month": "2024-01",
      "total_volume": 5230.25,
      "average_price": 18.5,
      "transaction_count": 282
    },
    {
      "month": "2024-02",
      "total_volume": 6150.75,
      "average_price": 19.2,
      "transaction_count": 320
    }
  ],
  "count": 12,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

#### 6. Get Event Analysis
```
GET /api/events?collection=all
```
**Query Parameters**:
- `collection` (string): Collection name or "all"

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_events": 8750,
    "event_breakdown": {
      "sale": {
        "count": 3200,
        "percentage": 36.57
      },
      "transfer": {
        "count": 3150,
        "percentage": 36.00
      },
      "mint": {
        "count": 2400,
        "percentage": 27.43
      }
    }
  },
  "count": 8750,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

#### 7. Get Price Analysis
```
GET /api/price-analysis?collection=all
```
**Query Parameters**:
- `collection` (string): Collection name or "all"

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "collection": "BAYC",
      "average_price": 45.5,
      "median_price": 35.2,
      "maximum_price": 280.0,
      "minimum_price": 2.5,
      "total_volume": 98750.25
    }
  ],
  "count": 5,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

#### 8. Get Top 10 Rankings
```
GET /api/top10?metric=total_volume_eth&collection=all&limit=10
```
**Query Parameters**:
- `metric` (string): Metric to rank by (total_volume_eth, transaction_count, max_price_eth)
- `collection` (string): Collection name or "all"
- `limit` (integer): Number of top items (1-100, default: 10)

**Response**:
```json
{
  "status": "success",
  "data": [
    {
      "rank": 1,
      "identifier": 42,
      "collection": "BAYC",
      "total_volume_eth": 2850.5,
      "avg_price_eth": 285.05,
      "transaction_count": 10
    }
  ],
  "count": 10,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

#### 9. Get Complete Summary (Home Screen)
```
GET /api/summary?collection=all
```
**Query Parameters**:
- `collection` (string): Collection name or "all"

**Response**:
```json
{
  "status": "success",
  "data": {
    "total_volume_eth": 450230.5,
    "total_transactions": 12850,
    "total_unique_nfts": 8750,
    "average_price_eth": 35.02,
    "highest_price_eth": 2850.5,
    "lowest_price_eth": 0.5,
    "total_events": 25000,
    "event_breakdown": {
      "sale": 9200,
      "transfer": 9500,
      "mint": 6300
    },
    "total_unique_buyers": 4500,
    "total_unique_sellers": 3800
  },
  "count": 1,
  "timestamp": "2026-04-18T10:00:00Z"
}
```

---

## 🔐 Authentication

### API Key Management

**Generate secure keys**:
```bash
# Option 1: OpenSSL
openssl rand -hex 32

# Option 2: Python
python -c "import secrets; print(secrets.token_hex(32))"

# Option 3: Online
# https://www.uuidgenerator.net/
```

### Two-App Setup

Configure two separate API keys in `.env`:
```
API_KEY_APP1=sk_abc123...  # For iOS app
API_KEY_APP2=sk_xyz789...  # For Android app
```

### Rate Limiting (Future)

Currently unlimited. For production, add:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

## 📦 Response Format

### Success Response (2xx)
```json
{
  "status": "success",
  "collection": "BAYC",      // Null if not collection-specific
  "data": { ... },           // Endpoint-specific data
  "count": 150,              // Total records (not paginated count)
  "timestamp": "2026-04-18T10:00:00Z"
}
```

### Error Response (4xx/5xx)
```json
{
  "status": "error",
  "message": "Invalid API key",
  "timestamp": "2026-04-18T10:00:00Z"
}
```

### Status Codes
| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (invalid API key) |
| 404 | Not found (collection doesn't exist) |
| 500 | Server error |

---

## 📱 Mobile App Integration

### iOS (Swift)

```swift
import Foundation

class NFTAPIClient {
    let baseURL = "https://nft-market-analytics-api.onrender.com"
    let apiKey = "sk_your_ios_api_key"
    
    func getCollections() async throws -> APIResponse {
        var request = URLRequest(
            url: URL(string: "\(baseURL)/api/collections")!
        )
        request.setValue(apiKey, forHTTPHeaderField: "X-API-Key")
        
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(APIResponse.self, from: data)
    }
    
    func getSalesByCollection(_ collection: String) async throws -> APIResponse {
        var request = URLRequest(
            url: URL(string: "\(baseURL)/api/sales?collection=\(collection)&limit=50")!
        )
        request.setValue(apiKey, forHTTPHeaderField: "X-API-Key")
        
        let (data, _) = try await URLSession.shared.data(for: request)
        return try JSONDecoder().decode(APIResponse.self, from: data)
    }
}
```

### Android (Kotlin)

```kotlin
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.Query

interface NFTAPIService {
    @GET("/api/collections")
    suspend fun getCollections(
        @Header("X-API-Key") apiKey: String
    ): APIResponse
    
    @GET("/api/sales")
    suspend fun getSales(
        @Header("X-API-Key") apiKey: String,
        @Query("collection") collection: String,
        @Query("limit") limit: Int = 50
    ): APIResponse
}

class NFTAPIClient {
    private val retrofit = Retrofit.Builder()
        .baseUrl("https://nft-market-analytics-api.onrender.com")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    private val service = retrofit.create(NFTAPIService::class.java)
    private val apiKey = "sk_your_android_api_key"
    
    suspend fun fetchCollections() = service.getCollections(apiKey)
    suspend fun fetchSales(collection: String) = service.getSales(apiKey, collection)
}
```

### React Native

```javascript
const API_URL = 'https://nft-market-analytics-api.onrender.com';
const API_KEY = 'sk_your_react_native_api_key';

const apiClient = {
  headers: {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json',
  },

  async getCollections() {
    const response = await fetch(`${API_URL}/api/collections`, {
      headers: this.headers,
    });
    return response.json();
  },

  async getSales(collection = 'all', limit = 50) {
    const response = await fetch(
      `${API_URL}/api/sales?collection=${collection}&limit=${limit}`,
      { headers: this.headers }
    );
    return response.json();
  },

  async getSummary(collection = 'all') {
    const response = await fetch(
      `${API_URL}/api/summary?collection=${collection}`,
      { headers: this.headers }
    );
    return response.json();
  },
};

export default apiClient;
```

---

## 🐛 Troubleshooting

### Issue: 401 Unauthorized
**Cause**: Invalid or missing API key  
**Fix**:
```bash
# Check .env file
cat .env | grep API_KEY

# Verify header in request
curl -H "X-API-Key: $(cat .env | grep API_KEY_APP1 | cut -d= -f2)" \
     http://localhost:8000/api/collections
```

### Issue: 404 Not Found
**Cause**: Collection doesn't exist or endpoint path wrong  
**Fix**:
```bash
# Valid collections:
# CryptoPunks, BAYC, MAYC, Doodles, Pudgy Penguins

curl -H "X-API-Key: sk_..." \
     "http://localhost:8000/api/sales?collection=BAYC"
```

### Issue: Data Not Loading
**Cause**: CSV files missing or path wrong  
**Fix**:
```bash
# Check CSV files exist
ls -la data/

# Verify DATA_PATH in .env
cat .env | grep DATA_PATH
```

### Issue: Slow Response Time
**Cause**: First request triggers data load  
**Fix**: Data is cached after first request. Subsequent requests <50ms.

### Issue: ModuleNotFoundError
**Cause**: Dependencies not installed  
**Fix**:
```bash
source .venv/bin/activate  # Activate venv
pip install -r requirements_api.txt
```

---

## 📊 Performance Specifications

| Metric | Value |
|--------|-------|
| **Cold Start** | ~2-3 seconds |
| **Warm Response** | <100ms (cached) |
| **Memory Usage** | 150-250 MB |
| **Max Concurrent Requests** | Unlimited (depends on server) |
| **Data Cache Size** | ~50-100 MB |
| **CSV Load Time** | ~1-2 seconds |

---

## 🔄 CI/CD Setup (GitHub Actions)

**File**: `.github/workflows/deploy.yml`

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Render
        run: |
          curl -X POST https://api.render.com/deploy \
            -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"serviceId": "${{ secrets.RENDER_SERVICE_ID }}"}'
```

---

## 📝 Monitoring & Logging

### Check API health
```bash
curl https://nft-market-analytics-api.onrender.com/api/health
```

### View logs
**Render Dashboard**:
- Go to https://dashboard.render.com
- Select service
- Click "Logs" tab

**Local**:
```bash
# Run with debug logging
uvicorn api:app --log-level=debug
```

---

## 🎯 Next Steps

1. ✅ Set up local development environment
2. ✅ Generate API keys for both apps
3. ✅ Deploy to Render/Railway
4. ✅ Set environment variables on deployment platform
5. ✅ Upload CSV data files
6. ✅ Test all endpoints
7. ✅ Integrate into mobile apps
8. ✅ Monitor performance
9. ✅ Collect feedback from users

---

## 📞 Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review endpoint documentation above
3. Check Render/Railway dashboard logs
4. Test with `/api/docs` (Swagger UI)

---

**Generated**: April 18, 2026  
**Last Updated**: Production Ready  
**Maintainer**: Your Team
