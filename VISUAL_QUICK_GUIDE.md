# 🎯 API Key & Testing - Visual Quick Guide

## 🔑 API Key Setup Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    API KEY SETUP FLOW                              │
└─────────────────────────────────────────────────────────────────────┘

STEP 1: Generate Keys
│
├─ Run: openssl rand -hex 32
├─ Run: openssl rand -hex 32
└─ You get two keys: sk_app1_xxx and sk_app2_xxx

     ↓

STEP 2: Store in .env
│
├─ Create .env file
├─ Add: API_KEY_APP1=sk_app1_xxx
├─ Add: API_KEY_APP2=sk_app2_xxx
├─ Add: DATA_PATH=data
└─ Add: ENV=development

     ↓

STEP 3: Start API
│
└─ Run: uvicorn api:app --reload
└─ You see: ✓ Application startup complete

     ↓

STEP 4: Test It
│
├─ Option A: bash test
│   └─ ./test_api_complete.sh
│
├─ Option B: python test
│   └─ python test_api_complete.py
│
└─ Option C: browser
    └─ http://localhost:8000/api/docs

     ↓

✅ DONE! API Ready
```

---

## 📡 Making API Requests

```
┌─────────────────────────────────────────────────────────────────────┐
│              API REQUEST STRUCTURE                                 │
└─────────────────────────────────────────────────────────────────────┘

REQUEST FORMAT:
┌──────────────────────────────────────────┐
│ METHOD: GET                              │
│ URL: http://localhost:8000/api/endpoint  │
│ HEADER: X-API-Key: sk_your_key_here     │
│ PARAMS: ?collection=BAYC&limit=10       │
└──────────────────────────────────────────┘
        ↓
     SEND
        ↓
┌──────────────────────────────────────────┐
│ RESPONSE:                                │
│ Status: 200 OK                          │
│ Body: {                                 │
│   "status": "success",                 │
│   "data": [...],                       │
│   "count": 1250,                       │
│   "timestamp": "2026-04-23T10:30:45Z"  │
│ }                                      │
└──────────────────────────────────────────┘

EXAMPLES:

🟢 GET /api/health (NO AUTH)
   curl http://localhost:8000/api/health

🟢 GET /api/collections (WITH AUTH)
   curl -H "X-API-Key: sk_xxx" \
        http://localhost:8000/api/collections

🟢 GET /api/sales?collection=BAYC
   curl -H "X-API-Key: sk_xxx" \
        "http://localhost:8000/api/sales?collection=BAYC&limit=10"
```

---

## 📊 All Endpoints at a Glance

```
┌──────────────────────────────────────────────────────────────────────┐
│                      ENDPOINT REFERENCE                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  🔓 /api/health (NO AUTH)                                           │
│     ├─ GET: Server status                                           │
│     └─ Response: {status, version, timestamp}                       │
│                                                                      │
│  🔐 /api/collections                                                │
│     ├─ GET: List all NFT collections                                │
│     └─ Response: [{name, color}, ...]                               │
│                                                                      │
│  🔐 /api/sales                                                      │
│     ├─ GET: Get sale transactions                                   │
│     ├─ Params: collection, limit, offset                            │
│     └─ Response: [{name, price_eth, timestamp}, ...]                │
│                                                                      │
│  🔐 /api/volume                                                     │
│     ├─ GET: Get volume metrics                                      │
│     ├─ Params: collection                                           │
│     └─ Response: [{collection, total_volume, avg_price}, ...]       │
│                                                                      │
│  🔐 /api/trends                                                     │
│     ├─ GET: Get monthly trends                                      │
│     ├─ Params: collection                                           │
│     └─ Response: [{month, total_volume, avg_price}, ...]            │
│                                                                      │
│  🔐 /api/events                                                     │
│     ├─ GET: Get event breakdown                                     │
│     ├─ Params: collection                                           │
│     └─ Response: {total_events, event_breakdown}                    │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 💻 Code Template - Pick Your Framework

```
┌──────────────────────────────────────────────────────────────────────┐
│                   FRAMEWORK TEMPLATES                               │
└──────────────────────────────────────────────────────────────────────┘

🐍 PYTHON
─────────────────────────────────────────────────────────────────────
import requests

headers = {"X-API-Key": "sk_your_key"}
response = requests.get(
    "http://localhost:8000/api/collections",
    headers=headers
)
print(response.json())

📘 JAVASCRIPT
─────────────────────────────────────────────────────────────────────
const response = await fetch(
  "http://localhost:8000/api/collections",
  {
    headers: { "X-API-Key": "sk_your_key" }
  }
);
const data = await response.json();
console.log(data);

⚛️  REACT NATIVE
─────────────────────────────────────────────────────────────────────
import axios from 'axios';

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "X-API-Key": "sk_your_key" }
});

api.get("/api/collections")
  .then(res => console.log(res.data));

🐦 FLUTTER
─────────────────────────────────────────────────────────────────────
import 'package:http/http.dart' as http;

http.get(
  Uri.parse('http://localhost:8000/api/collections'),
  headers: { 'X-API-Key': 'sk_your_key' },
).then((response) => print(response.body));
```

---

## 🧪 Testing Flowchart

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST WORKFLOW                               │
└─────────────────────────────────────────────────────────────────┘

START
  │
  ├─→ Health Check: /api/health
  │   └─ GET: http://localhost:8000/api/health
  │   └─ Status: 200
  │
  ├─→ Collections: /api/collections
  │   ├─ GET with X-API-Key header
  │   └─ Should return 5 collections
  │
  ├─→ Sales: /api/sales
  │   ├─ GET with collection=BAYC
  │   └─ Check pagination (limit=5&offset=10)
  │
  ├─→ Volume: /api/volume
  │   ├─ GET with collection=all
  │   └─ Check total_volume field
  │
  ├─→ Trends: /api/trends
  │   ├─ GET with collection=Doodles
  │   └─ Check month field format
  │
  ├─→ Events: /api/events
  │   ├─ GET with collection=MAYC
  │   └─ Check percentage sums to 100%
  │
  └─→ Error Cases:
      ├─ Missing Auth: Should return 401
      ├─ Invalid Collection: Should return 404
      └─ Bad Params: Should validate

✅ ALL TESTS PASS → API READY
```

---

## 🔒 Security Checklist

```
┌─────────────────────────────────────────────────────────────────┐
│                  SECURITY CHECKLIST                            │
└─────────────────────────────────────────────────────────────────┘

SETUP
  ☐ Generated API keys with: openssl rand -hex 32
  ☐ Stored in .env file (not in code)
  ☐ Added .env to .gitignore
  ☐ Keys are at least 64 characters

DEVELOPMENT
  ☐ Using X-API-Key header
  ☐ Not logging API keys
  ☐ Using environment variables
  ☐ Separate keys per app (APP1, APP2)

DEPLOYMENT
  ☐ Using HTTPS (not HTTP)
  ☐ Environment set to "production"
  ☐ Keys stored in deployment platform secrets
  ☐ IP whitelisting enabled

MAINTENANCE
  ☐ Keys rotated every 90 days
  ☐ Old keys revoked after rotation
  ☐ Usage logs monitored
  ☐ Suspicious activity reviewed
```

---

## 📚 Documentation Map

```
┌─────────────────────────────────────────────────────────────────┐
│         WHERE TO FIND WHAT YOU NEED                            │
└─────────────────────────────────────────────────────────────────┘

QUESTION                          → DOCUMENT
──────────────────────────────────────────────────────────────────
I'm new, where do I start?       → API_QUICK_REFERENCE.md
How do I generate API keys?      → API_KEY_GUIDE.md (Setup)
How do I use the key in Python?  → API_KEY_GUIDE.md (Examples)
How do I test an endpoint?       → ENDPOINT_TESTING_GUIDE.md
I want a quick command           → API_QUICK_REFERENCE.md
I need to integrate with React   → API_KEY_GUIDE.md (React Native)
API not responding?              → API_QUICK_REFERENCE.md
I want automated tests           → Run ./test_api_complete.sh
Can I see all endpoints?         → API_QUICK_REFERENCE.md
Security best practices?         → API_KEY_GUIDE.md (Security)
```

---

## ⚡ Quick Commands

```
┌──────────────────────────────────────────────────────────────────┐
│                  QUICK COMMANDS                                 │
└──────────────────────────────────────────────────────────────────┘

Generate API Key:
  $ openssl rand -hex 32

Start API:
  $ uvicorn api:app --reload

Health Check:
  $ curl http://localhost:8000/api/health

Get Collections:
  $ curl -H "X-API-Key: $API_KEY" http://localhost:8000/api/collections

Get BAYC Sales:
  $ curl -H "X-API-Key: $API_KEY" \
         "http://localhost:8000/api/sales?collection=BAYC"

Run Bash Tests:
  $ chmod +x test_api_complete.sh
  $ ./test_api_complete.sh

Run Python Tests:
  $ python test_api_complete.py

Open Swagger:
  $ open http://localhost:8000/api/docs
```

---

## 🎯 Common Errors & Fixes

```
┌──────────────────────────────────────────────────────────────────┐
│              COMMON ERRORS & SOLUTIONS                          │
└──────────────────────────────────────────────────────────────────┘

ERROR 1: 401 Unauthorized
  ├─ Cause: Missing or invalid API key
  ├─ Check: X-API-Key header is present
  └─ Fix: curl -H "X-API-Key: sk_xxx" ...

ERROR 2: 404 Collection Not Found
  ├─ Cause: Wrong collection name (case-sensitive)
  ├─ Wrong: bayc (lowercase)
  └─ Fix: BAYC (uppercase)

ERROR 3: 500 Internal Server Error
  ├─ Cause: Data files not found
  ├─ Check: ls -la data/
  └─ Fix: Copy data files to data/ folder

ERROR 4: Connection Refused
  ├─ Cause: API not running
  ├─ Check: Is uvicorn running?
  └─ Fix: uvicorn api:app --reload

ERROR 5: command not found: test_api_complete.sh
  ├─ Cause: Script not executable
  ├─ Check: ls -la test_api_complete.sh
  └─ Fix: chmod +x test_api_complete.sh
```

---

## 📈 Request/Response Flow

```
REQUEST:
┌────────────────────────────────────┐
│ GET /api/sales?collection=BAYC     │
│ X-API-Key: sk_your_key_here        │
│ Accept: application/json           │
└────────────────────────────────────┘
         │
         ├─→ Validate API Key
         │   └─ ✓ Valid
         │
         ├─→ Validate Collection
         │   └─ ✓ BAYC exists
         │
         ├─→ Load Data
         │   └─ ✓ CSV loaded from cache
         │
         ├─→ Filter & Paginate
         │   └─ ✓ Returned 50 items
         │
         └─→ Format Response
             └─ ✓ JSON encoded

RESPONSE:
┌────────────────────────────────────┐
│ HTTP/1.1 200 OK                    │
│ Content-Type: application/json     │
│                                    │
│ {                                  │
│   "status": "success",             │
│   "collection": "BAYC",            │
│   "data": [...],                   │
│   "count": 3456,                   │
│   "timestamp": "..."               │
│ }                                  │
└────────────────────────────────────┘
```

---

## 🚀 Next Steps

```
YOUR JOURNEY:

1️⃣  READ THIS FILE (Done! ✓)

2️⃣  QUICK SETUP (5 minutes)
    ├─ Generate API keys
    ├─ Create .env
    └─ Start API

3️⃣  RUN TESTS (30 seconds)
    ├─ ./test_api_complete.sh
    └─ See: ✅ All tests passed!

4️⃣  PICK A FRAMEWORK
    ├─ Python / JavaScript / Flutter / React Native
    └─ Copy example code

5️⃣  BUILD YOUR APP
    ├─ Add API calls to your app
    ├─ Handle errors gracefully
    └─ Test thoroughly

6️⃣  DEPLOY TO PRODUCTION
    ├─ Generate new API keys
    ├─ Set environment to "production"
    ├─ Use HTTPS
    └─ Monitor usage

✅ SUCCESS!
```

---

**Start with step 1 above or jump to any section you need! 🚀**
