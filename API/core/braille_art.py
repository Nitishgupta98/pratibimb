import json
import re
import logging
from typing import Dict, List, Optional
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import google.generativeai as genai
from typing import List
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Constants
MAX_RETRIES = 2
BATCH_SIZE = 4
MAX_LINE_WIDTH = 40
INPUT_JSON_PATH = "output/relevant_visual_objects.json"
ASCII_OUTPUT_PATH = "output/braille_art_ascii.txt"
BRAILLE_OUTPUT_PATH = "output/braille_art_unicode.txt"


# Initialize Gemini from .env
load_dotenv()  # This loads variables from .env into the environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env file")
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-pro")

def call_gemini_api(prompt: str) -> Optional[str]:
    for attempt in range(MAX_RETRIES):
        try:
            #print(prompt)
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            logging.warning(f"Gemini SDK call failed (attempt {attempt + 1}): {e}")
            time.sleep(2)
    return None

def is_valid_braille_char(char: str) -> bool:
    return '\u2800' <= char <= '\u28FF'

def validate_art_block(ascii_art: str, braille_art: str) -> bool:
    for line in ascii_art.splitlines():
        if len(line) > MAX_LINE_WIDTH:
            return False
    for line in braille_art.splitlines():
        if len(line) > MAX_LINE_WIDTH:
            return False
        if not all(is_valid_braille_char(c) or c.isspace() for c in line):
            return False
    return True

def chunk_list(data: List[Dict], size: int) -> List[List[Dict]]:
    return [data[i:i + size] for i in range(0, len(data), size)]

def extract_json_blocks(text: str) -> List[Dict]:
    """
    Parses the plain text Gemini response (not JSON) and extracts blocks for each object.
    Returns a list of dicts with keys: id, ascii_art.
    """
    try:
        # Split by '---' separator
        blocks = [b.strip() for b in text.split('---') if b.strip()]
        results = []
        for block in blocks:
            lines = block.splitlines()
            obj = {"id": None, "ascii_art": ""}
            current_section = None
            for line in lines:
                line = line.strip()
                if line.startswith("ID:"):
                    obj["id"] = line[3:].strip()
                elif line.startswith("ASCII ART:"):
                    current_section = "ascii_art"
                elif line.startswith("BRAILLE ART:"):
                    current_section = None  # Ignore braille section
                elif line.startswith("OBJECT:") or line.startswith("DESCRIPTION:"):
                    continue  # skip object name/description
                elif current_section == "ascii_art" and line:
                    obj["ascii_art"] += (line + "\n")
            # Remove trailing newlines
            obj["ascii_art"] = obj["ascii_art"].rstrip()
            if obj["id"]:
                results.append(obj)
        return results
    except Exception as e:
        logging.error(f"Failed to parse Gemini response as plain text blocks: {e}")
        with open("gemini_raw_response.txt", "w", encoding="utf-8") as f:
            f.write(text)
        return []

def generate_prompt(batch: List[Dict]) -> str:
    # Plain text, line-based prompt for ASCII art only, includes description
    lines = [
    "You are an AI assistant specialized in generating tactile-friendly ASCII diagrams optimized for conversion into Braille art for visually impaired users.",
    "",
    "For each requested object:",
    "- Output must start with: ID: Fig_X",
    "- Then write ASCII ART: followed by a clean ASCII diagram.",
    "- Use ONLY these characters to indicate raised parts: '@', '#', 'O', 'X'.",
    "- Use spaces for empty parts.",
    "- ASCII diagrams must be blocky, tactile-friendly, and follow the 2x4 Braille dot layout.",
    "- Avoid text labels, thin lines, or decorative shading.",
    "- ASCII width must NOT exceed 40 characters.",
    "- Do not return anything except in this strict format:",
    "",
    "ID: Fig_1",
    "ASCII ART:",
    "<ascii art block>",
    "---",
    "",
    "Repeat the format for each object."
]

    for obj in batch:
        lines.append(f"ID: {obj['id']}")
        lines.append(f"OBJECT: {obj['object']}")
        lines.append(f"DESCRIPTION: {obj.get('description','')}")
        lines.append("ASCII ART:")
        lines.append("[fill here]")
        lines.append("---")
    return '\n'.join(lines)


def generate_ascii_art_blocks(input_objects: List[Dict]) -> Dict[str, Dict[str, str]]:
    results = {}
    total_batches = (len(input_objects) + BATCH_SIZE - 1) // BATCH_SIZE
    logging.info(f"Starting ASCII art generation: {len(input_objects)} objects, {total_batches} batches, batch size {BATCH_SIZE}.")
    batches = list(chunk_list(input_objects, BATCH_SIZE))
    batch_outputs = [None] * len(batches)

    def process_batch(batch_idx, batch):
        logging.info(f"Processing batch {batch_idx+1}/{total_batches} (objects {batch_idx*BATCH_SIZE+1}-{batch_idx*BATCH_SIZE+len(batch)})...")
        prompt = generate_prompt(batch)
        time.sleep(batch_idx)  # Stagger API calls by 1 second per batch
        response = call_gemini_api(prompt)
        if not response:
            logging.error(f"Gemini API failed. Skipping batch {batch_idx+1}.")
            return (batch_idx, [])
        blocks = extract_json_blocks(response)
        logging.info(f"Batch {batch_idx+1}: Received {len(blocks)} blocks from Gemini.")
        batch_result = []
        for block in blocks:
            obj_id = block.get("id")
            ascii_art = block.get("ascii_art", "").strip()
            if not obj_id or not ascii_art:
                logging.warning(f"Batch {batch_idx+1}: Incomplete result for ID {obj_id}.")
                continue
            if all(len(line) <= MAX_LINE_WIDTH for line in ascii_art.splitlines()):
                batch_result.append((obj_id, ascii_art))
                logging.info(f"Batch {batch_idx+1}: ASCII art generated for ID {obj_id}.")
            else:
                logging.warning(f"Batch {batch_idx+1}: Invalid ASCII art format for ID {obj_id}. Skipping.")
        return (batch_idx, batch_result)

    with ThreadPoolExecutor(max_workers=min(8, total_batches)) as executor:
        futures = [executor.submit(process_batch, idx, batch) for idx, batch in enumerate(batches)]
        for future in as_completed(futures):
            batch_idx, batch_result = future.result()
            batch_outputs[batch_idx] = batch_result

    # Merge results in order
    for batch_result in batch_outputs:
        if batch_result:
            for obj_id, ascii_art in batch_result:
                results[obj_id] = {"ascii_art": ascii_art}
    logging.info(f"ASCII art generation complete. {len(results)} objects processed successfully.")
    return results

# --- Utility to save ASCII art to file ---
def save_ascii_art_file(ascii_blocks, output_file):
    output_path = output_file if output_file.startswith("output/") else f"output/{output_file}"
    with open(output_path, "w", encoding="utf-8") as f:
        for obj_id, arts in ascii_blocks.items():
            f.write(f"=== {obj_id} ===\n")
            f.write("ASCII ART:\n")
            f.write(arts["ascii_art"] + "\n\n")

RAISED_CHARS = set('#@OXo+*█▓■●◉+=|/\\()[]{}')

def ascii_block_to_braille(block: List[str]) -> str:
    dot_map = [(0,0), (1,0), (2,0), (0,1), (1,1), (2,1), (3,0), (3,1)]
    code = 0x2800
    for idx, (row, col) in enumerate(dot_map):
        try:
            if block[row][col] in RAISED_CHARS:
                code |= (1 << idx)
        except IndexError:
            pass
    return chr(code)

def preprocess_ascii_line(line: str) -> str:
    return line.rstrip()

def ascii_art_to_braille(ascii_art: str) -> str:
    lines = ascii_art.splitlines()
    if not lines:
        return ''
    
    lines = [preprocess_ascii_line(line) for line in lines]
    
    while len(lines) % 4 != 0:
        lines.append(' ' * len(lines[0]))
    
    max_width = max(len(line) for line in lines)
    if max_width % 2 != 0:
        max_width += 1
    
    lines = [line.ljust(max_width) for line in lines]
    
    braille_lines = []
    for row in range(0, len(lines), 4):
        braille_line = ''
        for col in range(0, max_width, 2):
            block = [lines[row + r][col:col + 2] for r in range(4)]
            braille_line += ascii_block_to_braille(block)
        braille_lines.append(braille_line.rstrip())
    
    return '\n'.join(braille_lines)

# --- Utility to save Braille art to file ---
def save_braille_art_file(ascii_blocks, output_file):
    output_path = output_file if output_file.startswith("output/") else f"output/{output_file}"
    with open(output_path, "w", encoding="utf-8") as f:
        for obj_id, arts in ascii_blocks.items():
            f.write(f"=== {obj_id} ===\n")
            f.write("BRAILLE ART:\n")
            braille_art = ascii_art_to_braille(arts["ascii_art"])
            f.write(braille_art + "\n\n")

def load_braille_art_blocks(braille_art_file):
    """Load Braille art blocks from braille_art_unicode.txt into a dict."""
    art_blocks = {}
    current_id = None
    current_art = []
    with open(braille_art_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.startswith('=== Fig_'):
                if current_id and current_art:
                    art_blocks[current_id] = '\n'.join(current_art).strip()
                current_id = re.search(r'Fig_\d+', line).group(0)
                current_art = []
            elif line.startswith('BRAILLE ART:'):
                continue
            elif line.strip() == '':
                continue
            elif current_id:
                current_art.append(line)
        # Add last block
        if current_id and current_art:
            art_blocks[current_id] = '\n'.join(current_art).strip()
    return art_blocks

def load_braille_art_blocks_from_content(braille_art_content):
    """Load Braille art blocks from braille art content string into a dict."""
    art_blocks = {}
    current_id = None
    current_art = []
    
    for line in braille_art_content.split('\n'):
        line = line.rstrip('\n')
        if line.startswith('=== Fig_'):
            # Save previous block
            if current_id and current_art:
                art_blocks[current_id] = '\n'.join(current_art).strip()
            # Start new block
            current_id = re.search(r'Fig_\d+', line).group(0)
            current_art = []
        elif line.startswith('BRAILLE ART:'):
            continue
        elif line.strip() == '':
            continue
        elif current_id:
            current_art.append(line)
    
    # Add last block
    if current_id and current_art:
        art_blocks[current_id] = '\n'.join(current_art).strip()
    return art_blocks

def text_to_braille_unicode(text):
    """Convert English text to Grade 1 Unicode Braille (matches pratibimb.py exactly)."""
    # Grade 1 Braille mapping (Unicode U+2800-U+28FF) - EXACT COPY from pratibimb.py
    braille_map = {
        'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛', 'h': '⠓',
        'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝', 'o': '⠕', 'p': '⠏',
        'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥', 'v': '⠧', 'w': '⠺', 'x': '⠭',
        'y': '⠽', 'z': '⠵',
        
        # Numbers (with number indicator ⠼)
        '1': '⠁', '2': '⠃', '3': '⠉', '4': '⠙', '5': '⠑',
        '6': '⠋', '7': '⠛', '8': '⠓', '9': '⠊', '0': '⠚',
        
        # Punctuation - CORRECTED to match pratibimb.py
        '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆', ':': '⠒',
        '-': '⠤', '(': '⠐⠣', ')': '⠐⠜', '"': '⠐⠦', "'": '⠄',
        '/': '⠸⠌', '*': '⠸⠔', '+': '⠸⠖', '=': '⠸⠿',
        
        # Special characters
        ' ': ' ',  # Regular space
        '\t': '  ',  # Tab to 2 spaces (default)
    }
    
    result = []
    i = 0
    in_number_sequence = False
    
    while i < len(text):
        char = text[i]
        
        # Skip carriage returns
        if char == '\r':
            i += 1
            continue
        
        if char == '\n':
            result.append('\n')
            in_number_sequence = False
        elif char.isupper():
            # Capital letter indicator + lowercase letter
            result.append('⠠')  # Capital indicator
            result.append(braille_map.get(char.lower(), char))
        elif char.isdigit():
            if not in_number_sequence:
                # Add number indicator for first digit in sequence
                result.append('⠼')
                in_number_sequence = True
            result.append(braille_map.get(char, char))
        elif char in braille_map:
            result.append(braille_map[char])
            if char != ' ':  # Space doesn't end number sequence
                in_number_sequence = False
        else:
            # Unknown character - preserve as is (following pratibimb.py behavior)
            result.append(char)
            in_number_sequence = False
        
        i += 1
    
    return ''.join(result)

def format_braille_for_embosser(braille_text, line_length=40, page_length=25):
    """Format Braille text for embosser: 40 chars/line, 25 lines/page, form feed after each page."""
    # Split into lines
    lines = []
    for paragraph in braille_text.split('\n'):
        while paragraph:
            lines.append(paragraph[:line_length])
            paragraph = paragraph[line_length:]
    # Group into pages
    pages = []
    for i in range(0, len(lines), page_length):
        pages.append('\n'.join(lines[i:i+page_length]))
    # Join with form feed
    return '\f'.join(pages)

def convert_transcript_to_braille_with_art_from_content(transcript_content: str, braille_art_content: str) -> str:
    """
    Convert transcript content to Braille, substituting [Fig_x: ...] tags with Braille art.
    
    Args:
        transcript_content (str): The transcript content with figure tags
        braille_art_content (str): The braille art content
        
    Returns:
        str: The formatted Braille output ready for embosser
    """
    if not transcript_content or not braille_art_content:
        logging.error("Transcript content or braille art content is empty")
        return ""

    # Load Braille art blocks from content
    art_blocks = load_braille_art_blocks_from_content(braille_art_content)
    
    transcript = transcript_content

    # --- Optional: Table of Figures ---
    fig_tags = re.findall(r'\[(Fig_\d+):([^\]]+)\]', transcript)
    table_of_figures = ""
    if fig_tags:
        table_of_figures += text_to_braille_unicode("Table of Figures:") + "\n\n"
        for fig_id, caption in fig_tags:
            table_of_figures += text_to_braille_unicode(f"{fig_id}: {caption}") + "\n"
        table_of_figures += "\n"

    # Replace [Fig_x: caption] tags with explicit Braille art placeholders
    def fig_replacer(match):
        fig_id = match.group(1)
        label = match.group(2).strip()
        art = art_blocks.get(fig_id)
        braille_label = text_to_braille_unicode(label)
        # Always add blank line before and after
        if art:
            return f"\n<<BRAILLE_ART_START:{fig_id}>>\n{braille_label}\n{art}\n<<BRAILLE_ART_END>>\n"
        else:
            return f"\n<<BRAILLE_ART_START:{fig_id}>>\n{braille_label}\n[Missing Braille Art: {fig_id}]\n<<BRAILLE_ART_END>>\n"
    transcript_with_art = re.sub(r'\[(Fig_\d+):([^\]]+)\]', fig_replacer, transcript)

    # Split transcript into segments: text and Braille art blocks
    segments = []
    pattern = r'(<<BRAILLE_ART_START:[^>]+>>.*?<<BRAILLE_ART_END>>\n?)'
    last_end = 0
    for m in re.finditer(pattern, transcript_with_art, re.DOTALL):
        start, end = m.span()
        if start > last_end:
            segments.append(('text', transcript_with_art[last_end:start]))
        segments.append(('art', transcript_with_art[start:end]))
        last_end = end
    if last_end < len(transcript_with_art):
        segments.append(('text', transcript_with_art[last_end:]))

    # --- Improved Braille text wrapping ---
    def braille_word_wrap(text, line_length=40):
        # Convert to Braille first
        braille = text_to_braille_unicode(text)
        # Split into words, but keep modifiers attached
        words = []
        i = 0
        while i < len(braille):
            # If modifier, attach to next char
            if braille[i] in ['⠠', '⠼'] and i+1 < len(braille):
                words.append(braille[i:i+2])
                i += 2
            else:
                # Find next space
                j = i
                while j < len(braille) and braille[j] != ' ':
                    j += 1
                words.append(braille[i:j])
                i = j+1 if j < len(braille) else j
        # Now wrap
        lines = []
        current = ""
        for word in words:
            if not word:
                continue
            if len(current) + len(word) + (1 if current else 0) <= line_length:
                if current:
                    current += ' ' + word
                else:
                    current = word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    # --- Improved Braille art block handling ---
    def process_art_block(block):
        # Remove markers, ensure blank lines before/after
        block = block.strip()
        block = re.sub(r'^<<BRAILLE_ART_START:[^>]+>>\n?', '', block)
        block = re.sub(r'<<BRAILLE_ART_END>>\n?$', '', block)
        # Ensure only Braille Unicode, whitespace, and \f
        block = ''.join(c for c in block if c == '\f' or c.isspace() or ('\u2800' <= c <= '\u28FF'))
        return [''] + block.splitlines() + ['']

    # --- Compose final output ---
    all_lines = []
    # Insert Table of Figures if present
    if table_of_figures:
        all_lines.extend(braille_word_wrap(table_of_figures))
        all_lines.append('')
    for typ, seg in segments:
        if typ == 'text':
            all_lines.extend(braille_word_wrap(seg))
        else:
            all_lines.extend(process_art_block(seg))

    # --- Page formatting ---
    def page_format(lines, line_length=40, page_length=25):
        # Pad/truncate lines
        out_lines = []
        for line in lines:
            # Only Braille Unicode, whitespace, and \f
            clean = ''.join(c for c in line if c == '\f' or c.isspace() or ('\u2800' <= c <= '\u28FF'))
            out_lines.append(clean.ljust(line_length)[:line_length])
        # Group into pages
        pages = []
        for i in range(0, len(out_lines), page_length):
            pages.append('\n'.join(out_lines[i:i+page_length]))
        return '\f'.join(pages)

    formatted_braille = page_format(all_lines)
    return formatted_braille

def convert_transcript_to_braille_with_art(transcript_path, braille_art_path, output_path):
    """File-based wrapper for convert_transcript_to_braille_with_art_from_content"""
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        with open(braille_art_path, 'r', encoding='utf-8') as f:
            braille_art_content = f.read()
    except Exception as e:
        logging.error(f"Could not read input files: {e}")
        return
    
    result = convert_transcript_to_braille_with_art_from_content(transcript_content, braille_art_content)
    
    if result:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ Final Braille transcript saved to {output_path}")
        except Exception as e:
            logging.error(f"Could not write output file {output_path}: {e}")

# Example usage:
# convert_transcript_to_braille_with_art(
#     transcript_path='output/transcript_with_figure_tags.txt',
#     braille_art_path='output/braille_art_unicode.txt',
#     output_path='output/final_braille_transcript.txt'
# )


# =========================
# Kannada Braille Mapping and Pipeline (FULL)
# =========================
kannada_braille_map = {
    # Vowels
    'ಅ': '⠁', 'ಆ': '⠜', 'ಇ': '⠊', 'ಈ': '⠔', 'ಉ': '⠥', 'ಊ': '⠳',
    'ಎ': '⠑', 'ಏ': '⠌', 'ಐ': '⠕', 'ಒ': '⠪', 'ಓ': '⠙', 'ಔ': '⠚',
    
    # Consonants
    'ಕ': '⠅', 'ಖ': '⠨', 'ಗ': '⠛', 'ಘ': '⠣', 'ಙ': '⠬',
    'ಚ': '⠉', 'ಛ': '⠡', 'ಜ': '⠚', 'ಝ': '⠴', 'ಞ': '⠒',
    'ಟ': '⠾', 'ಠ': '⠺', 'ಡ': '⠫', 'ಢ': '⠿', 'ಣ': '⠼',
    'ತ': '⠞', 'ಥ': '⠹', 'ದ': '⠙', 'ಧ': '⠮', 'ನ': '⠝',
    'ಪ': '⠏', 'ಫ': '⠖', 'ಬ': '⠃', 'ಭ': '⠘', 'ಮ': '⠍',
    'ಯ': '⠽', 'ರ': '⠗', 'ಲ': '⠇', 'ಳ': '⠸', 'ವ': '⠧',
    'ಶ': '⠩', 'ಷ': '⠯', 'ಸ': '⠎', 'ಹ': '⠓',
    
    # Special signs (FIXED - using proper Braille characters)
    '್': '⠈',     # Halant (virama) - using dot 4
    'ಂ': '⠰',     # Anusvara - using dots 5-6
    'ಃ': '⠠⠒',   # Visarga - using capital + colon
    
    # Punctuation (basic)
    '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆', ':': '⠒',
    
    # Numerals (Kannada digits)
    '೦': '⠴', '೧': '⠂', '೨': '⠆', '೩': '⠒', '೪': '⠲', '೫': '⠢', 
    '೬': '⠖', '೭': '⠶', '೮': '⠦', '೯': '⠔',
    
    # Whitespace
    ' ': ' ', '\n': '\n'
}

def text_to_braille_unicode_kannada(text):
    result = []
    for char in text:
        result.append(kannada_braille_map.get(char, '⍰'))
    return ''.join(result)

def convert_transcript_to_braille_with_art_kannada(transcript_path, braille_art_path, output_path):
    """File-based wrapper for convert_transcript_to_braille_with_art_kannada_from_content"""
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        with open(braille_art_path, 'r', encoding='utf-8') as f:
            braille_art_content = f.read()
    except Exception as e:
        logging.error(f"Could not read input files: {e}")
        return
    
    result = convert_transcript_to_braille_with_art_kannada_from_content(transcript_content, braille_art_content)
    
    if result:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ Kannada Braille transcript saved to {output_path}")
        except Exception as e:
            logging.error(f"Could not write output file {output_path}: {e}")

def convert_transcript_to_braille_with_art_kannada_from_content(transcript_content: str, braille_art_content: str) -> str:
    """
    Convert Kannada transcript content to Braille, substituting [Fig_x: ...] tags with Braille art.
    
    Args:
        transcript_content (str): The Kannada transcript content with figure tags
        braille_art_content (str): The braille art content
        
    Returns:
        str: The formatted Braille output ready for embosser
    """
    if not transcript_content or not braille_art_content:
        logging.error("Transcript content or braille art content is empty")
        return ""

    if transcript_content.strip().startswith('[Translation failed'):
        logging.error("Kannada transcript not available or translation failed")
        return ""

    # Load Braille art blocks from content
    art_blocks = load_braille_art_blocks_from_content(braille_art_content)
    
    transcript = transcript_content

    fig_tags = re.findall(r'\[(Fig_\d+):([^\]]+)\]', transcript)
    table_of_figures = ""
    if fig_tags:
        table_of_figures += text_to_braille_unicode_kannada("Table of Figures:") + "\n\n"
        for fig_id, caption in fig_tags:
            table_of_figures += text_to_braille_unicode_kannada(f"{fig_id}: {caption}") + "\n"
        table_of_figures += "\n"

    def fig_replacer(match):
        fig_id = match.group(1)
        label = match.group(2).strip()
        art = art_blocks.get(fig_id)
        braille_label = text_to_braille_unicode_kannada(label)
        if art:
            return f"\n<<BRAILLE_ART_START:{fig_id}>>\n{braille_label}\n{art}\n<<BRAILLE_ART_END>>\n"
        else:
            return f"\n<<BRAILLE_ART_START:{fig_id}>>\n{braille_label}\n[Missing Braille Art: {fig_id}]\n<<BRAILLE_ART_END>>\n"
    transcript_with_art = re.sub(r'\[(Fig_\d+):([^\]]+)\]', fig_replacer, transcript)

    segments = []
    pattern = r'(<<BRAILLE_ART_START:[^>]+>>.*?<<BRAILLE_ART_END>>\n?)'
    last_end = 0
    for m in re.finditer(pattern, transcript_with_art, re.DOTALL):
        start, end = m.span()
        if start > last_end:
            segments.append(('text', transcript_with_art[last_end:start]))
        segments.append(('art', transcript_with_art[start:end]))
        last_end = end
    if last_end < len(transcript_with_art):
        segments.append(('text', transcript_with_art[last_end:]))

    def braille_word_wrap(text, line_length=40):
        braille = text_to_braille_unicode_kannada(text)
        words = braille.split(' ')
        lines = []
        current = ''
        for word in words:
            if not word:
                continue
            if len(current) + len(word) + (1 if current else 0) <= line_length:
                if current:
                    current += ' ' + word
                else:
                    current = word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def process_art_block(block):
        block = block.strip()
        block = re.sub(r'^<<BRAILLE_ART_START:[^>]+>>\n?', '', block)
        block = re.sub(r'<<BRAILLE_ART_END>>\n?$', '', block)
        block = ''.join(c for c in block if c == '\f' or c.isspace() or ('\u2800' <= c <= '\u28FF'))
        return [''] + block.splitlines() + ['']

    all_lines = []
    if table_of_figures:
        all_lines.extend(braille_word_wrap(table_of_figures))
        all_lines.append('')
    for typ, seg in segments:
        if typ == 'text':
            all_lines.extend(braille_word_wrap(seg))
        else:
            all_lines.extend(process_art_block(seg))

    def page_format(lines, line_length=40, page_length=25):
        out_lines = []
        for line in lines:
            clean = ''.join(c for c in line if c == '\f' or c.isspace() or ('\u2800' <= c <= '\u28FF'))
            out_lines.append(clean.ljust(line_length)[:line_length])
        pages = []
        for i in range(0, len(out_lines), page_length):
            pages.append('\n'.join(out_lines[i:i+page_length]))
        return '\f'.join(pages)

    formatted_braille = page_format(all_lines)
    return formatted_braille

# =========================
# Telugu Braille Mapping and Pipeline (FULL)
# =========================
telugu_braille_map = {
    # Vowels
    'అ': '⠁', 'ఆ': '⠜', 'ఇ': '⠊', 'ఈ': '⠔', 'ఉ': '⠥', 'ఊ': '⠳',
    'ఎ': '⠑', 'ఏ': '⠌', 'ఐ': '⠕', 'ఒ': '⠪', 'ఓ': '⠙', 'ఔ': '⠚',
    
    # Consonants
    'క': '⠅', 'ఖ': '⠨', 'గ': '⠛', 'ఘ': '⠣', 'ఙ': '⠬',
    'చ': '⠉', 'ఛ': '⠡', 'జ': '⠚', 'ఝ': '⠴', 'ఞ': '⠒',
    'ట': '⠾', 'ఠ': '⠺', 'డ': '⠫', 'ఢ': '⠿', 'ణ': '⠼',
    'త': '⠞', 'థ': '⠹', 'ద': '⠙', 'ధ': '⠮', 'న': '⠝',
    'ప': '⠏', 'ఫ': '⠖', 'బ': '⠃', 'భ': '⠘', 'మ': '⠍',
    'య': '⠽', 'ర': '⠗', 'ల': '⠇', 'ళ': '⠸', 'వ': '⠧',
    'శ': '⠩', 'ష': '⠯', 'స': '⠎', 'హ': '⠓',
    
    # Special signs (FIXED - using proper Braille characters)
    '్': '⠈',     # Halant (virama) - using dot 4
    'ం': '⠰',     # Anusvara - using dots 5-6  
    'ః': '⠠⠒',   # Visarga - using capital + colon
    
    # Punctuation (basic)
    '.': '⠲', ',': '⠂', '?': '⠦', '!': '⠖', ';': '⠆', ':': '⠒',
    
    # Numerals (Telugu digits)
    '౦': '⠴', '౧': '⠂', '౨': '⠆', '౩': '⠒', '౪': '⠲', '౫': '⠢', 
    '౬': '⠖', '౭': '⠶', '౮': '⠦', '౯': '⠔',
    
    # Whitespace
    ' ': ' ', '\n': '\n'
}

def text_to_braille_unicode_telugu(text):
    result = []
    for char in text:
        result.append(telugu_braille_map.get(char, '⍰'))
    return ''.join(result)

def convert_transcript_to_braille_with_art_telugu(transcript_path, braille_art_path, output_path):
    """File-based wrapper for convert_transcript_to_braille_with_art_telugu_from_content"""
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        with open(braille_art_path, 'r', encoding='utf-8') as f:
            braille_art_content = f.read()
    except Exception as e:
        logging.error(f"Could not read input files: {e}")
        return
    
    result = convert_transcript_to_braille_with_art_telugu_from_content(transcript_content, braille_art_content)
    
    if result:
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ Telugu Braille transcript saved to {output_path}")
        except Exception as e:
            logging.error(f"Could not write output file {output_path}: {e}")

def convert_transcript_to_braille_with_art_telugu_from_content(transcript_content: str, braille_art_content: str) -> str:
    """
    Convert Telugu transcript content to Braille, substituting [Fig_x: ...] tags with Braille art.
    
    Args:
        transcript_content (str): The Telugu transcript content with figure tags
        braille_art_content (str): The braille art content
        
    Returns:
        str: The formatted Braille output ready for embosser
    """
    if not transcript_content or not braille_art_content:
        logging.error("Transcript content or braille art content is empty")
        return ""

    if transcript_content.strip().startswith('[Translation failed'):
        logging.error("Telugu transcript not available or translation failed")
        return ""

    # Load Braille art blocks from content
    art_blocks = load_braille_art_blocks_from_content(braille_art_content)
    
    transcript = transcript_content

    fig_tags = re.findall(r'\[(Fig_\d+):([^\]]+)\]', transcript)
    table_of_figures = ""
    if fig_tags:
        table_of_figures += text_to_braille_unicode_telugu("Table of Figures:") + "\n\n"
        for fig_id, caption in fig_tags:
            table_of_figures += text_to_braille_unicode_telugu(f"{fig_id}: {caption}") + "\n"
        table_of_figures += "\n"

    def fig_replacer(match):
        fig_id = match.group(1)
        label = match.group(2).strip()
        art = art_blocks.get(fig_id)
        braille_label = text_to_braille_unicode_telugu(label)
        if art:
            return f"\n<<BRAILLE_ART_START:{fig_id}>>\n{braille_label}\n{art}\n<<BRAILLE_ART_END>>\n"
        else:
            return f"\n<<BRAILLE_ART_START:{fig_id}>>\n{braille_label}\n[Missing Braille Art: {fig_id}]\n<<BRAILLE_ART_END>>\n"
    transcript_with_art = re.sub(r'\[(Fig_\d+):([^\]]+)\]', fig_replacer, transcript)

    segments = []
    pattern = r'(<<BRAILLE_ART_START:[^>]+>>.*?<<BRAILLE_ART_END>>\n?)'
    last_end = 0
    for m in re.finditer(pattern, transcript_with_art, re.DOTALL):
        start, end = m.span()
        if start > last_end:
            segments.append(('text', transcript_with_art[last_end:start]))
        segments.append(('art', transcript_with_art[start:end]))
        last_end = end
    if last_end < len(transcript_with_art):
        segments.append(('text', transcript_with_art[last_end:]))

    def braille_word_wrap(text, line_length=40):
        braille = text_to_braille_unicode_telugu(text)
        words = braille.split(' ')
        lines = []
        current = ''
        for word in words:
            if not word:
                continue
            if len(current) + len(word) + (1 if current else 0) <= line_length:
                if current:
                    current += ' ' + word
                else:
                    current = word
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def process_art_block(block):
        block = block.strip()
        block = re.sub(r'^<<BRAILLE_ART_START:[^>]+>>\n?', '', block)
        block = re.sub(r'<<BRAILLE_ART_END>>\n?$', '', block)
        block = ''.join(c for c in block if c == '\f' or c.isspace() or ('\u2800' <= c <= '\u28FF'))
        return [''] + block.splitlines() + ['']

    all_lines = []
    if table_of_figures:
        all_lines.extend(braille_word_wrap(table_of_figures))
        all_lines.append('')
    for typ, seg in segments:
        if typ == 'text':
            all_lines.extend(braille_word_wrap(seg))
        else:
            all_lines.extend(process_art_block(seg))

    def page_format(lines, line_length=40, page_length=25):
        out_lines = []
        for line in lines:
            clean = ''.join(c for c in line if c == '\f' or c.isspace() or ('\u2800' <= c <= '\u28FF'))
            out_lines.append(clean.ljust(line_length)[:line_length])
        pages = []
        for i in range(0, len(out_lines), page_length):
            pages.append('\n'.join(out_lines[i:i+page_length]))
        return '\f'.join(pages)

    formatted_braille = page_format(all_lines)
    return formatted_braille

# --- BRF Format Generation ---
def unicode_to_ascii_braille(unicode_braille_text):
    """
    Convert Unicode Braille patterns to BRF (Braille Ready Format) ASCII encoding.
    
    This function implements the exact BRF standard mapping where each Unicode
    Braille character maps to a specific ASCII character. Any unmapped Unicode
    Braille characters are converted to ASCII spaces.
    
    BRF Standard Mapping (Unicode → ASCII):
    - Letters: ⠁→a, ⠃→b, ⠉→c, etc.
    - Punctuation: ⠂→, (comma), ⠲→. (period), ⠦→? (question), etc.
    - Indicators: ⠠→' ' (capital), ⠼→# (number)
    - Control chars: \f and \n preserved as-is
    - Unknown chars: converted to space
    """
    
    # BRF Unicode to ASCII mapping table (exact specification)
    braille_to_ascii = {
        # Letters (a-z)
        '⠁': 'a',  # U+2801 - Dot 1
        '⠃': 'b',  # U+2803 - Dots 1-2
        '⠉': 'c',  # U+2809 - Dots 1-4
        '⠙': 'd',  # U+2819 - Dots 1-4-5
        '⠑': 'e',  # U+2811 - Dots 1-5
        '⠋': 'f',  # U+280B - Dots 1-2-4
        '⠛': 'g',  # U+281B - Dots 1-2-4-5
        '⠓': 'h',  # U+2813 - Dots 1-2-5
        '⠊': 'i',  # U+280A - Dots 2-4
        '⠚': 'j',  # U+281A - Dots 2-4-5
        '⠅': 'k',  # U+2805 - Dots 1-3
        '⠇': 'l',  # U+2807 - Dots 1-2-3
        '⠍': 'm',  # U+280D - Dots 1-3-4
        '⠝': 'n',  # U+281D - Dots 1-3-4-5
        '⠕': 'o',  # U+2815 - Dots 1-3-5
        '⠏': 'p',  # U+280F - Dots 1-2-3-4
        '⠟': 'q',  # U+281F - Dots 1-2-3-4-5
        '⠗': 'r',  # U+2817 - Dots 1-2-3-5
        '⠎': 's',  # U+280E - Dots 2-3-4
        '⠞': 't',  # U+281E - Dots 2-3-4-5
        '⠥': 'u',  # U+2825 - Dots 1-3-6
        '⠧': 'v',  # U+2827 - Dots 1-2-3-6
        '⠺': 'w',  # U+283A - Dots 2-4-5-6
        '⠭': 'x',  # U+282D - Dots 1-3-4-6
        '⠽': 'y',  # U+283D - Dots 1-3-4-5-6
        '⠵': 'z',  # U+2835 - Dots 1-3-5-6
        
        # Special indicators (CORRECTED)
        '⠠': ' ',  # U+2820 - Capital Sign (Dot 6) -> SPACE per BRF spec
        '⠼': '#',  # U+283C - Number Sign (Dots 3-4-5-6)
        
        # Punctuation
        '⠂': ',',  # U+2802 - Comma (Dot 2)
        '⠲': '.',  # U+2832 - Period (Dots 2-5-6)
        '⠦': '?',  # U+2826 - Question Mark (Dots 2-3-6)
        '⠖': '!',  # U+2816 - Exclamation Mark (Dots 2-3-5)
        '⠄': "'",  # U+2804 - Apostrophe (Dot 3)
        '⠤': '-',  # U+2824 - Hyphen/Dash (Dots 3-6)
        
        # Additional common punctuation
        '⠆': ';',  # U+2806 - Semicolon
        '⠒': ':',  # U+2812 - Colon
        
        # Blank Braille cell
        '⠀': ' ',  # U+2800 - Blank cell (space)
    }
    
    result = []
    
    for char in unicode_braille_text:
        if char in braille_to_ascii:
            # Convert using BRF mapping
            result.append(braille_to_ascii[char])
        elif char in ['\f', '\n']:
            # Preserve control characters as-is
            result.append(char)
        elif char == ' ':
            # Regular space remains space
            result.append(' ')
        elif '⠀' <= char <= '⣿':
            # Unknown Unicode Braille character - convert to space
            result.append(' ')
        else:
            # Non-Braille character - convert to space per BRF spec
            result.append(' ')
    
    return ''.join(result)

def format_for_embosser(braille_text, config=None):
    """
    Format Unicode Braille text for professional embosser output.
    
    This function formats Braille text according to international standards:
    - 40 characters per line (configurable)
    - 25 lines per page (configurable)  
    - Form feed (\\f) character between pages
    - Proper line padding and page structure
    - Compatible with all major embosser brands
    
    Args:
        braille_text (str): Unicode Braille text to format
        config (dict, optional): Configuration settings
            - line_length: Characters per line (default: 40)
            - page_length: Lines per page (default: 25)
            - pad_lines: Whether to pad lines to exact length (default: True)
    
    Returns:
        str: Properly formatted Braille text ready for embosser
    """
    if config is None:
        config = {}
    
    embosser_settings = config.get('embosser_settings', {})
    line_length = embosser_settings.get('line_length', 40)
    page_length = embosser_settings.get('page_length', 25)
    pad_lines = embosser_settings.get('pad_lines', True)
    
    # Convert tabs to spaces for consistent formatting
    braille_text = braille_text.replace('\t', '  ')
    
    # Split into paragraphs
    paragraphs = braille_text.split('\n\n')
    formatted_lines = []
    
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        
        # Process each paragraph
        lines = paragraph.split('\n')
        for line in lines:
            if not line.strip():
                # Empty line - add as blank line with proper spacing
                formatted_lines.append(' ' * line_length if pad_lines else '')
                continue
            
            # Word wrap at word boundaries
            words = line.split()
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 <= line_length:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
                else:
                    # Current line is full, start new line
                    if current_line:
                        # Pad to exact line length
                        if pad_lines:
                            formatted_lines.append(current_line.ljust(line_length))
                        else:
                            formatted_lines.append(current_line)
                    current_line = word
            
            # Add the last line of the paragraph
            if current_line:
                if pad_lines:
                    formatted_lines.append(current_line.ljust(line_length))
                else:
                    formatted_lines.append(current_line)
        
        # Add blank line between paragraphs
        if pad_lines:
            formatted_lines.append(' ' * line_length)
        else:
            formatted_lines.append('')
    
    # Group lines into pages
    pages = []
    for i in range(0, len(formatted_lines), page_length):
        page_lines = formatted_lines[i:i + page_length]
        
        # Pad page to exact page length if needed
        while len(page_lines) < page_length:
            if pad_lines:
                page_lines.append(' ' * line_length)
            else:
                page_lines.append('')
        
        pages.append('\n'.join(page_lines))
    
    # Join pages with form feed character
    return '\f'.join(pages)

def generate_brf_file(unicode_braille_text, config=None):
    """
    Generate a BRF (Braille Ready Format) string for embosser printing.
    This function creates a complete BRF string that can be sent directly
    to any professional Braille embosser worldwide.
    Args:
        unicode_braille_text (str): Unicode Braille text to convert
        config (dict, optional): Configuration settings
    Returns:
        str: BRF content as ASCII string (not written to file)
    """
    try:
        # Step 1: Format for embosser (40x25 pages with form feeds)
        formatted_braille = format_for_embosser(unicode_braille_text, config)
        # Step 2: Convert to ASCII BRF format
        brf_content = unicode_to_ascii_braille(formatted_braille)
        return brf_content
    except Exception as e:
        logging.error(f"Failed to generate BRF content: {e}")
        return ""

if __name__ == "__main__":

    # File reading and writing helper functions
    def read_file_content(filepath: str) -> str:
        """Helper to read file content as string"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logging.error(f"Could not read file {filepath}: {e}")
            return ""

    def write_file_content(filepath: str, content: str) -> None:
        """Helper to write content to file"""
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logging.info(f"Content saved to {filepath}")
        except Exception as e:
            logging.error(f"Could not write to file {filepath}: {e}")

    # Generate ASCII and Braille art files as before
    try:
        with open(INPUT_JSON_PATH, "r", encoding="utf-8") as f:
            objects_data = json.load(f)
    except Exception as e:
        logging.error(f"Failed to load input file: {e}")
        exit(1)

    ascii_results = generate_ascii_art_blocks(objects_data)
    if not ascii_results:
        logging.warning("No ASCII art was generated. Check Gemini API logs for errors or quota issues.")
    else:
        save_ascii_art_file(ascii_results, ASCII_OUTPUT_PATH)
        logging.info(f"ASCII art file saved to {ASCII_OUTPUT_PATH}")

        save_braille_art_file(ascii_results, BRAILLE_OUTPUT_PATH)
        logging.info(f"Braille art file saved to {BRAILLE_OUTPUT_PATH}")

    # Load braille art content once for reuse
    braille_art_content = read_file_content('output/braille_art_unicode.txt')

    # --- Convert English transcript to Braille with art ---
    english_transcript = read_file_content('output/transcript_with_figure_tags.txt')
    if english_transcript and braille_art_content:
        english_braille = convert_transcript_to_braille_with_art_from_content(english_transcript, braille_art_content)
        if english_braille:
            write_file_content('output/final_braille_transcript.txt', english_braille)
            print(f"✅ Final Braille transcript saved to output/final_braille_transcript.txt")

    # --- Convert Telugu transcript to Braille with art ---
    telugu_transcript = read_file_content('output/transcript_with_figure_tags_telugu.txt')
    if telugu_transcript and braille_art_content:
        telugu_braille = convert_transcript_to_braille_with_art_telugu_from_content(telugu_transcript, braille_art_content)
        if telugu_braille:
            write_file_content('output/final_braille_transcript_telugu.txt', telugu_braille)
            print(f"✅ Telugu Braille transcript saved to output/final_braille_transcript_telugu.txt")

    # --- Convert Kannada transcript to Braille with art ---
    kannada_transcript = read_file_content('output/transcript_with_figure_tags_kannada.txt')
    if kannada_transcript and braille_art_content:
        kannada_braille = convert_transcript_to_braille_with_art_kannada_from_content(kannada_transcript, braille_art_content)
        if kannada_braille:
            write_file_content('output/final_braille_transcript_kannada.txt', kannada_braille)
            print(f"✅ Kannada Braille transcript saved to output/final_braille_transcript_kannada.txt")

    # --- Generate BRF files ---
    try:
        # For English Braille transcript
        english_braille_text = read_file_content('output/final_braille_transcript.txt')
        if english_braille_text:
            english_brf_content = generate_brf_file(english_braille_text)
            write_file_content('output/final_braille_transcript.brf', english_brf_content)

        # For Telugu Braille transcript
        telugu_braille_text = read_file_content('output/final_braille_transcript_telugu.txt')
        if telugu_braille_text:
            telugu_brf_content = generate_brf_file(telugu_braille_text)
            write_file_content('output/final_braille_transcript_telugu.brf', telugu_brf_content)

        # For Kannada Braille transcript
        kannada_braille_text = read_file_content('output/final_braille_transcript_kannada.txt')
        if kannada_braille_text:
            kannada_brf_content = generate_brf_file(kannada_braille_text)
            write_file_content('output/final_braille_transcript_kannada.brf', kannada_brf_content)
    except Exception as e:
        logging.error(f"Error generating BRF files: {e}")
