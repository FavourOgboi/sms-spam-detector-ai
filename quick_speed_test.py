#!/usr/bin/env python3
"""
Quick speed test
"""

import sys
import os
import time
sys.path.append('backend')

def main():
    try:
        from ml_model.spam_detector import spam_detector
        
        message = "Your account is expiring. Verify your information to continue service"
        
        print("🚀 Speed Test Results:")
        
        # Test prediction speed
        start = time.time()
        result = spam_detector.predict(message)
        end = time.time()
        
        prediction_time = (end - start) * 1000
        print(f"   Prediction: {prediction_time:.1f}ms - {result['prediction'].upper()}")
        
        # Test explanation speed
        start = time.time()
        explanation = spam_detector.explain_prediction(message, 5)
        end = time.time()
        
        explanation_time = (end - start) * 1000
        print(f"   Explanation: {explanation_time:.0f}ms - {'SUCCESS' if explanation['success'] else 'FAILED'}")
        
        # Test cache (second prediction)
        start = time.time()
        result2 = spam_detector.predict(message)
        end = time.time()
        
        cached_time = (end - start) * 1000
        print(f"   Cached: {cached_time:.1f}ms - {result2['prediction'].upper()}")
        
        speed_improvement = ((prediction_time - cached_time) / prediction_time) * 100
        print(f"   Cache improvement: {speed_improvement:.1f}%")
        
        print(f"\n✅ Performance Summary:")
        print(f"   📈 Prediction: {prediction_time:.1f}ms")
        print(f"   📈 Explanation: {explanation_time/1000:.1f}s")
        print(f"   📈 Cache boost: {speed_improvement:.1f}%")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
