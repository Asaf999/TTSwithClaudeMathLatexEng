#!/usr/bin/env python3
"""Debug matrix extraction specifically"""

import sys
import re
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import process_math_to_speech, AudienceLevel, _extract_matrix_content

def test_matrix_extraction(latex):
    """Test matrix extraction function directly"""
    print(f"\nTesting: {latex}")
    
    # Create a match object manually
    class FakeMatch:
        def __init__(self, text):
            self.text = text
            self.lastindex = None
        
        def group(self, n):
            if n == 0:
                return self.text
            return self.text
    
    match = FakeMatch(latex)
    result = _extract_matrix_content(match)
    print(f"Extracted: {result}")
    return result

# Test specific matrix patterns
test_cases = [
    # Simple matrix
    r"\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}",
    
    # Nested matrix (test 10)
    r"\\begin{pmatrix} \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} & \\begin{pmatrix} e & f \\\\ g & h \\end{pmatrix} \\end{pmatrix}",
    
    # Two consecutive matrices (test 23)
    r"\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} \\begin{bmatrix} e & f \\\\ g & h \\end{bmatrix}",
    
    # Matrix with trace (test 24)
    r"\\text{tr}\\left(\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}\\right)",
]

print("=== Testing Matrix Extraction Function ===")
for latex in test_cases:
    test_matrix_extraction(latex)

print("\n=== Testing Full Processing ===")
for i, latex in enumerate(test_cases):
    print(f"\nTest {i+1}: {latex}")
    result = process_math_to_speech(latex, AudienceLevel.UNDERGRADUATE)
    print(f"Result: {result}")

# Test the specific failing patterns
failing_tests = [
    (10, r"\\begin{pmatrix} \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} & \\begin{pmatrix} e & f \\\\ g & h \\end{pmatrix} \\end{pmatrix}",
     "matrix matrix a b c d matrix e f g h"),
    
    (23, r"\\begin{bmatrix} a & b \\\\ c & d \\end{bmatrix} \\begin{bmatrix} e & f \\\\ g & h \\end{bmatrix}",
     "matrix a b c d matrix e f g h"),
    
    (24, r"\\text{tr}\\left(\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}\\right)",
     "trace of matrix a b c d"),
]

print("\n=== Testing Specific Failing Patterns ===")
for num, latex, expected in failing_tests:
    print(f"\nDevil Test {num}:")
    print(f"LaTeX: {latex}")
    print(f"Expected: {expected}")
    result = process_math_to_speech(latex, AudienceLevel.UNDERGRADUATE)
    print(f"Got: {result}")
    print(f"Match: {result.strip() == expected.strip()}")
    
    # Character-by-character comparison if not matching
    if result.strip() != expected.strip():
        print("\nCharacter differences:")
        for i, (e, g) in enumerate(zip(expected, result)):
            if e != g:
                print(f"  Position {i}: expected '{e}', got '{g}'")