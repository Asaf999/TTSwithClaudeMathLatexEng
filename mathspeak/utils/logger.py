#!/usr/bin/env python3
"""
Logging Configuration for Mathematical Text-to-Speech System
===========================================================

Provides comprehensive logging setup for debugging, performance tracking,
and error reporting across all MathSpeak components.

Features:
- Multiple log handlers (console, file, rotating)
- Performance metrics logging
- Structured logging with context
- Log filtering and formatting
- Integration with configuration system
"""

import logging
import logging.handlers
import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Any, List, Union
from dataclasses import dataclass, asdict
import platform
import traceback
from contextlib import contextmanager

# ===========================
# Logging Constants
# ===========================

# Default log directory
if platform.system() == "Windows":
    DEFAULT_LOG_DIR = Path(os.environ.get('APPDATA', '')) / 'MathSpeak' / 'logs'
else:
    DEFAULT_LOG_DIR = Path.home() / '.mathspeak' / 'logs'

# Log file names
MAIN_LOG_FILE = 'mathspeak.log'
ERROR_LOG_FILE = 'errors.log'
PERFORMANCE_LOG_FILE = 'performance.log'
DEBUG_LOG_FILE = 'debug.log'

# Log formatting
DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DETAILED_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s'
JSON_FORMAT = '%(message)s'  # For structured logging

# Log rotation settings
MAX_BYTES = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

# ===========================
# Custom Log Levels
# ===========================

# Performance logging level
PERFORMANCE = 35
logging.addLevelName(PERFORMANCE, "PERFORMANCE")

def performance(self, message, *args, **kwargs):
    """Log performance metrics"""
    if self.isEnabledFor(PERFORMANCE):
        self._log(PERFORMANCE, message, args, **kwargs)

# Add performance method to Logger
logging.Logger.performance = performance

# ===========================
# Custom Formatters
# ===========================

class ColoredFormatter(logging.Formatter):
    """Colored console output formatter"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'PERFORMANCE': '\033[34m', # Blue
        'RESET': '\033[0m'        # Reset
    }
    
    def __init__(self, fmt=None, use_colors=True):
        super().__init__(fmt)
        self.use_colors = use_colors and sys.stderr.isatty()
    
    def format(self, record):
        if self.use_colors:
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
                record.name = f"\033[37m{record.name}\033[0m"  # White
        
        return super().format(record)

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields
        if hasattr(record, 'context'):
            log_data['context'] = record.context
        if hasattr(record, 'performance_metrics'):
            log_data['performance'] = record.performance_metrics
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)

# ===========================
# Custom Filters
# ===========================

class ContextFilter(logging.Filter):
    """Add context information to log records"""
    
    def __init__(self, context: Optional[Dict[str, Any]] = None):
        super().__init__()
        self.context = context or {}
    
    def filter(self, record):
        # Add context to record
        for key, value in self.context.items():
            setattr(record, key, value)
        return True

class PerformanceFilter(logging.Filter):
    """Filter for performance-related logs"""
    
    def filter(self, record):
        return record.levelno == PERFORMANCE

# ===========================
# Log Handlers
# ===========================

def create_console_handler(
    level: int = logging.INFO,
    use_colors: bool = True,
    detailed: bool = False
) -> logging.StreamHandler:
    """Create console log handler"""
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    
    # Set formatter
    if detailed:
        formatter = ColoredFormatter(DETAILED_FORMAT, use_colors)
    else:
        formatter = ColoredFormatter(DEFAULT_FORMAT, use_colors)
    
    handler.setFormatter(formatter)
    return handler

def create_file_handler(
    filename: Union[str, Path],
    level: int = logging.DEBUG,
    max_bytes: int = MAX_BYTES,
    backup_count: int = BACKUP_COUNT,
    encoding: str = 'utf-8'
) -> logging.handlers.RotatingFileHandler:
    """Create rotating file handler"""
    handler = logging.handlers.RotatingFileHandler(
        filename,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=encoding
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(DETAILED_FORMAT))
    return handler

def create_json_handler(
    filename: Union[str, Path],
    level: int = logging.INFO
) -> logging.FileHandler:
    """Create JSON file handler for structured logging"""
    handler = logging.FileHandler(filename, encoding='utf-8')
    handler.setLevel(level)
    handler.setFormatter(JSONFormatter())
    return handler

# ===========================
# Performance Logger
# ===========================

@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    operation: str
    duration: float
    tokens_processed: Optional[int] = None
    cache_hit: Optional[bool] = None
    memory_used_mb: Optional[float] = None
    extra: Dict[str, Any] = None

class PerformanceLogger:
    """Specialized logger for performance metrics"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.metrics: List[PerformanceMetrics] = []
    
    @contextmanager
    def measure(self, operation: str, **extra):
        """Context manager to measure operation performance"""
        start_time = time.time()
        metrics = PerformanceMetrics(
            operation=operation,
            duration=0.0,
            extra=extra
        )
        
        try:
            yield metrics
        finally:
            metrics.duration = time.time() - start_time
            self.log_metrics(metrics)
    
    def log_metrics(self, metrics: PerformanceMetrics):
        """Log performance metrics"""
        self.metrics.append(metrics)
        
        # Create log message
        msg_parts = [
            f"Operation: {metrics.operation}",
            f"Duration: {metrics.duration:.3f}s"
        ]
        
        if metrics.tokens_processed:
            tokens_per_sec = metrics.tokens_processed / max(metrics.duration, 0.001)
            msg_parts.append(f"Tokens: {metrics.tokens_processed} ({tokens_per_sec:.1f}/s)")
        
        if metrics.cache_hit is not None:
            msg_parts.append(f"Cache: {'HIT' if metrics.cache_hit else 'MISS'}")
        
        if metrics.memory_used_mb:
            msg_parts.append(f"Memory: {metrics.memory_used_mb:.1f}MB")
        
        # Log with performance level
        self.logger.performance(
            " | ".join(msg_parts),
            extra={'performance_metrics': asdict(metrics)}
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics:
            return {}
        
        total_duration = sum(m.duration for m in self.metrics)
        avg_duration = total_duration / len(self.metrics)
        
        return {
            'total_operations': len(self.metrics),
            'total_duration': total_duration,
            'average_duration': avg_duration,
            'operations_by_type': self._group_by_operation(),
            'cache_stats': self._calculate_cache_stats(),
        }
    
    def _group_by_operation(self) -> Dict[str, Dict[str, float]]:
        """Group metrics by operation type"""
        groups = {}
        for metric in self.metrics:
            op = metric.operation
            if op not in groups:
                groups[op] = {'count': 0, 'total_duration': 0.0}
            groups[op]['count'] += 1
            groups[op]['total_duration'] += metric.duration
        
        # Calculate averages
        for op, stats in groups.items():
            stats['average_duration'] = stats['total_duration'] / stats['count']
        
        return groups
    
    def _calculate_cache_stats(self) -> Dict[str, Any]:
        """Calculate cache statistics"""
        cache_metrics = [m for m in self.metrics if m.cache_hit is not None]
        if not cache_metrics:
            return {}
        
        hits = sum(1 for m in cache_metrics if m.cache_hit)
        total = len(cache_metrics)
        
        return {
            'total_requests': total,
            'hits': hits,
            'misses': total - hits,
            'hit_rate': hits / total if total > 0 else 0.0
        }

# ===========================
# Main Logging Setup
# ===========================

def setup_logging(
    level: Union[int, str] = logging.INFO,
    log_dir: Optional[Path] = None,
    log_to_file: bool = True,
    log_to_console: bool = True,
    use_colors: bool = True,
    detailed_console: bool = False,
    json_logs: bool = False,
    context: Optional[Dict[str, Any]] = None
) -> logging.Logger:
    """
    Set up comprehensive logging for MathSpeak
    
    Args:
        level: Base logging level
        log_dir: Directory for log files
        log_to_file: Enable file logging
        log_to_console: Enable console logging
        use_colors: Use colored console output
        detailed_console: Use detailed format for console
        json_logs: Enable JSON structured logging
        context: Additional context for all logs
    
    Returns:
        Root logger configured for MathSpeak
    """
    # Convert string level to int
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    
    # Ensure log directory exists
    if log_to_file:
        if log_dir is None:
            log_dir = DEFAULT_LOG_DIR
        log_dir = Path(log_dir)
        log_dir.mkdir(parents=True, exist_ok=True)
    
    # Get root logger for mathspeak
    root_logger = logging.getLogger('mathspeak')
    root_logger.setLevel(level)
    
    # Remove existing handlers
    root_logger.handlers.clear()
    
    # Add console handler
    if log_to_console:
        console_handler = create_console_handler(
            level=level,
            use_colors=use_colors,
            detailed=detailed_console
        )
        root_logger.addHandler(console_handler)
    
    # Add file handlers
    if log_to_file:
        # Main log file
        main_handler = create_file_handler(
            log_dir / MAIN_LOG_FILE,
            level=level
        )
        root_logger.addHandler(main_handler)
        
        # Error log file (ERROR and above)
        error_handler = create_file_handler(
            log_dir / ERROR_LOG_FILE,
            level=logging.ERROR,
            max_bytes=5 * MAX_BYTES  # Larger for errors
        )
        root_logger.addHandler(error_handler)
        
        # Performance log file
        perf_handler = create_file_handler(
            log_dir / PERFORMANCE_LOG_FILE,
            level=PERFORMANCE
        )
        perf_handler.addFilter(PerformanceFilter())
        root_logger.addHandler(perf_handler)
        
        # Debug log file (if debug mode)
        if level <= logging.DEBUG:
            debug_handler = create_file_handler(
                log_dir / DEBUG_LOG_FILE,
                level=logging.DEBUG
            )
            root_logger.addHandler(debug_handler)
        
        # JSON structured logs
        if json_logs:
            json_handler = create_json_handler(
                log_dir / 'structured.json',
                level=level
            )
            root_logger.addHandler(json_handler)
    
    # Add context filter if provided
    if context:
        context_filter = ContextFilter(context)
        for handler in root_logger.handlers:
            handler.addFilter(context_filter)
    
    # Log startup information
    root_logger.info("MathSpeak logging initialized")
    root_logger.info(f"Log level: {logging.getLevelName(level)}")
    if log_to_file:
        root_logger.info(f"Log directory: {log_dir}")
    
    return root_logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module"""
    return logging.getLogger(f'mathspeak.{name}')

def get_performance_logger(name: str) -> PerformanceLogger:
    """Get a performance logger for a module"""
    logger = get_logger(name)
    return PerformanceLogger(logger)

# ===========================
# Error Reporting
# ===========================

class ErrorReporter:
    """Enhanced error reporting with context"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.error_count = 0
        self.error_history: List[Dict[str, Any]] = []
    
    def report_error(
        self,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_message: Optional[str] = None
    ) -> None:
        """Report an error with full context"""
        self.error_count += 1
        
        # Build error info
        error_info = {
            'timestamp': datetime.utcnow().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'traceback': traceback.format_exc(),
            'context': context or {},
        }
        
        self.error_history.append(error_info)
        
        # Log the error
        self.logger.error(
            f"{error_info['error_type']}: {error_info['error_message']}",
            exc_info=True,
            extra={'error_context': context}
        )
        
        # User-friendly message if provided
        if user_message:
            self.logger.info(f"User message: {user_message}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get summary of errors"""
        if not self.error_history:
            return {'error_count': 0}
        
        # Group by error type
        error_types = {}
        for error in self.error_history:
            error_type = error['error_type']
            if error_type not in error_types:
                error_types[error_type] = 0
            error_types[error_type] += 1
        
        return {
            'error_count': self.error_count,
            'error_types': error_types,
            'recent_errors': self.error_history[-5:],  # Last 5 errors
        }

# ===========================
# Utilities
# ===========================

def log_system_info(logger: logging.Logger) -> None:
    """Log system information for debugging"""
    import psutil
    
    info = {
        'platform': platform.platform(),
        'python_version': sys.version,
        'cpu_count': os.cpu_count(),
        'memory_total_gb': psutil.virtual_memory().total / (1024**3),
        'memory_available_gb': psutil.virtual_memory().available / (1024**3),
    }
    
    logger.info("System information:")
    for key, value in info.items():
        logger.info(f"  {key}: {value}")

def cleanup_old_logs(log_dir: Path, days: int = 30) -> None:
    """Clean up log files older than specified days"""
    import time
    
    cutoff_time = time.time() - (days * 24 * 60 * 60)
    
    for log_file in log_dir.glob('*.log*'):
        if log_file.stat().st_mtime < cutoff_time:
            try:
                log_file.unlink()
                logging.info(f"Deleted old log file: {log_file}")
            except Exception as e:
                logging.error(f"Failed to delete {log_file}: {e}")

# ===========================
# Testing Functions
# ===========================

def test_logging():
    """Test logging functionality"""
    import tempfile
    
    # Create temporary log directory
    with tempfile.TemporaryDirectory() as tmpdir:
        # Setup logging
        logger = setup_logging(
            level=logging.DEBUG,
            log_dir=tmpdir,
            detailed_console=True,
            json_logs=True,
            context={'session_id': 'test_123'}
        )
        
        print("Testing Logging System")
        print("=" * 50)
        
        # Test different log levels
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        
        # Test performance logging
        perf_logger = get_performance_logger('test')
        
        with perf_logger.measure('test_operation', tokens=100) as metrics:
            time.sleep(0.1)  # Simulate work
            metrics.tokens_processed = 100
            metrics.cache_hit = True
        
        # Test error reporting
        error_reporter = ErrorReporter(logger)
        try:
            raise ValueError("Test error")
        except ValueError as e:
            error_reporter.report_error(
                e,
                context={'function': 'test_logging'},
                user_message="This is a test error"
            )
        
        # Log system info
        log_system_info(logger)
        
        # Show performance summary
        print("\nPerformance Summary:")
        print(json.dumps(perf_logger.get_summary(), indent=2))
        
        # Show error summary
        print("\nError Summary:")
        print(json.dumps(error_reporter.get_error_summary(), indent=2))
        
        # Check created log files
        print(f"\nLog files created in {tmpdir}:")
        for log_file in Path(tmpdir).glob('*.log*'):
            print(f"  {log_file.name} ({log_file.stat().st_size} bytes)")

if __name__ == "__main__":
    test_logging()