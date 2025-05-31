#!/usr/bin/env python3
"""
Debug pattern processing step by step
"""

import sys
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import process_math_to_speech, AudienceLevel

def debug_step_by_step(text):
    """Debug what happens to text step by step"""
    
    print(f"Original: {text}")
    
    # Test just the derivative
    if "frac{d}" in text:
        print("This contains derivative pattern")
    
    # Test just the integral
    if "int_0^1" in text:
        print("This contains integral_0^1 pattern")
    
    result = process_math_to_speech(text, AudienceLevel.UNDERGRADUATE)
    print(f"Final result: {result}")

if __name__ == "__main__":
    print("=== Debugging Pattern Processing ===")
    
    test_cases = [
        "\\frac{d}{dx} f(x)",
        "\\int_0^1 x dx",
    ]
    
    for test in test_cases:
        print("\n" + "="*40)
        debug_step_by_step(test)
        print("="*40)