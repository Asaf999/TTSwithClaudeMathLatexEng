#!/usr/bin/env python3
"""Trace pattern application"""

from mathspeak.core.patterns_v2 import (
    MathSpeechProcessor, GeneralizationEngine, MathDomain, AudienceLevel
)

def trace_processing():
    """Trace the processing of a simple fraction"""
    
    processor = MathSpeechProcessor()
    engine = processor.engine
    
    # Test input
    test_input = r'\frac{1}{2}'
    print(f"Original input: {test_input}")
    
    # Manual processing following the new order
    result = test_input
    
    # Preprocess
    result = processor._preprocess(result)
    print(f"\n1. After preprocessing: '{result}'")
    
    # Apply general patterns
    for pattern in sorted(engine.general_patterns, key=lambda p: p.priority, reverse=True):
        old_result = result
        if callable(pattern.replacement):
            result = pattern.compiled.sub(pattern.replacement, result)
        else:
            result = pattern.compiled.sub(pattern.replacement, result)
        if result != old_result:
            print(f"   General pattern '{pattern.description}' changed: '{old_result}' -> '{result}'")
    
    # Apply domain-specific patterns in the new order
    priority_order = [
        MathDomain.ALGEBRA,
        MathDomain.FUNCTIONS,
        MathDomain.CALCULUS,
        MathDomain.LINEAR_ALGEBRA,
        MathDomain.SET_THEORY,
        MathDomain.PROBABILITY,
        MathDomain.NUMBER_THEORY,
        MathDomain.COMPLEX_ANALYSIS,
        MathDomain.LOGIC,
        MathDomain.BASIC_ARITHMETIC,
    ]
    
    for i, domain in enumerate(priority_order):
        if domain in engine.handlers:
            old_result = result
            result = engine.handlers[domain].process(result, AudienceLevel.UNDERGRADUATE)
            if result != old_result:
                print(f"\n{i+2}. Domain {domain.value} changed: '{old_result}' -> '{result}'")
    
    # Cleanup
    old_result = result
    result = engine._cleanup(result)
    if result != old_result:
        print(f"\nFinal cleanup changed: '{old_result}' -> '{result}'")
    
    print(f"\nFinal result: '{result}'")

if __name__ == "__main__":
    trace_processing()