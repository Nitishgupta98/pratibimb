#!/bin/bash
echo "🚀 PRATIBIMB PRODUCTION READINESS TEST"
echo "Starting test server..."

if [ -d "venv" ]; then
    source venv/bin/activate
fi

uvicorn main:app --host 127.0.0.1 --port 8888 &
SERVER_PID=$!
sleep 3

echo "Testing health endpoint..."
curl -s http://127.0.0.1:8888/health

echo "Testing text-to-braille..."
curl -s -X POST "http://127.0.0.1:8888/text-to-braille" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Hello\"}"

echo "Cleaning up..."
kill $SERVER_PID 2>/dev/null
echo "Production test complete!"
