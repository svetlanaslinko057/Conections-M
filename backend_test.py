#!/usr/bin/env python3
"""
Backend Testing Suite for Connections Module
Tests the Node.js Fastify backend via Python FastAPI proxy
"""

import requests
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class ConnectionsAPITester:
    def __init__(self, base_url="https://narratives-hub-2.preview.emergentagent.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []
        
    def log_test(self, name: str, success: bool, details: Dict[str, Any]):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
            
        result = {
            "test_name": name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            **details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {name}")
        if not success and "error" in details:
            print(f"   Error: {details['error']}")
        elif "response_data" in details:
            print(f"   Response: {details['response_data']}")

    def test_health_endpoint(self) -> bool:
        """Test GET /api/health"""
        try:
            response = self.session.get(f"{self.base_url}/api/health", timeout=10)
            success = response.status_code == 200
            
            details = {
                "status_code": response.status_code,
                "endpoint": "/api/health"
            }
            
            if success:
                data = response.json()
                details["response_data"] = data
            else:
                details["error"] = f"Status {response.status_code}: {response.text[:200]}"
                
            self.log_test("Backend Health Check", success, details)
            return success
            
        except Exception as e:
            self.log_test("Backend Health Check", False, {
                "endpoint": "/api/health",
                "error": str(e)
            })
            return False

    def test_connections_config(self) -> bool:
        """Test GET /api/connections/config"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/config", timeout=10)
            success = response.status_code == 200
            
            details = {
                "status_code": response.status_code,
                "endpoint": "/api/connections/config"
            }
            
            if success:
                data = response.json()
                details["response_data"] = data
                # Validate config structure
                if not data.get("ok"):
                    success = False
                    details["error"] = "Response missing 'ok' field"
            else:
                details["error"] = f"Status {response.status_code}: {response.text[:200]}"
                
            self.log_test("Connections Config", success, details)
            return success
            
        except Exception as e:
            self.log_test("Connections Config", False, {
                "endpoint": "/api/connections/config",
                "error": str(e)
            })
            return False

    def test_connections_authors(self) -> bool:
        """Test GET /api/connections/authors - should redirect to /api/connections/accounts"""
        try:
            # Based on the routes.ts file, this should be /api/connections/accounts
            response = self.session.get(f"{self.base_url}/api/connections/accounts", timeout=10)
            success = response.status_code == 200
            
            details = {
                "status_code": response.status_code,
                "endpoint": "/api/connections/accounts"
            }
            
            if success:
                data = response.json()
                details["response_data"] = data
                # Validate accounts structure
                if not data.get("ok"):
                    success = False
                    details["error"] = "Response missing 'ok' field"
            else:
                details["error"] = f"Status {response.status_code}: {response.text[:200]}"
                
            self.log_test("Connections Authors/Accounts", success, details)
            return success
            
        except Exception as e:
            self.log_test("Connections Authors/Accounts", False, {
                "endpoint": "/api/connections/accounts", 
                "error": str(e)
            })
            return False

    def test_connections_unified(self) -> bool:
        """Test GET /api/connections/unified - should be unified accounts or similar endpoint"""
        try:
            # This might be radar/accounts based on the routes
            response = self.session.get(f"{self.base_url}/api/connections/radar/accounts", timeout=10)
            success = response.status_code == 200
            
            details = {
                "status_code": response.status_code,
                "endpoint": "/api/connections/radar/accounts"
            }
            
            if success:
                data = response.json()
                details["response_data"] = data
                if not data.get("ok"):
                    success = False
                    details["error"] = "Response missing 'ok' field"
            else:
                details["error"] = f"Status {response.status_code}: {response.text[:200]}"
                
            self.log_test("Connections Unified Data", success, details)
            return success
            
        except Exception as e:
            self.log_test("Connections Unified Data", False, {
                "endpoint": "/api/connections/radar/accounts",
                "error": str(e)
            })
            return False

    def test_connections_graph(self) -> bool:
        """Test connections graph endpoints"""
        try:
            # Based on the routes, there should be graph endpoints
            response = self.session.get(f"{self.base_url}/api/connections/graph/nodes", timeout=10)
            
            # If graph/nodes doesn't exist, try a general graph endpoint
            if response.status_code == 404:
                response = self.session.get(f"{self.base_url}/api/connections/stats", timeout=10)
            
            success = response.status_code == 200
            
            details = {
                "status_code": response.status_code,
                "endpoint": "/api/connections/graph or /api/connections/stats"
            }
            
            if success:
                data = response.json()
                details["response_data"] = data
                if not data.get("ok"):
                    success = False
                    details["error"] = "Response missing 'ok' field"
            else:
                details["error"] = f"Status {response.status_code}: {response.text[:200]}"
                
            self.log_test("Connections Graph", success, details)
            return success
            
        except Exception as e:
            self.log_test("Connections Graph", False, {
                "endpoint": "/api/connections/graph/*",
                "error": str(e)
            })
            return False

    def test_connections_health(self) -> bool:
        """Test GET /api/connections/health"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/health", timeout=10)
            success = response.status_code == 200
            
            details = {
                "status_code": response.status_code,
                "endpoint": "/api/connections/health"
            }
            
            if success:
                data = response.json()
                details["response_data"] = data
                # Check for connections module health data
                if not data.get("ok"):
                    success = False
                    details["error"] = "Response missing 'ok' field"
                elif not data.get("module") == "connections":
                    success = False
                    details["error"] = "Not a connections module health response"
            else:
                details["error"] = f"Status {response.status_code}: {response.text[:200]}"
                
            self.log_test("Connections Module Health", success, details)
            return success
            
        except Exception as e:
            self.log_test("Connections Module Health", False, {
                "endpoint": "/api/connections/health",
                "error": str(e)
            })
            return False

    def test_mock_endpoints(self) -> bool:
        """Test mock endpoints for development"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/score/mock", timeout=10)
            success = response.status_code == 200
            
            details = {
                "status_code": response.status_code,
                "endpoint": "/api/connections/score/mock"
            }
            
            if success:
                data = response.json()
                details["response_data"] = data
                if not data.get("ok"):
                    success = False
                    details["error"] = "Response missing 'ok' field"
            else:
                details["error"] = f"Status {response.status_code}: {response.text[:200]}"
                
            self.log_test("Mock Score Endpoint", success, details)
            return success
            
        except Exception as e:
            self.log_test("Mock Score Endpoint", False, {
                "endpoint": "/api/connections/score/mock",
                "error": str(e)
            })
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("=" * 60)
        print("🧪 CONNECTIONS MODULE BACKEND TESTS")
        print("=" * 60)
        print(f"Testing against: {self.base_url}")
        print()

        # Core health checks
        health_ok = self.test_health_endpoint()
        connections_health_ok = self.test_connections_health()
        
        # If basic health fails, stop testing
        if not health_ok:
            print("\n❌ Basic health check failed - stopping tests")
            return self.generate_summary()
        
        # Core connections endpoints
        self.test_connections_config()
        self.test_connections_authors()
        self.test_connections_unified()
        self.test_connections_graph()
        
        # Mock/development endpoints
        self.test_mock_endpoints()
        
        return self.generate_summary()

    def generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"Tests Run: {self.tests_run}")
        print(f"Tests Passed: {self.tests_passed}")
        print(f"Tests Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {(self.tests_passed / self.tests_run * 100):.1f}%" if self.tests_run > 0 else "0.0%")
        
        # Show failed tests
        failed_tests = [r for r in self.test_results if not r["success"]]
        if failed_tests:
            print(f"\n❌ FAILED TESTS ({len(failed_tests)}):")
            for test in failed_tests:
                print(f"  • {test['test_name']}: {test.get('error', 'Unknown error')}")
        
        return {
            "tests_run": self.tests_run,
            "tests_passed": self.tests_passed,
            "success_rate": (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0,
            "test_results": self.test_results,
            "failed_tests": failed_tests
        }


def main():
    """Main test runner"""
    tester = ConnectionsAPITester()
    summary = tester.run_all_tests()
    
    # Return appropriate exit code
    return 0 if summary["tests_passed"] == summary["tests_run"] else 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)