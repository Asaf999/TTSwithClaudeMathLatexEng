#!/usr/bin/env python3
"""
Test script to verify the mathematical speech improvements
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

def test_improvements():
    """Test the improvements to mathematical speech"""
    
    # Initialize engine
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=False
    )
    
    # Test cases for improved speech
    test_cases = [
        # Subscripts
        ("$a_{ij}$", "Should be: 'a sub i j' or 'a i j'"),
        ("$x_1$", "Should be: 'x sub 1' or 'x one'"),
        ("$\\pi_1$", "Should be: 'pi sub 1' or 'pi one'"),
        ("$A_{ij}$", "Should be: 'A i j' or 'the i j-th element of A'"),
        ("$x_n$", "Should be: 'x sub n'"),
        
        # Superscripts
        ("$x^2$", "Should be: 'x squared'"),
        ("$y^3$", "Should be: 'y cubed'"),
        ("$z^n$", "Should be: 'z to the n'"),
        ("$a^{10}$", "Should be: 'a to the power of 10'"),
        
        # Fractions
        ("$\\frac{1}{2}$", "Should be: 'one half'"),
        ("$\\frac{3}{4}$", "Should be: 'three fourths'"),
        ("$\\frac{\\pi}{2}$", "Should be: 'pi over 2'"),
        ("$\\frac{a}{b}$", "Should be: 'a over b'"),
        
        # Differentials
        ("$\\int f(x) dx$", "Should have: 'd x' not 'dx'"),
        ("$\\frac{dy}{dx}$", "Should be: 'd y over d x'"),
        
        # Complex expressions
        ("$\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}$", 
         "Should be natural: integral from zero to infinity..."),
        ("$\\sum_{i=1}^n a_i$", "Should be: sum from i equals 1 to n of a sub i"),
        
        # Matrix elements
        ("$M_{ij} = a_{ij} + b_{ij}$", "Should be: M i j equals a i j plus b i j"),
    ]
    
    print("Testing Mathematical Speech Improvements")
    print("=" * 60)
    
    for i, (expression, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: {expression}")
        print(f"Expected: {expected}")
        
        # Process the expression
        result = engine.process_latex(expression)
        
        print(f"Result: {result.processed}")
        print("-" * 40)
    
    # Test that underscore is no longer in output
    underscore_test = "$x_1 + y_2 = z_3$"
    result = engine.process_latex(underscore_test)
    if "underscore" in result.processed.lower():
        print("\n❌ ERROR: 'underscore' still appears in output!")
        print(f"Expression: {underscore_test}")
        print(f"Result: {result.processed}")
    else:
        print("\n✅ SUCCESS: No 'underscore' in output")
    
    print("\nTest complete!")
    engine.shutdown()

if __name__ == "__main__":
    test_improvements()