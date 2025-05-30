#!/usr/bin/env python3
"""
Algebra Pattern Handler
======================

Handles algebraic expressions naturally, including:
- Powers and exponents with natural speech
- Subscripts and variable notation
- Fractions using "over" 
- Roots and radicals
- Decorated variables (hat, tilde, bar)
- Polynomial expressions
- Binomial expansions
- Absolute values
"""

import re
import logging
from typing import Dict, List, Optional, Tuple, Union, Callable, Any
from .base import PatternHandler, PatternRule, MathDomain

logger = logging.getLogger(__name__)

class AlgebraHandler(PatternHandler):
    """Handles algebraic expressions naturally"""
    
    def __init__(self):
        """Initialize with ALGEBRA domain"""
        super().__init__(MathDomain.ALGEBRA)
    
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
            
            # Mixed numbers - must come before fraction patterns
            PatternRule(
                r'(\d+)\\frac\{(\d+)\}\{(\d+)\}',
                lambda m: f'{m.group(1)} and {m.group(2)} over {m.group(3)}',
                self.domain,
                'Mixed number',
                priority=105  # Higher priority than regular fractions
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