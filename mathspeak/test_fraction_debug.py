#!/usr/bin/env python3
"""Debug script to test fraction pattern processing"""

from core.engine import MathematicalTTSEngine
from core.patterns import PatternProcessor

# Test 1: Pattern processor directly
print("Test 1: Pattern Processor Direct Test")
print("=" * 50)
processor = PatternProcessor()
test_text = r'\frac{\sqrt{\pi}}{2}'
result = processor.process(test_text)
print(f"Input:  {test_text}")
print(f"Output: {result}")
print()

# Test 2: Engine processing
print("Test 2: Engine Processing Test")
print("=" * 50)
engine = MathematicalTTSEngine()
test_expr = r'\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}'
result = engine.process_latex(test_expr)
print(f"Input:  {test_expr}")
print(f"Output: {result.processed}")
print()

# Test 3: Just the fraction through engine
print("Test 3: Fraction Only Through Engine")
print("=" * 50)
result2 = engine.process_latex(r'\frac{\sqrt{\pi}}{2}')
print(f"Input:  \\frac{{\\sqrt{{\\pi}}}}{{2}}")
print(f"Output: {result2.processed}")
print()

# Test 4: Check general processing
print("Test 4: General Processing Test")
print("=" * 50)
processed = engine._general_processing(r'\frac{\sqrt{\pi}}{2}')
print(f"Input:  \\frac{{\\sqrt{{\\pi}}}}{{2}}")
print(f"Output: {processed}")