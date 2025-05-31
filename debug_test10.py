#!/usr/bin/env python3
"""Debug test 10 specifically"""

import sys
import re
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import process_math_to_speech, AudienceLevel

# Test 10 latex
latex = r"\\begin{pmatrix} \\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix} & \\begin{pmatrix} e & f \\\\ g & h \\end{pmatrix} \\end{pmatrix}"
expected = "matrix matrix a b c d matrix e f g h"

print("Testing nested matrix (test 10)")
print(f"LaTeX: {latex}")
print(f"Expected: {expected}")

# Process it
result = process_math_to_speech(latex, AudienceLevel.UNDERGRADUATE)
print(f"Got: '{result}'")

# Show the exact issue
print("\nShowing character by character:")
print("Position: ", end="")
for i in range(max(len(expected), len(result))):
    print(f"{i%10}", end="")
print()

print("Expected: ", end="")
for c in expected:
    if c == ' ':
        print('_', end="")
    else:
        print(c, end="")
print()

print("Got:      ", end="")
for c in result:
    if c == ' ':
        print('_', end="")
    else:
        print(c, end="")
print()

# Debug the post-processing steps
print("\n\nLet's trace through post-processing manually:")

# Simulate what happens
test_text = "matrix  a b c d matrix e f g h"
print(f"Input: '{test_text}'")

# Apply the fix from line 2820
fixed = re.sub(r'matrix\s{2,}', 'matrix matrix ', test_text)
print(f"After matrix\\s{{2,}} fix: '{fixed}'")

# Apply the alternative fix
fixed2 = re.sub(r'matrix\s+([a-z])\s+([a-z])\s+([a-z])\s+([a-z])\s+matrix', r'matrix matrix \1 \2 \3 \4 matrix', test_text)
print(f"After alternative fix: '{fixed2}'")