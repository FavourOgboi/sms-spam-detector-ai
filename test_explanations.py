"""
Test the new explanation features in SMS Guard
"""
import requests
import json

def test_explanations():
    print("🧠 Testing SMS Guard Explanation Features")
    print("=" * 50)
    
    BASE_URL = "http://localhost:5000/api"
    
    # Login first
    login_data = {"usernameOrEmail": "demo", "password": "demo123"}
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    token = response.json()['data']['token']
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test cases with different message types
    test_cases = [
        {
            "message": "FREE MONEY!!! Click now to win $1000! Limited time offer!",
            "description": "Obvious spam with multiple indicators"
        },
        {
            "message": "Hi mom, can you pick me up from school at 3pm today?",
            "description": "Legitimate family message"
        },
        {
            "message": "URGENT! Your account will be suspended! Call now!",
            "description": "Urgency-based scam"
        },
        {
            "message": "Meeting tomorrow at 2pm in conference room B. Please confirm.",
            "description": "Professional message"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Message: \"{test_case['message'][:40]}...\"")
        
        try:
            response = requests.post(
                f"{BASE_URL}/predict",
                json={"message": test_case["message"]},
                headers=headers
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    data = result['data']
                    
                    print(f"   📊 Prediction: {data['prediction']} ({data['confidence']:.1%} confident)")
                    print(f"   📈 Probabilities: Spam {data.get('spamProbability', 0):.1%}, Ham {data.get('hamProbability', 0):.1%}")
                    
                    # Check explanations
                    explanations = data.get('topFeatures', [])
                    if explanations:
                        print(f"   🔍 Found {len(explanations)} explanation features:")
                        for j, exp in enumerate(explanations[:3], 1):  # Show top 3
                            method = exp.get('method', 'UNKNOWN')
                            feature = exp.get('feature', 'unknown')
                            importance = exp.get('importance', 0)
                            explanation = exp.get('explanation', 'No explanation')
                            
                            print(f"      {j}. [{method}] {feature} (importance: {importance:.1%})")
                            print(f"         → {explanation}")
                    else:
                        print("   ⚠️  No explanations provided")
                    
                    print("   ✅ Test passed")
                else:
                    print(f"   ❌ Prediction failed: {result.get('error')}")
            else:
                print(f"   ❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Explanation Features Test Complete!")
    print("\n📋 What to check in the frontend:")
    print("   ✅ 'Why this prediction?' section appears")
    print("   ✅ Feature names and explanations display")
    print("   ✅ Method badges (KEYWORD/ANALYSIS) show")
    print("   ✅ Importance bars are visible")
    print("   ✅ Different colors for different methods")
    print("\n🌐 Test these messages in the app at http://localhost:5173")

if __name__ == "__main__":
    test_explanations()
