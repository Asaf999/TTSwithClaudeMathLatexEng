#!/usr/bin/env python3
"""Test the matrix extraction fix"""

import sys
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import process_math_to_speech, AudienceLevel

# Test cases
test_cases = [
    # Simple 2x2 matrix
    (r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}', 'matrix a b c d'),
    
    # 2x2 with double backslash
    (r'\begin{pmatrix} a & b \\\\ c & d \end{pmatrix}', 'matrix a b c d'),
    
    # bmatrix
    (r'\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix}', 'matrix 1 2 3 4'),
    
    # vmatrix
    (r'\begin{vmatrix} x & y \\ z & w \end{vmatrix}', 'matrix x y z w'),
    
    # 3x3 matrix
    (r'\begin{pmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{pmatrix}', 'matrix 1 2 3 4 5 6 7 8 9'),
    
    # Matrix with determinant
    (r'\det\begin{pmatrix} a & b \\ c & d \end{pmatrix}', 'determinant of matrix a b c d'),
    
    # Column vector
    (r'\begin{pmatrix} x \\ y \\ z \end{pmatrix}', 'matrix x y z'),
    
    # Row vector
    (r'\begin{pmatrix} a & b & c \end{pmatrix}', 'matrix a b c'),
]

print("Testing Matrix Extraction Fix")
print("=" * 50)

passed = 0
total = len(test_cases)

for i, (latex, expected) in enumerate(test_cases):
    try:
        result = process_math_to_speech(latex, AudienceLevel.UNDERGRADUATE)
        success = result.strip().lower() == expected.strip().lower()
        
        if success:
            print(f"✅ Test {i+1}: {latex[:30]}...")
            print(f"   Result: {result}")
            passed += 1
        else:
            print(f"❌ Test {i+1}: {latex}")
            print(f"   Expected: {expected}")
            print(f"   Got:      {result}")
    except Exception as e:
        print(f"❌ Test {i+1} ERROR: {e}")

print("\n" + "=" * 50)
print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")