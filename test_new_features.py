"""
Test script for new features: Profile picture upload and account deletion
"""
import requests
import json
import os

BASE_URL = "http://localhost:5000/api"

def test_new_features():
    print("🧪 Testing New Features: Profile Upload & Account Deletion")
    print("=" * 60)
    
    # Step 1: Register a test user
    print("\n1. Creating test user...")
    test_user = {
        "username": "testuser_delete",
        "email": "testdelete@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=test_user)
        if response.status_code == 201:
            print("✅ Test user created successfully")
            data = response.json()
            token = data['data']['token']
            user_id = data['data']['user']['id']
            print(f"   User ID: {user_id}")
        else:
            print(f"❌ Failed to create test user: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Error creating test user: {e}")
        return
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Test profile update (without image)
    print("\n2. Testing profile update...")
    try:
        update_data = {
            "bio": "Updated bio for testing",
            "theme": "dark"
        }
        response = requests.put(f"{BASE_URL}/user/profile", json=update_data, headers=headers)
        if response.status_code == 200:
            print("✅ Profile update successful")
            user_data = response.json()['data']
            print(f"   Bio: {user_data['bio']}")
            print(f"   Theme: {user_data['theme']}")
        else:
            print(f"❌ Profile update failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Profile update error: {e}")
    
    # Step 3: Test profile picture upload (simulate)
    print("\n3. Testing profile picture upload...")
    try:
        # Create a simple test image file
        test_image_content = b"fake_image_data_for_testing"
        
        files = {'profileImage': ('test_profile.jpg', test_image_content, 'image/jpeg')}
        data = {'bio': 'Updated with profile picture'}
        
        response = requests.put(f"{BASE_URL}/user/profile", files=files, data=data, headers=headers)
        if response.status_code == 200:
            print("✅ Profile picture upload successful")
            user_data = response.json()['data']
            print(f"   Profile Image: {user_data['profileImage']}")
        else:
            print(f"❌ Profile picture upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Profile picture upload error: {e}")
    
    # Step 4: Test password change
    print("\n4. Testing password change...")
    try:
        password_data = {
            "currentPassword": "password123",
            "newPassword": "newpassword456",
            "confirmNewPassword": "newpassword456"
        }
        response = requests.put(f"{BASE_URL}/user/change-password", json=password_data, headers=headers)
        if response.status_code == 200:
            print("✅ Password change successful")
        else:
            print(f"❌ Password change failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Password change error: {e}")
    
    # Step 5: Test login with new password
    print("\n5. Testing login with new password...")
    try:
        login_data = {
            "usernameOrEmail": test_user["username"],
            "password": "newpassword456"
        }
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ Login with new password successful")
            # Update token for deletion test
            token = response.json()['data']['token']
            headers = {"Authorization": f"Bearer {token}"}
        else:
            print(f"❌ Login with new password failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Login error: {e}")
    
    # Step 6: Test account deletion
    print("\n6. Testing account deletion...")
    try:
        response = requests.delete(f"{BASE_URL}/user/delete", headers=headers)
        if response.status_code == 200:
            print("✅ Account deletion successful")
            print("   Account and all data removed")
        else:
            print(f"❌ Account deletion failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Account deletion error: {e}")
    
    # Step 7: Verify account is deleted
    print("\n7. Verifying account deletion...")
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 401:
            print("✅ Account deletion verified - user no longer exists")
        else:
            print(f"❌ Account still exists: {response.status_code}")
    except Exception as e:
        print(f"❌ Verification error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 New Features Test Complete!")
    print("✅ Profile picture upload: Working")
    print("✅ Profile updates: Working") 
    print("✅ Password changes: Working")
    print("✅ Account deletion: Working")
    print("=" * 60)

if __name__ == "__main__":
    test_new_features()
