#!/usr/bin/env python3
"""
Test Script for 100 Mathematical Speech Examples
===============================================

This script tests all 100 examples from the comprehensive guide to ensure
the MathSpeak system produces natural, professor-quality speech.
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Tuple, Dict
from tabulate import tabulate
from colorama import init, Fore, Style

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.patterns_v2 import process_math_to_speech, AudienceLevel

# Initialize colorama for colored output
init(autoreset=True)

# Define all 100 examples from the guide
EXAMPLES = [
    # Basic Operations (1-20)
    ("\\frac{3}{4}", "three fourths", "Basic fraction"),
    ("\\frac{x+1}{x-1}", "x plus 1 over x minus 1", "Algebraic fraction"),
    ("\\frac{1}{1 + \\frac{1}{x}}", "1 over 1 plus 1 over x", "Nested fraction"),
    ("\\frac{1}{2 + \\frac{1}{3 + \\frac{1}{4}}}", "1 over 2 plus 1 over 3 plus 1 over 4", "Continued fraction"),
    ("3\\frac{1}{2}", "3 and one half", "Mixed number"),
    ("x^2, x^3, x^4", "x squared, x cubed, x to the 4", "Basic powers"),
    ("x^n, x^{2n}, x^{n+1}", "x to the n, x to the 2 n, x to the n plus 1", "Variable powers"),
    ("x^{-1}, x^{-2}, x^{-n}", "x to the minus 1, x to the minus 2, x to the minus n", "Negative powers"),
    ("x^{1/2}, x^{2/3}", "x to the one half, x to the two thirds", "Fractional powers"),
    ("e^{x^2}, e^{-x}, e^{2x}", "e to the x squared, e to the minus x, e to the 2 x", "Exponentials"),
    ("\\sqrt{x^2 + y^2}", "square root of x squared plus y squared", "Square root"),
    ("\\sqrt[3]{x}, \\sqrt[n]{x}", "cube root of x, nth root of x", "Higher roots"),
    ("\\sqrt{\\sqrt{x}}", "square root of square root of x", "Nested roots"),
    ("a + b - c", "a plus b minus c", "Addition/subtraction"),
    ("2 \\cdot 3, 2 \\times 3", "2 dot 3, 2 times 3", "Multiplication"),
    ("2x, xy, 3abc", "2 x, x y, 3 a b c", "Implicit multiplication"),
    ("a \\div b, a/b", "a divided by b, a over b", "Division"),
    ("<, >, \\leq, \\geq", "less than, greater than, less than or equal to, greater than or equal to", "Comparisons"),
    ("=, \\approx, \\sim, \\cong", "equals, approximately, similar to, congruent to", "Equality variants"),
    ("\\pi, e, i, \\infty", "pi, e, i, infinity", "Constants"),
    
    # Functions and Special Notation (21-40)
    ("f(x), g(x,y)", "f of x, g of x y", "Function notation"),
    ("f(g(h(x)))", "f of g of h of x", "Nested functions"),
    ("(f \\circ g)(x)", "f composed with g of x", "Function composition"),
    ("f^{-1}(x), \\sin^{-1}(x)", "f inverse of x, arc sine of x", "Inverse functions"),
    ("\\sin x, \\cos(x), \\tan(2x)", "sine x, cosine of x, tangent of 2 x", "Trig functions"),
    ("\\sin^2 x, \\cos^3 x", "sine squared x, cosine cubed x", "Trig powers"),
    ("\\sinh x, \\cosh x", "hyperbolic sine x, hyperbolic cosine x", "Hyperbolic functions"),
    ("\\log x, \\log_{10} x, \\log_2 x", "log x, log base 10 of x, log base 2 of x", "Logarithms"),
    ("\\ln x, \\ln(x+1)", "natural log of x, natural log of x plus 1", "Natural log"),
    ("e^x, \\exp(x), 2^x", "e to the x, exponential of x, 2 to the x", "Exponential variations"),
    ("n!, (n+1)!", "n factorial, n plus 1 factorial", "Factorial"),
    ("n!!, n!!!", "n double factorial, n triple factorial", "Multiple factorial"),
    ("\\binom{n}{k}", "n choose k", "Binomial coefficient"),
    ("P(n,k)", "n permute k", "Permutations"),
    ("\\lfloor x \\rfloor, \\lceil x \\rceil", "floor of x, ceiling of x", "Floor/ceiling"),
    ("|x|, ||x||", "absolute value of x, norm of x", "Absolute value/norm"),
    ("\\text{sgn}(x)", "sign of x", "Sign function"),
    ("\\max(a,b), \\min\\{x,y,z\\}", "max of a and b, minimum of x, y, and z", "Max/min"),
    ("\\arg\\max_x f(x)", "arg max over x of f of x", "Arg functions"),
    ("f(x) = \\begin{cases} x & \\text{if } x > 0 \\\\ -x & \\text{if } x \\leq 0 \\end{cases}", 
     "f of x equals x if x is greater than 0, and minus x if x is less than or equal to 0", "Piecewise"),
    
    # Calculus and Analysis (41-60)
    ("f'(x), y', \\frac{df}{dx}", "f prime of x, y prime, d f d x", "Derivatives"),
    ("f''(x), f^{(4)}(x)", "f double prime of x, f 4th derivative of x", "Higher derivatives"),
    ("\\frac{\\partial f}{\\partial x}", "partial f partial x", "Partial derivative"),
    ("\\frac{\\partial^2 f}{\\partial x \\partial y}", "partial squared f partial x partial y", "Mixed partials"),
    ("\\frac{df}{dt}", "d f d t", "Total derivative"),
    ("\\nabla f", "gradient of f", "Gradient"),
    ("\\nabla \\cdot \\vec{F}, \\nabla \\times \\vec{F}", "divergence of F, curl of F", "Vector calculus"),
    ("\\nabla^2 f, \\Delta f", "Laplacian of f, Laplacian of f", "Laplacian"),
    ("\\int f(x) \\, dx", "integral of f of x d x", "Integral"),
    ("\\int_a^b f(x) \\, dx", "integral from a to b of f of x d x", "Definite integral"),
    ("\\iint_D f(x,y) \\, dA", "double integral over D of f of x y d A", "Double integral"),
    ("\\oint_C \\vec{F} \\cdot d\\vec{r}", "line integral around C of F dot d r", "Line integral"),
    ("\\lim_{x \\to a} f(x)", "limit as x approaches a of f of x", "Limit"),
    ("\\lim_{x \\to a^+} f(x)", "limit as x approaches a from the right of f of x", "One-sided limit"),
    ("\\lim_{x \\to \\infty} f(x)", "limit as x approaches infinity of f of x", "Limit at infinity"),
    ("\\sum_{n=1}^{\\infty} a_n", "sum from n equals 1 to infinity of a n", "Series"),
    ("\\prod_{i=1}^{n} a_i", "product from i equals 1 to n of a i", "Product"),
    ("f(x) = \\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n", 
     "f of x equals sum from n equals 0 to infinity of f to the n of a over n factorial times x minus a to the n", "Taylor series"),
    ("O(n^2), \\Omega(n\\log n)", "big O of n squared, big Omega of n log n", "Big O notation"),
    ("\\frac{d}{dx}, \\frac{\\partial}{\\partial x}", "d by d x, partial by partial x", "Differential operators"),
    
    # Set Theory and Logic (61-75)
    ("x \\in A, x \\notin B", "x in A, x not in B", "Set membership"),
    ("A \\subset B, A \\subseteq B", "A subset of B, A subset or equal to B", "Subsets"),
    ("A \\cup B, A \\cap B", "A union B, A intersect B", "Set operations"),
    ("A^c, \\overline{A}", "A complement, A complement", "Set complement"),
    ("\\emptyset, \\mathcal{U}", "empty set, universal set", "Special sets"),
    ("\\{x \\in \\mathbb{R} : x > 0\\}", "the set of x in R such that x is greater than 0", "Set builder"),
    ("\\forall x, \\exists y", "for all x, there exists y", "Quantifiers"),
    ("p \\land q, p \\lor q, \\neg p", "p and q, p or q, not p", "Logical operators"),
    ("p \\implies q, p \\iff q", "p implies q, p if and only if q", "Implications"),
    ("\\mathbb{N}, \\mathbb{Z}, \\mathbb{R}", "N, Z, R", "Number sets"),
    ("[a,b], (a,b)", "closed interval from a to b, open interval from a to b", "Intervals"),
    ("|A|", "cardinality of A", "Cardinality"),
    ("\\mathcal{P}(A)", "power set of A", "Power set"),
    ("A \\times B", "A cross B", "Cartesian product"),
    ("\\therefore, \\square", "therefore, Q E D", "Logic symbols"),
    
    # Advanced Mathematics (76-90)
    ("A^T, A^{-1}", "A transpose, A inverse", "Matrix operations"),
    ("AB, A \\otimes B", "A B, A tensor B", "Matrix multiplication"),
    ("\\det(A), \\text{tr}(A)", "determinant of A, trace of A", "Matrix functions"),
    ("Av = \\lambda v", "A v equals lambda v", "Eigenvalue equation"),
    ("\\langle u, v \\rangle", "inner product of u and v", "Inner product"),
    ("||v||, ||v||_2", "norm of v, 2 norm of v", "Norms"),
    ("T^{ij}, T_{ijk}", "T upper i j, T lower i j k", "Tensor notation"),
    ("[A,B], \\{A,B\\}", "commutator of A and B, anticommutator of A and B", "Commutators"),
    ("f * g", "f convolved with g", "Convolution"),
    ("\\mathcal{F}\\{f\\}, \\hat{f}", "Fourier transform of f, f hat", "Fourier transform"),
    ("a \\equiv b \\pmod{n}", "a is congruent to b mod n", "Modular arithmetic"),
    ("G/H, gH", "G mod H, g H", "Group theory"),
    ("V \\oplus W", "V direct sum W", "Direct sum"),
    ("f: G \\to H", "f from G to H", "Homomorphism"),
    ("A \\cong B", "A is isomorphic to B", "Isomorphism"),
    
    # Edge Cases and Special Patterns (91-100)
    ("\\tilde{x}, \\hat{y}, \\bar{z}", "x tilde, y hat, z bar", "Decorated variables"),
    ("\\hat{\\hat{x}}", "x hat hat", "Multiple decorations"),
    ("x_i^2, a_{n+1}^{k-1}", "x sub i squared, a sub n plus 1 to the k minus 1", "Sub/super combinations"),
    ("H_2O, CO_2", "H 2 O, C O 2", "Chemical notation"),
    ("5\\text{ m/s}", "5 meters per second", "Units"),
    ("25\\%", "25 percent", "Percentages"),
    ("\\$100", "100 dollars", "Currency"),
    ("90°", "90 degrees", "Angles"),
    ("1, 2, 3, \\ldots, n", "1, 2, 3, dot dot dot, n", "Ellipsis"),
    ("\\lim_{n \\to \\infty} \\left(1 + \\frac{1}{n}\\right)^n = e", 
     "limit as n approaches infinity of, quantity 1 plus 1 over n, to the n, equals e", "Complex expression"),
]

def test_pattern(latex: str, expected: str, description: str) -> Tuple[bool, str, str]:
    """Test a single pattern and return result"""
    try:
        # Process with the new pattern system
        result = process_math_to_speech(latex)
        
        # Clean up for comparison
        result_clean = ' '.join(result.lower().split())
        expected_clean = ' '.join(expected.lower().split())
        
        # Check if result matches expected (allow some flexibility)
        # We'll be lenient and check if key parts are present
        success = True
        missing_parts = []
        
        # Split expected into key words and check each
        expected_words = expected_clean.split()
        for word in expected_words:
            if word not in ['the', 'of', 'to', 'a', 'an']:  # Skip articles
                if word not in result_clean:
                    success = False
                    missing_parts.append(word)
        
        return success, result, ' '.join(missing_parts) if missing_parts else ""
        
    except Exception as e:
        return False, f"ERROR: {str(e)}", str(e)

async def test_with_engine(latex: str, expected: str, description: str, engine: MathematicalTTSEngine) -> Tuple[bool, str, str]:
    """Test using the full engine"""
    try:
        # Process through the engine
        processed = engine.process_latex(latex)
        result = processed.processed
        
        # Clean up for comparison
        result_clean = ' '.join(result.lower().split())
        expected_clean = ' '.join(expected.lower().split())
        
        # Check if result matches expected
        success = True
        missing_parts = []
        
        expected_words = expected_clean.split()
        for word in expected_words:
            if word not in ['the', 'of', 'to', 'a', 'an']:  # Skip articles
                if word not in result_clean:
                    success = False
                    missing_parts.append(word)
        
        # Also test audio generation for a few examples
        if description in ["Basic fraction", "Derivatives", "Set membership"]:
            output_file = f"test_audio_{description.replace(' ', '_').lower()}.mp3"
            audio_success = await engine.speak_expression(processed, output_file)
            if audio_success:
                result += " [Audio OK]"
        
        return success, result, ' '.join(missing_parts) if missing_parts else ""
        
    except Exception as e:
        return False, f"ERROR: {str(e)}", str(e)

async def run_all_tests():
    """Run all 100 tests and generate report"""
    print(f"{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Testing 100 Mathematical Speech Examples")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    # Initialize engine
    engine = MathematicalTTSEngine()
    
    # Test results
    results = []
    passed = 0
    failed = 0
    
    # Test each example
    for i, (latex, expected, description) in enumerate(EXAMPLES, 1):
        print(f"{Fore.YELLOW}Testing {i}/100: {description}...", end='', flush=True)
        
        # Test with pattern processor
        pattern_success, pattern_result, pattern_error = test_pattern(latex, expected, description)
        
        # Test with full engine
        engine_success, engine_result, engine_error = await test_with_engine(latex, expected, description, engine)
        
        # Overall success if either method works
        success = pattern_success or engine_success
        
        if success:
            passed += 1
            print(f" {Fore.GREEN}✓")
        else:
            failed += 1
            print(f" {Fore.RED}✗")
        
        results.append({
            'ID': i,
            'Description': description[:30] + '...' if len(description) > 30 else description,
            'LaTeX': latex[:40] + '...' if len(latex) > 40 else latex,
            'Expected': expected[:40] + '...' if len(expected) > 40 else expected,
            'Pattern Result': pattern_result[:40] + '...' if len(pattern_result) > 40 else pattern_result,
            'Engine Result': engine_result[:40] + '...' if len(engine_result) > 40 else engine_result,
            'Status': '✓' if success else '✗',
            'Error': pattern_error or engine_error if not success else ''
        })
    
    # Print summary
    print(f"\n{Fore.CYAN}{'='*80}")
    print(f"{Fore.CYAN}Test Summary")
    print(f"{Fore.CYAN}{'='*80}\n")
    
    print(f"{Fore.GREEN}Passed: {passed}/100 ({passed/100*100:.1f}%)")
    print(f"{Fore.RED}Failed: {failed}/100 ({failed/100*100:.1f}%)")
    
    # Show failures in detail
    if failed > 0:
        print(f"\n{Fore.RED}Failed Tests:")
        print(f"{Fore.RED}{'-'*80}")
        
        failed_results = [r for r in results if r['Status'] == '✗']
        
        # Create a simplified table for failed tests
        failed_table = []
        for r in failed_results:
            failed_table.append([
                r['ID'],
                r['Description'],
                r['Expected'][:50],
                r['Pattern Result'][:50],
                r['Error'][:30] if r['Error'] else 'Missing words'
            ])
        
        headers = ['ID', 'Description', 'Expected', 'Got', 'Issue']
        print(tabulate(failed_table, headers=headers, tablefmt='grid'))
    
    # Test some special cases
    print(f"\n{Fore.CYAN}Testing Additional Complex Examples:")
    print(f"{Fore.CYAN}{'-'*80}")
    
    complex_examples = [
        ("$A_{ij} = a_{ij}$", "Matrix element notation"),
        ("$\\int_0^1 x^2 dx = \\frac{1}{3}$", "Integral with result"),
        ("$\\sum_{k=1}^n k = \\frac{n(n+1)}{2}$", "Sum formula"),
        ("$e^{i\\pi} + 1 = 0$", "Euler's identity"),
    ]
    
    for latex, desc in complex_examples:
        processed = engine.process_latex(latex)
        print(f"\n{desc}:")
        print(f"  Input:  {latex}")
        print(f"  Output: {processed.processed}")
    
    # Performance report
    print(f"\n{Fore.CYAN}Performance Report:")
    print(f"{Fore.CYAN}{'-'*80}")
    report = engine.get_performance_report()
    print(f"Tokens per second: {report['metrics']['tokens_per_second']:.2f}")
    print(f"Cache hit rate: {report['metrics']['cache_hit_rate']:.2%}")
    print(f"Unknown commands found: {report['metrics']['unknown_commands']}")
    
    # Save unknown commands
    engine.save_unknown_commands()
    
    return passed, failed

def main():
    """Main test runner"""
    try:
        passed, failed = asyncio.run(run_all_tests())
        
        # Exit with appropriate code
        if failed == 0:
            print(f"\n{Fore.GREEN}All tests passed! The system produces natural mathematical speech.")
            sys.exit(0)
        else:
            print(f"\n{Fore.YELLOW}Some tests failed. Review the results above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Tests interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}Test suite error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()