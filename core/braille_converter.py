#!/usr/bin/env python3
"""
Braille Converter - English Text to Grade 1 Unicode Braille
Expert Braille transcriber agent for precise Grade 1 Braille conversion

This script reads input text from a file specified in config.json and converts it
to Grade 1 Braille Unicode, saving the output to a specified file.
"""

import json
import os
import sys

def text_to_braille_unicode(text, config=None):
    """
    Convert English text to Grade 1 Unicode Braille characters.
    Follows strict Grade 1 Braille standards with letter-for-letter translation.
    
    BRAILLE-FRIENDLY FORMATTING:
    - Newlines (\n): Preserved for proper paragraph structure
    - Carriage returns (\r): Ignored to prevent duplication
    - Tabs (\t): Converted to configurable spaces (Braille display friendly)
    - Spaces: Preserved for word separation
    - All formatting maintains screen reader and Braille display compatibility
    
    Args:
        text (str): Input English text to convert
        config (dict): Configuration settings for Braille conversion
        
    Returns:
        str: Unicode Braille representation optimized for accessibility
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
    
    # Grade 1 Braille mapping for lowercase letters a-z
    braille_alphabet = {
        'a': '\u2801',  # ⠁
        'b': '\u2803',  # ⠃
        'c': '\u2809',  # ⠉
        'd': '\u2819',  # ⠙
        'e': '\u2811',  # ⠑
        'f': '\u280B',  # ⠋
        'g': '\u281B',  # ⠛
        'h': '\u2813',  # ⠓
        'i': '\u280A',  # ⠊
        'j': '\u281A',  # ⠚
        'k': '\u2805',  # ⠅
        'l': '\u2807',  # ⠇
        'm': '\u280D',  # ⠍
        'n': '\u281D',  # ⠝
        'o': '\u2815',  # ⠕
        'p': '\u280F',  # ⠏
        'q': '\u281F',  # ⠟
        'r': '\u2817',  # ⠗
        's': '\u280E',  # ⠎
        't': '\u281E',  # ⠞
        'u': '\u2825',  # ⠥
        'v': '\u2827',  # ⠧
        'w': '\u283A',  # ⠺
        'x': '\u282D',  # ⠭
        'y': '\u283D',  # ⠽
        'z': '\u2835',  # ⠵
    }
    
    # Punctuation mapping
    braille_punctuation = {
        '.': '\u2832',  # ⠲ (period)
        ',': '\u2802',  # ⠂ (comma)
        '?': '\u2826',  # ⠦ (question mark)
        '!': '\u2816',  # ⠖ (exclamation mark)
        "'": '\u2804',  # ⠄ (apostrophe)
        '-': '\u2824',  # ⠤ (hyphen/dash)
        '—': '\u2824',  # ⠤ (em-dash, same as hyphen in Braille)
        ':': '\u2812',  # ⠒ (colon)
        ';': '\u2806',  # ⠆ (semicolon)
        '"': '\u2836',  # ⠶ (quotation mark)
        '(': '\u2836',  # ⠶ (opening parenthesis)
        ')': '\u2836',  # ⠶ (closing parenthesis)
    }
    
    # Number mapping (digits 0-9 use letters a-j with number sign prefix)
    braille_numbers = {
        '1': '\u283C\u2801',  # ⠼⠁
        '2': '\u283C\u2803',  # ⠼⠃
        '3': '\u283C\u2809',  # ⠼⠉
        '4': '\u283C\u2819',  # ⠼⠙
        '5': '\u283C\u2811',  # ⠼⠑
        '6': '\u283C\u280B',  # ⠼⠋
        '7': '\u283C\u281B',  # ⠼⠛
        '8': '\u283C\u2813',  # ⠼⠓
        '9': '\u283C\u280A',  # ⠼⠊
        '0': '\u283C\u281A',  # ⠼⠚
    }
    
    # Special characters
    capital_sign = '\u2820'  # ⠠ (capital sign)
    blank_pattern = '\u2800'  # ⠀ (pattern blank for unsupported characters)
    
    result = []
    
    for char in text:
        if char == ' ':
            # Space remains as regular space
            result.append(' ')
        elif char == '\n':
            # Newline character - preserve line breaks
            result.append('\n')
        elif char == '\r':
            # Carriage return - typically ignore or treat as newline
            continue  # Skip carriage returns
        elif char == '\t':
            # Tab character - convert to configurable spaces for Braille-friendly indentation
            tab_spaces = braille_settings.get('tab_spaces', braille_settings.get('tab_width', 4))
            result.append(' ' * tab_spaces)
        elif char.islower() and char in braille_alphabet:
            # Lowercase letter
            result.append(braille_alphabet[char])
        elif char.isupper() and char.lower() in braille_alphabet:
            # Uppercase letter (capital sign + lowercase braille)
            result.append(capital_sign + braille_alphabet[char.lower()])
        elif char.isdigit() and char in braille_numbers:
            # Number
            result.append(braille_numbers[char])
        elif char in braille_punctuation:
            # Punctuation
            result.append(braille_punctuation[char])
        else:
            # Unsupported character - use blank pattern
            result.append(blank_pattern)
    
    return ''.join(result)


def load_config(config_file='config.json'):
    """
    Load configuration from JSON file.
    
    Args:
        config_file (str): Path to the configuration file
        
    Returns:
        dict: Configuration settings
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        print("Please create a config.json file with the required settings.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in configuration file: {e}")
        sys.exit(1)


def read_input_file(file_path, encoding='utf-8'):
    """
    Read text content from input file.
    
    Args:
        file_path (str): Path to the input text file
        encoding (str): File encoding (default: utf-8)
        
    Returns:
        str: Text content from the file
    """
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: Input file '{file_path}' not found.")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error: Cannot decode file '{file_path}' with encoding '{encoding}': {e}")
        sys.exit(1)


def save_output_file(content, file_path, encoding='utf-8'):
    """
    Save Braille output to file.
    
    Args:
        content (str): Braille Unicode content to save
        file_path (str): Path to the output file
        encoding (str): File encoding (default: utf-8)
    """
    try:
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        print(f"✅ Braille output saved to '{file_path}'")
    except Exception as e:
        print(f"Error: Cannot save output file '{file_path}': {e}")
        sys.exit(1)


def main():
    """Main function to convert text file to Braille Unicode using configuration."""
    
    print("🔤 Braille Converter - English Text to Grade 1 Unicode Braille")
    print("=" * 65)
    
    # Load configuration
    print("📋 Loading configuration...")
    config = load_config()
    
    # Get file paths from config
    input_file = config.get('input_file', 'input_text.txt')
    output_file = config.get('output_file', 'braille_output.txt')
    encoding = config.get('encoding', 'utf-8')
    
    # Validate input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file '{input_file}' not found.")
        print(f"Please create the file or update the path in config.json")
        sys.exit(1)
    
    # Read input text
    print(f"📖 Reading input from '{input_file}'...")
    input_text = read_input_file(input_file, encoding)
    
    if not input_text.strip():
        print(f"⚠️  Warning: Input file '{input_file}' is empty.")
        sys.exit(1)
    
    # Convert to Braille Unicode
    print("🔄 Converting text to Grade 1 Braille Unicode...")
    braille_output = text_to_braille_unicode(input_text, config)
    
    # Save output
    print(f"💾 Saving Braille output to '{output_file}'...")
    save_output_file(braille_output, output_file, encoding)
    
    # Display statistics
    char_count = len(input_text)
    line_count = input_text.count('\n') + 1
    braille_char_count = len(braille_output)
    
    print("\n📊 Conversion Statistics:")
    print(f"   • Input characters: {char_count:,}")
    print(f"   • Input lines: {line_count:,}")
    print(f"   • Braille characters: {braille_char_count:,}")
    print(f"   • Input file: {input_file}")
    print(f"   • Output file: {output_file}")
    print(f"   • Encoding: {encoding}")
    
    print("\n✅ Conversion completed successfully!")
    print("🎯 The Braille output is optimized for screen readers and Braille displays.")


if __name__ == "__main__":
    main()
