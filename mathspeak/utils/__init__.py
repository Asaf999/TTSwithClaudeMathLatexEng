"""
MathSpeak Utility Modules
========================

Utility modules providing configuration management, logging, and other
supporting functionality for the Mathematical Text-to-Speech system.

Modules:
- config: Configuration management with user preferences
- logger: Comprehensive logging and performance tracking
"""

from .config import (
    Config,
    VoiceConfig,
    DomainConfig,
    ProcessingConfig,
    OutputConfig,
    NaturalLanguageConfig,
    DebugConfig,
    UserPreferences,
    OutputFormat,
    QualityLevel,
    ProcessingMode,
    get_default_config,
    load_config_from_env,
    DEFAULT_CONFIG_DIR,
    CONFIG_VERSION,
)

from .logger import (
    setup_logging,
    get_logger,
    get_performance_logger,
    PerformanceLogger,
    PerformanceMetrics,
    ErrorReporter,
    ColoredFormatter,
    JSONFormatter,
    PERFORMANCE,
    log_system_info,
    cleanup_old_logs,
    DEFAULT_LOG_DIR,
)

# Convenience functions
def quick_setup(debug: bool = False) -> tuple:
    """
    Quick setup for MathSpeak with default configuration and logging
    
    Args:
        debug: Enable debug mode
    
    Returns:
        Tuple of (config, logger)
    """
    # Load config with environment overrides
    config = load_config_from_env()
    
    # Setup logging
    log_level = 'DEBUG' if debug else config.debug.log_level
    logger = setup_logging(
        level=log_level,
        log_to_file=config.debug.log_to_file,
        log_to_console=True,
        json_logs=config.debug.save_performance_metrics
    )
    
    # Log system info if debug
    if debug:
        log_system_info(logger)
    
    return config, logger

def get_cache_dir() -> Path:
    """Get the cache directory for MathSpeak"""
    cache_dir = DEFAULT_CONFIG_DIR / 'cache'
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir

def get_data_dir() -> Path:
    """Get the data directory for MathSpeak"""
    data_dir = DEFAULT_CONFIG_DIR / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

# Version utilities
def get_version_info() -> Dict[str, str]:
    """Get version information for all components"""
    from ..core import __version__ as core_version
    
    return {
        'mathspeak': '1.0.0',
        'core': core_version,
        'config': CONFIG_VERSION,
        'python': sys.version.split()[0],
    }

# Export all
__all__ = [
    # Config
    'Config',
    'VoiceConfig',
    'DomainConfig',
    'ProcessingConfig',
    'OutputConfig',
    'NaturalLanguageConfig',
    'DebugConfig',
    'UserPreferences',
    'OutputFormat',
    'QualityLevel',
    'ProcessingMode',
    'get_default_config',
    'load_config_from_env',
    
    # Logger
    'setup_logging',
    'get_logger',
    'get_performance_logger',
    'PerformanceLogger',
    'PerformanceMetrics',
    'ErrorReporter',
    'PERFORMANCE',
    'log_system_info',
    'cleanup_old_logs',
    
    # Convenience
    'quick_setup',
    'get_cache_dir',
    'get_data_dir',
    'get_version_info',
    
    # Constants
    'DEFAULT_CONFIG_DIR',
    'DEFAULT_LOG_DIR',
    'CONFIG_VERSION',
]

# Type imports
from pathlib import Path
from typing import Dict
import sys

import logging
logger = logging.getLogger(__name__)