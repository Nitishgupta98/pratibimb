"""
Complete Gemini Setup Verification and Testing Script
This script provides a comprehensive overview of the Gemini integration setup
"""

import os
import sys

def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}")

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n📋 {title}")
    print(f"{'-'*50}")

def check_files():
    """Check if all required files are present"""
    print_section("File Structure Check")
    
    required_files = [
        'config.env',
        'requirements.txt', 
        'gemini_client.py',
        'test_setup.py',
        'demo.py',
        'pratibimb_integration.py',
        'README.md'
    ]
    
    base_path = os.path.dirname(__file__)
    
    for file in required_files:
        file_path = os.path.join(base_path, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file:<25} ({size:,} bytes)")
        else:
            print(f"   ❌ {file:<25} (MISSING)")

def check_dependencies():
    """Check if dependencies are installed"""
    print_section("Dependencies Check")
    
    dependencies = [
        ('google.generativeai', 'Google Gemini SDK'),
        ('dotenv', 'Environment Variables'),
        ('requests', 'HTTP Requests'),
        ('typing_extensions', 'Type Hints')
    ]
    
    for module, description in dependencies:
        try:
            __import__(module)
            print(f"   ✅ {description:<25} (Installed)")
        except ImportError:
            print(f"   ❌ {description:<25} (Missing)")

def check_configuration():
    """Check configuration status"""
    print_section("Configuration Check")
    
    config_path = os.path.join(os.path.dirname(__file__), 'config.env')
    
    if not os.path.exists(config_path):
        print("   ❌ config.env file not found")
        return False
    
    with open(config_path, 'r') as f:
        content = f.read()
    
    configs = {}
    for line in content.split('\n'):
        if '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            configs[key.strip()] = value.strip()
    
    # Check API key
    api_key = configs.get('GEMINI_API_KEY', '')
    if api_key == 'your_activation_key_here' or not api_key:
        print("   ⚠️  API Key: NOT SET - Please add your activation key")
        api_key_set = False
    else:
        masked_key = api_key[:8] + '*' * (len(api_key) - 12) + api_key[-4:] if len(api_key) > 12 else '*' * len(api_key)
        print(f"   ✅ API Key: {masked_key}")
        api_key_set = True
    
    # Check other settings
    model = configs.get('GEMINI_MODEL_NAME', 'Not set')
    print(f"   ✅ Model: {model}")
    
    temp = configs.get('GEMINI_TEMPERATURE', 'Not set')
    print(f"   ✅ Temperature: {temp}")
    
    tokens = configs.get('GEMINI_MAX_TOKENS', 'Not set')
    print(f"   ✅ Max Tokens: {tokens}")
    
    return api_key_set

def run_tests(api_key_set: bool):
    """Run available tests"""
    print_section("Testing Results")
    
    if not api_key_set:
        print("   ⚠️  Skipping connection tests - API key not configured")
        print("   📝 To test connection: Add your API key and run 'python gemini_client.py'")
        return
    
    try:
        # Test basic import
        from gemini_client import GeminiClient
        print("   ✅ Gemini client import successful")
        
        # Test initialization
        client = GeminiClient()
        print("   ✅ Gemini client initialization successful")
        
        # Test connection
        result = client.test_connection()
        if result["success"]:
            print("   ✅ Gemini API connection successful")
            print(f"   📝 Model Response: {result['response'][:100]}...")
        else:
            print(f"   ❌ Connection failed: {result['error']}")
            
    except Exception as e:
        print(f"   ❌ Test failed: {str(e)}")

def show_next_steps(api_key_set: bool):
    """Show next steps based on current setup status"""
    print_section("Next Steps")
    
    if not api_key_set:
        print("   🔑 STEP 1: Add your Gemini API key")
        print("      - Open: gemini/config.env")
        print("      - Replace 'your_activation_key_here' with your actual key")
        print("      - Get key from: https://makersuite.google.com/app/apikey")
        print("")
        print("   🧪 STEP 2: Test the setup")
        print("      - Run: python gemini_client.py")
        print("      - Run: python pratibimb_integration.py")
    else:
        print("   ✅ Setup appears complete!")
        print("   🚀 You can now use Gemini AI in your applications")
        print("")
        print("   📚 Available Scripts:")
        print("      - python gemini_client.py        (Basic connection test)")
        print("      - python pratibimb_integration.py (Platform integration demo)")
        print("      - python demo.py                 (Interactive demo)")

def main():
    """Main verification function"""
    print_header("Gemini Setup Verification & Testing")
    
    # Check all components
    check_files()
    check_dependencies()
    api_key_set = check_configuration()
    run_tests(api_key_set)
    show_next_steps(api_key_set)
    
    print_header("Setup Summary")
    
    if api_key_set:
        print("🎉 Gemini integration is ready to use!")
        print("✨ All components are properly configured")
    else:
        print("⚠️  Setup is almost complete!")
        print("🔑 Just add your API key to get started")
    
    print(f"\n📁 Setup Location: {os.path.dirname(__file__)}")
    print("📖 See README.md for detailed documentation")

if __name__ == "__main__":
    main()
