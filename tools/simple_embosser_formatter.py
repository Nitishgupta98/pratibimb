#!/usr/bin/env python3
"""
Simple Braille Embosser Formatter - Clean implementation for embosser standards
"""

import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))
from braille_converter import load_config, text_to_braille_unicode

def format_for_embosser_simple(braille_text, line_length=40, page_length=25, include_page_numbers=True):
    """
    Simple, clean formatting for embosser printing.
    
    Args:
        braille_text (str): Input Braille text
        line_length (int): Characters per line (default 40)
        page_length (int): Lines per page (default 25)
        include_page_numbers (bool): Include page numbers (default True)
    
    Returns:
        str: Properly formatted Braille for embosser
    """
    
    # Braille numbers for page numbering
    braille_numbers = {
        '0': '\u281a', '1': '\u2801', '2': '\u2803', '3': '\u2809', '4': '\u2819',
        '5': '\u2811', '6': '\u280b', '7': '\u281b', '8': '\u2813', '9': '\u280a'
    }
    NUMBER_INDICATOR = '\u283c'  # ⠼
    
    def to_braille_number(num):
        return NUMBER_INDICATOR + ''.join(braille_numbers[d] for d in str(num))
    
    # Step 1: Clean and normalize text
    text = braille_text.replace('\t', '  ')  # Convert tabs to 2 spaces
    
    # Step 2: Handle paragraph breaks - split by double newlines
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    # Step 3: Word wrap each paragraph
    all_lines = []
    
    for i, paragraph in enumerate(paragraphs):
        if i > 0:  # Add blank line between paragraphs
            all_lines.append(' ' * line_length)
        
        # Word wrap within paragraph
        words = paragraph.split()
        current_line = ""
        
        for word in words:
            if not current_line:
                current_line = word
            elif len(current_line + ' ' + word) <= line_length:
                current_line += ' ' + word
            else:
                # Line is full, save it and start new line
                all_lines.append(current_line.ljust(line_length))
                current_line = word
        
        # Add the last line of paragraph
        if current_line:
            all_lines.append(current_line.ljust(line_length))
    
    # Step 4: Format into pages
    formatted_output = []
    page_num = 1
    
    i = 0
    while i < len(all_lines):
        # Start a new page
        page_lines = []
        
        # Add content lines (leaving room for page number if needed)
        content_lines_per_page = page_length - (1 if include_page_numbers else 0)
        
        for j in range(content_lines_per_page):
            if i + j < len(all_lines):
                page_lines.append(all_lines[i + j])
            else:
                page_lines.append(' ' * line_length)  # Fill with blank lines
        
        # Add page number line if enabled
        if include_page_numbers:
            page_num_line = to_braille_number(page_num).rjust(line_length)
            page_lines.append(page_num_line)
        
        # Add this page to output
        formatted_output.extend(page_lines)
        
        # Add form feed between pages (except after last page)
        i += content_lines_per_page
        if i < len(all_lines):
            formatted_output.append('\f')
        
        page_num += 1
    
    return '\n'.join(formatted_output)

def main():
    """Simple command line interface"""
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python simple_embosser_formatter.py input.txt output.brl")
        sys.exit(1)
    
    input_file, output_file = sys.argv[1], sys.argv[2]
    
    # Load configuration
    config = load_config()
    
    print(f"🖨️  Simple Braille Embosser Formatter")
    print(f"📖 Reading: {input_file}")
    
    # Read and convert
    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    braille_text = text_to_braille_unicode(text, config)
    formatted_braille = format_for_embosser_simple(braille_text)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_braille)
    
    # Statistics
    lines = formatted_braille.split('\n')
    pages = formatted_braille.count('\f') + 1
    
    print(f"💾 Saved: {output_file}")
    print(f"📊 Statistics: {len(lines)} lines, {pages} pages")
    print(f"✅ Ready for embosser!")

if __name__ == "__main__":
    main()
