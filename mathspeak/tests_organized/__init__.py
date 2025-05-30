"""
MathSpeak Test Suite
===================

Organized test structure for the MathSpeak mathematical TTS system.

Structure:
    unit/       - Unit tests for individual components
    integration/ - Integration tests between components  
    performance/ - Performance and benchmark tests
    docs/       - Documentation tests and examples

Test Categories:
    - Core functionality (engine, patterns, voice manager)
    - Domain processors (topology, complex analysis, etc.)
    - Utilities (config, logging, validators)
    - TTS engines and audio generation
    - CLI and user interfaces
    - Performance and scalability

Use pytest markers to run specific test categories:
    pytest -m unit           # Unit tests only
    pytest -m integration    # Integration tests
    pytest -m performance    # Performance tests
    pytest -m "not slow"     # Skip slow tests
"""

import pytest
import sys
from pathlib import Path

# Add the parent directory to the path for imports
test_dir = Path(__file__).parent
mathspeak_dir = test_dir.parent
sys.path.insert(0, str(mathspeak_dir))

# Test configuration
pytest_plugins = [
    "pytest_asyncio",
    "pytest_cov",
    "pytest_mock",
    "pytest_benchmark",
]

# Common test fixtures and utilities
@pytest.fixture(scope="session")
def mathspeak_config():
    """Session-wide MathSpeak configuration for testing"""
    from mathspeak.utils import Config
    return Config(debug=True, cache_enabled=False)

@pytest.fixture(scope="session") 
def test_expressions():
    """Collection of test mathematical expressions"""
    return {
        "basic": [
            "x + y = z",
            "a^2 + b^2 = c^2", 
            "\\frac{1}{2} + \\frac{1}{3} = \\frac{5}{6}",
        ],
        "calculus": [
            "\\int_0^1 x^2 dx = \\frac{1}{3}",
            "\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1",
            "\\frac{d}{dx} x^n = nx^{n-1}",
        ],
        "complex": [
            "z = re^{i\\theta}",
            "\\oint_C f(z) dz = 2\\pi i \\sum \\text{Res}(f)",
            "|z|^2 = z\\bar{z}",
        ],
        "topology": [
            "\\overline{A} = A \\cup A'",
            "\\text{int}(A) = A \\setminus \\partial A",
            "X \\text{ is compact} \\Leftrightarrow X \\text{ is closed and bounded}",
        ]
    }

@pytest.fixture
def mock_tts_engine():
    """Mock TTS engine for testing without audio generation"""
    from unittest.mock import Mock, AsyncMock
    
    engine = Mock()
    engine.is_available.return_value = True
    engine.name = "MockTTS"
    engine.requires_internet = False
    engine.synthesize = AsyncMock(return_value=Mock(success=True))
    
    return engine

@pytest.fixture
def temp_audio_file(tmp_path):
    """Temporary audio file for testing"""
    return tmp_path / "test_output.mp3"

# Test utilities
def skip_if_no_internet():
    """Skip test if no internet connection"""
    import socket
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return False
    except OSError:
        return pytest.mark.skip(reason="No internet connection")

def skip_if_no_tts():
    """Skip test if TTS engines not available"""
    try:
        import edge_tts
        return False
    except ImportError:
        return pytest.mark.skip(reason="TTS engines not available")

def assert_valid_speech_output(text: str):
    """Assert that speech output is valid"""
    assert isinstance(text, str)
    assert len(text) > 0
    assert not any(c in text for c in "\\{}_^")  # No LaTeX symbols
    assert text.strip() == text  # No leading/trailing whitespace

def assert_performance_threshold(duration: float, max_seconds: float):
    """Assert performance meets threshold"""
    assert duration <= max_seconds, f"Performance threshold exceeded: {duration:.3f}s > {max_seconds}s"