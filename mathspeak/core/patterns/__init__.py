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
from .arithmetic import BasicArithmeticHandler
from .algebra import AlgebraHandler
from .calculus import CalculusHandler

# Import backward compatibility classes from the original patterns module
try:
    from ..patterns import (
        PatternProcessor,
        PatternCategory,
        MathematicalPattern,
        EpsilonDeltaHandler,
        LimitPatternHandler,
        SequenceSeriesHandler,
        SetNotationHandler,
        ProofPatternHandler,
        ReferencePatternHandler,
        CommonExpressionHandler,
        apply_common_patterns,
        apply_epsilon_delta_patterns,
        apply_proof_patterns,
    )
except ImportError as e:
    # Create placeholder imports if the patterns module doesn't have these
    PatternProcessor = None
    PatternCategory = None
    MathematicalPattern = None
    EpsilonDeltaHandler = None
    LimitPatternHandler = None
    SequenceSeriesHandler = None
    SetNotationHandler = None
    ProofPatternHandler = None
    ReferencePatternHandler = None
    CommonExpressionHandler = None
    apply_common_patterns = None
    apply_epsilon_delta_patterns = None
    apply_proof_patterns = None

# Note: Some imports may fail if modules don't exist yet
try:
    from .processor import MathSpeechProcessor
except ImportError:
    pass

try:
    from .special_symbols import SpecialSymbolsHandler
except ImportError:
    pass

__all__ = [
    'AudienceLevel',
    'MathDomain', 
    'PatternRule',
    'PatternHandler',
    'DomainProcessor',
    'BasicArithmeticHandler',
    'AlgebraHandler',
    'CalculusHandler',
    # Backward compatibility exports
    'PatternProcessor',
    'PatternCategory',
    'MathematicalPattern',
    'EpsilonDeltaHandler',
    'LimitPatternHandler',
    'SequenceSeriesHandler',
    'SetNotationHandler',
    'ProofPatternHandler',
    'ReferencePatternHandler',
    'CommonExpressionHandler',
    'apply_common_patterns',
    'apply_epsilon_delta_patterns',
    'apply_proof_patterns'
]