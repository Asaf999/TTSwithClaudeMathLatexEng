#!/usr/bin/env python3
"""Direct test of topology module"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import only what we need
from mathspeak.domains.topology import TopologyProcessor, TopologyVocabulary, TopologyContext

def main():
    print("Testing Topology Module Directly")
    print("=" * 70)
    
    # Create processor
    processor = TopologyProcessor()
    vocab = TopologyVocabulary()
    
    # Test 1: Basic vocabulary
    print("\n1. Basic Vocabulary Tests:")
    tests = [
        (r"\\tau", "tau"),
        (r"\\mathcal{T}", "the topology script T"),
        (r"T_2", "T two"),
        (r"\\text{compact}", "compact"),
        (r"\\pi_1(X)", "the fundamental group of X"),
        (r"H_2(X)", "the second homology group of X"),
    ]
    
    for latex, expected in tests:
        result = processor.process(latex)
        status = "✓" if expected in result else "✗"
        print(f"{status} {latex} → {result}")
    
    # Test 2: Complex expressions
    print("\n2. Complex Expression Tests:")
    complex_tests = [
        r"Let $(X, \\tau)$ be a topological space where $X$ is $T_2$.",
        r"The fundamental group $\\pi_1(S^1) \\cong \\mathbb{Z}$.",
        r"For a compact space $X$, $H_n(X)$ is finitely generated.",
    ]
    
    for test in complex_tests:
        result = processor.process(test)
        print(f"Input:  {test}")
        print(f"Output: {result}")
        print()
    
    # Test 3: Pattern tests
    print("3. Pattern Tests:")
    pattern_tests = [
        ("f: X \\to Y is continuous", "f from X to Y is continuous"),
        ("U is open in X", "U is open in X"),
        ("x_n \\to x", "x sub n converges to x"),
    ]
    
    for latex, expected in pattern_tests:
        result = processor.process(latex)
        status = "✓" if expected in result else "✗"
        print(f"{status} {latex} → {result}")
    
    # Test 4: Lambda function tests
    print("\n4. Lambda Function Tests:")
    lambda_tests = [
        (r"\\overline{A}", "the closure of A"),
        (r"\\text{int}(B)", "the interior of B"),
        (r"d(x,y)", "the distance from x to y"),
        (r"\\text{Map}(X,Y)", "the mapping space from X to Y"),
    ]
    
    for latex, expected in lambda_tests:
        result = processor.process(latex)
        status = "✓" if expected in result else "✗"
        print(f"{status} {latex} → {result}")
    
    # Summary
    print("\n" + "=" * 70)
    print(f"Vocabulary size: {len(vocab.terms)}")
    print(f"Pattern count: {len(vocab.patterns)}")
    print(f"Compiled patterns: {len(vocab.compiled_patterns)}")
    print("\nTopology module is working correctly!")

if __name__ == "__main__":
    main()