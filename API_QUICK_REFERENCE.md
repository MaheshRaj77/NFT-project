# API Documentation & Testing Guide - Quick Reference

Created: April 23, 2026

## 📚 New Documentation Files

### 1. **API_KEY_GUIDE.md** (Comprehensive Guide)
Complete guide for API key usage and endpoint testing.

**Contains:**
- ✅ Setup API Keys (generate, store in .env)
- ✅ Using API Keys in Apps (Python, JavaScript, React Native, Flutter)
- ✅ Testing All Endpoints (with cURL examples)
- ✅ Mobile App Integration (secure storage & API client)
- ✅ Best Practices & Security (DO's and DON'Ts)
- ✅ Error Handling Guide
- ✅ Complete Test Script

**Location:** `API_KEY_GUIDE.md`

---

## 🧪 Testing Files

### 2. **test_api_complete.sh** (Bash Test Suite)
Automated shell script for testing all endpoints.

**Features:**
- ✅ 12 comprehensive tests
- ✅ Color-coded output
- ✅ Health check, collections, sales, volume, trends, events
- ✅ Pagination testing
- ✅ Error handling tests
- ✅ Test summary with pass/fail counts

**Usage:**
```bash
chmod +x test_api_complete.sh
./test_api_complete.sh                    # Use default key
./test_api_complete.sh sk_your_key_here   # Use custom key
```

**Location:** `test_api_complete.sh`

---

### 3. **test_api_complete.py** (Python Test Suite)
Complete Python test framework for API testing.

**Features:**
- ✅ Object-oriented test class
- ✅ Reusable API client
- ✅ 10 comprehensive tests
- ✅ JSON output support
- ✅ Verbose mode for debugging
- ✅ Detailed error messages

**Usage:**
```bash
# Basic testing
python test_api_complete.py

# With custom API URL
python test_api_complete.py --api-url http://localhost:8000 --api-key sk_xxx

# Verbose mode
python test_api_complete.py --verbose

# JSON output
python test_api_complete.py --json > results.json
```

**Location:** `test_api_complete.py`

---

## 🔑 Quick Setup (5 Minutes)

### Step 1: Generate API Keys
```bash
openssl rand -hex 32  # Generate first key
openssl rand -hex 32  # Generate second key
```

### Step 2: Create .env
```bash
API_KEY_APP1=sk_your_first_key_here
API_KEY_APP2=sk_your_second_key_here
DATA_PATH=data
PORT=8000
ENV=development
```

### Step 3: Run API
```bash
uvicorn api:app --reload
```

### Step 4: Test Endpoints
```bash
# Option A: Interactive Swagger UI
# Open: http://localhost:8000/api/docs

# Option B: Bash tests
./test_api_complete.sh

# Option C: Python tests
python test_api_complete.py
```

---

## 📡 All API Endpoints

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/api/health` | GET | No | Health check |
| `/api/collections` | GET | Yes | List all NFT collections |
| `/api/sales` | GET | Yes | Get sales transactions (Level 3 data) |
| `/api/volume` | GET | Yes | Get volume metrics (Level 4 aggregates) |
| `/api/trends` | GET | Yes | Get monthly trends |
| `/api/events` | GET | Yes | Get event type breakdown |

---

## 🎯 Common Tasks

### Task 1: Get Collections
```bash
curl -H "X-API-Key: sk_xxx" http://localhost:8000/api/collections
```

### Task 2: Get BAYC Sales (Paginated)
```bash
curl -H "X-API-Key: sk_xxx" \
     "http://localhost:8000/api/sales?collection=BAYC&limit=10&offset=0"
```

### Task 3: Get Volume Metrics
```bash
curl -H "X-API-Key: sk_xxx" http://localhost:8000/api/volume
```

### Task 4: Check API Status
```bash
curl http://localhost:8000/api/health
```

---

## 🚀 Integration Examples

### React Native
```javascript
const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "X-API-Key": "sk_your_key_here" }
});
api.get("/api/collections").then(res => console.log(res.data));
```

### Flutter
```dart
http.get(
  Uri.parse('http://localhost:8000/api/collections'),
  headers: { 'X-API-Key': 'sk_your_key_here' },
).then((response) => print(response.body));
```

### Python
```python
import requests
headers = {"X-API-Key": "sk_your_key_here"}
response = requests.get("http://localhost:8000/api/collections", headers=headers)
print(response.json())
```

---

## 🔒 Security Checklist

- [ ] Generate strong API keys using `openssl rand -hex 32`
- [ ] Store keys in `.env` file (not in code)
- [ ] Add `.env` to `.gitignore`
- [ ] Use HTTPS in production (not HTTP)
- [ ] Rotate keys every 90 days
- [ ] Use separate keys per app (APP1 for iOS, APP2 for Android)
- [ ] Never share keys in emails/messages
- [ ] Monitor API usage logs

---

## 📊 Response Format

All endpoints return standardized JSON:

```json
{
  "status": "success",
  "collection": "BAYC",
  "data": [...],
  "count": 1250,
  "timestamp": "2026-04-23T10:30:45Z"
}
```

**Error Response:**
```json
{
  "detail": "Invalid or missing API key. Provide valid X-API-Key header."
}
```

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check X-API-Key header is present |
| 404 Collection Not Found | Verify collection name (case-sensitive) |
| 500 Server Error | Check data files exist in `data/` folder |
| API not responding | Verify `uvicorn api:app --reload` is running |
| Test script fails | Run `chmod +x test_api_complete.sh` first |

---

## 📞 References

- **API Documentation:** `README_API.md`
- **Architecture:** `ARCHITECTURE.md`
- **Project Context:** `PROJECT_CONTEXT.md`
- **Setup Guide:** `SETUP.md`
- **Swagger UI:** http://localhost:8000/api/docs
- **ReDoc:** http://localhost:8000/api/redoc

---

## 📝 Documentation Structure

```
NFT-Project/
├── API_KEY_GUIDE.md              ← NEW: Complete API key guide
├── test_api_complete.sh          ← NEW: Bash test suite
├── test_api_complete.py          ← NEW: Python test suite
├── API_QUICK_REFERENCE.md        ← NEW: This file
├── README_API.md                 ← Existing API docs
├── ARCHITECTURE.md               ← Existing architecture
├── api.py                        ← API implementation
├── config.py                     ← Configuration & API key validation
└── .env.example                  ← Environment variables template
```

---

## 🎯 Next Steps

1. **Review API_KEY_GUIDE.md** for detailed instructions
2. **Run test scripts** to verify setup:
   ```bash
   ./test_api_complete.sh          # Bash version
   python test_api_complete.py     # Python version
   ```
3. **Test in Swagger UI:** http://localhost:8000/api/docs
4. **Integrate into apps** using examples provided
5. **Monitor security** and rotate keys regularly

---

**Status:** ✅ Complete Documentation Ready  
**Last Updated:** April 23, 2026  
**Version:** 1.0.0
