#!/usr/bin/env python3
"""Test script to verify integral processing fix"""

import sys
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng')

from mathspeak import MathSpeak
from mathspeak.core.patterns import PatternProcessor

def test_pattern_processor():
    """Test the pattern processor directly"""
    print("Testing Pattern Processor")
    print("=" * 60)
    
    processor = PatternProcessor()
    
    test_cases = [
        # The problematic case
        "int_0^ infty e^-x^2 dx equals frac sqrt pi2",
        # With backslashes
        "\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}",
        # Other integral forms
        "\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}",
        "int_a^b f(x) dx",
    ]
    
    for test in test_cases:
        print(f"\nInput:  {test}")
        result = processor.process(test)
        print(f"Output: {result}")

def test_mathspeak():
    """Test the full MathSpeak system"""
    print("\n\nTesting MathSpeak System")
    print("=" * 60)
    
    ms = MathSpeak()
    
    test_expressions = [
        # The problematic case
        "int_0^ infty e^-x^2 dx equals frac sqrt pi2",
        # Properly formatted version
        "\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}",
        # Mixed formatting
        "int_0^infty e^{-x^2} dx = \\frac{\\sqrt{pi}}{2}",
    ]
    
    for expr in test_expressions:
        print(f"\nInput:  {expr}")
        result = ms.to_text(expr)
        print(f"Output: {result}")

if __name__ == "__main__":
    test_pattern_processor()
    test_mathspeak()