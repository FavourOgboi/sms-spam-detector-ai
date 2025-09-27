#!/usr/bin/env python3
"""
Test LIME fix
"""

import sys
import os
sys.path.append('backend')

def test_lime():
    """Test LIME explanation"""
    try:
        from ml_model.spam_detector import spam_detector
        
        message = "Your account is expiring. Verify your information to continue service"
        print(f"Testing LIME with: {message}")
        
        result = spam_detector.explain_prediction(message, 5)
        
        if result['success']:
            print("✅ LIME explanation successful!")
            exp = result['explanation']
            print(f"Method: {exp['method']}")
            print(f"Features found: {len(exp['features'])}")
            for feature in exp['features'][:3]:
                print(f"  - '{feature['feature']}' → {feature['direction']} ({feature['importance']:.4f})")
        else:
            print(f"❌ LIME failed: {result.get('error', 'Unknown error')}")
        
        return result['success']
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_lime()
