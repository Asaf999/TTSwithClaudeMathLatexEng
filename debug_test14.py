#!/usr/bin/env python3
"""Debug test 14 specifically"""

import sys
import re
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

from core.patterns_v2 import process_math_to_speech, AudienceLevel

# Test 14 latex
latex = r"\\sum_{\\substack{i=1\\\\j=1}}^{\\substack{n\\\\m}} a_{i,j}"
expected = "sum from i equals 1 j equals 1 to n m a i j"

print("Testing substack sum (test 14)")
print(f"LaTeX: {latex}")
print(f"Expected: {expected}")

# Process it
result = process_math_to_speech(latex, AudienceLevel.UNDERGRADUATE)
print(f"Got: '{result}'")

# Show where "an" appears
print("\nLooking for 'an' in the result:")
if 'an' in result:
    idx = result.index('an')
    print(f"Found 'an' at position {idx}")
    print(f"Context: '...{result[max(0,idx-5):idx+7]}...'")

# Test the fix directly
test_text = "sum from i equals 1 j equals 1 to n m an i j"
print(f"\nTesting fix on: '{test_text}'")
fixed = re.sub(r'\ban i j', 'a i j', test_text)
print(f"After fix: '{fixed}'")

# Maybe the issue is the "a" is being converted to "an" by article processing?
print("\nTesting article processing:")
test_text2 = "sum from i equals 1 j equals 1 to n m a i j"
# This is the article fix from line 3307
article_fixed = re.sub(r'\ba\s+((?![a-zA-Z]\s+over)(?![a-zA-Z]\s+is)[aeiou])', r'an \1', test_text2, flags=re.IGNORECASE)
print(f"Original: '{test_text2}'")
print(f"After article fix: '{article_fixed}'")