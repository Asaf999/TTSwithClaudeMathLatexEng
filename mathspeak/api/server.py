#!/usr/bin/env python3
"""
MathSpeak REST API Server
=========================

FastAPI-based REST API for MathSpeak TTS system.
Provides endpoints for single expression processing, batch processing,
streaming, and WebSocket support.
"""

import os
import asyncio
import tempfile
import uuid
import time
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator, Field
import uvicorn

# Import MathSpeak components
from ..core.engine import MathematicalTTSEngine, MathematicalContext
from ..core.voice_manager import VoiceManager
from ..core.security import SecurityConfig
from ..utils.user_errors import format_error

logger = logging.getLogger(__name__)

# ===========================
# Request/Response Models
# ===========================

class MathExpression(BaseModel):
    """Single math expression request"""
    expression: str = Field(..., description="LaTeX mathematical expression")
    voice: Optional[str] = Field("narrator", description="Voice role to use")
    context: Optional[str] = Field(None, description="Mathematical context")
    format: Optional[str] = Field("mp3", description="Audio output format")
    speed: Optional[float] = Field(1.0, ge=0.5, le=2.0, description="Speech speed multiplier")
    
    @validator('expression')
    def validate_expression(cls, v):
        if not v.strip():
            raise ValueError('Expression cannot be empty')
        if len(v) > 10000:
            raise ValueError('Expression too long (max 10000 characters)')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "expression": r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}",
                "voice": "narrator",
                "context": "calculus",
                "speed": 1.0
            }
        }


class BatchRequest(BaseModel):
    """Batch processing request"""
    expressions: List[MathExpression]
    output_format: Optional[str] = Field("zip", description="Output format (zip or json)")
    
    @validator('expressions')
    def validate_expressions(cls, v):
        if not v:
            raise ValueError('At least one expression required')
        if len(v) > 100:
            raise ValueError('Too many expressions (max 100)')
        return v


class ProcessingResponse(BaseModel):
    """Processing result response"""
    text: str
    context: str
    processing_time: float
    audio_url: Optional[str] = None
    unknown_commands: List[str] = []


class BatchJobResponse(BaseModel):
    """Batch job response"""
    job_id: str
    status: str
    count: int
    created_at: datetime
    
    
class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    engine: str
    cache_stats: Optional[Dict[str, Any]] = None


# ===========================
# Global State
# ===========================

class AppState:
    """Application state"""
    def __init__(self):
        self.engine: Optional[MathematicalTTSEngine] = None
        self.voice_manager: Optional[VoiceManager] = None
        self.batch_jobs: Dict[str, Dict] = {}
        self.temp_dir = Path(tempfile.gettempdir()) / "mathspeak_api"
        self.temp_dir.mkdir(exist_ok=True)

app_state = AppState()

# ===========================
# Lifespan Management
# ===========================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    # Startup
    logger.info("Starting MathSpeak API server...")
    
    # Initialize engine
    app_state.voice_manager = VoiceManager()
    app_state.engine = MathematicalTTSEngine(
        voice_manager=app_state.voice_manager,
        enable_caching=True,
        security_config=SecurityConfig(max_processing_time=30.0)
    )
    
    logger.info("MathSpeak engine initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down MathSpeak API server...")
    if app_state.engine:
        app_state.engine.shutdown()
    
    # Cleanup temp files
    for file in app_state.temp_dir.glob("*.mp3"):
        try:
            file.unlink()
        except:
            pass

# ===========================
# FastAPI App
# ===========================

app = FastAPI(
    title="MathSpeak API",
    description="Mathematical Text-to-Speech API for LaTeX expressions",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# API Endpoints
# ===========================

@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - returns API info"""
    return await health_check()


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    cache_stats = None
    if app_state.engine:
        try:
            cache_stats = app_state.engine._get_cache_stats()
        except:
            pass
    
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        engine="ready" if app_state.engine else "not initialized",
        cache_stats=cache_stats
    )


@app.post("/speak", response_class=FileResponse)
async def speak_math(expr: MathExpression):
    """Convert single math expression to speech audio file"""
    if not app_state.engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    try:
        # Process expression
        context = MathematicalContext(expr.context) if expr.context else None
        result = app_state.engine.process_latex(
            expr.expression,
            force_context=context
        )
        
        # Generate audio
        audio_file = app_state.temp_dir / f"speech_{uuid.uuid4().hex}.mp3"
        
        # For now, return a placeholder since we need the actual TTS integration
        # In production, this would call the TTS engine
        # await app_state.voice_manager.generate_audio(result, audio_file, speed=expr.speed)
        
        # Placeholder: create empty file
        audio_file.write_text("Audio would be here")
        
        return FileResponse(
            path=audio_file,
            media_type=f"audio/{expr.format}",
            filename=f"mathspeak_{int(time.time())}.{expr.format}",
            headers={
                "X-Processing-Time": str(result.processing_time),
                "X-Context": result.context
            }
        )
        
    except Exception as e:
        logger.error(f"Error processing expression: {e}")
        error_msg = format_error(e, verbose=False, use_emoji=False)
        raise HTTPException(status_code=400, detail=error_msg)


@app.post("/speak/text", response_model=ProcessingResponse)
async def speak_math_text(expr: MathExpression):
    """Convert math expression to speech text only"""
    if not app_state.engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    try:
        # Process expression
        context = MathematicalContext(expr.context) if expr.context else None
        result = app_state.engine.process_latex(
            expr.expression,
            force_context=context
        )
        
        return ProcessingResponse(
            text=result.processed,
            context=result.context,
            processing_time=result.processing_time,
            unknown_commands=result.unknown_commands
        )
        
    except Exception as e:
        logger.error(f"Error processing expression: {e}")
        error_msg = format_error(e, verbose=False, use_emoji=False)
        raise HTTPException(status_code=400, detail=error_msg)


@app.post("/speak/stream")
async def speak_math_stream(expr: MathExpression):
    """Stream audio as it's generated"""
    if not app_state.engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    async def audio_generator():
        try:
            # Process expression
            context = MathematicalContext(expr.context) if expr.context else None
            result = app_state.engine.process_latex(
                expr.expression,
                force_context=context
            )
            
            # In production, this would stream actual audio chunks
            # For now, yield text in chunks
            text = result.processed
            chunk_size = 50
            
            for i in range(0, len(text), chunk_size):
                chunk = text[i:i + chunk_size]
                yield chunk.encode()
                await asyncio.sleep(0.1)  # Simulate streaming delay
                
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield f"Error: {str(e)}".encode()
    
    return StreamingResponse(
        audio_generator(),
        media_type="audio/mpeg",
        headers={
            "X-Content-Type-Options": "nosniff",
            "Transfer-Encoding": "chunked"
        }
    )


@app.post("/batch", response_model=BatchJobResponse)
async def batch_process(
    batch: BatchRequest,
    background_tasks: BackgroundTasks
):
    """Process multiple expressions in background"""
    if not app_state.engine:
        raise HTTPException(status_code=503, detail="Engine not initialized")
    
    job_id = uuid.uuid4().hex
    
    # Create job entry
    job_info = {
        "id": job_id,
        "status": "processing",
        "count": len(batch.expressions),
        "created_at": datetime.now(),
        "results": [],
        "errors": []
    }
    app_state.batch_jobs[job_id] = job_info
    
    # Start background processing
    background_tasks.add_task(
        process_batch_job,
        job_id,
        batch.expressions
    )
    
    return BatchJobResponse(
        job_id=job_id,
        status="processing",
        count=len(batch.expressions),
        created_at=job_info["created_at"]
    )


@app.get("/batch/{job_id}")
async def get_batch_status(job_id: str):
    """Get batch job status"""
    if job_id not in app_state.batch_jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = app_state.batch_jobs[job_id]
    return {
        "job_id": job_id,
        "status": job["status"],
        "count": job["count"],
        "processed": len(job["results"]),
        "errors": len(job["errors"]),
        "created_at": job["created_at"]
    }


@app.get("/voices")
async def list_voices():
    """List available voices"""
    if not app_state.voice_manager:
        raise HTTPException(status_code=503, detail="Voice manager not initialized")
    
    # Get available voices
    voices = [
        {"name": "narrator", "description": "Default narrator voice"},
        {"name": "theorem", "description": "Authoritative theorem voice"},
        {"name": "proof", "description": "Methodical proof voice"},
        {"name": "definition", "description": "Clear definition voice"},
        {"name": "example", "description": "Conversational example voice"},
        {"name": "emphasis", "description": "Emphasized key points"},
        {"name": "warning", "description": "Warning/caution voice"}
    ]
    
    return {"voices": voices}


# ===========================
# WebSocket Support
# ===========================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time math speaking"""
    await websocket.accept()
    
    if not app_state.engine:
        await websocket.send_json({"error": "Engine not initialized"})
        await websocket.close()
        return
    
    try:
        while True:
            # Receive expression
            data = await websocket.receive_json()
            
            try:
                # Process
                expression = data.get("expression", "")
                voice = data.get("voice", "narrator")
                context = data.get("context")
                
                if context:
                    context = MathematicalContext(context)
                
                result = app_state.engine.process_latex(
                    expression,
                    force_context=context
                )
                
                # Send back result
                await websocket.send_json({
                    "type": "result",
                    "text": result.processed,
                    "context": result.context,
                    "processing_time": result.processing_time,
                    "unknown_commands": result.unknown_commands
                })
                
            except Exception as e:
                error_msg = format_error(e, verbose=False, use_emoji=False)
                await websocket.send_json({
                    "type": "error",
                    "error": error_msg
                })
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.close()


# ===========================
# Background Tasks
# ===========================

async def process_batch_job(job_id: str, expressions: List[MathExpression]):
    """Process batch job in background"""
    job = app_state.batch_jobs[job_id]
    
    try:
        for i, expr in enumerate(expressions):
            try:
                # Process expression
                context = MathematicalContext(expr.context) if expr.context else None
                result = app_state.engine.process_latex(
                    expr.expression,
                    force_context=context
                )
                
                job["results"].append({
                    "index": i,
                    "text": result.processed,
                    "context": result.context,
                    "processing_time": result.processing_time
                })
                
            except Exception as e:
                job["errors"].append({
                    "index": i,
                    "error": str(e)
                })
        
        job["status"] = "completed"
        
    except Exception as e:
        logger.error(f"Batch processing error: {e}")
        job["status"] = "failed"
        job["error"] = str(e)


# ===========================
# Main Entry Point
# ===========================

def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the API server"""
    uvicorn.run(
        "mathspeak.api.server:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    run_server(reload=True)