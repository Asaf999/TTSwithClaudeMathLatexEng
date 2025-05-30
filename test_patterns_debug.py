#!/usr/bin/env python3
"""Debug script to test pattern matching issues"""

from mathspeak.core.patterns_v2 import (
    MathSpeechProcessor, GeneralizationEngine, MathDomain, AudienceLevel
)

def test_pattern_matching():
    """Test pattern matching with LaTeX commands"""
    
    processor = MathSpeechProcessor()
    engine = processor.engine
    
    # Test input
    test_input = r'\frac{1}{2}'
    print(f"Original input: {test_input}")
    print(f"Input repr: {repr(test_input)}")
    
    # Test preprocessing
    preprocessed = processor._preprocess(test_input)
    print(f"\nAfter preprocessing: {preprocessed}")
    print(f"Preprocessed repr: {repr(preprocessed)}")
    
    # Get algebra handler
    algebra_handler = engine.handlers[MathDomain.ALGEBRA]
    
    # Check fraction patterns
    print("\n--- Checking Fraction Patterns ---")
    for pattern in algebra_handler.patterns:
        if 'frac' in pattern.pattern.lower():
            print(f"\nPattern: {pattern.description}")
            print(f"Regex: {pattern.pattern}")
            print(f"Compiled pattern: {pattern.compiled.pattern}")
            
            # Test if pattern matches
            match = pattern.compiled.search(preprocessed)
            if match:
                print(f"MATCH FOUND: {match.group()}")
                # Apply replacement
                if callable(pattern.replacement):
                    result = pattern.compiled.sub(pattern.replacement, preprocessed)
                else:
                    result = pattern.compiled.sub(pattern.replacement, preprocessed)
                print(f"After replacement: {result}")
            else:
                print("No match")
    
    # Test full processing
    print("\n--- Full Processing ---")
    result = processor.process(test_input)
    print(f"Final result: {result}")
    
    # Let's also check what happens character by character
    print("\n--- Character Analysis ---")
    for i, char in enumerate(result):
        print(f"Position {i}: '{char}' (ord: {ord(char)})")

if __name__ == "__main__":
    test_pattern_matching()