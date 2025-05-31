"""Type definitions for MathSpeak Clean Architecture."""

from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    NamedTuple,
    Optional,
    Protocol,
    Tuple,
    TypedDict,
    Union,
    runtime_checkable,
)

# Type aliases for common types
LaTeXExpression = str
SpeechText = str
PatternPriority = int
MatchPosition = Tuple[int, int]
PatternFlags = int

# Audience levels
AudienceLevel = Literal["elementary", "high_school", "undergraduate", "graduate", "research"]

# Voice configuration types
class VoiceConfig(TypedDict, total=False):
    """Configuration for TTS voice."""
    
    name: str
    language: str
    gender: Optional[str]
    speed: Optional[float]
    pitch: Optional[float]
    volume: Optional[float]


class ProcessingResult(NamedTuple):
    """Result of processing a mathematical expression."""
    
    latex: LaTeXExpression
    speech: SpeechText
    audience_level: AudienceLevel
    processing_time: float
    cache_hit: bool = False
    warnings: List[str] = []


class PatternMatch(NamedTuple):
    """Information about a pattern match."""
    
    pattern: str
    replacement: str
    position: MatchPosition
    priority: PatternPriority
    domain: str


class DomainInfo(TypedDict):
    """Information about a mathematical domain."""
    
    name: str
    description: str
    priority: int
    patterns_count: int
    enabled: bool


# Protocol definitions for interfaces
@runtime_checkable
class PatternProcessor(Protocol):
    """Protocol for pattern processing."""
    
    def process(self, latex: LaTeXExpression, level: AudienceLevel) -> SpeechText:
        """Process LaTeX expression to speech text."""
        ...
    
    def add_pattern(self, pattern: str, replacement: str, priority: int) -> None:
        """Add a new pattern."""
        ...
    
    def get_patterns(self) -> List[Tuple[str, str, int]]:
        """Get all patterns."""
        ...


@runtime_checkable
class TTSEngine(Protocol):
    """Protocol for text-to-speech engines."""
    
    def speak(self, text: str, voice: VoiceConfig) -> bytes:
        """Convert text to speech audio."""
        ...
    
    def list_voices(self) -> List[VoiceConfig]:
        """List available voices."""
        ...
    
    def is_available(self) -> bool:
        """Check if engine is available."""
        ...


@runtime_checkable
class Cache(Protocol):
    """Protocol for caching."""
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        ...
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        ...
    
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        ...
    
    def clear(self) -> None:
        """Clear all cache."""
        ...


# Domain-specific types
MathematicalDomain = Literal[
    "algebra",
    "calculus", 
    "linear_algebra",
    "statistics",
    "number_theory",
    "set_theory",
    "logic",
    "topology",
    "complex_analysis",
    "real_analysis",
    "combinatorics",
]

# Pattern transformation function type
PatternTransform = Callable[[str], str]

# Configuration types
class SystemConfig(TypedDict):
    """System-wide configuration."""
    
    default_audience_level: AudienceLevel
    cache_enabled: bool
    cache_ttl: int
    max_expression_length: int
    default_voice: VoiceConfig
    log_level: str
    pattern_timeout: float