#!/bin/bash
echo "🔍 PRATIBIMB SETUP VERIFICATION"
echo "Testing environment setup..."
if [ -d "venv" ]; then
    echo "✅ Virtual environment: OK"
    source venv/bin/activate
else
    echo "❌ Virtual environment: Missing"
fi

python3 -c "
try:
    import fastapi; print(\"✅ FastAPI: OK\")
except: print(\"❌ FastAPI: Missing\")
try:
    import uvicorn; print(\"✅ Uvicorn: OK\")
except: print(\"❌ Uvicorn: Missing\")
try:
    import torch; print(\"✅ PyTorch: OK\")
except: print(\"❌ PyTorch: Missing\")
"

if [ -f ".env" ]; then
    echo "✅ Environment file: OK"
else
    echo "❌ Environment file: Missing"
fi

echo "Verification complete!"
