#!/usr/bin/env python3
"""
Test script to check report endpoints
"""
import os
import json

def test_reports_folder():
    """Test if reports folder exists and has files"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_folder = os.path.join(script_dir, 'reports')
    
    print(f"🔍 Script directory: {script_dir}")
    print(f"📁 Reports folder: {reports_folder}")
    print(f"📂 Reports folder exists: {os.path.exists(reports_folder)}")
    
    if os.path.exists(reports_folder):
        files = os.listdir(reports_folder)
        html_files = [f for f in files if f.endswith('.html')]
        print(f"📋 Total files: {len(files)}")
        print(f"📊 HTML files: {len(html_files)}")
        
        if html_files:
            print("📄 HTML files found:")
            for i, f in enumerate(html_files[:5]):  # Show first 5
                print(f"   {i+1}. {f}")
            if len(html_files) > 5:
                print(f"   ... and {len(html_files) - 5} more")
            
            latest_report = sorted(html_files)[-1]
            print(f"🏆 Latest report: {latest_report}")
            
            # Check if latest report file is readable
            latest_path = os.path.join(reports_folder, latest_report)
            try:
                with open(latest_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"✅ Latest report is readable ({len(content)} characters)")
            except Exception as e:
                print(f"❌ Cannot read latest report: {e}")
        else:
            print("❌ No HTML files found")
    else:
        print("❌ Reports folder does not exist")

if __name__ == "__main__":
    test_reports_folder()
