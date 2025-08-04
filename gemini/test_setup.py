"""
Simple test script to verify Gemini setup
Run this after installing requirements
"""

import os
import sys

def check_environment():
    """Check if environment is properly configured"""
    print("🔍 Checking Gemini Environment Setup...")
    print("=" * 50)
    
    # Check if config.env exists
    config_path = os.path.join(os.path.dirname(__file__), 'config.env')
    if os.path.exists(config_path):
        print("✅ config.env file found")
        
        # Read config
        with open(config_path, 'r') as f:
            content = f.read()
            
        if 'GEMINI_API_KEY=your_activation_key_here' in content:
            print("⚠️  Please update your API key in config.env")
            return False
        else:
            print("✅ API key appears to be configured")
            
        if 'GEMINI_MODEL_NAME=gemini-1.5-flash' in content:
            print("✅ Model name configured: gemini-1.5-flash")
        
    else:
        print("❌ config.env file not found")
        return False
    
    # Check if required packages can be imported
    try:
        import google.generativeai
        print("✅ google-generativeai package available")
    except ImportError:
        print("❌ google-generativeai package not installed")
        print("   Run: pip install -r requirements.txt")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv package available")
    except ImportError:
        print("❌ python-dotenv package not installed")
        print("   Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main test function"""
    if check_environment():
        print("\n🎉 Environment setup looks good!")
        print("📋 Next steps:")
        print("1. Update your API key in gemini/config.env")
        print("2. Run: python gemini_client.py")
    else:
        print("\n❌ Environment setup needs attention")
        print("📋 Required steps:")
        print("1. Install packages: pip install -r requirements.txt")
        print("2. Update API key in gemini/config.env")
        print("3. Run this test again")

if __name__ == "__main__":
    main()
