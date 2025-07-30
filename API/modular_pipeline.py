# =============================
# Pratibimb Modular Pipeline API
# =============================
# 
# This file contains 13 individual API endpoints that break down the full-braille-pipeline
# into discrete, manageable steps for better scalability and debugging.
#
# Each endpoint performs a specific task in the Braille conversion pipeline:
# 1. /validate-youtube-url - Validate YouTube URL
# 2. /download-video - Download video from YouTube
# 3. /extract-audio-transcript - Extract audio transcript
# 4. /extract-video-frames - Extract video frames
# 5. /deduplicate-frames - Remove duplicate frames
# 6. /generate-visual-descriptions - Generate descriptions for frames
# 7. /merge-audio-visual - Merge audio and visual transcripts
# 8. /extract-visual-objects - Extract relevant visual objects
# 9. /enrich-with-figure-tags - Add figure tags to transcript
# 10. /generate-ascii-art - Generate ASCII art from objects
# 11. /generate-braille-art - Convert ASCII to Braille art
# 12. /assemble-final-document - Combine transcript with Braille art
# 13. /finalize-output - Generate final downloadable files

# --- Imports ---
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import logging
import os
import json
import uuid
import sys
import tempfile
import base64
from datetime import datetime
from urllib.parse import urlparse, parse_qs

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
    enrich_transcript_with_figures
)

from core.braille_art import (
    generate_ascii_art_blocks,
    save_ascii_art_file,
    save_braille_art_file,
    convert_transcript_to_braille_with_art,
    convert_transcript_to_braille_with_art_from_content,
    convert_transcript_to_braille_with_art_telugu_from_content,
    convert_transcript_to_braille_with_art_kannada_from_content
)

# Import translation utils for translation step
from core.translation_utils import translate_figure_tagged_transcript_content
# --- Request Models ---
class BrailleLangRequest(BaseModel):
    transcript_content: str
    braille_art_content: str

# --- Load Config ---
CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

# --- Config Values ---
yt_cfg = config['youtube_analyzer']
braille_cfg = config['braille_art']
request_files_cfg = config.get('request_files', {
    'folder': 'Request_files',
    'video_filename': 'downloaded_video.mp4',
    'audio_transcript_filename': 'audio_transcript.txt',
    'frames_dir': 'video_frames',
    'dedup_frames_dir': 'dedup_frames',
    'visual_description_filename': 'visual_description.txt'
})

# Ensure Request_files and subfolders exist
def ensure_request_files_structure():
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), request_files_cfg['folder'])
    os.makedirs(base, exist_ok=True)
    os.makedirs(os.path.join(base, request_files_cfg['frames_dir']), exist_ok=True)
    os.makedirs(os.path.join(base, request_files_cfg['dedup_frames_dir']), exist_ok=True)
    return base

ensure_request_files_structure()

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler('logs/modular_pipeline.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# --- FastAPI App ---
app = FastAPI(title="Pratibimb Modular Pipeline API (Content-Based)", version="2.0.0")

# --- CORS Setup ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request Models ---
class YouTubeUrlRequest(BaseModel):
    youtube_url: str

class VideoContentRequest(BaseModel):
    video_content: str  # Base64 encoded video content
    video_title: str = "Video Content"

class AudioTranscriptRequest(BaseModel):
    youtube_url: str

class FrameExtractionRequest(BaseModel):
    video_content: str  # Base64 encoded video content

class DeduplicationRequest(BaseModel):
    frames_data: List[Dict[str, Any]]  # List of frame data with base64 content
    ssim_threshold: float = 0.95

class VisualDescriptionRequest(BaseModel):
    frames_data: List[Dict[str, Any]]  # List of frame data with base64 content
    video_title: str

class MergeTranscriptRequest(BaseModel):
    audio_transcript: str
    visual_description: str

class VisualObjectsRequest(BaseModel):
    audio_transcript: str
    visual_description: str

class EnrichTranscriptRequest(BaseModel):
    merged_transcript: str
    visual_objects: List[Dict[str, Any]]

class GenerateArtRequest(BaseModel):
    visual_objects: List[Dict[str, Any]]

class AssembleDocumentRequest(BaseModel):
    transcript_content: str
    braille_art_content: str

class FinalizeRequest(BaseModel):
    final_document: str
    ascii_art: str
    braille_art: str
    tagged_transcript: str

# --- Utility Functions ---
def get_video_id(youtube_url):
    """Extract video ID from YouTube URL"""
    parsed_url = urlparse(youtube_url)
    if 'youtube.com' in parsed_url.netloc:
        query = parse_qs(parsed_url.query)
        return query.get('v', [None])[0]
    elif 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.lstrip('/')
    else:
        raise ValueError("Invalid YouTube URL format")

def create_temp_file(content: str, suffix: str = ".txt") -> str:
    """Create a temporary file with content and return the path"""
    with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False, encoding='utf-8') as f:
        f.write(content)
        return f.name

def create_temp_binary_file(content: bytes, suffix: str = ".mp4") -> str:
    """Create a temporary binary file with content and return the path"""
    with tempfile.NamedTemporaryFile(mode='wb', suffix=suffix, delete=False) as f:
        f.write(content)
        return f.name

def cleanup_temp_file(file_path: str):
    """Remove temporary file"""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
    except Exception as e:
        logging.warning(f"Failed to cleanup temp file {file_path}: {e}")

def encode_file_to_base64(file_path: str) -> str:
    """Encode file content to base64"""
    try:
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Failed to encode file to base64: {e}")
        return ""

def decode_base64_to_bytes(encoded_content: str) -> bytes:
    """Decode base64 content to bytes"""
    try:
        return base64.b64decode(encoded_content)
    except Exception as e:
        logging.error(f"Failed to decode base64 content: {e}")
        return b""

# --- API Endpoints ---

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Pratibimb Modular Pipeline API (Content-Based)",
        "version": "2.0.0",
        "total_steps": 13,
        "description": "Individual API endpoints for each step of the Braille conversion pipeline. Content-based - no file storage.",
        "endpoints": [
            "/validate-youtube-url",
            "/download-video",
            "/extract-audio-transcript",
            "/extract-video-frames",
            "/deduplicate-frames",
            "/generate-visual-descriptions",
            "/merge-audio-visual",
            "/extract-visual-objects",
            "/enrich-with-figure-tags",
            "/generate-ascii-art",
            "/generate-braille-art",
            "/assemble-final-document",
            "/finalize-output"
        ]
    }

@app.post("/validate-youtube-url")
async def validate_youtube_url(request: YouTubeUrlRequest):
    """
    Validate YouTube URL format and accessibility
    """
    try:
        # Validate URL format
        video_id = get_video_id(request.youtube_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL - could not extract video ID")
        
        logging.info(f"YouTube URL validated successfully - Video ID: {video_id}")
        
        return {
            "step": 1,
            "status": "success",
            "message": "🔍 YouTube URL validated successfully",
            "data": {
                "video_id": video_id,
                "original_url": request.youtube_url,
                "is_valid": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"URL validation failed: {str(e)}")
        return JSONResponse(
            status_code=400,
            content={
                "step": 1,
                "status": "error",
                "message": f"❌ YouTube URL validation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/download-video")
async def download_video_endpoint(request: YouTubeUrlRequest):
    """
    Download video from YouTube and save to Request_files, return only a success or error message.
    """
    try:
        logging.info(f"Starting video download from {request.youtube_url}")
        base = ensure_request_files_structure()
        video_path = os.path.join(base, request_files_cfg['video_filename'])
        # Download video
        video_path_result, video_title = download_video(request.youtube_url, video_path)
        if not video_path_result or not video_title:
            raise Exception("Video download failed - no file or title returned")
        logging.info(f"Video downloaded successfully - {video_title}")
        return {
            "step": 2,
            "status": "success",
            "message": f"🔄 Video downloaded successfully: {video_title}"
        }
    except Exception as e:
        logging.error(f"Video download failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 2,
                "status": "error",
                "message": f"❌ Video download failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/extract-audio-transcript")
async def extract_audio_transcript_endpoint(request: YouTubeUrlRequest):
    """
    Extract audio transcript from YouTube video, save to Request_files, and return transcript file and text.
    """
    try:
        logging.info("Extracting audio transcript")
        base = ensure_request_files_structure()
        video_path = os.path.join(base, request_files_cfg['video_filename'])
        transcript_path = os.path.join(base, request_files_cfg['audio_transcript_filename'])
        # Extract audio transcript
        audio_transcript = get_audio_transcript(request.youtube_url, video_path)
        # Save transcript to file
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(audio_transcript)
        logging.info("Audio transcript extracted and saved successfully")
        # Return transcript file as base64 and text
        transcript_b64 = encode_file_to_base64(transcript_path)
        return {
            "step": 3,
            "status": "success",
            "message": "🔊 Audio transcript extracted successfully",
            "data": {
                "transcript_file": transcript_b64,
                "transcript_content": audio_transcript,
                "filename": os.path.basename(transcript_path)
            }
        }
    except Exception as e:
        logging.error(f"Audio transcript extraction failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 3,
                "status": "error",
                "message": f"❌ Audio transcript extraction failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/extract-video-frames")
async def extract_video_frames_endpoint():
    """
    Extract frames from video in Request_files and return only a success message and frame count.
    """
    try:
        logging.info("Extracting video frames from Request_files video")
        base = ensure_request_files_structure()
        video_path = os.path.join(base, request_files_cfg['video_filename'])
        frames_dir = os.path.join(base, request_files_cfg['frames_dir'])
        import shutil
        if os.path.exists(frames_dir):
            shutil.rmtree(frames_dir)
        os.makedirs(frames_dir, exist_ok=True)
        extract_frames(video_path, frames_dir)
        frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.jpg')])
        frame_count = len(frame_files)
        logging.info(f"{frame_count} frames extracted successfully and saved to {frames_dir}")
        return {
            "step": 4,
            "status": "success",
            "message": f"🖼️ {frame_count} video frames extracted successfully",
            "data": {
                "frame_count": frame_count
            }
        }
    except Exception as e:
        logging.error(f"Video frame extraction failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 4,
                "status": "error",
                "message": f"❌ Video frame extraction failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/deduplicate-frames")
async def deduplicate_frames_endpoint():
    """
    Remove duplicate frames using SSIM similarity and save unique frames to Request_files. Return only a success message and count.
    """
    try:
        logging.info("Deduplicating frames using SSIM in Request_files")
        base = ensure_request_files_structure()
        frames_dir = os.path.join(base, request_files_cfg['frames_dir'])
        dedup_dir = os.path.join(base, request_files_cfg['dedup_frames_dir'])
        import shutil
        if os.path.exists(dedup_dir):
            shutil.rmtree(dedup_dir)
        os.makedirs(dedup_dir, exist_ok=True)
        unique_frame_paths = deduplicate_frames(frames_dir, request_files_cfg.get('ssim_threshold', 0.95))
        unique_count = len(unique_frame_paths) if unique_frame_paths else 0
        if not unique_frame_paths:
            return {
                "step": 5,
                "status": "warning",
                "message": "⚠️ No visually distinct scenes found after deduplication",
                "data": {
                    "unique_count": 0
                }
            }
        for frame_path in unique_frame_paths:
            dest_path = os.path.join(dedup_dir, os.path.basename(frame_path))
            shutil.copy2(frame_path, dest_path)
        logging.info(f"{unique_count} unique frames identified and saved to {dedup_dir}")
        return {
            "step": 5,
            "status": "success",
            "message": f"🧹 {unique_count} unique frames identified after deduplication",
            "data": {
                "unique_count": unique_count
            }
        }
    except Exception as e:
        logging.error(f"Frame deduplication failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 5,
                "status": "error",
                "message": f"❌ Frame deduplication failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/generate-visual-descriptions")
async def generate_visual_descriptions_endpoint():
    """
    Generate visual descriptions for deduplicated frames in Request_files and respond as file and its content as string.
    """
    try:
        logging.info("Generating visual descriptions using BLIP model from Request_files")
        base = ensure_request_files_structure()
        dedup_dir = os.path.join(base, request_files_cfg['dedup_frames_dir'])
        visual_desc_path = os.path.join(base, request_files_cfg['visual_description_filename'])
        frame_files = sorted([f for f in os.listdir(dedup_dir) if f.endswith('.jpg')])
        if not frame_files:
            return {
                "step": 6,
                "status": "warning",
                "message": "⚠️ No frames available for visual description",
                "data": {
                    "description_content": "No visually distinct scenes found.",
                    "descriptions_count": 0
                }
            }
        frame_paths = [os.path.join(dedup_dir, f) for f in frame_files]
        from transformers import BlipProcessor, BlipForConditionalGeneration
        import torch
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        blip_model.to(device)
        visual_descriptions = generate_visual_descriptions(
            frame_paths, "", blip_model, blip_processor, device
        )
        description_content = "\n\n".join(visual_descriptions)
        with open(visual_desc_path, 'w', encoding='utf-8') as f:
            f.write(description_content)
        desc_b64 = encode_file_to_base64(visual_desc_path)
        logging.info(f"Visual descriptions generated for {len(frame_paths)} frames and saved to {visual_desc_path}")
        return {
            "step": 6,
            "status": "success",
            "message": f"📝 Visual descriptions generated for {len(frame_paths)} frames",
            "data": {
                "description_file": desc_b64,
                "description_content": description_content,
                "filename": os.path.basename(visual_desc_path)
            }
        }
    except Exception as e:
        logging.error(f"Visual description generation failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 6,
                "status": "error",
                "message": f"❌ Visual description generation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/merge-audio-visual")
async def merge_audio_visual_endpoint(request: MergeTranscriptRequest):
    """
    Merge audio transcript and visual descriptions and return merged content
    """
    try:
        logging.info("Merging audio transcript and visual descriptions")
        
        if not request.audio_transcript or not request.visual_description:
            raise ValueError("Both audio transcript and visual description are required")
        
        # Generate merged transcript
        merged_transcript = generate_merged_transcript(request.audio_transcript, request.visual_description)
        
        logging.info("Merged transcript generated successfully")
        
        # Attempt to delete Request_files folder after success
        try:
            base = os.path.join(os.path.dirname(os.path.abspath(__file__)), request_files_cfg['folder'])
            import shutil
            if os.path.exists(base):
                shutil.rmtree(base)
                logging.info(f"Request_files folder deleted after merge-audio-visual step.")
        except Exception as cleanup_err:
            logging.warning(f"Failed to cleanup Request_files after merge-audio-visual: {cleanup_err}")

        return {
            "step": 7,
            "status": "success",
            "message": "🔗 Audio and visual transcripts merged successfully",
            "data": {
                "merged_transcript": merged_transcript,
                "merged_length": len(merged_transcript),
                "preview": merged_transcript[:300] + "..." if len(merged_transcript) > 300 else merged_transcript
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Audio-visual merge failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 7,
                "status": "error",
                "message": f"❌ Audio-visual merge failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/extract-visual-objects")
async def extract_visual_objects_endpoint(request: VisualObjectsRequest):
    """
    Extract relevant visual objects from transcripts and return as JSON data
    """
    try:
        logging.info("Extracting relevant visual objects")
        
        if not request.audio_transcript or not request.visual_description:
            raise ValueError("Both audio transcript and visual description are required")
        
        # Extract visual objects
        visual_objects = extract_relevant_visual_objects(request.audio_transcript, request.visual_description)
        
        logging.info(f"{len(visual_objects)} visual objects extracted successfully")
        
        return {
            "step": 8,
            "status": "success",
            "message": f"🔍 {len(visual_objects)} relevant visual objects extracted",
            "data": {
                "visual_objects": visual_objects,
                "objects_count": len(visual_objects),
                "objects_preview": visual_objects[:3] if len(visual_objects) > 3 else visual_objects
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Visual objects extraction failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 8,
                "status": "error",
                "message": f"❌ Visual objects extraction failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/enrich-with-figure-tags")
async def enrich_with_figure_tags_endpoint(request: EnrichTranscriptRequest):
    """
    Enrich transcript with figure tags and return enriched content (NO temp files, only payload)
    """
    try:
        logging.info("Enriching transcript with figure tags (payload only, no temp files)")
        if not request.merged_transcript or not request.visual_objects:
            raise ValueError("Both merged transcript and visual objects are required")

        # Use the payload directly: merged_transcript (str), visual_objects (list/dict)
        transcript_str = request.merged_transcript
        # Accept both list/dict or JSON string for visual_objects
        if isinstance(request.visual_objects, str):
            objects_json = request.visual_objects
        else:
            objects_json = json.dumps(request.visual_objects)

        # Enrich transcript with figure tags (pass strings, not file paths)
        enriched_content = enrich_transcript_with_figures(transcript_str, objects_json)

        logging.info("Transcript enriched with figure tags successfully (no temp files)")
        return {
            "step": 9,
            "status": "success",
            "message": "🏷️ Transcript enriched with figure tags successfully",
            "data": {
                "enriched_transcript": enriched_content,
                "content_length": len(enriched_content),
                "preview": enriched_content[:300] + "..." if len(enriched_content) > 300 else enriched_content
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logging.error(f"Figure tag enrichment failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 9,
                "status": "error",
                "message": f"❌ Figure tag enrichment failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/generate-ascii-art")
async def generate_ascii_art_endpoint(request: GenerateArtRequest):
    """
    Generate ASCII art from visual objects and return art content
    """
    try:
        logging.info("Generating ASCII art from visual objects")
        
        if not request.visual_objects:
            raise ValueError("Visual objects are required for ASCII art generation")
        
        # Generate ASCII art
        ascii_results = generate_ascii_art_blocks(request.visual_objects)
        
        if not ascii_results:
            logging.warning("No ASCII art was generated")
            return JSONResponse(
                status_code=500,
                content={
                    "step": 10,
                    "status": "error",
                    "message": "❌ No ASCII art was generated. Check Gemini API configuration.",
                    "timestamp": datetime.now().isoformat()
                }
            )
        
        # Convert ASCII results to string format
        ascii_content_lines = []
        for fig_id, art_data in ascii_results.items():
            ascii_content_lines.append(f"ID: {fig_id}")
            ascii_content_lines.append("ASCII ART:")
            ascii_content_lines.append(art_data.get('ascii_art', ''))
            ascii_content_lines.append("---")
        
        ascii_content = "\n".join(ascii_content_lines)
        
        logging.info(f"ASCII art generated for {len(ascii_results)} objects")
        
        return {
            "step": 10,
            "status": "success",
            "message": f"🎨 ASCII art generated for {len(ascii_results)} objects",
            "data": {
                "ascii_art_content": ascii_content,
                "ascii_results": ascii_results,
                "art_blocks_count": len(ascii_results),
                "objects_processed": len(request.visual_objects)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"ASCII art generation failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 10,
                "status": "error",
                "message": f"❌ ASCII art generation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/generate-braille-art")
async def generate_braille_art_endpoint(request: GenerateArtRequest):
    """
    Convert ASCII art to Braille art and return braille content
    """
    try:
        logging.info("Converting ASCII art to Braille art")
        
        if not request.visual_objects:
            raise ValueError("Visual objects are required for Braille art generation")
        
        # Generate ASCII results first (needed for Braille conversion)
        ascii_results = generate_ascii_art_blocks(request.visual_objects)
        
        if not ascii_results:
            raise ValueError("No ASCII art available for Braille conversion")
        
        # Convert to braille using the core function
        from core.braille_art import ascii_art_to_braille
        
        braille_content_lines = []
        for fig_id, art_data in ascii_results.items():
            ascii_art = art_data.get('ascii_art', '')
            if ascii_art:
                braille_art = ascii_art_to_braille(ascii_art)
                braille_content_lines.append(f"ID: {fig_id}")
                braille_content_lines.append("BRAILLE ART:")
                braille_content_lines.append(braille_art)
                braille_content_lines.append("---")
        
        braille_content = "\n".join(braille_content_lines)
        
        logging.info(f"Braille art generated for {len(ascii_results)} objects")
        
        return {
            "step": 11,
            "status": "success",
            "message": "⠃ ASCII art converted to Braille art successfully",
            "data": {
                "braille_art_content": braille_content,
                "ascii_results": ascii_results,
                "conversion_completed": True
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Braille art generation failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 11,
                "status": "error",
                "message": f"❌ Braille art generation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/generate-braille-text")
async def generate_braille_text_endpoint(request: AssembleDocumentRequest):
    """
    Assemble final Braille document with text and art and return final content
    """
    try:
        logging.info("Assembling final Braille document")
        
        if not request.transcript_content or not request.braille_art_content:
            raise ValueError("Both transcript content and braille art content are required")
        
        # Use the content-based conversion function
        final_braille_content = convert_transcript_to_braille_with_art_from_content(
            request.transcript_content, 
            request.braille_art_content
        )
        
        file_size = len(final_braille_content.encode('utf-8'))
        
        logging.info("Final Braille document assembled successfully")
        
        return {
            "step": 12,
            "status": "success",
            "message": "📦 Final Braille document assembled successfully",
            "data": {
                "final_braille_content": final_braille_content,
                "file_size": file_size,
                "contains_text": True,
                "contains_art": True,
                "preview": final_braille_content[:300] + "..." if len(final_braille_content) > 300 else final_braille_content
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Final document assembly failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 12,
                "status": "error",
                "message": f"❌ Final document assembly failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.post("/combine-braille-text-and-art")
async def combine_braille_text_and_art_endpoint(request: FinalizeRequest):
    """
    Finalize output and prepare all downloadable content
    """
    try:
        logging.info("Finalizing output and preparing downloadable content")
        
        # Prepare all file contents
        available_files = []
        
        if request.final_document:
            available_files.append({
                "name": "Final Braille Transcript",
                "content": request.final_document,
                "size": len(request.final_document.encode('utf-8')),
                "type": "text/plain; charset=utf-8"
            })
        
        if request.tagged_transcript:
            available_files.append({
                "name": "Figure-Tagged Transcript",
                "content": request.tagged_transcript,
                "size": len(request.tagged_transcript.encode('utf-8')),
                "type": "text/plain; charset=utf-8"
            })
        
        if request.braille_art:
            available_files.append({
                "name": "Braille Art",
                "content": request.braille_art,
                "size": len(request.braille_art.encode('utf-8')),
                "type": "text/plain; charset=utf-8"
            })
        
        if request.ascii_art:
            available_files.append({
                "name": "ASCII Art",
                "content": request.ascii_art,
                "size": len(request.ascii_art.encode('utf-8')),
                "type": "text/plain; charset=utf-8"
            })
        
        logging.info("Output finalization completed")
        
        return {
            "step": 13,
            "status": "success",
            "message": "✅ Braille conversion pipeline completed successfully!",
            "data": {
                "available_files": available_files,
                "total_files": len(available_files),
                "pipeline_completed": True,
                "ready_for_download": len(available_files) > 0
            },
            "summary": {
                "process": "Full Braille conversion pipeline",
                "total_steps": 13,
                "status": "completed",
                "files_generated": len(available_files)
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logging.error(f"Output finalization failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "step": 13,
                "status": "error",
                "message": f"❌ Output finalization failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    # --- Braille in Telugu Endpoint ---
@app.post("/braille-in-telugu")
async def braille_in_telugu_endpoint(request: BrailleLangRequest):
    """
    Translate transcript to Telugu and generate final Telugu Braille document (content-based, no files).
    """
    try:
        logging.info("Translating transcript to Telugu and generating Braille (content-based)")
        if not request.transcript_content or not request.braille_art_content:
            raise ValueError("Both transcript content and braille art content are required")

        # Step 1: Translate transcript to Telugu (preserving figure tags)
        translations = translate_figure_tagged_transcript_content(request.transcript_content, lang_map={'te': 'Telugu'})
        telugu_transcript = translations.get('te', None)
        if not telugu_transcript or telugu_transcript.strip().startswith('[Translation failed'):
            raise ValueError("Telugu translation failed or not available")

        # Step 2: Generate final Telugu Braille document (content-based)
        final_braille_content = convert_transcript_to_braille_with_art_telugu_from_content(
            telugu_transcript,
            request.braille_art_content
        )
        if not final_braille_content:
            raise ValueError("Failed to generate Telugu Braille content")

        file_size = len(final_braille_content.encode('utf-8'))
        logging.info("Telugu Braille document generated successfully")
        return {
            "status": "success",
            "message": "🟣 Telugu Braille document generated successfully",
            "data": {
                "telugu_braille_content": final_braille_content,
                "telugu_transcript": telugu_transcript,
                "file_size": file_size,
                "contains_text": True,
                "contains_art": True,
                "preview": final_braille_content[:300] + "..." if len(final_braille_content) > 300 else final_braille_content
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logging.error(f"Telugu Braille generation failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"❌ Telugu Braille generation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )

# --- Braille in Kannada Endpoint ---
@app.post("/braille-in-kannada")
async def braille_in_kannada_endpoint(request: BrailleLangRequest):
    """
    Translate transcript to Kannada and generate final Kannada Braille document (content-based, no files).
    """
    try:
        logging.info("Translating transcript to Kannada and generating Braille (content-based)")
        if not request.transcript_content or not request.braille_art_content:
            raise ValueError("Both transcript content and braille art content are required")

        # Step 1: Translate transcript to Kannada (preserving figure tags)
        translations = translate_figure_tagged_transcript_content(request.transcript_content, lang_map={'kn': 'Kannada'})
        kannada_transcript = translations.get('kn', None)
        if not kannada_transcript or kannada_transcript.strip().startswith('[Translation failed'):
            raise ValueError("Kannada translation failed or not available")

        # Step 2: Generate final Kannada Braille document (content-based)
        final_braille_content = convert_transcript_to_braille_with_art_kannada_from_content(
            kannada_transcript,
            request.braille_art_content
        )
        if not final_braille_content:
            raise ValueError("Failed to generate Kannada Braille content")

        file_size = len(final_braille_content.encode('utf-8'))
        logging.info("Kannada Braille document generated successfully")
        return {
            "status": "success",
            "message": "🟢 Kannada Braille document generated successfully",
            "data": {
                "kannada_braille_content": final_braille_content,
                "kannada_transcript": kannada_transcript,
                "file_size": file_size,
                "contains_text": True,
                "contains_art": True,
                "preview": final_braille_content[:300] + "..." if len(final_braille_content) > 300 else final_braille_content
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logging.error(f"Kannada Braille generation failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"❌ Kannada Braille generation failed: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
        )


# --- Health Check Endpoints ---

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Pratibimb Modular Pipeline API (Content-Based)",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/status")
async def status_check():
    """Status check with system information"""
    return {
        "status": "operational",
        "service": "Pratibimb Modular Pipeline API (Content-Based)",
        "version": "2.0.0",
        "total_steps": 13,
        "mode": "content-based",
        "features": [
            "No local file storage",
            "Content-based requests/responses",
            "Base64 encoded file transfers",
            "Temporary file handling"
        ],
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    print("🌟 PRATIBIMB - Modular Pipeline API Server (Content-Based) 🌟")
    print("==================================================================")
    print("📍 Server will be available at: http://localhost:8001")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("🔧 Individual step endpoints available:")
    print("   • POST /validate-youtube-url")
    print("   • POST /download-video") 
    print("   • POST /extract-audio-transcript")
    print("   • POST /extract-video-frames")
    print("   • POST /deduplicate-frames")
    print("   • POST /generate-visual-descriptions")
    print("   • POST /merge-audio-visual")
    print("   • POST /extract-visual-objects")
    print("   • POST /enrich-with-figure-tags")
    print("   • POST /generate-ascii-art")
    print("   • POST /generate-braille-art")
    print("   • POST /assemble-final-document")
    print("   • POST /finalize-output")
    print("==================================================================")
    print("📋 Content-Based Features:")
    print("   • No local file storage")
    print("   • Content passed in request body")
    print("   • Files returned as content in response")
    print("   • Base64 encoding for binary data")
    print("   • Temporary file handling only")
    print("==================================================================")
    print("Press Ctrl+C to stop the server")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=False)
