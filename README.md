# YouTube Video Analyzer

This script downloads a YouTube video, transcribes its audio, and generates a timestamped visual description of its scenes.

## Features

-   **Video Download**: Uses `yt-dlp` to download the best quality MP4 video.
-   **Audio Transcription**:
    -   First attempts to use the official `youtube-transcript-api` for fast and accurate transcripts.
    -   Falls back to `faster-whisper` (a CPU-optimized version of OpenAI's Whisper) if the API transcript is unavailable.
-   **Visual Analysis**:
    -   Extracts frames from the video at 1 frame per second using `ffmpeg`.
    -   **Deduplicates frames** using the Structural Similarity Index (SSIM) to identify visually distinct scenes.
    -   Generates detailed captions for each unique scene using the **BLIP** image captioning model.
-   **Outputs**:
    1.  `audio_transcript.txt`: The full audio transcript.
    2.  `visual_description.txt`: Timestamped descriptions of unique visual scenes.

## Prerequisites

1.  **Python 3.8+**
2.  **FFmpeg**: You must have `ffmpeg` installed and accessible in your system's PATH.
    -   **Windows**: Download from ffmpeg.org and add the `bin` folder to your PATH.
    -   **macOS (using Homebrew)**: `brew install ffmpeg`
    -   **Linux (using apt)**: `sudo apt update && sudo apt install ffmpeg`

## Setup

1.  **Clone the repository or save the files:**
    Save `youtube_analyzer.py`, `requirements.txt`, and this `README.md` to a new directory.

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required Python libraries:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the script from your terminal, providing the YouTube video URL as an argument.

```bash
python youtube_analyzer.py "YOUTUBE_VIDEO_URL_HERE"
```

The script will log its progress to the console. Once complete, you will find `audio_transcript.txt` and `visual_description.txt` in the same directory. Temporary files are automatically cleaned up.