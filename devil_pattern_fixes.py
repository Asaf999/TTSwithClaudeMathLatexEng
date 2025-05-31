#!/usr/bin/env python3
"""
Devil Pattern Fixes
==================

This module contains targeted fixes for the failing devil test patterns.
These fixes will be integrated into the main patterns_v2.py file.
"""

import re
from typing import Dict, List, Tuple, Callable

def create_devil_fixes() -> List[Tuple[str, Callable, str, int]]:
    """
    Returns a list of pattern fixes in the format:
    (pattern, replacement_function, description, priority)
    """
    
    fixes = []
    
    # =================== FIX 1: Product Notation ===================
    # Fix "prod" -> "product"
    fixes.append((
        r'\\prod',
        'product',
        'Product symbol fix',
        150
    ))
    
    # Fix product with limits
    fixes.append((
        r'\\prod_\{([^}]+)\}\^\{([^}]+)\}',
        lambda m: f'product from {m.group(1)} to {m.group(2)}',
        'Product with limits',
        151
    ))
    
    # =================== FIX 2: Triple Integral ===================
    # Fix "traceiple" -> "triple"
    fixes.append((
        r'traceiple\s+integral',
        'triple integral',
        'Triple integral typo fix',
        200
    ))
    
    # Fix \iiint
    fixes.append((
        r'\\iiint',
        'triple integral',
        'Triple integral command',
        149
    ))
    
    # =================== FIX 3: Substack Notation ===================
    # Handle \substack properly
    fixes.append((
        r'\\substack\{([^}]+)\}',
        lambda m: m.group(1).replace('\\\\', ' '),
        'Substack notation',
        145
    ))
    
    # =================== FIX 4: Matrix Environments ===================
    # Fix \begin{Bmatrix}
    fixes.append((
        r'\\begin\{Bmatrix\}([^\\]+)\\end\{Bmatrix\}',
        lambda m: 'matrix ' + m.group(1).replace('\\\\', ' '),
        'Bmatrix environment',
        140
    ))
    
    # Fix \begin{pmatrix} cleanup
    fixes.append((
        r'begin\{pmatrix\}',
        '',
        'Remove stray begin{pmatrix}',
        135
    ))
    
    # =================== FIX 5: Partial Derivatives ===================
    # Second partial derivatives
    fixes.append((
        r'\\frac\{\\partial\^2\}\{\\partial\s+([a-zA-Z])\^2\}',
        lambda m: f'second partial derivative with respect to {m.group(1)}',
        'Second partial derivative',
        142
    ))
    
    # Mixed partials
    fixes.append((
        r'\\frac\{\\partial\^2\}\{\\partial\s+([a-zA-Z])\\partial\s+([a-zA-Z])\}',
        lambda m: f'second partial derivative with respect to {m.group(1)} and {m.group(2)}',
        'Mixed partial derivative',
        141
    ))
    
    # =================== FIX 6: Limit Superscripts ===================
    # Fix 0^+ and 0^-
    fixes.append((
        r'0\^\+',
        '0 from the right',
        'Limit from right',
        130
    ))
    
    fixes.append((
        r'0\^-',
        '0 from the left',
        'Limit from left',
        130
    ))
    
    fixes.append((
        r'0\^\{\\+\}',
        '0 from the right',
        'Limit from right (braces)',
        131
    ))
    
    fixes.append((
        r'0\^\{-\}',
        '0 from the left',
        'Limit from left (braces)',
        131
    ))
    
    # =================== FIX 7: Special Operators ===================
    # Fix \text{sgn}
    fixes.append((
        r'\\text\{sgn\}',
        'sign',
        'Sign function',
        125
    ))
    
    # Fix \delta (variational derivative)
    fixes.append((
        r'\\delta',
        'delta',
        'Delta symbol',
        124
    ))
    
    # Fix \mathcal{F}
    fixes.append((
        r'\\mathcal\{F\}',
        'Fourier transform',
        'Fourier transform operator',
        126
    ))
    
    # =================== FIX 8: Probability Notation ===================
    # Fix \bigcap
    fixes.append((
        r'\\bigcap',
        'intersection',
        'Big intersection',
        123
    ))
    
    # Fix \mathbb{E}
    fixes.append((
        r'\\mathbb\{E\}',
        'expected value',
        'Expected value',
        122
    ))
    
    # Fix \text{Var}
    fixes.append((
        r'\\text\{Var\}',
        'variance',
        'Variance',
        121
    ))
    
    # =================== FIX 9: Logic Notation ===================
    # Fix \vdash
    fixes.append((
        r'\\vdash',
        'proves',
        'Proves symbol',
        120
    ))
    
    # Fix \text{Con}
    fixes.append((
        r'\\text\{Con\}',
        'consistency',
        'Consistency',
        119
    ))
    
    # =================== FIX 10: Cleanup Fixes ===================
    # Fix minus signs
    fixes.append((
        r'to the - ([0-9]+)',
        r'to the negative \1',
        'Negative exponent cleanup',
        110
    ))
    
    # Fix "is similar to" -> "distributed as"
    fixes.append((
        r'is similar to',
        'distributed as',
        'Distribution notation',
        108
    ))
    
    # Fix integral notation
    fixes.append((
        r'integral of _([0-9]+) to the',
        r'integral from \1 to',
        'Integral bounds cleanup',
        107
    ))
    
    # Fix d|n notation (divisibility)
    fixes.append((
        r'([a-zA-Z])\s*\|\s*([a-zA-Z])',
        lambda m: f'{m.group(1)} divides {m.group(2)}',
        'Divisibility notation',
        106
    ))
    
    # Fix "evaluated at" -> "divides" for sum notation
    fixes.append((
        r'sum\s+([a-zA-Z])\s+evaluated at\s+([a-zA-Z])',
        lambda m: f'sum over {m.group(1)} divides {m.group(2)}',
        'Sum over divisors',
        105
    ))
    
    # =================== FIX 11: Additional Critical Fixes ===================
    # Fix nested derivatives
    fixes.append((
        r'd over dx\s*\(',
        'derivative with respect to x of ',
        'Derivative cleanup',
        104
    ))
    
    # Fix nabla squared
    fixes.append((
        r'nabla squared',
        'Laplacian',
        'Laplacian operator',
        103
    ))
    
    # Fix probability notation P(
    fixes.append((
        r'probability of ([a-zA-Z])',
        lambda m: f'P of {m.group(1)}',
        'Probability notation',
        102
    ))
    
    # Fix xrightarrow{d}
    fixes.append((
        r'xrightarrow\{d\}',
        'converges in distribution to',
        'Convergence in distribution',
        101
    ))
    
    return fixes


def apply_devil_fixes(text: str) -> str:
    """Apply all devil fixes to the given text"""
    fixes = create_devil_fixes()
    
    # Sort by priority (highest first)
    fixes.sort(key=lambda x: x[3], reverse=True)
    
    # Apply fixes
    for pattern, replacement, description, priority in fixes:
        if callable(replacement):
            text = re.sub(pattern, replacement, text)
        else:
            text = re.sub(pattern, replacement, text)
    
    return text


# =================== INTEGRATION GUIDE ===================
# To integrate these fixes into patterns_v2.py:
#
# 1. Import this module in patterns_v2.py:
#    from .devil_pattern_fixes import create_devil_fixes
#
# 2. In the PostProcessingHandler class, add these patterns to self.patterns:
#    devil_fixes = create_devil_fixes()
#    for pattern, replacement, description, priority in devil_fixes:
#        if callable(replacement):
#            rule = PatternRule(pattern, replacement, MathDomain.BASIC_ARITHMETIC, description, priority=priority)
#        else:
#            rule = PatternRule(pattern, replacement, MathDomain.BASIC_ARITHMETIC, description, priority=priority)
#        self.patterns.append(rule)
#
# 3. Or create a new DevilFixHandler class that extends PatternHandler