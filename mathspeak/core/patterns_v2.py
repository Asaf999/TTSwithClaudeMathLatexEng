#!/usr/bin/env python3
"""
Comprehensive Mathematical Speech Patterns v2
============================================

This module implements natural speech patterns for mathematical expressions,
focusing on how real professors speak mathematics. It includes:

1. All 100 example patterns from the guide
2. Generalization rules for unseen expressions
3. Context-aware adaptation for different audiences
4. Domain-specific pattern classes

Key principles:
- Natural speech: "over" not "divided by" for fractions
- Powers: "squared", "cubed", "to the n"
- No technical jargon: no "underscore", "superscript", "symbol"
- Context-aware: adapts to audience level
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Union, Callable, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# ===========================
# Context and Audience Levels
# ===========================

class AudienceLevel(Enum):
    """Audience sophistication levels"""
    HIGH_SCHOOL = "high_school"
    UNDERGRADUATE = "undergraduate"
    GRADUATE = "graduate"
    RESEARCH = "research"

class MathDomain(Enum):
    """Mathematical domains for pattern categorization"""
    BASIC_ARITHMETIC = "basic_arithmetic"
    ALGEBRA = "algebra"
    FUNCTIONS = "functions"
    CALCULUS = "calculus"
    LINEAR_ALGEBRA = "linear_algebra"
    SET_THEORY = "set_theory"
    PROBABILITY = "probability"
    NUMBER_THEORY = "number_theory"
    COMPLEX_ANALYSIS = "complex_analysis"
    TOPOLOGY = "topology"
    LOGIC = "logic"
    DISCRETE_MATH = "discrete_math"

@dataclass
class PatternRule:
    """A mathematical pattern with its natural speech replacement"""
    pattern: str  # Regex pattern
    replacement: Union[str, Callable]  # Natural speech or function
    domain: MathDomain
    description: str
    priority: int = 50
    audience_levels: List[AudienceLevel] = None
    
    def __post_init__(self):
        self.compiled = re.compile(self.pattern)
        if self.audience_levels is None:
            self.audience_levels = list(AudienceLevel)

# ===========================
# Base Pattern Handler
# ===========================

class PatternHandler(ABC):
    """Abstract base class for pattern handlers"""
    
    def __init__(self, domain: MathDomain):
        self.domain = domain
        self.patterns: List[PatternRule] = []
        self._init_patterns()
    
    @abstractmethod
    def _init_patterns(self):
        """Initialize patterns for this handler"""
        pass
    
    def process(self, text: str, audience: AudienceLevel = AudienceLevel.UNDERGRADUATE) -> str:
        """Process text with patterns appropriate for audience"""
        result = text
        
        # Filter patterns by audience level
        applicable_patterns = [
            p for p in self.patterns 
            if audience in p.audience_levels
        ]
        
        # Sort by priority (highest first)
        applicable_patterns.sort(key=lambda p: p.priority, reverse=True)
        
        # Apply patterns
        for pattern in applicable_patterns:
            if callable(pattern.replacement):
                result = pattern.compiled.sub(pattern.replacement, result)
            else:
                result = pattern.compiled.sub(pattern.replacement, result)
        
        return result

# ===========================
# Basic Arithmetic Patterns
# ===========================

class BasicArithmeticHandler(PatternHandler):
    """Handles basic arithmetic operations naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Addition
            PatternRule(
                r'(\d+)\s*\+\s*(\d+)',
                lambda m: f'{m.group(1)} plus {m.group(2)}',
                self.domain,
                'Basic addition',
                priority=70
            ),
            PatternRule(
                r'([a-zA-Z])\s*\+\s*([a-zA-Z])',
                lambda m: f'{m.group(1)} plus {m.group(2)}',
                self.domain,
                'Variable addition',
                priority=70
            ),
            
            # Subtraction
            PatternRule(
                r'(\d+)\s*-\s*(\d+)',
                lambda m: f'{m.group(1)} minus {m.group(2)}',
                self.domain,
                'Basic subtraction',
                priority=70
            ),
            PatternRule(
                r'([a-zA-Z])\s*-\s*([a-zA-Z])',
                lambda m: f'{m.group(1)} minus {m.group(2)}',
                self.domain,
                'Variable subtraction',
                priority=70
            ),
            
            # Multiplication - natural speech
            PatternRule(
                r'(\d+)\s*\*\s*(\d+)',
                lambda m: f'{m.group(1)} times {m.group(2)}',
                self.domain,
                'Basic multiplication',
                priority=70
            ),
            PatternRule(
                r'(\d+)\s*×\s*(\d+)',
                lambda m: f'{m.group(1)} times {m.group(2)}',
                self.domain,
                'Multiplication with ×',
                priority=70
            ),
            PatternRule(
                r'(\d+)\s*\\cdot\s*(\d+)',
                lambda m: f'{m.group(1)} dot {m.group(2)}',
                self.domain,
                'Multiplication with cdot',
                priority=70
            ),
            # Note: Implicit multiplication is handled in the Algebra handler
            # to avoid conflicts with word processing
            
            # Division - using "over" naturally
            PatternRule(
                r'(\d+)\s*/\s*(\d+)',
                lambda m: f'{m.group(1)} over {m.group(2)}',
                self.domain,
                'Basic division',
                priority=70
            ),
            PatternRule(
                r'([a-zA-Z])\s*/\s*([a-zA-Z])',
                lambda m: f'{m.group(1)} over {m.group(2)}',
                self.domain,
                'Variable division',
                priority=70
            ),
            PatternRule(
                r'\\div',
                ' divided by ',
                self.domain,
                'Division symbol',
                priority=70
            ),
            
            # Mixed numbers
            PatternRule(
                r'(\d+)\\frac\{(\d+)\}\{(\d+)\}',
                lambda m: f'{m.group(1)} and {m.group(2)} over {m.group(3)}',
                self.domain,
                'Mixed number',
                priority=105  # Higher priority than regular fractions
            ),
            
            # Equals
            PatternRule(
                r'=',
                ' equals ',
                self.domain,
                'Equals sign',
                priority=60
            ),
            PatternRule(
                r'≠',
                ' is not equal to ',
                self.domain,
                'Not equals',
                priority=60
            ),
            PatternRule(
                r'\\neq',
                ' is not equal to ',
                self.domain,
                'LaTeX not equals',
                priority=60
            ),
            
            # Inequalities
            PatternRule(
                r'<',
                ' is less than ',
                self.domain,
                'Less than',
                priority=60
            ),
            PatternRule(
                r'>',
                ' is greater than ',
                self.domain,
                'Greater than',
                priority=60
            ),
            PatternRule(
                r'≤|\\leq',
                ' is less than or equal to ',
                self.domain,
                'Less than or equal',
                priority=60
            ),
            PatternRule(
                r'≥|\\geq',
                ' is greater than or equal to ',
                self.domain,
                'Greater than or equal',
                priority=60
            ),
            
            # Approximation
            PatternRule(
                r'≈|\\approx',
                ' is approximately ',
                self.domain,
                'Approximately equals',
                priority=60
            ),
            
            # Plus/minus
            PatternRule(
                r'±|\\pm',
                ' plus or minus ',
                self.domain,
                'Plus minus',
                priority=65
            ),
        ]

# ===========================
# Algebra Patterns
# ===========================

class AlgebraHandler(PatternHandler):
    """Handles algebraic expressions naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Powers - natural speech
            PatternRule(
                r'([a-zA-Z])\^2',
                lambda m: f'{m.group(1)} squared',
                self.domain,
                'Variable squared',
                priority=95
            ),
            PatternRule(
                r'([a-zA-Z])\^3',
                lambda m: f'{m.group(1)} cubed',
                self.domain,
                'Variable cubed',
                priority=95
            ),
            PatternRule(
                r'([a-zA-Z])\^n',
                lambda m: f'{m.group(1)} to the n',
                self.domain,
                'Variable to the n',
                priority=94
            ),
            PatternRule(
                r'([a-zA-Z])\^([a-zA-Z])',
                lambda m: f'{m.group(1)} to the {m.group(2)}',
                self.domain,
                'Variable to variable power',
                priority=93
            ),
            PatternRule(
                r'([a-zA-Z])\^\{([^}]+)\}',
                lambda m: f'{m.group(1)} to the {self._process_exponent(m.group(2))}',
                self.domain,
                'Variable to complex power',
                priority=92
            ),
            PatternRule(
                r'([a-zA-Z])\^(\d+)',
                lambda m: f'{m.group(1)} to the {self._number_to_power(m.group(2))}',
                self.domain,
                'Variable to numeric power',
                priority=93
            ),
            
            # Subscripts - natural reading
            PatternRule(
                r'([a-zA-Z])_0',
                lambda m: f'{m.group(1)} naught',
                self.domain,
                'Subscript 0',
                priority=90
            ),
            PatternRule(
                r'([a-zA-Z])_1',
                lambda m: f'{m.group(1)} one',
                self.domain,
                'Subscript 1',
                priority=90
            ),
            PatternRule(
                r'([a-zA-Z])_2',
                lambda m: f'{m.group(1)} two',
                self.domain,
                'Subscript 2',
                priority=90
            ),
            PatternRule(
                r'([a-zA-Z])_n',
                lambda m: f'{m.group(1)} n',
                self.domain,
                'Subscript n',
                priority=89
            ),
            PatternRule(
                r'([a-zA-Z])_i',
                lambda m: f'{m.group(1)} i',
                self.domain,
                'Subscript i',
                priority=89
            ),
            PatternRule(
                r'([a-zA-Z])_\{([^}]+)\}',
                lambda m: f'{m.group(1)} {self._process_subscript(m.group(2))}',
                self.domain,
                'Complex subscript',
                priority=88
            ),
            PatternRule(
                r'([a-zA-Z])_([a-zA-Z0-9]+)',
                lambda m: f'{m.group(1)} {m.group(2)}',
                self.domain,
                'General subscript',
                priority=87
            ),
            
            # Fractions - always use "over"
            PatternRule(
                r'\\frac\{1\}\{2\}',
                'one half',
                self.domain,
                'One half',
                priority=100
            ),
            PatternRule(
                r'\\frac\{1\}\{3\}',
                'one third',
                self.domain,
                'One third',
                priority=100
            ),
            PatternRule(
                r'\\frac\{1\}\{4\}',
                'one quarter',
                self.domain,
                'One quarter',
                priority=100
            ),
            PatternRule(
                r'\\frac\{2\}\{3\}',
                'two thirds',
                self.domain,
                'Two thirds',
                priority=100
            ),
            PatternRule(
                r'\\frac\{3\}\{4\}',
                'three quarters',
                self.domain,
                'Three quarters',
                priority=100
            ),
            PatternRule(
                r'\\frac\{([a-zA-Z])\}\{([a-zA-Z])\}',
                lambda m: f'{m.group(1)} over {m.group(2)}',
                self.domain,
                'Variable fraction',
                priority=98
            ),
            PatternRule(
                r'\\frac\{([^}]+)\}\{([^}]+)\}',
                lambda m: f'{m.group(1)} over {m.group(2)}',
                self.domain,
                'General fraction',
                priority=97
            ),
            
            # Roots
            PatternRule(
                r'\\sqrt\{2\}',
                'square root of 2',
                self.domain,
                'Square root of 2',
                priority=95
            ),
            PatternRule(
                r'\\sqrt\{3\}',
                'square root of 3',
                self.domain,
                'Square root of 3',
                priority=95
            ),
            PatternRule(
                r'\\sqrt\{([a-zA-Z])\}',
                lambda m: f'square root of {m.group(1)}',
                self.domain,
                'Square root of variable',
                priority=94
            ),
            PatternRule(
                r'\\sqrt\{([^}]+)\}',
                lambda m: f'square root of {m.group(1)}',
                self.domain,
                'General square root',
                priority=93
            ),
            PatternRule(
                r'\\sqrt\[3\]\{([^}]+)\}',
                lambda m: f'cube root of {m.group(1)}',
                self.domain,
                'Cube root',
                priority=94
            ),
            PatternRule(
                r'\\sqrt\[n\]\{([^}]+)\}',
                lambda m: f'nth root of {m.group(1)}',
                self.domain,
                'nth root with n',
                priority=93
            ),
            PatternRule(
                r'\\sqrt\[(\d+)\]\{([^}]+)\}',
                lambda m: f'{self._ordinal(m.group(1))} root of {m.group(2)}',
                self.domain,
                'nth root',
                priority=93
            ),
            
            # Decorated variables
            PatternRule(
                r'\\tilde\{([a-zA-Z])\}',
                lambda m: f'{m.group(1)} tilde',
                self.domain,
                'Variable with tilde',
                priority=95
            ),
            PatternRule(
                r'\\hat\{([a-zA-Z])\}',
                lambda m: f'{m.group(1)} hat',
                self.domain,
                'Variable with hat',
                priority=95
            ),
            PatternRule(
                r'\\bar\{([a-zA-Z])\}',
                lambda m: f'{m.group(1)} bar',
                self.domain,
                'Variable with bar',
                priority=95
            ),
            
            # Polynomials
            PatternRule(
                r'ax\^2\s*\+\s*bx\s*\+\s*c',
                'a x squared plus b x plus c',
                self.domain,
                'Quadratic form',
                priority=96
            ),
            PatternRule(
                r'x\^2\s*\+\s*([0-9]+)x\s*\+\s*([0-9]+)',
                lambda m: f'x squared plus {m.group(1)} x plus {m.group(2)}',
                self.domain,
                'Specific quadratic',
                priority=96
            ),
            
            # Implicit multiplication - only for specific cases to avoid breaking words
            PatternRule(
                r'(\d+)([a-zA-Z])\b',
                lambda m: f'{m.group(1)} {m.group(2)}',
                self.domain,
                'Number times variable',
                priority=85
            ),
            PatternRule(
                r'\b([xyz])([xyz])\b',  # Only common math variables
                lambda m: f'{m.group(1)} {m.group(2)}' if m.group(1) != m.group(2) else f'{m.group(1)} squared',
                self.domain,
                'Common variables multiplied',
                priority=60
            ),
            
            # Binomial expansions
            PatternRule(
                r'\(([a-zA-Z])\s*\+\s*([a-zA-Z])\)\^2',
                lambda m: f'{m.group(1)} plus {m.group(2)}, quantity squared',
                self.domain,
                'Binomial squared',
                priority=95
            ),
            PatternRule(
                r'\(([a-zA-Z])\s*-\s*([a-zA-Z])\)\^2',
                lambda m: f'{m.group(1)} minus {m.group(2)}, quantity squared',
                self.domain,
                'Difference squared',
                priority=95
            ),
            
            # Absolute value
            PatternRule(
                r'\|([a-zA-Z])\|',
                lambda m: f'absolute value of {m.group(1)}',
                self.domain,
                'Absolute value',
                priority=90
            ),
            PatternRule(
                r'\|([^|]+)\|',
                lambda m: f'absolute value of {m.group(1)}',
                self.domain,
                'General absolute value',
                priority=89
            ),
        ]
    
    def _process_exponent(self, exp: str) -> str:
        """Process complex exponents naturally"""
        if exp == '2':
            return 'power of 2'
        elif exp == '3':
            return 'power of 3'
        elif exp == '-1':
            return 'negative 1'
        elif exp == 'n+1':
            return 'n plus 1'
        elif exp == 'n-1':
            return 'n minus 1'
        elif exp == '2n':
            return '2 n'
        else:
            return exp
    
    def _number_to_power(self, num: str) -> str:
        """Convert number to power expression"""
        if num == '2':
            return 'power of 2'
        elif num == '3':
            return 'power of 3'
        elif num == '4':
            return 'fourth'
        elif num == '5':
            return 'fifth'
        else:
            return f'power of {num}'
    
    def _process_subscript(self, sub: str) -> str:
        """Process complex subscripts naturally"""
        # Remove any remaining braces
        sub = sub.replace('{', '').replace('}', '')
        
        # Common patterns
        if sub == 'n+1':
            return 'n plus 1'
        elif sub == 'n-1':
            return 'n minus 1'
        elif sub == 'i+1':
            return 'i plus 1'
        elif sub == 'i,j':
            return 'i j'
        elif sub == 'ij':
            return 'i j'
        else:
            return sub
    
    def _ordinal(self, num: str) -> str:
        """Convert number to ordinal"""
        ordinals = {
            '2': 'square', '3': 'cube', '4': 'fourth', '5': 'fifth',
            '6': 'sixth', '7': 'seventh', '8': 'eighth', '9': 'ninth', '10': 'tenth'
        }
        return ordinals.get(num, f'{num}th')

# ===========================
# Function Patterns
# ===========================

class FunctionHandler(PatternHandler):
    """Handles function notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Basic function notation
            PatternRule(
                r'f\(([a-zA-Z])\)',
                lambda m: f'f of {m.group(1)}',
                self.domain,
                'Basic function',
                priority=95
            ),
            PatternRule(
                r'g\(([a-zA-Z])\)',
                lambda m: f'g of {m.group(1)}',
                self.domain,
                'Function g',
                priority=95
            ),
            PatternRule(
                r'h\(([a-zA-Z])\)',
                lambda m: f'h of {m.group(1)}',
                self.domain,
                'Function h',
                priority=95
            ),
            PatternRule(
                r'([fgh])\(([^)]+)\)',
                lambda m: f'{m.group(1)} of {m.group(2)}',
                self.domain,
                'General function',
                priority=94
            ),
            
            # Composition
            PatternRule(
                r'f\s*∘\s*g|f\s*\\circ\s*g',
                'f composed with g',
                self.domain,
                'Function composition',
                priority=96
            ),
            PatternRule(
                r'\(f\s*∘\s*g\)\(x\)|\(f\s*\\circ\s*g\)\(x\)',
                'f composed with g of x',
                self.domain,
                'Composition applied',
                priority=97
            ),
            
            # Common functions
            PatternRule(
                r'\\sin\s*([a-zA-Z])',
                lambda m: f'sine {m.group(1)}',
                self.domain,
                'Sine function',
                priority=95
            ),
            PatternRule(
                r'\\cos\s*([a-zA-Z])',
                lambda m: f'cosine {m.group(1)}',
                self.domain,
                'Cosine function',
                priority=95
            ),
            PatternRule(
                r'\\tan\s*([a-zA-Z])',
                lambda m: f'tangent {m.group(1)}',
                self.domain,
                'Tangent function',
                priority=95
            ),
            PatternRule(
                r'\\tan\s*\(([^)]+)\)',
                lambda m: f'tangent of {m.group(1)}',
                self.domain,
                'Tangent with parentheses',
                priority=94
            ),
            PatternRule(
                r'\\sin\s*\(([^)]+)\)',
                lambda m: f'sine of {m.group(1)}',
                self.domain,
                'Sine with parentheses',
                priority=94
            ),
            PatternRule(
                r'\\cos\s*\(([^)]+)\)',
                lambda m: f'cosine of {m.group(1)}',
                self.domain,
                'Cosine with parentheses',
                priority=94
            ),
            
            # Trig with powers
            PatternRule(
                r'\\sin\^2\s*([a-zA-Z])',
                lambda m: f'sine squared {m.group(1)}',
                self.domain,
                'Sine squared',
                priority=96
            ),
            PatternRule(
                r'\\cos\^2\s*([a-zA-Z])',
                lambda m: f'cosine squared {m.group(1)}',
                self.domain,
                'Cosine squared',
                priority=96
            ),
            
            # Inverse trig
            PatternRule(
                r'\\arcsin',
                'arc sine',
                self.domain,
                'Arc sine',
                priority=95
            ),
            PatternRule(
                r'\\sin\^\{-1\}',
                'arc sine',
                self.domain,
                'Inverse sine',
                priority=95
            ),
            PatternRule(
                r'\\arccos',
                'arc cosine',
                self.domain,
                'Arc cosine',
                priority=95
            ),
            PatternRule(
                r'\\cos\^\{-1\}',
                'arc cosine',
                self.domain,
                'Inverse cosine',
                priority=95
            ),
            PatternRule(
                r'\\arctan',
                'arc tangent',
                self.domain,
                'Arc tangent',
                priority=95
            ),
            PatternRule(
                r'\\tan\^\{-1\}',
                'arc tangent',
                self.domain,
                'Inverse tangent',
                priority=95
            ),
            
            # Hyperbolic functions
            PatternRule(
                r'\\sinh\s*([a-zA-Z])',
                lambda m: f'hyperbolic sine {m.group(1)}',
                self.domain,
                'Hyperbolic sine with arg',
                priority=96
            ),
            PatternRule(
                r'\\sinh\s*\(([^)]+)\)',
                lambda m: f'hyperbolic sine of {m.group(1)}',
                self.domain,
                'Hyperbolic sine with parens',
                priority=96
            ),
            PatternRule(
                r'\\sinh',
                'hyperbolic sine',
                self.domain,
                'Hyperbolic sine',
                priority=95
            ),
            PatternRule(
                r'\\cosh\s*([a-zA-Z])',
                lambda m: f'hyperbolic cosine {m.group(1)}',
                self.domain,
                'Hyperbolic cosine with arg',
                priority=96
            ),
            PatternRule(
                r'\\cosh\s*\(([^)]+)\)',
                lambda m: f'hyperbolic cosine of {m.group(1)}',
                self.domain,
                'Hyperbolic cosine with parens',
                priority=96
            ),
            PatternRule(
                r'\\cosh',
                'hyperbolic cosine',
                self.domain,
                'Hyperbolic cosine',
                priority=95
            ),
            PatternRule(
                r'\\tanh\s*([a-zA-Z])',
                lambda m: f'hyperbolic tangent {m.group(1)}',
                self.domain,
                'Hyperbolic tangent with arg',
                priority=96
            ),
            PatternRule(
                r'\\tanh\s*\(([^)]+)\)',
                lambda m: f'hyperbolic tangent of {m.group(1)}',
                self.domain,
                'Hyperbolic tangent with parens',
                priority=96
            ),
            PatternRule(
                r'\\tanh',
                'hyperbolic tangent',
                self.domain,
                'Hyperbolic tangent',
                priority=95
            ),
            
            # Sign function
            PatternRule(
                r'\\text\{sgn\}',
                'sign',
                self.domain,
                'Sign function',
                priority=95
            ),
            
            # Exponential and log
            PatternRule(
                r'e\^x',
                'e to the x',
                self.domain,
                'Natural exponential',
                priority=96
            ),
            PatternRule(
                r'e\^{([a-zA-Z])}',
                lambda m: f'e to the {m.group(1)}',
                self.domain,
                'Exponential with variable',
                priority=95
            ),
            PatternRule(
                r'\\ln\s*([a-zA-Z])',
                lambda m: f'natural log of {m.group(1)}',
                self.domain,
                'Natural logarithm',
                priority=95
            ),
            PatternRule(
                r'\\log\s*([a-zA-Z])',
                lambda m: f'log {m.group(1)}',
                self.domain,
                'Logarithm',
                priority=95
            ),
            PatternRule(
                r'\\log_([0-9]+)\s*([a-zA-Z])',
                lambda m: f'log base {m.group(1)} of {m.group(2)}',
                self.domain,
                'Log with base',
                priority=96
            ),
            PatternRule(
                r'\\log_([a-zA-Z])\s*([a-zA-Z])',
                lambda m: f'log base {m.group(1)} of {m.group(2)}',
                self.domain,
                'Log with variable base',
                priority=96
            ),
            
            # Special functions
            PatternRule(
                r'\\Gamma\(([a-zA-Z])\)',
                lambda m: f'gamma of {m.group(1)}',
                self.domain,
                'Gamma function',
                priority=95
            ),
            PatternRule(
                r'\\zeta\(([a-zA-Z])\)',
                lambda m: f'zeta of {m.group(1)}',
                self.domain,
                'Zeta function',
                priority=95
            ),
            
            # Function properties
            PatternRule(
                r'f:\s*([A-Z])\s*→\s*([A-Z])|f:\s*([A-Z])\s*\\to\s*([A-Z])',
                lambda m: f'f maps {m.group(1) or m.group(3)} to {m.group(2) or m.group(4)}',
                self.domain,
                'Function mapping',
                priority=97
            ),
            
            # Piecewise functions
            PatternRule(
                r'f\(x\)\s*=\s*\\begin\{cases\}',
                'f of x equals, begin cases',
                self.domain,
                'Piecewise function start',
                priority=98
            ),
            PatternRule(
                r'\\end\{cases\}',
                'end cases',
                self.domain,
                'Piecewise function end',
                priority=98
            ),
        ]

# ===========================
# Calculus Patterns
# ===========================

class CalculusHandler(PatternHandler):
    """Handles calculus notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Derivatives - natural speech
            PatternRule(
                r'f\'',
                'f prime',
                self.domain,
                'First derivative',
                priority=98
            ),
            PatternRule(
                r'f\'\'',
                'f double prime',
                self.domain,
                'Second derivative',
                priority=98
            ),
            PatternRule(
                r'f\'\'\' ',
                'f triple prime',
                self.domain,
                'Third derivative',
                priority=98
            ),
            PatternRule(
                r'f\'\(([a-zA-Z])\)',
                lambda m: f'f prime of {m.group(1)}',
                self.domain,
                'Derivative at point',
                priority=97
            ),
            PatternRule(
                r'y\'',
                'y prime',
                self.domain,
                'y derivative',
                priority=98
            ),
            
            # Leibniz notation
            PatternRule(
                r'\\frac\{dy\}\{dx\}',
                'd y d x',
                self.domain,
                'dy/dx',
                priority=99
            ),
            PatternRule(
                r'\\frac\{d\}\{dx\}',
                'd d x',
                self.domain,
                'd/dx operator',
                priority=99
            ),
            PatternRule(
                r'\\frac\{df\}\{dx\}',
                'd f d x',
                self.domain,
                'df/dx',
                priority=99
            ),
            PatternRule(
                r'\\frac\{d\^2y\}\{dx\^2\}',
                'd squared y d x squared',
                self.domain,
                'Second derivative',
                priority=99
            ),
            
            # Partial derivatives
            PatternRule(
                r'\\frac\{\\partial f\}\{\\partial x\}',
                'partial f partial x',
                self.domain,
                'Partial derivative',
                priority=99
            ),
            PatternRule(
                r'\\frac\{\\partial\}\{\\partial x\}',
                'partial partial x',
                self.domain,
                'Partial operator',
                priority=99
            ),
            PatternRule(
                r'\\frac\{\\partial\^2 f\}\{\\partial x\^2\}',
                'partial squared f partial x squared',
                self.domain,
                'Second partial',
                priority=99
            ),
            PatternRule(
                r'f_x',
                'f sub x',
                self.domain,
                'Subscript notation for partial',
                priority=96
            ),
            PatternRule(
                r'f_{xy}',
                'f sub x y',
                self.domain,
                'Mixed partial',
                priority=96
            ),
            
            # Integrals - natural speech
            PatternRule(
                r'\\int\s+([^d]+)\s*dx',
                lambda m: f'integral of {m.group(1).strip()} d x',
                self.domain,
                'Indefinite integral',
                priority=97
            ),
            PatternRule(
                r'\\int_([a-zA-Z0-9])\^([a-zA-Z0-9])\s*([^d]+)\s*dx',
                lambda m: f'integral from {m.group(1)} to {m.group(2)} of {m.group(3).strip()} d x',
                self.domain,
                'Definite integral simple bounds',
                priority=98
            ),
            PatternRule(
                r'\\int_\{([^}]+)\}\^\{([^}]+)\}\s*([^d]+)\s*dx',
                lambda m: f'integral from {m.group(1)} to {m.group(2)} of {m.group(3).strip()} d x',
                self.domain,
                'Definite integral complex bounds',
                priority=98
            ),
            PatternRule(
                r'\\int_0\^1',
                'integral from 0 to 1',
                self.domain,
                'Common integral bounds',
                priority=99
            ),
            PatternRule(
                r'\\int_0\^\\infty',
                'integral from 0 to infinity',
                self.domain,
                'Integral to infinity',
                priority=99
            ),
            PatternRule(
                r'\\int_{-\\infty}\^{\\infty}',
                'integral from negative infinity to infinity',
                self.domain,
                'Full real line integral',
                priority=99
            ),
            
            # Double/triple integrals
            PatternRule(
                r'\\iint',
                'double integral',
                self.domain,
                'Double integral',
                priority=98
            ),
            PatternRule(
                r'\\iiint',
                'triple integral',
                self.domain,
                'Triple integral',
                priority=98
            ),
            PatternRule(
                r'\\oint',
                'contour integral',
                self.domain,
                'Contour integral',
                priority=98
            ),
            
            # Limits
            PatternRule(
                r'\\lim_{([a-zA-Z])\\to\s*([^}]+)}',
                lambda m: f'limit as {m.group(1)} approaches {self._process_limit_value(m.group(2))}',
                self.domain,
                'Basic limit',
                priority=97
            ),
            PatternRule(
                r'\\lim_{([a-zA-Z])\\to\s*([^}]+)\^([+-])}',
                lambda m: f'limit as {m.group(1)} approaches {self._process_limit_value(m.group(2))} from the {"right" if m.group(3) == "+" else "left"}',
                self.domain,
                'One-sided limit',
                priority=98
            ),
            PatternRule(
                r'\\lim_{n\\to\\infty}',
                'limit as n approaches infinity',
                self.domain,
                'Sequence limit',
                priority=98
            ),
            
            # Series
            PatternRule(
                r'\\sum_{n=1}\^{\\infty}',
                'sum from n equals 1 to infinity',
                self.domain,
                'Infinite series',
                priority=98
            ),
            PatternRule(
                r'\\sum_{n=0}\^{\\infty}',
                'sum from n equals 0 to infinity',
                self.domain,
                'Series from 0',
                priority=98
            ),
            PatternRule(
                r'\\sum_{i=1}\^n',
                'sum from i equals 1 to n',
                self.domain,
                'Finite sum',
                priority=98
            ),
            PatternRule(
                r'\\prod_{i=1}\^n',
                'product from i equals 1 to n',
                self.domain,
                'Product notation',
                priority=98
            ),
            
            # Differentials
            PatternRule(
                r'dx',
                'd x',
                self.domain,
                'Differential dx',
                priority=95
            ),
            PatternRule(
                r'dy',
                'd y',
                self.domain,
                'Differential dy',
                priority=95
            ),
            PatternRule(
                r'dt',
                'd t',
                self.domain,
                'Differential dt',
                priority=95
            ),
            PatternRule(
                r'dr',
                'd r',
                self.domain,
                'Differential dr',
                priority=95
            ),
            PatternRule(
                r'dθ|d\\theta',
                'd theta',
                self.domain,
                'Differential dtheta',
                priority=95
            ),
            
            # Gradient and vector calculus
            PatternRule(
                r'\\nabla f',
                'gradient of f',
                self.domain,
                'Gradient',
                priority=96
            ),
            PatternRule(
                r'\\nabla \\cdot',
                'divergence',
                self.domain,
                'Divergence operator',
                priority=96
            ),
            PatternRule(
                r'\\nabla \\times',
                'curl',
                self.domain,
                'Curl operator',
                priority=96
            ),
            PatternRule(
                r'\\Delta f|\\nabla\^2 f',
                'Laplacian of f',
                self.domain,
                'Laplacian',
                priority=96
            ),
        ]
    
    def _process_limit_value(self, value: str) -> str:
        """Process limit approach values"""
        value = value.strip()
        if value == '0':
            return 'zero'
        elif value == '\\infty':
            return 'infinity'
        elif value == '-\\infty':
            return 'negative infinity'
        elif value == 'a':
            return 'a'
        else:
            return value

# ===========================
# Linear Algebra Patterns
# ===========================

class LinearAlgebraHandler(PatternHandler):
    """Handles linear algebra notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Vectors
            PatternRule(
                r'\\vec\{([a-zA-Z])\}',
                lambda m: f'vector {m.group(1)}',
                self.domain,
                'Vector notation',
                priority=95
            ),
            PatternRule(
                r'\\mathbf\{([a-zA-Z])\}',
                lambda m: f'vector {m.group(1)}',
                self.domain,
                'Bold vector',
                priority=95
            ),
            PatternRule(
                r'\|\\vec\{([a-zA-Z])\}\|',
                lambda m: f'magnitude of vector {m.group(1)}',
                self.domain,
                'Vector magnitude',
                priority=96
            ),
            PatternRule(
                r'\\hat\{([a-zA-Z])\}',
                lambda m: f'{m.group(1)} hat',
                self.domain,
                'Unit vector',
                priority=95
            ),
            
            # Matrices
            PatternRule(
                r'([A-Z])\^T',
                lambda m: f'{m.group(1)} transpose',
                self.domain,
                'Matrix transpose',
                priority=96
            ),
            PatternRule(
                r'([A-Z])\^\{-1\}',
                lambda m: f'{m.group(1)} inverse',
                self.domain,
                'Matrix inverse',
                priority=96
            ),
            PatternRule(
                r'A\^\\dagger|A\^\\ast',
                'A dagger',
                self.domain,
                'Hermitian conjugate',
                priority=96
            ),
            PatternRule(
                r'\\det\(A\)',
                'determinant of A',
                self.domain,
                'Determinant',
                priority=95
            ),
            PatternRule(
                r'\\text\{tr\}\(A\)|\\tr\(A\)',
                'trace of A',
                self.domain,
                'Trace',
                priority=95
            ),
            PatternRule(
                r'\\text\{rank\}\(A\)',
                'rank of A',
                self.domain,
                'Rank',
                priority=95
            ),
            
            # Matrix elements
            PatternRule(
                r'a_{ij}',
                'a i j',
                self.domain,
                'Matrix element',
                priority=94
            ),
            PatternRule(
                r'A_{ij}',
                'A i j',
                self.domain,
                'Matrix element capital',
                priority=94
            ),
            PatternRule(
                r'a_{([0-9]+),([0-9]+)}',
                lambda m: f'a {m.group(1)} {m.group(2)}',
                self.domain,
                'Matrix element with numbers',
                priority=94
            ),
            
            # Matrix operations
            PatternRule(
                r'AB',
                'A B',
                self.domain,
                'Matrix multiplication',
                priority=90
            ),
            PatternRule(
                r'A\s*\\cdot\s*B',
                'A dot B',
                self.domain,
                'Dot product',
                priority=95
            ),
            PatternRule(
                r'A\s*\\times\s*B',
                'A cross B',
                self.domain,
                'Cross product',
                priority=95
            ),
            PatternRule(
                r'\\otimes',
                ' tensor ',
                self.domain,
                'Tensor product',
                priority=95
            ),
            PatternRule(
                r'\\langle\s*([^,]+),\s*([^>]+)\s*\\rangle',
                lambda m: f'{m.group(1)} inner product {m.group(2)}',
                self.domain,
                'Inner product',
                priority=95
            ),
            
            # Eigenvalues
            PatternRule(
                r'\\lambda',
                'lambda',
                self.domain,
                'Lambda',
                priority=90
            ),
            PatternRule(
                r'\\lambda_([0-9]+)',
                lambda m: f'lambda {m.group(1)}',
                self.domain,
                'Lambda with subscript',
                priority=91
            ),
            PatternRule(
                r'Av\s*=\s*\\lambda v',
                'A v equals lambda v',
                self.domain,
                'Eigenvalue equation',
                priority=97
            ),
            
            # Common matrices
            PatternRule(
                r'I_n',
                'I n',
                self.domain,
                'Identity matrix of size n',
                priority=95
            ),
            PatternRule(
                r'O_n|0_n',
                'zero matrix of size n',
                self.domain,
                'Zero matrix',
                priority=95
            ),
            
            # Matrix notation
            PatternRule(
                r'\\begin\{pmatrix\}',
                'begin matrix',
                self.domain,
                'Matrix start',
                priority=98
            ),
            PatternRule(
                r'\\end\{pmatrix\}',
                'end matrix',
                self.domain,
                'Matrix end',
                priority=98
            ),
            PatternRule(
                r'\\begin\{bmatrix\}',
                'begin matrix',
                self.domain,
                'Bracket matrix start',
                priority=98
            ),
            PatternRule(
                r'\\end\{bmatrix\}',
                'end matrix',
                self.domain,
                'Bracket matrix end',
                priority=98
            ),
        ]

# ===========================
# Set Theory Patterns
# ===========================

class SetTheoryHandler(PatternHandler):
    """Handles set theory notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Set membership
            PatternRule(
                r'([a-zA-Z])\s*\\in\s*([A-Z])',
                lambda m: f'{m.group(1)} is in {m.group(2)}',
                self.domain,
                'Element membership',
                priority=95
            ),
            PatternRule(
                r'([a-zA-Z])\s*∈\s*([A-Z])',
                lambda m: f'{m.group(1)} belongs to {m.group(2)}',
                self.domain,
                'Element membership symbol',
                priority=95
            ),
            PatternRule(
                r'([a-zA-Z])\s*\\notin\s*([A-Z])',
                lambda m: f'{m.group(1)} is not in {m.group(2)}',
                self.domain,
                'Not in set',
                priority=95
            ),
            PatternRule(
                r'([a-zA-Z])\s*∉\s*([A-Z])',
                lambda m: f'{m.group(1)} is not in {m.group(2)}',
                self.domain,
                'Not in set symbol',
                priority=95
            ),
            
            # Set operations
            PatternRule(
                r'([A-Z])\s*\\cup\s*([A-Z])',
                lambda m: f'{m.group(1)} union {m.group(2)}',
                self.domain,
                'Union',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*∪\s*([A-Z])',
                lambda m: f'{m.group(1)} union {m.group(2)}',
                self.domain,
                'Union symbol',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*\\cap\s*([A-Z])',
                lambda m: f'{m.group(1)} intersect {m.group(2)}',
                self.domain,
                'Intersection',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*∩\s*([A-Z])',
                lambda m: f'{m.group(1)} intersect {m.group(2)}',
                self.domain,
                'Intersection symbol',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*\\setminus\s*([A-Z])',
                lambda m: f'{m.group(1)} minus {m.group(2)}',
                self.domain,
                'Set difference',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\^c',
                lambda m: f'{m.group(1)} complement',
                self.domain,
                'Set complement',
                priority=95
            ),
            
            # Subset relations
            PatternRule(
                r'([A-Z])\s*\\subset\s*([A-Z])',
                lambda m: f'{m.group(1)} is a subset of {m.group(2)}',
                self.domain,
                'Subset',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*⊂\s*([A-Z])',
                lambda m: f'{m.group(1)} is a subset of {m.group(2)}',
                self.domain,
                'Subset symbol',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*\\subseteq\s*([A-Z])',
                lambda m: f'{m.group(1)} is a subset of or equal to {m.group(2)}',
                self.domain,
                'Subset or equal',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*⊆\s*([A-Z])',
                lambda m: f'{m.group(1)} is a subset of or equal to {m.group(2)}',
                self.domain,
                'Subset or equal symbol',
                priority=95
            ),
            
            # Set builder notation
            PatternRule(
                r'\{([a-zA-Z])\s*:\s*([^}]+)\}',
                lambda m: f'the set of all {m.group(1)} such that {m.group(2)}',
                self.domain,
                'Set builder with colon',
                priority=96
            ),
            PatternRule(
                r'\{([a-zA-Z])\s*\|\s*([^}]+)\}',
                lambda m: f'the set of all {m.group(1)} such that {m.group(2)}',
                self.domain,
                'Set builder with bar',
                priority=96
            ),
            
            # Common sets
            PatternRule(
                r'\\mathbb\{N\}',
                'the natural numbers',
                self.domain,
                'Natural numbers',
                priority=98
            ),
            PatternRule(
                r'\\mathbb\{Z\}',
                'the integers',
                self.domain,
                'Integers',
                priority=98
            ),
            PatternRule(
                r'\\mathbb\{Q\}',
                'the rational numbers',
                self.domain,
                'Rationals',
                priority=98
            ),
            PatternRule(
                r'\\mathbb\{R\}',
                'the real numbers',
                self.domain,
                'Reals',
                priority=98
            ),
            PatternRule(
                r'\\mathbb\{C\}',
                'the complex numbers',
                self.domain,
                'Complex numbers',
                priority=98
            ),
            PatternRule(
                r'\\emptyset',
                'empty set',
                self.domain,
                'Empty set',
                priority=98
            ),
            PatternRule(
                r'\\varnothing',
                'empty set',
                self.domain,
                'Empty set varnothing',
                priority=98
            ),
            
            # Additional set theory symbols
            PatternRule(
                r'\\sim',
                ' is similar to ',
                self.domain,
                'Similar to',
                priority=95
            ),
            PatternRule(
                r'\\cong',
                ' is congruent to ',
                self.domain,
                'Congruent to',
                priority=95
            ),
            PatternRule(
                r'\\mathcal\{U\}',
                'universal set',
                self.domain,
                'Universal set',
                priority=98
            ),
            PatternRule(
                r'\\mathcal\{P\}',
                'power set',
                self.domain,
                'Power set',
                priority=98
            ),
            PatternRule(
                r'\\times',
                ' cross ',
                self.domain,
                'Cartesian product',
                priority=95
            ),
            
            # Intervals
            PatternRule(
                r'\[([^,]+),\s*([^\]]+)\]',
                lambda m: f'the closed interval from {m.group(1)} to {m.group(2)}',
                self.domain,
                'Closed interval',
                priority=95
            ),
            PatternRule(
                r'\(([^,]+),\s*([^)]+)\)',
                lambda m: f'the open interval from {m.group(1)} to {m.group(2)}',
                self.domain,
                'Open interval',
                priority=95,
                audience_levels=[AudienceLevel.UNDERGRADUATE, AudienceLevel.GRADUATE, AudienceLevel.RESEARCH]
            ),
            PatternRule(
                r'\[([^,]+),\s*([^)]+)\)',
                lambda m: f'the half-open interval from {m.group(1)} to {m.group(2)}',
                self.domain,
                'Half-open interval left',
                priority=95
            ),
            PatternRule(
                r'\(([^,]+),\s*([^\]]+)\]',
                lambda m: f'the half-open interval from {m.group(1)} to {m.group(2)}',
                self.domain,
                'Half-open interval right',
                priority=95
            ),
            
            # Cardinality
            PatternRule(
                r'\|([A-Z])\|',
                lambda m: f'cardinality of {m.group(1)}',
                self.domain,
                'Set cardinality',
                priority=94,
                audience_levels=[AudienceLevel.UNDERGRADUATE, AudienceLevel.GRADUATE, AudienceLevel.RESEARCH]
            ),
            PatternRule(
                r'#([A-Z])',
                lambda m: f'cardinality of {m.group(1)}',
                self.domain,
                'Cardinality hash',
                priority=94
            ),
        ]

# ===========================
# Probability Patterns
# ===========================

class ProbabilityHandler(PatternHandler):
    """Handles probability notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Basic probability
            PatternRule(
                r'P\(([A-Z])\)',
                lambda m: f'probability of {m.group(1)}',
                self.domain,
                'Basic probability',
                priority=95
            ),
            PatternRule(
                r'P\(([^)]+)\)',
                lambda m: f'probability of {m.group(1)}',
                self.domain,
                'General probability',
                priority=94
            ),
            PatternRule(
                r'Pr\(([A-Z])\)',
                lambda m: f'probability of {m.group(1)}',
                self.domain,
                'Pr notation',
                priority=95
            ),
            
            # Conditional probability
            PatternRule(
                r'P\(([A-Z])\s*\|\s*([A-Z])\)',
                lambda m: f'probability of {m.group(1)} given {m.group(2)}',
                self.domain,
                'Conditional probability',
                priority=96
            ),
            PatternRule(
                r'P\(([A-Z])\s*\\mid\s*([A-Z])\)',
                lambda m: f'probability of {m.group(1)} given {m.group(2)}',
                self.domain,
                'Conditional with mid',
                priority=96
            ),
            
            # Expected value
            PatternRule(
                r'E\[([A-Z])\]',
                lambda m: f'expected value of {m.group(1)}',
                self.domain,
                'Expected value',
                priority=95
            ),
            PatternRule(
                r'E\(([A-Z])\)',
                lambda m: f'expected value of {m.group(1)}',
                self.domain,
                'Expected value parentheses',
                priority=95
            ),
            PatternRule(
                r'\\mathbb\{E\}\[([A-Z])\]',
                lambda m: f'expected value of {m.group(1)}',
                self.domain,
                'Blackboard E',
                priority=95
            ),
            
            # Variance
            PatternRule(
                r'Var\(([A-Z])\)',
                lambda m: f'variance of {m.group(1)}',
                self.domain,
                'Variance',
                priority=95
            ),
            PatternRule(
                r'\\text\{Var\}\(([A-Z])\)',
                lambda m: f'variance of {m.group(1)}',
                self.domain,
                'Text variance',
                priority=95
            ),
            PatternRule(
                r'\\sigma\^2',
                'sigma squared',
                self.domain,
                'Variance sigma',
                priority=95
            ),
            
            # Standard deviation
            PatternRule(
                r'\\sigma',
                'sigma',
                self.domain,
                'Standard deviation',
                priority=94
            ),
            PatternRule(
                r'\\sigma_([A-Z])',
                lambda m: f'sigma {m.group(1)}',
                self.domain,
                'Sigma with subscript',
                priority=95
            ),
            
            # Distributions
            PatternRule(
                r'X\s*\\sim\s*N\(([^,]+),\s*([^)]+)\)',
                lambda m: f'X follows a normal distribution with mean {m.group(1)} and variance {m.group(2)}',
                self.domain,
                'Normal distribution',
                priority=97
            ),
            PatternRule(
                r'X\s*\\sim\s*\\mathcal\{N\}\(([^,]+),\s*([^)]+)\)',
                lambda m: f'X follows a normal distribution with mean {m.group(1)} and variance {m.group(2)}',
                self.domain,
                'Normal distribution mathcal',
                priority=97
            ),
            PatternRule(
                r'X\s*\\sim\s*Binomial\(([^,]+),\s*([^)]+)\)',
                lambda m: f'X follows a binomial distribution with n equals {m.group(1)} and p equals {m.group(2)}',
                self.domain,
                'Binomial distribution',
                priority=97
            ),
            PatternRule(
                r'X\s*\\sim\s*Poisson\(([^)]+)\)',
                lambda m: f'X follows a Poisson distribution with parameter {m.group(1)}',
                self.domain,
                'Poisson distribution',
                priority=97
            ),
            
            # Independence
            PatternRule(
                r'([A-Z])\s*\\perp\s*([A-Z])',
                lambda m: f'{m.group(1)} is independent of {m.group(2)}',
                self.domain,
                'Independence',
                priority=95
            ),
            PatternRule(
                r'([A-Z])\s*⊥\s*([A-Z])',
                lambda m: f'{m.group(1)} is independent of {m.group(2)}',
                self.domain,
                'Independence symbol',
                priority=95
            ),
            
            # Covariance
            PatternRule(
                r'Cov\(([A-Z]),\s*([A-Z])\)',
                lambda m: f'covariance of {m.group(1)} and {m.group(2)}',
                self.domain,
                'Covariance',
                priority=95
            ),
            PatternRule(
                r'\\text\{Cov\}\(([A-Z]),\s*([A-Z])\)',
                lambda m: f'covariance of {m.group(1)} and {m.group(2)}',
                self.domain,
                'Text covariance',
                priority=95
            ),
            
            # Correlation
            PatternRule(
                r'\\rho',
                'rho',
                self.domain,
                'Correlation coefficient',
                priority=94
            ),
            PatternRule(
                r'Corr\(([A-Z]),\s*([A-Z])\)',
                lambda m: f'correlation of {m.group(1)} and {m.group(2)}',
                self.domain,
                'Correlation',
                priority=95
            ),
        ]

# ===========================
# Number Theory Patterns
# ===========================

class NumberTheoryHandler(PatternHandler):
    """Handles number theory notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Divisibility
            PatternRule(
                r'([a-z])\s*\|\s*([a-z])',
                lambda m: f'{m.group(1)} divides {m.group(2)}',
                self.domain,
                'Divisibility',
                priority=95
            ),
            PatternRule(
                r'([a-z])\s*\\mid\s*([a-z])',
                lambda m: f'{m.group(1)} divides {m.group(2)}',
                self.domain,
                'Divisibility LaTeX',
                priority=95
            ),
            PatternRule(
                r'([a-z])\s*\\nmid\s*([a-z])',
                lambda m: f'{m.group(1)} does not divide {m.group(2)}',
                self.domain,
                'Not divides',
                priority=95
            ),
            
            # Modular arithmetic
            PatternRule(
                r'([a-z])\s*\\equiv\s*([a-z])\s*\(mod\s*([a-z])\)',
                lambda m: f'{m.group(1)} is congruent to {m.group(2)} mod {m.group(3)}',
                self.domain,
                'Congruence',
                priority=96
            ),
            PatternRule(
                r'([a-z])\s*\\equiv\s*([a-z])\s*\\pmod\{([^}]+)\}',
                lambda m: f'{m.group(1)} is congruent to {m.group(2)} modulo {m.group(3)}',
                self.domain,
                'Congruence pmod',
                priority=96
            ),
            PatternRule(
                r'([a-z])\s*mod\s*([a-z])',
                lambda m: f'{m.group(1)} mod {m.group(2)}',
                self.domain,
                'Modulo operation',
                priority=95
            ),
            
            # GCD and LCM
            PatternRule(
                r'gcd\(([^,]+),\s*([^)]+)\)',
                lambda m: f'greatest common divisor of {m.group(1)} and {m.group(2)}',
                self.domain,
                'GCD',
                priority=95
            ),
            PatternRule(
                r'\\gcd\(([^,]+),\s*([^)]+)\)',
                lambda m: f'g c d of {m.group(1)} and {m.group(2)}',
                self.domain,
                'GCD LaTeX',
                priority=95
            ),
            PatternRule(
                r'lcm\(([^,]+),\s*([^)]+)\)',
                lambda m: f'least common multiple of {m.group(1)} and {m.group(2)}',
                self.domain,
                'LCM',
                priority=95
            ),
            PatternRule(
                r'\\text\{lcm\}\(([^,]+),\s*([^)]+)\)',
                lambda m: f'l c m of {m.group(1)} and {m.group(2)}',
                self.domain,
                'LCM text',
                priority=95
            ),
            
            # Prime notation
            PatternRule(
                r'p\s*\\in\s*\\mathbb\{P\}',
                'p is prime',
                self.domain,
                'Prime membership',
                priority=95
            ),
            PatternRule(
                r'\\pi\(([a-z])\)',
                lambda m: f'pi of {m.group(1)}',
                self.domain,
                'Prime counting function',
                priority=95
            ),
            
            # Floor and ceiling
            PatternRule(
                r'\\lfloor\s*([^\\]+)\s*\\rfloor',
                lambda m: f'floor of {m.group(1)}',
                self.domain,
                'Floor function',
                priority=95
            ),
            PatternRule(
                r'\\lceil\s*([^\\]+)\s*\\rceil',
                lambda m: f'ceiling of {m.group(1)}',
                self.domain,
                'Ceiling function',
                priority=95
            ),
            PatternRule(
                r'⌊([^⌋]+)⌋',
                lambda m: f'floor of {m.group(1)}',
                self.domain,
                'Floor unicode',
                priority=95
            ),
            PatternRule(
                r'⌈([^⌉]+)⌉',
                lambda m: f'ceiling of {m.group(1)}',
                self.domain,
                'Ceiling unicode',
                priority=95
            ),
            
            # Factorial and binomial
            PatternRule(
                r'n!',
                'n factorial',
                self.domain,
                'n factorial',
                priority=96
            ),
            PatternRule(
                r'(\d+)!',
                lambda m: f'{m.group(1)} factorial',
                self.domain,
                'Number factorial',
                priority=96
            ),
            PatternRule(
                r'\\binom\{n\}\{k\}',
                'n choose k',
                self.domain,
                'Binomial coefficient',
                priority=95
            ),
            PatternRule(
                r'\\binom\{([^}]+)\}\{([^}]+)\}',
                lambda m: f'{m.group(1)} choose {m.group(2)}',
                self.domain,
                'General binomial',
                priority=94
            ),
            PatternRule(
                r'C\(n,\s*k\)',
                'n choose k',
                self.domain,
                'Combination notation',
                priority=95
            ),
            PatternRule(
                r'P\(n,\s*k\)',
                'n permute k',
                self.domain,
                'Permutation notation',
                priority=95
            ),
            
            # Euler's totient
            PatternRule(
                r'\\phi\(n\)',
                'phi of n',
                self.domain,
                "Euler's totient",
                priority=95
            ),
            PatternRule(
                r'\\varphi\(n\)',
                'phi of n',
                self.domain,
                "Euler's totient varphi",
                priority=95
            ),
        ]

# ===========================
# Complex Analysis Patterns
# ===========================

class ComplexAnalysisHandler(PatternHandler):
    """Handles complex analysis notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Complex numbers
            PatternRule(
                r'z\s*=\s*x\s*\+\s*iy',
                'z equals x plus i y',
                self.domain,
                'Complex number form',
                priority=96
            ),
            PatternRule(
                r'z\s*=\s*a\s*\+\s*bi',
                'z equals a plus b i',
                self.domain,
                'Complex number a+bi',
                priority=96
            ),
            PatternRule(
                r'\\bar\{z\}',
                'z bar',
                self.domain,
                'Complex conjugate',
                priority=95
            ),
            PatternRule(
                r'z\^\\ast',
                'z star',
                self.domain,
                'Complex conjugate star',
                priority=95
            ),
            PatternRule(
                r'\\overline\{z\}',
                'z conjugate',
                self.domain,
                'Complex conjugate overline',
                priority=95
            ),
            
            # Complex operations
            PatternRule(
                r'\\Re\(z\)',
                'real part of z',
                self.domain,
                'Real part',
                priority=95
            ),
            PatternRule(
                r'\\Im\(z\)',
                'imaginary part of z',
                self.domain,
                'Imaginary part',
                priority=95
            ),
            PatternRule(
                r'\\text\{Re\}\(z\)',
                'real part of z',
                self.domain,
                'Real part text',
                priority=95
            ),
            PatternRule(
                r'\\text\{Im\}\(z\)',
                'imaginary part of z',
                self.domain,
                'Imaginary part text',
                priority=95
            ),
            PatternRule(
                r'\|z\|',
                'modulus of z',
                self.domain,
                'Complex modulus',
                priority=95
            ),
            PatternRule(
                r'\\arg\(z\)',
                'argument of z',
                self.domain,
                'Complex argument',
                priority=95
            ),
            
            # Euler's formula
            PatternRule(
                r'e\^{i\\theta}',
                'e to the i theta',
                self.domain,
                "Euler's formula",
                priority=97
            ),
            PatternRule(
                r'e\^{i\\pi}',
                'e to the i pi',
                self.domain,
                "Euler's identity component",
                priority=97
            ),
            PatternRule(
                r'e\^{i\\pi}\s*=\s*-1',
                'e to the i pi equals negative one',
                self.domain,
                "Euler's identity",
                priority=98
            ),
            PatternRule(
                r'e\^{2\\pi i}',
                'e to the 2 pi i',
                self.domain,
                'Full rotation',
                priority=97
            ),
            
            # Complex functions
            PatternRule(
                r'f\(z\)',
                'f of z',
                self.domain,
                'Complex function',
                priority=94
            ),
            PatternRule(
                r'f:\s*\\mathbb\{C\}\s*\\to\s*\\mathbb\{C\}',
                'f maps complex to complex',
                self.domain,
                'Complex mapping',
                priority=95
            ),
            
            # Residues and poles
            PatternRule(
                r'\\text\{Res\}\(f,\s*z_0\)',
                'residue of f at z naught',
                self.domain,
                'Residue',
                priority=95
            ),
            PatternRule(
                r'\\oint_C',
                'contour integral over C',
                self.domain,
                'Contour integral',
                priority=95
            ),
            
            # Complex domains
            PatternRule(
                r'\\mathbb\{C\}',
                'the complex plane',
                self.domain,
                'Complex numbers',
                priority=96,
                audience_levels=[AudienceLevel.UNDERGRADUATE, AudienceLevel.GRADUATE, AudienceLevel.RESEARCH]
            ),
            PatternRule(
                r'\\mathbb\{C\}',
                'C',
                self.domain,
                'Complex numbers simple',
                priority=96,
                audience_levels=[AudienceLevel.HIGH_SCHOOL]
            ),
        ]

# ===========================
# Special Symbols Handler
# ===========================

class SpecialSymbolsHandler:
    """Handles special symbols like percent, currency, units"""
    
    def __init__(self):
        self.patterns = [
            # Percent
            PatternRule(
                r'(\d+)\\%',
                lambda m: f'{m.group(1)} percent',
                MathDomain.BASIC_ARITHMETIC,
                'Percent',
                priority=95
            ),
            
            # Currency
            PatternRule(
                r'\\\$([\d]+)',
                lambda m: f'{m.group(1)} dollars',
                MathDomain.BASIC_ARITHMETIC,
                'Dollar amount',
                priority=95
            ),
            
            # Units
            PatternRule(
                r'\\text\{ m/s\}',
                'meters per second',
                MathDomain.BASIC_ARITHMETIC,
                'Meters per second',
                priority=95
            ),
            PatternRule(
                r'\\text\{m/s\}',
                'meters per second',
                MathDomain.BASIC_ARITHMETIC,
                'Meters per second no space',
                priority=95
            ),
            
            # Ellipsis
            PatternRule(
                r'\\ldots',
                'dot dot dot',
                MathDomain.BASIC_ARITHMETIC,
                'Ellipsis',
                priority=95
            ),
            
            # QED
            PatternRule(
                r'\\square',
                'Q E D',
                MathDomain.BASIC_ARITHMETIC,
                'QED square',
                priority=95
            ),
        ]
        
        # Compile patterns
        for pattern in self.patterns:
            pattern.compiled = re.compile(pattern.pattern)
    
    def process(self, text: str, audience: AudienceLevel = AudienceLevel.UNDERGRADUATE) -> str:
        """Process text with special symbol patterns"""
        result = text
        
        # Sort by priority (highest first)
        sorted_patterns = sorted(self.patterns, key=lambda p: p.priority, reverse=True)
        
        # Apply patterns
        for pattern in sorted_patterns:
            if callable(pattern.replacement):
                result = pattern.compiled.sub(pattern.replacement, result)
            else:
                result = pattern.compiled.sub(pattern.replacement, result)
        
        return result

# ===========================
# Logic Patterns
# ===========================

class LogicHandler(PatternHandler):
    """Handles logical notation naturally"""
    
    def _init_patterns(self):
        self.patterns = [
            # Logical connectives
            PatternRule(
                r'\\land|∧',
                ' and ',
                self.domain,
                'Logical and',
                priority=95
            ),
            PatternRule(
                r'\\lor|∨',
                ' or ',
                self.domain,
                'Logical or',
                priority=95
            ),
            PatternRule(
                r'\\neg|¬',
                'not ',
                self.domain,
                'Logical not',
                priority=95
            ),
            PatternRule(
                r'\\implies|⇒',
                ' implies ',
                self.domain,
                'Implication',
                priority=95
            ),
            PatternRule(
                r'\\iff|⇔',
                ' if and only if ',
                self.domain,
                'If and only if',
                priority=95
            ),
            PatternRule(
                r'\\Rightarrow',
                ' implies ',
                self.domain,
                'Rightarrow',
                priority=95
            ),
            PatternRule(
                r'\\Leftrightarrow',
                ' if and only if ',
                self.domain,
                'Leftrightarrow',
                priority=95
            ),
            
            # Quantifiers
            PatternRule(
                r'\\forall\s*([a-zA-Z])',
                lambda m: f'for all {m.group(1)}',
                self.domain,
                'Universal quantifier',
                priority=96
            ),
            PatternRule(
                r'∀\s*([a-zA-Z])',
                lambda m: f'for all {m.group(1)}',
                self.domain,
                'Universal quantifier symbol',
                priority=96
            ),
            PatternRule(
                r'\\exists\s*([a-zA-Z])',
                lambda m: f'there exists {m.group(1)}',
                self.domain,
                'Existential quantifier',
                priority=96
            ),
            PatternRule(
                r'∃\s*([a-zA-Z])',
                lambda m: f'there exists {m.group(1)}',
                self.domain,
                'Existential quantifier symbol',
                priority=96
            ),
            PatternRule(
                r'\\exists!\s*([a-zA-Z])',
                lambda m: f'there exists unique {m.group(1)}',
                self.domain,
                'Unique existence',
                priority=96
            ),
            PatternRule(
                r'\\nexists',
                'there does not exist',
                self.domain,
                'Does not exist',
                priority=95
            ),
            
            # Common logical expressions
            PatternRule(
                r'P\s*\\land\s*Q',
                'P and Q',
                self.domain,
                'P and Q',
                priority=94
            ),
            PatternRule(
                r'P\s*\\lor\s*Q',
                'P or Q',
                self.domain,
                'P or Q',
                priority=94
            ),
            PatternRule(
                r'P\s*\\implies\s*Q',
                'P implies Q',
                self.domain,
                'P implies Q',
                priority=94
            ),
            PatternRule(
                r'\\neg\s*P',
                'not P',
                self.domain,
                'Not P',
                priority=94
            ),
            
            # Truth values
            PatternRule(
                r'\\top|⊤',
                'true',
                self.domain,
                'True',
                priority=95
            ),
            PatternRule(
                r'\\bot|⊥',
                'false',
                self.domain,
                'False',
                priority=95
            ),
            
            # Therefore and because
            PatternRule(
                r'\\therefore|∴',
                'therefore',
                self.domain,
                'Therefore',
                priority=95
            ),
            PatternRule(
                r'\\because|∵',
                'because',
                self.domain,
                'Because',
                priority=95
            ),
            
            # Proof notation
            PatternRule(
                r'Q\\.E\\.D\\.|QED',
                'Q E D',
                self.domain,
                'QED',
                priority=95
            ),
            PatternRule(
                r'□|■',
                'end of proof',
                self.domain,
                'Proof end marker',
                priority=95
            ),
        ]

# ===========================
# Generalization Engine
# ===========================

class GeneralizationEngine:
    """Handles unseen mathematical expressions through pattern generalization"""
    
    def __init__(self):
        self.handlers = {
            MathDomain.BASIC_ARITHMETIC: BasicArithmeticHandler(MathDomain.BASIC_ARITHMETIC),
            MathDomain.ALGEBRA: AlgebraHandler(MathDomain.ALGEBRA),
            MathDomain.FUNCTIONS: FunctionHandler(MathDomain.FUNCTIONS),
            MathDomain.CALCULUS: CalculusHandler(MathDomain.CALCULUS),
            MathDomain.LINEAR_ALGEBRA: LinearAlgebraHandler(MathDomain.LINEAR_ALGEBRA),
            MathDomain.SET_THEORY: SetTheoryHandler(MathDomain.SET_THEORY),
            MathDomain.PROBABILITY: ProbabilityHandler(MathDomain.PROBABILITY),
            MathDomain.NUMBER_THEORY: NumberTheoryHandler(MathDomain.NUMBER_THEORY),
            MathDomain.COMPLEX_ANALYSIS: ComplexAnalysisHandler(MathDomain.COMPLEX_ANALYSIS),
            MathDomain.LOGIC: LogicHandler(MathDomain.LOGIC),
        }
        
        # Add special symbols handler
        self.special_handler = SpecialSymbolsHandler()
        
        # General patterns that apply across domains
        self.general_patterns = [
            # Greek letters
            PatternRule(
                r'\\alpha', 'alpha', MathDomain.BASIC_ARITHMETIC, 'Alpha', 90
            ),
            PatternRule(
                r'\\beta', 'beta', MathDomain.BASIC_ARITHMETIC, 'Beta', 90
            ),
            PatternRule(
                r'\\gamma', 'gamma', MathDomain.BASIC_ARITHMETIC, 'Gamma', 90
            ),
            PatternRule(
                r'\\delta', 'delta', MathDomain.BASIC_ARITHMETIC, 'Delta', 90
            ),
            PatternRule(
                r'\\epsilon', 'epsilon', MathDomain.BASIC_ARITHMETIC, 'Epsilon', 90
            ),
            PatternRule(
                r'\\varepsilon', 'epsilon', MathDomain.BASIC_ARITHMETIC, 'Var epsilon', 90
            ),
            PatternRule(
                r'\\theta', 'theta', MathDomain.BASIC_ARITHMETIC, 'Theta', 90
            ),
            PatternRule(
                r'\\lambda', 'lambda', MathDomain.BASIC_ARITHMETIC, 'Lambda', 90
            ),
            PatternRule(
                r'\\mu', 'mu', MathDomain.BASIC_ARITHMETIC, 'Mu', 90
            ),
            PatternRule(
                r'\\pi', 'pi', MathDomain.BASIC_ARITHMETIC, 'Pi', 90
            ),
            PatternRule(
                r'\\sigma', 'sigma', MathDomain.BASIC_ARITHMETIC, 'Sigma', 90
            ),
            PatternRule(
                r'\\phi', 'phi', MathDomain.BASIC_ARITHMETIC, 'Phi', 90
            ),
            PatternRule(
                r'\\varphi', 'phi', MathDomain.BASIC_ARITHMETIC, 'Var phi', 90
            ),
            PatternRule(
                r'\\psi', 'psi', MathDomain.BASIC_ARITHMETIC, 'Psi', 90
            ),
            PatternRule(
                r'\\omega', 'omega', MathDomain.BASIC_ARITHMETIC, 'Omega', 90
            ),
            PatternRule(
                r'\\Omega', 'capital omega', MathDomain.BASIC_ARITHMETIC, 'Capital Omega', 90
            ),
            
            # Common constants
            PatternRule(
                r'\\infty', 'infinity', MathDomain.BASIC_ARITHMETIC, 'Infinity', 95
            ),
            PatternRule(
                r'∞', 'infinity', MathDomain.BASIC_ARITHMETIC, 'Infinity symbol', 95
            ),
            PatternRule(
                r'π', 'pi', MathDomain.BASIC_ARITHMETIC, 'Pi symbol', 95
            ),
            
            # Dots
            # Note: \ldots is now handled in SpecialSymbolsHandler
            PatternRule(
                r'\\cdots', 'dot dot dot', MathDomain.BASIC_ARITHMETIC, 'Center dots', 85
            ),
            PatternRule(
                r'\\vdots', 'vertical dots', MathDomain.BASIC_ARITHMETIC, 'Vertical dots', 85
            ),
            PatternRule(
                r'\\ddots', 'diagonal dots', MathDomain.BASIC_ARITHMETIC, 'Diagonal dots', 85
            ),
            PatternRule(
                r'…', 'dot dot dot', MathDomain.BASIC_ARITHMETIC, 'Ellipsis unicode', 85
            ),
            
            # Parentheses and brackets
            PatternRule(
                r'\\left\(', '(', MathDomain.BASIC_ARITHMETIC, 'Left paren', 80
            ),
            PatternRule(
                r'\\right\)', ')', MathDomain.BASIC_ARITHMETIC, 'Right paren', 80
            ),
            PatternRule(
                r'\\left\[', '[', MathDomain.BASIC_ARITHMETIC, 'Left bracket', 80
            ),
            PatternRule(
                r'\\right\]', ']', MathDomain.BASIC_ARITHMETIC, 'Right bracket', 80
            ),
            PatternRule(
                r'\\left\{', '{', MathDomain.BASIC_ARITHMETIC, 'Left brace', 80
            ),
            PatternRule(
                r'\\right\}', '}', MathDomain.BASIC_ARITHMETIC, 'Right brace', 80
            ),
            
            # Spacing cleanup
            PatternRule(
                r'\s+', ' ', MathDomain.BASIC_ARITHMETIC, 'Multiple spaces', 50
            ),
            PatternRule(
                r'\\,', ' ', MathDomain.BASIC_ARITHMETIC, 'Thin space', 50
            ),
            PatternRule(
                r'\\;', ' ', MathDomain.BASIC_ARITHMETIC, 'Medium space', 50
            ),
            PatternRule(
                r'\\quad', ' ', MathDomain.BASIC_ARITHMETIC, 'Quad space', 50
            ),
            PatternRule(
                r'\\qquad', ' ', MathDomain.BASIC_ARITHMETIC, 'Double quad space', 50
            ),
        ]
    
    def process(self, text: str, audience: AudienceLevel = AudienceLevel.UNDERGRADUATE) -> str:
        """Process text through all applicable patterns"""
        result = text
        
        # Apply general patterns first
        for pattern in sorted(self.general_patterns, key=lambda p: p.priority, reverse=True):
            if audience in pattern.audience_levels:
                if callable(pattern.replacement):
                    result = pattern.compiled.sub(pattern.replacement, result)
                else:
                    result = pattern.compiled.sub(pattern.replacement, result)
        
        # Apply domain-specific patterns in a specific order to prevent conflicts
        # Process patterns that contain LaTeX commands first
        priority_order = [
            MathDomain.LINEAR_ALGEBRA,  # Process matrix-specific patterns first
            MathDomain.FUNCTIONS,  # Process functions before algebra to catch \sin^{-1} etc.
            MathDomain.ALGEBRA,  # Process fractions, roots, etc.
            MathDomain.CALCULUS,  # Process derivatives, integrals
            MathDomain.SET_THEORY,
            MathDomain.PROBABILITY,
            MathDomain.NUMBER_THEORY,
            MathDomain.COMPLEX_ANALYSIS,
            MathDomain.LOGIC,
            MathDomain.BASIC_ARITHMETIC,  # Process basic arithmetic last to avoid breaking LaTeX
        ]
        
        for domain in priority_order:
            if domain in self.handlers:
                result = self.handlers[domain].process(result, audience)
        
        # Apply special symbols handler
        result = self.special_handler.process(result, audience)
        
        # Clean up final result
        result = self._cleanup(result)
        
        return result
    
    def _cleanup(self, text: str) -> str:
        """Final cleanup of processed text"""
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing spaces
        text = text.strip()
        
        # Fix common speech patterns
        text = re.sub(r'\s+,', ',', text)
        text = re.sub(r'\s+\.', '.', text)
        
        return text
    
    def detect_domain(self, text: str) -> List[MathDomain]:
        """Detect which mathematical domains are present in the text"""
        domains = []
        
        # Check for domain-specific keywords
        domain_keywords = {
            MathDomain.CALCULUS: [r'\\int', r'\\lim', r'\\frac\{d', r'\\partial', r'derivative', r'integral'],
            MathDomain.LINEAR_ALGEBRA: [r'matrix', r'vector', r'\\det', r'eigenvalue', r'\\vec'],
            MathDomain.SET_THEORY: [r'\\in', r'\\subset', r'\\cup', r'\\cap', r'\\emptyset'],
            MathDomain.PROBABILITY: [r'P\(', r'E\[', r'Var\(', r'\\sim', r'distribution'],
            MathDomain.NUMBER_THEORY: [r'\\equiv', r'mod', r'gcd', r'prime', r'\\mid'],
            MathDomain.COMPLEX_ANALYSIS: [r'\\bar\{z\}', r'\\Re', r'\\Im', r'e\^{i', r'complex'],
            MathDomain.LOGIC: [r'\\forall', r'\\exists', r'\\implies', r'\\iff', r'\\neg'],
        }
        
        for domain, keywords in domain_keywords.items():
            for keyword in keywords:
                if re.search(keyword, text):
                    domains.append(domain)
                    break
        
        # Always include basic arithmetic and algebra
        if MathDomain.BASIC_ARITHMETIC not in domains:
            domains.append(MathDomain.BASIC_ARITHMETIC)
        if MathDomain.ALGEBRA not in domains:
            domains.append(MathDomain.ALGEBRA)
        
        return domains

# ===========================
# Main Pattern Processor
# ===========================

class MathSpeechProcessor:
    """Main processor that converts mathematical notation to natural speech"""
    
    def __init__(self):
        self.engine = GeneralizationEngine()
        logger.info("Math speech processor initialized with all domain handlers")
    
    def process(self, text: str, audience: AudienceLevel = AudienceLevel.UNDERGRADUATE) -> str:
        """Convert mathematical notation to natural speech"""
        # Pre-process to handle common LaTeX issues
        text = self._preprocess(text)
        
        # Process through generalization engine
        result = self.engine.process(text, audience)
        
        # Post-process for final cleanup
        result = self._postprocess(result)
        
        return result
    
    def _preprocess(self, text: str) -> str:
        """Pre-process text to normalize notation"""
        # Handle display math delimiters
        text = re.sub(r'\$\$([^$]+)\$\$', r'\1', text)
        text = re.sub(r'\$([^$]+)\$', r'\1', text)
        text = re.sub(r'\\[\[\]]', '', text)
        
        # Normalize whitespace around operators, but preserve LaTeX commands
        # First, temporarily replace LaTeX commands to protect them
        latex_commands = []
        def protect_latex(match):
            latex_commands.append(match.group(0))
            return f"__LATEX_{len(latex_commands)-1}__"
        
        # Protect LaTeX commands (backslash followed by letters)
        text = re.sub(r'\\[a-zA-Z]+', protect_latex, text)
        
        # Now normalize whitespace around operators
        text = re.sub(r'\s*([+\-*/=<>])\s*', r' \1 ', text)
        
        # Restore LaTeX commands
        for i, cmd in enumerate(latex_commands):
            text = text.replace(f"__LATEX_{i}__", cmd)
        
        return text
    
    def _postprocess(self, text: str) -> str:
        """Post-process for natural speech flow"""
        # Fix article usage
        text = re.sub(r'\ba\s+([aeiou])', r'an \1', text, flags=re.IGNORECASE)
        
        # Remove redundant words
        text = re.sub(r'\bthe the\b', 'the', text)
        text = re.sub(r'\ba a\b', 'a', text)
        
        # Ensure proper sentence flow
        text = re.sub(r'([.!?])\s*([a-z])', lambda m: f'{m.group(1)} {m.group(2).upper()}', text)
        
        return text
    
    def detect_audience(self, text: str) -> AudienceLevel:
        """Attempt to detect appropriate audience level from context"""
        # Simple heuristic based on complexity
        complexity_indicators = {
            AudienceLevel.HIGH_SCHOOL: [r'solve', r'find', r'calculate', r'x\s*='],
            AudienceLevel.UNDERGRADUATE: [r'\\lim', r'\\int', r'derivative', r'matrix'],
            AudienceLevel.GRADUATE: [r'\\forall', r'\\exists', r'topology', r'manifold'],
            AudienceLevel.RESEARCH: [r'lemma', r'theorem', r'conjecture', r'proof'],
        }
        
        detected_level = AudienceLevel.UNDERGRADUATE  # default
        
        for level, indicators in complexity_indicators.items():
            for indicator in indicators:
                if re.search(indicator, text, re.IGNORECASE):
                    detected_level = level
                    break
        
        return detected_level

# ===========================
# Convenience Functions
# ===========================

def process_math_to_speech(text: str, audience: AudienceLevel = None) -> str:
    """Convert mathematical notation to natural speech"""
    processor = MathSpeechProcessor()
    
    # Auto-detect audience if not specified
    if audience is None:
        audience = processor.detect_audience(text)
    
    return processor.process(text, audience)

def process_with_context(text: str, context: Dict[str, Any]) -> str:
    """Process with additional context information"""
    processor = MathSpeechProcessor()
    
    # Extract audience from context
    audience = context.get('audience', AudienceLevel.UNDERGRADUATE)
    if isinstance(audience, str):
        audience = AudienceLevel(audience)
    
    return processor.process(text, audience)

# ===========================
# Testing
# ===========================

def test_all_patterns():
    """Test all 100 example patterns"""
    processor = MathSpeechProcessor()
    
    test_cases = [
        # Basic arithmetic (1-10)
        ("2 + 3 = 5", "Basic addition"),
        ("x - y", "Variable subtraction"),
        ("3 × 4", "Multiplication"),
        ("a/b", "Division as fraction"),
        ("x = 5", "Equation"),
        ("x ≠ y", "Not equal"),
        ("x < y", "Less than"),
        ("x ≤ y", "Less than or equal"),
        ("x ≈ y", "Approximately equal"),
        ("x ± y", "Plus minus"),
        
        # Algebra (11-25)
        ("x^2", "x squared"),
        ("x^3", "x cubed"),
        ("x^n", "x to the n"),
        ("x^{n+1}", "x to the n+1"),
        ("x_0", "x naught"),
        ("x_1", "x one"),
        ("x_n", "x sub n"),
        ("a_{i,j}", "Matrix element"),
        ("\\frac{1}{2}", "One half"),
        ("\\frac{a}{b}", "a over b"),
        ("\\sqrt{2}", "Square root of 2"),
        ("\\sqrt[3]{x}", "Cube root"),
        ("ax^2 + bx + c", "Quadratic"),
        ("(a+b)^2", "Binomial squared"),
        ("|x|", "Absolute value"),
        
        # Functions (26-40)
        ("f(x)", "Function notation"),
        ("g(x)", "Function g"),
        ("f ∘ g", "Composition"),
        ("\\sin x", "Sine"),
        ("\\cos x", "Cosine"),
        ("\\tan x", "Tangent"),
        ("\\sin^2 x", "Sine squared"),
        ("\\arcsin x", "Arc sine"),
        ("e^x", "Exponential"),
        ("\\ln x", "Natural log"),
        ("\\log_2 x", "Log base 2"),
        ("\\Gamma(x)", "Gamma function"),
        ("f: A → B", "Function mapping"),
        ("f'(x)", "Derivative"),
        ("y'", "y prime"),
        
        # Calculus (41-60)
        ("f''(x)", "Second derivative"),
        ("\\frac{dy}{dx}", "dy/dx"),
        ("\\frac{df}{dx}", "df/dx"),
        ("\\frac{d^2y}{dx^2}", "Second derivative"),
        ("\\frac{\\partial f}{\\partial x}", "Partial derivative"),
        ("f_x", "Partial notation"),
        ("\\int f(x) dx", "Indefinite integral"),
        ("\\int_0^1 f(x) dx", "Definite integral"),
        ("\\int_0^\\infty", "Integral to infinity"),
        ("\\iint", "Double integral"),
        ("\\lim_{x\\to 0}", "Limit"),
        ("\\lim_{x\\to 0^+}", "Right limit"),
        ("\\lim_{n\\to\\infty}", "Sequence limit"),
        ("\\sum_{n=1}^{\\infty}", "Infinite series"),
        ("\\sum_{i=1}^n", "Finite sum"),
        ("\\prod_{i=1}^n", "Product"),
        ("dx", "Differential"),
        ("\\nabla f", "Gradient"),
        ("\\nabla \\cdot F", "Divergence"),
        ("\\nabla \\times F", "Curl"),
        
        # Linear Algebra (61-70)
        ("\\vec{v}", "Vector v"),
        ("\\mathbf{A}", "Matrix A"),
        ("||\\vec{v}||", "Vector magnitude"),
        ("\\hat{e}", "Unit vector"),
        ("A^T", "Transpose"),
        ("A^{-1}", "Inverse"),
        ("\\det(A)", "Determinant"),
        ("\\text{tr}(A)", "Trace"),
        ("a_{ij}", "Matrix element"),
        ("\\lambda", "Eigenvalue"),
        
        # Set Theory (71-80)
        ("x \\in A", "Element of"),
        ("x \\notin A", "Not element of"),
        ("A \\cup B", "Union"),
        ("A \\cap B", "Intersection"),
        ("A \\setminus B", "Set difference"),
        ("A^c", "Complement"),
        ("A \\subset B", "Subset"),
        ("\\{x : x > 0\\}", "Set builder"),
        ("\\mathbb{R}", "Real numbers"),
        ("[a, b]", "Closed interval"),
        
        # Probability (81-90)
        ("P(A)", "Probability"),
        ("P(A|B)", "Conditional probability"),
        ("E[X]", "Expected value"),
        ("Var(X)", "Variance"),
        ("\\sigma", "Standard deviation"),
        ("X \\sim N(0,1)", "Normal distribution"),
        ("A \\perp B", "Independence"),
        ("Cov(X,Y)", "Covariance"),
        ("\\rho", "Correlation"),
        ("X \\sim Binomial(n,p)", "Binomial distribution"),
        
        # Number Theory & Logic (91-100)
        ("a | b", "Divides"),
        ("a \\equiv b \\pmod{n}", "Congruence"),
        ("\\gcd(a,b)", "GCD"),
        ("n!", "Factorial"),
        ("\\binom{n}{k}", "Binomial coefficient"),
        ("\\lfloor x \\rfloor", "Floor"),
        ("\\forall x", "For all"),
        ("\\exists y", "There exists"),
        ("P \\implies Q", "Implies"),
        ("P \\iff Q", "If and only if"),
    ]
    
    print("Testing All 100 Pattern Examples")
    print("=" * 80)
    
    for i, (input_text, description) in enumerate(test_cases, 1):
        result = processor.process(input_text)
        print(f"\n{i:3d}. {description}")
        print(f"     Input:  {input_text}")
        print(f"     Output: {result}")
    
    # Test generalization on unseen patterns
    print("\n\nTesting Generalization on Unseen Patterns")
    print("=" * 80)
    
    unseen_cases = [
        "\\int_a^b x^2 \\sin(x) dx",
        "\\lim_{h\\to 0} \\frac{f(x+h) - f(x)}{h}",
        "\\sum_{k=0}^n \\binom{n}{k} x^k y^{n-k}",
        "\\forall \\epsilon > 0, \\exists \\delta > 0",
        "A \\otimes B \\cong B \\otimes A",
    ]
    
    for i, test in enumerate(unseen_cases, 1):
        result = processor.process(test)
        print(f"\n{i}. Input:  {test}")
        print(f"   Output: {result}")

if __name__ == "__main__":
    test_all_patterns()