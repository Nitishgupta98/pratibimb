import sys
import os

# Add the current directory to path to import main
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

def check_routes():
    print("=== FastAPI Routes Debug ===")
    print("Registered routes:")
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            print(f"  {list(route.methods)} {route.path}")
    
    print("\nChecking for /api/latest-report specifically:")
    latest_route_found = False
    for route in app.routes:
        if hasattr(route, 'path') and '/api/latest-report' in route.path:
            print(f"  ✅ Found: {list(route.methods)} {route.path}")
            latest_route_found = True
    
    if not latest_route_found:
        print("  ❌ /api/latest-report route NOT found!")
    
    print("\nChecking reports folder:")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    reports_path = os.path.join(current_dir, 'reports')
    print(f"  Reports path: {reports_path}")
    print(f"  Exists: {os.path.exists(reports_path)}")
    
    if os.path.exists(reports_path):
        html_files = [f for f in os.listdir(reports_path) if f.endswith('.html')]
        print(f"  HTML files: {html_files}")
        if html_files:
            latest = sorted(html_files)[-1]
            print(f"  Latest file: {latest}")

if __name__ == "__main__":
    check_routes()
