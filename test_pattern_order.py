#!/usr/bin/env python3
"""Debug pattern application order"""

from mathspeak.core.patterns_v2 import (
    MathSpeechProcessor, GeneralizationEngine, MathDomain, AudienceLevel
)

def test_pattern_order():
    """Test the order of pattern application"""
    
    processor = MathSpeechProcessor()
    engine = processor.engine
    
    # Test input
    test_input = r'\frac{1}{2}'
    print(f"Original input: {test_input}")
    
    # Manual step-by-step processing
    result = test_input
    
    # Preprocess
    result = processor._preprocess(result)
    print(f"\nAfter preprocessing: {result}")
    
    # Apply general patterns
    print("\n--- Applying General Patterns ---")
    for pattern in sorted(engine.general_patterns, key=lambda p: p.priority, reverse=True):
        old_result = result
        if callable(pattern.replacement):
            result = pattern.compiled.sub(pattern.replacement, result)
        else:
            result = pattern.compiled.sub(pattern.replacement, result)
        if result != old_result:
            print(f"Pattern '{pattern.description}' (priority {pattern.priority}) changed: {old_result} -> {result}")
    
    print(f"\nAfter general patterns: {result}")
    
    # Apply domain-specific patterns
    print("\n--- Applying Domain-Specific Patterns ---")
    for domain, handler in engine.handlers.items():
        print(f"\nProcessing domain: {domain.value}")
        old_result = result
        result = handler.process(result, AudienceLevel.UNDERGRADUATE)
        if result != old_result:
            print(f"  Changed: {old_result} -> {result}")
        else:
            print(f"  No change")
    
    print(f"\nFinal result: {result}")

if __name__ == "__main__":
    test_pattern_order()