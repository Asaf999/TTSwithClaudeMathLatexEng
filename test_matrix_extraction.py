#!/usr/bin/env python3
"""Test the matrix extraction function directly"""

import sys
import re
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import _extract_matrix_content

# Test the extraction function directly
test_cases = [
    r'\begin{pmatrix} a & b \\ c & d \end{pmatrix}',
    r'\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \end{bmatrix}',
    r'\begin{vmatrix} x \\ y \\ z \end{vmatrix}',
]

print("Testing _extract_matrix_content directly:")
print("=" * 50)

for test in test_cases:
    # Create a match object
    pattern = r'(\\begin\{[a-z]*matrix\}.*?\\end\{[a-z]*matrix\})'
    match = re.search(pattern, test)
    if match:
        result = _extract_matrix_content(match)
        print(f"Input: {test}")
        print(f"Result: {result}")
        print()
    else:
        print(f"No match for: {test}")
        print()