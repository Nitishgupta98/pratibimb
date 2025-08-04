# Gemini Integration Setup Guide

## 📁 Folder Structure Created:
```
Text2Braile/
└── gemini/
    ├── config.env          # Environment configuration
    ├── requirements.txt    # Python dependencies
    ├── gemini_client.py   # Main Gemini client class
    ├── test_setup.py      # Environment test script
    └── README.md          # This file
```

## 🚀 Quick Setup Instructions:

### Step 1: Install Dependencies
```bash
# Navigate to the gemini folder
cd gemini

# Install required packages
pip install -r requirements.txt
```

### Step 2: Configure API Key
1. Open `config.env` file
2. Replace `your_activation_key_here` with your actual Gemini API key:
   ```
   GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_HERE
   ```

### Step 3: Test Connection
```bash
# Test environment setup
python test_setup.py

# Test Gemini connection
python gemini_client.py
```

## 🔧 Configuration Options

The `config.env` file contains these settings:

- **GEMINI_API_KEY**: Your activation key for Gemini API
- **GEMINI_MODEL_NAME**: Model to use (gemini-1.5-flash)
- **GEMINI_TEMPERATURE**: Creativity level (0.7)
- **GEMINI_MAX_TOKENS**: Maximum response length (2048)
- **GEMINI_TOP_P**: Nucleus sampling parameter (0.9)
- **GEMINI_TOP_K**: Top-k sampling parameter (40)

## 📚 Usage Examples

### Basic Text Generation
```python
from gemini_client import GeminiClient

client = GeminiClient()
response = client.generate_text("Explain braille reading in simple terms")
print(response)
```

### Braille-Friendly Content
```python
client = GeminiClient()
description = client.generate_braille_description("Complex visual diagram")
print(description)
```

### Test Connection
```python
client = GeminiClient()
result = client.test_connection()
if result["success"]:
    print("✅ Connected successfully!")
else:
    print(f"❌ Error: {result['error']}")
```

## 🔍 Troubleshooting

### Common Issues:

1. **Import Error**: Install dependencies with `pip install -r requirements.txt`
2. **API Key Error**: Update your key in `config.env`
3. **Permission Error**: Verify API key has proper permissions
4. **Network Error**: Check internet connection

### Getting Your API Key:
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to `config.env`

## 🎯 Integration with Pratibimb Platform

The GeminiClient class provides:
- **Text Generation**: For content enhancement
- **Braille Descriptions**: Convert complex content to braille-friendly format
- **Accessibility Features**: AI-powered content optimization
- **Error Handling**: Robust error management
- **Configuration**: Flexible settings via environment variables

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your API key is valid
3. Ensure internet connectivity
4. Review error messages in console output
