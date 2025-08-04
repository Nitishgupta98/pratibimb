#!/usr/bin/env python3
"""
Braille to Text Converter - Reverse conversion from Braille Unicode to English
Convert Grade 1 Braille back to readable English text
"""

import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from braille_converter import load_config

def braille_to_text(braille_text, config=None):
    """
    Convert Grade 1 Unicode Braille back to English text.
    
    Args:
        braille_text (str): Unicode Braille text to convert
        config (dict): Configuration settings
        
    Returns:
        str: English text representation
    """
    
    # Default settings if no config provided
    if config is None:
        config = {
            'braille_settings': {
                'tab_spaces': 2,
                'preserve_line_breaks': True,
                'skip_carriage_returns': True
            }
        }
    
    braille_settings = config.get('braille_settings', {})
    
    # Reverse mapping from Braille to English
    braille_to_english = {
        '\u2801': 'a',  # ⠁
        '\u2803': 'b',  # ⠃
        '\u2809': 'c',  # ⠉
        '\u2819': 'd',  # ⠙
        '\u2811': 'e',  # ⠑
        '\u280b': 'f',  # ⠋
        '\u281b': 'g',  # ⠛
        '\u2813': 'h',  # ⠓
        '\u280a': 'i',  # ⠊
        '\u281a': 'j',  # ⠚
        '\u2805': 'k',  # ⠅
        '\u2807': 'l',  # ⠇
        '\u280d': 'm',  # ⠍
        '\u281d': 'n',  # ⠝
        '\u2815': 'o',  # ⠕
        '\u280f': 'p',  # ⠏
        '\u281f': 'q',  # ⠟
        '\u2817': 'r',  # ⠗
        '\u280e': 's',  # ⠎
        '\u281e': 't',  # ⠞
        '\u2825': 'u',  # ⠥
        '\u2827': 'v',  # ⠧
        '\u283a': 'w',  # ⠺
        '\u282d': 'x',  # ⠭
        '\u283d': 'y',  # ⠽
        '\u2835': 'z',  # ⠵
    }
    
    # Braille digits (0-9)
    braille_digits = {
        '\u281a': '1',  # ⠚ (j)
        '\u2803': '2',  # ⠃ (b)
        '\u2809': '3',  # ⠉ (c)
        '\u2819': '4',  # ⠙ (d)
        '\u2811': '5',  # ⠑ (e)
        '\u280b': '6',  # ⠋ (f)
        '\u281b': '7',  # ⠛ (g)
        '\u2813': '8',  # ⠓ (h)
        '\u280a': '9',  # ⠊ (i)
        '\u281a': '0',  # ⠚ (j) - Note: context dependent
    }
    
    # Braille punctuation
    braille_punctuation = {
        '\u2802': ',',    # ⠂
        '\u2806': ';',    # ⠆
        '\u2812': ':',    # ⠒
        '\u2816': '.',    # ⠖
        '\u2826': '!',    # ⠦
        '\u2822': '?',    # ⠢
        '\u2836': '"',    # ⠶
        '\u2836': '(',    # ⠶ (same as quote)
        '\u2836': ')',    # ⠶ (same as quote)
        '\u2824': '\'',   # ⠄
        '\u2820': '-',    # ⠠ (also capital indicator)
    }
    
    # Special Braille indicators
    CAPITAL_INDICATOR = '\u2820'  # ⠠
    NUMBER_INDICATOR = '\u283c'   # ⠼
    
    result = []
    i = 0
    in_number_mode = False
    
    while i < len(braille_text):
        char = braille_text[i]
        
        # Handle line breaks and whitespace
        if char == '\n':
            result.append('\n')
            in_number_mode = False
        elif char == ' ':
            result.append(' ')
            in_number_mode = False
        elif char == '\t':
            # Convert back to tabs or spaces based on config
            tab_spaces = braille_settings.get('tab_spaces', 2)
            result.append('\t')
        elif char == '\r' and not braille_settings.get('skip_carriage_returns', True):
            result.append('\r')
        
        # Handle capital indicator
        elif char == CAPITAL_INDICATOR:
            # Check if next character is a letter
            if i + 1 < len(braille_text) and braille_text[i + 1] in braille_to_english:
                next_char = braille_text[i + 1]
                result.append(braille_to_english[next_char].upper())
                i += 1  # Skip the next character as it's been processed
            else:
                # If not followed by a letter, treat as hyphen
                result.append('-')
        
        # Handle number indicator
        elif char == NUMBER_INDICATOR:
            in_number_mode = True
        
        # Handle digits (when in number mode)
        elif in_number_mode and char in braille_digits:
            # Special case for '0' which uses same pattern as 'j'
            if char == '\u281a':  # ⠚
                # Determine if it's '0' or '1' based on context
                # This is a simplification - in real Braille, context matters more
                result.append('0' if len(result) > 0 and result[-1].isdigit() else '1')
            else:
                result.append(braille_digits[char])
        
        # Handle regular letters
        elif char in braille_to_english:
            result.append(braille_to_english[char])
            in_number_mode = False
        
        # Handle punctuation
        elif char in braille_punctuation:
            result.append(braille_punctuation[char])
            in_number_mode = False
        
        # Unknown character
        else:
            # Keep unknown characters as-is
            result.append(char)
            in_number_mode = False
        
        i += 1
    
    return ''.join(result)

def convert_braille_file(input_file, output_file, config_file='config.json'):
    """
    Convert a Braille file back to English text
    
    Args:
        input_file (str): Path to Braille input file
        output_file (str): Path to English output file
        config_file (str): Configuration file path
    """
    
    # Load configuration
    config = load_config(config_file)
    
    try:
        print(f"🔤 Braille to Text Converter")
        print("=" * 50)
        print(f"📖 Reading Braille from '{input_file}'...")
        
        # Read Braille file
        with open(input_file, 'r', encoding=config.get('encoding', 'utf-8')) as f:
            braille_text = f.read()
        
        print(f"🔄 Converting Braille to English text...")
        
        # Convert to English
        english_text = braille_to_text(braille_text, config)
        
        print(f"💾 Saving English text to '{output_file}'...")
        
        # Write English output
        with open(output_file, 'w', encoding=config.get('encoding', 'utf-8')) as f:
            f.write(english_text)
        
        print(f"✅ English text saved to '{output_file}'")
        print(f"📊 Conversion Statistics:")
        print(f"   • Braille characters: {len(braille_text):,}")
        print(f"   • English characters: {len(english_text):,}")
        print(f"   • Input file: {input_file}")
        print(f"   • Output file: {output_file}")
        print(f"✅ Conversion completed successfully!")
        
    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found!")
    except Exception as e:
        print(f"❌ Error during conversion: {str(e)}")

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python braille_to_text.py <input_braille_file> <output_text_file>")
        print("Example: python braille_to_text.py braille_output.txt converted_text.txt")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    convert_braille_file(input_file, output_file)

if __name__ == "__main__":
    main()
