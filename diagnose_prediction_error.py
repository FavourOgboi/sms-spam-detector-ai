#!/usr/bin/env python3
"""
Diagnose the prediction error
"""

import sys
import os
sys.path.append('backend')

def check_model_files():
    """Check if model files exist and are readable"""
    print("🔍 Checking Model Files")
    print("=" * 40)
    
    model_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\clf_model.pkl'
    vectorizer_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\vectorizer.pkl'
    
    print(f"📁 Model path: {model_path}")
    print(f"📁 Vectorizer path: {vectorizer_path}")
    
    model_exists = os.path.exists(model_path)
    vectorizer_exists = os.path.exists(vectorizer_path)
    
    print(f"✅ Model exists: {model_exists}")
    print(f"✅ Vectorizer exists: {vectorizer_exists}")
    
    if model_exists:
        try:
            size = os.path.getsize(model_path)
            print(f"📊 Model size: {size} bytes")
        except Exception as e:
            print(f"❌ Error checking model size: {e}")
    
    if vectorizer_exists:
        try:
            size = os.path.getsize(vectorizer_path)
            print(f"📊 Vectorizer size: {size} bytes")
        except Exception as e:
            print(f"❌ Error checking vectorizer size: {e}")
    
    return model_exists and vectorizer_exists

def test_direct_loading():
    """Test loading models directly"""
    print("\n🔧 Testing Direct Model Loading")
    print("=" * 40)
    
    try:
        import joblib
        
        model_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\clf_model.pkl'
        vectorizer_path = r'C:\Users\USER\Documents\GitHub\sms-spam-detector-ai\models\main_model\vectorizer.pkl'
        
        print("Loading model...")
        model = joblib.load(model_path)
        print(f"✅ Model loaded: {type(model).__name__}")
        
        print("Loading vectorizer...")
        vectorizer = joblib.load(vectorizer_path)
        print(f"✅ Vectorizer loaded: {type(vectorizer).__name__}")
        
        # Test basic prediction
        test_text = "hello world"
        features = vectorizer.transform([test_text])
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        print(f"🧪 Test prediction: {'SPAM' if prediction == 1 else 'HAM'}")
        print(f"🧪 Test probabilities: {probabilities}")
        
        return True, model, vectorizer
        
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None

def test_nltk_setup():
    """Test NLTK setup"""
    print("\n🔧 Testing NLTK Setup")
    print("=" * 40)
    
    try:
        import nltk
        print("✅ NLTK imported")
        
        # Test punkt tokenizer
        try:
            nltk.data.find('tokenizers/punkt')
            print("✅ Punkt tokenizer available")
        except LookupError:
            print("⚠️ Punkt tokenizer missing - downloading...")
            nltk.download('punkt')
        
        # Test stopwords
        try:
            nltk.data.find('corpora/stopwords')
            print("✅ Stopwords available")
        except LookupError:
            print("⚠️ Stopwords missing - downloading...")
            nltk.download('stopwords')
        
        # Test tokenization
        from nltk.corpus import stopwords
        from nltk.stem.porter import PorterStemmer
        
        test_text = "This is a test message"
        tokens = nltk.word_tokenize(test_text.lower())
        print(f"🧪 Test tokenization: {tokens}")
        
        # Test stopwords
        stop_words = stopwords.words('english')
        print(f"🧪 Stopwords count: {len(stop_words)}")
        
        # Test stemming
        ps = PorterStemmer()
        stemmed = [ps.stem(word) for word in tokens if word.isalnum()]
        print(f"🧪 Test stemming: {stemmed}")
        
        return True
        
    except Exception as e:
        print(f"❌ NLTK error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_spam_detector():
    """Test the SpamDetector class"""
    print("\n🔧 Testing SpamDetector Class")
    print("=" * 40)
    
    try:
        from ml_model.spam_detector import spam_detector
        
        # Check initialization
        print(f"✅ SpamDetector imported")
        
        # Check model info
        info = spam_detector.get_model_info()
        print(f"📊 Model loaded: {info['model_loaded']}")
        print(f"📊 Vectorizer loaded: {info['vectorizer_loaded']}")
        print(f"📊 NLTK available: {info.get('nltk_available', 'Unknown')}")
        print(f"📊 Preprocessing: {info.get('preprocessing', 'Unknown')}")
        
        # Test preprocessing
        test_message = "Hello world this is a test"
        processed = spam_detector.preprocess_text(test_message)
        print(f"🧪 Preprocessing test:")
        print(f"   Input: {test_message}")
        print(f"   Output: {processed}")
        
        # Test prediction
        print(f"\n🧪 Prediction test:")
        result = spam_detector.predict(test_message)
        print(f"   Result: {result}")
        
        if 'error' in result:
            print(f"❌ Prediction error: {result.get('error', 'Unknown error')}")
            return False
        else:
            print(f"✅ Prediction successful: {result['prediction']}")
            return True
        
    except Exception as e:
        print(f"❌ SpamDetector error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main diagnostic function"""
    print("🔍 SMS Guard Prediction Error Diagnosis")
    print("=" * 60)
    
    # Check model files
    files_ok = check_model_files()
    
    # Test direct loading
    loading_ok, model, vectorizer = test_direct_loading()
    
    # Test NLTK
    nltk_ok = test_nltk_setup()
    
    # Test SpamDetector
    detector_ok = test_spam_detector()
    
    print("\n" + "=" * 60)
    print("📊 DIAGNOSIS SUMMARY")
    print("=" * 60)
    
    print(f"✅ Model Files: {'OK' if files_ok else 'FAILED'}")
    print(f"✅ Direct Loading: {'OK' if loading_ok else 'FAILED'}")
    print(f"✅ NLTK Setup: {'OK' if nltk_ok else 'FAILED'}")
    print(f"✅ SpamDetector: {'OK' if detector_ok else 'FAILED'}")
    
    if all([files_ok, loading_ok, nltk_ok, detector_ok]):
        print("\n🎉 ALL SYSTEMS WORKING!")
        print("The prediction error might be elsewhere.")
    else:
        print("\n🔧 ISSUES FOUND:")
        if not files_ok:
            print("   - Model files missing or inaccessible")
        if not loading_ok:
            print("   - Cannot load models directly")
        if not nltk_ok:
            print("   - NLTK setup problems")
        if not detector_ok:
            print("   - SpamDetector class issues")
        
        print("\n💡 RECOMMENDED FIXES:")
        if not files_ok:
            print("   1. Check model file paths")
            print("   2. Ensure models were saved correctly from notebook")
        if not loading_ok:
            print("   3. Retrain and save models from notebook")
        if not nltk_ok:
            print("   4. Install NLTK: pip install nltk")
            print("   5. Download NLTK data")
        if not detector_ok:
            print("   6. Fix SpamDetector initialization")

if __name__ == "__main__":
    main()
