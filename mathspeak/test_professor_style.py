#!/usr/bin/env python3
"""
Test Script for Professor-Style Mathematical Speech
===================================================

Tests the MathSpeak system to ensure it speaks exactly like a math professor
would in a classroom setting.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.engine import MathematicalTTSEngine
from core.patterns import PatternProcessor

def test_professor_style():
    """Test various mathematical expressions for professor-style speech"""
    
    # Initialize the engine
    engine = MathematicalTTSEngine(enable_caching=False)
    
    # Test cases from the requirements
    test_cases = [
        # Integrals
        (r"$\int_0^1 x^2 dx$", "Should say: 'the integral from 0 to 1 of x squared d x'"),
        (r"$\int_0^\infty e^{-x^2} dx$", "Should say: 'the integral from 0 to infinity of e to the minus x squared d x'"),
        
        # Sums and limits
        (r"$\sum_{i=1}^n i^2$", "Should say: 'the sum from i equals 1 to n of i squared'"),
        (r"$\lim_{x \to 0} \frac{\sin x}{x}$", "Should say: 'the limit as x approaches 0 of sine x over x'"),
        (r"$\lim_{n \to \infty} (1 + \frac{1}{n})^n$", "Should say: 'the limit as n goes to infinity of (1 plus 1 over n) to the n'"),
        
        # Logic and sets
        (r"$\forall x \in \mathbb{R}$", "Should say: 'for all x in R'"),
        (r"$\exists y \in \mathbb{N}$", "Should say: 'there exists a y in N'"),
        (r"$f: X \to Y$", "Should say: 'f maps X to Y'"),
        (r"$x \in A$", "Should say: 'x is in A' or 'x belongs to A'"),
        (r"$A \subset B$", "Should say: 'A subset B' or 'A is a subset of B'"),
        (r"$\therefore x = 2$", "Should say: 'therefore x equals 2'"),
        (r"$p \implies q$", "Should say: 'p implies q'"),
        
        # Derivatives and differentials
        (r"$f'(x)$", "Should say: 'f prime of x'"),
        (r"$f''(x)$", "Should say: 'f double prime of x'"),
        (r"$\frac{df}{dx}$", "Should say: 'd f d x'"),
        (r"$\frac{\partial f}{\partial x}$", "Should say: 'partial f partial x'"),
        
        # Common expressions
        (r"$e^x$", "Should say: 'e to the x'"),
        (r"$e^{-x^2}$", "Should say: 'e to the minus x squared'"),
        (r"$\sin^2 x$", "Should say: 'sine squared x'"),
        (r"$\log_2 x$", "Should say: 'log base 2 of x'"),
        (r"$\sqrt[3]{x}$", "Should say: 'the cube root of x'"),
        (r"$n!$", "Should say: 'n factorial'"),
        (r"$\binom{n}{k}$", "Should say: 'n choose k'"),
        
        # Matrix notation
        (r"$A_{ij}$", "Should say: 'A i j' (the i j entry of matrix A)"),
        
        # Greek letters
        (r"$\alpha + \beta$", "Should say: 'alpha plus beta'"),
        (r"$\epsilon > 0$", "Should say: 'epsilon greater than 0'"),
        (r"$\Delta x$", "Should say: 'delta x'"),
        
        # Special values
        (r"$||x||$", "Should say: 'the norm of x'"),
        (r"$|x|$", "Should say: 'the absolute value of x'"),
        (r"$(a,b)$", "Should say: 'the open interval from a to b'"),
        (r"$[a,b]$", "Should say: 'the closed interval from a to b'"),
        (r"$\mathbb{R}^n$", "Should say: 'R n'"),
        (r"$2\pi i$", "Should say: 'two pi i'"),
        
        # Subscripts - NEVER say underscore
        (r"$x_0$", "Should say: 'x naught' or 'x 0'"),
        (r"$x_1, x_2, \ldots, x_n$", "Should say: 'x 1, x 2, ..., x n'"),
        (r"$\pi_1(X)$", "Should say: 'pi 1 of X'"),
        
        # Complex example
        (r"$\int_0^1 x^2 e^{-x} dx = \frac{\sqrt{\pi}}{2}$", 
         "Should say: 'the integral from 0 to 1 of x squared e to the minus x d x equals square root of pi over 2'"),
    ]
    
    print("Testing Professor-Style Mathematical Speech")
    print("=" * 80)
    print()
    
    for i, (latex, expected) in enumerate(test_cases, 1):
        print(f"Test {i}:")
        print(f"LaTeX: {latex}")
        print(f"Expected: {expected}")
        
        # Process the expression
        result = engine.process_latex(latex)
        
        print(f"Actual: {result.processed}")
        print(f"Processing time: {result.processing_time:.3f}s")
        
        if result.unknown_commands:
            print(f"Unknown commands: {result.unknown_commands}")
        
        print("-" * 80)
        print()
    
    # Test pattern processor directly
    print("\nTesting Pattern Processor Directly:")
    print("=" * 80)
    
    processor = PatternProcessor()
    direct_tests = [
        r"\int_0^1 x^2 dx",
        r"\sum_{i=1}^n i^2",
        r"\lim_{x \to 0} \sin x",
        r"f: X \to Y",
        r"\forall x \in \mathbb{R}",
    ]
    
    for test in direct_tests:
        processed = processor.process(test)
        print(f"Input:  {test}")
        print(f"Output: {processed}")
        print()
    
    # Summary
    print("\nProfessor-Style Speech Guidelines:")
    print("=" * 80)
    print("1. Never say 'underscore' - use 'sub' or just read indices")
    print("2. Say 'e to the x' not 'e caret x'")
    print("3. Say 'd f d x' quickly for derivatives")
    print("4. Say 'R' not 'the real numbers' for \\mathbb{R}")
    print("5. Say 'pi 1' not 'pi sub 1' for fundamental groups")
    print("6. Group terms naturally: '2 pi i' not '2 times pi times i'")
    print("7. Use natural mathematical language: 'maps to', 'belongs to', etc.")

if __name__ == "__main__":
    test_professor_style()