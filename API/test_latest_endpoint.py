import requests
import json

def test_latest_endpoint():
    try:
        print("Testing /api/latest-report endpoint...")
        response = requests.get("http://localhost:8000/api/latest-report")
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content: {response.text}")
        
        if response.status_code == 200:
            print("✅ Success! Latest report filename retrieved.")
        else:
            print(f"❌ Failed with status {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Server might not be running on localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_server_status():
    try:
        print("Testing server status...")
        response = requests.get("http://localhost:8000/docs")
        print(f"Server docs status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("❌ Server might not be running properly")
    except Exception as e:
        print(f"❌ Server connection error: {e}")

if __name__ == "__main__":
    test_server_status()
    print()
    test_latest_endpoint()
