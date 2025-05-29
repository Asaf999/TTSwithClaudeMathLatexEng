#!/usr/bin/env python3
"""Debug numerical analysis patterns"""

from domains.numerical_analysis import NumericalAnalysisProcessor

proc = NumericalAnalysisProcessor()

# Check what patterns are being compiled
print("Checking compiled patterns for 'norm of the error':")
for i, (pattern, replacement) in enumerate(proc.vocabulary.compiled_patterns):
    if "norm of the error" in str(replacement):
        print(f"\nPattern {i}:")
        print(f"  Pattern: {pattern.pattern}")
        print(f"  Replacement: {replacement}")
        
        # Test the pattern
        test_str = "This is a test |e| string"
        matches = pattern.findall(test_str)
        if matches:
            print(f"  Matches in '{test_str}': {matches}")

# Test simple case
print("\n\nTesting simple norm pattern:")
test = r"\\|e\\|"
result = proc.process(test)
print(f"Input: {repr(test)}")
print(f"Output: {result}")

# Check if the pattern is being applied correctly
import re
pattern = r'\\\\|e\\\\|'
compiled = re.compile(pattern)
print(f"\nDirect pattern test:")
print(f"Pattern: {repr(pattern)}")
print(f"Matches in {repr(test)}: {compiled.findall(test)}")

# Check what the escape function does
print("\n\nChecking escape function:")
original = r'\\|e\\|'
escaped = proc.vocabulary._escape_for_both_backslashes(original)
print(f"Original: {repr(original)}")
print(f"Escaped: {repr(escaped)}")