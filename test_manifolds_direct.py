#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct test for manifolds processor patterns
"""

import re

# Test the problematic patterns
patterns = [
    (r'\|X\|', 'the norm of X'),
    (r'T\^\{1,0\}M', 'the 1 0 tangent bundle'),
    (r'\\\[([X-Z]),\s*([X-Z])\\\]\s*=\s*0', 'bracket equals zero'),
]

test_strings = [
    "|X|",
    "T^{1,0}M",
    "[X,Y] = 0",
]

print("Testing individual patterns:")
print("=" * 50)

for pattern, replacement in patterns:
    print(f"\nPattern: {pattern}")
    print(f"Replacement: {replacement}")
    try:
        compiled = re.compile(pattern)
        print("✓ Pattern compiled successfully")
    except re.error as e:
        print(f"✗ Error: {e}")

print("\n\nTesting basic replacements:")
print("=" * 50)

# Test basic vocabulary replacements
basic_vocab = {
    'M': 'M',
    'N': 'N',
    'TM': 'the tangent bundle of M',
}

test_text = "Let M be a manifold with tangent bundle TM"
print(f"\nOriginal: {test_text}")

for pattern, replacement in basic_vocab.items():
    # Use word boundaries to avoid partial matches
    test_text = re.sub(r'\b' + re.escape(pattern) + r'\b', replacement, test_text)

print(f"Processed: {test_text}")