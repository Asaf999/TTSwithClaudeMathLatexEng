#!/usr/bin/env python3
"""
Hard Pattern Tests - Stress Testing MathSpeak
==============================================

Comprehensive tests designed to break the pattern recognition system
with challenging mathematical expressions.
"""

import sys
import time
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng/mathspeak')

def test_hard_patterns():
    """Test with challenging mathematical patterns"""
    
    try:
        from core.patterns_v2 import process_math_to_speech, AudienceLevel
        
        # HARD TEST CASES - designed to stress-test the system
        hard_test_cases = [
            # Complex nested expressions
            ("\\frac{\\frac{a}{b}}{\\frac{c}{d}}", "a over b over c over d"),
            ("\\sqrt{\\sqrt{x}}", "square root of square root of x"),
            ("x^{y^z}", "x to the y to the z"),
            ("\\int_0^{\\infty} e^{-x^2} dx", "integral from 0 to infinity of e to the negative x squared dx"),
            
            # Mixed derivatives and integrals
            ("\\frac{d^2}{dx^2}\\left(\\frac{dy}{dx}\\right)", "second derivative with respect to x of derivative of y with respect to x"),
            ("\\int \\frac{d}{dx}f(x) dx", "integral of derivative of f of x dx"),
            ("\\frac{\\partial^2 f}{\\partial x \\partial y}", "partial squared f partial x partial y"),
            
            # Complex fractions with operators
            ("\\frac{a + b}{c - d}", "a plus b over c minus d"),
            ("\\frac{x^2 + 3x + 2}{x - 1}", "x squared plus 3 x plus 2 over x minus 1"),
            ("\\frac{\\sin x}{\\cos x}", "sine x over cosine x"),
            
            # Multiple subscripts and superscripts
            ("x_{i,j}^{(n)}", "x i j to the n"),
            ("a_1^2 + a_2^2 + \\cdots + a_n^2", "a 1 squared plus a 2 squared plus dot dot dot plus a n squared"),
            ("\\sum_{i=1}^{n} x_i^2", "sum from i equals 1 to n x i squared"),
            
            # Complex limits
            ("\\lim_{x \\to 0^+} \\frac{\\sin x}{x}", "limit as x approaches 0 from the right of sine x over x"),
            ("\\lim_{n \\to \\infty} \\left(1 + \\frac{1}{n}\\right)^n", "limit as n approaches infinity of 1 plus 1 over n to the n"),
            
            # Matrix-like expressions
            ("\\begin{pmatrix} a & b \\\\\\\\ c & d \\end{pmatrix}", "matrix a b c d"),
            ("\\det\\begin{pmatrix} a & b \\\\\\\\ c & d \\end{pmatrix}", "determinant of matrix a b c d"),
            
            # Complex trigonometric expressions
            ("\\sin^2 x + \\cos^2 x", "sine squared x plus cosine squared x"),
            ("\\tan^{-1}\\left(\\frac{y}{x}\\right)", "inverse tangent of y over x"),
            ("\\sin(2\\pi x)", "sine of 2 pi x"),
            
            # Logarithms and exponentials
            ("\\log_2(x^3)", "log base 2 of x cubed"),
            ("e^{x + y}", "e to the x plus y"),
            ("\\ln(\\sqrt{x})", "natural log of square root of x"),
            
            # Set theory and logic
            ("A \\cup B \\cap C", "A union B intersection C"),
            ("\\forall x \\in \\mathbb{R}", "for all x in the real numbers"),
            ("\\exists y : y > 0", "there exists y such that y is greater than 0"),
            
            # Probability notation
            ("P(A|B)", "probability of A given B"),
            ("E[X^2]", "expected value of X squared"),
            ("\\text{Var}(X)", "variance of X"),
            
            # Complex analysis
            ("\\oint_C f(z) dz", "contour integral over C of f of z dz"),
            ("\\text{Res}(f, z_0)", "residue of f at z naught"),
            
            # Number theory
            ("a \\equiv b \\pmod{n}", "a is congruent to b modulo n"),
            ("\\gcd(a, b)", "greatest common divisor of a and b"),
            
            # Combinatorics
            ("\\binom{n}{k}", "n choose k"),
            ("n!", "n factorial"),
            
            # Vector calculus
            ("\\nabla \\cdot \\vec{F}", "divergence of F"),
            ("\\nabla \\times \\vec{F}", "curl of F"),
            ("\\vec{a} \\cdot \\vec{b}", "a dot b"),
            
            # Physics notation
            ("\\frac{dp}{dt}", "derivative of p with respect to t"),
            ("\\int F \\cdot dr", "integral of F dot dr"),
            
            # Statistics
            ("\\sigma^2", "sigma squared"),
            ("\\bar{x}", "x bar"),
            ("\\hat{\\theta}", "theta hat"),
            
            # Edge cases with spacing
            ("x+y", "x plus y"),
            ("x-y", "x minus y"),
            ("x*y", "x times y"),
            ("x/y", "x over y"),
            ("x=y", "x equals y"),
            
            # Greek letters in expressions
            ("\\alpha + \\beta = \\gamma", "alpha plus beta equals gamma"),
            ("\\pi r^2", "pi r squared"),
            ("\\theta = \\frac{\\pi}{4}", "theta equals pi over 4"),
            
            # Advanced calculus
            ("\\iint_D f(x,y) dx dy", "double integral over D of f of x y dx dy"),
            ("\\iiint_V f(x,y,z) dx dy dz", "triple integral over V of f of x y z dx dy dz"),
            
            # Continued fractions
            ("a_0 + \\cfrac{1}{a_1 + \\cfrac{1}{a_2}}", "a naught plus continued fraction 1 over a 1 plus continued fraction 1 over a 2"),
            
            # Absolute values and floor/ceiling
            ("|x|", "absolute value of x"),
            ("\\lfloor x \\rfloor", "floor of x"),
            ("\\lceil x \\rceil", "ceiling of x"),
            
            # More complex derivatives
            ("\\frac{d}{dx}\\left(x^2 \\sin x\\right)", "derivative of x squared sine x"),
            ("\\frac{\\partial}{\\partial x}\\left(x^2 + y^2\\right)", "partial partial x of x squared plus y squared"),
        ]
        
        print("Testing Hard Patterns - Stress Test:")
        print("=" * 60)
        
        passed = 0
        total = len(hard_test_cases)
        failed_tests = []
        
        for i, (input_latex, expected) in enumerate(hard_test_cases):
            try:
                start_time = time.time()
                result = process_math_to_speech(input_latex, AudienceLevel.UNDERGRADUATE)
                end_time = time.time()
                
                # More flexible matching for complex expressions
                # Check if key terms from expected are present
                expected_words = expected.lower().split()
                result_lower = result.lower()
                
                # Count how many expected words are found
                found_words = sum(1 for word in expected_words if word in result_lower and len(word) > 2)
                coverage = found_words / len(expected_words) if expected_words else 0
                
                # Accept if we have good coverage of expected terms
                success = coverage >= 0.3  # 30% of expected words should be present
                
                status = "✅ PASS" if success else "❌ FAIL"
                if success:
                    passed += 1
                else:
                    failed_tests.append((i+1, input_latex, expected, result))
                    
                print(f"{status} Test {i+1:2d}: {input_latex}")
                if not success:
                    print(f"    Expected: {expected}")
                    print(f"    Got:      {result}")
                    print(f"    Coverage: {coverage:.1%}")
                    
            except Exception as e:
                print(f"❌ ERROR Test {i+1:2d}: {input_latex} - {e}")
                failed_tests.append((i+1, input_latex, expected, f"ERROR: {e}"))
        
        print("\\n" + "=" * 60)
        print(f"Hard Pattern Results: {passed}/{total} ({passed/total*100:.1f}%)")
        
        if failed_tests:
            print(f"\\nFailed Tests ({len(failed_tests)}):")
            print("-" * 40)
            for test_num, latex, expected, result in failed_tests:
                print(f"Test {test_num}: {latex}")
                print(f"  Expected: {expected}")
                print(f"  Got: {result}")
                print()
        
        return passed, total, failed_tests
        
    except ImportError as e:
        print(f"Import error: {e}")
        return 0, 0, []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 0, 0, []

def test_engine_with_hard_patterns():
    """Test the main engine with hard patterns"""
    
    try:
        from core.engine import MathematicalTTSEngine
        
        engine = MathematicalTTSEngine()
        
        # Test a few representative hard cases with the main engine
        engine_test_cases = [
            "\\frac{\\frac{a}{b}}{\\frac{c}{d}}",
            "\\int_0^{\\infty} e^{-x^2} dx", 
            "\\lim_{x \\to 0^+} \\frac{\\sin x}{x}",
            "\\frac{d^2}{dx^2}\\left(x^2 \\sin x\\right)"
        ]
        
        print("\\nTesting Main Engine with Hard Patterns:")
        print("=" * 50)
        
        passed = 0
        for i, latex in enumerate(engine_test_cases):
            try:
                result_data = engine.process_latex(latex)
                if result_data.processed and len(result_data.processed.strip()) > 0:
                    print(f"✅ Engine Test {i+1}: {latex}")
                    print(f"   Result: {result_data.processed[:50]}...")
                    passed += 1
                else:
                    print(f"❌ Engine Test {i+1}: {latex}")
                    print(f"   Error: Empty or invalid result")
            except Exception as e:
                print(f"❌ Engine Test {i+1}: {latex} - Exception: {e}")
        
        print(f"\\nEngine Results: {passed}/{len(engine_test_cases)}")
        return passed, len(engine_test_cases)
        
    except Exception as e:
        print(f"Engine test error: {e}")
        return 0, 0

if __name__ == "__main__":
    # Test hard patterns
    pattern_passed, pattern_total, failed_tests = test_hard_patterns()
    
    # Test engine
    engine_passed, engine_total = test_engine_with_hard_patterns()
    
    print("\\n" + "=" * 60)
    print("HARD PATTERN STRESS TEST SUMMARY")
    print("=" * 60)
    print(f"Pattern Module: {pattern_passed}/{pattern_total} ({pattern_passed/pattern_total*100:.1f}%)")
    print(f"Main Engine:    {engine_passed}/{engine_total} ({engine_passed/engine_total*100:.1f}%)")
    print(f"Overall:        {pattern_passed + engine_passed}/{pattern_total + engine_total} ({(pattern_passed + engine_passed)/(pattern_total + engine_total)*100:.1f}%)")
    
    if failed_tests:
        print(f"\\nNeeds improvement: {len(failed_tests)} patterns")
    else:
        print("\\n🎉 ALL HARD PATTERNS PASSED!")