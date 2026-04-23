# API Key Usage Guide for NFT Market Analytics

## 📖 Table of Contents
1. [Setup API Keys](#setup-api-keys)
2. [Using API Keys in Apps](#using-api-keys-in-apps)
3. [Testing Endpoints](#testing-endpoints)
4. [Mobile App Integration](#mobile-app-integration)
5. [Best Practices & Security](#best-practices--security)

---

## 🔑 Setup API Keys

### Step 1: Generate Strong API Keys

Generate two secure API keys (one per mobile app):

```bash
# Generate first key
openssl rand -hex 32
# Output: abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567

# Generate second key
openssl rand -hex 32
# Output: xyz789abc012def345ghi678jkl901mno234pqr567stu890vwx123
```

### Step 2: Create .env File

Create a `.env` file in the project root:

```bash
# API Keys (one per mobile app)
API_KEY_APP1=sk_your_first_key_here
API_KEY_APP2=sk_your_second_key_here

# Server Configuration
DATA_PATH=data
PORT=8000
HOST=0.0.0.0
ENV=development
```

### Step 3: Load Environment Variables

The API automatically loads from `.env` on startup:

```python
# config.py handles this automatically
from dotenv import load_dotenv
load_dotenv()
```

---

## 🚀 Using API Keys in Apps

### HTTP Header Format

All authenticated endpoints require the API key in the request header:

```
Header: X-API-Key
Value: sk_your_api_key_here
```

### Python Example

```python
import requests

API_URL = "http://localhost:8000"
API_KEY = "sk_your_api_key_here"

# Set header
headers = {
    "X-API-Key": API_KEY
}

# Example: Get all collections
response = requests.get(
    f"{API_URL}/api/collections",
    headers=headers
)

print(response.json())
# Output: 
# {
#   "status": "success",
#   "data": [
#     {"name": "CryptoPunks", "color": "#534AB7"},
#     {"name": "BAYC", "color": "#1D9E75"},
#     ...
#   ],
#   "count": 5,
#   "timestamp": "2026-04-23T10:00:00Z"
# }
```

### JavaScript/Node.js Example

```javascript
const API_URL = "http://localhost:8000";
const API_KEY = "sk_your_api_key_here";

// Fetch collections
const response = await fetch(`${API_URL}/api/collections`, {
  method: "GET",
  headers: {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
  }
});

const data = await response.json();
console.log(data);
```

### cURL Example

```bash
# Test API endpoint with cURL
curl -H "X-API-Key: sk_your_api_key_here" \
     http://localhost:8000/api/collections

# With pretty-printed JSON
curl -s -H "X-API-Key: sk_your_api_key_here" \
     http://localhost:8000/api/collections | jq .
```

### React Native / Flutter Example

**React Native (Axios)**:
```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: {
    "X-API-Key": "sk_your_api_key_here"
  }
});

// Usage
api.get("/api/collections")
  .then(res => console.log(res.data))
  .catch(err => console.error(err));
```

**Flutter (Dart)**:
```dart
import 'package:http/http.dart' as http;

Future<void> fetchCollections() async {
  final response = await http.get(
    Uri.parse('http://localhost:8000/api/collections'),
    headers: {
      'X-API-Key': 'sk_your_api_key_here',
    },
  );

  if (response.statusCode == 200) {
    print(response.body);
  } else {
    throw Exception('Failed to load collections');
  }
}
```

---

## 🧪 Testing Endpoints

### Method 1: Swagger UI (Interactive)

1. Start the API:
   ```bash
   uvicorn api:app --reload
   ```

2. Open browser:
   ```
   http://localhost:8000/api/docs
   ```

3. Click "Authorize" button
4. Enter your API key: `sk_your_api_key_here`
5. Try endpoints directly in the UI

### Method 2: Test All Endpoints

#### 1️⃣ Health Check (No Auth)

```bash
curl http://localhost:8000/api/health | jq .
```

**Response**:
```json
{
  "status": "operational",
  "timestamp": "2026-04-23T10:30:45Z",
  "version": "1.0.0"
}
```

---

#### 2️⃣ Get Collections

```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     http://localhost:8000/api/collections | jq .
```

**Response**:
```json
{
  "status": "success",
  "data": [
    {"name": "CryptoPunks", "color": "#534AB7"},
    {"name": "BAYC", "color": "#1D9E75"},
    {"name": "MAYC", "color": "#D85A30"},
    {"name": "Doodles", "color": "#BA7517"},
    {"name": "Pudgy Penguins", "color": "#D4537E"}
  ],
  "count": 5,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

---

#### 3️⃣ Get Sales Data

**Get all sales (first 50)**:
```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     "http://localhost:8000/api/sales?limit=50&offset=0" | jq .
```

**Get BAYC sales (paginated)**:
```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     "http://localhost:8000/api/sales?collection=BAYC&limit=10&offset=0" | jq .
```

**Query Parameters**:
| Parameter | Type | Description |
|-----------|------|-------------|
| `collection` | string | Collection name (CryptoPunks, BAYC, MAYC, Doodles, Pudgy Penguins) or "all" |
| `limit` | integer | Results per page (1-1000, default: 50) |
| `offset` | integer | Pagination offset (default: 0) |

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
    },
    {
      "identifier": 2,
      "name": "Bored Ape #2",
      "event_type": "sale",
      "price_eth": 98.75,
      "timestamp": "2024-01-16T09:15:00",
      "collection": "BAYC"
    }
  ],
  "count": 1250,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

---

#### 4️⃣ Get Volume Metrics

**All collections**:
```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     "http://localhost:8000/api/volume" | jq .
```

**Specific collection**:
```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     "http://localhost:8000/api/volume?collection=BAYC" | jq .
```

**Response**:
```json
{
  "status": "success",
  "collection": null,
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

---

#### 5️⃣ Get Trends

```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     "http://localhost:8000/api/trends?collection=BAYC" | jq .
```

**Response**:
```json
{
  "status": "success",
  "collection": "BAYC",
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

---

#### 6️⃣ Get Events

```bash
curl -H "X-API-Key: sk_your_api_key_here" \
     "http://localhost:8000/api/events?collection=BAYC" | jq .
```

**Response**:
```json
{
  "status": "success",
  "collection": "BAYC",
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

---

## 📱 Mobile App Integration

### Step 1: Store API Key Securely

**React Native (AsyncStorage)**:
```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';

// Store API key
await AsyncStorage.setItem('apiKey', 'sk_your_api_key_here');

// Retrieve API key
const apiKey = await AsyncStorage.getItem('apiKey');
```

**Flutter (SharedPreferences)**:
```dart
import 'package:shared_preferences/shared_preferences.dart';

// Store API key
final prefs = await SharedPreferences.getInstance();
await prefs.setString('apiKey', 'sk_your_api_key_here');

// Retrieve API key
final apiKey = prefs.getString('apiKey');
```

### Step 2: Create API Client

**React Native Example**:
```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

class NFTApiClient {
  constructor(baseURL = 'https://api.nftanalytics.com') {
    this.baseURL = baseURL;
    this.apiKey = null;
  }

  async init() {
    this.apiKey = await AsyncStorage.getItem('apiKey');
    if (!this.apiKey) {
      throw new Error('API key not found. Please login first.');
    }
  }

  async get(endpoint, params = {}) {
    const response = await axios.get(`${this.baseURL}${endpoint}`, {
      headers: { 'X-API-Key': this.apiKey },
      params,
    });
    return response.data;
  }

  async getCollections() {
    return this.get('/api/collections');
  }

  async getSales(collection = 'all', limit = 50, offset = 0) {
    return this.get('/api/sales', { collection, limit, offset });
  }

  async getVolume(collection = 'all') {
    return this.get('/api/volume', { collection });
  }

  async getTrends(collection = 'all') {
    return this.get('/api/trends', { collection });
  }

  async getEvents(collection = 'all') {
    return this.get('/api/events', { collection });
  }
}

// Usage
const client = new NFTApiClient();
await client.init();
const collections = await client.getCollections();
```

### Step 3: Use in Components

**React Native with React Query**:
```javascript
import { useQuery } from '@tanstack/react-query';

function CollectionsScreen() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['collections'],
    queryFn: async () => {
      const client = new NFTApiClient();
      await client.init();
      return client.getCollections();
    },
  });

  if (isLoading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error.message}</Text>;

  return (
    <ScrollView>
      {data.data.map(collection => (
        <Text key={collection.name}>{collection.name}</Text>
      ))}
    </ScrollView>
  );
}
```

---

## 🔒 Best Practices & Security

### ✅ DO's

1. **Use Environment Variables**
   ```bash
   # Store keys in .env (never commit to git)
   API_KEY_APP1=sk_xxx
   API_KEY_APP2=sk_yyy
   ```

2. **Add to .gitignore**
   ```
   .env
   .env.local
   *.key
   ```

3. **Rotate Keys Regularly**
   - Generate new keys every 90 days
   - Update in deployment platform (Render, Railway, etc.)
   - Remove old keys

4. **Use HTTPS in Production**
   ```python
   # config.py
   ENV = os.getenv("ENV", "production")  # Must be "production" on live
   ```

5. **Separate Keys Per App**
   - `API_KEY_APP1` for iOS app
   - `API_KEY_APP2` for Android app
   - Easier to revoke if one is compromised

### ❌ DON'Ts

1. **Never hardcode keys in code**
   ```javascript
   // ❌ WRONG
   const API_KEY = "sk_your_key_here";
   
   // ✅ CORRECT
   const API_KEY = process.env.API_KEY;
   ```

2. **Never commit .env to git**
   ```bash
   # Add to .gitignore
   echo ".env" >> .gitignore
   ```

3. **Never share keys in messages/emails**
   - Use secure password managers
   - Share only with team members who need them
   - Use deployment platform's secret management

4. **Never expose keys in client-side code**
   - Always route through backend
   - Use proxy/gateway in production

### Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| `200` | Success | Use returned data |
| `400` | Bad Request | Check query parameters |
| `401` | Unauthorized | Verify API key in header |
| `404` | Not Found | Check if collection exists |
| `500` | Server Error | Check data loading issues |

**Error Response Example**:
```json
{
  "detail": "Invalid or missing API key. Provide valid X-API-Key header."
}
```

---

## 🧪 Complete Test Script

Save as `test_api.sh`:

```bash
#!/bin/bash

API_URL="http://localhost:8000"
API_KEY="sk_your_api_key_here"

echo "🧪 Testing NFT Market Analytics API"
echo "===================================="

# Test 1: Health Check
echo -e "\n1️⃣  Health Check (no auth)..."
curl -s "$API_URL/api/health" | jq .

# Test 2: Collections
echo -e "\n2️⃣  Get Collections..."
curl -s -H "X-API-Key: $API_KEY" "$API_URL/api/collections" | jq .

# Test 3: Sales
echo -e "\n3️⃣  Get BAYC Sales (limit 5)..."
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/sales?collection=BAYC&limit=5" | jq .

# Test 4: Volume
echo -e "\n4️⃣  Get Volume Metrics..."
curl -s -H "X-API-Key: $API_KEY" "$API_URL/api/volume" | jq .

# Test 5: Trends
echo -e "\n5️⃣  Get Trends..."
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/trends?collection=CryptoPunks" | jq .

# Test 6: Events
echo -e "\n6️⃣  Get Events..."
curl -s -H "X-API-Key: $API_KEY" \
     "$API_URL/api/events?collection=MAYC" | jq .

echo -e "\n✅ All tests completed!"
```

Run it:
```bash
chmod +x test_api.sh
./test_api.sh
```

---

## 📞 Support

For issues:
1. Check `/api/docs` Swagger UI
2. Review error messages in API logs
3. Verify API key is set in `.env`
4. Check data files exist in `data/` folder
5. Run tests with `test_api.sh`
