#!/usr/bin/env python3
"""
🔤 Braille Converter - Main Entry Point
Simple command-line interface for text-to-Braille conversion

Usage:
    python convert.py <input_file> [output_file]
    
Examples:
    python convert.py input.txt
    python convert.py input.txt output.txt
    python convert.py examples/input_text.txt output/braille_output.txt
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from braille_converter import text_to_braille_unicode, load_config

def main():
    """Main conversion function with user-friendly interface"""
    
    try:
        # Load configuration first
        config = load_config('config.json')
    except Exception as e:
        print(f"⚠️  Warning: Could not load config.json ({e}). Using defaults.")
        config = {
            "input_file": "input_text.txt",
            "output_file": "braille_output.txt",
            "encoding": "utf-8"
        }
    
    # Determine input and output files
    if len(sys.argv) >= 2:
        # Command line arguments provided - use them
        input_file = sys.argv[1]
        
        if len(sys.argv) >= 3:
            output_file = sys.argv[2]
        else:
            # Create output filename by adding _braille before extension
            base_name = os.path.splitext(input_file)[0]
            extension = os.path.splitext(input_file)[1]
            output_file = f"{base_name}_braille.txt"
    else:
        # No command line arguments - use config file
        input_file = config.get('input_file', 'input_text.txt')
        output_file = config.get('output_file', 'braille_output.txt')
        
        # Check if config file input exists
        if not os.path.exists(input_file):
            print("🔤 Pratibimb - Braille Converter")
            print("=" * 50)
            print("Convert English text to Grade 1 Unicode Braille")
            print()
            print("📋 Configuration Mode:")
            print(f"  • Input file (from config): {input_file}")
            print(f"  • Output file (from config): {output_file}")
            print()
            print("❌ Input file not found! You can:")
            print("  1. Create the file specified in config.json")
            print("  2. Update config.json with correct file path")
            print("  3. Use command line: python convert.py <input_file> [output_file]")
            print()
            print("📁 Available Tools:")
            print("  • GUI Interface: python tools/braille_gui.py")
            print("  • Batch Convert: python tools/batch_converter.py")
            print("  • Embosser Format: python tools/braille_embosser_formatter.py")
            print("  • Back to Text: python tools/braille_to_text.py")
            print("  • Analysis: python tools/braille_analyzer.py")
            print()
            print("📚 Documentation: Open ui/Documentation.html in your browser")
            sys.exit(1)
    
    try:
        print(f"🔤 Pratibimb - Braille Converter")
        print("=" * 50)
        
        # Show which mode we're using
        if len(sys.argv) >= 2:
            print("📝 Command Line Mode:")
            print(f"📖 Reading: {input_file}")
            print(f"💾 Output: {output_file}")
        else:
            print("📋 Configuration Mode:")
            print(f"📖 Reading: {input_file} (from config)")
            print(f"💾 Output: {output_file} (from config)")
        
        print()
        
        # Load configuration
        config = load_config('config.json')
        
        # Read input file
        with open(input_file, 'r', encoding=config.get('encoding', 'utf-8')) as f:
            text = f.read()
        
        print(f"🔄 Converting to Grade 1 Braille...")
        
        # Convert to Braille
        braille_text = text_to_braille_unicode(text, config)
        
        # Write output file
        with open(output_file, 'w', encoding=config.get('encoding', 'utf-8')) as f:
            f.write(braille_text)
        
        # Calculate statistics
        char_count = len(text)
        braille_count = len(braille_text)
        lines = braille_text.count('\n') + 1
        
        print(f"✅ Conversion completed successfully!")
        print()
        print(f"📊 Statistics:")
        print(f"   • Original characters: {char_count:,}")
        print(f"   • Braille characters: {braille_count:,}")
        print(f"   • Lines: {lines:,}")
        print()
        print(f"🎯 Next Steps:")
        print(f"   • View output: {output_file}")
        print(f"   • For embosser: python tools/braille_embosser_formatter.py {input_file} output.brl")
        print(f"   • Validate: python tools/embosser_validator.py output.brl")
        print(f"   • GUI view: python tools/braille_gui.py")
        
    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found!")
        print(f"💡 Make sure the file path is correct and the file exists.")
        if len(sys.argv) < 2:
            print(f"💡 You can also update the 'input_file' path in config.json")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
