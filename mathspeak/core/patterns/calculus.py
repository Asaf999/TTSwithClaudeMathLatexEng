#!/usr/bin/env python3
"""
Calculus and Analysis Patterns
==============================

This module implements natural speech patterns for calculus and mathematical analysis
expressions, focusing on how real professors speak mathematics.

Includes patterns for:
- Derivatives (prime notation, Leibniz notation)
- Partial derivatives 
- Integrals (definite, indefinite, multiple)
- Limits and limit notation
- Series and summations
- Differentials
- Vector calculus (gradient, divergence, curl)
"""

from .base import PatternHandler, PatternRule, MathDomain


class CalculusHandler(PatternHandler):
    """Handles calculus notation naturally"""
    
    def __init__(self):
        super().__init__(MathDomain.CALCULUS)
    
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
            
            # Leibniz notation - FIXED for natural speech
            PatternRule(
                r'\\frac\{d\}\{d([a-zA-Z])\}\s*([a-zA-Z])\(([a-zA-Z])\)',
                lambda m: f'derivative of {m.group(2)} of {m.group(3)}',
                self.domain,
                'Derivative of function',
                priority=100
            ),
            PatternRule(
                r'\\frac\{d\}\{d([a-zA-Z])\}\s*([a-zA-Z]+)',
                lambda m: f'derivative of {m.group(2)}',
                self.domain,
                'Derivative operator applied',
                priority=100
            ),
            PatternRule(
                r'\\frac\{d([a-zA-Z]*)\}\{d([a-zA-Z])\}',
                lambda m: f'derivative of {m.group(1)} with respect to {m.group(2)}' if m.group(1) else f'derivative with respect to {m.group(2)}',
                self.domain,
                'General derivative',
                priority=99
            ),
            PatternRule(
                r'\\frac\{dy\}\{dx\}',
                'derivative of y with respect to x',
                self.domain,
                'dy/dx',
                priority=99
            ),
            PatternRule(
                r'\\frac\{df\}\{dx\}',
                'derivative of f with respect to x',
                self.domain,
                'df/dx',
                priority=99
            ),
            PatternRule(
                r'\\frac\{d\^2\}\{d([a-zA-Z])\^2\}',
                lambda m: f'second derivative with respect to {m.group(1)}',
                self.domain,
                'Second derivative operator',
                priority=100
            ),
            PatternRule(
                r'\\frac\{d\^2([a-zA-Z]*)\}\{d([a-zA-Z])\^2\}',
                lambda m: f'second derivative of {m.group(1)} with respect to {m.group(2)}' if m.group(1) else f'second derivative with respect to {m.group(2)}',
                self.domain,
                'Second derivative',
                priority=99
            ),
            
            # Partial derivatives - FIXED for natural speech
            PatternRule(
                r'\\frac\{\\partial ([a-zA-Z])\}\{\\partial ([a-zA-Z])\}',
                lambda m: f'partial derivative of {m.group(1)} with respect to {m.group(2)}',
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
            
            # Integrals - enhanced for nested cases
            # Nested integral bounds (very high priority)
            PatternRule(
                r'\\int_\{\\int_([^}]*)\^\{([^}]*)\}\s*([^}d]*)\s*d([a-zA-Z])\}\^\{\\int_([^}]*)\^\{([^}]*)\}\s*([^}d]*)\s*d([a-zA-Z])\}\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral from integral from {self._process_bound(m.group(1))} to {self._process_bound(m.group(2))} of {m.group(3).strip()} d{m.group(4)} to integral from {self._process_bound(m.group(5))} to {self._process_bound(m.group(6))} of {m.group(7).strip()} d{m.group(8)} of {m.group(9).strip()} d{m.group(10)}',
                self.domain,
                'Nested integral bounds',
                priority=125
            ),
            # Handle complex bounds first
            PatternRule(
                r'\\int_\{([^}]+)\}\^\{([^}]+)\}\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral from {self._process_bound(m.group(1))} to {self._process_bound(m.group(2))} of {m.group(3).strip()} d{m.group(4)}',
                self.domain,
                'Definite integral complex bounds',
                priority=109
            ),
            PatternRule(
                r'\\int_([a-zA-Z0-9])\^\{([^}]+)\}\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral from {self._process_bound(m.group(1))} to {self._process_bound(m.group(2))} of {m.group(3).strip()} d{m.group(4)}',
                self.domain,
                'Definite integral mixed bounds',
                priority=108
            ),
            PatternRule(
                r'\\int_([a-zA-Z0-9])\^([a-zA-Z0-9])\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral from {self._process_bound(m.group(1))} to {self._process_bound(m.group(2))} of {m.group(3).strip()} d{m.group(4)}',
                self.domain,
                'Definite integral simple bounds',
                priority=107
            ),
            PatternRule(
                r'\\int\s+([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral of {m.group(1).strip()} d{m.group(2)}',
                self.domain,
                'Indefinite integral with space',
                priority=97
            ),
            PatternRule(
                r'\\int\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral of {m.group(1).strip()} d{m.group(2)}',
                self.domain,
                'Indefinite integral no space',
                priority=96
            ),
            PatternRule(
                r'\\int_0\^\{\\\\infty\}\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral from 0 to infinity of {m.group(1).strip()} d{m.group(2)}',
                self.domain,
                'Common integral 0 to infinity',
                priority=111
            ),
            PatternRule(
                r'\\int_0\^1\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'integral from 0 to 1 of {m.group(1).strip()} d{m.group(2)}',
                self.domain,
                'Common integral 0 to 1',
                priority=110
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
                r'\\iint_([a-zA-Z])\s*([^d]+)\s*d([a-zA-Z])\s*d([a-zA-Z])',
                lambda m: f'double integral over {m.group(1)} of {m.group(2).strip()} d{m.group(3)} d{m.group(4)}',
                self.domain,
                'Double integral with region',
                priority=99
            ),
            PatternRule(
                r'\\iint',
                'double integral',
                self.domain,
                'Double integral',
                priority=98
            ),
            PatternRule(
                r'\\iiint_([a-zA-Z])\s*([^d]+)\s*d([a-zA-Z])\s*d([a-zA-Z])\s*d([a-zA-Z])',
                lambda m: f'triple integral over {m.group(1)} of {m.group(2).strip()} d{m.group(3)} d{m.group(4)} d{m.group(5)}',
                self.domain,
                'Triple integral with region',
                priority=99
            ),
            PatternRule(
                r'\\iiint',
                'triple integral',
                self.domain,
                'Triple integral',
                priority=98
            ),
            PatternRule(
                r'\\oint_([a-zA-Z])\s*([^d]+)\s*d([a-zA-Z])',
                lambda m: f'contour integral over {m.group(1)} of {m.group(2).strip()} d{m.group(3)}',
                self.domain,
                'Contour integral with path',
                priority=99
            ),
            PatternRule(
                r'\\oint',
                'contour integral',
                self.domain,
                'Contour integral',
                priority=98
            ),
            
            # Limits - enhanced for nested cases
            # Nested limits (very high priority)
            PatternRule(
                r'\\lim_\{([a-zA-Z])\s*\\to\s*\\lim_\{([a-zA-Z])\s*\\to\s*([^}]+)\}\s*([^}]*)\}',
                lambda m: f'limit as {m.group(1)} approaches limit as {m.group(2)} approaches {self._process_limit_value(m.group(3))} {m.group(4).strip()}',
                self.domain,
                'Nested limits',
                priority=120
            ),
            # One-sided limits
            PatternRule(
                r'\\lim_\{([a-zA-Z])\s*\\to\s*([^}]+)\^\+\}',
                lambda m: f'limit as {m.group(1)} approaches {self._process_limit_value(m.group(2))} from the right',
                self.domain,
                'One-sided limit right',
                priority=100
            ),
            PatternRule(
                r'\\lim_\{([a-zA-Z])\s*\\to\s*([^}]+)\^\-\}',
                lambda m: f'limit as {m.group(1)} approaches {self._process_limit_value(m.group(2))} from the left',
                self.domain,
                'One-sided limit left',
                priority=100
            ),
            PatternRule(
                r'\\lim_\{([^}]+)\\to\s*([^}]+)\}',
                lambda m: f'limit as {m.group(1)} approaches {self._process_limit_value(m.group(2))}',
                self.domain,
                'Basic limit',
                priority=98
            ),
            PatternRule(
                r'\\lim_{([a-zA-Z])\\to\s*([^}]+)}',
                lambda m: f'limit as {m.group(1)} approaches {self._process_limit_value(m.group(2))}',
                self.domain,
                'Basic limit simple',
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
            
            # Series and summations
            PatternRule(
                r'\\sum_\{([^}]+)\}\^\{([^}]+)\}',
                lambda m: f'sum from {self._process_bound(m.group(1))} to {self._process_bound(m.group(2))}',
                self.domain,
                'General summation',
                priority=99
            ),
            PatternRule(
                r'\\sum_\{([^}]+)\}',
                lambda m: f'sum over {self._process_bound(m.group(1))}',
                self.domain,
                'Sum over index',
                priority=98
            ),
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
                'dx',
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
        elif value == '0^+':
            return '0 from the right'
        elif value == '0^-':
            return '0 from the left'
        elif value == '\\infty':
            return 'infinity'
        elif value == '-\\infty':
            return 'negative infinity'
        elif value == 'a':
            return 'a'
        else:
            return value
    
    def _process_bound(self, bound: str) -> str:
        """Process integral/sum bounds"""
        bound = bound.strip()
        if bound == '0':
            return '0'
        elif bound == '1':
            return '1'
        elif bound == '\\infty':
            return 'infinity'
        elif bound == '-\\infty':
            return 'negative infinity'
        elif bound == 'n=1':
            return 'n equals 1'
        elif bound == 'i=1':
            return 'i equals 1'
        elif '=' in bound:
            var, val = bound.split('=', 1)
            return f'{var.strip()} equals {val.strip()}'
        else:
            return bound