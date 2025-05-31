"""Exception hierarchy for MathSpeak Clean Architecture."""

from typing import Any, Dict, Optional


class MathSpeakError(Exception):
    """Base exception for all MathSpeak errors."""
    
    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize MathSpeak error.
        
        Args:
            message: Error message
            code: Error code for programmatic handling
            details: Additional error details
        """
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}


class DomainError(MathSpeakError):
    """Domain layer errors."""
    
    pass


class ValidationError(DomainError):
    """Validation errors for domain rules."""
    
    def __init__(self, field: str, message: str, value: Any = None) -> None:
        """Initialize validation error.
        
        Args:
            field: Field that failed validation
            message: Validation error message
            value: Invalid value
        """
        super().__init__(
            f"Validation failed for {field}: {message}",
            code="VALIDATION_ERROR",
            details={"field": field, "value": value},
        )


class PatternError(DomainError):
    """Pattern processing errors."""
    
    pass


class PatternSyntaxError(PatternError):
    """Invalid pattern syntax."""
    
    def __init__(self, pattern: str, message: str) -> None:
        """Initialize pattern syntax error.
        
        Args:
            pattern: Invalid pattern
            message: Error message
        """
        super().__init__(
            f"Invalid pattern syntax: {message}",
            code="PATTERN_SYNTAX_ERROR",
            details={"pattern": pattern},
        )


class PatternMatchError(PatternError):
    """Pattern matching failed."""
    
    def __init__(self, expression: str, pattern: str, message: str) -> None:
        """Initialize pattern match error.
        
        Args:
            expression: Expression being matched
            pattern: Pattern that failed
            message: Error message
        """
        super().__init__(
            f"Pattern match failed: {message}",
            code="PATTERN_MATCH_ERROR",
            details={"expression": expression, "pattern": pattern},
        )


class ApplicationError(MathSpeakError):
    """Application layer errors."""
    
    pass


class UseCaseError(ApplicationError):
    """Use case execution errors."""
    
    pass


class ProcessingError(UseCaseError):
    """Expression processing errors."""
    
    def __init__(self, expression: str, stage: str, message: str) -> None:
        """Initialize processing error.
        
        Args:
            expression: Expression being processed
            stage: Processing stage where error occurred
            message: Error message
        """
        super().__init__(
            f"Processing failed at {stage}: {message}",
            code="PROCESSING_ERROR",
            details={"expression": expression, "stage": stage},
        )


class InfrastructureError(MathSpeakError):
    """Infrastructure layer errors."""
    
    pass


class TTSError(InfrastructureError):
    """Text-to-speech engine errors."""
    
    pass


class TTSEngineNotAvailableError(TTSError):
    """TTS engine is not available."""
    
    def __init__(self, engine: str, reason: str) -> None:
        """Initialize TTS engine not available error.
        
        Args:
            engine: Engine name
            reason: Reason for unavailability
        """
        super().__init__(
            f"TTS engine '{engine}' not available: {reason}",
            code="TTS_ENGINE_NOT_AVAILABLE",
            details={"engine": engine},
        )


class TTSVoiceNotFoundError(TTSError):
    """Requested voice not found."""
    
    def __init__(self, voice: str, available_voices: list) -> None:
        """Initialize TTS voice not found error.
        
        Args:
            voice: Requested voice
            available_voices: List of available voices
        """
        super().__init__(
            f"Voice '{voice}' not found",
            code="TTS_VOICE_NOT_FOUND",
            details={"requested_voice": voice, "available_voices": available_voices},
        )


class CacheError(InfrastructureError):
    """Cache-related errors."""
    
    pass


class ConfigurationError(InfrastructureError):
    """Configuration errors."""
    
    def __init__(self, key: str, message: str, current_value: Any = None) -> None:
        """Initialize configuration error.
        
        Args:
            key: Configuration key
            message: Error message
            current_value: Current invalid value
        """
        super().__init__(
            f"Configuration error for '{key}': {message}",
            code="CONFIGURATION_ERROR",
            details={"key": key, "current_value": current_value},
        )


class TimeoutError(MathSpeakError):
    """Operation timeout errors."""
    
    def __init__(self, operation: str, timeout: float) -> None:
        """Initialize timeout error.
        
        Args:
            operation: Operation that timed out
            timeout: Timeout duration in seconds
        """
        super().__init__(
            f"Operation '{operation}' timed out after {timeout}s",
            code="TIMEOUT_ERROR",
            details={"operation": operation, "timeout": timeout},
        )