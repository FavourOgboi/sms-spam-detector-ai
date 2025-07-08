"""
Quick test to see what's happening
"""
import requests
import json

def test_backend():
    try:
        print("Testing backend connection...")
        
        # Test health endpoint
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.text}")
        
        # Test login
        login_data = {
            "usernameOrEmail": "demo",
            "password": "demo123"
        }
        
        response = requests.post('http://localhost:5000/api/auth/login', 
                               json=login_data, 
                               timeout=5)
        print(f"\nLogin status: {response.status_code}")
        print(f"Login response: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - is it running on port 5000?")
    except requests.exceptions.Timeout:
        print("❌ Backend request timed out")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_backend()
