
# =============================
# Pratibimb API - Main Entrypoint
# =============================

# --- Download API for result files ---
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
#     "enhanced_transcript_file": "enhanced_transcript_for_braille.txt",
#     "enhanced_text": "...string output..."
#   }

# --- Imports ---
from fastapi import FastAPI, HTTPException, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Any, List
import logging
import os
import json
import uuid
from datetime import datetime
import sys

# --- External Modules ---
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from urllib.parse import urlparse, parse_qs
from core.translation_utils import translate_figure_tagged_transcript
import pratibimb

# --- Import Project Modules ---
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "core"))
from core.youtube_analyzer import (
    download_video,
    get_audio_transcript,
    extract_frames,
    deduplicate_frames,
    generate_visual_descriptions,
    save_output,
    generate_merged_transcript,
    extract_relevant_visual_objects,
    enrich_transcript_with_figures,
    VIDEO_FILENAME,
    FRAMES_DIR,
    SSIM_THRESHOLD,
)
from core.braille_art import (
    generate_ascii_art_blocks,
    save_ascii_art_file,
    save_braille_art_file,
    ascii_art_to_braille,
    convert_transcript_to_braille_with_art
)

# --- Load Config ---
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- Validate Config ---
required_keys = [
    'logging_settings', 'output', 'google', 'youtube_analyzer', 'braille_art'
]
for key in required_keys:
    if key not in config:
        raise RuntimeError(f"Missing required key '{key}' in config.json")

# --- Config Values ---
output_folder = config['output']['folder']
raw_transcript_file = config['output']['raw_transcript_file']
enhanced_transcript_file = config['output']['enhanced_transcript_file']
google_api_key = config['google']['api_key']

yt_cfg = config['youtube_analyzer']
yt_video_filename = yt_cfg['video_filename']
yt_frames_dir = yt_cfg['frames_dir']
yt_ssim_threshold = yt_cfg['ssim_threshold']
yt_audio_transcript_filename = yt_cfg['audio_transcript_filename']
yt_visual_description_filename = yt_cfg['visual_description_filename']
yt_merged_transcript_filename = yt_cfg['merged_transcript_filename']
yt_visual_objects_filename = yt_cfg['visual_objects_filename']
yt_figure_tagged_transcript_filename = yt_cfg['figure_tagged_transcript_filename']
yt_output_folder = yt_cfg.get('output_folder', 'output')

braille_cfg = config['braille_art']
braille_ascii_output_path = braille_cfg['ascii_output_path']
braille_unicode_output_path = braille_cfg['unicode_output_path']
braille_max_line_width = braille_cfg['max_line_width']
braille_batch_size = braille_cfg['batch_size']

# --- Logging Setup ---
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), config['logging_settings']['log_file'])
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    level=getattr(logging, config['logging_settings'].get('log_level', 'INFO')),
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# --- Utility Functions ---
def create_request_logger(request_id: str):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"request_{request_id}_{timestamp}.log"
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "requests", log_filename)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger = logging.getLogger(f"request_{request_id}")
    logger.setLevel(logging.INFO)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s [STEP-%(step)s] %(levelname)s: %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger, log_path

def log_step(logger, step_number: int, message: str, level: str = "INFO"):
    extra = {'step': f"{step_number:02d}"}
    if level.upper() == "ERROR":
        logger.error(message, extra=extra)
    elif level.upper() == "WARNING":
        logger.warning(message, extra=extra)
    else:
        logger.info(message, extra=extra)

# --- FastAPI App ---
from fastapi.concurrency import run_in_threadpool
app = FastAPI()

# --- CORS Setup ---
ENV = os.environ.get("PRATIBIMB_ENV", "development")
allowed_origins = config.get('cors_allowed_origins', ["*"]) if ENV == "production" else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False if allowed_origins == ["*"] else True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class TranscriptRequest(BaseModel):
    youtube_url: str

class RawTranscriptRequest(BaseModel):
    youtube_url: str

class EnhanceTranscriptRequest(BaseModel):
    raw_transcript: str

class YoutubeAnalyzeRequest(BaseModel):
    youtube_url: str

class AudioVisualMergeRequest(BaseModel):
    audio_transcript_file: str = "audio_transcript.txt"
    visual_description_file: str = "visual_description.txt"

class BrailleArtRequest(BaseModel):
    objects_data: List

class FullPipelineRequest(BaseModel):
    youtube_url: str

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

# --- API Endpoints ---
# @app.post("/get_raw_transcript")
# async def get_raw_transcript(request: RawTranscriptRequest):
#     url = request.youtube_url
#     logging.info(f"Received request for /get_raw_transcript with URL: {url}")
#     try:
#         transcript = get_youtube_transcript(url)
#         if transcript.startswith("Error fetching transcript"):
#             logging.error(f"Transcript fetch error: {transcript}")
#             raise ValueError(transcript)
#     except Exception as e:
#         logging.error(f"Failed to fetch YouTube transcript: {str(e)}")
#         return JSONResponse(status_code=400, content={"error": f"Failed to fetch YouTube transcript: {str(e)}"})
#     raw_folder = output_folder
#     raw_path = os.path.join(raw_folder, raw_transcript_file)
#     try:
#         os.makedirs(raw_folder, exist_ok=True)
#         with open(raw_path, "w", encoding="utf-8") as f:
#             f.write(transcript)
#     except Exception as e:
#         logging.error(f"Failed to write raw transcript file: {str(e)}")
#         return JSONResponse(status_code=500, content={"error": f"Failed to write raw transcript file: {str(e)}"})
#     return {
#         "raw_transcript_file": FileResponse(raw_path, media_type='text/plain', filename=raw_transcript_file),
#         "raw_transcript": transcript
#     }

# @app.post("/get_enhance_transcript")
# async def enhance_transcript(request: EnhanceTranscriptRequest):
#     transcript = request.raw_transcript
#     logging.info("Received request for /get_enhance_transcript.")
#     try:
#         enhanced = enhance_transcript_for_blind_users(transcript)
#     except Exception as e:
#         logging.error(f"Failed to enhance transcript: {str(e)}")
#         return JSONResponse(status_code=500, content={"error": f"Failed to enhance transcript: {str(e)}"})
#     enhanced_folder = output_folder
#     enhanced_path = os.path.join(enhanced_folder, enhanced_transcript_file)
#     try:
#         os.makedirs(enhanced_folder, exist_ok=True)
#         with open(enhanced_path, "w", encoding="utf-8") as f:
#             f.write(enhanced)
#     except Exception as e:
#         logging.error(f"Failed to write enhanced transcript file: {str(e)}")
#         return JSONResponse(status_code=500, content={"error": f"Failed to write enhanced transcript file: {str(e)}"})
#     return {
#         "enhanced_transcript_file": FileResponse(enhanced_path, media_type='text/plain', filename=enhanced_transcript_file),
#         "enhanced_text": enhanced
#     }

# @app.post("/process_transcript")
# async def process_transcript(request: TranscriptRequest):
#     request_id = str(uuid.uuid4())[:8]
#     req_logger, log_file_path = create_request_logger(request_id)
#     url = request.youtube_url
#     log_step(req_logger, 1, f"🌟 Starting Braille conversion process...")
#     log_step(req_logger, 2, f"📺 Processing YouTube video: {url}")
#     try:
#         log_step(req_logger, 3, "🔄 Extracting video transcript...")
#         transcript = get_youtube_transcript(url)
#         if transcript.startswith("Error fetching transcript"):
#             log_step(req_logger, 3, f"❌ Unable to extract transcript: {transcript}", "ERROR")
#             raise ValueError(transcript)
#     except Exception as e:
#         log_step(req_logger, 3, f"❌ Failed to extract video transcript: {str(e)}", "ERROR")
#         return JSONResponse(status_code=400, content={"error": f"Failed to extract video transcript: {str(e)}", "request_id": request_id, "log_file": log_file_path})
#     raw_folder = output_folder
#     raw_path = os.path.join(raw_folder, raw_transcript_file)
#     try:
#         log_step(req_logger, 4, "💾 Saving original transcript...")
#         os.makedirs(raw_folder, exist_ok=True)
#         with open(raw_path, "w", encoding="utf-8") as f:
#             f.write(transcript)
#     except Exception as e:
#         log_step(req_logger, 4, f"❌ Failed to save transcript: {str(e)}", "ERROR")
#         return JSONResponse(status_code=500, content={"error": f"Failed to save transcript: {str(e)}", "request_id": request_id, "log_file": log_file_path})
#     try:
#         log_step(req_logger, 5, "🎯 Enhancing content for accessibility...")
#         enhanced = enhance_transcript_for_blind_users(transcript)
#     except Exception as e:
#         log_step(req_logger, 5, f"❌ Failed to enhance content: {str(e)}", "ERROR")
#         return JSONResponse(status_code=500, content={"error": f"Failed to enhance content: {str(e)}", "request_id": request_id, "log_file": log_file_path})
#     enhanced_folder = output_folder
#     enhanced_path = os.path.join(enhanced_folder, enhanced_transcript_file)
#     try:
#         log_step(req_logger, 6, "💾 Saving enhanced content...")
#         os.makedirs(enhanced_folder, exist_ok=True)
#         with open(enhanced_path, "w", encoding="utf-8") as f:
#             f.write(enhanced)
#     except Exception as e:
#         log_step(req_logger, 6, f"❌ Failed to save enhanced content: {str(e)}", "ERROR")
#         return JSONResponse(status_code=500, content={"error": f"Failed to save enhanced content: {str(e)}", "request_id": request_id, "log_file": log_file_path})
#     try:
#         log_step(req_logger, 7, "🔤 Starting Braille conversion engine...")
#         pratibimb_result = pratibimb.main()
#         log_step(req_logger, 8, f"⠃ Converting text to Grade 1 Braille format...")
#         log_step(req_logger, 9, f"🖨️ Generating embosser-ready BRF file...")
#         log_step(req_logger, 10, f"✅ Braille conversion completed successfully")
#     except Exception as e:
#         log_step(req_logger, 7, f"❌ Braille conversion failed: {str(e)}", "ERROR")
#         return JSONResponse(status_code=500, content={"error": f"Braille conversion failed: {str(e)}", "request_id": request_id, "log_file": log_file_path})
#     try:
#         log_step(req_logger, 11, "📦 Preparing files for download...")
#         raw_file_response = FileResponse(raw_path, media_type='text/plain', filename=raw_transcript_file)
#         enhanced_file_response = FileResponse(enhanced_path, media_type='text/plain', filename=enhanced_transcript_file)
#     except Exception as e:
#         log_step(req_logger, 11, f"❌ Failed to prepare files: {str(e)}", "ERROR")
#         return JSONResponse(status_code=500, content={"error": f"Failed to prepare files: {str(e)}", "request_id": request_id, "log_file": log_file_path})
#     log_step(req_logger, 12, "🎉 Braille conversion process completed successfully!")
#     return {
#         "raw_transcript_file": raw_file_response,
#         "enhanced_transcript_file": enhanced_file_response,
#         "raw_transcript": transcript,
#         "enhanced_text": enhanced,
#         "request_id": request_id,
#         "log_file": log_file_path,
#         "pratibimb_result": pratibimb_result
#     }

@app.post("/youtube-analyze")
async def youtube_analyze(request: YoutubeAnalyzeRequest):
    """
    Analyze YouTube video: download, transcribe, extract frames, deduplicate, caption.
    All outputs saved in 'raw-output-files' folder.
    Returns file paths and contents.
    """
    url = request.youtube_url
    output_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), yt_output_folder)
    os.makedirs(output_folder_path, exist_ok=True)

    video_path = os.path.join(output_folder_path, yt_video_filename)
    frames_dir = os.path.join(output_folder_path, yt_frames_dir)
    audio_transcript_path = os.path.join(output_folder_path, yt_audio_transcript_filename)
    visual_description_path = os.path.join(output_folder_path, yt_visual_description_filename)

    try:
        # 1. Download Video
        logging.info(f"Step 1: Downloading video from {url}")
        video_path_result, video_title = download_video(url, video_path)
        if not video_path_result or not video_title:
            logging.error("Video download failed.")
            return JSONResponse(status_code=400, content={"error": "Video download failed."})

        # 2. Get Audio Transcript
        logging.info("Step 2: Getting audio transcript")
        audio_transcript = get_audio_transcript(url, video_path_result)
        save_output(audio_transcript_path, audio_transcript)

        # 3. Extract Frames
        logging.info("Step 3: Extracting frames")
        extract_frames(video_path_result, frames_dir)

        # 4. Deduplicate Frames
        logging.info("Step 4: Deduplicating frames")
        unique_frame_paths = deduplicate_frames(frames_dir, yt_ssim_threshold)
        if not unique_frame_paths:
            logging.warning("No unique frames found. Skipping visual description.")
            save_output(visual_description_path, "No visually distinct scenes found.")
            return {
                "audio_transcript_file": audio_transcript_path,
                "audio_transcript_content": audio_transcript,
                "visual_description_file": visual_description_path,
                "visual_description_content": "No visually distinct scenes found.",
                "unique_frames": [],
                "message": "No visually distinct scenes found."
            }

        # 5. Generate Visual Descriptions
        logging.info("Step 5: Generating visual descriptions")
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        blip_model.to(device)
        logging.info(f"BLIP model loaded on device: {device}")

        visual_descriptions = generate_visual_descriptions(
            unique_frame_paths, video_title, blip_model, blip_processor, device
        )
        save_output(visual_description_path, visual_descriptions)

        # Read file contents for response
        with open(audio_transcript_path, "r", encoding="utf-8") as f:
            audio_transcript_content = f.read()
        with open(visual_description_path, "r", encoding="utf-8") as f:
            visual_description_content = f.read()

        return {
            "audio_transcript_file": audio_transcript_path,
            "audio_transcript_content": audio_transcript_content,
            "visual_description_file": visual_description_path,
            "visual_description_content": visual_description_content,
            "unique_frames": unique_frame_paths,
            "message": "Analysis completed successfully."
        }

    except Exception as e:
        logging.error(f"Error in youtube-analyze pipeline: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": f"Analysis failed: {str(e)}"})

@app.post("/audio-visual-merge")
async def audio_visual_merge(request: AudioVisualMergeRequest):
    """
    Merge audio and visual transcripts, extract relevant objects, enrich transcript with figure tags.
    All intermediate files saved in 'raw-output-files', final enriched transcript in 'output'.
    Returns file paths and contents.
    """
    output_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), yt_output_folder)
    final_output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_folder_path, exist_ok=True)
    os.makedirs(final_output_folder, exist_ok=True)

    audio_transcript_path = os.path.join(output_folder_path, request.audio_transcript_file)
    visual_description_path = os.path.join(output_folder_path, request.visual_description_file)

    merged_transcript_path = os.path.join(output_folder_path, yt_merged_transcript_filename)
    visual_objects_path = os.path.join(output_folder_path, yt_visual_objects_filename)
    figure_tagged_transcript_path = os.path.join(final_output_folder, yt_figure_tagged_transcript_filename)

    try:
        # 7. Generate Merged Audio-Visual Transcript
        merged_transcript = generate_merged_transcript(audio_transcript_path, visual_description_path)
        save_output(merged_transcript_path, merged_transcript)

        # 8. Extract Relevant Visual Objects
        visual_objects = extract_relevant_visual_objects(audio_transcript_path, visual_description_path)
        with open(visual_objects_path, 'w', encoding='utf-8') as f:
            json.dump(visual_objects, f, indent=2)

        # 9. Insert Figure Tags into Transcript
        enrich_transcript_with_figures(merged_transcript_path, visual_objects_path, figure_tagged_transcript_path)

        # Read file contents for response
        with open(merged_transcript_path, "r", encoding="utf-8") as f:
            merged_transcript_content = f.read()
        with open(visual_objects_path, "r", encoding="utf-8") as f:
            visual_objects_content = f.read()
        with open(figure_tagged_transcript_path, "r", encoding="utf-8") as f:
            figure_tagged_content = f.read()

        return {
            "merged_transcript_file": merged_transcript_path,
            "merged_transcript_content": merged_transcript_content,
            "visual_objects_file": visual_objects_path,
            "visual_objects_content": visual_objects_content,
            "figure_tagged_transcript_file": figure_tagged_transcript_path,
            "figure_tagged_transcript_content": figure_tagged_content,
            "message": "Audio-visual merge and enrichment completed successfully."
        }

    except Exception as e:
        logging.error(f"Error in audio-visual-merge pipeline: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": f"Audio-visual merge failed: {str(e)}"})

@app.post("/generate-braille-art")
async def generate_braille_art(request: BrailleArtRequest):
    """
    Generate ASCII and Braille art from object data.
    Returns file contents and file paths.
    All filenames and constants are read from config.json.
    """
    objects_data = request.objects_data

    try:
        # Generate ASCII art blocks
        ascii_results = generate_ascii_art_blocks(objects_data)
        if not ascii_results:
            logging.warning("No ASCII art was generated. Check Gemini API logs for errors or quota issues.")
            return JSONResponse(status_code=500, content={"error": "No ASCII art was generated."})

        # Save ASCII art file
        save_ascii_art_file(ascii_results, braille_ascii_output_path)
        logging.info(f"ASCII art file saved to {braille_ascii_output_path}")

        # Save Braille art file
        save_braille_art_file(ascii_results, braille_unicode_output_path)
        logging.info(f"Braille art file saved to {braille_unicode_output_path}")

        # Read file contents
        with open(braille_ascii_output_path, "r", encoding="utf-8") as f:
            ascii_content = f.read()
        with open(braille_unicode_output_path, "r", encoding="utf-8") as f:
            braille_content = f.read()

        return {
            "ascii_art_file": braille_ascii_output_path,
            "ascii_art_content": ascii_content,
            "braille_art_file": braille_unicode_output_path,
            "braille_art_content": braille_content,
            "message": "Braille art generation completed successfully."
        }

    except Exception as e:
        logging.error(f"Error in braille art generation: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": f"Braille art generation failed: {str(e)}"})

@app.post("/full-braille-pipeline")
async def full_braille_pipeline(request: FullPipelineRequest):
    """
    Complete pipeline: YouTube analysis, audio-visual merge, Braille art generation.
    Starts processing in background and returns immediately.
    Use /api/stream-logs to monitor progress.
    """
    # Generate request ID first
    request_id = str(uuid.uuid4())[:8]
    
    def pipeline_job():
        req_logger, log_file_path = create_request_logger(request_id)
        url = request.youtube_url
        log_step(req_logger, 1, f"🌟 Starting Full Braille pipeline process...")
        log_step(req_logger, 2, f"📺 Processing YouTube video: {url}")
        output_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), yt_output_folder)
        final_output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
        os.makedirs(output_folder_path, exist_ok=True)
        os.makedirs(final_output_folder, exist_ok=True)

        video_path = os.path.join(output_folder_path, yt_video_filename)
        frames_dir = os.path.join(output_folder_path, yt_frames_dir)
        audio_transcript_path = os.path.join(output_folder_path, yt_audio_transcript_filename)
        visual_description_path = os.path.join(output_folder_path, yt_visual_description_filename)
        merged_transcript_path = os.path.join(output_folder_path, yt_merged_transcript_filename)
        visual_objects_path = os.path.join(output_folder_path, yt_visual_objects_filename)
        figure_tagged_transcript_path = os.path.join(final_output_folder, yt_figure_tagged_transcript_filename)
        ascii_art_path = braille_ascii_output_path
        braille_art_path = braille_unicode_output_path
        final_braille_transcript_path = os.path.join(final_output_folder, "final_braille_transcript.txt")

        try:
            # 1. Download Video
            log_step(req_logger, 3, "🔄 Downloading YouTube video...")
            video_path_result, video_title = download_video(url, video_path)
            if not video_path_result or not video_title:
                log_step(req_logger, 3, "❌ Video download failed.", "ERROR")
                return

            # 2. Get Audio Transcript
            log_step(req_logger, 4, "🔊 Extracting audio transcript...")
            audio_transcript = get_audio_transcript(url, video_path_result)
            save_output(audio_transcript_path, audio_transcript)

            # 3. Extract Frames
            log_step(req_logger, 5, "🖼️ Extracting video frames...")
            extract_frames(video_path_result, frames_dir)

            # 4. Deduplicate Frames
            log_step(req_logger, 6, "🧹 Deduplicating frames...")
            unique_frame_paths = deduplicate_frames(frames_dir, yt_ssim_threshold)
            if not unique_frame_paths:
                log_step(req_logger, 6, "⚠️ No visually distinct scenes found. Skipping visual description.", "WARNING")
                save_output(visual_description_path, "No visually distinct scenes found.")
                return

            # 5. Generate Visual Descriptions
            log_step(req_logger, 7, "📝 Generating visual descriptions...")
            from transformers import BlipProcessor, BlipForConditionalGeneration
            import torch
            blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
            blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
            device = "cuda" if torch.cuda.is_available() else "cpu"
            blip_model.to(device)
            visual_descriptions = generate_visual_descriptions(
                unique_frame_paths, video_title, blip_model, blip_processor, device
            )
            save_output(visual_description_path, visual_descriptions)

            # 6. Merge Audio-Visual Transcript
            log_step(req_logger, 8, "🔗 Merging audio and visual transcripts...")
            merged_transcript = generate_merged_transcript(audio_transcript_path, visual_description_path)
            save_output(merged_transcript_path, merged_transcript)

            # 7. Extract Relevant Visual Objects
            log_step(req_logger, 9, "🔍 Extracting relevant visual objects...")
            visual_objects = extract_relevant_visual_objects(audio_transcript_path, visual_description_path)
            with open(visual_objects_path, 'w', encoding='utf-8') as f:
                json.dump(visual_objects, f, indent=2)

            # 8. Insert Figure Tags
            log_step(req_logger, 10, "🏷️ Inserting figure tags into transcript...")
            enrich_transcript_with_figures(merged_transcript_path, visual_objects_path, figure_tagged_transcript_path)

            # 9. Generate Braille/ASCII Art
            log_step(req_logger, 11, "🎨 Generating ASCII and Braille art blocks...")
            ascii_results = generate_ascii_art_blocks(visual_objects)
            if not ascii_results:
                log_step(req_logger, 11, "❌ No ASCII art was generated. Check Gemini API logs for errors or quota issues.", "ERROR")
                return

            save_ascii_art_file(ascii_results, ascii_art_path)
            save_braille_art_file(ascii_results, braille_art_path)

            # 10. Assemble Final Braille Document
            log_step(req_logger, 12, "📦 Assembling final Braille document with text and art...")
            convert_transcript_to_braille_with_art(
                transcript_path=figure_tagged_transcript_path,
                braille_art_path=braille_art_path,
                output_path=final_braille_transcript_path
            )

            log_step(req_logger, 13, "✅ Full Braille pipeline completed successfully!")

        except Exception as e:
            log_step(req_logger, 99, f"❌ Error in full-braille-pipeline: {str(e)}", "ERROR")
            logging.error(f"Pipeline error: {str(e)}", exc_info=True)

    # Start the pipeline job in a background thread and return immediately
    import threading
    
    # Create a background thread to run the pipeline
    def run_pipeline_background():
        try:
            pipeline_job()
        except Exception as e:
            logging.error(f"Background pipeline error: {str(e)}")
    
    # Start background thread
    thread = threading.Thread(target=run_pipeline_background, daemon=True)
    thread.start()
    
    # Return immediately with basic info
    return {
        "message": "Full Braille pipeline started successfully. Use /api/stream-logs to monitor progress.",
        "request_id": request_id,
        "status": "processing"
    }

@app.get("/api/stream-logs")
async def stream_logs_latest():
    """
    Stream logs for the latest process in real-time (no request_id needed). 
    Always returns current log state immediately and is fully independent of any other process.
    This endpoint is non-blocking and responds instantly.
    """
    try:
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "requests")
        
        # Check if logs directory exists
        if not os.path.exists(logs_dir):
            return {
                "progress_steps": [], 
                "total_steps": 13, 
                "current_step": 0, 
                "is_complete": False,
                "message": "No logs directory found. Start a pipeline process first."
            }
        
        # Get all log files
        try:
            log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
        except Exception as e:
            return {
                "progress_steps": [], 
                "total_steps": 13, 
                "current_step": 0, 
                "is_complete": False,
                "error": f"Could not list log files: {str(e)}"
            }
            
        if not log_files:
            return {
                "progress_steps": [], 
                "total_steps": 13, 
                "current_step": 0, 
                "is_complete": False,
                "message": "No log files found. Start a pipeline process first."
            }
            
        # Get the latest log file
        latest_log = sorted(log_files)[-1]
        log_path = os.path.join(logs_dir, latest_log)
        progress_steps = []
        seen_steps = set()
        
        # Read the log file in a non-blocking way
        if os.path.exists(log_path):
            try:
                # Read only the last 150 lines for speed and to catch all steps
                with open(log_path, 'r', encoding='utf-8') as f:
                    log_lines = f.readlines()[-150:]
            except Exception as e:
                return {
                    "progress_steps": [], 
                    "total_steps": 13, 
                    "current_step": 0, 
                    "is_complete": False, 
                    "error": f"Could not read log: {str(e)}"
                }
                
            for line in log_lines:
                if '[STEP-' in line and ('] INFO:' in line or '] ERROR:' in line or '] WARNING:' in line):
                    try:
                        step_part = line.split('[STEP-')[1].split(']')[0]
                        message_part = ""
                        status = "completed"
                        
                        if '] INFO: ' in line:
                            message_part = line.split('] INFO: ')[1].strip()
                            status = "completed"
                        elif '] ERROR: ' in line:
                            message_part = line.split('] ERROR: ')[1].strip()
                            status = "error"
                        elif '] WARNING: ' in line:
                            message_part = line.split('] WARNING: ')[1].strip()
                            status = "warning"
                            
                        step_num = int(step_part)
                        
                        if step_num not in seen_steps:
                            seen_steps.add(step_num)
                            timestamp_str = line.split(' [STEP-')[0]
                            try:
                                # Handle timestamp parsing more robustly
                                parsed_time = datetime.fromisoformat(timestamp_str.replace(',', '.'))
                                formatted_timestamp = parsed_time.strftime("%H:%M:%S")
                            except:
                                formatted_timestamp = datetime.now().strftime("%H:%M:%S")
                                
                            progress_steps.append({
                                "step": step_num,
                                "message": message_part,
                                "status": status,
                                "timestamp": formatted_timestamp
                            })
                    except Exception as parse_error:
                        # Skip malformed lines silently
                        continue
                        
            progress_steps.sort(key=lambda x: x["step"])
        
        # Determine completion status
        has_error = any(step["status"] == "error" for step in progress_steps)
        is_complete = len(progress_steps) >= 12 or has_error
        
        # Always return immediately, even if log is empty or process is ongoing
        return {
            "progress_steps": progress_steps,
            "total_steps": 13,
            "current_step": len(progress_steps),
            "is_complete": is_complete,
            "has_error": has_error,
            "latest_log_file": latest_log,
            "processing_status": "error" if has_error else ("completed" if is_complete else "processing")
        }
        
    except Exception as e:
        # Return error but don't raise exception - keep endpoint responsive
        return {
            "progress_steps": [], 
            "total_steps": 13, 
            "current_step": 0, 
            "is_complete": False,
            "error": f"Error streaming logs: {str(e)}",
            "processing_status": "error"
        }

@app.get("/api/pipeline-status")
async def pipeline_status():
    """
    Check the status of the pipeline and available files.
    Returns which files are available and their last modification times.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Define expected output files
        files_to_check = {
            "audio_transcript": os.path.join(base_dir, "raw-output-files", "audio_transcript.txt"),
            "visual_description": os.path.join(base_dir, "raw-output-files", "visual_description.txt"),
            "merged_transcript": os.path.join(base_dir, "raw-output-files", "merged_audio_visual_transcript.txt"),
            "visual_objects": os.path.join(base_dir, "raw-output-files", "relevant_visual_objects.json"),
            "figure_tagged_transcript": os.path.join(base_dir, "output", "transcript_with_figure_tags.txt"),
            "ascii_art": os.path.join(base_dir, "output", "braille_art_ascii.txt"),
            "braille_art": os.path.join(base_dir, "output", "braille_art_unicode.txt"),
            "final_braille_transcript": os.path.join(base_dir, "output", "final_braille_transcript.txt")
        }
        
        file_status = {}
        for file_key, file_path in files_to_check.items():
            if os.path.exists(file_path):
                try:
                    stat = os.stat(file_path)
                    mod_time = datetime.fromtimestamp(stat.st_mtime)
                    file_status[file_key] = {
                        "exists": True,
                        "path": file_path,
                        "size": stat.st_size,
                        "modified": mod_time.isoformat(),
                        "modified_human": mod_time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                except Exception as e:
                    file_status[file_key] = {
                        "exists": True,
                        "path": file_path,
                        "error": f"Could not read file stats: {str(e)}"
                    }
            else:
                file_status[file_key] = {
                    "exists": False,
                    "path": file_path
                }
        
        # Count available files
        available_files = sum(1 for status in file_status.values() if status.get("exists", False))
        total_files = len(file_status)
        
        # Determine overall status
        if available_files == 0:
            overall_status = "not_started"
        elif available_files == total_files:
            overall_status = "completed"
        else:
            overall_status = "in_progress"
        
        return {
            "overall_status": overall_status,
            "available_files": available_files,
            "total_files": total_files,
            "completion_percentage": round((available_files / total_files) * 100, 1),
            "files": file_status,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500, 
            content={
                "error": f"Error checking pipeline status: {str(e)}",
                "overall_status": "error"
            }
        )

import mimetypes
@app.get("/api/download/{file_type}")
async def download_file(file_type: str):
    """
    Download result files by type. Supported types: merged_transcript, figure_tagged_transcript, braille_art, final_braille_transcript
    """
    file_map = {
        "merged_transcript": os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw-output-files", "merged_audio_visual_transcript.txt"),
        "figure_tagged_transcript": os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "transcript_with_figure_tags.txt"),
        "braille_art": os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "braille_art_unicode.txt"),
        "final_braille_transcript": os.path.join(os.path.dirname(os.path.abspath(__file__)), "output", "final_braille_transcript.txt"),
    }
    if file_type not in file_map:
        return JSONResponse(status_code=404, content={"error": f"Unknown file type: {file_type}"})
    file_path = file_map[file_type]
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": f"File not found: {file_type}"})
    mime_type, _ = mimetypes.guess_type(file_path)
    return FileResponse(file_path, media_type=mime_type or 'application/octet-stream', filename=os.path.basename(file_path))

@app.post("/generate-braille-telugu")
async def generate_braille_telugu():
    """
    Translate figure-tagged transcript to Telugu and generate final Telugu Braille transcript.
    Returns file paths and contents.
    """
    # 1. Translate transcript to Telugu
    input_path = os.path.join("output", "transcript_with_figure_tags.txt")
    translate_figure_tagged_transcript(input_path, lang_map={'te': 'Telugu'})
    telugu_transcript_path = os.path.join("output", "transcript_with_figure_tags_telugu.txt")
    braille_art_path = os.path.join("output", "braille_art_unicode.txt")
    final_braille_transcript_path = os.path.join("output", "final_braille_transcript_telugu.txt")

    # 2. Generate final Telugu Braille transcript (call the function from braille_art.py)
    from core.braille_art import convert_transcript_to_braille_with_art_telugu
    convert_transcript_to_braille_with_art_telugu(
        transcript_path=telugu_transcript_path,
        braille_art_path=braille_art_path,
        output_path=final_braille_transcript_path
    )

    # 3. Read and return files and contents
    def read_file(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    return {
        "telugu_transcript_file": telugu_transcript_path,
        "telugu_transcript_content": read_file(telugu_transcript_path),
        "final_braille_transcript_telugu_file": final_braille_transcript_path,
        "final_braille_transcript_telugu_content": read_file(final_braille_transcript_path),
        "braille_art_file": braille_art_path,
        "braille_art_content": read_file(braille_art_path),
        "message": "Telugu Braille transcript generated successfully."
    }

# --- Kannada Braille API ---
@app.post("/generate-braille-kannada")
async def generate_braille_kannada():
    """
    Translate figure-tagged transcript to Kannada and generate final Kannada Braille transcript.
    Returns file paths and contents.
    """
    # 1. Translate transcript to Kannada
    input_path = os.path.join("output", "transcript_with_figure_tags.txt")
    translate_figure_tagged_transcript(input_path, lang_map={'kn': 'Kannada'})
    kannada_transcript_path = os.path.join("output", "transcript_with_figure_tags_kannada.txt")
    braille_art_path = os.path.join("output", "braille_art_unicode.txt")
    final_braille_transcript_path = os.path.join("output", "final_braille_transcript_kannada.txt")

    # 2. Generate final Kannada Braille transcript (call the function from braille_art.py)
    from core.braille_art import convert_transcript_to_braille_with_art_kannada
    convert_transcript_to_braille_with_art_kannada(
        transcript_path=kannada_transcript_path,
        braille_art_path=braille_art_path,
        output_path=final_braille_transcript_path
    )

    # 3. Read and return files and contents
    def read_file(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    return {
        "kannada_transcript_file": kannada_transcript_path,
        "kannada_transcript_content": read_file(kannada_transcript_path),
        "final_braille_transcript_kannada_file": final_braille_transcript_path,
        "final_braille_transcript_kannada_content": read_file(final_braille_transcript_path),
        "braille_art_file": braille_art_path,
        "braille_art_content": read_file(braille_art_path),
        "message": "Kannada Braille transcript generated successfully."
    }



if __name__ == "__main__":
    import uvicorn
    print("🌟 PRATIBIMB - True Reflection of Digital World 🌟")
    print("Starting API Server...")
    print("============================================================")
    print("📍 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 Available endpoints:")
    print("   • POST /process_transcript - Complete processing")
    print("   • POST /get_raw_transcript - Get YouTube transcript")
    print("   • POST /get_enhance_transcript - Enhance for blind users")
    print("   • GET /api/reports/{name} - Get report file")
    print("   • GET /api/latest-report - Get latest report")
    print("   • GET /api/latest-report-data - Get latest report as JSON")
    print("   • GET /api/download/{file_type} - Download generated files")
    print("   • GET /api/request-log/{request_id} - Get request-specific log")
    print("   • GET /api/stream-logs/{request_id} - Stream real-time progress")
    print("   • GET /api/download/{file_type} - Download specific file type")
    print("   • GET /api/request-log/{request_id} - Get request-specific log")
    print("   • POST /youtube-analyze - Analyze YouTube video")
    print("   • POST /generate-braille-art - Generate ASCII and Braille art")
    print("============================================================")
    print("Press Ctrl+C to stop the server")
    print()
    
    #uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
