"""Use case for processing mathematical expressions."""

import logging
import time
from dataclasses import dataclass
from typing import Optional

from mathspeak_clean.domain.entities.expression import MathExpression
from mathspeak_clean.domain.services.pattern_processor import PatternProcessorService
from mathspeak_clean.shared.exceptions import ProcessingError, UseCaseError
from mathspeak_clean.shared.types import (
    AudienceLevel,
    Cache,
    LaTeXExpression,
    ProcessingResult,
    SpeechText,
)

logger = logging.getLogger(__name__)


@dataclass
class ProcessExpressionRequest:
    """Request for processing expression use case."""
    
    latex: LaTeXExpression
    audience_level: AudienceLevel = "undergraduate"
    use_cache: bool = True


@dataclass
class ProcessExpressionResponse:
    """Response from processing expression use case."""
    
    result: ProcessingResult
    cached: bool = False


class ProcessExpressionUseCase:
    """Use case for processing mathematical expressions to speech.
    
    This use case orchestrates the process of converting LaTeX mathematical
    expressions to natural speech text.
    """
    
    def __init__(
        self,
        pattern_processor: PatternProcessorService,
        cache: Optional[Cache] = None,
    ) -> None:
        """Initialize use case.
        
        Args:
            pattern_processor: Domain service for pattern processing
            cache: Optional cache implementation
        """
        self.pattern_processor = pattern_processor
        self.cache = cache
    
    def execute(self, request: ProcessExpressionRequest) -> ProcessExpressionResponse:
        """Execute the use case.
        
        Args:
            request: Processing request
            
        Returns:
            Processing response
            
        Raises:
            UseCaseError: If use case execution fails
        """
        start_time = time.time()
        
        try:
            # Check cache if enabled
            cache_key = None
            if request.use_cache and self.cache:
                cache_key = self._generate_cache_key(
                    request.latex,
                    request.audience_level
                )
                cached_result = self.cache.get(cache_key)
                
                if cached_result:
                    logger.debug(f"Cache hit for expression: {request.latex[:50]}...")
                    
                    # Create result with cached data
                    result = ProcessingResult(
                        latex=request.latex,
                        speech=cached_result,
                        audience_level=request.audience_level,
                        processing_time=time.time() - start_time,
                        cache_hit=True,
                    )
                    
                    return ProcessExpressionResponse(result=result, cached=True)
            
            # Create domain entity
            expression = MathExpression(
                latex=request.latex,
                audience_level=request.audience_level
            )
            
            # Process expression
            logger.info(
                f"Processing expression (complexity: {expression.complexity_score}): "
                f"{request.latex[:50]}..."
            )
            
            speech_text = self.pattern_processor.process_expression(expression)
            
            # Create result
            processing_time = time.time() - start_time
            result = ProcessingResult(
                latex=request.latex,
                speech=speech_text,
                audience_level=request.audience_level,
                processing_time=processing_time,
                cache_hit=False,
            )
            
            # Store in cache if enabled
            if request.use_cache and self.cache and cache_key:
                try:
                    self.cache.set(cache_key, speech_text)
                    logger.debug(f"Cached result for expression: {request.latex[:50]}...")
                except Exception as e:
                    # Cache errors should not fail the use case
                    logger.warning(f"Failed to cache result: {e}")
            
            logger.info(
                f"Successfully processed expression in {processing_time:.3f}s: "
                f"{request.latex[:30]}... -> {speech_text[:30]}..."
            )
            
            return ProcessExpressionResponse(result=result, cached=False)
            
        except ProcessingError as e:
            # Re-raise domain errors with use case context
            raise UseCaseError(
                f"Failed to process expression: {e.message}",
                code="EXPRESSION_PROCESSING_FAILED",
                details={
                    "expression": request.latex,
                    "audience_level": request.audience_level,
                    "error": str(e),
                }
            )
        except Exception as e:
            # Wrap unexpected errors
            logger.error(f"Unexpected error processing expression: {e}")
            raise UseCaseError(
                "An unexpected error occurred while processing the expression",
                code="UNEXPECTED_ERROR",
                details={
                    "expression": request.latex,
                    "error": str(e),
                }
            )
    
    def _generate_cache_key(
        self,
        latex: LaTeXExpression,
        audience_level: AudienceLevel
    ) -> str:
        """Generate cache key for expression.
        
        Args:
            latex: LaTeX expression
            audience_level: Target audience
            
        Returns:
            Cache key
        """
        import hashlib
        
        # Use hash to handle long expressions
        expression_hash = hashlib.md5(latex.encode()).hexdigest()
        return f"mathspeak:expression:{audience_level}:{expression_hash}"