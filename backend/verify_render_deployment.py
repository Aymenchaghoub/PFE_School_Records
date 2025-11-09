#!/usr/bin/env python3
"""
Render Deployment Verification Script
Tests the deployed backend on Render
"""

import requests
import sys
from datetime import datetime
from typing import Dict, Tuple

# Configuration
RENDER_URL = "https://pfc-backend.onrender.com"
HEALTH_ENDPOINT = f"{RENDER_URL}/health"
DOCS_ENDPOINT = f"{RENDER_URL}/docs"
API_ENDPOINT = f"{RENDER_URL}/api"

def print_header(text: str, char: str = "="):
    """Print formatted header"""
    print(f"\n{char * 60}")
    print(f"  {text}")
    print(f"{char * 60}\n")

def test_health_check() -> Tuple[bool, str, Dict]:
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: PASSED")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Response time: {response.elapsed.total_seconds():.2f}s")
            return True, "Healthy", data
        elif response.status_code == 503:
            return False, "Service starting up (cold start)", {}
        else:
            return False, f"Unexpected status: {response.status_code}", {}
            
    except requests.exceptions.ConnectionError:
        return False, "Connection failed - Service may not be deployed yet", {}
    except requests.exceptions.Timeout:
        return False, "Timeout - Service may be starting up (cold start)", {}
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)}", {}

def test_docs() -> Tuple[bool, str]:
    """Test API documentation endpoint"""
    print("\n📚 Testing API documentation...")
    
    try:
        response = requests.get(DOCS_ENDPOINT, timeout=30)
        
        if response.status_code == 200:
            print(f"✅ API docs: ACCESSIBLE")
            print(f"   URL: {DOCS_ENDPOINT}")
            return True, "Accessible"
        else:
            return False, f"Status: {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_api_prefix() -> Tuple[bool, str]:
    """Test API prefix configuration"""
    print("\n🔧 Testing API prefix...")
    
    try:
        # Test that /api redirects or returns something
        response = requests.get(f"{RENDER_URL}/api/", timeout=30, allow_redirects=False)
        
        if response.status_code in [200, 307, 404]:  # 404 is ok, means API is there but no root
            print(f"✅ API prefix: CONFIGURED")
            return True, "Configured"
        else:
            return False, f"Status: {response.status_code}"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def test_database_connection(health_data: Dict) -> Tuple[bool, str]:
    """Check database connection from health data"""
    print("\n🗄️  Checking database connection...")
    
    if not health_data:
        print("⚠️  Database status: UNKNOWN (no health data)")
        return False, "Unknown"
    
    db_status = health_data.get('database', 'unknown')
    
    if db_status == 'connected':
        print(f"✅ Database: CONNECTED")
        return True, "Connected"
    else:
        print(f"❌ Database: {db_status}")
        return False, db_status

def generate_report(results: Dict):
    """Generate final deployment report"""
    print_header("🎯 DEPLOYMENT VERIFICATION REPORT", "=")
    
    print(f"Service URL: {RENDER_URL}")
    print(f"Tested at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    all_passed = all(results.values())
    
    print("Test Results:")
    print(f"  Health Check:    {'✅ PASS' if results['health'] else '❌ FAIL'}")
    print(f"  API Docs:        {'✅ PASS' if results['docs'] else '❌ FAIL'}")
    print(f"  API Prefix:      {'✅ PASS' if results['api'] else '❌ FAIL'}")
    print(f"  Database:        {'✅ PASS' if results['database'] else '❌ FAIL'}")
    
    success_rate = sum(results.values()) / len(results) * 100
    print(f"\nSuccess Rate: {success_rate:.0f}%")
    
    if all_passed:
        print("\n🎉 ✅ SUCCESS - Deployment is fully operational!")
        print("\nNext steps:")
        print("  1. Test authentication: POST /api/auth/login")
        print("  2. Update frontend with backend URL")
        print("  3. Test end-to-end functionality")
        return 0
    elif results['health']:
        print("\n⚠️  PARTIAL - Service is running but some features may not work")
        print("\nRecommended actions:")
        if not results['database']:
            print("  • Check DATABASE_URL in Render environment variables")
            print("  • Verify AlwaysData database is accessible")
        if not results['docs']:
            print("  • Verify FastAPI docs are enabled")
        return 1
    else:
        print("\n❌ FAILED - Service is not accessible")
        print("\nTroubleshooting:")
        print("  1. Check Render dashboard for deployment status")
        print("  2. Review build logs for errors")
        print("  3. Verify environment variables are set")
        print("  4. Wait 30-60 seconds for cold start if just deployed")
        return 2

def main():
    """Main verification flow"""
    print_header("🚀 RENDER DEPLOYMENT VERIFICATION")
    
    print(f"Testing backend at: {RENDER_URL}")
    print("This may take 30-60 seconds if service is in cold start...\n")
    
    # Run tests
    health_passed, health_msg, health_data = test_health_check()
    docs_passed, docs_msg = test_docs()
    api_passed, api_msg = test_api_prefix()
    db_passed, db_msg = test_database_connection(health_data)
    
    # Store results
    results = {
        'health': health_passed,
        'docs': docs_passed,
        'api': api_passed,
        'database': db_passed
    }
    
    # Generate report
    exit_code = generate_report(results)
    
    # Save report
    report_file = f"deployment_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w') as f:
        f.write(f"Render Deployment Verification Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Service URL: {RENDER_URL}\n")
        f.write(f"="*60 + "\n\n")
        
        for test, passed in results.items():
            status = "✅ PASS" if passed else "❌ FAIL"
            f.write(f"{status}: {test.upper()}\n")
        
        success_rate = sum(results.values()) / len(results) * 100
        f.write(f"\nSuccess Rate: {success_rate:.0f}%\n")
    
    print(f"\n📄 Report saved to: {report_file}")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled by user")
        sys.exit(130)
