"""
Mathematical Speech Patterns Package
====================================

This package contains the refactored mathematical speech patterns,
organized into focused modules for better maintainability.

Structure:
- base.py: Abstract base classes and core types
- arithmetic.py: Basic arithmetic patterns
- algebra.py: Algebraic expression patterns
- calculus.py: Calculus and analysis patterns
- linear_algebra.py: Linear algebra patterns
- set_theory.py: Set theory and logic patterns
- special_symbols.py: Special mathematical symbols
- processor.py: Main pattern processing engine
"""

# Import main classes for backward compatibility
from .base import (
    AudienceLevel,
    MathDomain,
    PatternRule,
    PatternHandler,
    DomainProcessor
)
from .processor import MathSpeechProcessor
from .special_symbols import SpecialSymbolsHandler

__all__ = [
    'AudienceLevel',
    'MathDomain', 
    'PatternRule',
    'PatternHandler',
    'DomainProcessor',
    'MathSpeechProcessor',
    'SpecialSymbolsHandler'
]