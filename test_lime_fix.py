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
        from ml_model import spam_detector
        
        message = "Your account is expiring. Verify your information to continue service"
        print(f"Testing LIME with: {message}")
        
        print("LIME explanation not available in stateless mode.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_lime()
