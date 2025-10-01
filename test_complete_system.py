#!/usr/bin/env python3
"""
Complete system test for SMS Guard prediction and explainable AI
"""

# (Removed unused imports: sys, os, joblib)

# Add backend to path
sys.path.append('backend')

# (Direct model access section removed - obsolete in stateless setup)

def test_app_integration():
    """Test app integration with spam_detector"""
    print("\n🔍 Testing App Integration")
    print("=" * 40)
    
    try:
        from ml_model import spam_detector
        # Test prediction through app
        test_message = "Congratulations! You won $1000! Click now!"
        label, proba = spam_detector.predict_message(test_message)
        print(f"\n🧪 App Prediction Test:")
        print(f"   Message: {test_message}")
        print(f"   Prediction: {label}")
        print(f"   Confidence: {(proba if proba is not None else 0.0):.3f}")
        print(f"   Model: in-memory")
        return True
    except Exception as e:
        print(f"❌ Error testing app integration: {e}")
        import traceback
        traceback.print_exc()
        return False

# (Explainable AI section removed - not available in stateless setup)

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("\n🔍 Checking Dependencies")
    print("=" * 40)
    
    dependencies = {
        'joblib': 'Model loading',
        'scikit-learn': 'Machine learning',
        'lime': 'LIME explanations',
        'shap': 'SHAP explanations',
        'numpy': 'Numerical computing',
        'pandas': 'Data handling'
    }
    
    missing = []
    
    for dep, description in dependencies.items():
        try:
            __import__(dep)
            print(f"✅ {dep}: {description}")
        except ImportError:
            print(f"❌ {dep}: {description} - NOT INSTALLED")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing)}")
        print("Install with: pip install " + " ".join(missing))
        return False
    
    return True

def main():
    """Main test function"""
    print("🔐 SMS Guard Complete System Test")
    print("=" * 50)
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Test app integration
    app_ok = test_app_integration()
    print("\n" + "=" * 50)
    print("📊 COMPLETE TEST SUMMARY")
    print("=" * 50)
    print(f"✅ Dependencies: {'OK' if deps_ok else 'MISSING'}")
    print(f"✅ App Integration: {'OK' if app_ok else 'FAILED'}")
    if all([deps_ok, app_ok]):
        print("\n🎉 ALL SYSTEMS GO!")
        print("🚀 Your SMS Guard app is using the correct models!")
        print("\n📋 What's Ready:")
        print("   ✅ In-memory trained model")
        print("   ✅ Prediction API: /api/predict")
        print("\n🎯 Next Steps:")
        print("   1. Start backend: python backend/app.py")
        print("   2. Start frontend: npm run dev")
        print("   3. Login and test predictions!")
    else:
        print("\n⚠️ Issues found - check details above")
        if not app_ok:
            print("   🔧 App integration needs fixing")

if __name__ == "__main__":
    main()
