"""FastAPI application for MathSpeak Clean Architecture."""

import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from mathspeak_clean.application.use_cases.process_expression import (
    ProcessExpressionRequest,
    ProcessExpressionUseCase,
)
from mathspeak_clean.infrastructure.config.settings import get_settings
from mathspeak_clean.infrastructure.container import get_container
from mathspeak_clean.infrastructure.logging.logger import get_logger
from mathspeak_clean.shared.exceptions import MathSpeakError
from mathspeak_clean.shared.types import AudienceLevel

logger = get_logger(__name__)


# Pydantic models for API
class ProcessRequest(BaseModel):
    """Request model for processing endpoint."""
    
    latex: str = Field(..., description="LaTeX mathematical expression")
    audience_level: AudienceLevel = Field(
        "undergraduate",
        description="Target audience level"
    )
    use_cache: bool = Field(True, description="Whether to use cache")


class ProcessResponse(BaseModel):
    """Response model for processing endpoint."""
    
    latex: str = Field(..., description="Original LaTeX expression")
    speech: str = Field(..., description="Natural speech representation")
    audience_level: AudienceLevel = Field(..., description="Target audience level")
    processing_time: float = Field(..., description="Processing time in seconds")
    cached: bool = Field(..., description="Whether result was from cache")


class HealthResponse(BaseModel):
    """Health check response."""
    
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    uptime: float = Field(..., description="Uptime in seconds")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    code: str = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Error details")


# Create FastAPI app
def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI app
    """
    settings = get_settings()
    
    app = FastAPI(
        title="MathSpeak Clean Architecture API",
        description="Mathematical expression to speech conversion API",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Store start time for health check
    app.state.start_time = time.time()
    
    # Initialize container
    app.state.container = get_container()
    
    return app


app = create_app()


@app.on_event("startup")
async def startup_event() -> None:
    """Initialize application on startup."""
    logger.info("MathSpeak API starting up...")
    
    # Pre-initialize use case to load patterns
    try:
        container = app.state.container
        use_case = container.get(ProcessExpressionUseCase)
        logger.info("Use case initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize use case: {e}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Clean up on shutdown."""
    logger.info("MathSpeak API shutting down...")


@app.get("/", response_model=Dict[str, str])
async def root() -> Dict[str, str]:
    """Root endpoint."""
    return {
        "message": "MathSpeak Clean Architecture API",
        "version": "2.0.0",
        "docs": "/docs",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    uptime = time.time() - app.state.start_time
    
    return HealthResponse(
        status="healthy",
        version="2.0.0",
        uptime=uptime,
    )


@app.post(
    "/process",
    response_model=ProcessResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Internal error"},
    },
)
async def process_expression(
    request: ProcessRequest,
) -> ProcessResponse:
    """Process mathematical expression to speech.
    
    Args:
        request: Processing request
        
    Returns:
        Processing response
        
    Raises:
        HTTPException: If processing fails
    """
    try:
        # Get use case from container
        container = app.state.container
        use_case = container.get(ProcessExpressionUseCase)
        
        # Create use case request
        uc_request = ProcessExpressionRequest(
            latex=request.latex,
            audience_level=request.audience_level,
            use_cache=request.use_cache,
        )
        
        # Execute use case
        uc_response = use_case.execute(uc_request)
        
        # Create API response
        return ProcessResponse(
            latex=uc_response.result.latex,
            speech=uc_response.result.speech,
            audience_level=uc_response.result.audience_level,
            processing_time=uc_response.result.processing_time,
            cached=uc_response.cached,
        )
        
    except MathSpeakError as e:
        logger.warning(f"Processing error: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": e.message,
                "code": e.code,
                "details": e.details,
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Internal server error",
                "code": "INTERNAL_ERROR",
                "details": {"message": str(e)},
            },
        )


@app.get("/stats", response_model=Dict[str, Any])
async def get_stats() -> Dict[str, Any]:
    """Get application statistics."""
    container = app.state.container
    
    # Get cache stats
    cache = container.get(container._factories[type(container.get(ProcessExpressionUseCase).cache)])
    cache_stats = cache.get_stats() if hasattr(cache, "get_stats") else {}
    
    # Get pattern stats
    use_case = container.get(ProcessExpressionUseCase)
    pattern_stats = use_case.pattern_processor.get_pattern_statistics()
    
    # Get container stats
    container_stats = container.get_stats()
    
    return {
        "cache": cache_stats,
        "patterns": pattern_stats,
        "container": container_stats,
        "uptime": time.time() - app.state.start_time,
    }


# Example usage for testing
if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower(),
    )