import requests
import json

url = "https://public-beckn.sandbox.run/sandbox/search"
payload = {
    "context": {
        "domain": "retail",
        "country": "IND",
        "city": "std:011",
        "action": "search",
        "core_version": "1.1.0",
        "bap_id": "buyer-app.ondc.org",
        "bap_uri": "https://a0b73638c65a.ngrok-free.app",
        "transaction_id": "12345",
        "message_id": "67890",
        "timestamp": "2025-08-01T12:00:00Z"
    },
    "message": {
        "intent": {
            "item": {
                "descriptor": {"name": "braille"}
            },
            "fulfillment": {
                "end": {
                    "location": {
                        "gps": "28.6139,77.2090",
                        "address": {"area_code": "110001"}
                    }
                }
            }
        }
    }
}

print('Sending request to:', url)
print('Payload:', json.dumps(payload))
try:
    response = requests.post(url, json=payload, timeout=10, verify=False)
    print('Response status code:', response.status_code)
    print('Response text:', response.text)
except Exception as e:
    import traceback
    print('ERROR:', e)
    traceback.print_exc()
