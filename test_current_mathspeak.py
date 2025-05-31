#!/usr/bin/env python3
"""
Simple test to check current MathSpeak functionality
"""

import sys
import os
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

def test_patterns_v2():
    """Test the patterns_v2 module directly"""
    
    try:
        from core.patterns_v2 import process_math_to_speech, AudienceLevel
        
        test_cases = [
            # Basic cases
            ("\\frac{3}{4}", "three fourths"),
            ("x^2", "x squared"),
            ("\\sqrt{x}", "square root of x"),
            ("\\int_0^1 x dx", "integral from 0 to 1 of x dx"),
            ("\\frac{d}{dx} f(x)", "derivative of f of x"),
            ("f(x) = x^2", "f of x equals x squared"),
            ("\\sin x", "sine x"),
            ("\\pi", "pi"),
            ("\\infty", "infinity"),
            ("2x + 3", "2 x plus 3")
        ]
        
        print("Testing patterns_v2 module:")
        print("=" * 50)
        
        passed = 0
        total = len(test_cases)
        
        for i, (input_latex, expected) in enumerate(test_cases):
            try:
                result = process_math_to_speech(input_latex, AudienceLevel.UNDERGRADUATE)
                success = expected.lower() in result.lower() or result.lower() in expected.lower()
                
                status = "✅ PASS" if success else "❌ FAIL"
                if success:
                    passed += 1
                    
                print(f"{status} Test {i+1:2d}: {input_latex}")
                if not success:
                    print(f"    Expected: {expected}")
                    print(f"    Got:      {result}")
                    
            except Exception as e:
                print(f"❌ ERROR Test {i+1:2d}: {input_latex} - {e}")
        
        print("\n" + "=" * 50)
        print(f"Results: {passed}/{total} ({passed/total*100:.1f}%)")
        return passed, total
        
    except Exception as e:
        print(f"Failed to import patterns_v2: {e}")
        return 0, 0

def test_main_engine():
    """Test the main engine if available"""
    
    try:
        from core.engine import MathematicalTTSEngine
        
        engine = MathematicalTTSEngine(enable_caching=False)
        
        test_cases = [
            "\\frac{3}{4}",
            "x^2 + 5x + 6",
            "\\int_0^1 x^2 dx",
            "f(x) = \\sin x"
        ]
        
        print("\nTesting main engine:")
        print("=" * 50)
        
        for i, latex in enumerate(test_cases):
            try:
                result = engine.process_latex(latex)
                print(f"✅ Test {i+1}: {latex}")
                print(f"    Result: {result.processed[:100]}...")
                print(f"    Context: {result.context}")
                print(f"    Time: {result.processing_time:.3f}s")
                print()
                
            except Exception as e:
                print(f"❌ ERROR Test {i+1}: {latex} - {e}")
        
        engine.shutdown()
        
    except Exception as e:
        print(f"Failed to test main engine: {e}")

if __name__ == "__main__":
    passed, total = test_patterns_v2()
    test_main_engine()
    
    print(f"\nOverall: {passed}/{total} patterns working")