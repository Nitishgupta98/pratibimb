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

if __name__ == "__main__":
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
