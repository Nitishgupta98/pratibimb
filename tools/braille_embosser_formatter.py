#!/usr/bin/env python3
"""
Braille Embosser Formatter - Format Braille text for embosser-based printers
Ensures compliance with professional Braille printing standards
"""

import json
import os
import re
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from braille_converter import load_config, text_to_braille_unicode

def format_for_embosser(braille_text, config=None):
    """
    Format Braille text according to embosser printing standards.
    
    Standards implemented:
    - Line Length: Exactly 40 characters per line
    - Page Length: Exactly 25 lines per page
    - Page Breaks: Form feed character (\f) after every 25 lines
    - Word Wrapping: No hyphenation, wrap entire words
    - Page Numbers: Right-aligned Braille numbers on line 25
    - Paragraph Breaks: Blank lines (40 spaces) for new paragraphs
    - Tab Handling: Convert tabs to 2 spaces
    
    Args:
        braille_text (str): Input Braille text to format
        config (dict): Configuration settings
        
    Returns:
        str: Formatted Braille text ready for embosser printing
    """
    
    # Default settings if no config provided
    if config is None:
        config = {
            'embosser_settings': {
                'line_length': 40,
                'page_length': 25,
                'include_page_numbers': True,
                'tab_spaces': 2
            }
        }
    
    embosser_settings = config.get('embosser_settings', {})
    line_length = embosser_settings.get('line_length', 40)
    page_length = embosser_settings.get('page_length', 25)
    include_page_numbers = embosser_settings.get('include_page_numbers', True)
    tab_spaces = embosser_settings.get('tab_spaces', 2)
    
    # Braille number patterns for page numbering
    braille_numbers = {
        '0': '\u281a',  # ⠚ (j pattern, but represents 0 in number context)
        '1': '\u2801',  # ⠁ (a pattern)
        '2': '\u2803',  # ⠃ (b pattern)
        '3': '\u2809',  # ⠉ (c pattern)
        '4': '\u2819',  # ⠙ (d pattern)
        '5': '\u2811',  # ⠑ (e pattern)
        '6': '\u280b',  # ⠋ (f pattern)
        '7': '\u281b',  # ⠛ (g pattern)
        '8': '\u2813',  # ⠓ (h pattern)
        '9': '\u280a',  # ⠊ (i pattern)
    }
    NUMBER_INDICATOR = '\u283c'  # ⠼
    
    def convert_to_braille_number(num):
        """Convert a number to Braille representation"""
        result = NUMBER_INDICATOR  # Start with number indicator
        for digit in str(num):
            result += braille_numbers[digit]
        return result
    
    # Step 1: Handle tabs - convert to spaces
    text = braille_text.replace('\t', ' ' * tab_spaces)
    
    # Step 2: Handle paragraph breaks
    # Split by double newlines to identify paragraphs
    paragraphs = text.split('\n\n')
    processed_paragraphs = []
    
    for paragraph in paragraphs:
        if paragraph.strip():  # Non-empty paragraph
            # Remove single newlines within paragraph and normalize spaces
            para_text = re.sub(r'\n', ' ', paragraph)
            para_text = re.sub(r'\s+', ' ', para_text).strip()
            processed_paragraphs.append(para_text)
    
    # Step 3: Word wrapping with 40-character line limit
    formatted_lines = []
    
    for i, paragraph in enumerate(processed_paragraphs):
        if i > 0:  # Add blank line between paragraphs (except before first)
            formatted_lines.append(' ' * line_length)
        
        # Split paragraph into words
        words = paragraph.split()
        current_line = ""
        
        for word in words:
            # Check if adding this word would exceed line length
            test_line = current_line + (' ' if current_line else '') + word
            
            if len(test_line) <= line_length:
                current_line = test_line
            else:
                # Current line is full, start new line
                if current_line:
                    # Pad current line to exactly 40 characters
                    formatted_lines.append(current_line.ljust(line_length))
                current_line = word
        
        # Add the last line of the paragraph
        if current_line:
            formatted_lines.append(current_line.ljust(line_length))
    
    # Step 4: Add page breaks and page numbers
    final_output = []
    page_number = 1
    
    # Process lines in chunks of page_length
    for page_start in range(0, len(formatted_lines), page_length - (1 if include_page_numbers else 0)):
        page_end = min(page_start + page_length - (1 if include_page_numbers else 0), len(formatted_lines))
        page_lines = formatted_lines[page_start:page_end]
        
        # Add the content lines for this page
        final_output.extend(page_lines)
        
        # Fill remaining lines with blanks if needed
        lines_needed = page_length - (1 if include_page_numbers else 0) - len(page_lines)
        if lines_needed > 0:
            final_output.extend([' ' * line_length] * lines_needed)
        
        # Add page number if enabled
        if include_page_numbers:
            page_num_braille = convert_to_braille_number(page_number)
            page_line = page_num_braille.rjust(line_length)
            final_output.append(page_line)
        
        # Add form feed for page break (except after last page)
        # The form feed should replace the newline, not add to it
        if page_end < len(formatted_lines):
            # Instead of appending \f as a separate line, we'll handle it differently
            pass
        
        page_number += 1
    
    # Join with newlines, but insert form feeds at page boundaries
    result = []
    lines_per_page = page_length
    current_line = 0
    
    for line in final_output:
        result.append(line)
        current_line += 1
        
        # Check if we've completed a page (and it's not the last page)
        if current_line % lines_per_page == 0 and current_line < len(final_output):
            result.append('\f')  # Add form feed after complete page
    
    return '\n'.join(result)

def convert_and_format_for_embosser(input_file, output_file, config_file='config.json'):
    """
    Convert text to Braille and format for embosser printing.
    
    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output embosser-ready Braille file
        config_file (str): Configuration file path
    """
    
    # Load configuration
    config = load_config(config_file)
    
    # Add default embosser settings if not present
    if 'embosser_settings' not in config:
        config['embosser_settings'] = {
            'line_length': 40,
            'page_length': 25,
            'include_page_numbers': True,
            'tab_spaces': 2
        }
    
    try:
        print(f"🖨️  Braille Embosser Formatter")
        print("=" * 50)
        print(f"📖 Reading text from '{input_file}'...")
        
        # Read input file
        with open(input_file, 'r', encoding=config.get('encoding', 'utf-8')) as f:
            text = f.read()
        
        print(f"🔄 Converting to Grade 1 Braille...")
        
        # Convert to Braille
        braille_text = text_to_braille_unicode(text, config)
        
        print(f"📏 Formatting for embosser printing...")
        print(f"   • Line length: {config['embosser_settings']['line_length']} characters")
        print(f"   • Page length: {config['embosser_settings']['page_length']} lines")
        print(f"   • Page numbers: {'Enabled' if config['embosser_settings']['include_page_numbers'] else 'Disabled'}")
        
        # Format for embosser
        formatted_braille = format_for_embosser(braille_text, config)
        
        print(f"💾 Saving embosser-ready file to '{output_file}'...")
        
        # Write formatted output
        with open(output_file, 'w', encoding=config.get('encoding', 'utf-8')) as f:
            f.write(formatted_braille)
        
        # Calculate statistics
        lines = formatted_braille.split('\n')
        pages = formatted_braille.count('\f') + 1
        total_chars = len(formatted_braille)
        
        print(f"✅ Embosser-ready Braille saved to '{output_file}'")
        print(f"📊 Formatting Statistics:")
        print(f"   • Total characters: {total_chars:,}")
        print(f"   • Total lines: {len(lines):,}")
        print(f"   • Total pages: {pages:,}")
        print(f"   • Lines per page: {config['embosser_settings']['page_length']}")
        print(f"   • Characters per line: {config['embosser_settings']['line_length']}")
        print(f"   • Input file: {input_file}")
        print(f"   • Output file: {output_file}")
        print(f"✅ Ready for embosser printing!")
        print(f"🖨️  Send this file directly to your Braille embosser.")
        
    except FileNotFoundError:
        print(f"❌ Error: Input file '{input_file}' not found!")
    except Exception as e:
        print(f"❌ Error during formatting: {str(e)}")

def main():
    """Main function for command-line usage"""
    import sys
    
    if len(sys.argv) < 3:
        print("Braille Embosser Formatter")
        print("=" * 30)
        print("Usage: python braille_embosser_formatter.py <input_file> <output_file> [config_file]")
        print("")
        print("Examples:")
        print("  python braille_embosser_formatter.py input.txt embosser_output.brl")
        print("  python braille_embosser_formatter.py document.txt print_ready.brl custom_config.json")
        print("")
        print("Output Format:")
        print("  • 40 characters per line")
        print("  • 25 lines per page")
        print("  • Form feed (\\f) page breaks")
        print("  • Right-aligned page numbers")
        print("  • Grade 1 Braille (no contractions)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    config_file = sys.argv[3] if len(sys.argv) > 3 else 'config.json'
    
    convert_and_format_for_embosser(input_file, output_file, config_file)

if __name__ == "__main__":
    main()
