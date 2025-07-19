import os
import shutil
import argparse
import logging
import subprocess
import multiprocessing
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from functools import partial

import torch
from PIL import Image
from tqdm import tqdm
from skimage.metrics import structural_similarity as ssim
import numpy as np

# --- Dependency Check ---
try:
    from yt_dlp import YoutubeDL
except ImportError:
    raise ImportError("yt-dlp is not installed. Please install it with 'pip install yt-dlp'")

try:
    from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
except ImportError:
    raise ImportError("youtube-transcript-api is not installed. Please install it with 'pip install youtube-transcript-api'")

try:
    from faster_whisper import WhisperModel
except ImportError:
    raise ImportError("faster-whisper is not installed. Please install it with 'pip install faster-whisper'")

try:
    from transformers import BlipProcessor, BlipForConditionalGeneration
except ImportError:
    raise ImportError("transformers is not installed. Please install it with 'pip install transformers'")

# --- Constants ---
VIDEO_FILENAME = "downloaded_video.mp4"
FRAMES_DIR = "temp_frames"
SSIM_THRESHOLD = 0.95
AUDIO_TRANSCRIPT_FILENAME = "audio_transcript.txt"
VISUAL_DESCRIPTION_FILENAME = "visual_description.txt"

# --- Setup ---
def setup_logging():
    """Configures logging for the script."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_ffmpeg():
    """Checks if ffmpeg is installed and available in the system's PATH."""
    if shutil.which("ffmpeg") is None:
        logging.error("ffmpeg not found. Please install ffmpeg and ensure it is in your system's PATH.")
        exit(1)

# --- Core Functions ---

def download_video(url: str, output_path: str) -> tuple[str, str]:
    """
    Downloads a YouTube video and returns its path and title.
    The title will be used to create context-aware prompts for captioning.
    """
    logging.info(f"Downloading video and metadata from URL: {url}")
    ydl_opts = {
        'format': 'bestvideo[height<=360]+bestaudio/best[height<=360]/best',
        'outtmpl': output_path,
        'quiet': True,
        'merge_output_format': 'mp4',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'this video')

        logging.info(f"Video downloaded successfully to {output_path}")
        logging.info(f"Extracted video title: '{video_title}'")
        return output_path, video_title
    except Exception as e:
        logging.error(f"Failed to download video: {e}")
        return None, None

def get_audio_transcript(url: str, video_path: str) -> str:
    """
    Extracts audio transcript. First tries youtube-transcript-api,
    then falls back to Whisper if unavailable. Returns a timestamped transcript.
    """
    logging.info("Attempting to fetch transcript from YouTube API...")
    try:
        video_id = parse_qs(urlparse(url).query).get("v")[0]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format with timestamps
        formatted_transcript = []
        for d in transcript_list:
            timestamp = format_seconds_to_hhmmss(d['start'])
            text = d['text'].replace('\n', ' ').strip()
            formatted_transcript.append(f"[{timestamp}] {text}")

        transcript = "\n".join(formatted_transcript)
        logging.info("Successfully fetched transcript from YouTube API.")
        return transcript
    except (TranscriptsDisabled, NoTranscriptFound, KeyError, IndexError):
        logging.warning("YouTube API transcript not available. Falling back to Whisper.")
        return transcribe_with_whisper(video_path)
    except Exception as e:
        logging.error(f"An unexpected error occurred with YouTubeTranscriptApi: {e}")
        logging.warning("Falling back to Whisper.")
        return transcribe_with_whisper(video_path)

def transcribe_with_whisper(video_path: str) -> str:
    """
    Transcribes audio from a video file using faster-whisper.
    Returns a timestamped transcript.
    """
    logging.info("Transcribing audio with Whisper. This may take a while...")
    try:
        # Using a smaller, faster model for CPU execution
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(video_path, beam_size=5)

        formatted_transcript = []
        for segment in segments:
            timestamp = format_seconds_to_hhmmss(segment.start)
            text = segment.text.strip()
            formatted_transcript.append(f"[{timestamp}] {text}")

        transcript = "\n".join(formatted_transcript)
        logging.info("Whisper transcription complete.")
        return transcript
    except Exception as e:
        logging.error(f"Failed to transcribe audio with Whisper: {e}")
        return "Audio transcription failed."

def extract_frames(video_path: str, output_dir: str):
    """Extracts frames from a video at 1 frame per second using ffmpeg."""
    logging.info(f"Extracting frames from {video_path} to {output_dir}...")
    output_dir_path = Path(output_dir)
    if output_dir_path.exists():
        shutil.rmtree(output_dir_path)
    output_dir_path.mkdir(parents=True)

    command = [
        'ffmpeg',
        '-i', video_path,
        '-vf', 'fps=1',
        '-q:v', '2', # High quality JPEGs
        f'{output_dir_path}/frame_%06d.jpg' # Use JPG for smaller size
    ]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("Frame extraction complete.")
    except subprocess.CalledProcessError as e:
        logging.error(f"ffmpeg error during frame extraction: {e.stderr}")
        exit(1)

def get_image_grayscale(image_path: str) -> np.ndarray:
    """Reads an image and converts it to grayscale."""
    with Image.open(image_path) as img:
        return np.array(img.convert("L"))

def _process_dedup_chunk(frame_paths_chunk: list[str], threshold: float) -> list[str]:
    """
    Processes a single chunk of frames for deduplication.
    This function is run by each worker process. It finds unique frames *within* its chunk.
    """
    if not frame_paths_chunk:
        return []

    local_unique_paths = [frame_paths_chunk[0]]
    last_unique_frame_data = get_image_grayscale(frame_paths_chunk[0])

    for frame_path in frame_paths_chunk[1:]:
        current_frame_data = get_image_grayscale(frame_path)

        if last_unique_frame_data.shape != current_frame_data.shape:
            h, w = last_unique_frame_data.shape
            current_frame_data = np.array(Image.fromarray(current_frame_data).resize((w, h)))

        similarity = ssim(last_unique_frame_data, current_frame_data, data_range=255)

        if similarity < threshold:
            local_unique_paths.append(frame_path)
            last_unique_frame_data = current_frame_data
    
    return local_unique_paths

def deduplicate_frames(frames_dir: str, threshold: float) -> list[str]:
    """
    Deduplicates frames based on Structural Similarity Index (SSIM) using multiprocessing.
    Returns a list of paths to unique frames.
    """
    logging.info("Deduplicating frames using SSIM with multiprocessing...")
    frame_files = sorted([str(p) for p in Path(frames_dir).glob('*.jpg')])
    if not frame_files:
        logging.warning("No frames found to deduplicate.")
        return []

    num_workers = multiprocessing.cpu_count()
    # Ensure chunk_size is at least 1 and chunks are distributed evenly
    chunk_size = (len(frame_files) + num_workers - 1) // num_workers
    chunks = [frame_files[i:i + chunk_size] for i in range(0, len(frame_files), chunk_size)]

    process_chunk_with_threshold = partial(_process_dedup_chunk, threshold=threshold)

    with multiprocessing.Pool(processes=num_workers) as pool:
        chunk_results = list(tqdm(pool.imap(process_chunk_with_threshold, chunks), total=len(chunks), desc="Deduplicating Chunks"))

    logging.info("Merging results and handling chunk boundaries...")
    unique_frames = []
    if not chunk_results:
        return []

    # Add all unique frames from the first chunk
    unique_frames.extend(chunk_results[0])
    
    # Process subsequent chunks, checking boundaries
    for i in range(1, len(chunk_results)):
        if not unique_frames or not chunk_results[i]:
            continue

        prev_chunk_last_unique_path = unique_frames[-1]
        curr_chunk_first_unique_path = chunk_results[i][0]

        last_img = get_image_grayscale(prev_chunk_last_unique_path)
        curr_img = get_image_grayscale(curr_chunk_first_unique_path)
        
        if last_img.shape != curr_img.shape:
            h, w = last_img.shape
            curr_img = np.array(Image.fromarray(curr_img).resize((w, h)))

        if ssim(last_img, curr_img, data_range=255) >= threshold:
            # They are similar, so discard the first frame of the current chunk
            chunk_results[i].pop(0)
        
        unique_frames.extend(chunk_results[i])

    # Delete the duplicate frames from disk
    all_original_paths = set(frame_files)
    final_unique_paths = set(unique_frames)
    paths_to_delete = all_original_paths - final_unique_paths

    for path in tqdm(paths_to_delete, desc="Deleting duplicate frames"):
        try:
            os.remove(path)
        except OSError as e:
            logging.warning(f"Could not delete duplicate frame {path}: {e}")

    logging.info(f"Found {len(unique_frames)} unique frames out of {len(frame_files)} total frames.")
    return sorted(list(final_unique_paths))

def format_seconds_to_hhmmss(seconds: float) -> str:
    """Formats seconds into HH:MM:SS string."""
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def get_timestamp_from_frame(frame_path: str) -> str:
    """Extracts the second from the frame filename and formats it as HH:MM:SS."""
    try:
        # e.g., 'temp_frames/frame_000123.jpg' -> 123
        # ffmpeg starts frame numbering at 1, so second 0 is frame 1.
        frame_number = int(Path(frame_path).stem.split('_')[-1])
        seconds = frame_number - 1
        return format_seconds_to_hhmmss(seconds)
    except (IndexError, ValueError):
        logging.warning(f"Could not parse timestamp from {frame_path}. Defaulting to 00:00:00.")
        return "00:00:00"

def generate_visual_descriptions(frame_paths: list[str], video_title: str, model, processor, device) -> list[str]:
    """Generates detailed captions for a list of image frames using BLIP."""
    descriptions = []
    # The original prompt was an instruction, which doesn't work well with this model.
    # A simple, descriptive prefix like "a photo of" is much more effective for captioning.
    # This allows the model to complete the sentence with a description of the image.
    prompt = f""
    logging.info(f"Using prompt for captioning: '{prompt}' (Video context: '{video_title}')")

    for frame_path in tqdm(frame_paths, desc="Generating Visual Descriptions"):
        try:
            raw_image = Image.open(frame_path).convert('RGB')
            
            # For conditional captioning, we provide the image and the prefix text.
            inputs = processor(raw_image, text=prompt, return_tensors="pt").to(device)
            out = model.generate(**inputs, max_new_tokens=50)
            # The output includes the prompt, so we decode the full sequence.
            caption = processor.decode(out[0], skip_special_tokens=True)
            
            timestamp = get_timestamp_from_frame(frame_path)
            descriptions.append(f"[{timestamp}] {caption.capitalize()}")
        except Exception as e:
            logging.error(f"Could not generate caption for {frame_path}: {e}")
            continue
            
    return descriptions

def save_output(filename: str, content: str | list[str]):
    """Saves content to a text file."""
    logging.info(f"Saving output to {filename}")
    with open(filename, 'w', encoding='utf-8') as f:
        if isinstance(content, list):
            f.write('\n'.join(content))
        else:
            f.write(content)
    logging.info("File saved successfully.")

def cleanup(paths: list[str]):
    """Removes temporary files and directories."""
    logging.info("Cleaning up temporary files...")
    for path in paths:
        path_obj = Path(path)
        if path_obj.is_dir():
            shutil.rmtree(path_obj, ignore_errors=True)
        elif path_obj.is_file():
            path_obj.unlink(missing_ok=True)
    logging.info("Cleanup complete.")

def main():
    """Main function to run the YouTube analysis pipeline."""
    parser = argparse.ArgumentParser(description="Analyze a YouTube video for audio and visual content.")
    parser.add_argument("url", type=str, help="The URL of the YouTube video.")
    args = parser.parse_args()

    setup_logging()
    check_ffmpeg()

    temp_paths_to_clean = [VIDEO_FILENAME, FRAMES_DIR]

    try:
        # 1. Download Video
        video_path, video_title = download_video(args.url, VIDEO_FILENAME)
        if not video_path or not video_title:
            return  # Exit if download fails

        # 2. Get Audio Transcript
        audio_transcript = get_audio_transcript(args.url, video_path)
        save_output(AUDIO_TRANSCRIPT_FILENAME, audio_transcript)

        # 3. Extract Frames
        extract_frames(video_path, FRAMES_DIR)

        # 4. Deduplicate Frames
        unique_frame_paths = deduplicate_frames(FRAMES_DIR, SSIM_THRESHOLD)
        if not unique_frame_paths:
            logging.warning("No unique frames were found. Skipping visual description.")
            save_output(VISUAL_DESCRIPTION_FILENAME, "No visually distinct scenes found.")
            return

        # 5. Generate Visual Descriptions
        logging.info("Initializing BLIP model for image captioning...")
        # Use float32 for CPU, as float16 is not well-supported and can be slower.
        blip_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        blip_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        blip_model.to(device)
        logging.info(f"BLIP model loaded on device: {device}")

        visual_descriptions = generate_visual_descriptions(
            unique_frame_paths, video_title, blip_model, blip_processor, device
        )
        
        # 6. Save Visual Descriptions
        save_output(VISUAL_DESCRIPTION_FILENAME, visual_descriptions)

        logging.info(f"Analysis complete! Check the output files: {AUDIO_TRANSCRIPT_FILENAME} and {VISUAL_DESCRIPTION_FILENAME}")

    except Exception as e:
        logging.error(f"An unexpected error occurred in the main pipeline: {e}", exc_info=True)
    finally:
        # Cleanup
        cleanup(temp_paths_to_clean)

if __name__ == "__main__":
    main()