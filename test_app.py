#!/usr/bin/env python3
"""
Simple test script to verify the wildlife crime dashboard application works correctly.
"""

import requests
import json
import time
import sys

def test_api_endpoints():
    """Test the main API endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Wildlife Crime Dashboard API...")
    print("=" * 50)
    
    # Test main page
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Main page (/) - OK")
        else:
            print(f"❌ Main page (/) - Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Main page (/) - Error: {e}")
        return False
    
    # Test API data endpoint
    try:
        response = requests.get(f"{base_url}/api/data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print("✅ API data endpoint (/api/data) - OK")
            print(f"   - Alerts: {len(data.get('alerts', []))}")
            print(f"   - Locations: {len(data.get('locations', []))}")
            print(f"   - Trends: {len(data.get('trends', []))}")
        else:
            print(f"❌ API data endpoint (/api/data) - Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ API data endpoint (/api/data) - Error: {e}")
        return False
    
    # Test incidents endpoint
    try:
        response = requests.get(f"{base_url}/api/incidents", timeout=10)
        if response.status_code == 200:
            incidents = response.json()
            print(f"✅ Incidents endpoint (/api/incidents) - OK ({len(incidents)} incidents)")
        else:
            print(f"❌ Incidents endpoint (/api/incidents) - Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Incidents endpoint (/api/incidents) - Error: {e}")
        return False
    
    # Test alerts endpoint
    try:
        response = requests.get(f"{base_url}/api/alerts", timeout=10)
        if response.status_code == 200:
            alerts = response.json()
            print(f"✅ Alerts endpoint (/api/alerts) - OK ({len(alerts)} alerts)")
        else:
            print(f"❌ Alerts endpoint (/api/alerts) - Status: {response.status_code}")
    except requests.RequestException as e:
        print(f"❌ Alerts endpoint (/api/alerts) - Error: {e}")
        return False
    
    print("=" * 50)
    print("🎉 All tests passed! The application is working correctly.")
    return True

def main():
    """Main test function"""
    print("🚀 Starting Wildlife Crime Dashboard Test Suite")
    print("Make sure the Flask application is running on http://localhost:5000")
    print()
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    success = test_api_endpoints()
    
    if success:
        print("\n✅ Application is ready to use!")
        print("🌐 Open your browser and go to: http://localhost:5000")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please check the application.")
        sys.exit(1)

if __name__ == "__main__":
    main()
