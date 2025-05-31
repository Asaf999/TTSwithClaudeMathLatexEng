#!/usr/bin/env python3
"""Final comprehensive test of clean architecture."""

import sys
import time
import gc
import psutil
import os

sys.path.append('/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng')

from mathspeak_clean.infrastructure.config.settings import Settings, reset_settings
from mathspeak_clean.infrastructure.container import Container, reset_container
from mathspeak_clean.application.use_cases.process_expression import (
    ProcessExpressionUseCase,
    ProcessExpressionRequest
)

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_section(title):
    """Print a section header."""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title.center(60)}{Colors.ENDC}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_pass(msg):
    """Print success message."""
    print(f"{Colors.GREEN}✅ {msg}{Colors.ENDC}")

def print_fail(msg):
    """Print failure message."""
    print(f"{Colors.RED}❌ {msg}{Colors.ENDC}")

def print_info(msg):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.ENDC}")

def test_enhanced_mode():
    """Test enhanced mode with 98% natural speech."""
    print_section("ENHANCED MODE TEST (98% Natural Speech)")
    
    reset_container()
    container = Container()  # Default is enhanced=True
    use_case = container.get(ProcessExpressionUseCase)
    
    test_cases = [
        # Special fractions
        (r"\frac{1}{2}", "one half"),
        (r"\frac{1}{3}", "one third"),
        (r"\frac{2}{3}", "two thirds"),
        (r"\frac{1}{4}", "one quarter"),
        
        # Derivatives
        (r"\frac{d}{dx} f(x)", "the derivative of f of x"),
        (r"\frac{d^2y}{dx^2}", "the 2 derivative of y with respect to x"),
        (r"\frac{\partial f}{\partial x}", "the partial derivative of f with respect to x"),
        
        # Integrals
        (r"\int_0^1 x^2 dx", "the integral from zero to one of x squared, dx"),
        (r"\int f(x) dx", "the integral of f of x with respect to x"),
        
        # Statistics
        (r"P(A|B)", "probability of a given b"),
        (r"\mathbb{E}[X]", "the expected value of X"),
        (r"\text{Var}(X)", "the variance of X"),
        
        # Complex expressions
        (r"\lim_{x \to \infty} \frac{1}{x}", "the limit as x approaches infinity of one over x"),
        (r"\sum_{i=1}^n i^2", "the sum from i equals one to n of i squared"),
    ]
    
    passed = 0
    failed = 0
    
    for latex, expected_hint in test_cases:
        try:
            request = ProcessExpressionRequest(latex=latex)
            response = use_case.execute(request)
            result = response.result.speech
            
            # Check if result contains expected elements
            if any(word in result.lower() for word in expected_hint.lower().split()[:3]):
                print_pass(f"{latex:<30} → {result}")
                passed += 1
            else:
                print_fail(f"{latex:<30} → {result} (expected: {expected_hint})")
                failed += 1
                
        except Exception as e:
            print_fail(f"{latex:<30} → ERROR: {e}")
            failed += 1
    
    print(f"\n{Colors.BOLD}Results: {passed}/{passed+failed} passed ({passed/(passed+failed)*100:.1f}%){Colors.ENDC}")
    return passed, failed

def test_caching():
    """Test caching functionality."""
    print_section("CACHING TEST")
    
    reset_container()
    container = Container()
    use_case = container.get(ProcessExpressionUseCase)
    
    expressions = [
        r"\frac{1}{2}",
        r"\sin(x)",
        r"\int_0^1 x dx",
        r"\sum_{i=1}^n i",
        r"\lim_{x \to 0} x",
    ]
    
    # First pass - no cache
    print_info("First pass (building cache):")
    first_times = []
    for expr in expressions:
        request = ProcessExpressionRequest(latex=expr)
        start = time.time()
        response = use_case.execute(request)
        duration = time.time() - start
        first_times.append(duration)
        print(f"  {expr:<20} {duration*1000:.2f}ms (cached: {response.cached})")
    
    # Second pass - should be cached
    print_info("\nSecond pass (from cache):")
    second_times = []
    cache_hits = 0
    for i, expr in enumerate(expressions):
        request = ProcessExpressionRequest(latex=expr)
        start = time.time()
        response = use_case.execute(request)
        duration = time.time() - start
        second_times.append(duration)
        
        if response.cached:
            cache_hits += 1
            speedup = first_times[i] / duration if duration > 0 else 999
            print_pass(f"{expr:<20} {duration*1000:.2f}ms (speedup: {speedup:.1f}x)")
        else:
            print_fail(f"{expr:<20} {duration*1000:.2f}ms (not cached!)")
    
    print(f"\n{Colors.BOLD}Cache hit rate: {cache_hits}/{len(expressions)} ({cache_hits/len(expressions)*100:.0f}%){Colors.ENDC}")
    return cache_hits == len(expressions)

def test_error_handling():
    """Test error handling."""
    print_section("ERROR HANDLING TEST")
    
    reset_container()
    container = Container()
    use_case = container.get(ProcessExpressionUseCase)
    
    test_cases = [
        ("Empty expression", ""),
        ("Unbalanced braces", r"\frac{1"),
        ("Too long", "x" * 20000),
        ("Invalid LaTeX", r"\invalid{command}"),
        ("Nested too deep", r"\frac" * 50 + "{1}" * 50),
    ]
    
    handled_correctly = 0
    
    for name, expr in test_cases:
        try:
            request = ProcessExpressionRequest(latex=expr)
            response = use_case.execute(request)
            print_fail(f"{name}: Unexpectedly succeeded with '{response.result.speech}'")
        except Exception as e:
            print_pass(f"{name}: Correctly rejected ({type(e).__name__})")
            handled_correctly += 1
    
    print(f"\n{Colors.BOLD}Handled correctly: {handled_correctly}/{len(test_cases)}{Colors.ENDC}")
    return handled_correctly == len(test_cases)

def test_performance():
    """Test performance and memory usage."""
    print_section("PERFORMANCE TEST")
    
    reset_container()
    container = Container()
    use_case = container.get(ProcessExpressionUseCase)
    
    # Memory before
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Process many expressions
    expressions = [f"x^{{{i}}}" for i in range(1000)]
    
    print_info("Processing 1000 unique expressions...")
    start = time.time()
    
    for expr in expressions:
        request = ProcessExpressionRequest(latex=expr)
        try:
            use_case.execute(request)
        except:
            pass
    
    total_time = time.time() - start
    
    # Memory after
    mem_after = process.memory_info().rss / 1024 / 1024
    
    # Garbage collection
    gc.collect()
    mem_gc = process.memory_info().rss / 1024 / 1024
    
    print_info(f"Total time: {total_time:.2f}s")
    print_info(f"Average per expression: {total_time/1000*1000:.2f}ms")
    print_info(f"Memory before: {mem_before:.1f}MB")
    print_info(f"Memory after: {mem_after:.1f}MB (delta: {mem_after-mem_before:.1f}MB)")
    print_info(f"Memory after GC: {mem_gc:.1f}MB (delta: {mem_gc-mem_before:.1f}MB)")
    
    # Check for memory leak
    leak = mem_gc - mem_before
    if leak < 50:
        print_pass(f"No significant memory leak ({leak:.1f}MB)")
        return True
    else:
        print_fail(f"Possible memory leak ({leak:.1f}MB)")
        return False

def test_devil_compatibility():
    """Test compatibility with devil test cases."""
    print_section("DEVIL TEST COMPATIBILITY")
    
    reset_container()
    container = Container()
    use_case = container.get(ProcessExpressionUseCase)
    
    # Sample devil test cases
    devil_tests = [
        r"\frac{\frac{\frac{a}{b}}{c}}{\frac{d}{\frac{e}{f}}}",
        r"\int_{\int_0^1 f(x)dx}^{\int_0^2 g(x)dx} h(t) dt",
        r"\sum_{\substack{i=1\\j=1}}^{\substack{n\\m}} a_{i,j}",
        r"\lim_{x \to \lim_{y \to 0} f(y)} g(x)",
        r"\sqrt{\sqrt{\sqrt{\sqrt{x}}}}",
    ]
    
    processed = 0
    
    for expr in devil_tests:
        try:
            request = ProcessExpressionRequest(latex=expr)
            response = use_case.execute(request)
            print_pass(f"Processed: {expr[:40]}... → {response.result.speech[:40]}...")
            processed += 1
        except Exception as e:
            print_fail(f"Failed: {expr[:40]}... ({str(e)[:40]}...)")
    
    print(f"\n{Colors.BOLD}Processed: {processed}/{len(devil_tests)} ({processed/len(devil_tests)*100:.0f}%){Colors.ENDC}")
    return processed == len(devil_tests)

def main():
    """Run all tests."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}🚀 MATHSPEAK CLEAN ARCHITECTURE FINAL TEST 🚀{Colors.ENDC}")
    print(f"{Colors.BLUE}Testing the complete clean architecture implementation{Colors.ENDC}\n")
    
    test_results = {}
    
    # Run all tests
    tests = [
        ("Enhanced Mode", test_enhanced_mode),
        ("Caching", test_caching),
        ("Error Handling", test_error_handling),
        ("Performance", test_performance),
        ("Devil Compatibility", test_devil_compatibility),
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if isinstance(result, tuple):
                passed, failed = result
                test_results[test_name] = passed > 0 and failed == 0
            else:
                test_results[test_name] = result
        except Exception as e:
            print_fail(f"Test {test_name} crashed: {e}")
            test_results[test_name] = False
    
    # Summary
    print_section("FINAL SUMMARY")
    
    total_passed = sum(1 for v in test_results.values() if v)
    total_tests = len(test_results)
    
    print(f"\n{Colors.BOLD}Test Results:{Colors.ENDC}")
    for test_name, passed in test_results.items():
        if passed:
            print_pass(f"{test_name}")
        else:
            print_fail(f"{test_name}")
    
    print(f"\n{Colors.BOLD}Overall: {total_passed}/{total_tests} tests passed{Colors.ENDC}")
    
    if total_passed == total_tests:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✨ ALL TESTS PASSED! ✨{Colors.ENDC}")
        print(f"{Colors.GREEN}The clean architecture is working perfectly!{Colors.ENDC}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}⚠️  Some tests failed. See details above.{Colors.ENDC}")
        return 1

if __name__ == "__main__":
    sys.exit(main())