"""Configuration management for MathSpeak Clean Architecture."""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

from mathspeak_clean.shared.constants import (
    DEFAULT_AUDIENCE_LEVEL,
    DEFAULT_CACHE_TTL,
    DEFAULT_LOG_LEVEL,
    DEFAULT_MAX_EXPRESSION_LENGTH,
    DEFAULT_PATTERN_TIMEOUT,
)
from mathspeak_clean.shared.exceptions import ConfigurationError
from mathspeak_clean.shared.types import AudienceLevel, SystemConfig, VoiceConfig


@dataclass
class Settings:
    """System-wide configuration settings."""
    
    # Core settings
    default_audience_level: AudienceLevel = DEFAULT_AUDIENCE_LEVEL
    max_expression_length: int = DEFAULT_MAX_EXPRESSION_LENGTH
    pattern_timeout: float = DEFAULT_PATTERN_TIMEOUT
    
    # Cache settings
    cache_enabled: bool = True
    cache_ttl: int = DEFAULT_CACHE_TTL
    cache_max_size: int = 1000
    
    # TTS settings
    default_voice: VoiceConfig = field(default_factory=lambda: {
        "name": "en-US-AriaNeural",
        "language": "en-US",
        "speed": 1.0,
        "pitch": 1.0,
        "volume": 1.0,
    })
    fallback_voices: list[VoiceConfig] = field(default_factory=lambda: [
        {"name": "en-US-GuyNeural", "language": "en-US"},
        {"name": "espeak", "language": "en"},
    ])
    
    # Logging settings
    log_level: str = DEFAULT_LOG_LEVEL
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    api_cors_origins: list[str] = field(default_factory=lambda: ["*"])
    
    # Pattern settings
    pattern_directories: list[str] = field(default_factory=lambda: [
        "mathspeak/core/patterns",
        "mathspeak/domains",
    ])
    enable_pattern_caching: bool = True
    
    # Performance settings
    enable_profiling: bool = False
    profile_output_dir: str = "profiles"
    max_concurrent_requests: int = 100
    request_timeout: float = 30.0
    
    # Development settings
    debug_mode: bool = False
    enable_hot_reload: bool = False
    
    def validate(self) -> None:
        """Validate settings.
        
        Raises:
            ConfigurationError: If settings are invalid
        """
        # Validate audience level
        valid_levels = ["elementary", "high_school", "undergraduate", "graduate", "research"]
        if self.default_audience_level not in valid_levels:
            raise ConfigurationError(
                "default_audience_level",
                f"Must be one of {valid_levels}",
                self.default_audience_level
            )
        
        # Validate numeric ranges
        if self.max_expression_length <= 0:
            raise ConfigurationError(
                "max_expression_length",
                "Must be positive",
                self.max_expression_length
            )
        
        if self.pattern_timeout <= 0:
            raise ConfigurationError(
                "pattern_timeout",
                "Must be positive",
                self.pattern_timeout
            )
        
        if self.cache_ttl < 0:
            raise ConfigurationError(
                "cache_ttl",
                "Must be non-negative",
                self.cache_ttl
            )
        
        # Validate log level
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.log_level.upper() not in valid_log_levels:
            raise ConfigurationError(
                "log_level",
                f"Must be one of {valid_log_levels}",
                self.log_level
            )
        
        # Validate API settings
        if not 0 <= self.api_port <= 65535:
            raise ConfigurationError(
                "api_port",
                "Must be between 0 and 65535",
                self.api_port
            )
        
        if self.api_workers <= 0:
            raise ConfigurationError(
                "api_workers",
                "Must be positive",
                self.api_workers
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert settings to dictionary.
        
        Returns:
            Dictionary representation
        """
        return {
            "default_audience_level": self.default_audience_level,
            "max_expression_length": self.max_expression_length,
            "pattern_timeout": self.pattern_timeout,
            "cache_enabled": self.cache_enabled,
            "cache_ttl": self.cache_ttl,
            "cache_max_size": self.cache_max_size,
            "default_voice": self.default_voice,
            "fallback_voices": self.fallback_voices,
            "log_level": self.log_level,
            "log_format": self.log_format,
            "log_file": self.log_file,
            "api_host": self.api_host,
            "api_port": self.api_port,
            "api_workers": self.api_workers,
            "api_cors_origins": self.api_cors_origins,
            "pattern_directories": self.pattern_directories,
            "enable_pattern_caching": self.enable_pattern_caching,
            "enable_profiling": self.enable_profiling,
            "profile_output_dir": self.profile_output_dir,
            "max_concurrent_requests": self.max_concurrent_requests,
            "request_timeout": self.request_timeout,
            "debug_mode": self.debug_mode,
            "enable_hot_reload": self.enable_hot_reload,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Settings":
        """Create settings from dictionary.
        
        Args:
            data: Dictionary with settings
            
        Returns:
            Settings instance
        """
        return cls(**data)
    
    @classmethod
    def from_json_file(cls, file_path: str) -> "Settings":
        """Load settings from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Settings instance
            
        Raises:
            ConfigurationError: If file cannot be loaded
        """
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            return cls.from_dict(data)
        except FileNotFoundError:
            raise ConfigurationError(
                "settings_file",
                f"File not found: {file_path}"
            )
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                "settings_file",
                f"Invalid JSON in {file_path}: {e}"
            )
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Load settings from environment variables.
        
        Environment variables are prefixed with MATHSPEAK_.
        
        Returns:
            Settings instance
        """
        settings = cls()
        
        # Map environment variables to settings
        env_mappings = {
            "MATHSPEAK_AUDIENCE_LEVEL": ("default_audience_level", str),
            "MATHSPEAK_MAX_EXPRESSION_LENGTH": ("max_expression_length", int),
            "MATHSPEAK_PATTERN_TIMEOUT": ("pattern_timeout", float),
            "MATHSPEAK_CACHE_ENABLED": ("cache_enabled", lambda x: x.lower() == "true"),
            "MATHSPEAK_CACHE_TTL": ("cache_ttl", int),
            "MATHSPEAK_CACHE_MAX_SIZE": ("cache_max_size", int),
            "MATHSPEAK_LOG_LEVEL": ("log_level", str),
            "MATHSPEAK_LOG_FILE": ("log_file", str),
            "MATHSPEAK_API_HOST": ("api_host", str),
            "MATHSPEAK_API_PORT": ("api_port", int),
            "MATHSPEAK_API_WORKERS": ("api_workers", int),
            "MATHSPEAK_DEBUG": ("debug_mode", lambda x: x.lower() == "true"),
        }
        
        for env_var, (attr_name, converter) in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                try:
                    setattr(settings, attr_name, converter(value))
                except ValueError as e:
                    raise ConfigurationError(
                        env_var,
                        f"Invalid value: {e}",
                        value
                    )
        
        return settings
    
    def save_to_json(self, file_path: str) -> None:
        """Save settings to JSON file.
        
        Args:
            file_path: Path to save to
        """
        with open(file_path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get global settings instance.
    
    Returns:
        Settings instance
    """
    global _settings
    
    if _settings is None:
        # Try to load from file first
        config_file = os.environ.get("MATHSPEAK_CONFIG_FILE", "mathspeak.json")
        if Path(config_file).exists():
            _settings = Settings.from_json_file(config_file)
        else:
            # Fall back to environment variables
            _settings = Settings.from_env()
        
        # Validate settings
        _settings.validate()
    
    return _settings


def reset_settings() -> None:
    """Reset global settings (mainly for testing)."""
    global _settings
    _settings = None