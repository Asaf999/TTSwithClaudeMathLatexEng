#!/usr/bin/env python3
"""
Demonstration of Professor-Style Mathematical Speech
===================================================

Shows how the updated MathSpeak system speaks exactly like a math professor.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mathspeak.core.patterns import PatternProcessor

def demonstrate_professor_speech():
    """Demonstrate professor-style mathematical speech"""
    
    processor = PatternProcessor()
    
    # Examples of professor-style speech
    examples = [
        # Basic calculus
        ("Integral", r"\int_0^1 x^2 dx", 
         "A professor would say: 'the integral from 0 to 1 of x squared d x'"),
        
        ("Limit", r"\lim_{x \to 0} \frac{\sin x}{x} = 1",
         "A professor would say: 'the limit as x approaches 0 of sine x over x equals 1'"),
        
        ("Sum", r"\sum_{i=1}^n i = \frac{n(n+1)}{2}",
         "A professor would say: 'the sum from i equals 1 to n of i equals n times n plus 1 over 2'"),
        
        # Logic and sets
        ("Universal quantifier", r"\forall x \in \mathbb{R}, x^2 \geq 0",
         "A professor would say: 'for all x in R, x squared is greater than or equal to 0'"),
        
        ("Existence", r"\exists y \in \mathbb{N} : y > x",
         "A professor would say: 'there exists a y in N such that y is greater than x'"),
        
        ("Function mapping", r"f: \mathbb{R} \to \mathbb{R}",
         "A professor would say: 'f maps R to R'"),
        
        # Derivatives
        ("First derivative", r"f'(x) = 2x",
         "A professor would say: 'f prime of x equals 2 x'"),
        
        ("Partial derivative", r"\frac{\partial f}{\partial x}",
         "A professor would say: 'partial f partial x'"),
        
        # Common expressions
        ("Exponential", r"e^{-x^2}",
         "A professor would say: 'e to the minus x squared'"),
        
        ("Trig function", r"\sin^2 x + \cos^2 x = 1",
         "A professor would say: 'sine squared x plus cosine squared x equals 1'"),
        
        ("Binomial coefficient", r"\binom{n}{k} = \frac{n!}{k!(n-k)!}",
         "A professor would say: 'n choose k equals n factorial over k factorial times n minus k factorial'"),
        
        # Matrix notation
        ("Matrix element", r"A_{ij}",
         "A professor would say: 'A i j' (not 'A sub i j')"),
        
        # Subscripts
        ("Subscript zero", r"x_0",
         "A professor would say: 'x naught' or 'x 0'"),
        
        ("Pi subscript", r"\pi_1(S^1) = \mathbb{Z}",
         "A professor would say: 'pi 1 of S 1 equals Z'"),
        
        # Complex expressions
        ("Gaussian integral", r"\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}",
         "A professor would say: 'the integral from negative infinity to infinity of e to the minus x squared d x equals square root of pi'"),
    ]
    
    print("Professor-Style Mathematical Speech Demonstration")
    print("=" * 80)
    print()
    print("The updated MathSpeak system now speaks exactly like a math professor would")
    print("in a classroom setting. Here are some examples:")
    print()
    
    for title, latex, expected in examples:
        print(f"{title}:")
        print(f"  LaTeX:     {latex}")
        
        # Process with our pattern processor
        processed = processor.process(latex)
        # Clean up any remaining backslashes
        processed = processed.replace('\\', ' ').replace('  ', ' ').strip()
        
        print(f"  Processed: {processed}")
        print(f"  {expected}")
        print()
    
    print("\nKey Professor-Style Speech Patterns:")
    print("=" * 80)
    print("1. Integrals: 'the integral from 0 to 1 of x squared d x'")
    print("2. Limits: 'the limit as x approaches 0'")
    print("3. Sums: 'the sum from i equals 1 to n'")
    print("4. Logic: 'for all x in R' (not 'for all x in the real numbers')")
    print("5. Sets: Just say 'R', 'N', 'Z' for \\mathbb{R}, etc.")
    print("6. Functions: 'f maps X to Y' or 'f from X to Y'")
    print("7. Derivatives: 'f prime of x', 'd f d x', 'partial f partial x'")
    print("8. Subscripts: NEVER say 'underscore' - use 'sub' or just indices")
    print("9. Matrix elements: 'A i j' (not 'A sub i j')")
    print("10. Greek letters: Natural pronunciation - 'epsilon' not 'ep-si-lon'")
    print()
    print("The system now produces natural, professor-quality mathematical speech!")

if __name__ == "__main__":
    demonstrate_professor_speech()