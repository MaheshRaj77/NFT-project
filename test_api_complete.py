#!/usr/bin/env python3
"""
NFT Market Analytics API - Complete Python Test Suite

Usage:
    python test_api_complete.py                           # Use default settings
    python test_api_complete.py --api-url http://localhost:8000 --api-key sk_xxx
    python test_api_complete.py --json                    # Output as JSON
    python test_api_complete.py --verbose                 # Verbose output

Prerequisites:
    pip install requests pytest
"""

import requests
import json
import sys
import argparse
from typing import Dict, Any, Tuple
from datetime import datetime
from urllib.parse import urljoin


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BOLD = '\033[1m'
    END = '\033[0m'


class NFTAPITester:
    """Test suite for NFT Market Analytics API"""
    
    def __init__(self, api_url: str = "http://localhost:8000", 
                 api_key: str = "sk_test_key_12345",
                 verbose: bool = False):
        """
        Initialize tester
        
        Args:
            api_url: Base API URL
            api_key: API key for authentication
            verbose: Print detailed output
        """
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.verbose = verbose
        self.tests_passed = 0
        self.tests_failed = 0
        self.results = []
    
    def print_header(self, text: str):
        """Print formatted header"""
        print(f"\n{Colors.BLUE}{'=' * 70}")
        print(f"{text}")
        print(f"{'=' * 70}{Colors.END}\n")
    
    def print_test(self, text: str):
        """Print test name"""
        print(f"{Colors.YELLOW}→ {text}{Colors.END}")
    
    def print_success(self, text: str):
        """Print success message"""
        print(f"{Colors.GREEN}✅ {text}{Colors.END}")
        self.tests_passed += 1
    
    def print_error(self, text: str):
        """Print error message"""
        print(f"{Colors.RED}❌ {text}{Colors.END}")
        self.tests_failed += 1
    
    def make_request(self, method: str, endpoint: str, 
                    auth: bool = True, params: Dict = None) -> Tuple[int, Dict]:
        """
        Make API request
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            auth: Include authorization header
            params: Query parameters
        
        Returns:
            Tuple of (status_code, response_data)
        """
        url = urljoin(self.api_url, endpoint)
        headers = {}
        
        if auth:
            headers['X-API-Key'] = self.api_key
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, params=params, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            if self.verbose:
                print(f"  → {method} {url}")
                if params:
                    print(f"  → Params: {params}")
                print(f"  → Status: {response.status_code}")
            
            try:
                data = response.json()
            except:
                data = {"raw": response.text}
            
            return response.status_code, data
        
        except requests.exceptions.RequestException as e:
            print(f"  {Colors.RED}Request failed: {e}{Colors.END}")
            return 0, {"error": str(e)}
    
    def assert_success(self, status: int, data: Dict, test_name: str) -> bool:
        """
        Assert successful response
        
        Args:
            status: HTTP status code
            data: Response data
            test_name: Test name for reporting
        
        Returns:
            bool: True if successful
        """
        if status == 200:
            self.print_success(test_name)
            return True
        else:
            detail = data.get('detail', data.get('message', 'Unknown error'))
            self.print_error(f"{test_name} - Status {status}: {detail}")
            return False
    
    def test_health_check(self):
        """Test 1: Health check (no auth required)"""
        self.print_test("Health Check (No Auth)")
        status, data = self.make_request('GET', '/api/health', auth=False)
        
        if self.assert_success(status, data, "Health check passed"):
            version = data.get('version', 'unknown')
            timestamp = data.get('timestamp', 'unknown')
            print(f"  Version: {version}")
            print(f"  Timestamp: {timestamp}")
            self.results.append({
                'test': 'Health Check',
                'status': 'PASS',
                'details': data
            })
        else:
            self.results.append({
                'test': 'Health Check',
                'status': 'FAIL',
                'details': data
            })
    
    def test_collections(self):
        """Test 2: Get collections"""
        self.print_test("Get Collections")
        status, data = self.make_request('GET', '/api/collections')
        
        if self.assert_success(status, data, "Collections retrieved"):
            count = data.get('count', 0)
            collections = data.get('data', [])
            print(f"  Total: {count} collections")
            for coll in collections:
                print(f"    • {coll.get('name')} ({coll.get('color')})")
            self.results.append({
                'test': 'Get Collections',
                'status': 'PASS',
                'count': count,
                'collections': [c['name'] for c in collections]
            })
        else:
            self.results.append({
                'test': 'Get Collections',
                'status': 'FAIL',
                'details': data
            })
    
    def test_sales_all(self):
        """Test 3: Get sales - all collections"""
        self.print_test("Get Sales (All Collections)")
        status, data = self.make_request('GET', '/api/sales', 
                                        params={'limit': 5, 'offset': 0})
        
        if self.assert_success(status, data, "Sales data retrieved"):
            count = data.get('count', 0)
            items = data.get('data', [])
            print(f"  Total records: {count}")
            print(f"  Returned: {len(items)} items")
            if items:
                first = items[0]
                print(f"  First item: {first.get('name')} - {first.get('price_eth')} ETH")
            self.results.append({
                'test': 'Get Sales (All)',
                'status': 'PASS',
                'count': count,
                'returned': len(items)
            })
        else:
            self.results.append({
                'test': 'Get Sales (All)',
                'status': 'FAIL',
                'details': data
            })
    
    def test_sales_by_collection(self, collection: str = 'BAYC'):
        """Test 4: Get sales - specific collection"""
        self.print_test(f"Get Sales ({collection} Only)")
        status, data = self.make_request('GET', '/api/sales',
                                        params={'collection': collection, 
                                               'limit': 3, 'offset': 0})
        
        if self.assert_success(status, data, f"{collection} sales retrieved"):
            count = data.get('count', 0)
            items = data.get('data', [])
            print(f"  Total {collection} records: {count}")
            print(f"  Returned: {len(items)} items")
            self.results.append({
                'test': f'Get Sales ({collection})',
                'status': 'PASS',
                'count': count
            })
        else:
            self.results.append({
                'test': f'Get Sales ({collection})',
                'status': 'FAIL',
                'details': data
            })
    
    def test_pagination(self):
        """Test 5: Pagination"""
        self.print_test("Pagination Test")
        status1, data1 = self.make_request('GET', '/api/sales',
                                          params={'collection': 'CryptoPunks',
                                                 'limit': 5, 'offset': 0})
        status2, data2 = self.make_request('GET', '/api/sales',
                                          params={'collection': 'CryptoPunks',
                                                 'limit': 5, 'offset': 5})
        
        if status1 == 200 and status2 == 200:
            items1 = data1.get('data', [])
            items2 = data2.get('data', [])
            
            if items1 and items2:
                id1 = items1[0].get('identifier')
                id2 = items2[0].get('identifier')
                
                if id1 != id2:
                    self.print_success("Pagination working correctly")
                    print(f"  Page 1 first ID: {id1}")
                    print(f"  Page 2 first ID: {id2}")
                    self.results.append({
                        'test': 'Pagination',
                        'status': 'PASS'
                    })
                else:
                    self.print_error("Pagination may not be working (same IDs)")
                    self.results.append({
                        'test': 'Pagination',
                        'status': 'FAIL',
                        'reason': 'Same IDs in different pages'
                    })
            else:
                self.print_error("Not enough data to test pagination")
                self.results.append({
                    'test': 'Pagination',
                    'status': 'FAIL',
                    'reason': 'Not enough data'
                })
        else:
            self.print_error("Pagination test failed")
            self.results.append({
                'test': 'Pagination',
                'status': 'FAIL'
            })
    
    def test_volume(self):
        """Test 6: Volume metrics"""
        self.print_test("Get Volume Metrics")
        status, data = self.make_request('GET', '/api/volume')
        
        if self.assert_success(status, data, "Volume metrics retrieved"):
            items = data.get('data', [])
            print(f"  Collections: {len(items)}")
            for item in items:
                coll = item.get('collection')
                volume = item.get('total_volume')
                print(f"    • {coll}: {volume} ETH")
            self.results.append({
                'test': 'Get Volume',
                'status': 'PASS',
                'collections': len(items)
            })
        else:
            self.results.append({
                'test': 'Get Volume',
                'status': 'FAIL',
                'details': data
            })
    
    def test_trends(self):
        """Test 7: Trends data"""
        self.print_test("Get Trends (Doodles)")
        status, data = self.make_request('GET', '/api/trends',
                                        params={'collection': 'Doodles'})
        
        if self.assert_success(status, data, "Trends data retrieved"):
            items = data.get('data', [])
            print(f"  Total months: {len(items)}")
            if items:
                print(f"  Latest month: {items[-1].get('month')}")
            self.results.append({
                'test': 'Get Trends',
                'status': 'PASS',
                'months': len(items)
            })
        else:
            self.results.append({
                'test': 'Get Trends',
                'status': 'FAIL',
                'details': data
            })
    
    def test_events(self):
        """Test 8: Events data"""
        self.print_test("Get Events (Pudgy Penguins)")
        status, data = self.make_request('GET', '/api/events',
                                        params={'collection': 'Pudgy Penguins'})
        
        if self.assert_success(status, data, "Events data retrieved"):
            event_data = data.get('data', {})
            total = event_data.get('total_events', 0)
            breakdown = event_data.get('event_breakdown', {})
            print(f"  Total events: {total}")
            for event_type, stats in breakdown.items():
                percentage = stats.get('percentage', 0)
                print(f"    • {event_type}: {percentage}%")
            self.results.append({
                'test': 'Get Events',
                'status': 'PASS',
                'total_events': total
            })
        else:
            self.results.append({
                'test': 'Get Events',
                'status': 'FAIL',
                'details': data
            })
    
    def test_error_missing_key(self):
        """Test 9: Error handling - missing API key"""
        self.print_test("Error Handling - Missing API Key")
        status, data = self.make_request('GET', '/api/collections', auth=False)
        
        if status == 401 or status == 403:
            self.print_success("Proper auth error returned")
            self.results.append({
                'test': 'Error - Missing Key',
                'status': 'PASS'
            })
        elif 'detail' in data and 'unauthorized' in str(data).lower():
            self.print_success("Proper auth error returned")
            self.results.append({
                'test': 'Error - Missing Key',
                'status': 'PASS'
            })
        else:
            self.print_error(f"Expected auth error but got {status}")
            self.results.append({
                'test': 'Error - Missing Key',
                'status': 'FAIL',
                'got_status': status
            })
    
    def test_error_invalid_collection(self):
        """Test 10: Error handling - invalid collection"""
        self.print_test("Error Handling - Invalid Collection")
        status, data = self.make_request('GET', '/api/sales',
                                        params={'collection': 'InvalidCollection'})
        
        if status == 404:
            self.print_success("Proper 404 error returned")
            self.results.append({
                'test': 'Error - Invalid Collection',
                'status': 'PASS'
            })
        else:
            self.print_error(f"Expected 404 error but got {status}")
            self.results.append({
                'test': 'Error - Invalid Collection',
                'status': 'FAIL',
                'got_status': status
            })
    
    def run_all_tests(self):
        """Run complete test suite"""
        self.print_header("🧪 NFT Market Analytics API - Python Test Suite")
        
        print("Configuration:")
        print(f"  API URL: {self.api_url}")
        print(f"  API Key: {self.api_key[:20]}...")
        print(f"  Verbose: {self.verbose}\n")
        
        # Run tests
        self.test_health_check()
        self.test_collections()
        self.test_sales_all()
        self.test_sales_by_collection('BAYC')
        self.test_pagination()
        self.test_volume()
        self.test_trends()
        self.test_events()
        self.test_error_missing_key()
        self.test_error_invalid_collection()
        
        # Print summary
        self.print_header("📊 Test Summary")
        
        total = self.tests_passed + self.tests_failed
        print(f"Total Tests: {Colors.BLUE}{total}{Colors.END}")
        print(f"Passed: {Colors.GREEN}{self.tests_passed}{Colors.END}")
        print(f"Failed: {Colors.RED}{self.tests_failed}{Colors.END}")
        
        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}🎉 All tests passed!{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.RED}⚠️  Some tests failed{Colors.END}")
            return 1
    
    def export_results_json(self) -> str:
        """Export test results as JSON"""
        return json.dumps({
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': self.tests_passed + self.tests_failed,
                'passed': self.tests_passed,
                'failed': self.tests_failed
            },
            'results': self.results
        }, indent=2)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='NFT Market Analytics API - Test Suite'
    )
    parser.add_argument('--api-url', default='http://localhost:8000',
                       help='API base URL (default: http://localhost:8000)')
    parser.add_argument('--api-key', default='sk_test_key_12345',
                       help='API key for authentication')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Print verbose output')
    
    args = parser.parse_args()
    
    tester = NFTAPITester(
        api_url=args.api_url,
        api_key=args.api_key,
        verbose=args.verbose
    )
    
    exit_code = tester.run_all_tests()
    
    if args.json:
        print("\n" + tester.export_results_json())
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
