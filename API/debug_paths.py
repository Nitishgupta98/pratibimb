#!/usr/bin/env python3
"""
Debug script to test path resolution for reports
"""
import os

def debug_paths():
    """Debug the path resolution for reports folder"""
    print("🔍 DEBUG: Path Resolution for Reports")
    print("=" * 50)
    
    # Get current script location
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    
    print(f"📍 Current script: {current_file}")
    print(f"📁 Current directory: {current_dir}")
    
    # Test all possible paths
    possible_paths = [
        os.path.join(current_dir, 'reports'),  # Same directory as script
        os.path.join(os.path.dirname(current_dir), 'reports'),  # Parent directory
        os.path.join(current_dir, '..', 'reports'),  # Explicit parent
    ]
    
    print(f"\n🧪 Testing {len(possible_paths)} possible paths:")
    
    for i, path in enumerate(possible_paths, 1):
        abs_path = os.path.abspath(path)
        exists = os.path.exists(abs_path)
        print(f"   {i}. {path}")
        print(f"      → Absolute: {abs_path}")
        print(f"      → Exists: {'✅ YES' if exists else '❌ NO'}")
        
        if exists:
            try:
                files = os.listdir(abs_path)
                html_files = [f for f in files if f.endswith('.html')]
                print(f"      → Files: {len(files)} total, {len(html_files)} HTML")
                if html_files:
                    latest = sorted(html_files)[-1]
                    print(f"      → Latest: {latest}")
            except Exception as e:
                print(f"      → Error reading: {e}")
        print()
    
    # Also check if we're in a nested API folder
    print("🔍 Directory structure analysis:")
    parts = current_dir.split(os.sep)
    if 'API' in parts:
        api_indices = [i for i, part in enumerate(parts) if part == 'API']
        print(f"   Found 'API' at positions: {api_indices}")
        if len(api_indices) > 1:
            print("   ⚠️  WARNING: Multiple 'API' folders detected - might be in nested structure")

if __name__ == "__main__":
    debug_paths()
