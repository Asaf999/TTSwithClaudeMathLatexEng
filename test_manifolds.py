#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test for manifolds processor
"""

# Add the parent directory to path
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mathspeak.domains.manifolds import ManifoldsProcessor

def test_simple():
    processor = ManifoldsProcessor()
    
    # Test simple cases
    test_cases = [
        "Let M be a manifold",
        "The tangent space T_p M",
        "A smooth map f: M to N",
        "The vector field X",
        "The differential form omega",
    ]
    
    print("Simple Manifolds Test")
    print("=" * 50)
    
    for test in test_cases:
        print(f"\nInput:  {test}")
        result = processor.process(test)
        print(f"Output: {result}")

if __name__ == "__main__":
    test_simple()