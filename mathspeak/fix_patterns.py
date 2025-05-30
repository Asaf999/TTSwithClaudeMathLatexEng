#!/usr/bin/env python3
"""
Quick fixes for missing patterns
"""

import re
from typing import Dict, List, Tuple

# Additional patterns to add
MISSING_PATTERNS = [
    # Division
    (r'\\div', 'divided by'),
    
    # Multiplication variations
    (r'(\d+)\s*\\cdot\s*(\d+)', lambda m: f'{m.group(1)} dot {m.group(2)}'),
    
    # Trig functions
    (r'\\tan\(([^)]+)\)', lambda m: f'tangent of {m.group(1)}'),
    (r'\\tan\s+([a-zA-Z0-9]+)', lambda m: f'tangent {m.group(1)}'),
    
    # Mixed numbers - fix pattern
    (r'(\d+)\\frac\{(\d+)\}\{(\d+)\}', lambda m: f'{m.group(1)} and {m.group(2)} over {m.group(3)}'),
    
    # Hyperbolic with h
    (r'\\sinh\s+', 'hyperbolic sine '),
    (r'\\cosh\s+', 'hyperbolic cosine '),
    (r'\\tanh\s+', 'hyperbolic tangent '),
    
    # Similar/congruent
    (r'\\sim', 'is similar to'),
    (r'\\cong', 'is congruent to'),
    
    # Arc functions
    (r'\\sin\^{-1}', 'arc sine'),
    (r'\\cos\^{-1}', 'arc cosine'),
    (r'\\tan\^{-1}', 'arc tangent'),
    
    # nth root
    (r'\\sqrt\[n\]\{([^}]+)\}', lambda m: f'nth root of {m.group(1)}'),
    
    # Sign function 
    (r'\\text\{sgn\}', 'sign'),
    
    # Max/min with braces
    (r'\\min\\\{([^}]+)\\\}', lambda m: f'minimum of {m.group(1)}'),
    
    # Special sets
    (r'\\emptyset', 'empty set'),
    (r'\\mathcal\{U\}', 'universal set'),
    (r'\\mathcal\{P\}', 'power set'),
    
    # Cartesian product
    (r'\\times', 'cross'),
    
    # QED
    (r'\\square', 'Q E D'),
    
    # Matrix operations
    (r'\^T\b', 'transpose'),
    (r'\^{-1}\b', 'inverse'),
    (r'\\otimes', 'tensor'),
    
    # Decorated variables
    (r'\\tilde\{([^}]+)\}', lambda m: f'{m.group(1)} tilde'),
    (r'\\hat\{([^}]+)\}', lambda m: f'{m.group(1)} hat'),
    (r'\\bar\{([^}]+)\}', lambda m: f'{m.group(1)} bar'),
    
    # Units
    (r'\\text\{\s*m/s\s*\}', 'meters per second'),
    
    # Percent
    (r'(\d+)\\%', lambda m: f'{m.group(1)} percent'),
    
    # Currency
    (r'\\\$(\d+)', lambda m: f'{m.group(1)} dollars'),
    
    # Ellipsis
    (r'\\ldots', 'dot dot dot'),
    
    # Better handling of nested fractions
    (r'\\frac\{1\}\{([^}]+)\\frac', lambda m: f'1 over {m.group(1)}'),
]

def test_patterns():
    """Test the missing patterns"""
    test_cases = [
        (r"a \div b", "a divided by b"),
        (r"2 \cdot 3", "2 dot 3"),
        (r"\tan(x)", "tangent of x"),
        (r"3\frac{1}{2}", "3 and 1 over 2"),
        (r"\sinh x", "hyperbolic sine x"),
        (r"\sim", "is similar to"),
        (r"\sin^{-1}(x)", "arc sine(x)"),
        (r"\sqrt[n]{x}", "nth root of x"),
        (r"\text{sgn}(x)", "sign(x)"),
        (r"A^T", "A transpose"),
        (r"\tilde{x}", "x tilde"),
        (r"5\text{ m/s}", "5 meters per second"),
        (r"25\%", "25 percent"),
        (r"\$100", "100 dollars"),
        (r"1, 2, \ldots", "1, 2, dot dot dot"),
    ]
    
    for latex, expected in test_cases:
        result = latex
        for pattern, replacement in MISSING_PATTERNS:
            if callable(replacement):
                result = re.sub(pattern, replacement, result)
            else:
                result = re.sub(pattern, replacement, result)
        
        print(f"Input:    {latex}")
        print(f"Expected: {expected}")
        print(f"Got:      {result}")
        print(f"Match:    {'✓' if expected.lower() in result.lower() else '✗'}")
        print()

if __name__ == "__main__":
    test_patterns()
    
    print("\nTo integrate these patterns, add them to the appropriate handlers in patterns_v2.py")