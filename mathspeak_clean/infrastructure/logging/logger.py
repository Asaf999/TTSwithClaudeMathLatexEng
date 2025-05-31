"""Structured logging configuration for MathSpeak."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from mathspeak_clean.infrastructure.config.settings import get_settings


class StructuredFormatter(logging.Formatter):
    """JSON structured log formatter."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON.
        
        Args:
            record: Log record
            
        Returns:
            JSON formatted log entry
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add extra fields
        if hasattr(record, "expression"):
            log_data["expression"] = record.expression
        if hasattr(record, "processing_time"):
            log_data["processing_time"] = record.processing_time
        if hasattr(record, "cache_hit"):
            log_data["cache_hit"] = record.cache_hit
        if hasattr(record, "error_code"):
            log_data["error_code"] = record.error_code
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class ConsoleFormatter(logging.Formatter):
    """Colored console formatter for development."""
    
    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors.
        
        Args:
            record: Log record
            
        Returns:
            Colored log entry
        """
        # Get color for level
        color = self.COLORS.get(record.levelname, "")
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
        
        # Build log message
        log_msg = f"{color}{timestamp} [{record.levelname}] {record.name}: {record.getMessage()}{self.RESET}"
        
        # Add extra context
        extras = []
        if hasattr(record, "expression"):
            extras.append(f"expr={record.expression[:30]}...")
        if hasattr(record, "processing_time"):
            extras.append(f"time={record.processing_time:.3f}s")
        if hasattr(record, "cache_hit"):
            extras.append(f"cache={'hit' if record.cache_hit else 'miss'}")
        
        if extras:
            log_msg += f" ({', '.join(extras)})"
        
        # Add exception if present
        if record.exc_info:
            log_msg += f"\n{self.formatException(record.exc_info)}"
        
        return log_msg


def setup_logging(
    name: Optional[str] = None,
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    structured: bool = False,
) -> logging.Logger:
    """Set up logging configuration.
    
    Args:
        name: Logger name (None for root logger)
        level: Log level (uses settings if not provided)
        log_file: Log file path (uses settings if not provided)
        structured: Use structured JSON logging
        
    Returns:
        Configured logger
    """
    settings = get_settings()
    
    # Get logger
    logger = logging.getLogger(name)
    
    # Set level
    log_level = level or settings.log_level
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if structured or not settings.debug_mode:
        console_handler.setFormatter(StructuredFormatter())
    else:
        console_handler.setFormatter(ConsoleFormatter())
    logger.addHandler(console_handler)
    
    # File handler
    file_path = log_file or settings.log_file
    if file_path:
        # Create log directory if needed
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(StructuredFormatter())
        logger.addHandler(file_handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """Get a configured logger.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger
    """
    return setup_logging(name)


class LogContext:
    """Context manager for adding extra fields to logs."""
    
    def __init__(self, logger: logging.Logger, **kwargs: Any) -> None:
        """Initialize log context.
        
        Args:
            logger: Logger to add context to
            **kwargs: Extra fields to add
        """
        self.logger = logger
        self.extras = kwargs
        self.old_extras: Dict[str, Any] = {}
    
    def __enter__(self) -> None:
        """Enter context and add extras to logger."""
        # Save old values and set new ones
        for key, value in self.extras.items():
            if hasattr(self.logger, key):
                self.old_extras[key] = getattr(self.logger, key)
            setattr(self.logger, key, value)
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context and restore logger state."""
        # Remove added extras
        for key in self.extras:
            if key in self.old_extras:
                setattr(self.logger, key, self.old_extras[key])
            else:
                delattr(self.logger, key)


def log_performance(
    logger: logging.Logger,
    operation: str,
    duration: float,
    **kwargs: Any
) -> None:
    """Log performance metrics.
    
    Args:
        logger: Logger to use
        operation: Operation name
        duration: Duration in seconds
        **kwargs: Additional metrics
    """
    logger.info(
        f"Performance: {operation}",
        extra={
            "operation": operation,
            "duration": duration,
            "metrics": kwargs,
        }
    )


def log_error(
    logger: logging.Logger,
    error: Exception,
    context: Optional[Dict[str, Any]] = None,
) -> None:
    """Log error with context.
    
    Args:
        logger: Logger to use
        error: Exception to log
        context: Additional context
    """
    logger.error(
        f"Error: {type(error).__name__}: {str(error)}",
        exc_info=error,
        extra={
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {},
        }
    )