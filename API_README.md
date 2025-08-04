# 🚀 Pratibimb FastAPI Integration

This FastAPI wrapper exposes all the powerful features of `pratibimb.py` through a modern REST API, making it easy to integrate with web UIs, mobile apps, and other services.

## 🎯 Features

### Core Functionality
- **Text to Braille Conversion**: Grade 1 Unicode Braille conversion
- **Embosser-Ready Output**: Professional BRF format for tactile printers
- **Real-time Processing**: Live status updates during conversion
- **Batch Processing**: Convert multiple texts simultaneously
- **Content Validation**: Embosser format compliance checking
- **Content Analysis**: Detailed statistics and metrics

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/convert` | POST | Convert text to Braille format |
| `/api/status/{id}` | GET | Get conversion status |
| `/api/validate` | POST | Validate Braille content |
| `/api/bulk-convert` | POST | Batch convert multiple texts |
| `/api/config` | GET | Get current configuration |
| `/api/history` | GET | Get conversion history |
| `/api/logs` | GET | Get recent log entries |
| `/api/download/{id}` | GET | Download conversion files |
| `/health` | GET | Health check |

## 🚀 Quick Start

### Method 1: Using the Startup Scripts

#### Windows (PowerShell)
```powershell
.\start_server.ps1
```

#### Python (Cross-platform)
```bash
python start_server.py
```

### Method 2: Manual Startup

#### 1. Install Dependencies
```bash
pip install -r requirements-api.txt
```

#### 2. Start the FastAPI Server
```bash
python -m uvicorn api:app --host 0.0.0.0 --port 8001 --reload
```

#### 3. Serve the UI (separate terminal)
```bash
cd ui
python -m http.server 3000
```

### Method 3: Direct API Usage

#### Start only the API server:
```bash
python api.py
```

## 📖 API Documentation

Once running, visit:
- **Interactive Docs**: http://localhost:8001/docs
- **Alternative Docs**: http://localhost:8001/redoc
- **API Health**: http://localhost:8001/health

## 💡 Usage Examples

### Basic Text Conversion

```python
import requests

# Convert text to Braille
response = requests.post("http://localhost:8001/api/convert", json={
    "text": "Hello World! How are you today?",
    "config": {
        "braille_settings": {
            "preserve_line_breaks": True,
            "tab_width": 4
        },
        "embosser_settings": {
            "line_length": 40,
            "page_length": 25,
            "include_page_numbers": True
        }
    }
})

result = response.json()
print("Original:", result["original_text"])
print("Braille:", result["braille_unicode"])
print("BRF:", result["embosser_brf"])
```

### JavaScript Integration

```javascript
// Convert text using fetch API
const convertText = async (text) => {
    const response = await fetch('http://localhost:8000/api/convert', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: text,
            config: {
                braille_settings: {
                    preserve_line_breaks: true
                }
            }
        })
    });
    
    const result = await response.json();
    return result;
};

// Use in your application
convertText("Hello Braille World!")
    .then(result => {
        console.log("Conversion successful:", result);
        // Update your UI with result.braille_unicode
    })
    .catch(error => {
        console.error("Conversion failed:", error);
    });
```

### Batch Processing

```python
# Convert multiple texts at once
response = requests.post("http://localhost:8000/api/bulk-convert", json={
    "texts": [
        "First document to convert",
        "Second document to convert", 
        "Third document to convert"
    ],
    "config": {
        "embosser_settings": {
            "line_length": 40
        }
    }
})

results = response.json()
for i, result in enumerate(results["results"]):
    print(f"Document {i+1}: {len(result['braille_unicode'])} Braille chars")
```

### Validation

```python
# Validate Braille content
response = requests.post("http://localhost:8000/api/validate", json={
    "content": "⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙",
    "format_type": "unicode",
    "config": {}
})

validation = response.json()
if validation["validation_report"]["valid"]:
    print("✅ Content is valid!")
else:
    print("❌ Validation errors:", validation["validation_report"]["errors"])
```

## 🔧 Configuration

The API uses the same `config.json` file as the main Pratibimb application. Key settings:

```json
{
    "braille_settings": {
        "preserve_line_breaks": true,
        "tab_width": 4,
        "skip_carriage_returns": true
    },
    "embosser_settings": {
        "line_length": 40,
        "page_length": 25,
        "include_page_numbers": true,
        "validate_output": true
    },
    "logging_settings": {
        "log_level": "INFO",
        "log_file": "logs/pratibimb.log",
        "include_console_output": true
    }
}
```

## 📊 Response Format

### Conversion Response
```json
{
    "success": true,
    "conversion_id": "conv_abc12345",
    "original_text": "Hello World!",
    "braille_unicode": "⠓⠑⠇⠇⠕ ⠺⠕⠗⠇⠙⠖",
    "embosser_brf": "8ELLO WORLD6",
    "stats": {
        "original_characters": 12,
        "original_words": 2,
        "braille_characters": 13,
        "embosser_pages": 1,
        "embosser_lines": 1,
        "conversion_ratio": 1.08,
        "reading_time_minutes": 0.05,
        "processing_time_ms": 45
    },
    "analysis": {
        "character_count": 13,
        "line_count": 1,
        "word_count": 2,
        "paragraph_count": 1,
        "reading_time_minutes": 0.05
    },
    "validation": {
        "valid": true,
        "errors": [],
        "warnings": [],
        "stats": {
            "total_pages": 1,
            "total_lines": 1,
            "line_length_compliance": 100
        }
    },
    "timestamp": "2025-07-12T10:30:00Z",
    "processing_time_ms": 45
}
```

## 🔒 Security Notes

- **CORS**: Currently configured to allow all origins (`*`) for development
- **Rate Limiting**: Not implemented (add nginx or similar for production)
- **Authentication**: Not implemented (add JWT or similar for production)
- **File Access**: Limited to designated output directories

## 🚀 Production Deployment

For production deployment:

1. **Configure CORS** properly in `api.py`
2. **Add authentication** middleware
3. **Use proper WSGI server** like gunicorn
4. **Add rate limiting** and monitoring
5. **Set up proper logging** and error tracking

Example production startup:
```bash
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🔄 Integration with UI

The web UI in the `ui/` folder is already configured to work with this API:

1. **Real-time Processing**: Shows live conversion progress
2. **Error Handling**: Displays user-friendly error messages  
3. **File Downloads**: Direct download of BRF and Unicode files
4. **History Tracking**: Maintains conversion history
5. **Log Monitoring**: Displays recent processing logs

## 📞 Support

- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Logs**: Check `logs/pratibimb.log` for detailed information
- **Configuration**: Edit `config.json` for custom settings

Happy Converting! 🔤✨
