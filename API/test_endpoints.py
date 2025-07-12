#!/usr/bin/env python3
"""
Simple test to check if the report endpoints work
"""
import os
import json

def test_reports_access():
    """Test if we can access reports the same way the API does"""
    print("🧪 Testing Reports Access")
    print("=" * 40)
    
    # Simulate the same logic as the API
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(current_dir, 'reports'),  # Same directory as main.py
        os.path.join(os.path.dirname(current_dir), 'reports'),  # Parent directory
        os.path.join(current_dir, '..', 'reports'),  # Explicit parent
    ]
    
    print(f"📁 Current directory: {current_dir}")
    print(f"🔍 Testing {len(possible_paths)} possible paths:")
    
    reports_folder = None
    for i, path in enumerate(possible_paths, 1):
        abs_path = os.path.abspath(path)
        exists = os.path.exists(abs_path)
        is_dir = os.path.isdir(abs_path) if exists else False
        
        print(f"   {i}. {path}")
        print(f"      → Absolute: {abs_path}")
        print(f"      → Exists: {'✅ YES' if exists else '❌ NO'}")
        print(f"      → Is Directory: {'✅ YES' if is_dir else '❌ NO'}")
        
        if exists and is_dir:
            if reports_folder is None:
                reports_folder = abs_path
                print(f"      → ⭐ SELECTED as reports folder")
            
            try:
                files = os.listdir(abs_path)
                html_files = [f for f in files if f.endswith('.html')]
                print(f"      → Files: {len(files)} total, {len(html_files)} HTML")
                if html_files:
                    latest = sorted(html_files)[-1]
                    print(f"      → Latest: {latest}")
                    
                    # Test reading the latest file
                    latest_path = os.path.join(abs_path, latest)
                    try:
                        with open(latest_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            print(f"      → File size: {len(content)} characters")
                            print(f"      → File readable: ✅ YES")
                    except Exception as read_err:
                        print(f"      → File readable: ❌ NO ({read_err})")
            except Exception as e:
                print(f"      → Error reading: {e}")
        print()
    
    print(f"🎯 Final result:")
    if reports_folder:
        print(f"   ✅ Reports folder found: {reports_folder}")
        
        # Test the API endpoints logic
        try:
            report_files = [f for f in os.listdir(reports_folder) if f.endswith('.html')]
            if report_files:
                latest_report = sorted(report_files)[-1]
                print(f"   📊 Latest report: {latest_report}")
                
                # Simulate API response
                api_response = {
                    "latest_report": latest_report,
                    "report_url": f"/api/reports/{latest_report}",
                    "full_url": f"http://localhost:8000/api/reports/{latest_report}"
                }
                print(f"   📡 API Response would be:")
                print(f"   {json.dumps(api_response, indent=6)}")
            else:
                print(f"   ❌ No HTML files found")
        except Exception as e:
            print(f"   ❌ Error accessing reports: {e}")
    else:
        print(f"   ❌ No reports folder found")

if __name__ == "__main__":
    test_reports_access()
