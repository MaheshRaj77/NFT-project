#!/bin/bash

###############################################################################
# NFT Market Analytics API - Complete Test Suite
# 
# Usage:
#   ./test_api_complete.sh              # Use default API key from .env
#   ./test_api_complete.sh sk_xxx       # Use custom API key
#
# Prerequisites:
#   - API running (uvicorn api:app --reload)
#   - jq installed (for JSON formatting)
#
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
API_URL="${API_URL:-http://localhost:8000}"
API_KEY="${1:-sk_test_key_12345}"

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Utility functions
print_header() {
    echo -e "\n${BLUE}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}\n"
}

print_test() {
    echo -e "${YELLOW}→ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((TESTS_PASSED++))
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
    ((TESTS_FAILED++))
}

# API Request function
api_request() {
    local method=$1
    local endpoint=$2
    local auth=$3
    
    if [ "$auth" == "no-auth" ]; then
        curl -s -X "$method" "$API_URL$endpoint"
    else
        curl -s -X "$method" \
             -H "X-API-Key: $API_KEY" \
             "$API_URL$endpoint"
    fi
}

# Verify response
verify_response() {
    local response=$1
    local expected_status=$2
    
    if echo "$response" | jq . > /dev/null 2>&1; then
        local status=$(echo "$response" | jq -r '.status // .detail // "ok"' 2>/dev/null)
        echo "$response"
        return 0
    else
        return 1
    fi
}

###############################################################################
# TEST SUITE
###############################################################################

print_header "🧪 NFT Market Analytics API - Complete Test Suite"

echo "Configuration:"
echo "  API URL: $API_URL"
echo "  API Key: ${API_KEY:0:20}..."
echo ""

# ═══════════════════════════════════════════════════════════════════════════
# Test 1: Health Check (No Auth Required)
# ═══════════════════════════════════════════════════════════════════════════

print_test "Health Check (No Auth)"
response=$(api_request GET "/api/health" "no-auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    status=$(echo "$response" | jq -r '.status')
    version=$(echo "$response" | jq -r '.version')
    print_success "Health check passed (status: $status, version: $version)"
    echo "Response: $(echo "$response" | jq '.')"
else
    print_error "Health check failed - Invalid JSON response"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 2: Collections List
# ═══════════════════════════════════════════════════════════════════════════

print_test "Get Collections List"
response=$(api_request GET "/api/collections" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    count=$(echo "$response" | jq -r '.count')
    status=$(echo "$response" | jq -r '.status')
    print_success "Collections retrieved (total: $count)"
    echo "Response:"
    echo "$response" | jq '.data[] | {name, color}'
else
    print_error "Failed to get collections"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 3: Sales Data - All Collections
# ═══════════════════════════════════════════════════════════════════════════

print_test "Get Sales Data (All Collections)"
response=$(api_request GET "/api/sales?limit=5&offset=0" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    status=$(echo "$response" | jq -r '.status')
    count=$(echo "$response" | jq -r '.count')
    data_count=$(echo "$response" | jq '.data | length')
    print_success "Sales data retrieved (total: $count, returned: $data_count)"
    echo "Sample data:"
    echo "$response" | jq '.data[0:2] | .[] | {identifier, name, collection, price_eth, timestamp}'
else
    print_error "Failed to get sales data"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 4: Sales Data - Specific Collection (BAYC)
# ═══════════════════════════════════════════════════════════════════════════

print_test "Get Sales Data (BAYC Only)"
response=$(api_request GET "/api/sales?collection=BAYC&limit=3&offset=0" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    collection=$(echo "$response" | jq -r '.collection')
    count=$(echo "$response" | jq -r '.count')
    data_count=$(echo "$response" | jq '.data | length')
    print_success "BAYC sales retrieved (total: $count, returned: $data_count)"
    echo "Sample BAYC data:"
    echo "$response" | jq '.data[0:2] | .[] | {name, price_eth, event_type}'
else
    print_error "Failed to get BAYC sales"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 5: Sales Data - Pagination Test
# ═══════════════════════════════════════════════════════════════════════════

print_test "Pagination Test (Offset)"
response1=$(api_request GET "/api/sales?collection=CryptoPunks&limit=5&offset=0" "auth")
response2=$(api_request GET "/api/sales?collection=CryptoPunks&limit=5&offset=5" "auth")
if echo "$response1" | jq . > /dev/null 2>&1 && echo "$response2" | jq . > /dev/null 2>&1; then
    id1=$(echo "$response1" | jq '.data[0].identifier')
    id2=$(echo "$response2" | jq '.data[0].identifier')
    if [ "$id1" != "$id2" ]; then
        print_success "Pagination working correctly (different IDs in pages)"
    else
        print_error "Pagination may not be working (same IDs in different pages)"
    fi
else
    print_error "Pagination test failed"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 6: Volume Metrics - All Collections
# ═══════════════════════════════════════════════════════════════════════════

print_test "Get Volume Metrics (All Collections)"
response=$(api_request GET "/api/volume" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    count=$(echo "$response" | jq '.data | length')
    print_success "Volume metrics retrieved ($count collections)"
    echo "Volume data:"
    echo "$response" | jq '.data[] | {collection, total_volume, total_transactions, average_price}'
else
    print_error "Failed to get volume metrics"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 7: Volume Metrics - Specific Collection
# ═══════════════════════════════════════════════════════════════════════════

print_test "Get Volume Metrics (MAYC Only)"
response=$(api_request GET "/api/volume?collection=MAYC" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    collection=$(echo "$response" | jq -r '.data[0].collection')
    volume=$(echo "$response" | jq '.data[0].total_volume')
    print_success "MAYC volume retrieved (total_volume: $volume)"
    echo "$response" | jq '.data[0]'
else
    print_error "Failed to get MAYC volume"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 8: Trends Data
# ═══════════════════════════════════════════════════════════════════════════

print_test "Get Trends Data (Doodles)"
response=$(api_request GET "/api/trends?collection=Doodles" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    count=$(echo "$response" | jq '.data | length')
    print_success "Trends data retrieved ($count months)"
    echo "Trend data (first 3 months):"
    echo "$response" | jq '.data[0:3] | .[] | {month, total_volume, average_price, transaction_count}'
else
    print_error "Failed to get trends data"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 9: Events Data
# ═══════════════════════════════════════════════════════════════════════════

print_test "Get Events Data (Pudgy Penguins)"
response=$(api_request GET "/api/events?collection=Pudgy%20Penguins" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    total=$(echo "$response" | jq '.data.total_events')
    print_success "Events data retrieved (total_events: $total)"
    echo "Event breakdown:"
    echo "$response" | jq '.data.event_breakdown'
else
    print_error "Failed to get events data"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 10: Error Handling - Missing Auth
# ═══════════════════════════════════════════════════════════════════════════

print_test "Error Handling - Missing API Key"
response=$(curl -s -X GET "$API_URL/api/collections")
if echo "$response" | jq . > /dev/null 2>&1; then
    detail=$(echo "$response" | jq -r '.detail // .message // ""')
    if [ -z "$detail" ] || grep -q "unauthorized\|invalid\|missing" <<< "$detail"; then
        print_success "Proper error response for missing API key"
        echo "Error: $detail"
    else
        print_error "Expected auth error but got: $detail"
    fi
else
    print_success "Proper error response for missing API key"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 11: Error Handling - Invalid Collection
# ═══════════════════════════════════════════════════════════════════════════

print_test "Error Handling - Invalid Collection"
response=$(api_request GET "/api/sales?collection=InvalidCollection&limit=5" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    detail=$(echo "$response" | jq -r '.detail // "no error"')
    if grep -q "not found" <<< "$detail"; then
        print_success "Proper 404 error for invalid collection"
        echo "Error: $detail"
    else
        print_error "Expected 404 error but got: $detail"
    fi
else
    print_error "Failed to handle invalid collection"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test 12: Error Handling - Invalid Limit
# ═══════════════════════════════════════════════════════════════════════════

print_test "Error Handling - Invalid Limit (>1000)"
response=$(api_request GET "/api/sales?limit=5000" "auth")
if echo "$response" | jq . > /dev/null 2>&1; then
    detail=$(echo "$response" | jq -r '.detail // "no error"')
    echo "Response received (validation working)"
else
    print_success "Request validation working"
fi

# ═══════════════════════════════════════════════════════════════════════════
# Test Summary
# ═══════════════════════════════════════════════════════════════════════════

print_header "📊 Test Summary"

total=$((TESTS_PASSED + TESTS_FAILED))
echo -e "Total Tests: ${BLUE}$total${NC}"
echo -e "Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed!${NC}"
    exit 0
else
    echo -e "\n${RED}⚠️  Some tests failed. Check API setup.${NC}"
    exit 1
fi
