#!/usr/bin/env python3
"""
Test Railway deployment
"""
import requests
import time

def test_railway_deployment(app_url):
    """Test if the Railway app is accessible"""
    
    print("🚂 Testing Railway Deployment...")
    print(f"📍 App URL: {app_url}")
    print("-" * 50)
    
    try:
        # Test main page
        print("1. Testing main page...")
        response = requests.get(app_url, timeout=15)
        
        if response.status_code == 200:
            print("✅ Main page is accessible!")
            print(f"   Status Code: {response.status_code}")
        else:
            print(f"❌ Main page error - Status Code: {response.status_code}")
            
        # Test admin page
        print("\n2. Testing admin page...")
        admin_url = f"{app_url}/admin/"
        admin_response = requests.get(admin_url, timeout=15)
        
        if admin_response.status_code == 200:
            print("✅ Admin page is accessible!")
        else:
            print(f"❌ Admin page - Status Code: {admin_response.status_code}")
            
        # Test elections page
        print("\n3. Testing elections page...")
        elections_url = f"{app_url}/elections/"
        elections_response = requests.get(elections_url, timeout=15)
        
        if elections_response.status_code == 200:
            print("✅ Elections page is accessible!")
        else:
            print(f"⚠️ Elections page - Status Code: {elections_response.status_code}")
            
        print("\n" + "="*50)
        print("🎉 RAILWAY DEPLOYMENT RESULTS:")
        print(f"📱 Main App: {app_url}")
        print(f"⚙️  Admin Panel: {admin_url}")
        print(f"🗳️  Elections: {elections_url}")
        print("="*50)
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")
        print("💡 App might still be building - try again in a few minutes")
        return False

if __name__ == "__main__":
    # You'll get this URL from Railway after deployment
    railway_url = input("Enter your Railway app URL (e.g., https://your-app.up.railway.app): ")
    
    if railway_url:
        test_railway_deployment(railway_url)
    else:
        print("⚠️ Please provide the Railway app URL after deployment completes")
