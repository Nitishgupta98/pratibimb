# 🔤 Pratibimb Integration Guide for FastAPI

This document explains how to integrate the Braille conversion functionality from `pratibimb.py` into your FastAPI application (`main.py`).

## 📋 Overview of Workflow

```
YouTube Video → Transcript → Enhanced for Blind → Unicode Braille → Embosser-Ready BRF
     ↑              ↑                ↑                    ↑              ↑
  main.py      main.py         main.py           pratibimb.py    pratibimb.py
```

### Current Workflow (main.py):
1. **Extract YouTube transcript** (`/get_raw_transcript`)
2. **Enhance for visually impaired** (`/get_enhance_transcript`)

### Extended Workflow (with pratibimb.py):
3. **Convert to Unicode Braille** 
4. **Generate embosser-ready BRF file**
5. **Validate Braille output**

## 🔧 Key Methods in pratibimb.py

### 1. `text_to_braille_unicode(text, config=None)`
**Purpose**: Converts English text to Grade 1 Unicode Braille characters

**Input**: 
- `text` (str): Enhanced transcript text
- `config` (dict): Configuration settings (optional)

**Output**: Unicode Braille text with proper formatting

**Features**:
- Letter-for-letter Grade 1 Braille conversion
- Handles capitalization indicators (⠠)
- Converts numbers with number indicators (⠼)
- Formats text for embosser standards (40 chars/line, 25 lines/page)
- Includes form feeds for page breaks

```python
# Example usage
enhanced_text = "Hello World! This is a test with numbers 123."
braille_unicode = text_to_braille_unicode(enhanced_text, config)
# Output: "⠠⠓⠑⠇⠇⠕ ⠠⠺⠕⠗⠇⠙⠖ ⠠⠞⠓⠊⠎ ⠊⠎ ⠁ ⠞⠑⠎⠞ ⠺⠊⠞⠓ ⠝⠥⠍⠃⠑⠗⠎ ⠼⠁⠃⠉⠲"
```

### 2. `format_for_embosser(braille_text, config=None)`
**Purpose**: Converts Unicode Braille to BRF (Braille Ready Format) ASCII encoding

**Input**: 
- `braille_text` (str): Unicode Braille text
- `config` (dict): Configuration settings (optional)

**Output**: ASCII Braille in BRF format ready for embossers

**Features**:
- Converts Unicode Braille patterns to ASCII characters
- Maintains page structure and line breaks
- Compatible with professional embossers (ViewPlus, Index, Braillo, HumanWare)
- Preserves form feeds and formatting

```python
# Example usage
unicode_braille = "⠠⠓⠑⠇⠇⠕ ⠠⠺⠕⠗⠇⠙⠖"
brf_ascii = format_for_embosser(unicode_braille, config)
# Output: " HELLO  WORLD!"  (ASCII Braille format)
```

### 3. `validate_embosser_output(content, config=None)`
**Purpose**: Validates embosser output for compliance with professional standards

**Input**: 
- `content` (str): BRF formatted content
- `config` (dict): Configuration settings (optional)

**Output**: Validation report with errors, warnings, and statistics

**Features**:
- Checks line length compliance (40 characters)
- Validates page structure (25 lines per page)
- Verifies BRF character compliance
- Provides detailed statistics and recommendations

```python
# Example usage
validation_report = validate_embosser_output(brf_content, config)
# Returns: {'valid': True/False, 'errors': [], 'warnings': [], 'stats': {...}}
```

### 4. `analyze_braille_content(braille_text, original_text="")`
**Purpose**: Generates detailed analysis of Braille content

**Input**: 
- `braille_text` (str): Unicode Braille text
- `original_text` (str): Original text for comparison (optional)

**Output**: Comprehensive analysis with statistics

**Features**:
- Character and word counts
- Reading time estimation
- Braille pattern analysis
- Conversion ratio calculation

## 🔗 FastAPI Integration

### Step 1: Add Required Imports to main.py

```python
# Add to main.py imports
import sys
import os

# Add the API directory to path to import pratibimb
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pratibimb import (
    text_to_braille_unicode,
    format_for_embosser,
    validate_embosser_output,
    analyze_braille_content,
    load_config
)
```

### Step 2: Add New API Endpoints

#### A. Convert to Unicode Braille
```python
class BrailleRequest(BaseModel):
    enhanced_text: str

@app.post("/convert_to_braille")
async def convert_to_braille(request: BrailleRequest):
    enhanced_text = request.enhanced_text
    logging.info("Received request for /convert_to_braille")
    
    try:
        # Load pratibimb configuration
        pratibimb_config = load_config()
        
        # Convert to Unicode Braille
        braille_unicode = text_to_braille_unicode(enhanced_text, pratibimb_config)
        
        # Save Unicode Braille file
        braille_folder = config['output']['folder']
        braille_path = os.path.join(braille_folder, "unicode_braille.txt")
        
        with open(braille_path, "w", encoding="utf-8") as f:
            f.write(braille_unicode)
        
        # Analyze content
        analysis = analyze_braille_content(braille_unicode, enhanced_text)
        
        return {
            "unicode_braille": braille_unicode,
            "braille_file": FileResponse(braille_path, media_type='text/plain', filename="unicode_braille.txt"),
            "analysis": analysis
        }
    
    except Exception as e:
        logging.error(f"Failed to convert to Braille: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to convert to Braille: {str(e)}"
        })
```

#### B. Generate Embosser-Ready BRF
```python
class EmbosserRequest(BaseModel):
    unicode_braille: str

@app.post("/generate_embosser_file")
async def generate_embosser_file(request: EmbosserRequest):
    unicode_braille = request.unicode_braille
    logging.info("Received request for /generate_embosser_file")
    
    try:
        # Load pratibimb configuration
        pratibimb_config = load_config()
        
        # Convert to embosser-ready format
        brf_content = format_for_embosser(unicode_braille, pratibimb_config)
        
        # Save BRF file
        embosser_folder = config['output']['folder']
        embosser_path = os.path.join(embosser_folder, "embosser_ready.brf")
        
        with open(embosser_path, "w", encoding="utf-8") as f:
            f.write(brf_content)
        
        # Validate embosser output
        validation_report = validate_embosser_output(brf_content, pratibimb_config)
        
        return {
            "brf_content": brf_content,
            "embosser_file": FileResponse(embosser_path, media_type='text/plain', filename="embosser_ready.brf"),
            "validation": validation_report
        }
    
    except Exception as e:
        logging.error(f"Failed to generate embosser file: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to generate embosser file: {str(e)}"
        })
```

#### C. Complete Braille Workflow
```python
@app.post("/complete_braille_workflow")
async def complete_braille_workflow(request: TranscriptRequest):
    url = request.youtube_url
    logging.info(f"Received request for complete Braille workflow with URL: {url}")
    
    try:
        # Step 1: Get raw transcript
        raw_transcript = get_youtube_transcript(url)
        if raw_transcript.startswith("Error"):
            raise ValueError(raw_transcript)
        
        # Step 2: Enhance for blind users
        enhanced_text = enhance_transcript_for_blind_users(raw_transcript)
        
        # Step 3: Convert to Unicode Braille
        pratibimb_config = load_config()
        unicode_braille = text_to_braille_unicode(enhanced_text, pratibimb_config)
        
        # Step 4: Generate embosser-ready BRF
        brf_content = format_for_embosser(unicode_braille, pratibimb_config)
        
        # Step 5: Save all files
        output_folder = config['output']['folder']
        
        # Save files
        raw_path = os.path.join(output_folder, "raw_transcript.txt")
        enhanced_path = os.path.join(output_folder, "enhanced_transcript.txt")
        braille_path = os.path.join(output_folder, "unicode_braille.txt")
        embosser_path = os.path.join(output_folder, "embosser_ready.brf")
        
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(raw_transcript)
        with open(enhanced_path, "w", encoding="utf-8") as f:
            f.write(enhanced_text)
        with open(braille_path, "w", encoding="utf-8") as f:
            f.write(unicode_braille)
        with open(embosser_path, "w", encoding="utf-8") as f:
            f.write(brf_content)
        
        # Step 6: Analyze and validate
        analysis = analyze_braille_content(unicode_braille, enhanced_text)
        validation = validate_embosser_output(brf_content, pratibimb_config)
        
        return {
            "raw_transcript": raw_transcript,
            "enhanced_text": enhanced_text,
            "unicode_braille": unicode_braille,
            "brf_content": brf_content,
            "files": {
                "raw_transcript_file": raw_path,
                "enhanced_file": enhanced_path,
                "braille_file": braille_path,
                "embosser_file": embosser_path
            },
            "analysis": analysis,
            "validation": validation
        }
    
    except Exception as e:
        logging.error(f"Complete Braille workflow failed: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Complete Braille workflow failed: {str(e)}"
        })
```

### Step 3: Update React Frontend

Add new endpoints to your `environment.json`:

```json
{
  "apiBaseUrl": "http://localhost:8000",
  "endpoints": {
    "processTranscript": "/process_transcript",
    "getRawTranscript": "/get_raw_transcript", 
    "getEnhanceTranscript": "/get_enhance_transcript",
    "convertToBraille": "/convert_to_braille",
    "generateEmbosserFile": "/generate_embosser_file",
    "completeBrailleWorkflow": "/complete_braille_workflow"
  }
}
```

## 📊 Configuration

Create a `config.json` file for pratibimb settings:

```json
{
  "braille_settings": {
    "tab_width": 4,
    "preserve_line_breaks": true,
    "skip_carriage_returns": true
  },
  "embosser_settings": {
    "line_length": 40,
    "page_length": 25,
    "include_page_numbers": true,
    "tab_spaces": 2,
    "validate_output": true
  }
}
```

## 🎯 Usage Examples

### Complete Workflow
```javascript
// React frontend - Complete Braille generation
const handleCompleteBrailleGeneration = async (youtubeUrl) => {
  const response = await fetch(`${environment.apiBaseUrl}/complete_braille_workflow`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ youtube_url: youtubeUrl })
  });
  
  const result = await response.json();
  // result contains: raw_transcript, enhanced_text, unicode_braille, brf_content, files, analysis, validation
};
```

### Step-by-Step Workflow
```javascript
// Step 1: Get enhanced transcript (existing)
const enhanced = await getEnhancedTranscript(youtubeUrl);

// Step 2: Convert to Braille
const brailleResponse = await fetch(`${environment.apiBaseUrl}/convert_to_braille`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ enhanced_text: enhanced.enhanced_text })
});

// Step 3: Generate embosser file
const embosserResponse = await fetch(`${environment.apiBaseUrl}/generate_embosser_file`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ unicode_braille: brailleResult.unicode_braille })
});
```

## 🔍 Key Benefits of Integration

1. **Complete Accessibility Workflow**: YouTube → Enhanced Text → Unicode Braille → Embosser-Ready
2. **Professional Standards**: Meets all Braille embosser requirements
3. **Quality Validation**: Automatic validation and analysis
4. **Multiple Output Formats**: Unicode Braille for display, BRF for printing
5. **Comprehensive Analysis**: Reading time, statistics, compliance reports

## 📁 File Outputs

After integration, your API will generate:
- `raw_transcript.txt` - Original YouTube transcript
- `enhanced_transcript.txt` - Enhanced for visually impaired
- `unicode_braille.txt` - Unicode Braille for display
- `embosser_ready.brf` - Professional embosser file

This creates a complete accessibility pipeline from YouTube videos to professional Braille output! 🌟
