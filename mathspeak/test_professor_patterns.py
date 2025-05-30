#!/usr/bin/env python3
"""
Direct test of professor-style patterns without full engine
"""

import re
from collections import OrderedDict

def test_patterns_directly():
    """Test mathematical patterns directly without the full engine"""
    
    # Professor-style replacements based on our updates
    replacements = OrderedDict([
        # Subscripts - NEVER say underscore
        (r'x_0', 'x naught'),
        (r'x_([0-9]+)', lambda m: f'x {m.group(1)}'),
        (r'([a-zA-Z])_([0-9]+)', lambda m: f'{m.group(1)} {m.group(1) if m.group(1).isupper() else "sub"} {m.group(2)}'),
        (r'\\pi_1', 'pi 1'),
        (r'\\pi_([0-9]+)', lambda m: f'pi {m.group(1)}'),
        (r'A_{ij}', 'A i j'),
        
        # Integrals - professor style
        (r'\\int_0\^1\s*x\^2\s*dx', 'the integral from 0 to 1 of x squared d x'),
        (r'\\int_([^\\s]+)\^([^\\s]+)', lambda m: f'the integral from {m.group(1)} to {m.group(2)}'),
        
        # Limits
        (r'\\lim_{x \\to 0}', 'the limit as x approaches 0'),
        (r'\\lim_{n \\to \\infty}', 'the limit as n goes to infinity'),
        
        # Sums
        (r'\\sum_{i=1}\^n', 'the sum from i equals 1 to n'),
        
        # Greek letters - natural
        (r'\\alpha', 'alpha'),
        (r'\\beta', 'beta'),
        (r'\\epsilon', 'epsilon'),
        (r'\\Delta', 'delta'),
        
        # Sets - professor style
        (r'\\mathbb\{R\}', 'R'),
        (r'\\mathbb\{N\}', 'N'),
        (r'\\mathbb\{R\}\^n', 'R n'),
        
        # Logic
        (r'\\forall', 'for all'),
        (r'\\exists', 'there exists'),
        (r'\\in', ' in '),
        (r'\\subset', ' subset '),
        
        # Functions
        (r'f\'\\(x\\)', 'f prime of x'),
        (r'f\'\'\\(x\\)', 'f double prime of x'),
        (r'\\frac\{df\}\{dx\}', 'd f d x'),
        (r'\\frac\{\\partial f\}\{\\partial x\}', 'partial f partial x'),
        
        # Common expressions
        (r'e\^x', 'e to the x'),
        (r'e\^\{-x\^2\}', 'e to the minus x squared'),
        (r'\\sin\^2 x', 'sine squared x'),
        (r'\\log_2 x', 'log base 2 of x'),
        (r'\\sqrt\[3\]\{x\}', 'the cube root of x'),
        (r'n!', 'n factorial'),
        (r'\\binom\{n\}\{k\}', 'n choose k'),
        
        # Mathematical phrasing
        (r'f\s*:\s*X\s*\\to\s*Y', 'f maps X to Y'),
        (r'x \\in A', 'x is in A'),
        (r'A \\subset B', 'A subset B'),
        (r'\\therefore', 'therefore'),
        (r'\\implies', 'implies'),
        (r'\|\|x\|\|', 'the norm of x'),
        (r'\|x\|', 'the absolute value of x'),
        (r'2\\pi i', 'two pi i'),
        
        # Remove LaTeX artifacts
        (r'\$', ''),
        (r'\\', ' '),
        (r'\{', ''),
        (r'\}', ''),
    ])
    
    # Test cases
    test_cases = [
        r"$\int_0^1 x^2 dx$",
        r"$\sum_{i=1}^n i^2$",
        r"$\lim_{x \to 0} \frac{\sin x}{x}$",
        r"$\forall x \in \mathbb{R}$",
        r"$\exists y \in \mathbb{N}$",
        r"$f: X \to Y$",
        r"$f'(x)$",
        r"$f''(x)$",
        r"$\frac{df}{dx}$",
        r"$e^x$",
        r"$e^{-x^2}$",
        r"$\sin^2 x$",
        r"$n!$",
        r"$\binom{n}{k}$",
        r"$A_{ij}$",
        r"$x_0$",
        r"$\pi_1(X)$",
        r"$||x||$",
        r"$|x|$",
        r"$\mathbb{R}^n$",
        r"$2\pi i$",
    ]
    
    print("Testing Professor-Style Pattern Replacements")
    print("=" * 80)
    print()
    
    for test in test_cases:
        result = test
        
        # Apply replacements
        for pattern, replacement in replacements.items():
            if callable(replacement):
                result = re.sub(pattern, replacement, result)
            else:
                result = re.sub(pattern, replacement, result)
        
        # Clean up
        result = ' '.join(result.split())
        
        print(f"Input:  {test}")
        print(f"Output: {result}")
        print()
    
    # Test specific professor-style phrases
    print("\nProfessor-Style Phrases:")
    print("=" * 80)
    
    phrases = [
        ("$x_0, x_1, x_2, \\ldots, x_n$", "x naught, x 1, x 2, ..., x n"),
        ("$\\int_0^\\infty e^{-x^2} dx$", "the integral from 0 to infinity of e to the minus x squared d x"),
        ("$\\lim_{x \\to 0} f(x)$", "the limit as x approaches 0 of f of x"),
        ("$\\sum_{i=1}^n a_i$", "the sum from i equals 1 to n of a sub i"),
        ("$f: \\mathbb{R} \\to \\mathbb{R}$", "f maps R to R"),
        ("$\\forall \\epsilon > 0$", "for all epsilon greater than 0"),
        ("$A \\subset B$", "A subset B"),
    ]
    
    for latex, expected in phrases:
        print(f"LaTeX:    {latex}")
        print(f"Expected: {expected}")
        print()

if __name__ == "__main__":
    test_patterns_directly()