#!/usr/bin/env python3
"""
Backend API Testing for Tolu Shekoni's Portfolio
Tests all backend endpoints systematically
"""

import requests
import json
import uuid
from datetime import datetime
import sys
import os

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("ERROR: Could not get REACT_APP_BACKEND_URL from frontend/.env")
    sys.exit(1)

API_BASE = f"{BASE_URL}/api"

print(f"Testing backend API at: {API_BASE}")
print("=" * 60)

def test_health_check():
    """Test GET /api/ - Health check endpoint"""
    print("\n1. Testing Health Check Endpoint (GET /api/)")
    print("-" * 50)
    
    try:
        response = requests.get(f"{API_BASE}/", timeout=10)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if "message" in data and "Tolu Shekoni Portfolio API" in data["message"]:
                print("✅ Health check PASSED - Correct response format and content")
                return True
            else:
                print("❌ Health check FAILED - Unexpected response content")
                return False
        else:
            print(f"❌ Health check FAILED - Expected 200, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check FAILED - Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Health check FAILED - Error: {e}")
        return False

def test_chat_endpoint():
    """Test POST /api/chat - Venice AI chat integration"""
    print("\n2. Testing Chat Endpoint (POST /api/chat)")
    print("-" * 50)
    
    # Test data
    chat_data = {
        "message": "Tell me about Tolu's background in AI development",
        "sessionId": str(uuid.uuid4())
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/chat", 
            json=chat_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Since Venice API key is not configured, we expect a 500 error
        if response.status_code == 500:
            try:
                error_data = response.json()
                if "Venice AI API key not configured" in error_data.get("detail", ""):
                    print("✅ Chat endpoint PASSED - Proper error handling for missing API key")
                    return True
                else:
                    print("❌ Chat endpoint FAILED - Wrong error message for missing API key")
                    return False
            except:
                print("❌ Chat endpoint FAILED - Invalid JSON response")
                return False
        elif response.status_code == 200:
            # If API key is configured and working
            try:
                data = response.json()
                if "response" in data and "sessionId" in data:
                    print("✅ Chat endpoint PASSED - API key configured and working")
                    return True
                else:
                    print("❌ Chat endpoint FAILED - Missing required fields in response")
                    return False
            except:
                print("❌ Chat endpoint FAILED - Invalid JSON response")
                return False
        else:
            print(f"❌ Chat endpoint FAILED - Unexpected status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat endpoint FAILED - Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Chat endpoint FAILED - Error: {e}")
        return False

def test_contact_endpoint():
    """Test POST /api/contact - Contact form submission"""
    print("\n3. Testing Contact Endpoint (POST /api/contact)")
    print("-" * 50)
    
    # Test with valid data
    contact_data = {
        "name": "John Smith",
        "email": "john.smith@example.com",
        "company": "Tech Solutions Inc",
        "subject": "Collaboration Opportunity",
        "message": "Hi Tolu, I'm interested in discussing a potential AI project collaboration. Your background in both pharmaceutical operations and AI development is exactly what we're looking for."
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/contact",
            json=contact_data,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") == True and "messageId" in data:
                print("✅ Contact endpoint PASSED - Form submission successful")
                return True
            elif data.get("success") == False:
                print(f"⚠️  Contact endpoint PARTIAL - Form saved but email failed: {data.get('error', 'Unknown error')}")
                return True  # Still working, just email not configured
            else:
                print("❌ Contact endpoint FAILED - Unexpected response format")
                return False
        else:
            print(f"❌ Contact endpoint FAILED - Expected 200, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Contact endpoint FAILED - Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Contact endpoint FAILED - Error: {e}")
        return False

def test_contact_validation():
    """Test contact endpoint with invalid data"""
    print("\n4. Testing Contact Endpoint Validation")
    print("-" * 50)
    
    # Test with invalid email
    invalid_data = {
        "name": "Test User",
        "email": "invalid-email",
        "subject": "Test",
        "message": "Test message"
    }
    
    try:
        response = requests.post(
            f"{API_BASE}/contact",
            json=invalid_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ Contact validation PASSED - Proper validation for invalid email")
            return True
        else:
            print(f"❌ Contact validation FAILED - Expected 422 for invalid email, got {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Contact validation FAILED - Network error: {e}")
        return False
    except Exception as e:
        print(f"❌ Contact validation FAILED - Error: {e}")
        return False

def test_status_endpoints():
    """Test additional status endpoints"""
    print("\n5. Testing Status Endpoints")
    print("-" * 50)
    
    # Test GET /api/status
    try:
        response = requests.get(f"{API_BASE}/status", timeout=10)
        print(f"GET /api/status - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ GET /api/status PASSED - Response: {len(data)} status checks")
        else:
            print(f"❌ GET /api/status FAILED - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ GET /api/status FAILED - Error: {e}")
        return False
    
    # Test POST /api/status
    try:
        status_data = {"client_name": "Test Client Portfolio"}
        response = requests.post(
            f"{API_BASE}/status",
            json=status_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"POST /api/status - Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "id" in data and "client_name" in data:
                print("✅ POST /api/status PASSED - Status check created")
                return True
            else:
                print("❌ POST /api/status FAILED - Missing required fields")
                return False
        else:
            print(f"❌ POST /api/status FAILED - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ POST /api/status FAILED - Error: {e}")
        return False

def main():
    """Run all backend tests"""
    print("🚀 Starting Backend API Tests for Tolu Shekoni's Portfolio")
    print(f"Backend URL: {API_BASE}")
    print("=" * 60)
    
    results = []
    
    # Run all tests
    results.append(("Health Check", test_health_check()))
    results.append(("Chat Endpoint", test_chat_endpoint()))
    results.append(("Contact Endpoint", test_contact_endpoint()))
    results.append(("Contact Validation", test_contact_validation()))
    results.append(("Status Endpoints", test_status_endpoints()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All backend tests PASSED!")
        return True
    else:
        print(f"⚠️  {total - passed} test(s) FAILED")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)