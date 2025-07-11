# API for YouTube transcript enhancement for blind users
#
# POST /process_transcript
# Request JSON body:
#   {
#     "youtube_url": "<YouTube video URL>"
#   }
# Response JSON:
#   {
#     "raw_transcript_file": "raw_transcript.txt",
#     "enhanced_transcript_file": "enhanced_transcript_for_blind.txt",
#     "enhanced_text": "...string output..."
#   }

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs

import logging
import os
import json



# Load config
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Setup logging from config
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['logging']['log_file'])
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

app = FastAPI()

class TranscriptRequest(BaseModel):
    youtube_url: str

def get_video_id(youtube_url):
    parsed_url = urlparse(youtube_url)
    if 'youtube.com' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.lstrip('/')
    else:
        raise ValueError("Invalid YouTube URL format")

def get_youtube_transcript(video_url, language='en'):
    try:
        video_id = get_video_id(video_url)
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        if transcript_list.find_transcript([language]):
            transcript = transcript_list.find_transcript([language]).fetch()
        else:
            transcript = transcript_list.find_transcript(transcript_list._manually_created_transcripts).fetch()
        formatter = TextFormatter()
        text_transcript = formatter.format_transcript(transcript)
        return text_transcript
    except Exception as e:
        return f"Error fetching transcript: {e}"

def enhance_transcript_for_blind_users(transcript: str) -> str:
    GOOGLE_API_KEY = config['google']['api_key']
    genai.configure(api_key=GOOGLE_API_KEY)
    prompt = f"""
You are an accessibility-focused editor.

Your task is to enhance a raw transcript of a spoken YouTube video so it is suitable for blind and visually impaired users. The enhanced output will be used in a braille transcription system, so formatting must be plain text only. Follow these instructions carefully:

1. Start your response with a simple, descriptive title summarizing the topic. It should be one line only, like "Phases of the Moon - Enhanced Transcript for Visually Impaired Users".
2. Remove all informal chatter, greetings, first-person expressions, or irrelevant side comments (such as "Hey everyone", "I'm excited", "Mr. Whiskers", etc.).
3. Eliminate all visual-only references like "look at this", "as you can see", "notice the shape", "see here", etc.
4. If something visual is essential for understanding, describe it clearly in words suitable for a blind user (e.g., "The crescent moon resembles a thin curve").
5. Keep the language objective, respectful, and focused on the topic.
6. Maintain proper grammar and punctuation, but do not include any formatting symbols such as asterisks, underscores, or markdown characters.
7. Return only plain, well-structured, clean text with no code, formatting, or symbols.

Rewrite the transcript below according to these rules.
{transcript}
"""

    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()


class RawTranscriptRequest(BaseModel):
    youtube_url: str

class EnhanceTranscriptRequest(BaseModel):
    raw_transcript: str

# API 1: POST /get_raw_transcript
# Request JSON body:
#   {
#     "youtube_url": "<YouTube video URL>"
#   }
# Response JSON:
#   {
#     "raw_transcript_file": "raw_transcript.txt",
#     "raw_transcript": "...string output..."
#   }
@app.post("/get_raw_transcript")
async def get_raw_transcript(request: RawTranscriptRequest):
    url = request.youtube_url
    logging.info(f"Received request for /get_raw_transcript with URL: {url}")
    try:
        logging.info("Fetching YouTube transcript...")
        transcript = get_youtube_transcript(url)
        if transcript.startswith("Error fetching transcript"):
            logging.error(f"Transcript fetch error: {transcript}")
            raise ValueError(transcript)
        logging.info("Transcript fetched successfully.")
    except Exception as e:
        logging.error(f"Failed to fetch YouTube transcript: {str(e)}")
        return JSONResponse(status_code=400, content={
            "error": f"Failed to fetch YouTube transcript: {str(e)}"
        })

    raw_folder = config['output']['folder'] 
    raw_path = os.path.join(raw_folder, config['output']['raw_transcript_file'])
    try:
        if not os.path.exists(raw_folder):
            logging.info(f"Output folder {raw_folder} does not exist. Creating...")
            os.makedirs(raw_folder, exist_ok=True)
        logging.info(f"Writing raw transcript to {raw_path}...")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        logging.info("Raw transcript written successfully.")
    except Exception as e:
        logging.error(f"Failed to write raw transcript file: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to write raw transcript file: {str(e)}"
        })

    logging.info("Returning raw transcript response.")
    return {
        "raw_transcript_file": FileResponse(raw_path, media_type='text/plain', filename=config['output']['raw_transcript_file']),
        "raw_transcript": transcript
    }

# API 2: POST /enhance_transcript
# Request JSON body:
#   {
#     "raw_transcript": "...string..."
#   }
# Response JSON:
#   {
#     "enhanced_transcript_file": "enhanced_transcript_for_blind.txt",
#     "enhanced_text": "...string output..."
#   }
@app.post("/get_enhance_transcript")
async def enhance_transcript(request: EnhanceTranscriptRequest):
    transcript = request.raw_transcript
    logging.info("Received request for /get_enhance_transcript.")
    try:
        logging.info("Enhancing transcript for blind users...")
        enhanced = enhance_transcript_for_blind_users(transcript)
        logging.info("Transcript enhanced successfully.")
    except Exception as e:
        logging.error(f"Failed to enhance transcript: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to enhance transcript: {str(e)}"
        })

    enhanced_folder = config['output']['folder']
    enhanced_path = os.path.join(enhanced_folder, config['output']['enhanced_transcript_file'])
    try:
        if not os.path.exists(enhanced_folder):
            logging.info(f"Output folder {enhanced_folder} does not exist. Creating...")
            os.makedirs(enhanced_folder, exist_ok=True)
        logging.info(f"Writing enhanced transcript to {enhanced_path}...")
        with open(enhanced_path, "w", encoding="utf-8") as f:
            f.write(enhanced)
        logging.info("Enhanced transcript written successfully.")
    except Exception as e:
        logging.error(f"Failed to write enhanced transcript file: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to write enhanced transcript file: {str(e)}"
        })

    logging.info("Returning enhanced transcript response.")
    return {
        "enhanced_transcript_file": FileResponse(enhanced_path, media_type='text/plain', filename=config['output']['enhanced_transcript_file']),
        "enhanced_text": enhanced
    }

@app.post("/process_transcript")
async def process_transcript(request: TranscriptRequest):
    url = request.youtube_url
    logging.info(f"Received request for /process_transcript with URL: {url}")
    try:
        logging.info("Fetching YouTube transcript...")
        transcript = get_youtube_transcript(url)
        if transcript.startswith("Error fetching transcript"):
            logging.error(f"Transcript fetch error: {transcript}")
            raise ValueError(transcript)
        logging.info("Transcript fetched successfully.")
    except Exception as e:
        logging.error(f"Failed to fetch YouTube transcript: {str(e)}")
        return JSONResponse(status_code=400, content={
            "error": f"Failed to fetch YouTube transcript: {str(e)}"
        })

    raw_folder = config['output']['folder']
    raw_path = os.path.join(raw_folder, config['output']['raw_transcript_file'])
    try:
        if not os.path.exists(raw_folder):
            logging.info(f"Output folder {raw_folder} does not exist. Creating...")
            os.makedirs(raw_folder, exist_ok=True)
        logging.info(f"Writing raw transcript to {raw_path}...")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        logging.info("Raw transcript written successfully.")
    except Exception as e:
        logging.error(f"Failed to write raw transcript file: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to write raw transcript file: {str(e)}"
        })

    try:
        logging.info("Enhancing transcript for blind users...")
        enhanced = enhance_transcript_for_blind_users(transcript)
        logging.info("Transcript enhanced successfully.")
    except Exception as e:
        logging.error(f"Failed to enhance transcript: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to enhance transcript: {str(e)}"
        })

    enhanced_folder = config['output']['folder']
    enhanced_path = os.path.join(enhanced_folder, config['output']['enhanced_transcript_file'])
    try:
        if not os.path.exists(enhanced_folder):
            logging.info(f"Output folder {enhanced_folder} does not exist. Creating...")
            os.makedirs(enhanced_folder, exist_ok=True)
        logging.info(f"Writing enhanced transcript to {enhanced_path}...")
        with open(enhanced_path, "w", encoding="utf-8") as f:
            f.write(enhanced)
        logging.info("Enhanced transcript written successfully.")
    except Exception as e:
        logging.error(f"Failed to write enhanced transcript file: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to write enhanced transcript file: {str(e)}"
        })

    try:
        logging.info("Preparing file responses for download...")
        raw_file_response = FileResponse(raw_path, media_type='text/plain', filename="raw_transcript.txt")
        enhanced_file_response = FileResponse(enhanced_path, media_type='text/plain', filename="enhanced_transcript_for_blind.txt")
        logging.info("File responses prepared successfully.")
    except Exception as e:
        logging.error(f"Failed to prepare file responses: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to prepare file responses: {str(e)}"
        })

    logging.info("Returning process_transcript response.")
    return {
        "raw_transcript_file": raw_file_response,
        "enhanced_transcript_file": enhanced_file_response,
        "raw_transcript": transcript,
        "enhanced_text": enhanced
    }
