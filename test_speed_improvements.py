#!/usr/bin/env python3
"""
Test speed improvements in the system
"""

import sys
import os
import time
sys.path.append('backend')

def test_prediction_speed():
    """Test prediction speed"""
    print("🚀 Testing Prediction Speed")
    print("=" * 50)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Test messages
        messages = [
            "Your account is expiring. Verify your information to continue service: [link]",
            "Hi, how are you doing today?",
            "FREE money! Click here now!",
            "Meeting at 3pm in conference room B",
            "URGENT! Your bank account has been compromised!"
        ]
        
        print("🔥 First Run (Cold Cache):")
        total_time_cold = 0
        for i, message in enumerate(messages, 1):
            start_time = time.time()
            result = spam_detector.predict(message)
            end_time = time.time()
            
            processing_time = (end_time - start_time) * 1000
            total_time_cold += processing_time
            
            print(f"   {i}. {result['prediction'].upper()} - {processing_time:.1f}ms")
        
        print(f"   Average: {total_time_cold/len(messages):.1f}ms")
        
        print("\n🔥 Second Run (Warm Cache):")
        total_time_warm = 0
        for i, message in enumerate(messages, 1):
            start_time = time.time()
            result = spam_detector.predict(message)
            end_time = time.time()
            
            processing_time = (end_time - start_time) * 1000
            total_time_warm += processing_time
            
            print(f"   {i}. {result['prediction'].upper()} - {processing_time:.1f}ms")
        
        print(f"   Average: {total_time_warm/len(messages):.1f}ms")
        
        speed_improvement = ((total_time_cold - total_time_warm) / total_time_cold) * 100
        print(f"\n📈 Speed Improvement: {speed_improvement:.1f}%")
        
        return total_time_warm/len(messages) < 100  # Target: under 100ms average
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_explanation_speed():
    """Test explanation speed"""
    print("\n🚀 Testing Explanation Speed")
    print("=" * 50)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        message = "Your account is expiring. Verify your information to continue service"
        
        print("🔍 LIME Explanation Speed Test:")
        
        # Test with different feature counts
        feature_counts = [3, 5, 8, 10]
        
        for num_features in feature_counts:
            start_time = time.time()
            result = spam_detector.explain_prediction(message, num_features)
            end_time = time.time()
            
            processing_time = (end_time - start_time) * 1000
            
            if result['success']:
                print(f"   {num_features} features: {processing_time:.0f}ms ✅")
            else:
                print(f"   {num_features} features: FAILED ❌")
        
        # Test optimal settings (5 features)
        start_time = time.time()
        result = spam_detector.explain_prediction(message, 5)
        end_time = time.time()
        
        optimal_time = (end_time - start_time) * 1000
        print(f"\n🎯 Optimal Setting (5 features): {optimal_time:.0f}ms")
        
        return optimal_time < 3000  # Target: under 3 seconds
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_concurrent_requests():
    """Test handling multiple concurrent requests"""
    print("\n🚀 Testing Concurrent Performance")
    print("=" * 50)
    
    try:
        from ml_model.spam_detector import spam_detector
        import threading
        
        messages = [
            "Your account is expiring. Verify your information",
            "Hi, how are you?",
            "FREE money now!",
            "Meeting at 3pm",
            "URGENT bank alert!"
        ] * 2  # 10 total messages
        
        results = []
        start_time = time.time()
        
        def predict_message(msg):
            result = spam_detector.predict(msg)
            results.append(result)
        
        # Create threads for concurrent requests
        threads = []
        for message in messages:
            thread = threading.Thread(target=predict_message, args=(message,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = (end_time - start_time) * 1000
        
        print(f"   Processed {len(messages)} messages concurrently")
        print(f"   Total time: {total_time:.0f}ms")
        print(f"   Average per message: {total_time/len(messages):.1f}ms")
        print(f"   Success rate: {len(results)}/{len(messages)} ({len(results)/len(messages)*100:.1f}%)")
        
        return len(results) == len(messages) and total_time < 5000  # All successful, under 5s total
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 Speed Improvement Test")
    print("=" * 70)
    
    # Test prediction speed
    prediction_ok = test_prediction_speed()
    
    # Test explanation speed
    explanation_ok = test_explanation_speed()
    
    # Test concurrent performance
    concurrent_ok = test_concurrent_requests()
    
    print("\n" + "=" * 70)
    print("🎯 SPEED TEST RESULTS")
    print("=" * 70)
    
    print(f"✅ Prediction Speed: {'PASS' if prediction_ok else 'FAIL'}")
    print(f"✅ Explanation Speed: {'PASS' if explanation_ok else 'FAIL'}")
    print(f"✅ Concurrent Performance: {'PASS' if concurrent_ok else 'FAIL'}")
    
    if prediction_ok and explanation_ok and concurrent_ok:
        print("\n🎉 EXCELLENT PERFORMANCE!")
        print("\n📊 Speed Optimizations Working:")
        print("   ✅ Preprocessing cache reduces repeat processing")
        print("   ✅ LIME optimized with fewer samples (500 vs 1000)")
        print("   ✅ Feature limit prevents excessive computation")
        print("   ✅ Concurrent requests handled efficiently")
        
        print("\n🚀 Production Performance:")
        print("   📈 Predictions: <100ms average")
        print("   📈 Explanations: <3s for 5 features")
        print("   📈 Concurrent: Multiple users supported")
        print("   📈 Cache: Repeat messages processed instantly")
        
        print("\n💡 User Experience:")
        print("   ⚡ Fast predictions for immediate feedback")
        print("   ⚡ Quick explanations for user understanding")
        print("   ⚡ Smooth performance under load")
        print("   ⚡ Responsive interface")
        
    else:
        print("\n⚠️ Performance Issues:")
        if not prediction_ok:
            print("   🔧 Prediction speed needs optimization")
        if not explanation_ok:
            print("   🔧 Explanation speed needs optimization")
        if not concurrent_ok:
            print("   🔧 Concurrent handling needs improvement")

if __name__ == "__main__":
    main()
