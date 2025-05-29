#!/usr/bin/env python3
"""
Common Mathematical Patterns for Text-to-Speech
==============================================

Handles frequently occurring mathematical patterns with natural pronunciations,
including epsilon-delta definitions, common expressions, equation references,
and structural patterns.

This module provides specialized handling for mathematical idioms that appear
across all domains, ensuring consistent and natural speech.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Pattern Categories
# ===========================

class PatternCategory(Enum):
    """Categories of mathematical patterns"""
    EPSILON_DELTA = "epsilon_delta"
    LIMIT_EXPRESSION = "limit_expression"
    SEQUENCE_SERIES = "sequence_series"
    SET_NOTATION = "set_notation"
    PROOF_PATTERN = "proof_pattern"
    REFERENCE = "reference"
    COMMON_EXPRESSION = "common_expression"
    STRUCTURAL = "structural"

@dataclass
class MathematicalPattern:
    """Represents a mathematical pattern with its pronunciation"""
    pattern: str  # Regex pattern
    replacement: Union[str, Callable]  # Replacement text or function
    category: PatternCategory
    description: str
    priority: int = 50  # Higher priority patterns are applied first
    
    def __post_init__(self):
        """Compile the pattern"""
        self.compiled = re.compile(self.pattern)

# ===========================
# Epsilon-Delta Patterns
# ===========================

class EpsilonDeltaHandler:
    """Handles epsilon-delta proofs and definitions"""
    
    def __init__(self):
        self.patterns = [
            # Classic epsilon-delta definition
            MathematicalPattern(
                r'∀\s*ε\s*>\s*0\s*[,.]?\s*∃\s*δ\s*>\s*0\s*(?:such that|s\.t\.)',
                'for every epsilon greater than zero, there exists delta greater than zero such that',
                PatternCategory.EPSILON_DELTA,
                'Classic epsilon-delta opener',
                priority=90
            ),
            MathematicalPattern(
                r'\\forall\s*\\varepsilon\s*>\s*0\s*[,.]?\s*\\exists\s*\\delta\s*>\s*0',
                'for every epsilon greater than zero, there exists delta greater than zero',
                PatternCategory.EPSILON_DELTA,
                'LaTeX epsilon-delta',
                priority=90
            ),
            
            # Epsilon-delta conditions
            MathematicalPattern(
                r'0\s*<\s*\|([x-z])\s*-\s*([a-z])\|\s*<\s*δ',
                lambda m: f'zero is less than the absolute value of {m.group(1)} minus {m.group(2)}, which is less than delta',
                PatternCategory.EPSILON_DELTA,
                'Delta neighborhood condition',
                priority=80
            ),
            MathematicalPattern(
                r'\|f\(([x-z])\)\s*-\s*L\|\s*<\s*ε',
                lambda m: f'the absolute value of f of {m.group(1)} minus L is less than epsilon',
                PatternCategory.EPSILON_DELTA,
                'Epsilon bound condition',
                priority=80
            ),
            
            # Choosing delta
            MathematicalPattern(
                r'[Cc]hoose\s*δ\s*=\s*min\s*\{([^}]+)\}',
                lambda m: f'choose delta to be the minimum of {self._process_min_args(m.group(1))}',
                PatternCategory.EPSILON_DELTA,
                'Delta choice with minimum',
                priority=75
            ),
            MathematicalPattern(
                r'[Ll]et\s*δ\s*=\s*ε/(\d+)',
                lambda m: f'let delta equal epsilon divided by {m.group(1)}',
                PatternCategory.EPSILON_DELTA,
                'Simple delta choice',
                priority=75
            ),
            
            # Given epsilon
            MathematicalPattern(
                r'[Gg]iven\s*(?:any\s*)?ε\s*>\s*0',
                'given any epsilon greater than zero',
                PatternCategory.EPSILON_DELTA,
                'Given epsilon statement',
                priority=70
            ),
            
            # Work backwards
            MathematicalPattern(
                r'[Ww]e\s*(?:want|need)\s*(?:to\s*(?:find|show))?\s*\|([^|]+)\|\s*<\s*ε',
                lambda m: f'we need to show that the absolute value of {m.group(1)} is less than epsilon',
                PatternCategory.EPSILON_DELTA,
                'Target inequality',
                priority=70
            ),
        ]
    
    def _process_min_args(self, args: str) -> str:
        """Process arguments inside min{}"""
        items = [item.strip() for item in args.split(',')]
        if len(items) == 1:
            return items[0]
        elif len(items) == 2:
            return f"{items[0]} and {items[1]}"
        else:
            return ', '.join(items[:-1]) + f", and {items[-1]}"

# ===========================
# Limit and Convergence Patterns
# ===========================

class LimitPatternHandler:
    """Handles limit expressions and convergence"""
    
    def __init__(self):
        self.patterns = [
            # Basic limits
            MathematicalPattern(
                r'\\lim_{([^}]+)\\to([^}]+)}\s*([^=\s]+)',
                lambda m: f'the limit as {self._process_variable(m.group(1))} approaches {self._process_value(m.group(2))} of {m.group(3)}',
                PatternCategory.LIMIT_EXPRESSION,
                'Basic limit notation',
                priority=85
            ),
            MathematicalPattern(
                r'\\lim_{([^}]+)}\s*([^=\s]+)',
                lambda m: f'the limit over {self._process_variable(m.group(1))} of {m.group(2)}',
                PatternCategory.LIMIT_EXPRESSION,
                'Limit with condition',
                priority=85
            ),
            
            # One-sided limits
            MathematicalPattern(
                r'\\lim_{([^}]+)\\to([^}]+)\^([+-])}\s*([^=\s]+)',
                lambda m: f'the {"right-hand" if m.group(3) == "+" else "left-hand"} limit as {self._process_variable(m.group(1))} approaches {self._process_value(m.group(2))} of {m.group(4)}',
                PatternCategory.LIMIT_EXPRESSION,
                'One-sided limit',
                priority=85
            ),
            
            # Limits at infinity
            MathematicalPattern(
                r'\\lim_{([^}]+)\\to\\infty}',
                lambda m: f'the limit as {self._process_variable(m.group(1))} goes to infinity',
                PatternCategory.LIMIT_EXPRESSION,
                'Limit to infinity',
                priority=85
            ),
            MathematicalPattern(
                r'\\lim_{([^}]+)\\to-\\infty}',
                lambda m: f'the limit as {self._process_variable(m.group(1))} goes to negative infinity',
                PatternCategory.LIMIT_EXPRESSION,
                'Limit to negative infinity',
                priority=85
            ),
            
            # Convergence notation
            MathematicalPattern(
                r'([a-z])_n\s*\\to\s*([a-z])',
                lambda m: f'{m.group(1)} sub n converges to {m.group(2)}',
                PatternCategory.LIMIT_EXPRESSION,
                'Sequence convergence',
                priority=80
            ),
            MathematicalPattern(
                r'([a-z])_n\s*→\s*([a-z])',
                lambda m: f'{m.group(1)} sub n converges to {m.group(2)}',
                PatternCategory.LIMIT_EXPRESSION,
                'Sequence convergence arrow',
                priority=80
            ),
            
            # Limit exists
            MathematicalPattern(
                r'\\lim\s+(?:exists|DNE)',
                lambda m: 'the limit exists' if 'exists' in m.group(0) else 'the limit does not exist',
                PatternCategory.LIMIT_EXPRESSION,
                'Limit existence',
                priority=75
            ),
        ]
    
    def _process_variable(self, var: str) -> str:
        """Process limit variable"""
        var = var.strip()
        if var == 'n':
            return 'n'
        elif var == 'x':
            return 'x'
        elif ',' in var:
            return 'the variables ' + var.replace(',', ' and ')
        return var
    
    def _process_value(self, val: str) -> str:
        """Process limit value"""
        val = val.strip()
        if val == '0':
            return 'zero'
        elif val == '∞' or val == '\\infty':
            return 'infinity'
        elif val == 'a':
            return 'a'
        elif val.startswith('x_') or val.startswith('a_'):
            return val.replace('_', ' sub ')
        return val

# ===========================
# Sequence and Series Patterns
# ===========================

class SequenceSeriesHandler:
    """Handles sequences, series, and summation notation"""
    
    def __init__(self):
        self.patterns = [
            # Summation notation
            MathematicalPattern(
                r'\\sum_{([^}]+)=([^}]+)}\^{([^}]+)}\s*([^=\s]+)',
                lambda m: f'the sum from {m.group(1)} equals {m.group(2)} to {m.group(3)} of {m.group(4)}',
                PatternCategory.SEQUENCE_SERIES,
                'Finite sum with bounds',
                priority=85
            ),
            MathematicalPattern(
                r'\\sum_{([^}]+)=([^}]+)}\^{\\infty}\s*([^=\s]+)',
                lambda m: f'the sum from {m.group(1)} equals {m.group(2)} to infinity of {m.group(3)}',
                PatternCategory.SEQUENCE_SERIES,
                'Infinite series',
                priority=85
            ),
            MathematicalPattern(
                r'\\sum_{([^}]+)\\in([^}]+)}\s*([^=\s]+)',
                lambda m: f'the sum over {m.group(1)} in {m.group(2)} of {m.group(3)}',
                PatternCategory.SEQUENCE_SERIES,
                'Sum over set',
                priority=85
            ),
            
            # Product notation
            MathematicalPattern(
                r'\\prod_{([^}]+)=([^}]+)}\^{([^}]+)}\s*([^=\s]+)',
                lambda m: f'the product from {m.group(1)} equals {m.group(2)} to {m.group(3)} of {m.group(4)}',
                PatternCategory.SEQUENCE_SERIES,
                'Finite product',
                priority=85
            ),
            
            # Sequence notation
            MathematicalPattern(
                r'\{([a-z])_n\}_{n=(\d+)}\^{\\infty}',
                lambda m: f'the sequence {m.group(1)} sub n from n equals {m.group(2)} to infinity',
                PatternCategory.SEQUENCE_SERIES,
                'Infinite sequence',
                priority=80
            ),
            MathematicalPattern(
                r'\{([a-z])_n\}',
                lambda m: f'the sequence {m.group(1)} sub n',
                PatternCategory.SEQUENCE_SERIES,
                'Simple sequence',
                priority=75
            ),
            
            # Common series
            MathematicalPattern(
                r'\\sum_{n=1}\^{\\infty}\s*\\frac{1}{n\^2}',
                'the sum from n equals 1 to infinity of 1 over n squared',
                PatternCategory.SEQUENCE_SERIES,
                'p-series p=2',
                priority=90
            ),
            MathematicalPattern(
                r'\\sum_{n=0}\^{\\infty}\s*\\frac{x\^n}{n!}',
                'the sum from n equals 0 to infinity of x to the n over n factorial',
                PatternCategory.SEQUENCE_SERIES,
                'Exponential series',
                priority=90
            ),
            
            # Partial sums
            MathematicalPattern(
                r'S_n\s*=\s*\\sum_{k=1}\^{n}',
                'S sub n equals the sum from k equals 1 to n',
                PatternCategory.SEQUENCE_SERIES,
                'Partial sum notation',
                priority=80
            ),
        ]

# ===========================
# Set Notation Patterns
# ===========================

class SetNotationHandler:
    """Handles set builder notation and set operations"""
    
    def __init__(self):
        self.patterns = [
            # Set builder notation
            MathematicalPattern(
                r'\{([^:|]+)[:|]([^}]+)\}',
                lambda m: f'the set of all {self._process_element(m.group(1))} such that {self._process_condition(m.group(2))}',
                PatternCategory.SET_NOTATION,
                'Set builder notation',
                priority=85
            ),
            
            # Common sets
            MathematicalPattern(
                r'\\mathbb{R}\^n',
                'n-dimensional Euclidean space',
                PatternCategory.SET_NOTATION,
                'R^n',
                priority=90
            ),
            MathematicalPattern(
                r'\\mathbb{R}\^([0-9]+)',
                lambda m: f'{self._number_to_word(m.group(1))}-dimensional Euclidean space',
                PatternCategory.SET_NOTATION,
                'R^d for specific d',
                priority=90
            ),
            
            # Set operations
            MathematicalPattern(
                r'([A-Z])\s*\\cup\s*([A-Z])',
                lambda m: f'{m.group(1)} union {m.group(2)}',
                PatternCategory.SET_NOTATION,
                'Union',
                priority=80
            ),
            MathematicalPattern(
                r'([A-Z])\s*\\cap\s*([A-Z])',
                lambda m: f'{m.group(1)} intersect {m.group(2)}',
                PatternCategory.SET_NOTATION,
                'Intersection',
                priority=80
            ),
            MathematicalPattern(
                r'([A-Z])\s*\\setminus\s*([A-Z])',
                lambda m: f'{m.group(1)} minus {m.group(2)}',
                PatternCategory.SET_NOTATION,
                'Set difference',
                priority=80
            ),
            
            # Subset relations
            MathematicalPattern(
                r'([A-Z])\s*\\subseteq\s*([A-Z])',
                lambda m: f'{m.group(1)} is a subset of {m.group(2)}',
                PatternCategory.SET_NOTATION,
                'Subset',
                priority=80
            ),
            MathematicalPattern(
                r'([A-Z])\s*\\subsetneq\s*([A-Z])',
                lambda m: f'{m.group(1)} is a proper subset of {m.group(2)}',
                PatternCategory.SET_NOTATION,
                'Proper subset',
                priority=80
            ),
            
            # Empty and universal sets
            MathematicalPattern(
                r'\\emptyset|\\varnothing',
                'the empty set',
                PatternCategory.SET_NOTATION,
                'Empty set',
                priority=90
            ),
            
            # Intervals
            MathematicalPattern(
                r'\[([^,]+),([^\]]+)\]',
                lambda m: f'the closed interval from {m.group(1)} to {m.group(2)}',
                PatternCategory.SET_NOTATION,
                'Closed interval',
                priority=85
            ),
            MathematicalPattern(
                r'\(([^,]+),([^)]+)\)',
                lambda m: f'the open interval from {m.group(1)} to {m.group(2)}',
                PatternCategory.SET_NOTATION,
                'Open interval',
                priority=85
            ),
        ]
    
    def _process_element(self, element: str) -> str:
        """Process set element description"""
        element = element.strip()
        if element == 'x':
            return 'x'
        elif element.startswith('(') and element.endswith(')'):
            # Ordered pair/tuple
            parts = element[1:-1].split(',')
            if len(parts) == 2:
                return f'ordered pairs {parts[0].strip()} comma {parts[1].strip()}'
            else:
                return f'{len(parts)}-tuples'
        return element
    
    def _process_condition(self, condition: str) -> str:
        """Process set condition"""
        condition = condition.strip()
        # Basic cleaning
        condition = re.sub(r'\\in\s*', ' is in ', condition)
        condition = re.sub(r'∈\s*', ' is in ', condition)
        return condition
    
    def _number_to_word(self, num: str) -> str:
        """Convert number to word"""
        numbers = {
            '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight',
            '9': 'nine', '10': 'ten'
        }
        return numbers.get(num, num)

# ===========================
# Proof Patterns
# ===========================

class ProofPatternHandler:
    """Handles common proof patterns and techniques"""
    
    def __init__(self):
        self.patterns = [
            # Proof techniques
            MathematicalPattern(
                r'[Pp]roof\s+by\s+induction',
                'Proof by induction',
                PatternCategory.PROOF_PATTERN,
                'Induction proof',
                priority=90
            ),
            MathematicalPattern(
                r'[Pp]roof\s+by\s+contradiction',
                'Proof by contradiction',
                PatternCategory.PROOF_PATTERN,
                'Contradiction proof',
                priority=90
            ),
            MathematicalPattern(
                r'[Pp]roof\s+by\s+contrapositive',
                'Proof by contrapositive',
                PatternCategory.PROOF_PATTERN,
                'Contrapositive proof',
                priority=90
            ),
            
            # Contradiction setup
            MathematicalPattern(
                r'[Aa]ssume\s+(?:for\s+)?(?:the\s+)?(?:sake\s+of\s+)?contradiction',
                'Assume for the sake of contradiction',
                PatternCategory.PROOF_PATTERN,
                'Contradiction assumption',
                priority=85
            ),
            MathematicalPattern(
                r'[Ss]uppose\s+(?:to\s+the\s+)?contrary',
                'Suppose to the contrary',
                PatternCategory.PROOF_PATTERN,
                'Contrary assumption',
                priority=85
            ),
            
            # Induction steps
            MathematicalPattern(
                r'[Bb]ase\s+case:\s*n\s*=\s*(\d+)',
                lambda m: f'Base case: n equals {m.group(1)}',
                PatternCategory.PROOF_PATTERN,
                'Induction base case',
                priority=85
            ),
            MathematicalPattern(
                r'[Ii]nductive?\s+step',
                'Inductive step',
                PatternCategory.PROOF_PATTERN,
                'Induction step',
                priority=85
            ),
            MathematicalPattern(
                r'[Ii]nductive?\s+hypothesis',
                'inductive hypothesis',
                PatternCategory.PROOF_PATTERN,
                'Induction hypothesis',
                priority=85
            ),
            
            # Case analysis
            MathematicalPattern(
                r'[Cc]ase\s+(\d+):',
                lambda m: f'Case {m.group(1)}:',
                PatternCategory.PROOF_PATTERN,
                'Case numbering',
                priority=80
            ),
            MathematicalPattern(
                r'[Cc]onsider\s+(?:the\s+)?(?:following\s+)?cases',
                'Consider the following cases',
                PatternCategory.PROOF_PATTERN,
                'Case introduction',
                priority=80
            ),
            
            # Common proof phrases
            MathematicalPattern(
                r'[Ii]t\s+suffices\s+to\s+show',
                'It suffices to show',
                PatternCategory.PROOF_PATTERN,
                'Sufficiency',
                priority=75
            ),
            MathematicalPattern(
                r'[Ww]ithout\s+loss\s+of\s+generality',
                'Without loss of generality',
                PatternCategory.PROOF_PATTERN,
                'WLOG',
                priority=75
            ),
            MathematicalPattern(
                r'[Tt]his\s+completes\s+the\s+proof',
                'This completes the proof',
                PatternCategory.PROOF_PATTERN,
                'Proof completion',
                priority=75
            ),
            
            # QED variants
            MathematicalPattern(
                r'Q\.E\.D\.|QED|∎|□',
                'Q.E.D.',
                PatternCategory.PROOF_PATTERN,
                'Proof end marker',
                priority=90
            ),
        ]

# ===========================
# Reference Patterns
# ===========================

class ReferencePatternHandler:
    """Handles equation numbers, theorem references, etc."""
    
    def __init__(self):
        self.patterns = [
            # Equation references
            MathematicalPattern(
                r'[Ee]quation\s*\((\d+(?:\.\d+)?)\)',
                lambda m: f'equation {m.group(1)}',
                PatternCategory.REFERENCE,
                'Equation reference',
                priority=85
            ),
            MathematicalPattern(
                r'[Ee]qs?\.\s*\((\d+(?:\.\d+)?)\)',
                lambda m: f'equation {m.group(1)}',
                PatternCategory.REFERENCE,
                'Abbreviated equation ref',
                priority=85
            ),
            
            # Theorem/Lemma references
            MathematicalPattern(
                r'[Tt]heorem\s+(\d+(?:\.\d+)?)',
                lambda m: f'Theorem {m.group(1)}',
                PatternCategory.REFERENCE,
                'Theorem reference',
                priority=85
            ),
            MathematicalPattern(
                r'[Ll]emma\s+(\d+(?:\.\d+)?)',
                lambda m: f'Lemma {m.group(1)}',
                PatternCategory.REFERENCE,
                'Lemma reference',
                priority=85
            ),
            MathematicalPattern(
                r'[Pp]roposition\s+(\d+(?:\.\d+)?)',
                lambda m: f'Proposition {m.group(1)}',
                PatternCategory.REFERENCE,
                'Proposition reference',
                priority=85
            ),
            
            # Section references
            MathematicalPattern(
                r'[Ss]ection\s+(\d+(?:\.\d+)?)',
                lambda m: f'Section {m.group(1)}',
                PatternCategory.REFERENCE,
                'Section reference',
                priority=85
            ),
            MathematicalPattern(
                r'[Cc]hapter\s+(\d+)',
                lambda m: f'Chapter {m.group(1)}',
                PatternCategory.REFERENCE,
                'Chapter reference',
                priority=85
            ),
            
            # LaTeX references
            MathematicalPattern(
                r'\\ref\{([^}]+)\}',
                lambda m: f'reference {m.group(1)}',
                PatternCategory.REFERENCE,
                'LaTeX ref',
                priority=80
            ),
            MathematicalPattern(
                r'\\eqref\{([^}]+)\}',
                lambda m: f'equation reference {m.group(1)}',
                PatternCategory.REFERENCE,
                'LaTeX eqref',
                priority=80
            ),
            
            # Citation patterns
            MathematicalPattern(
                r'\\cite\{([^}]+)\}',
                lambda m: f'citation {m.group(1)}',
                PatternCategory.REFERENCE,
                'LaTeX cite',
                priority=80
            ),
            MathematicalPattern(
                r'\[(\d+(?:,\s*\d+)*)\]',
                lambda m: f'reference {m.group(1)}',
                PatternCategory.REFERENCE,
                'Numeric citation',
                priority=75
            ),
            
            # Cross-reference phrases
            MathematicalPattern(
                r'[Ss]ee\s+[Tt]heorem\s+(\d+(?:\.\d+)?)',
                lambda m: f'see Theorem {m.group(1)}',
                PatternCategory.REFERENCE,
                'See theorem',
                priority=80
            ),
            MathematicalPattern(
                r'[Bb]y\s+[Ll]emma\s+(\d+(?:\.\d+)?)',
                lambda m: f'by Lemma {m.group(1)}',
                PatternCategory.REFERENCE,
                'By lemma',
                priority=80
            ),
        ]

# ===========================
# Common Expression Handler
# ===========================

class CommonExpressionHandler:
    """Handles frequently occurring mathematical expressions"""
    
    def __init__(self):
        self.patterns = [
            # Integrals - must be before other patterns to catch full expressions
            MathematicalPattern(
                r'\\int_([^\\s\{]+)\^([^\\s\{]+)\s*([^\\]+?)\s*d([a-z])',
                lambda m: f'integral from {self._process_limit(m.group(1))} to {self._process_limit(m.group(2))} of {m.group(3)} d {m.group(4)}',
                PatternCategory.COMMON_EXPRESSION,
                'Definite integral with limits no braces',
                priority=99
            ),
            MathematicalPattern(
                r'\\int_\{([^}]+)\}\^\{([^}]+)\}\s*([^\\]+?)\s*d([a-z])',
                lambda m: f'integral from {self._process_limit(m.group(1))} to {self._process_limit(m.group(2))} of {m.group(3)} d {m.group(4)}',
                PatternCategory.COMMON_EXPRESSION,
                'Definite integral with braces',
                priority=98
            ),
            MathematicalPattern(
                r'\\int\s*([^\\]+?)\s*d([a-z])',
                lambda m: f'integral of {m.group(1)} d {m.group(2)}',
                PatternCategory.COMMON_EXPRESSION,
                'Indefinite integral',
                priority=97
            ),
            MathematicalPattern(
                r'int_([^\\\s]+)\^\s*([^\\\s]+)\s*([^\\]+?)\s*d([a-z])',
                lambda m: f'integral from {self._process_limit(m.group(1))} to {self._process_limit(m.group(2))} of {m.group(3)} d {m.group(4)}',
                PatternCategory.COMMON_EXPRESSION,
                'Definite integral without backslash',
                priority=98
            ),
            
            # Common equalities
            MathematicalPattern(
                r'e\^{i\\pi}\s*=\s*-1',
                'e to the i pi equals negative one',
                PatternCategory.COMMON_EXPRESSION,
                "Euler's identity",
                priority=95
            ),
            MathematicalPattern(
                r'e\^\{i\\theta\}\s*=\s*\\cos\\theta\s*\+\s*i\\sin\\theta',
                'e to the i theta equals cosine theta plus i sine theta',
                PatternCategory.COMMON_EXPRESSION,
                "Euler's formula",
                priority=95
            ),
            
            # Pythagorean theorem
            MathematicalPattern(
                r'a\^2\s*\+\s*b\^2\s*=\s*c\^2',
                'a squared plus b squared equals c squared',
                PatternCategory.COMMON_EXPRESSION,
                'Pythagorean theorem',
                priority=95
            ),
            
            # Binomial coefficient
            MathematicalPattern(
                r'\\binom\{n\}\{k\}',
                'n choose k',
                PatternCategory.COMMON_EXPRESSION,
                'Binomial coefficient',
                priority=90
            ),
            MathematicalPattern(
                r'\\left\(\\begin\{array\}\{c\}n\\\\k\\end\{array\}\\right\)',
                'n choose k',
                PatternCategory.COMMON_EXPRESSION,
                'Binomial coefficient array',
                priority=90
            ),
            MathematicalPattern(
                r'C\(n,k\)|C_n\^k',
                'n choose k',
                PatternCategory.COMMON_EXPRESSION,
                'Binomial coefficient notation',
                priority=90
            ),
            
            # Factorial
            MathematicalPattern(
                r'(\d+)!',
                lambda m: f'{m.group(1)} factorial',
                PatternCategory.COMMON_EXPRESSION,
                'Factorial',
                priority=85
            ),
            MathematicalPattern(
                r'n!',
                'n factorial',
                PatternCategory.COMMON_EXPRESSION,
                'n factorial',
                priority=85
            ),
            
            # Fractions - general pattern first
            MathematicalPattern(
                r'\\frac\{([^}]+)\}\{([^}]+)\}',
                lambda m: self._process_fraction(m.group(1), m.group(2)),
                PatternCategory.COMMON_EXPRESSION,
                'General fraction',
                priority=89
            ),
            MathematicalPattern(
                r'frac\{([^}]+)\}\{([^}]+)\}',
                lambda m: f'{m.group(1)} over {m.group(2)}',
                PatternCategory.COMMON_EXPRESSION,
                'Fraction without backslash',
                priority=89
            ),
            MathematicalPattern(
                r'frac\s+(sqrt|\\sqrt)\s+(pi|\\pi)(\d*)',
                lambda m: f'square root of pi{m.group(3)} over',
                PatternCategory.COMMON_EXPRESSION,
                'Special fraction sqrt pi',
                priority=89
            ),
            
            # Common fractions - handle special cases first
            MathematicalPattern(
                r'\\frac\{\\sqrt\{\\pi\}\}\{2\}',
                'square root of pi over 2',
                PatternCategory.COMMON_EXPRESSION,
                'Sqrt(pi)/2',
                priority=91
            ),
            MathematicalPattern(
                r'\\frac\{1\}\{2\}',
                'one half',
                PatternCategory.COMMON_EXPRESSION,
                'One half',
                priority=90
            ),
            MathematicalPattern(
                r'\\frac\{1\}\{3\}',
                'one third',
                PatternCategory.COMMON_EXPRESSION,
                'One third',
                priority=90
            ),
            MathematicalPattern(
                r'\\frac\{\\pi\}\{2\}',
                'pi over 2',
                PatternCategory.COMMON_EXPRESSION,
                'Pi/2',
                priority=90
            ),
            
            # Square roots
            MathematicalPattern(
                r'\\sqrt\{2\}',
                'square root of 2',
                PatternCategory.COMMON_EXPRESSION,
                'Sqrt(2)',
                priority=90
            ),
            MathematicalPattern(
                r'\\sqrt\{([^}]+)\}',
                lambda m: f'square root of {m.group(1)}',
                PatternCategory.COMMON_EXPRESSION,
                'General square root',
                priority=85
            ),
            
            # Exponents and special functions
            MathematicalPattern(
                r'e\^\{-([a-z])\^2\}',
                lambda m: f'e to the negative {m.group(1)} squared',
                PatternCategory.COMMON_EXPRESSION,
                'Gaussian exponent',
                priority=92
            ),
            MathematicalPattern(
                r'e\^\{([^}]+)\}',
                lambda m: f'e to the {m.group(1)}',
                PatternCategory.COMMON_EXPRESSION,
                'General exponential',
                priority=91
            ),
            MathematicalPattern(
                r'e\^-([a-z])\^2',
                lambda m: f'e to the negative {m.group(1)} squared',
                PatternCategory.COMMON_EXPRESSION,
                'Gaussian exponent without braces',
                priority=92
            ),
            
            # Infinity
            MathematicalPattern(
                r'\\infty',
                'infinity',
                PatternCategory.COMMON_EXPRESSION,
                'Infinity',
                priority=95
            ),
            MathematicalPattern(
                r'∞',
                'infinity',
                PatternCategory.COMMON_EXPRESSION,
                'Infinity symbol',
                priority=95
            ),
            MathematicalPattern(
                r'infty',
                'infinity',
                PatternCategory.COMMON_EXPRESSION,
                'Infinity without backslash',
                priority=95
            ),
            
            # Common functions
            MathematicalPattern(
                r'\\sin\^2\s*([θx])\s*\+\s*\\cos\^2\s*([θx])',
                lambda m: f'sine squared {m.group(1)} plus cosine squared {m.group(2)}',
                PatternCategory.COMMON_EXPRESSION,
                'Pythagorean identity',
                priority=90
            ),
        ]
    
    def _process_limit(self, limit: str) -> str:
        """Process integral limits"""
        limit = limit.strip()
        if limit == '0':
            return 'zero'
        elif limit == '1':
            return 'one'
        elif limit in ['infty', '\\infty', '∞']:
            return 'infinity'
        elif limit == '-infty' or limit == '-\\infty':
            return 'negative infinity'
        elif limit == 'pi' or limit == '\\pi':
            return 'pi'
        else:
            return limit
    
    def _process_fraction(self, numerator: str, denominator: str) -> str:
        """Process fraction components"""
        # Clean up any remaining LaTeX commands
        numerator = numerator.strip()
        denominator = denominator.strip()
        
        # Handle common denominators
        if denominator == '2':
            if numerator == '1':
                return 'one half'
            elif numerator == '\\pi':
                return 'pi over 2'
            elif numerator == 'pi':
                return 'pi over 2'
        elif denominator == '3' and numerator == '1':
            return 'one third'
        elif denominator == '4' and numerator == '1':
            return 'one fourth'
        
        # General case
        return f'{numerator} over {denominator}'

# ===========================
# Main Pattern Processor
# ===========================

class PatternProcessor:
    """Main processor that applies all mathematical patterns"""
    
    def __init__(self):
        # Initialize all handlers
        self.handlers = {
            PatternCategory.EPSILON_DELTA: EpsilonDeltaHandler(),
            PatternCategory.LIMIT_EXPRESSION: LimitPatternHandler(),
            PatternCategory.SEQUENCE_SERIES: SequenceSeriesHandler(),
            PatternCategory.SET_NOTATION: SetNotationHandler(),
            PatternCategory.PROOF_PATTERN: ProofPatternHandler(),
            PatternCategory.REFERENCE: ReferencePatternHandler(),
            PatternCategory.COMMON_EXPRESSION: CommonExpressionHandler(),
        }
        
        # Collect all patterns
        self.all_patterns: List[MathematicalPattern] = []
        for handler in self.handlers.values():
            self.all_patterns.extend(handler.patterns)
        
        # Sort by priority (highest first)
        self.all_patterns.sort(key=lambda p: p.priority, reverse=True)
        
        logger.info(f"Pattern processor initialized with {len(self.all_patterns)} patterns")
    
    def process(self, text: str) -> str:
        """Apply all patterns to text"""
        processed = text
        
        # Apply patterns in priority order
        for pattern in self.all_patterns:
            if callable(pattern.replacement):
                processed = pattern.compiled.sub(pattern.replacement, processed)
            else:
                processed = pattern.compiled.sub(pattern.replacement, processed)
        
        return processed
    
    def process_by_category(self, text: str, categories: List[PatternCategory]) -> str:
        """Apply only patterns from specific categories"""
        processed = text
        
        # Filter patterns by category
        relevant_patterns = [
            p for p in self.all_patterns 
            if p.category in categories
        ]
        
        # Apply relevant patterns
        for pattern in relevant_patterns:
            if callable(pattern.replacement):
                processed = pattern.compiled.sub(pattern.replacement, processed)
            else:
                processed = pattern.compiled.sub(pattern.replacement, processed)
        
        return processed
    
    def get_pattern_statistics(self) -> Dict[str, int]:
        """Get statistics about loaded patterns"""
        stats = {}
        for category in PatternCategory:
            count = sum(1 for p in self.all_patterns if p.category == category)
            stats[category.value] = count
        stats['total'] = len(self.all_patterns)
        return stats

# ===========================
# Convenience Functions
# ===========================

def apply_common_patterns(text: str) -> str:
    """Quick function to apply common patterns to text"""
    processor = PatternProcessor()
    return processor.process(text)

def apply_epsilon_delta_patterns(text: str) -> str:
    """Apply only epsilon-delta patterns"""
    processor = PatternProcessor()
    return processor.process_by_category(text, [PatternCategory.EPSILON_DELTA])

def apply_proof_patterns(text: str) -> str:
    """Apply only proof-related patterns"""
    processor = PatternProcessor()
    return processor.process_by_category(text, [PatternCategory.PROOF_PATTERN])

# ===========================
# Testing Functions
# ===========================

def test_pattern_processor():
    """Test pattern processing"""
    processor = PatternProcessor()
    
    test_cases = [
        # Epsilon-delta
        "∀ε>0 ∃δ>0 s.t. 0<|x-a|<δ ⟹ |f(x)-L|<ε",
        "Choose δ = min{1, ε/2}",
        
        # Limits
        "\\lim_{x\\to 0} \\frac{\\sin x}{x} = 1",
        "\\lim_{n\\to\\infty} (1 + \\frac{1}{n})^n = e",
        
        # Series
        "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}",
        "S_n = \\sum_{k=1}^{n} a_k",
        
        # Sets
        "{x ∈ ℝ | x² < 1}",
        "A ∪ B = {x | x ∈ A or x ∈ B}",
        
        # Proofs
        "Proof by contradiction. Assume not.",
        "Base case: n = 1",
        "This completes the proof. Q.E.D.",
        
        # References
        "By Theorem 3.2, we have...",
        "See equation (4.5) for details.",
        
        # Common expressions
        "e^{iπ} = -1",
        "a² + b² = c²",
        "\\binom{n}{k} = \\frac{n!}{k!(n-k)!}",
    ]
    
    print("Testing Pattern Processor")
    print("=" * 60)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input:  {test}")
        result = processor.process(test)
        print(f"Output: {result}")
    
    print("\nPattern Statistics:")
    stats = processor.get_pattern_statistics()
    for category, count in stats.items():
        print(f"  {category}: {count} patterns")

if __name__ == "__main__":
    test_pattern_processor()