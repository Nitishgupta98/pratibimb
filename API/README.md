# Pratibimb API Server

## Quick Start

### Option 1: Automatic Setup (Recommended)
1. Double-click `start_server.bat` - This will automatically:
   - Check Python installation
   - Create virtual environment
   - Install all dependencies
   - Start the API server

### Option 2: Manual Setup
1. Run `setup.bat` first (one-time setup)
2. Then use `quick_start.bat` for faster startup

### Option 3: Command Line
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Testing
- Run `test_api.bat` to verify the server is working
- Visit http://localhost:8000/docs for API documentation

## API Endpoints
- `POST /process_transcript` - Process YouTube video and get both raw and enhanced transcripts
- `POST /get_raw_transcript` - Get raw transcript from YouTube video
- `POST /get_enhance_transcript` - Enhance existing transcript for visually impaired users

## Requirements
- Python 3.8 or higher
- Windows 10/11 or Windows VM
- Internet connection for package installation

## Configuration
- Edit `config.json` to change output folders or API keys
- Logs are saved to `Output_files/api_logs.txt`
- Transcript files are saved to `Output_files/` folder

## Troubleshooting
1. **Python not found**: Install Python from https://www.python.org/downloads/
2. **Port 8000 in use**: Change port in start_server.bat or stop other services
3. **Missing packages**: Run setup.bat again or install manually
4. **API key issues**: Check config.json for valid Google AI API key

## File Structure
```
API/
├── main.py                 # Main API application
├── config.json            # Configuration file
├── requirements.txt       # Python dependencies
├── start_server.bat       # Main startup script
├── quick_start.bat        # Quick startup (after setup)
├── setup.bat             # One-time setup script
├── test_api.bat          # API testing script
├── venv/                 # Virtual environment (created automatically)
└── Output_files/         # Generated transcripts and logs
```
