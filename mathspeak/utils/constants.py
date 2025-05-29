#!/usr/bin/env python3
"""
System Constants and Configuration Defaults
==========================================

Centralized location for all system constants to avoid hardcoded values.
"""

from typing import Dict, Any


class SystemConstants:
    """System-wide constants"""
    
    # Cache settings
    DEFAULT_CACHE_SIZE = 1000
    CACHE_CLEANUP_RATIO = 0.5  # Remove 50% when full
    
    # Performance settings
    MAX_EXPRESSION_LENGTH = 10000
    MAX_PROCESSING_TIME = 30.0  # seconds
    DEFAULT_THREAD_WORKERS = 4
    
    # Audio settings
    DEFAULT_VOICE = "en-US-AriaNeural"
    DEFAULT_RATE = "+0%"
    MIN_SPEED = 0.5
    MAX_SPEED = 2.0
    
    # Logging settings
    DEFAULT_LOG_LEVEL = "INFO"
    MAX_LOG_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Pattern processing
    MAX_PATTERN_ITERATIONS = 10
    PATTERN_TIMEOUT = 5.0  # seconds
    
    # File paths
    DEFAULT_CONFIG_DIR = "~/.mathspeak"
    UNKNOWN_COMMANDS_FILE = "unknown_latex_commands.json"
    
    # Domain settings
    DEFAULT_DOMAIN = "general"
    DOMAIN_DETECTION_THRESHOLD = 0.3
    
    # Voice roles
    VOICE_ROLES = {
        'narrator': 'en-US-AriaNeural',
        'definition': 'en-US-JennyNeural',
        'theorem': 'en-US-GuyNeural',
        'proof': 'en-US-AriaNeural',
        'example': 'en-US-JennyNeural',
        'emphasis': 'en-US-GuyNeural',
        'warning': 'en-US-JennyNeural'
    }
    
    # Speed profiles
    SPEED_PROFILES = {
        'theorem_statement': '-10%',
        'proof_start': '-15%',
        'proof_middle': '+0%',
        'proof_end': '-5%',
        'definition': '-20%',
        'example': '+5%',
        'complex_formula': '-25%',
        'simple_formula': '+10%',
        'normal': '+0%'
    }


def get_default_config() -> Dict[str, Any]:
    """Get default configuration dictionary"""
    return {
        'cache': {
            'enabled': True,
            'max_size': SystemConstants.DEFAULT_CACHE_SIZE,
            'cleanup_ratio': SystemConstants.CACHE_CLEANUP_RATIO
        },
        'performance': {
            'max_expression_length': SystemConstants.MAX_EXPRESSION_LENGTH,
            'max_processing_time': SystemConstants.MAX_PROCESSING_TIME,
            'thread_workers': SystemConstants.DEFAULT_THREAD_WORKERS
        },
        'audio': {
            'default_voice': SystemConstants.DEFAULT_VOICE,
            'default_rate': SystemConstants.DEFAULT_RATE,
            'min_speed': SystemConstants.MIN_SPEED,
            'max_speed': SystemConstants.MAX_SPEED
        },
        'logging': {
            'level': SystemConstants.DEFAULT_LOG_LEVEL,
            'max_file_size': SystemConstants.MAX_LOG_FILE_SIZE,
            'backup_count': SystemConstants.LOG_BACKUP_COUNT
        },
        'domains': {
            'default': SystemConstants.DEFAULT_DOMAIN,
            'detection_threshold': SystemConstants.DOMAIN_DETECTION_THRESHOLD
        }
    }