#!/usr/bin/env python3
"""
Configuration Management for Mathematical Text-to-Speech System
==============================================================

Manages all configuration settings including user preferences, domain toggles,
voice settings, and performance options. Supports both file-based and
programmatic configuration.

This module provides:
- Default settings for all components
- User preference management
- Domain-specific configuration
- Performance tuning options
- Configuration validation
"""

import json
import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field, asdict
from enum import Enum
import platform

logger = logging.getLogger(__name__)

# ===========================
# Configuration Constants
# ===========================

# Default paths
if platform.system() == "Windows":
    DEFAULT_CONFIG_DIR = Path(os.environ.get('APPDATA', '')) / 'MathSpeak'
else:
    DEFAULT_CONFIG_DIR = Path.home() / '.mathspeak'

DEFAULT_CONFIG_FILE = 'config.json'
DEFAULT_USER_PREFS_FILE = 'user_preferences.json'

# Configuration version for migration
CONFIG_VERSION = "1.0.0"

# ===========================
# Configuration Enums
# ===========================

class OutputFormat(Enum):
    """Supported audio output formats"""
    MP3 = "mp3"
    WAV = "wav"
    OGG = "ogg"

class QualityLevel(Enum):
    """Audio quality levels"""
    LOW = "low"          # Fast processing, smaller files
    MEDIUM = "medium"    # Balanced
    HIGH = "high"        # Best quality, larger files

class ProcessingMode(Enum):
    """Processing modes for performance tuning"""
    FAST = "fast"              # Minimal processing
    BALANCED = "balanced"      # Default mode
    QUALITY = "quality"        # Maximum quality

# ===========================
# Configuration Data Classes
# ===========================

@dataclass
class VoiceConfig:
    """Voice-related configuration"""
    default_voice: str = "en-US-AriaNeural"
    speed_multiplier: float = 1.0
    pitch_adjustment: float = 0.0
    volume: float = 1.0
    enable_commentary: bool = True
    commentary_frequency: float = 0.3  # 0.0 to 1.0
    emphasis_strength: float = 1.0
    pause_duration_multiplier: float = 1.0

@dataclass
class DomainConfig:
    """Domain-specific configuration"""
    enabled_domains: List[str] = field(default_factory=lambda: [
        "topology",
        "complex_analysis",
        "numerical_analysis",
        "manifolds",
        "ode",
        "real_analysis",
        "measure_theory",
        "combinatorics",
        "algebra"
    ])
    priority_domains: List[str] = field(default_factory=lambda: [
        "topology",
        "complex_analysis"
    ])
    domain_specific_settings: Dict[str, Dict[str, Any]] = field(default_factory=dict)

@dataclass
class ProcessingConfig:
    """Processing and performance configuration"""
    mode: ProcessingMode = ProcessingMode.BALANCED
    enable_caching: bool = True
    cache_size_mb: int = 100
    max_expression_length: int = 10000
    parallel_processing: bool = True
    worker_threads: int = 4
    memory_limit_mb: int = 500
    timeout_seconds: int = 30

@dataclass
class OutputConfig:
    """Output configuration"""
    format: OutputFormat = OutputFormat.MP3
    quality: QualityLevel = QualityLevel.MEDIUM
    sample_rate: int = 22050
    bitrate: str = "128k"
    save_intermediate_files: bool = False
    output_directory: Optional[str] = None
    filename_template: str = "mathspeak_{timestamp}_{hash}"

@dataclass
class NaturalLanguageConfig:
    """Natural language processing configuration"""
    use_variations: bool = True
    correct_grammar: bool = True
    insert_pauses: bool = True
    detect_emphasis: bool = True
    add_clarifications: bool = True
    max_clarifications_per_expression: int = 2
    tone: str = "conversational"  # formal, conversational, explanatory, rigorous
    variation_frequency: float = 0.7

@dataclass
class DebugConfig:
    """Debug and logging configuration"""
    debug_mode: bool = False
    log_level: str = "INFO"
    log_to_file: bool = True
    log_directory: Optional[str] = None
    save_unknown_commands: bool = True
    save_performance_metrics: bool = True
    verbose_output: bool = False

@dataclass
class UserPreferences:
    """User-specific preferences"""
    preferred_voice_role: str = "narrator"
    preferred_speed: float = 1.0
    auto_play_audio: bool = True
    save_history: bool = True
    max_history_items: int = 1000
    remember_symbols: bool = True
    interface_theme: str = "auto"  # auto, light, dark
    recently_used_expressions: List[str] = field(default_factory=list)
    favorite_expressions: List[str] = field(default_factory=list)

# ===========================
# Main Configuration Class
# ===========================

class Config:
    """Main configuration manager for MathSpeak"""
    
    def __init__(self, config_dir: Optional[Path] = None):
        self.config_dir = Path(config_dir) if config_dir else DEFAULT_CONFIG_DIR
        self.config_file = self.config_dir / DEFAULT_CONFIG_FILE
        self.user_prefs_file = self.config_dir / DEFAULT_USER_PREFS_FILE
        
        # Initialize all configuration sections
        self.voice = VoiceConfig()
        self.domains = DomainConfig()
        self.processing = ProcessingConfig()
        self.output = OutputConfig()
        self.natural_language = NaturalLanguageConfig()
        self.debug = DebugConfig()
        self.user_preferences = UserPreferences()
        
        # Configuration metadata
        self.version = CONFIG_VERSION
        self.last_modified = None
        
        # Load configuration
        self._ensure_config_dir()
        self.load()
        
        logger.info(f"Configuration loaded from {self.config_dir}")
    
    def _ensure_config_dir(self) -> None:
        """Ensure configuration directory exists"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def load(self) -> None:
        """Load configuration from files"""
        # Load main configuration
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._load_from_dict(data)
                logger.info("Loaded configuration from file")
            except Exception as e:
                logger.error(f"Failed to load configuration: {e}")
                logger.info("Using default configuration")
        else:
            logger.info("No configuration file found, using defaults")
            self.save()  # Save defaults
        
        # Load user preferences
        if self.user_prefs_file.exists():
            try:
                with open(self.user_prefs_file, 'r', encoding='utf-8') as f:
                    prefs_data = json.load(f)
                    self._load_user_preferences(prefs_data)
                logger.info("Loaded user preferences")
            except Exception as e:
                logger.error(f"Failed to load user preferences: {e}")
    
    def save(self) -> None:
        """Save configuration to files"""
        try:
            # Save main configuration
            config_data = self._to_dict()
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            # Save user preferences separately
            prefs_data = asdict(self.user_preferences)
            with open(self.user_prefs_file, 'w', encoding='utf-8') as f:
                json.dump(prefs_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
    
    def _load_from_dict(self, data: Dict[str, Any]) -> None:
        """Load configuration from dictionary"""
        # Check version
        file_version = data.get('version', '0.0.0')
        if file_version != CONFIG_VERSION:
            logger.warning(f"Configuration version mismatch: {file_version} vs {CONFIG_VERSION}")
            # Future: Add migration logic here
        
        # Load each section
        if 'voice' in data:
            self.voice = VoiceConfig(**data['voice'])
        if 'domains' in data:
            self.domains = DomainConfig(**data['domains'])
        if 'processing' in data:
            # Convert enum strings back to enums
            proc_data = data['processing'].copy()
            if 'mode' in proc_data:
                proc_data['mode'] = ProcessingMode(proc_data['mode'])
            self.processing = ProcessingConfig(**proc_data)
        if 'output' in data:
            out_data = data['output'].copy()
            if 'format' in out_data:
                out_data['format'] = OutputFormat(out_data['format'])
            if 'quality' in out_data:
                out_data['quality'] = QualityLevel(out_data['quality'])
            self.output = OutputConfig(**out_data)
        if 'natural_language' in data:
            self.natural_language = NaturalLanguageConfig(**data['natural_language'])
        if 'debug' in data:
            self.debug = DebugConfig(**data['debug'])
    
    def _to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'version': self.version,
            'voice': asdict(self.voice),
            'domains': asdict(self.domains),
            'processing': {
                **asdict(self.processing),
                'mode': self.processing.mode.value
            },
            'output': {
                **asdict(self.output),
                'format': self.output.format.value,
                'quality': self.output.quality.value
            },
            'natural_language': asdict(self.natural_language),
            'debug': asdict(self.debug),
        }
    
    def _load_user_preferences(self, data: Dict[str, Any]) -> None:
        """Load user preferences from dictionary"""
        self.user_preferences = UserPreferences(**data)
    
    # ===== Configuration Access Methods =====
    
    def get_voice_settings(self) -> VoiceConfig:
        """Get voice configuration"""
        return self.voice
    
    def get_enabled_domains(self) -> List[str]:
        """Get list of enabled domains"""
        return self.domains.enabled_domains
    
    def is_domain_enabled(self, domain: str) -> bool:
        """Check if a domain is enabled"""
        return domain in self.domains.enabled_domains
    
    def get_processing_mode(self) -> ProcessingMode:
        """Get current processing mode"""
        return self.processing.mode
    
    def get_output_settings(self) -> OutputConfig:
        """Get output configuration"""
        return self.output
    
    def get_cache_settings(self) -> Dict[str, Any]:
        """Get cache-related settings"""
        return {
            'enabled': self.processing.enable_caching,
            'size_mb': self.processing.cache_size_mb,
        }
    
    # ===== Configuration Update Methods =====
    
    def set_voice_speed(self, speed: float) -> None:
        """Set voice speed multiplier"""
        self.voice.speed_multiplier = max(0.5, min(2.0, speed))
        self.save()
    
    def set_processing_mode(self, mode: Union[str, ProcessingMode]) -> None:
        """Set processing mode"""
        if isinstance(mode, str):
            mode = ProcessingMode(mode)
        self.processing.mode = mode
        
        # Adjust related settings based on mode
        if mode == ProcessingMode.FAST:
            self.processing.enable_caching = True
            self.natural_language.add_clarifications = False
            self.natural_language.variation_frequency = 0.3
        elif mode == ProcessingMode.QUALITY:
            self.processing.enable_caching = True
            self.natural_language.add_clarifications = True
            self.natural_language.variation_frequency = 0.9
        
        self.save()
    
    def enable_domain(self, domain: str) -> None:
        """Enable a mathematical domain"""
        if domain not in self.domains.enabled_domains:
            self.domains.enabled_domains.append(domain)
            self.save()
    
    def disable_domain(self, domain: str) -> None:
        """Disable a mathematical domain"""
        if domain in self.domains.enabled_domains:
            self.domains.enabled_domains.remove(domain)
            self.save()
    
    def add_favorite_expression(self, expression: str) -> None:
        """Add expression to favorites"""
        if expression not in self.user_preferences.favorite_expressions:
            self.user_preferences.favorite_expressions.append(expression)
            # Limit favorites
            if len(self.user_preferences.favorite_expressions) > 100:
                self.user_preferences.favorite_expressions.pop(0)
            self.save()
    
    def update_recent_expression(self, expression: str) -> None:
        """Update recently used expressions"""
        recent = self.user_preferences.recently_used_expressions
        if expression in recent:
            recent.remove(expression)
        recent.insert(0, expression)
        # Limit recent items
        if len(recent) > 50:
            recent.pop()
        self.save()
    
    # ===== Configuration Validation =====
    
    def validate(self) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        # Voice settings
        if not 0.5 <= self.voice.speed_multiplier <= 2.0:
            issues.append(f"Voice speed {self.voice.speed_multiplier} out of range [0.5, 2.0]")
        
        # Processing settings
        if self.processing.worker_threads < 1:
            issues.append("Worker threads must be at least 1")
        if self.processing.cache_size_mb < 10:
            issues.append("Cache size should be at least 10 MB")
        
        # Output settings
        if self.output.sample_rate not in [16000, 22050, 44100, 48000]:
            issues.append(f"Unusual sample rate: {self.output.sample_rate}")
        
        # Domain settings
        if not self.domains.enabled_domains:
            issues.append("No domains enabled")
        
        return issues
    
    def reset_to_defaults(self) -> None:
        """Reset all configuration to defaults"""
        self.voice = VoiceConfig()
        self.domains = DomainConfig()
        self.processing = ProcessingConfig()
        self.output = OutputConfig()
        self.natural_language = NaturalLanguageConfig()
        self.debug = DebugConfig()
        self.user_preferences = UserPreferences()
        self.save()
        logger.info("Configuration reset to defaults")
    
    def export_config(self, filepath: Path) -> None:
        """Export configuration to a file"""
        try:
            config_data = self._to_dict()
            config_data['user_preferences'] = asdict(self.user_preferences)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuration exported to {filepath}")
        except Exception as e:
            logger.error(f"Failed to export configuration: {e}")
            raise
    
    def import_config(self, filepath: Path) -> None:
        """Import configuration from a file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load main config
            if 'user_preferences' in data:
                prefs_data = data.pop('user_preferences')
                self._load_user_preferences(prefs_data)
            
            self._load_from_dict(data)
            self.save()
            
            logger.info(f"Configuration imported from {filepath}")
        except Exception as e:
            logger.error(f"Failed to import configuration: {e}")
            raise

# ===========================
# Configuration Helpers
# ===========================

def get_default_config() -> Config:
    """Get default configuration instance"""
    return Config()

def load_config_from_env() -> Config:
    """Load configuration with environment variable overrides"""
    config = Config()
    
    # Override from environment variables
    if 'MATHSPEAK_VOICE_SPEED' in os.environ:
        try:
            config.voice.speed_multiplier = float(os.environ['MATHSPEAK_VOICE_SPEED'])
        except ValueError:
            pass
    
    if 'MATHSPEAK_DEBUG' in os.environ:
        config.debug.debug_mode = os.environ['MATHSPEAK_DEBUG'].lower() in ('1', 'true', 'yes')
    
    if 'MATHSPEAK_CACHE_DIR' in os.environ:
        # This would be used by the caching system
        pass
    
    return config

# ===========================
# Testing Functions
# ===========================

def test_config():
    """Test configuration functionality"""
    import tempfile
    
    # Create temporary config directory
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(config_dir=tmpdir)
        
        print("Testing Configuration System")
        print("=" * 50)
        
        # Test basic operations
        print("\nDefault voice speed:", config.voice.speed_multiplier)
        config.set_voice_speed(1.5)
        print("Updated voice speed:", config.voice.speed_multiplier)
        
        # Test domain management
        print("\nEnabled domains:", config.get_enabled_domains())
        config.disable_domain("algebra")
        print("After disabling algebra:", config.get_enabled_domains())
        
        # Test processing modes
        print("\nCurrent mode:", config.get_processing_mode().value)
        config.set_processing_mode(ProcessingMode.FAST)
        print("After setting FAST mode:", config.get_processing_mode().value)
        
        # Test validation
        issues = config.validate()
        print("\nValidation issues:", issues if issues else "None")
        
        # Test export/import
        export_path = Path(tmpdir) / "exported_config.json"
        config.export_config(export_path)
        print(f"\nExported configuration to {export_path}")
        
        # Reset and re-import
        config.reset_to_defaults()
        print("Reset to defaults")
        config.import_config(export_path)
        print("Re-imported configuration")
        print("Voice speed after import:", config.voice.speed_multiplier)

if __name__ == "__main__":
    test_config()