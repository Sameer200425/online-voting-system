#!/usr/bin/env python3
"""
Test script to verify Heroku deployment
"""
import requests
import sys

def test_deployment():
    """Test if the Heroku app is accessible"""
    
    # Your Heroku app URL
    app_url = "https://sameer-voting-system-2025.herokuapp.com"
    
    print("🧪 Testing Heroku Deployment...")
    print(f"📍 App URL: {app_url}")
    print("-" * 50)
    
    try:
        # Test main page
        print("1. Testing main page...")
        response = requests.get(app_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Main page is accessible!")
            print(f"   Status Code: {response.status_code}")
        else:
            print(f"❌ Main page error - Status Code: {response.status_code}")
            
        # Test admin page
        print("\n2. Testing admin page...")
        admin_url = f"{app_url}/admin/"
        admin_response = requests.get(admin_url, timeout=10)
        
        if admin_response.status_code == 200:
            print("✅ Admin page is accessible!")
            print(f"   Admin URL: {admin_url}")
        else:
            print(f"❌ Admin page error - Status Code: {admin_response.status_code}")
            
        # Test elections page
        print("\n3. Testing elections page...")
        elections_url = f"{app_url}/elections/"
        elections_response = requests.get(elections_url, timeout=10)
        
        if elections_response.status_code == 200:
            print("✅ Elections page is accessible!")
            print(f"   Elections URL: {elections_url}")
        else:
            print(f"❌ Elections page error - Status Code: {elections_response.status_code}")
            
        print("\n" + "="*50)
        print("🎉 DEPLOYMENT TEST RESULTS:")
        print(f"📱 Main App: {app_url}")
        print(f"⚙️  Admin Panel: {admin_url}")
        print(f"🗳️  Elections: {elections_url}")
        print("="*50)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("💡 Make sure your Heroku app is deployed and running")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_deployment()
    sys.exit(0 if success else 1)
