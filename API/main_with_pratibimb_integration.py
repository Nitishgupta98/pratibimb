# 🔤 Enhanced main.py with Pratibimb Integration
# This is an example of how to integrate pratibimb.py methods into your existing FastAPI application

# Add these imports to your existing main.py
import sys
import os

# Add the current directory to path to import pratibimb
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pratibimb import (
        text_to_braille_unicode,
        format_for_embosser,
        validate_embosser_output,
        analyze_braille_content,
        load_config
    )
    PRATIBIMB_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Pratibimb module not available: {e}")
    PRATIBIMB_AVAILABLE = False

# Add these new request models to your existing ones
class BrailleRequest(BaseModel):
    enhanced_text: str

class EmbosserRequest(BaseModel):
    unicode_braille: str

class ValidationRequest(BaseModel):
    brf_content: str

class AnalysisRequest(BaseModel):
    braille_text: str
    original_text: str = ""

# Add these new endpoints to your existing FastAPI app

@app.post("/convert_to_braille")
async def convert_to_braille(request: BrailleRequest):
    """
    🔤 Convert enhanced transcript text to Unicode Braille format
    
    This endpoint takes the enhanced transcript from /get_enhance_transcript
    and converts it to professional Grade 1 Unicode Braille.
    """
    if not PRATIBIMB_AVAILABLE:
        return JSONResponse(status_code=503, content={
            "error": "Braille conversion service not available"
        })
    
    enhanced_text = request.enhanced_text
    logging.info("Received request for /convert_to_braille")
    
    try:
        # Load pratibimb configuration
        pratibimb_config = load_config()
        
        logging.info("Converting text to Unicode Braille...")
        # Convert to Unicode Braille
        braille_unicode = text_to_braille_unicode(enhanced_text, pratibimb_config)
        logging.info("Unicode Braille conversion completed successfully")
        
        # Save Unicode Braille file
        braille_folder = config['output']['folder']
        if not os.path.exists(braille_folder):
            os.makedirs(braille_folder, exist_ok=True)
        
        braille_path = os.path.join(braille_folder, "unicode_braille.txt")
        with open(braille_path, "w", encoding="utf-8") as f:
            f.write(braille_unicode)
        
        # Analyze content
        analysis = analyze_braille_content(braille_unicode, enhanced_text)
        
        logging.info("Returning Unicode Braille conversion response")
        return {
            "unicode_braille": braille_unicode,
            "braille_file": FileResponse(braille_path, media_type='text/plain', filename="unicode_braille.txt"),
            "analysis": {
                "total_characters": analysis['character_count'],
                "lines": analysis['line_count'],
                "words": analysis['word_count'],
                "reading_time_minutes": analysis['reading_time_minutes'],
                "conversion_ratio": analysis.get('conversion_ratio', 1.0)
            }
        }
    
    except Exception as e:
        logging.error(f"Failed to convert to Braille: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to convert to Braille: {str(e)}"
        })

@app.post("/generate_embosser_file")
async def generate_embosser_file(request: EmbosserRequest):
    """
    🖨️ Generate embosser-ready BRF file from Unicode Braille
    
    This endpoint converts Unicode Braille to ASCII BRF format
    that can be sent directly to professional Braille embossers.
    """
    if not PRATIBIMB_AVAILABLE:
        return JSONResponse(status_code=503, content={
            "error": "Braille embosser service not available"
        })
    
    unicode_braille = request.unicode_braille
    logging.info("Received request for /generate_embosser_file")
    
    try:
        # Load pratibimb configuration
        pratibimb_config = load_config()
        
        logging.info("Converting Unicode Braille to BRF format...")
        # Convert to embosser-ready format
        brf_content = format_for_embosser(unicode_braille, pratibimb_config)
        logging.info("BRF conversion completed successfully")
        
        # Save BRF file
        embosser_folder = config['output']['folder']
        if not os.path.exists(embosser_folder):
            os.makedirs(embosser_folder, exist_ok=True)
        
        embosser_path = os.path.join(embosser_folder, "embosser_ready.brf")
        with open(embosser_path, "w", encoding="utf-8") as f:
            f.write(brf_content)
        
        # Validate embosser output
        validation_report = validate_embosser_output(brf_content, pratibimb_config)
        
        logging.info("Returning embosser file generation response")
        return {
            "brf_content": brf_content,
            "embosser_file": FileResponse(embosser_path, media_type='application/x-brf', filename="embosser_ready.brf"),
            "validation": {
                "valid": validation_report['valid'],
                "ready_for_printing": validation_report['valid'],
                "total_pages": validation_report['stats']['total_pages'],
                "total_lines": validation_report['stats']['total_lines'],
                "compliance_percentage": validation_report['stats'].get('line_length_percentage', 100)
            },
            "embosser_info": {
                "format": "BRF (Braille Ready Format)",
                "compatible_embossers": ["ViewPlus Tiger", "Index Everest", "Braillo 650", "HumanWare"],
                "file_ready": True
            }
        }
    
    except Exception as e:
        logging.error(f"Failed to generate embosser file: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Failed to generate embosser file: {str(e)}"
        })

@app.post("/complete_braille_workflow")
async def complete_braille_workflow(request: TranscriptRequest):
    """
    🌟 Complete workflow: YouTube → Enhanced → Unicode Braille → Embosser BRF
    
    This is the main endpoint that handles the entire process from YouTube URL
    to professional embosser-ready Braille files.
    """
    if not PRATIBIMB_AVAILABLE:
        return JSONResponse(status_code=503, content={
            "error": "Complete Braille workflow service not available"
        })
    
    url = request.youtube_url
    logging.info(f"Received request for complete Braille workflow with URL: {url}")
    
    try:
        # Step 1: Get raw transcript
        logging.info("Step 1: Fetching YouTube transcript...")
        raw_transcript = get_youtube_transcript(url)
        if raw_transcript.startswith("Error"):
            raise ValueError(raw_transcript)
        logging.info("Raw transcript fetched successfully")
        
        # Step 2: Enhance for blind users
        logging.info("Step 2: Enhancing transcript for visually impaired users...")
        enhanced_text = enhance_transcript_for_blind_users(raw_transcript)
        logging.info("Transcript enhancement completed")
        
        # Step 3: Convert to Unicode Braille
        logging.info("Step 3: Converting to Unicode Braille...")
        pratibimb_config = load_config()
        unicode_braille = text_to_braille_unicode(enhanced_text, pratibimb_config)
        logging.info("Unicode Braille conversion completed")
        
        # Step 4: Generate embosser-ready BRF
        logging.info("Step 4: Generating embosser-ready BRF file...")
        brf_content = format_for_embosser(unicode_braille, pratibimb_config)
        logging.info("BRF file generation completed")
        
        # Step 5: Save all files
        output_folder = config['output']['folder']
        if not os.path.exists(output_folder):
            os.makedirs(output_folder, exist_ok=True)
        
        # Generate timestamped filenames for this session
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        raw_path = os.path.join(output_folder, f"raw_transcript_{timestamp}.txt")
        enhanced_path = os.path.join(output_folder, f"enhanced_transcript_{timestamp}.txt")
        braille_path = os.path.join(output_folder, f"unicode_braille_{timestamp}.txt")
        embosser_path = os.path.join(output_folder, f"embosser_ready_{timestamp}.brf")
        
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(raw_transcript)
        with open(enhanced_path, "w", encoding="utf-8") as f:
            f.write(enhanced_text)
        with open(braille_path, "w", encoding="utf-8") as f:
            f.write(unicode_braille)
        with open(embosser_path, "w", encoding="utf-8") as f:
            f.write(brf_content)
        
        # Step 6: Analyze and validate
        logging.info("Step 5: Analyzing content and validating output...")
        analysis = analyze_braille_content(unicode_braille, enhanced_text)
        validation = validate_embosser_output(brf_content, pratibimb_config)
        
        logging.info("Complete Braille workflow completed successfully")
        return {
            "workflow_completed": True,
            "youtube_url": url,
            "processing_timestamp": timestamp,
            "content": {
                "raw_transcript": raw_transcript,
                "enhanced_text": enhanced_text,
                "unicode_braille": unicode_braille,
                "brf_content": brf_content
            },
            "files": {
                "raw_transcript_file": raw_path,
                "enhanced_file": enhanced_path,
                "braille_file": braille_path,
                "embosser_file": embosser_path
            },
            "analysis": {
                "total_characters": analysis['character_count'],
                "lines": analysis['line_count'],
                "words": analysis['word_count'],
                "estimated_reading_time": f"{analysis['reading_time_minutes']:.1f} minutes",
                "conversion_ratio": analysis.get('conversion_ratio', 1.0),
                "capital_indicators": analysis['special_indicators']['capitals'],
                "number_indicators": analysis['special_indicators']['numbers']
            },
            "validation": {
                "embosser_ready": validation['valid'],
                "total_pages": validation['stats']['total_pages'],
                "compliance_status": "PASSED" if validation['valid'] else "NEEDS_REVIEW",
                "warnings_count": len(validation['warnings']),
                "errors_count": len(validation['errors'])
            },
            "next_steps": {
                "ready_for_printing": validation['valid'],
                "embosser_file": embosser_path,
                "instructions": "Send the .brf file directly to your Braille embosser"
            }
        }
    
    except Exception as e:
        logging.error(f"Complete Braille workflow failed: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Complete Braille workflow failed: {str(e)}",
            "workflow_completed": False
        })

# Add validation endpoint
@app.post("/validate_braille_output")
async def validate_braille_output(request: ValidationRequest):
    """
    🔍 Validate BRF content for embosser compliance
    """
    if not PRATIBIMB_AVAILABLE:
        return JSONResponse(status_code=503, content={
            "error": "Braille validation service not available"
        })
    
    brf_content = request.brf_content
    logging.info("Received request for /validate_braille_output")
    
    try:
        pratibimb_config = load_config()
        validation_report = validate_embosser_output(brf_content, pratibimb_config)
        
        return {
            "validation_passed": validation_report['valid'],
            "ready_for_printing": validation_report['valid'],
            "compliance_details": {
                "total_pages": validation_report['stats']['total_pages'],
                "total_lines": validation_report['stats']['total_lines'],
                "line_length_compliance": f"{validation_report['stats'].get('line_length_percentage', 100):.1f}%",
                "character_compliance": validation_report['stats']['character_compliance'],
                "ascii_braille_format": validation_report['stats'].get('ascii_braille_compliance', False)
            },
            "issues": {
                "errors": validation_report['errors'],
                "warnings": validation_report['warnings']
            },
            "professional_standards": {
                "ansi_compliant": validation_report['valid'],
                "embosser_compatible": validation_report['valid'],
                "brf_format": True
            }
        }
    
    except Exception as e:
        logging.error(f"Braille validation failed: {str(e)}")
        return JSONResponse(status_code=500, content={
            "error": f"Braille validation failed: {str(e)}"
        })

# Update your main server startup to include Pratibimb info
if __name__ == "__main__":
    import uvicorn
    logging.info("Starting Pratibimb API server...")
    print("=" * 60)
    print("🌟 PRATIBIMB - True Reflection of Digital World 🌟")
    print("Accessibility-focused YouTube transcript enhancement API")
    print("🔤 WITH PROFESSIONAL BRAILLE CONVERSION")
    print("=" * 60)
    print("📍 Server starting at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 Available endpoints:")
    print("   • POST /process_transcript - Complete processing")
    print("   • POST /get_raw_transcript - Get YouTube transcript")
    print("   • POST /get_enhance_transcript - Enhance for blind users")
    if PRATIBIMB_AVAILABLE:
        print("   • POST /convert_to_braille - Convert to Unicode Braille")
        print("   • POST /generate_embosser_file - Create BRF embosser file")
        print("   • POST /complete_braille_workflow - Full YouTube→Braille pipeline")
        print("   • POST /validate_braille_output - Validate embosser compliance")
        print("🖨️ Braille embosser support: ENABLED")
    else:
        print("⚠️ Braille conversion: DISABLED (pratibimb.py not found)")
    print("=" * 60)
    uvicorn.run(app, host="localhost", port=8000, log_level="info")
