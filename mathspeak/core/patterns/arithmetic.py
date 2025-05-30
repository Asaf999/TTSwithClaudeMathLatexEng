#!/usr/bin/env python3
"""
Basic Arithmetic Pattern Handler
===============================

Handles basic arithmetic operations with natural speech patterns.
"""

from .base import PatternHandler, PatternRule, MathDomain

class BasicArithmeticHandler(PatternHandler):
    """Handles basic arithmetic operations naturally"""
    
    def __init__(self):
        super().__init__(MathDomain.BASIC_ARITHMETIC)
    
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