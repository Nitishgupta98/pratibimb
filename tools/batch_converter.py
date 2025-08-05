#!/usr/bin/env python3
"""
Batch Braille Converter - Process multiple files
Convert multiple text files to Braille in batch mode
"""

import os
import json
import glob
import argparse
from pathlib import Path
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from braille_converter import text_to_braille_unicode, load_config

def batch_convert_files(input_pattern, output_dir=None, config_file='config.json'):
    """
    Convert multiple files matching a pattern to Braille
    
    Args:
        input_pattern (str): Glob pattern for input files (e.g., "*.txt", "docs/*.txt")
        output_dir (str): Directory for output files (default: same as input)
        config_file (str): Configuration file path
    """
    
    # Load configuration
    config = load_config(config_file)
    
    # Find matching files
    input_files = glob.glob(input_pattern)
    
    if not input_files:
        print(f"❌ No files found matching pattern: {input_pattern}")
        return
    
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    successful_conversions = 0
    total_files = len(input_files)
    
    print(f"🔄 Batch Braille Conversion Started")
    print(f"📂 Found {total_files} files matching: {input_pattern}")
    print("=" * 60)
    
    for i, input_file in enumerate(input_files, 1):
        try:
            print(f"📄 [{i}/{total_files}] Processing: {input_file}")
            
            # Read input file
            with open(input_file, 'r', encoding=config.get('encoding', 'utf-8')) as f:
                text = f.read()
            
            # Convert to Braille
            braille_text = text_to_braille_unicode(text, config)
            
            # Determine output file path
            input_path = Path(input_file)
            if output_dir:
                output_file = os.path.join(output_dir, f"{input_path.stem}_braille{input_path.suffix}")
            else:
                output_file = str(input_path.parent / f"{input_path.stem}_braille{input_path.suffix}")
            
            # Write Braille output
            with open(output_file, 'w', encoding=config.get('encoding', 'utf-8')) as f:
                f.write(braille_text)
            
            print(f"   ✅ Saved to: {output_file}")
            print(f"   📊 {len(text)} chars → {len(braille_text)} Braille chars")
            successful_conversions += 1
            
        except Exception as e:
            print(f"   ❌ Error processing {input_file}: {str(e)}")
    
    print("=" * 60)
    print(f"✅ Batch conversion completed!")
    print(f"📈 Successfully converted: {successful_conversions}/{total_files} files")
    
    if successful_conversions < total_files:
        print(f"⚠️  Failed conversions: {total_files - successful_conversions}")

def main():
    parser = argparse.ArgumentParser(description='Batch convert text files to Braille')
    parser.add_argument('pattern', help='Glob pattern for input files (e.g., "*.txt", "docs/*.txt")')
    parser.add_argument('-o', '--output-dir', help='Output directory (default: same as input)')
    parser.add_argument('-c', '--config', default='config.json', help='Configuration file')
    
    args = parser.parse_args()
    
    try:
        batch_convert_files(args.pattern, args.output_dir, args.config)
    except KeyboardInterrupt:
        print("\n❌ Batch conversion interrupted by user")
    except Exception as e:
        print(f"❌ Batch conversion failed: {str(e)}")

if __name__ == "__main__":
    main()
