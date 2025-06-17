#!/usr/bin/env python3
"""
🧪 Test Registration System
Quick test to verify registration is working
"""

import requests
import json

def test_registration():
    """Test the registration endpoint"""
    
    # Test data
    test_user = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "test123",
        "experience_level": "complete_beginner",
        "learning_goals": ["web_development", "career_change"]
    }
    
    print("🧪 Testing Registration System...")
    print(f"📝 Test user data: {test_user}")
    
    try:
        # Send registration request
        response = requests.post(
            'http://localhost:5000/register',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(test_user)
        )
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📄 Response content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Registration successful!")
                print(f"🔗 Redirect URL: {result.get('redirect')}")
            else:
                print(f"❌ Registration failed: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the app is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_login():
    """Test the login endpoint"""
    
    login_data = {
        "email": "test@example.com",
        "password": "test123"
    }
    
    print("\n🔑 Testing Login System...")
    print(f"📝 Login data: {login_data}")
    
    try:
        response = requests.post(
            'http://localhost:5000/login',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(login_data)
        )
        
        print(f"📡 Response status: {response.status_code}")
        print(f"📄 Response content: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Login successful!")
                print(f"🔗 Redirect URL: {result.get('redirect')}")
            else:
                print(f"❌ Login failed: {result.get('error')}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Registration Tests...")
    test_registration()
    test_login()
    print("\n✨ Tests completed!")
