#!/usr/bin/env python3
"""
🚀 Pratibimb FastAPI Server
REST API wrapper for the Pratibimb Braille converter

Exposes Pratibimb's core functionality via HTTP endpoints:
- Text to Braille conversion
- Embosser-ready formatting
- Validation and analysis
- Real-time processing status

Author: Pratibimb Development Team
Version: 1.0
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import os
import json
import uuid
import asyncio
from datetime import datetime
import logging
from contextlib import asynccontextmanager

# Import Pratibimb functions
from pratibimb import (
    text_to_braille_unicode,
    format_for_embosser,
    validate_embosser_output,
    analyze_braille_content,
    load_config,
    setup_logging,
    log_workflow_start,
    log_step_start,
    log_step_success,
    log_step_error,
    log_workflow_end
)

# Global variables for tracking conversions
active_conversions = {}
conversion_history = []
app_logger = None

# Pydantic Models
class ConversionRequest(BaseModel):
    text: str = Field(..., description="Text content to convert to Braille")
    youtube_url: Optional[str] = Field(None, description="YouTube URL (for future implementation)")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Custom configuration options")
    session_id: Optional[str] = Field(None, description="Session ID for tracking")

class ConversionResponse(BaseModel):
    success: bool
    conversion_id: str
    original_text: str
    braille_unicode: str
    embosser_brf: str
    stats: Dict[str, Any]
    analysis: Dict[str, Any]
    validation: Dict[str, Any]
    timestamp: datetime
    processing_time_ms: int

class ConversionStatus(BaseModel):
    conversion_id: str
    status: str  # 'processing', 'completed', 'failed'
    progress: int  # 0-100
    current_step: str
    message: str
    timestamp: datetime

class BulkConversionRequest(BaseModel):
    texts: List[str] = Field(..., description="List of texts to convert")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Configuration for all conversions")

class ValidationRequest(BaseModel):
    content: str = Field(..., description="Braille content to validate")
    format_type: str = Field("brf", description="Format type: 'brf' or 'unicode'")
    config: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Validation configuration")

# Initialize FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize application on startup"""
    global app_logger
    
    # Load default configuration
    config = load_config()
    
    # Setup logging
    app_logger = setup_logging(config)
    app_logger.info("🚀 Pratibimb FastAPI Server Starting...")
    app_logger.info("📋 Configuration loaded successfully")
    
    # Ensure output directories exist
    os.makedirs("output", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    yield
    
    # Cleanup on shutdown
    app_logger.info("🛑 Pratibimb FastAPI Server Shutting Down...")

app = FastAPI(
    title="Pratibimb Braille Converter API",
    description="Professional Grade 1 Braille conversion with embosser-ready output",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS middleware for web UI integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility Functions
def generate_conversion_id() -> str:
    """Generate unique conversion ID"""
    return f"conv_{uuid.uuid4().hex[:8]}"

def update_conversion_status(conversion_id: str, status: str, progress: int, step: str, message: str):
    """Update conversion status for real-time tracking"""
    active_conversions[conversion_id] = ConversionStatus(
        conversion_id=conversion_id,
        status=status,
        progress=progress,
        current_step=step,
        message=message,
        timestamp=datetime.now()
    )
    
    # Log status update
    if app_logger:
        app_logger.info(f"🔄 Conversion {conversion_id}: {status} - {step} ({progress}%) - {message}")

async def process_text_conversion(text: str, config: Dict[str, Any], conversion_id: str) -> ConversionResponse:
    """Process text conversion asynchronously"""
    start_time = datetime.now()
    
    try:
        # Step 1: Prepare input
        update_conversion_status(conversion_id, "processing", 10, "Preparing input", "Processing input text...")
        await asyncio.sleep(0.1)  # Allow status update
        
        # Step 2: Convert to Braille Unicode
        update_conversion_status(conversion_id, "processing", 30, "Converting to Braille", "Converting text to Grade 1 Braille Unicode...")
        
        # Merge with default config
        default_config = load_config()
        merged_config = {**default_config, **config}
        
        braille_text = text_to_braille_unicode(text, merged_config)
        await asyncio.sleep(0.1)
        
        # Step 3: Format for embosser
        update_conversion_status(conversion_id, "processing", 60, "Formatting for embosser", "Converting to embosser-ready BRF format...")
        
        embosser_content = format_for_embosser(braille_text, merged_config)
        await asyncio.sleep(0.1)
        
        # Step 4: Validate output
        update_conversion_status(conversion_id, "processing", 80, "Validating output", "Validating embosser format compliance...")
        
        validation_report = validate_embosser_output(embosser_content, merged_config)
        await asyncio.sleep(0.1)
        
        # Step 5: Analyze content
        update_conversion_status(conversion_id, "processing", 90, "Analyzing content", "Generating content analysis...")
        
        analysis = analyze_braille_content(braille_text, text)
        
        # Step 6: Calculate statistics
        update_conversion_status(conversion_id, "processing", 95, "Finalizing", "Calculating final statistics...")
        
        pages = embosser_content.count('\f') + 1
        lines = len([line for line in embosser_content.split('\n') if line != '\f'])
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        stats = {
            "original_characters": len(text),
            "original_words": len(text.split()),
            "braille_characters": len(braille_text),
            "embosser_pages": pages,
            "embosser_lines": lines,
            "conversion_ratio": len(braille_text) / len(text) if text else 1.0,
            "reading_time_minutes": analysis.get('reading_time_minutes', 0),
            "processing_time_ms": int(processing_time)
        }
        
        # Complete
        update_conversion_status(conversion_id, "completed", 100, "Completed", "Conversion completed successfully!")
        
        # Create response
        response = ConversionResponse(
            success=True,
            conversion_id=conversion_id,
            original_text=text,
            braille_unicode=braille_text,
            embosser_brf=embosser_content,
            stats=stats,
            analysis=analysis,
            validation=validation_report,
            timestamp=datetime.now(),
            processing_time_ms=int(processing_time)
        )
        
        # Add to history
        conversion_history.append(response)
        
        # Remove from active conversions
        if conversion_id in active_conversions:
            del active_conversions[conversion_id]
        
        return response
        
    except Exception as e:
        update_conversion_status(conversion_id, "failed", 0, "Error", f"Conversion failed: {str(e)}")
        if app_logger:
            app_logger.error(f"❌ Conversion {conversion_id} failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Conversion failed: {str(e)}")

# API Endpoints

@app.get("/")
async def root():
    """API root endpoint with welcome message"""
    return {
        "message": "🔤 Pratibimb Braille Converter API",
        "version": "1.0.0",
        "description": "Professional Grade 1 Braille conversion with embosser-ready output",
        "docs": "/docs",
        "endpoints": {
            "convert": "/api/convert",
            "status": "/api/status/{conversion_id}",
            "validate": "/api/validate",
            "config": "/api/config",
            "history": "/api/history"
        }
    }

@app.post("/api/convert", response_model=ConversionResponse)
async def convert_text(request: ConversionRequest, background_tasks: BackgroundTasks):
    """
    Convert text to Braille format with real-time processing status.
    
    Returns immediately with conversion_id for status tracking.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text content is required")
    
    conversion_id = generate_conversion_id()
    
    # Start background processing
    background_tasks.add_task(process_text_conversion, request.text, request.config or {}, conversion_id)
    
    # Return immediate response with conversion ID
    update_conversion_status(conversion_id, "processing", 5, "Starting", "Conversion initiated...")
    
    if app_logger:
        app_logger.info(f"🚀 Started conversion {conversion_id} for {len(request.text)} characters")
    
    # For demo purposes, we'll process synchronously
    # In production, you might want true async processing
    return await process_text_conversion(request.text, request.config or {}, conversion_id)

@app.get("/api/status/{conversion_id}", response_model=ConversionStatus)
async def get_conversion_status(conversion_id: str):
    """Get real-time status of a conversion process"""
    if conversion_id not in active_conversions:
        # Check if it's in history (completed)
        for conversion in conversion_history:
            if conversion.conversion_id == conversion_id:
                return ConversionStatus(
                    conversion_id=conversion_id,
                    status="completed",
                    progress=100,
                    current_step="Completed",
                    message="Conversion completed successfully",
                    timestamp=conversion.timestamp
                )
        
        raise HTTPException(status_code=404, detail="Conversion not found")
    
    return active_conversions[conversion_id]

@app.post("/api/validate")
async def validate_braille_content(request: ValidationRequest):
    """Validate Braille content for embosser compliance"""
    try:
        config = load_config()
        merged_config = {**config, **(request.config or {})}
        
        validation_report = validate_embosser_output(request.content, merged_config)
        
        return {
            "success": True,
            "format_type": request.format_type,
            "validation_report": validation_report,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        if app_logger:
            app_logger.error(f"❌ Validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@app.post("/api/bulk-convert")
async def bulk_convert_texts(request: BulkConversionRequest):
    """Convert multiple texts in batch"""
    if not request.texts:
        raise HTTPException(status_code=400, detail="At least one text is required")
    
    results = []
    
    for i, text in enumerate(request.texts):
        try:
            conversion_id = generate_conversion_id()
            result = await process_text_conversion(text, request.config or {}, conversion_id)
            results.append(result)
            
        except Exception as e:
            results.append({
                "success": False,
                "error": str(e),
                "text_index": i,
                "original_text": text[:100] + "..." if len(text) > 100 else text
            })
    
    return {
        "success": True,
        "total_texts": len(request.texts),
        "successful_conversions": len([r for r in results if r.get("success", False)]),
        "results": results,
        "timestamp": datetime.now()
    }

@app.get("/api/config")
async def get_configuration():
    """Get current configuration settings"""
    try:
        config = load_config()
        return {
            "success": True,
            "config": config,
            "timestamp": datetime.now()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load configuration: {str(e)}")

@app.get("/api/history")
async def get_conversion_history(limit: int = 20):
    """Get recent conversion history"""
    limited_history = conversion_history[-limit:] if limit > 0 else conversion_history
    
    return {
        "success": True,
        "total_conversions": len(conversion_history),
        "returned_count": len(limited_history),
        "conversions": limited_history,
        "timestamp": datetime.now()
    }

@app.get("/api/logs")
async def get_recent_logs(lines: int = 50):
    """Get recent log entries"""
    try:
        config = load_config()
        log_file = config.get('logging_settings', {}).get('log_file', 'logs/pratibimb.log')
        
        if not os.path.exists(log_file):
            return {
                "success": True,
                "message": "No log file found",
                "logs": [],
                "timestamp": datetime.now()
            }
        
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if lines > 0 else all_lines
        
        return {
            "success": True,
            "log_file": log_file,
            "total_lines": len(all_lines),
            "returned_lines": len(recent_lines),
            "logs": [line.strip() for line in recent_lines],
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read logs: {str(e)}")

@app.get("/api/download/{conversion_id}")
async def download_conversion_files(conversion_id: str, file_type: str = "brf"):
    """Download conversion output files"""
    # Find conversion in history
    conversion = None
    for conv in conversion_history:
        if conv.conversion_id == conversion_id:
            conversion = conv
            break
    
    if not conversion:
        raise HTTPException(status_code=404, detail="Conversion not found")
    
    # Create temporary file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if file_type == "brf":
        filename = f"braille_{conversion_id}_{timestamp}.brf"
        content = conversion.embosser_brf
        media_type = "text/plain"
    elif file_type == "unicode":
        filename = f"braille_{conversion_id}_{timestamp}.txt"
        content = conversion.braille_unicode
        media_type = "text/plain; charset=utf-8"
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Use 'brf' or 'unicode'")
    
    # Save to output directory
    output_path = os.path.join("output", filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return FileResponse(
        path=output_path,
        filename=filename,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "Pratibimb Braille Converter API",
        "version": "1.0.0",
        "timestamp": datetime.now(),
        "active_conversions": len(active_conversions),
        "total_conversions": len(conversion_history)
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "success": False,
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": [
                "/docs",
                "/api/convert",
                "/api/status/{conversion_id}",
                "/api/validate",
                "/api/config",
                "/api/history"
            ]
        }
    )

@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    if app_logger:
        app_logger.error(f"❌ Internal server error: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "message": "An unexpected error occurred while processing your request"
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Pratibimb FastAPI Server...")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("🔄 API Status: http://localhost:8001/health")
    print("💡 Example Usage: http://localhost:8001/")
    print("🌐 UI Available at: file:///c:/Users/bhupinder_chawla/OneDrive%20-%20Infosys%20Limited/2023/PMO/GenAi/Text2Braile/ui/index.html")
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        reload_dirs=["./"],
        log_level="info"
    )
