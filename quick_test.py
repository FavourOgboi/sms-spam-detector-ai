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

        if response.status_code == 200:
            login_result = response.json()
            token = login_result['data']['token']
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Login successful")

            # Test stats endpoint
            stats_response = requests.get('http://localhost:5000/api/user/stats',
                                        headers=headers, timeout=5)
            print(f"\nStats status: {stats_response.status_code}")
            if stats_response.status_code == 200:
                stats_data = stats_response.json()['data']
                print(f"✅ Stats working - Total messages: {stats_data.get('totalMessages', 0)}")
                print(f"   Has accuracy data: {'accuracyData' in stats_data}")
            else:
                print(f"❌ Stats error: {stats_response.text[:100]}")

            # Test profile update
            profile_response = requests.put('http://localhost:5000/api/user/profile',
                                          json={"username": "demo", "email": "demo@example.com", "bio": "test"},
                                          headers=headers, timeout=5)
            print(f"\nProfile update status: {profile_response.status_code}")
            if profile_response.status_code == 200:
                print("✅ Profile update working")
            else:
                print(f"❌ Profile error: {profile_response.text[:100]}")
        else:
            print(f"❌ Login failed: {response.text}")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend - is it running on port 5000?")
    except requests.exceptions.Timeout:
        print("❌ Backend request timed out")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_backend()
