"""
Gemini API Key Setup and Test Demo
This script demonstrates how to set up and test your Gemini API key
"""

import os

def show_current_config():
    """Display current configuration"""
    print("📋 Current Gemini Configuration:")
    print("=" * 40)
    
    config_path = os.path.join(os.path.dirname(__file__), 'config.env')
    
    try:
        with open(config_path, 'r') as f:
            lines = f.readlines()
            
        for line in lines:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                if 'API_KEY' in key:
                    # Mask the API key for security
                    if value == 'your_activation_key_here':
                        print(f"   {key}: ⚠️  NOT SET - Please add your key")
                    else:
                        masked = value[:8] + '*' * (len(value) - 12) + value[-4:] if len(value) > 12 else '*' * len(value)
                        print(f"   {key}: {masked}")
                else:
                    print(f"   {key}: {value}")
                    
    except FileNotFoundError:
        print("❌ config.env file not found!")

def test_with_dummy_key():
    """Test the client with a dummy key to show error handling"""
    print("\n🧪 Testing with placeholder key (will fail):")
    print("-" * 50)
    
    try:
        from gemini_client import GeminiClient
        client = GeminiClient()
        result = client.test_connection()
        
        if result["success"]:
            print("✅ Connection successful!")
            print(f"📝 Response: {result['response']}")
        else:
            print(f"❌ Expected failure: {result['error']}")
            
    except Exception as e:
        print(f"❌ Expected error: {str(e)}")
        
    print("\n💡 This is expected! Update your API key in config.env to test properly.")

def show_instructions():
    """Show step-by-step instructions"""
    print("\n📚 How to Set Up Your API Key:")
    print("=" * 40)
    print("1. 🌐 Go to: https://makersuite.google.com/app/apikey")
    print("2. 🔑 Create a new API key")
    print("3. 📋 Copy the generated key")
    print("4. 📝 Open: gemini/config.env")
    print("5. ✏️  Replace 'your_activation_key_here' with your actual key")
    print("6. 💾 Save the file")
    print("7. 🚀 Run: python gemini_client.py")

def main():
    """Main demonstration function"""
    print("🚀 Gemini Setup and Test Demo")
    print("=" * 50)
    
    # Show current configuration
    show_current_config()
    
    # Show instructions
    show_instructions()
    
    # Test with current setup
    test_with_dummy_key()
    
    print("\n🎯 Next Steps:")
    print("1. Add your real API key to config.env")
    print("2. Run: python test_setup.py")
    print("3. Run: python gemini_client.py")
    print("4. Start using Gemini in your applications!")

if __name__ == "__main__":
    main()
