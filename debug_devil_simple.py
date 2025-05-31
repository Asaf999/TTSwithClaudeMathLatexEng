#!/usr/bin/env python3
"""Debug specific failing devil tests - simple version"""

import sys
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import process_math_to_speech, AudienceLevel
from core.engine import MathematicalTTSEngine

def debug_test(test_num, latex, expected):
    """Debug a single test case"""
    print(f"\n{'='*60}")
    print(f"DEBUGGING DEVIL TEST {test_num}")
    print(f"{'='*60}")
    print(f"LaTeX input: {latex}")
    print(f"Expected output: {expected}")
    
    try:
        # Test with patterns_v2
        print(f"\n--- Testing with patterns_v2 ---")
        result = process_math_to_speech(latex, AudienceLevel.UNDERGRADUATE)
        print(f"Got: {result}")
        print(f"Match: {result.strip().lower() == expected.strip().lower()}")
        
        # Test with engine
        print(f"\n--- Testing with MathematicalTTSEngine ---")
        engine = MathematicalTTSEngine()
        engine_result = engine.process_latex(latex)
        if hasattr(engine_result, 'processed'):
            engine_text = engine_result.processed
        else:
            engine_text = str(engine_result)
        print(f"Got: {engine_text}")
        print(f"Match: {engine_text.strip().lower() == expected.strip().lower()}")
        
        # Compare character by character if not matching
        if result.strip().lower() != expected.strip().lower():
            print(f"\n--- Character comparison ---")
            print(f"Expected: '{expected}'")
            print(f"Got:      '{result}'")
            print(f"\nDifferences:")
            for i, (e, g) in enumerate(zip(expected, result)):
                if e != g:
                    print(f"  Position {i}: expected '{e}', got '{g}'")
            
            # Check length differences
            if len(expected) != len(result):
                print(f"\nLength difference: expected {len(expected)}, got {len(result)}")
                if len(result) > len(expected):
                    print(f"Extra characters: '{result[len(expected):]}'")
                else:
                    print(f"Missing characters: '{expected[len(result):]}'")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

# Test cases
test_cases = [
    (10, r"\\begin{pmatrix} \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} & \\begin{pmatrix} e & f \\\\ g & h \\end{pmatrix} \\end{pmatrix}",
     "matrix matrix a b c d matrix e f g h"),
    
    (14, r"\\sum_{\\substack{i=1\\\\j=1}}^{\\substack{n\\\\m}} a_{i,j}",
     "sum from i equals 1 j equals 1 to n m a i j"),
    
    (23, r"\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} \\begin{bmatrix} e & f \\\\ g & h \\end{bmatrix}",
     "matrix a b c d matrix e f g h"),
    
    (24, r"\\text{tr}\\left(\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}\\right)",
     "trace of matrix a b c d"),
    
    (107, r"\\frac{d}{dt} \\mathbb{E}[X(t)] = \\mathbb{E}\\left[\\frac{dX(t)}{dt}\\right]",
     "derivative with respect to t expected value of X of t equals expected value of derivative of X of t with respect to t")
]

if __name__ == "__main__":
    # Test specific case if provided
    if len(sys.argv) > 1:
        test_num = int(sys.argv[1])
        for num, latex, expected in test_cases:
            if num == test_num:
                debug_test(num, latex, expected)
                break
    else:
        # Test all cases
        for num, latex, expected in test_cases:
            debug_test(num, latex, expected)