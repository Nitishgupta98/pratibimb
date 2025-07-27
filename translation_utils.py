
import logging
import re
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Constants
SUPPORTED_LANGS = {'te': 'Telugu', 'kn': 'Kannada'}
GEMINI_MODEL_NAME = "gemini-2.5-flash"

# Configure Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env file")
genai.configure(api_key=GEMINI_API_KEY)


def _translate_batch(text_batch: str, lang_name: str) -> str:
    prompt = f"""
Translate the following text to {lang_name}. Preserve any [Fig_x: ...] tags exactly as they are. 
Only return the translated text. Do not add explanations.

Text:
{text_batch.strip()}
"""
    try:
        model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Translation failed: {e}")
        return "[Translation failed]"


def translate_text_to_language(text: str, target_lang: str) -> str:
    if target_lang not in SUPPORTED_LANGS:
        return f"[Translation failed: Unsupported language code '{target_lang}']"
    
    lang_name = SUPPORTED_LANGS[target_lang]
    pattern = re.compile(r'(\[Fig_\d+:\s*[^\]]+\])')
    segments = pattern.split(text)

    translated_segments = []
    buffer = []

    for seg in segments:
        if pattern.fullmatch(seg):
            if buffer:
                combined_text = ''.join(buffer).strip()
                if combined_text:
                    translated_segments.append(_translate_batch(combined_text, lang_name))
                buffer = []
            translated_segments.append(seg)
        else:
            buffer.append(seg)

    # Handle remaining buffer
    if buffer:
        combined_text = ''.join(buffer).strip()
        if combined_text:
            translated_segments.append(_translate_batch(combined_text, lang_name))

    return ''.join(translated_segments)


def translate_figure_tagged_transcript(input_path: str = "output/transcript_with_figure_tags.txt", lang_map: dict = None) -> None:
    if lang_map is None:
        lang_map = {'te': 'Telugu', 'kn': 'Kannada'}

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            transcript_text = f.read()
    except Exception as e:
        logging.error(f"Could not read {input_path} for translation: {e}")
        return

    for lang_code, lang_name in lang_map.items():
        logging.info(f"🔤 Translating transcript to {lang_name} ({lang_code}) using Gemini API...")
        translated = translate_text_to_language(transcript_text, lang_code)
        output_file = f"output/transcript_with_figure_tags_{lang_name.lower()}.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(translated)
            logging.info(f"✅ Translated transcript saved to {output_file}")
        except Exception as e:
            logging.error(f"❌ Failed to save translated transcript for {lang_name}: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate a figure-tagged transcript to Telugu using Gemini API, preserving [Fig_x: ...] tags.")
    parser.add_argument('--input', type=str, default='output/transcript_with_figure_tags.txt', help='Input transcript file (default: output/transcript_with_figure_tags.txt)')
    args = parser.parse_args()
    translate_figure_tagged_transcript(args.input, lang_map={'te': 'Telugu'})


# === PREVIOUS CODE COMMENTED OUT ===
r'''
# Multilingual translation utilities using IndicTrans2 (AI4Bharat/indictrans2-en-indic)
from typing import List
import logging
import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

SUPPORTED_LANGS = {'te': 'Telugu', 'kn': 'Kannada'}
MODEL_NAME = 'Helsinki-NLP/opus-mt-en-mul'

_tokenizer = None
_model = None
_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def _load_model():
    global _tokenizer, _model
    if _tokenizer is None or _model is None:
        try:
            logging.info("Loading tokenizer and model from Hugging Face (Helsinki-NLP/opus-mt-en-mul)...")
            _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(_device)
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load translation model: {e}")
            raise RuntimeError("Could not load translation model.")

def translate_text_to_language(text: str, target_lang: str) -> str:
    if target_lang not in SUPPORTED_LANGS:
        return f"[Translation failed: Unsupported language code '{target_lang}']"
    _load_model()

    pattern = re.compile(r'(\[Fig_\d+:\s*[^\]]+\])')
    segments = pattern.split(text)
    translated_segments = []

    # Marian models require prepending the language token to the input, e.g., '>>te<< '
    lang_token = f">>{target_lang}<< "
    for seg in segments:
        if pattern.fullmatch(seg):
            translated_segments.append(seg)  # Skip translation for figure tags
        elif seg.strip():
            try:
                # Prepend language token
                input_text = lang_token + seg.strip()
                inputs = _tokenizer([input_text], return_tensors="pt", padding=True, truncation=True, max_length=512).to(_device)
                with torch.no_grad():
                    output = _model.generate(**inputs)
                translated = _tokenizer.batch_decode(output, skip_special_tokens=True)[0]
                translated_segments.append(translated)
            except Exception as e:
                logging.error(f"Translation failed: {e}")
                translated_segments.append("[Translation failed: Could not translate text]")
        else:
            translated_segments.append(seg)  # Preserve whitespace
    return ''.join(translated_segments)

def batch_translate(texts: List[str], target_lang: str) -> List[str]:
    if target_lang not in SUPPORTED_LANGS:
        return [f"[Translation failed: Unsupported language code '{target_lang}']" for _ in texts]
    _load_model()
    try:
        lang_token = f">>{target_lang}<< "
        texts_with_token = [lang_token + t.strip() for t in texts]
        inputs = _tokenizer(texts_with_token, return_tensors="pt", padding=True, truncation=True, max_length=512).to(_device)
        with torch.no_grad():
            output = _model.generate(**inputs)
        return _tokenizer.batch_decode(output, skip_special_tokens=True)
    except Exception as e:
        logging.error(f"Batch translation failed: {e}")
        return ["[Translation failed: Could not translate text]" for _ in texts]

def translate_figure_tagged_transcript(input_path: str = "transcript_with_figure_tags.txt", lang_map: dict = None) -> None:
    if lang_map is None:
        lang_map = {'te': 'Telugu', 'kn': 'Kannada'}

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            transcript_text = f.read()
    except Exception as e:
        logging.error(f"Could not read {input_path} for translation: {e}")
        return

    for lang_code, lang_name in lang_map.items():
        logging.info(f"Translating transcript to {lang_name} ({lang_code})...")
        translated = translate_text_to_language(transcript_text, lang_code)
        output_file = f"transcript_with_figure_tags_{lang_name.lower()}.txt"
        try:
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.write(translated)
            logging.info(f"Translated transcript saved to {output_file}")
        except Exception as e:
            logging.error(f"Failed to save translated transcript for {lang_name}: {e}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Translate a figure-tagged transcript to Telugu and Kannada, preserving [Fig_x: ...] tags.")
    parser.add_argument('--input', type=str, default='transcript_with_figure_tags.txt', help='Input transcript file')
    args = parser.parse_args()
    translate_figure_tagged_transcript(args.input)

if __name__ == "__main__":
    main()
'''
