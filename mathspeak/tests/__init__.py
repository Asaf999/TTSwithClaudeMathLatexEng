"""
Test utilities and shared fixtures for MathSpeak tests.
"""

from typing import List, Tuple, Dict, Any
import pytest
from pathlib import Path
import time


def get_test_expressions() -> List[Tuple[str, str]]:
    """
    Get a list of test mathematical expressions with expected outputs.
    
    Returns:
        List of tuples (latex_expression, expected_phrase_fragment)
    """
    return [
        # Basic algebra
        ("x^2", "x squared"),
        ("\\sqrt{x}", "square root of x"),
        ("\\frac{a}{b}", "a over b"),
        
        # Calculus
        ("\\int_0^\\infty", "integral from 0 to infinity"),
        ("\\frac{d}{dx}", "d over d x"),
        ("\\lim_{x \\to 0}", "limit as x approaches 0"),
        
        # Complex analysis
        ("e^{i\\pi}", "e to the i pi"),
        ("\\Re(z)", "real part of z"),
        
        # Topology
        ("T_2", "T 2"),
        ("\\mathcal{T}", "script T"),
        
        # Numerical analysis
        ("O(n^2)", "order n squared"),
        ("x_{k+1}", "x sub k plus 1"),
    ]


def get_sample_math_context() -> Dict[str, Any]:
    """
    Get a sample mathematical context for testing.
    
    Returns:
        Dictionary with context information
    """
    return {
        'in_definition': False,
        'in_theorem': False,
        'in_proof': False,
        'current_domain': 'general',
        'defined_symbols': {
            'x': 'real variable',
            'f': 'function',
            'A': 'matrix'
        }
    }


def assert_speech_quality(text: str) -> None:
    """
    Assert that generated speech meets quality standards.
    
    Args:
        text: The generated speech text
        
    Raises:
        AssertionError: If quality standards are not met
    """
    # Should not contain raw LaTeX commands
    assert not any(char in text for char in ['\\', '{', '}']), \
        f"Speech contains LaTeX artifacts: {text}"
    
    # Should not be empty
    assert text.strip(), "Generated speech is empty"
    
    # Should not have excessive whitespace
    assert '  ' not in text, f"Speech has excessive whitespace: {text}"
    
    # Should end with proper punctuation or be a fragment
    last_char = text.strip()[-1] if text.strip() else ''
    assert last_char in '.!?,:;' or len(text.split()) < 5, \
        f"Speech should end with punctuation or be a short fragment: {text}"


# Common test configuration
TEST_CONFIG = {
    'cache_enabled': False,
    'debug': True,
    'stats_enabled': False,
    'voice_enabled': False
}


# Sample LaTeX documents for integration testing
SAMPLE_DOCUMENTS = {
    'basic_calculus': """
Let $f(x) = x^2 + 3x + 2$. The derivative is:
$$f'(x) = 2x + 3$$

The integral is:
$$\\int f(x)dx = \\frac{x^3}{3} + \\frac{3x^2}{2} + 2x + C$$
""",
    
    'complex_analysis': """
Consider the complex function $f(z) = e^z$. By Euler's formula:
$$e^{i\\theta} = \\cos\\theta + i\\sin\\theta$$

For $\\theta = \\pi$, we get $e^{i\\pi} = -1$.
""",
    
    'topology': """
A topological space $(X, \\tau)$ is called $T_2$ (Hausdorff) if for any 
two distinct points $x, y \\in X$, there exist disjoint open sets 
$U, V \\in \\tau$ such that $x \\in U$ and $y \\in V$.
"""
}


def assert_contains_all(text: str, phrases: List[str]) -> None:
    """
    Assert that text contains all given phrases.
    
    Args:
        text: The text to check
        phrases: List of phrases that should be in the text
        
    Raises:
        AssertionError: If any phrase is missing
    """
    text_lower = text.lower()
    missing = [phrase for phrase in phrases if phrase.lower() not in text_lower]
    assert not missing, f"Missing phrases: {missing} in text: {text}"


def assert_natural_language(text: str) -> None:
    """
    Assert that text reads as natural language.
    
    Args:
        text: The text to check
        
    Raises:
        AssertionError: If text doesn't meet naturalness criteria
    """
    # Check for proper sentence structure
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    for sentence in sentences:
        words = sentence.split()
        if len(words) > 2:  # Skip very short fragments
            # Should start with capital letter
            assert words[0][0].isupper() or words[0][0].isdigit(), \
                f"Sentence should start with capital: {sentence}"
    
    # Should not have LaTeX artifacts
    assert_speech_quality(text)


def create_mock_config() -> Dict[str, Any]:
    """
    Create a mock configuration for testing.
    
    Returns:
        Dictionary with test configuration
    """
    return {
        **TEST_CONFIG,
        'domains': {
            'enabled': ['topology', 'complex_analysis', 'numerical_analysis'],
            'default': 'general'
        },
        'voice': {
            'default_role': 'narrator',
            'speed': 1.0
        }
    }


class PerformanceTimer:
    """Context manager for timing code execution."""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.elapsed = None
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start_time
        print(f"\n{self.name} took {self.elapsed:.4f} seconds")
        return False