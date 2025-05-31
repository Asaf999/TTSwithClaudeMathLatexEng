#!/usr/bin/env python3
"""
User-Friendly Error Handler
===========================

Converts technical error messages into user-friendly explanations
with helpful suggestions for resolution.
"""

import re
import logging
from typing import Dict, Optional, Any, Callable
from functools import wraps
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ErrorInfo:
    """Structured error information"""
    message: str
    suggestion: str
    technical: str
    error_code: Optional[str] = None
    
    def format(self, verbose: bool = False, use_emoji: bool = True) -> str:
        """Format error for display"""
        lines = []
        
        if use_emoji:
            lines.append(f"❌ {self.message}")
            lines.append(f"💡 {self.suggestion}")
            if verbose and self.technical:
                lines.append(f"🔧 Technical details: {self.technical}")
            if self.error_code:
                lines.append(f"📋 Error code: {self.error_code}")
        else:
            lines.append(f"Error: {self.message}")
            lines.append(f"Suggestion: {self.suggestion}")
            if verbose and self.technical:
                lines.append(f"Technical details: {self.technical}")
            if self.error_code:
                lines.append(f"Error code: {self.error_code}")
        
        return "\n".join(lines)


class UserFriendlyErrorHandler:
    """Convert technical errors to user-friendly messages"""
    
    ERROR_MAPPINGS = {
        # Import/System errors
        "ImportError": {
            "message": "System configuration error. Some required components are missing.",
            "suggestion": "Try reinstalling MathSpeak: pip install --upgrade mathspeak",
            "code": "SYS001"
        },
        "ModuleNotFoundError": {
            "message": "A required module is not installed.",
            "suggestion": "Install missing dependencies: pip install -r requirements.txt",
            "code": "SYS002"
        },
        
        # LaTeX errors
        "Unknown LaTeX command": {
            "message": "The mathematical notation '{command}' is not recognized.",
            "suggestion": "Check your LaTeX syntax or use standard notation. See documentation for supported commands.",
            "code": "TEX001"
        },
        "Malformed LaTeX": {
            "message": "The mathematical expression contains syntax errors.",
            "suggestion": "Check for matching brackets, braces, and proper command syntax.",
            "code": "TEX002"
        },
        
        # Network errors
        "ConnectionError": {
            "message": "Cannot connect to the speech service.",
            "suggestion": "Check your internet connection or use --offline mode for local TTS.",
            "code": "NET001"
        },
        "TimeoutError": {
            "message": "The speech service is taking too long to respond.",
            "suggestion": "Try again later or use --offline mode for faster processing.",
            "code": "NET002"
        },
        
        # File errors
        "FileNotFoundError": {
            "message": "Cannot find the file '{filename}'.",
            "suggestion": "Check the file path and ensure the file exists.",
            "code": "FILE001"
        },
        "PermissionError": {
            "message": "Permission denied accessing '{filename}'.",
            "suggestion": "Check file permissions or try running with appropriate privileges.",
            "code": "FILE002"
        },
        
        # Audio errors
        "AudioError": {
            "message": "Cannot play audio on your system.",
            "suggestion": "Save to file using --output option instead, or check your audio drivers.",
            "code": "AUD001"
        },
        "NoAudioDevice": {
            "message": "No audio output device found.",
            "suggestion": "Connect speakers/headphones or use --output to save as file.",
            "code": "AUD002"
        },
        
        # Processing errors
        "ProcessingTimeout": {
            "message": "Expression too complex to process within time limit.",
            "suggestion": "Try breaking the expression into smaller parts.",
            "code": "PROC001"
        },
        "MemoryError": {
            "message": "Not enough memory to process this expression.",
            "suggestion": "Close other applications or process smaller expressions.",
            "code": "PROC002"
        },
        
        # Validation errors
        "ValidationError": {
            "message": "Invalid mathematical expression.",
            "suggestion": "Check for matching brackets and valid LaTeX syntax.",
            "code": "VAL001"
        },
        "SecurityViolation": {
            "message": "Expression contains potentially dangerous content.",
            "suggestion": "Remove file I/O commands and ensure expression is purely mathematical.",
            "code": "SEC001"
        },
        
        # TTS errors
        "TTSEngineError": {
            "message": "The text-to-speech engine encountered an error.",
            "suggestion": "Try a different voice or use --offline mode.",
            "code": "TTS001"
        },
        "VoiceNotFound": {
            "message": "The requested voice '{voice}' is not available.",
            "suggestion": "Use 'mathspeak voices list' to see available voices.",
            "code": "TTS002"
        }
    }
    
    # Pattern-based error detection
    ERROR_PATTERNS = [
        (r"Unknown.*command.*\\(\\w+)", "Unknown LaTeX command"),
        (r"[Mm]alformed.*[Ll]a[Tt]e[Xx]", "Malformed LaTeX"),
        (r"[Nn]o.*audio.*device", "NoAudioDevice"),
        (r"[Vv]oice.*not.*found|[Vv]oice.*'(\w+)'.*not", "VoiceNotFound"),
        (r"[Tt]ime.*limit.*exceeded|[Tt]imeout", "ProcessingTimeout"),
        (r"[Ss]ecurity.*violation|[Dd]angerous.*command", "SecurityViolation"),
        (r"TTS.*[Ee]rror|edge.*tts.*error", "TTSEngineError"),
    ]
    
    def translate_error(self, error: Exception) -> ErrorInfo:
        """Translate exception to user-friendly message"""
        error_type = type(error).__name__
        error_str = str(error)
        
        # Direct type mapping
        if error_type in self.ERROR_MAPPINGS:
            mapping = self.ERROR_MAPPINGS[error_type]
            return self._create_error_info(mapping, error_str, error)
        
        # Pattern matching
        for pattern, mapped_type in self.ERROR_PATTERNS:
            match = re.search(pattern, error_str, re.IGNORECASE)
            if match:
                mapping = self.ERROR_MAPPINGS.get(mapped_type)
                if mapping:
                    # Extract matched groups for formatting
                    format_args = {}
                    if match.groups():
                        if mapped_type == "Unknown LaTeX command":
                            format_args['command'] = match.group(1)
                        elif mapped_type == "VoiceNotFound":
                            format_args['voice'] = match.group(1) if match.group(1) else "unknown"
                    
                    return self._create_error_info(mapping, error_str, error, format_args)
        
        # Generic error
        return ErrorInfo(
            message="An unexpected error occurred while processing your request.",
            suggestion="Try simplifying your expression or contact support if the issue persists.",
            technical=error_str,
            error_code="GEN001"
        )
    
    def _create_error_info(self, mapping: Dict[str, str], error_str: str, 
                          error: Exception, format_args: Optional[Dict[str, str]] = None) -> ErrorInfo:
        """Create ErrorInfo from mapping"""
        message = mapping["message"]
        suggestion = mapping["suggestion"]
        
        # Format with any extracted values
        if format_args:
            try:
                message = message.format(**format_args)
                suggestion = suggestion.format(**format_args)
            except KeyError:
                pass
        
        # Try to extract filename from error
        if "{filename}" in message or "{filename}" in suggestion:
            filename_match = re.search(r"['\"]([^'\"]+)['\"]", error_str)
            if filename_match:
                filename = filename_match.group(1)
                message = message.format(filename=filename)
                suggestion = suggestion.format(filename=filename)
        
        return ErrorInfo(
            message=message,
            suggestion=suggestion,
            technical=error_str,
            error_code=mapping.get("code")
        )
    
    def format_error_output(self, error_info: ErrorInfo, verbose: bool = False, 
                           use_emoji: bool = True) -> str:
        """Format error for display"""
        return error_info.format(verbose=verbose, use_emoji=use_emoji)


# Global handler instance
_error_handler = UserFriendlyErrorHandler()


def handle_user_error(func: Optional[Callable] = None, *, 
                     verbose_arg: str = 'debug',
                     use_emoji: bool = True,
                     reraise: bool = False):
    """
    Decorator to handle errors in user-facing functions
    
    Args:
        func: Function to decorate
        verbose_arg: Name of the argument that controls verbosity
        use_emoji: Whether to use emoji in error messages
        reraise: Whether to re-raise the exception after handling
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except Exception as e:
                # Check if we should show verbose output
                verbose = kwargs.get(verbose_arg, False)
                
                # Translate error
                error_info = _error_handler.translate_error(e)
                
                # Format and print
                formatted = error_info.format(verbose=verbose, use_emoji=use_emoji)
                print(formatted)
                
                # Log the technical details
                logger.error(f"Error in {f.__name__}: {error_info.technical}")
                
                if reraise or verbose:
                    raise
                
                return None
        
        return wrapper
    
    # Handle being called with or without arguments
    if func is None:
        return decorator
    else:
        return decorator(func)


# Convenience functions
def translate_error(error: Exception) -> ErrorInfo:
    """Translate an exception to user-friendly error info"""
    return _error_handler.translate_error(error)


def format_error(error: Exception, verbose: bool = False, use_emoji: bool = True) -> str:
    """Format an exception as user-friendly text"""
    error_info = translate_error(error)
    return error_info.format(verbose=verbose, use_emoji=use_emoji)