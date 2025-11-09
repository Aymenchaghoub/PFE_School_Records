#!/usr/bin/env python3
"""
Deployment Validation Script
Tests live deployment endpoints to ensure everything is working
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, List, Tuple

# Configuration
BACKEND_URL = "https://school-records-backend.onrender.com"  # Update with your Render URL
FRONTEND_URL = "https://your-site.netlify.app"  # Update with your Netlify URL

# Test results storage
test_results = []

def print_header(text: str):
    """Print formatted section header"""
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50)

def test_endpoint(name: str, url: str, expected_status: int = 200, method: str = "GET", 
                  headers: Dict = None, data: Dict = None) -> Tuple[bool, str]:
    """Test a single endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        else:
            return False, f"Unsupported method: {method}"
        
        if response.status_code == expected_status:
            return True, f"✅ {name}: OK (Status: {response.status_code})"
        else:
            return False, f"❌ {name}: Failed (Expected: {expected_status}, Got: {response.status_code})"
    except requests.exceptions.ConnectionError:
        return False, f"❌ {name}: Connection failed (Service may be down)"
    except requests.exceptions.Timeout:
        return False, f"❌ {name}: Timeout (Service may be starting up)"
    except Exception as e:
        return False, f"❌ {name}: Error - {str(e)}"

def test_backend():
    """Test backend API endpoints"""
    print_header("Testing Backend API")
    
    tests = [
        ("Health Check", f"{BACKEND_URL}/health"),
        ("API Documentation", f"{BACKEND_URL}/docs", 200),
        ("OpenAPI Schema", f"{BACKEND_URL}/openapi.json"),
    ]
    
    for test in tests:
        if len(test) == 2:
            name, url = test
            expected_status = 200
        else:
            name, url, expected_status = test
            
        success, message = test_endpoint(name, url, expected_status)
        print(message)
        test_results.append((name, success))
    
    # Test authentication endpoint (expected to fail without credentials)
    success, message = test_endpoint(
        "Auth Endpoint (No Credentials)", 
        f"{BACKEND_URL}/api/auth/login",
        expected_status=422,  # Expecting validation error
        method="POST",
        data={}
    )
    print(message)
    test_results.append(("Auth Endpoint", success))

def test_frontend():
    """Test frontend deployment"""
    print_header("Testing Frontend")
    
    success, message = test_endpoint("Frontend Homepage", FRONTEND_URL)
    print(message)
    test_results.append(("Frontend", success))
    
    # Check if frontend can load static assets
    success, message = test_endpoint(
        "Frontend Assets", 
        f"{FRONTEND_URL}/index.html"
    )
    print(message)
    test_results.append(("Frontend Assets", success))

def test_integration():
    """Test backend-frontend integration"""
    print_header("Testing Integration")
    
    # This would require actual test credentials
    print("⚠️  Integration tests require valid credentials")
    print("   Please test manually by:")
    print("   1. Opening the frontend URL")
    print("   2. Attempting to log in")
    print("   3. Verifying API calls succeed")

def generate_report():
    """Generate final deployment report"""
    print_header("Deployment Validation Report")
    
    total_tests = len(test_results)
    passed_tests = sum(1 for _, success in test_results if success)
    success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
    
    print(f"\nTest Results:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {total_tests - passed_tests}")
    print(f"  Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("\n✅ All tests passed! Deployment successful.")
    elif success_rate >= 75:
        print("\n⚠️  Most tests passed. Check failed endpoints.")
    else:
        print("\n❌ Deployment validation failed. Please check logs.")
    
    # Save report to file
    report_file = f"deployment_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(f"Deployment Validation Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"="*50 + "\n\n")
        
        for name, success in test_results:
            status = "✅ PASS" if success else "❌ FAIL"
            f.write(f"{status}: {name}\n")
        
        f.write(f"\n{'-'*50}\n")
        f.write(f"Success Rate: {success_rate:.1f}%\n")
    
    print(f"\n📄 Report saved to: {report_file}")

def main():
    """Main validation flow"""
    print("\n🚀 School Records Deployment Validator")
    print("="*50)
    
    # Update URLs if provided as arguments
    global BACKEND_URL, FRONTEND_URL
    if len(sys.argv) > 1:
        BACKEND_URL = sys.argv[1]
    if len(sys.argv) > 2:
        FRONTEND_URL = sys.argv[2]
    
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Frontend URL: {FRONTEND_URL}")
    
    # Run tests
    test_backend()
    test_frontend()
    test_integration()
    
    # Generate report
    generate_report()

if __name__ == "__main__":
    main()
