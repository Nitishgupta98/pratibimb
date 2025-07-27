
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
import json
from dotenv import load_dotenv
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

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError("google-generativeai is not installed. Please install it with 'pip install google-generativeai'")

# --- Gemini API Setup ---
load_dotenv()  # This loads variables from .env into the environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env file")
genai.configure(api_key=GEMINI_API_KEY)

try:
    from concurrent.futures import ThreadPoolExecutor, as_completed
except ImportError:
    raise ImportError("concurrent.futures is not available. This is a standard library module in Python 3.2 and later.")

try:
    from translation_utils import translate_figure_tagged_transcript
except ImportError as e:
    raise ImportError("translation_utils module not found. Ensure it is in the same directory as this script.")

# --- Constants ---
VIDEO_FILENAME = "downloaded_video.mp4"
FRAMES_DIR = "temp_frames"
SSIM_THRESHOLD = 0.95
AUDIO_TRANSCRIPT_FILENAME = "output/audio_transcript.txt"
VISUAL_DESCRIPTION_FILENAME = "output/visual_description.txt"
MERGED_TRANSCRIPT_FILENAME = "output/merged_audio_visual_transcript.txt"
VISUAL_OBJECTS_FILENAME = "output/relevant_visual_objects.json"
FIGURE_TAGGED_TRANSCRIPT_FILENAME = "output/transcript_with_figure_tags.txt"

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
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        transcript_list = fetched_transcript.to_raw_data()
        
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

def process_single_frame(frame_path, prompt, model, processor, device):
    try:
        raw_image = Image.open(frame_path).convert('RGB')
        inputs = processor(raw_image, text=prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=50)
        caption = processor.decode(out[0], skip_special_tokens=True)
        timestamp = get_timestamp_from_frame(frame_path)
        return f"[{timestamp}] {caption.capitalize()}"
    except Exception as e:
        logging.error(f"Could not generate caption for {frame_path}: {e}")
        return None

def generate_visual_descriptions(frame_paths: list[str], video_title: str, model, processor, device, max_workers=4) -> list[str]:
    """Generates detailed captions for a list of image frames using BLIP in parallel."""
    descriptions = []
    prompt = ""  # Leave empty or dynamically generate
    logging.info(f"Using prompt for captioning: '{prompt}' (Video context: '{video_title}')")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_frame = {
            executor.submit(process_single_frame, frame, prompt, model, processor, device): frame
            for frame in frame_paths
        }

        for future in tqdm(as_completed(future_to_frame), total=len(frame_paths), desc="Generating Visual Descriptions"):
            result = future.result()
            if result:
                descriptions.append(result)

    return descriptions


def generate_merged_transcript(audio_transcript_path: str, visual_description_path: str) -> str:
    """
    Merges audio and visual transcripts into a single, enhanced narrative using the Gemini API.

    This function reads the content from the audio and visual transcript files,
    sends them to the Gemini 2.5 Pro model with a specialized prompt, and returns
    a single, formatted string that is accessible for visually impaired users.

    Note:
        This function requires the GOOGLE_API_KEY environment variable to be set.
        For very large files, the combined content might exceed the API's context
        limit. This implementation does not currently handle chunking.

    Args:
        audio_transcript_path (str): Path to the audio transcript file.
        visual_transcript_path (str): Path to the visual description file.

    Returns:
        str: The enhanced, merged transcript as a single string.
    """
    logging.info("Generating merged audio-visual transcript with Gemini 2.5 Pro...")
    # if "GOOGLE_API_KEY" not in os.environ:
    #     logging.error("GOOGLE_API_KEY environment variable not set. Cannot generate merged transcript.")
    #     return "Merged transcript generation failed: GOOGLE_API_KEY is not configured."

    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
    except Exception as e:
        logging.error(f"Failed to configure or initialize Gemini model: {e}")
        return f"Merged transcript generation failed: {e}"

    try:
        with open(audio_transcript_path, 'r', encoding='utf-8') as f:
            audio_content = f.read()
        with open(visual_description_path, 'r', encoding='utf-8') as f:
            visual_content = f.read()
    except FileNotFoundError as e:
        logging.error(f"Could not read input files for merging: {e}")
        return f"Merged transcript generation failed: {e}"

    prompt = f"""Your task is to merge a raw transcript of a spoken YouTube video with visual descriptions so that it is clear, engaging, and suitable for blind and visually impaired readers. The merged version will be used for Braille transcription and should be plain text only.

        Follow these exact instructions:

        1. Begin with a one-line title that clearly summarizes the topic of the video. Do not mention accessibility or visual impairment.
        2. Rewrite the transcript into clean, fluent, and simple language that follows a natural storytelling style. Assume the reader has no prior knowledge of the topic.
        3. Remove all informal chatter, greetings, personal comments, side conversations, and sound effects. Stay focused on the actual content and ideas.
        4. **Do not include any visual references** like “see this”, “look here”, “as shown above”, “picture this”, or “watch closely”. If a visual element contains information essential to understanding (e.g., a diagram of the moon phases), describe it concisely in plain language — otherwise ignore it.
        5. If a visual transcript is available, use it **only if it adds new, meaningful information that is not already stated in the audio**. Do not duplicate what's already explained verbally.
        6. Avoid any formatting such as bullet points, asterisks, emojis, markdown, or code.
        7. The output should be readable aloud and easy to follow — as if someone is narrating the content clearly for someone who can’t see or rewind.

        Only use the transcript(s) provided and do not add your own facts, opinions, or examples. Just make the original video content more readable, smooth, and understandable.

        --- AUDIO TRANSCRIPT ---
        {audio_content}

        --- VISUAL DESCRIPTIONS ---
        {visual_content}
        """

    try:
        response = model.generate_content(prompt)
        merged_transcript = response.text
        logging.info("Successfully generated merged audio-visual transcript.")
        return merged_transcript
    except Exception as e:
        logging.error(f"An error occurred while calling the Gemini API: {e}")
        return f"Merged transcript generation failed due to an API error: {e}"

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


def extract_relevant_visual_objects(audio_transcript_path: str, visual_transcript_path: str) -> list[dict]:
    """
    Uses Gemini to extract relevant visual objects with descriptions for Braille representation.

    :param audio_transcript_path: Path to audio transcript text file.
    :param visual_transcript_path: Path to visual transcript text file.
    :return: List of dicts with keys: 'timestamp', 'object', 'description', 'relevance'
    """
    logging.info("Extracting relevant visual objects using Gemini...")

    try:
        with open(audio_transcript_path, 'r', encoding='utf-8') as f:
            audio_content = f.read()
        with open(visual_transcript_path, 'r', encoding='utf-8') as f:
            visual_content = f.read()
    except Exception as e:
        logging.error(f"Could not read transcript files: {e}")
        return []

    prompt = f"""
        You are an AI assistant helping design accessible educational content for blind users.
        You are given two transcripts:

        AUDIO TRANSCRIPT:
        {audio_content}

        VISUAL TRANSCRIPT:
        {visual_content}

        Based on the context of the video, extract a chronological list of meaningful visual objects or concepts that can be represented as Braille art.

        For each object, return:
        - the timestamp (from the visual transcript),
        - the name of the object or concept,
        - a short description of why it matters,
        - and a relevance tag ("critical", "high", "medium").

        Ignore unrelated objects like desks, people, or background items unless they support the explanation.

        Output the result as JSON in the following format:
        [
        {{
            "id": "Fig_1",
            "timestamp": "00:00:21",
            "object": "Telescope",
            "description": "Used to introduce the concept of observing the moon in the sky.",
            "relevance": "high"
        }},
        ...
        ]
        """

    try:
        model = genai.GenerativeModel('gemini-2.5-pro')
        response = model.generate_content(prompt)
        response_text = response.text

        # Try to extract JSON from the response robustly
        json_start = response_text.find('[')
        json_end = response_text.rfind(']')
        if json_start == -1 or json_end == -1:
            logging.error("Could not find JSON array in Gemini response.")
            return []
        json_data = response_text[json_start:json_end+1]
        visual_objects = json.loads(json_data)
        logging.info(f"Extracted {len(visual_objects)} relevant visual objects.")
        return visual_objects

    except Exception as e:
        logging.error(f"Error extracting relevant visual objects: {e}")
        return []

def enrich_transcript_with_figures(
    enhanced_transcript_path: str,
    objects_json_path: str,
    output_path: str,
    ) -> None:
    """
    Enriches a transcript with inline object figure tags based on context.

    Parameters:
        enhanced_transcript_path: Path to the cleaned full transcript (no timestamps, ready for user).
        objects_json_path: Path to the JSON list of visual objects (with id, name, description).
        output_path: File to write enriched transcript to.

    Returns:
        None – Writes the enriched transcript to disk.
    """

    # Load inputs
    with open(enhanced_transcript_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    with open(objects_json_path, 'r', encoding='utf-8') as f:
        objects = json.load(f)

    # Final production-safe Gemini prompt
    prompt = f"""
        You are an accessibility AI assistant helping adapt educational content for visually impaired users.

        You are given:
        - A plain English transcript of an educational video
        - A list of important visual objects (e.g., diagrams, scenes, labeled images) with a unique ID and description

        Your task:
        - Carefully read the transcript
        - Identify semantically appropriate locations to insert figure references inline
        - For each object, insert it in this format:
        [Fig_1: Lunar Cycle Diagram]

        Guidelines:
        - Insert each figure reference **only once**, at the **most relevant** position
        - The insertion must be **natural**, helpful, and not interrupt the reading flow
        - Do **not** add explanations — only insert the tag
        - Preserve the original structure of the transcript as much as possible

        --- Transcript:
        {transcript_text}

        --- Visual Objects:
        {json.dumps(objects, indent=2)}
        """

    # Send to Gemini API
    try:
        model = genai.GenerativeModel("gemini-2.5-pro")
        response = model.generate_content(prompt)

        enriched_text = response.text.strip()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enriched_text)

        print(f"✅ Enriched transcript saved to: {output_path}")

    except Exception as e:
        print("❌ Gemini API enrichment failed:", str(e))


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


        # 7. Generate Merged Audio-Visual Transcript
        merged_transcript = generate_merged_transcript(
            AUDIO_TRANSCRIPT_FILENAME,
            VISUAL_DESCRIPTION_FILENAME
        )

        save_output(MERGED_TRANSCRIPT_FILENAME, merged_transcript)
        logging.info(f"Merged audio-visual transcript saved to {MERGED_TRANSCRIPT_FILENAME}")

        # 8. Extract Relevant Visual Objects
        visual_objects = extract_relevant_visual_objects(AUDIO_TRANSCRIPT_FILENAME, VISUAL_DESCRIPTION_FILENAME)
        with open(VISUAL_OBJECTS_FILENAME, 'w', encoding='utf-8') as f:
            json.dump(visual_objects, f, indent=2)
        logging.info(f"Relevant visual objects saved to {VISUAL_OBJECTS_FILENAME}")

        # 9. Insert Figure Tags into Transcript
        enrich_transcript_with_figures(MERGED_TRANSCRIPT_FILENAME, VISUAL_OBJECTS_FILENAME, FIGURE_TAGGED_TRANSCRIPT_FILENAME)
        logging.info(f"Transcript with figure tags saved to {FIGURE_TAGGED_TRANSCRIPT_FILENAME}")

        # 10. Translate the figure-tagged transcript to Telugu and Kannada
        translate_figure_tagged_transcript(FIGURE_TAGGED_TRANSCRIPT_FILENAME)

        #logging.info(f"Analysis complete! Check the output files: {AUDIO_TRANSCRIPT_FILENAME}, {VISUAL_DESCRIPTION_FILENAME}, and {ENHANCED_TRANSCRIPT_FILENAME}")

    except Exception as e:
        logging.error(f"An unexpected error occurred in the main pipeline: {e}", exc_info=True)
    finally:
        # Cleanup
        cleanup(temp_paths_to_clean)

if __name__ == "__main__":
    main()