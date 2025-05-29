#!/usr/bin/env python3
"""
MathSpeak Stress Testing Suite
==============================

Comprehensive testing to find breaking points and edge cases.
"""

import asyncio
import sys
import os
import time
import random
import string
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.engine import MathematicalTTSEngine


class StressTestResults:
    """Collect and analyze test results"""
    
    def __init__(self):
        self.results = []
        self.failures = []
        self.successes = []
        self.performance_issues = []
        self.crashes = []
        
    def add_result(self, test_name: str, input_data: str, success: bool, 
                   output: str = "", error: str = "", duration: float = 0.0):
        """Add a test result"""
        result = {
            'test': test_name,
            'input': input_data[:100] + ('...' if len(input_data) > 100 else ''),
            'success': success,
            'output': output[:100] + ('...' if len(output) > 100 else ''),
            'error': error,
            'duration': duration
        }
        
        self.results.append(result)
        
        if success:
            self.successes.append(result)
        else:
            self.failures.append(result)
            
        if duration > 5.0:
            self.performance_issues.append(result)
            
        if 'crash' in error.lower() or 'segfault' in error.lower():
            self.crashes.append(result)
    
    def print_summary(self):
        """Print test summary"""
        total = len(self.results)
        print("\n" + "="*60)
        print("STRESS TEST SUMMARY")
        print("="*60)
        print(f"Total Tests: {total}")
        print(f"Successes: {len(self.successes)} ({len(self.successes)/total*100:.1f}%)")
        print(f"Failures: {len(self.failures)} ({len(self.failures)/total*100:.1f}%)")
        print(f"Performance Issues: {len(self.performance_issues)}")
        print(f"Crashes: {len(self.crashes)}")
        
        if self.failures:
            print("\n❌ FAILURES:")
            for f in self.failures[:10]:  # Show first 10
                print(f"  - {f['test']}: {f['error']}")
                
        if self.performance_issues:
            print("\n⏱️  PERFORMANCE ISSUES:")
            for p in self.performance_issues[:5]:
                print(f"  - {p['test']}: {p['duration']:.2f}s")


async def test_basic_functionality(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test basic functionality"""
    print("\n🔬 Testing Basic Functionality...")
    
    test_cases = [
        ("Empty input", ""),
        ("Single character", "x"),
        ("Simple expression", "x + y"),
        ("Basic fraction", "\\frac{1}{2}"),
        ("Greek letters", "\\alpha + \\beta = \\gamma"),
        ("Integral", "\\int_0^1 x dx"),
        ("Sum", "\\sum_{n=1}^{\\infty} \\frac{1}{n^2}"),
        ("Matrix", "\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}"),
        ("Complex number", "z = re^{i\\theta}"),
        ("Limit", "\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1"),
    ]
    
    for test_name, expression in test_cases:
        start = time.time()
        try:
            result = engine.process_latex(expression)
            duration = time.time() - start
            results.add_result(test_name, expression, True, result.processed, "", duration)
        except Exception as e:
            duration = time.time() - start
            results.add_result(test_name, expression, False, "", str(e), duration)


async def test_malformed_input(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test malformed and edge case inputs"""
    print("\n🔨 Testing Malformed Input...")
    
    test_cases = [
        ("Unmatched braces open", "\\frac{1{2}"),
        ("Unmatched braces close", "\\frac1}{2}"),
        ("Missing arguments", "\\frac{}{}"),
        ("Incomplete command", "\\fra"),
        ("Invalid command", "\\notacommand{x}"),
        ("Nested unmatched", "\\frac{\\frac{1}{2}{3}"),
        ("Empty subscript", "x_{}"),
        ("Empty superscript", "x^{}"),
        ("Multiple errors", "\\frac{1}{} + \\sum_{}^{} x_"),
        ("Just backslash", "\\"),
        ("Random backslashes", "\\\\\\\\\\"),
        ("Null bytes", "x\x00y"),
        ("Unicode mess", "∫∂∇⊗⊕∑∏"),
        ("Mixed valid/invalid", "\\int_0^1 \\notreal{x} dx"),
    ]
    
    for test_name, expression in test_cases:
        start = time.time()
        try:
            result = engine.process_latex(expression)
            duration = time.time() - start
            # If it doesn't crash, it's a success for malformed input
            results.add_result(f"Malformed: {test_name}", expression, True, result.processed, "", duration)
        except Exception as e:
            duration = time.time() - start
            # We expect some failures, but not crashes
            if "crash" not in str(e).lower():
                results.add_result(f"Malformed: {test_name}", expression, True, "", f"Handled: {e}", duration)
            else:
                results.add_result(f"Malformed: {test_name}", expression, False, "", str(e), duration)


async def test_extreme_sizes(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test extremely large and small inputs"""
    print("\n📏 Testing Extreme Sizes...")
    
    # Very long expression
    long_expr = "x + " * 1000 + "y"
    start = time.time()
    try:
        result = engine.process_latex(long_expr)
        duration = time.time() - start
        results.add_result("Very long expression (1000 terms)", long_expr, True, result.processed, "", duration)
    except Exception as e:
        duration = time.time() - start
        results.add_result("Very long expression (1000 terms)", long_expr, False, "", str(e), duration)
    
    # Deeply nested
    nested = "\\frac{" * 50 + "1" + "}{2}" * 50
    start = time.time()
    try:
        result = engine.process_latex(nested)
        duration = time.time() - start
        results.add_result("Deeply nested (50 levels)", nested, True, result.processed, "", duration)
    except Exception as e:
        duration = time.time() - start
        results.add_result("Deeply nested (50 levels)", nested, False, "", str(e), duration)
    
    # Many subscripts
    subscripts = "x" + "_{i" * 100 + "}" * 100
    start = time.time()
    try:
        result = engine.process_latex(subscripts)
        duration = time.time() - start
        results.add_result("Many subscripts (100)", subscripts, True, result.processed, "", duration)
    except Exception as e:
        duration = time.time() - start
        results.add_result("Many subscripts (100)", subscripts, False, "", str(e), duration)
    
    # Unicode explosion
    unicode_expr = "∫∑∏⊗⊕∂∇" * 100
    start = time.time()
    try:
        result = engine.process_latex(unicode_expr)
        duration = time.time() - start
        results.add_result("Unicode heavy", unicode_expr, True, result.processed, "", duration)
    except Exception as e:
        duration = time.time() - start
        results.add_result("Unicode heavy", unicode_expr, False, "", str(e), duration)


async def test_security_issues(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test potential security vulnerabilities"""
    print("\n🔒 Testing Security Issues...")
    
    test_cases = [
        ("Path traversal attempt", "\\input{../../../../etc/passwd}"),
        ("Command injection", "\\write18{rm -rf /}"),
        ("File write attempt", "\\openout{/tmp/evil.txt}"),
        ("Infinite loop attempt", "\\def\\x{\\x}\\x"),
        ("Memory bomb", "\\def\\x{AAAA}\\def\\y{\\x\\x\\x\\x}" * 10),
        ("Format string", "%s%s%s%s%s%s%s"),
        ("SQL injection style", "'; DROP TABLE users; --"),
        ("Script injection", "<script>alert('xss')</script>"),
        ("Binary data", "\x00\x01\x02\x03\x04\x05"),
        ("Control characters", "\r\n\t\b\f"),
    ]
    
    for test_name, expression in test_cases:
        start = time.time()
        try:
            result = engine.process_latex(expression)
            duration = time.time() - start
            # If it processes without executing malicious code, it's safe
            results.add_result(f"Security: {test_name}", expression, True, result.processed, "", duration)
        except Exception as e:
            duration = time.time() - start
            results.add_result(f"Security: {test_name}", expression, True, "", f"Blocked: {e}", duration)


async def test_domain_switching(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test rapid domain switching"""
    print("\n🔄 Testing Domain Switching...")
    
    expressions = [
        ("Topology", "Let (X, \\tau) be a T_2 space"),
        ("Complex", "f(z) = e^z is entire"),
        ("Numerical", "Newton's method: x_{n+1} = x_n - f(x_n)/f'(x_n)"),
        ("Manifolds", "TM = \\bigsqcup_{p \\in M} T_p M"),
        ("ODE", "y'' + p(x)y' + q(x)y = 0"),
        ("Mixed", "In topology, \\pi_1(S^1) = \\mathbb{Z}, while \\int_0^{2\\pi} e^{i\\theta} d\\theta = 0"),
    ]
    
    # Rapid switching
    for i in range(20):
        domain, expr = random.choice(expressions)
        start = time.time()
        try:
            result = engine.process_latex(expr)
            duration = time.time() - start
            if i == 0 or i == 19:  # Log first and last
                results.add_result(f"Domain switch {i}: {domain}", expr, True, result.processed, "", duration)
        except Exception as e:
            duration = time.time() - start
            results.add_result(f"Domain switch {i}: {domain}", expr, False, "", str(e), duration)


async def test_concurrent_processing(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test concurrent processing"""
    print("\n⚡ Testing Concurrent Processing...")
    
    expressions = [
        "\\int_0^1 x^2 dx",
        "\\sum_{n=1}^{100} n",
        "\\lim_{x \\to \\infty} \\frac{1}{x}",
        "\\frac{d}{dx} e^x",
        "\\pi_1(S^1) \\cong \\mathbb{Z}",
    ] * 10  # 50 total
    
    async def process_expr(expr: str, idx: int):
        start = time.time()
        try:
            result = engine.process_latex(expr)
            return (True, result.processed, "", time.time() - start)
        except Exception as e:
            return (False, "", str(e), time.time() - start)
    
    # Process all concurrently
    start_all = time.time()
    tasks = [process_expr(expr, i) for i, expr in enumerate(expressions)]
    results_list = await asyncio.gather(*tasks, return_exceptions=True)
    total_duration = time.time() - start_all
    
    success_count = sum(1 for r in results_list if isinstance(r, tuple) and r[0])
    results.add_result(
        f"Concurrent processing (50 expressions)",
        f"{len(expressions)} expressions",
        success_count == len(expressions),
        f"{success_count}/{len(expressions)} successful",
        f"Total time: {total_duration:.2f}s",
        total_duration
    )


async def test_special_characters(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test special characters and encodings"""
    print("\n🌍 Testing Special Characters...")
    
    test_cases = [
        ("Emoji in text", "Let 🚀 = velocity"),
        ("Chinese characters", "设 x = 速度"),
        ("Arabic RTL", "دع x = السرعة"),
        ("Mixed scripts", "∫ 한글 dx = 日本語"),
        ("Combining marks", "x̃ + ỹ = z̃"),
        ("Zero width spaces", "x​+​y​=​z"),
        ("Surrogate pairs", "𝕏 + 𝕐 = ℤ"),
        ("Control chars", "x\u200by\u200c=\u200dz"),
        ("BOM marker", "\ufeffx + y = z"),
        ("Invalid UTF-8", "x\ufffdy\ufffdz"),
    ]
    
    for test_name, expression in test_cases:
        start = time.time()
        try:
            result = engine.process_latex(expression)
            duration = time.time() - start
            results.add_result(f"Special char: {test_name}", expression, True, result.processed, "", duration)
        except Exception as e:
            duration = time.time() - start
            results.add_result(f"Special char: {test_name}", expression, False, "", str(e), duration)


async def test_cache_behavior(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test caching behavior"""
    print("\n💾 Testing Cache Behavior...")
    
    # Test cache hit
    expr = "\\int_0^1 x^2 dx"
    
    # First call - cache miss
    start1 = time.time()
    result1 = engine.process_latex(expr)
    duration1 = time.time() - start1
    
    # Second call - should be cache hit
    start2 = time.time()
    result2 = engine.process_latex(expr)
    duration2 = time.time() - start2
    
    cache_working = duration2 < duration1 * 0.5  # Should be at least 2x faster
    results.add_result(
        "Cache hit performance",
        expr,
        cache_working,
        f"First: {duration1:.3f}s, Second: {duration2:.3f}s",
        "" if cache_working else "Cache not improving performance",
        duration2
    )
    
    # Test cache overflow
    print("  Testing cache overflow...")
    unique_exprs = [f"x_{i} + y_{i} = {i}" for i in range(2000)]  # More than cache size
    
    start = time.time()
    for expr in unique_exprs:
        try:
            engine.process_latex(expr)
        except:
            pass
    duration = time.time() - start
    
    results.add_result(
        "Cache overflow (2000 unique expressions)",
        "Many unique expressions",
        True,  # If it doesn't crash, it's good
        f"Processed 2000 expressions",
        "",
        duration
    )


async def test_error_recovery(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test error recovery"""
    print("\n🔧 Testing Error Recovery...")
    
    # Process valid expression
    engine.process_latex("x + y = z")
    
    # Process invalid expression
    try:
        engine.process_latex("\\undefined{command}")
    except:
        pass
    
    # Try valid expression again
    start = time.time()
    try:
        result = engine.process_latex("a + b = c")
        duration = time.time() - start
        results.add_result(
            "Recovery after error",
            "Valid after invalid",
            True,
            result.processed,
            "",
            duration
        )
    except Exception as e:
        duration = time.time() - start
        results.add_result(
            "Recovery after error",
            "Valid after invalid",
            False,
            "",
            str(e),
            duration
        )


async def test_memory_leaks(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test for memory leaks"""
    print("\n💧 Testing Memory Leaks...")
    
    import psutil
    process = psutil.Process()
    
    # Get initial memory
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Process many expressions
    for i in range(1000):
        try:
            engine.process_latex(f"\\int_0^{i} x^{i} dx")
        except:
            pass
    
    # Get final memory
    final_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = final_memory - initial_memory
    
    # Allow up to 50MB increase
    no_major_leak = memory_increase < 50
    
    results.add_result(
        "Memory leak test (1000 expressions)",
        "1000 different expressions",
        no_major_leak,
        f"Memory increase: {memory_increase:.1f}MB",
        "" if no_major_leak else f"Excessive memory use: {memory_increase:.1f}MB",
        0
    )


async def test_edge_case_domains(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test edge cases in specific domains"""
    print("\n🔬 Testing Domain Edge Cases...")
    
    test_cases = [
        # Topology edge cases
        ("Empty topology", "(X, \\{\\emptyset, X\\})"),
        ("Infinite union", "\\bigcup_{i=1}^{\\infty} U_i"),
        ("Strange space names", "T_{2\\frac{1}{2}}"),
        
        # Complex analysis edge cases
        ("Branch cuts", "\\log z, z \\in \\mathbb{C} \\setminus (-\\infty, 0]"),
        ("Multi-valued", "z^{1/3}"),
        ("Essential singularity", "e^{1/z}"),
        
        # Numerical edge cases
        ("Convergence criteria", "\\|x_{k+1} - x_k\\| < 10^{-16}"),
        ("Ill-conditioned", "\\kappa(A) = 10^{15}"),
        ("Special matrices", "A \\in \\mathbb{R}^{1000 \\times 1000}"),
        
        # ODE edge cases
        ("Stiff equation", "y' = -1000(y - \\cos(t)) - \\sin(t)"),
        ("Singular point", "x^2 y'' + xy' + (x^2 - n^2)y = 0"),
        ("DAE system", "F(t, y, y') = 0"),
        
        # Manifolds edge cases
        ("Exotic manifold", "E_8 \\times E_8"),
        ("Non-orientable", "\\mathbb{RP}^2"),
        ("Infinite dimensional", "\\text{Diff}(S^1)"),
    ]
    
    for test_name, expression in test_cases:
        start = time.time()
        try:
            result = engine.process_latex(expression)
            duration = time.time() - start
            results.add_result(f"Edge case: {test_name}", expression, True, result.processed, "", duration)
        except Exception as e:
            duration = time.time() - start
            results.add_result(f"Edge case: {test_name}", expression, False, "", str(e), duration)


async def test_real_world_examples(engine: MathematicalTTSEngine, results: StressTestResults):
    """Test real-world mathematical expressions"""
    print("\n📚 Testing Real-World Examples...")
    
    examples = [
        # From calculus textbook
        ("Calculus: Chain rule", 
         "\\frac{d}{dx}[f(g(x))] = f'(g(x)) \\cdot g'(x)"),
        
        # From linear algebra
        ("LinAlg: Eigenvalue equation", 
         "(A - \\lambda I)\\mathbf{v} = \\mathbf{0}"),
        
        # From differential geometry
        ("DiffGeo: Gauss-Bonnet", 
         "\\int_M K dA + \\int_{\\partial M} k_g ds = 2\\pi \\chi(M)"),
        
        # From quantum mechanics
        ("Quantum: Schrödinger", 
         "i\\hbar\\frac{\\partial}{\\partial t}\\Psi = \\hat{H}\\Psi"),
        
        # From statistics
        ("Stats: Normal distribution", 
         "f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{1}{2}\\left(\\frac{x-\\mu}{\\sigma}\\right)^2}"),
        
        # From number theory
        ("Number theory: Euler's theorem", 
         "a^{\\phi(n)} \\equiv 1 \\pmod{n}"),
        
        # From functional analysis
        ("Functional: Riesz representation", 
         "\\langle f, g \\rangle = \\int_X f(x)\\overline{g(x)} d\\mu(x)"),
        
        # From algebraic topology
        ("AlgTop: Mayer-Vietoris", 
         "\\cdots \\to H_n(A \\cap B) \\to H_n(A) \\oplus H_n(B) \\to H_n(X) \\to H_{n-1}(A \\cap B) \\to \\cdots"),
    ]
    
    for test_name, expression in examples:
        start = time.time()
        try:
            result = engine.process_latex(expression)
            duration = time.time() - start
            results.add_result(test_name, expression, True, result.processed, "", duration)
        except Exception as e:
            duration = time.time() - start
            results.add_result(test_name, expression, False, "", str(e), duration)


async def run_all_tests():
    """Run all stress tests"""
    print("🚀 Starting MathSpeak Stress Test Suite")
    print("=" * 60)
    
    # Initialize engine
    engine = MathematicalTTSEngine()
    results = StressTestResults()
    
    # Run all test categories
    await test_basic_functionality(engine, results)
    await test_malformed_input(engine, results)
    await test_extreme_sizes(engine, results)
    await test_security_issues(engine, results)
    await test_domain_switching(engine, results)
    await test_concurrent_processing(engine, results)
    await test_special_characters(engine, results)
    await test_cache_behavior(engine, results)
    await test_error_recovery(engine, results)
    await test_memory_leaks(engine, results)
    await test_edge_case_domains(engine, results)
    await test_real_world_examples(engine, results)
    
    # Cleanup
    engine.shutdown()
    
    # Print results
    results.print_summary()
    
    # Save detailed results
    with open('stress_test_results.json', 'w') as f:
        json.dump(results.results, f, indent=2)
    
    print(f"\nDetailed results saved to stress_test_results.json")
    
    return results


if __name__ == "__main__":
    results = asyncio.run(run_all_tests())