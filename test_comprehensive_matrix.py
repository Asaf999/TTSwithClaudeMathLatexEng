#!/usr/bin/env python3
"""Comprehensive matrix pattern testing"""

import sys
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import process_math_to_speech, AudienceLevel

# Test cases from the hard patterns and devil patterns
test_cases = [
    # Basic matrices
    (r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}', 'matrix a b c d'),
    (r'\begin{pmatrix} a & b \\\\ c & d \end{pmatrix}', 'matrix a b c d'),
    (r'\begin{bmatrix} a & b \\\\ c & d \end{bmatrix}', 'matrix a b c d'),
    (r'\begin{vmatrix} a & b \\\\ c & d \end{vmatrix}', 'matrix a b c d'),
    
    # 3x3 matrices
    (r'\begin{pmatrix} 1 & 2 & 3 \\\\ 4 & 5 & 6 \\\\ 7 & 8 & 9 \end{pmatrix}', 
     'matrix 1 2 3 4 5 6 7 8 9'),
    
    # Column vectors
    (r'\begin{pmatrix} x \\\\ y \\\\ z \end{pmatrix}', 'matrix x y z'),
    (r'\begin{Bmatrix} x \\\\ y \\\\ z \end{Bmatrix}', 'matrix x y z'),
    
    # Determinants
    (r'\det\begin{pmatrix} a & b \\\\ c & d \end{pmatrix}', 
     'determinant of matrix a b c d'),
    (r'\det \begin{pmatrix} a & b \\\\ c & d \end{pmatrix}', 
     'determinant of matrix a b c d'),
    
    # Matrix operations
    (r'\begin{pmatrix} a & b \\\\ c & d \end{pmatrix}^{-1}', 
     'matrix a b c d to the negative 1'),
    (r'\begin{pmatrix} a & b \\\\ c & d \end{pmatrix}^T', 
     'matrix a b c d ^T'),
    
    # Nested matrices (from devil patterns)
    (r'\begin{pmatrix} \begin{pmatrix} a & b \\\\ c & d \end{pmatrix} & \begin{pmatrix} e & f \\\\ g & h \end{pmatrix} \end{pmatrix}', 
     'matrix matrix a b c d matrix e f g h'),
     
    # Matrix with expressions
    (r'\begin{pmatrix} \sin\theta & \cos\theta \\\\ -\cos\theta & \sin\theta \end{pmatrix}',
     'matrix sin theta cos theta negative cos theta sin theta'),
]

print("Comprehensive Matrix Pattern Testing")
print("=" * 60)

passed = 0
total = len(test_cases)

for i, (latex, expected) in enumerate(test_cases):
    try:
        result = process_math_to_speech(latex, AudienceLevel.UNDERGRADUATE)
        
        # Normalize for comparison
        result_normalized = result.strip().lower().replace('  ', ' ')
        expected_normalized = expected.strip().lower()
        
        # Check for exact match or close match
        if result_normalized == expected_normalized:
            success = True
        else:
            # Check if key parts match
            expected_parts = expected_normalized.split()
            result_parts = result_normalized.split()
            matching_parts = sum(1 for part in expected_parts if part in result_parts)
            success = matching_parts >= len(expected_parts) * 0.8
        
        if success:
            print(f"✅ Test {i+1}: PASS")
            print(f"   Input:  {latex[:50]}...")
            print(f"   Result: {result}")
            passed += 1
        else:
            print(f"❌ Test {i+1}: FAIL")
            print(f"   Input:    {latex}")
            print(f"   Expected: {expected}")
            print(f"   Got:      {result}")
    except Exception as e:
        print(f"❌ Test {i+1} ERROR: {e}")
        print(f"   Input: {latex}")

print("\n" + "=" * 60)
print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")

# Debug the determinant issue specifically
print("\n" + "=" * 60)
print("Debugging determinant issue:")
test_det = r'\det\begin{pmatrix} a & b \\\\ c & d \end{pmatrix}'
print(f"Input: {test_det}")
print(f"Output: {repr(process_math_to_speech(test_det, AudienceLevel.UNDERGRADUATE))}")