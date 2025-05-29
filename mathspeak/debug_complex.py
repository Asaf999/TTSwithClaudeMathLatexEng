#!/usr/bin/env python3
"""Debug script for complex analysis processor"""

from domains.complex_analysis import ComplexAnalysisProcessor

processor = ComplexAnalysisProcessor()

# Test cases from the failing tests
test_cases = [
    r"\\mathbb{C}",
    r"\mathbb{C}",
    "\\mathbb{C}",
    "\mathbb{C}",
]

print("Testing different backslash variations:")
for test in test_cases:
    result = processor.process(test)
    print(f"Input: {repr(test)}")
    print(f"Output: {result}")
    print(f"Expected: the complex numbers")
    print()

# Check vocabulary
print("\nChecking vocabulary patterns:")
vocab = processor.vocabulary
for pattern, replacement in list(vocab.terms.items())[:5]:
    print(f"Pattern: {repr(pattern)}")
    print(f"Replacement: {replacement}")
    print()

# Check compiled patterns
print("\nChecking compiled patterns:")
for i, (pattern, replacement) in enumerate(vocab.compiled_patterns[:5]):
    print(f"Pattern {i}: {pattern.pattern}")
    print(f"Replacement: {replacement}")
    print()