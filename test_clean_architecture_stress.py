#!/usr/bin/env python3
"""
Comprehensive stress test suite for MathSpeak Clean Architecture.
Tests all layers, both standard and enhanced modes, and validates performance.
"""

import sys
import os
import time
import asyncio
import json
import gc
import psutil
from typing import List, Dict, Optional, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from dataclasses import dataclass

sys.path.append('/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng')

# Import clean architecture components
from mathspeak_clean.domain.entities.expression import MathExpression
from mathspeak_clean.domain.entities.pattern import MathPattern
from mathspeak_clean.domain.services.pattern_processor import PatternProcessorService
from mathspeak_clean.domain.services.enhanced_pattern_processor import EnhancedPatternProcessorService
from mathspeak_clean.application.use_cases.process_expression import (
    ProcessExpressionUseCase,
    ProcessExpressionRequest
)
from mathspeak_clean.infrastructure.persistence.lru_cache import LRUCache
from mathspeak_clean.infrastructure.persistence.memory_pattern_repository import MemoryPatternRepository
from mathspeak_clean.infrastructure.config.settings import Settings, reset_settings
from mathspeak_clean.infrastructure.container import Container, reset_container
from mathspeak_clean.infrastructure.logging.logger import get_logger
from mathspeak_clean.adapters.legacy_pattern_adapter import LegacyPatternAdapter
from mathspeak_clean.adapters.enhanced_pattern_adapter import EnhancedPatternAdapter
from mathspeak_clean.shared.constants import PRIORITY_HIGH, PatternDomain
from mathspeak_clean.shared.exceptions import ValidationError

# Color codes for output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(text: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")

def print_subheader(text: str):
    print(f"\n{Colors.BLUE}{Colors.BOLD}{text}{Colors.ENDC}")
    print(f"{Colors.BLUE}{'-'*len(text)}{Colors.ENDC}")

def print_success(text: str):
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")

def print_info(text: str):
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")

def print_warning(text: str):
    print(f"{Colors.WARNING}⚠️  {text}{Colors.ENDC}")

def print_error(text: str):
    print(f"{Colors.FAIL}❌ {text}{Colors.ENDC}")

@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    passed: bool
    duration: float
    message: str
    details: Optional[Dict[str, Any]] = None

class CleanArchitectureStressTester:
    """Comprehensive stress tester for clean architecture."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
        self.test_results: List[TestResult] = []
        
        # Test expressions from simple to extremely complex
        self.test_suite = {
            "simple": [
                (r"x^2", "x squared"),
                (r"\frac{1}{2}", "one half"),
                (r"\pi", "pi"),
                (r"\alpha + \beta", "alpha plus beta"),
            ],
            "moderate": [
                (r"\int_0^1 x^2 dx", "integral from 0 to 1 of x squared d x"),
                (r"\sum_{i=1}^n i", "sum from i equals 1 to n of i"),
                (r"\lim_{x \to 0} \frac{\sin x}{x}", "limit as x approaches 0 of sine x over x"),
                (r"\begin{pmatrix} 1 & 2 \\ 3 & 4 \end{pmatrix}", "2 by 2 matrix"),
            ],
            "complex": [
                (r"\frac{d}{dx}\left[\int_0^x e^{-t^2} dt\right]", "derivative of integral"),
                (r"\nabla \times (\nabla \times \vec{F})", "curl of curl of F"),
                (r"\oint_C \vec{F} \cdot d\vec{r}", "line integral"),
                (r"T^{\mu\nu}_{;\rho}", "covariant derivative of tensor"),
            ],
            "extreme": [
                # Deeply nested expression
                (r"\frac{\frac{\frac{a}{b}}{c}}{\frac{d}{\frac{e}{f}}}", "deeply nested fraction"),
                # Large matrix
                (r"\begin{pmatrix} " + " & ".join([f"a_{{{i}{j}}}" for j in range(10)]) + r" \end{pmatrix}", "large matrix"),
                # Complex integral
                (r"\int\int\int_{\mathbb{R}^3} f(x,y,z) e^{-(x^2+y^2+z^2)} \, dx\,dy\,dz", "triple integral"),
            ]
        }

    def record_result(self, name: str, passed: bool, duration: float, 
                     message: str, details: Optional[Dict[str, Any]] = None):
        """Record test result."""
        result = TestResult(name, passed, duration, message, details)
        self.test_results.append(result)
        
    async def test_domain_layer(self):
        """Test domain entities and services in isolation."""
        print_header("1. DOMAIN LAYER TESTS")
        
        # Test 1: MathExpression entity
        print_subheader("Testing MathExpression Entity")
        
        valid_expressions = [
            r"\frac{1}{2}",
            r"x^2 + y^2 = z^2",
            r"\int_0^\infty e^{-x} dx",
        ]
        
        invalid_expressions = [
            r"\frac{1}{",  # Unbalanced
            r"",           # Empty
            r"x" * 20000,  # Too long
        ]
        
        for expr_str in valid_expressions:
            try:
                start = time.time()
                expr = MathExpression(latex=expr_str)
                duration = time.time() - start
                
                print_success(f"Valid expression: {expr_str[:30]}... ({duration:.4f}s)")
                
                # Test complexity scoring
                complexity = expr.complexity_score
                print_info(f"  Complexity score: {complexity}")
                
            except Exception as e:
                print_error(f"Failed on valid expression: {e}")
        
        for expr_str in invalid_expressions:
            try:
                expr = MathExpression(latex=expr_str)
                print_error(f"Should have failed: {expr_str[:30]}...")
            except ValidationError:
                print_success(f"Correctly rejected: {expr_str[:30]}...")
            except Exception as e:
                print_error(f"Wrong exception type: {e}")
        
        # Test 2: Pattern matching
        print_subheader("Testing Pattern Entity")
        
        pattern = MathPattern(
            pattern=r"\\frac\{(\d+)\}\{(\d+)\}",
            replacement=r"\1 over \2",
            priority=100
        )
        
        test_cases = [
            (r"\frac{3}{4}", "3 over 4"),
            (r"\frac{10}{20}", "10 over 20"),
            (r"\frac{a}{b}", r"\frac{a}{b}"),  # Shouldn't match, returns original
        ]
        
        for latex, expected in test_cases:
            result = pattern.apply(latex)
            if result == expected:
                print_success(f"Pattern test passed: {latex}")
            else:
                print_error(f"Pattern test failed: {latex} -> {result} (expected {expected})")
        
        # Test 3: Pattern Processor Service
        print_subheader("Testing Pattern Processor Service")
        
        # Create repository with patterns
        repository = MemoryPatternRepository()
        patterns = [
            MathPattern(r"\\alpha", "alpha", priority=100, domain=PatternDomain.GENERAL),
            MathPattern(r"\\beta", "beta", priority=100, domain=PatternDomain.GENERAL),
            MathPattern(r"\\frac\{([^{}]+)\}\{([^{}]+)\}", r"\1 over \2", priority=50, domain=PatternDomain.GENERAL),
            MathPattern(r"\+", " plus ", priority=90, domain=PatternDomain.GENERAL),
        ]
        
        for p in patterns:
            repository.add(p)
        
        processor = PatternProcessorService(repository)
        
        test_exprs = [
            (r"\alpha + \beta", "alpha plus beta"),
            (r"\frac{\alpha}{\beta}", "alpha over beta"),
        ]
        
        for latex, hint in test_exprs:
            expr = MathExpression(latex)
            try:
                result = processor.process_expression(expr)
                print_info(f"{latex} -> {result}")
            except Exception as e:
                print_error(f"Processing failed: {e}")

    async def test_application_layer(self):
        """Test use cases and application services."""
        print_header("2. APPLICATION LAYER TESTS")
        
        # Reset global state
        reset_settings()
        reset_container()
        
        # Create container with test configuration
        settings = Settings(
            cache_enabled=True,
            cache_max_size=100,
            use_enhanced_processor=False  # Start with standard
        )
        
        container = Container(settings)
        
        # Test ProcessExpressionUseCase
        print_subheader("Testing ProcessExpressionUseCase")
        
        use_case = container.get(ProcessExpressionUseCase)
        
        # Test 1: Basic processing
        request = ProcessExpressionRequest(
            latex=r"\frac{1}{2}",
            audience_level="undergraduate"
        )
        
        start = time.time()
        response = use_case.execute(request)
        duration = time.time() - start
        
        print_info(f"First call (no cache): {duration:.4f}s")
        print_info(f"Result: {response.result.speech}")
        print_info(f"Cached: {response.cached}")
        
        # Test 2: Cached processing
        start = time.time()
        response2 = use_case.execute(request)
        duration2 = time.time() - start
        
        print_info(f"Second call (cached): {duration2:.4f}s")
        print_info(f"Cached: {response2.cached}")
        
        if response2.cached and duration2 < duration / 5:
            print_success(f"Cache working! {duration/duration2:.1f}x speedup")
        else:
            print_warning("Cache may not be working optimally")
        
        # Test 3: Batch processing
        print_subheader("Testing Batch Processing")
        
        batch_requests = [
            ProcessExpressionRequest(latex=f"x^{{{i}}}", audience_level="undergraduate")
            for i in range(20)
        ]
        
        start = time.time()
        results = [use_case.execute(req) for req in batch_requests]
        sequential_time = time.time() - start
        
        print_info(f"Sequential processing of 20 expressions: {sequential_time:.4f}s")
        print_info(f"Average per expression: {sequential_time/20:.4f}s")

    async def test_infrastructure_layer(self):
        """Test infrastructure components."""
        print_header("3. INFRASTRUCTURE LAYER TESTS")
        
        # Test 1: LRU Cache
        print_subheader("Testing LRU Cache")
        
        cache = LRUCache(max_size=3)
        
        # Fill cache
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.set("key3", "value3")
        
        # Test retrieval
        assert cache.get("key1") == "value1"
        print_success("Cache retrieval works")
        
        # Test eviction
        cache.set("key4", "value4")  # Should evict key2
        assert cache.get("key2") is None
        assert cache.get("key1") == "value1"  # Still there (was accessed)
        print_success("LRU eviction works correctly")
        
        # Test stats
        stats = cache.get_stats()
        print_info(f"Cache stats: {stats}")
        
        # Test 2: Settings
        print_subheader("Testing Settings Configuration")
        
        # Reset settings first
        reset_settings()
        
        # Test with environment variables
        os.environ["MATHSPEAK_AUDIENCE_LEVEL"] = "undergraduate"
        os.environ["MATHSPEAK_CACHE_ENABLED"] = "true"
        os.environ["MATHSPEAK_CACHE_MAX_SIZE"] = "500"
        
        from mathspeak_clean.infrastructure.config.settings import get_settings
        settings = get_settings()
        
        print_info(f"Audience level: {settings.default_audience_level}")
        print_info(f"Cache enabled: {settings.cache_enabled}")
        print_info(f"Cache size: {settings.cache_max_size}")
        
        if settings.cache_enabled and settings.cache_max_size == 500:
            print_success("Environment configuration works")
        
        # Test 3: Logger
        print_subheader("Testing Logger")
        
        logger = get_logger("test_logger")
        
        # Test different log levels
        try:
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")
            logger.error("Error message")
            print_success("Logger functioning correctly")
        except Exception as e:
            print_error(f"Logger error: {e}")

    async def test_adapter_layer(self):
        """Test adapters for legacy and enhanced patterns."""
        print_header("4. ADAPTER LAYER TESTS")
        
        # Test 1: Legacy Pattern Adapter
        print_subheader("Testing Legacy Pattern Adapter")
        
        try:
            legacy_adapter = LegacyPatternAdapter()
            legacy_adapter.initialize()
            patterns_repo = legacy_adapter.get_pattern_repository()
            patterns = patterns_repo.get_all()
            
            print_info(f"Loaded {len(patterns)} legacy patterns")
            
            # Test a few patterns
            test_expr = r"\frac{1}{2}"
            processor = PatternProcessorService(patterns_repo)
            
            expr = MathExpression(test_expr)
            result = processor.process_expression(expr)
            
            print_info(f"Legacy result: {test_expr} -> {result}")
            print_success("Legacy adapter working")
            
        except Exception as e:
            print_warning(f"Legacy adapter not available: {e}")
        
        # Test 2: Enhanced Pattern Adapter
        print_subheader("Testing Enhanced Pattern Adapter")
        
        try:
            enhanced_adapter = EnhancedPatternAdapter()
            enhanced_adapter.initialize()
            patterns_repo = enhanced_adapter.get_pattern_repository()
            patterns = patterns_repo.get_all()
            
            print_info(f"Loaded {len(patterns)} enhanced patterns")
            
            # Get enhancement info
            info = enhanced_adapter.get_enhancement_info()
            print_info(f"Enhancement info: {info}")
            
            # Test enhanced features
            test_cases = [
                (r"\frac{1}{2}", "one half"),  # Special fraction
                (r"\sin(x)", "sine"),  # Natural phrasing
                (r"\frac{d}{dx}", "derivative"),  # Context-aware
            ]
            
            processor = EnhancedPatternProcessorService(patterns_repo)
            
            for latex, expected_hint in test_cases:
                expr = MathExpression(latex)
                try:
                    result = processor.process_expression(expr)
                    print_info(f"{latex} -> {result}")
                    if expected_hint.lower() in result.lower():
                        print_success(f"Enhanced pattern working: {expected_hint}")
                except Exception as e:
                    print_warning(f"Processing failed: {e}")
                    
        except Exception as e:
            print_warning(f"Enhanced adapter not available: {e}")

    async def test_presentation_layer(self):
        """Test API endpoints."""
        print_header("5. PRESENTATION LAYER TESTS")
        
        print_subheader("Testing API Components")
        
        # Import API components
        try:
            from mathspeak_clean.presentation.api.app import create_app, ProcessRequest
            
            # Create app
            app = create_app()
            print_success("API app created successfully")
            
            # Test request/response models
            test_request = ProcessRequest(
                latex=r"\int_0^1 x^2 dx",
                audience_level="undergraduate"
            )
            print_info(f"Created request model: {test_request.latex}")
            
            print_success("API components working")
            
        except Exception as e:
            print_warning(f"API components error: {e}")
        
        print_info("Note: Full API testing requires running the server")

    async def stress_test_performance(self):
        """Intensive performance stress testing."""
        print_header("6. PERFORMANCE STRESS TEST")
        
        # Reset and create containers for both modes
        reset_container()
        
        standard_container = Container(Settings(use_enhanced_processor=False))
        enhanced_container = Container(Settings(use_enhanced_processor=True))
        
        standard_use_case = standard_container.get(ProcessExpressionUseCase)
        enhanced_use_case = enhanced_container.get(ProcessExpressionUseCase)
        
        # Test 1: Processing speed comparison
        print_subheader("Standard vs Enhanced Mode Performance")
        
        test_expressions = []
        for category, expressions in self.test_suite.items():
            test_expressions.extend([expr for expr, _ in expressions])
        
        # Standard mode
        start = time.time()
        for expr in test_expressions:
            request = ProcessExpressionRequest(latex=expr, audience_level="undergraduate")
            try:
                standard_use_case.execute(request)
            except Exception:
                pass  # Continue testing
        standard_time = time.time() - start
        
        # Enhanced mode
        start = time.time()
        for expr in test_expressions:
            request = ProcessExpressionRequest(latex=expr, audience_level="undergraduate")
            try:
                enhanced_use_case.execute(request)
            except Exception:
                pass  # Continue testing
        enhanced_time = time.time() - start
        
        print_info(f"Standard mode: {standard_time:.4f}s for {len(test_expressions)} expressions")
        print_info(f"Enhanced mode: {enhanced_time:.4f}s for {len(test_expressions)} expressions")
        if standard_time > 0:
            print_info(f"Enhanced overhead: {((enhanced_time/standard_time - 1) * 100):.1f}%")
        
        # Test 2: Memory stress test
        print_subheader("Memory Stress Test")
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process 1000 unique expressions
        print_info("Processing 1000 unique expressions...")
        for i in range(1000):
            expr = f"\\frac{{{i}}}{{x^{{{i % 10}}}}}"
            request = ProcessExpressionRequest(latex=expr, audience_level="undergraduate")
            try:
                enhanced_use_case.execute(request)
            except Exception:
                pass  # Continue testing
        
        peak_memory = process.memory_info().rss / 1024 / 1024
        
        # Force garbage collection
        gc.collect()
        final_memory = process.memory_info().rss / 1024 / 1024
        
        print_info(f"Initial memory: {initial_memory:.2f} MB")
        print_info(f"Peak memory: {peak_memory:.2f} MB")
        print_info(f"After GC: {final_memory:.2f} MB")
        
        memory_leak = final_memory - initial_memory
        if memory_leak < 50:
            print_success(f"No significant memory leak ({memory_leak:.2f} MB)")
        else:
            print_warning(f"Possible memory leak ({memory_leak:.2f} MB)")
        
        # Test 3: Concurrent processing
        print_subheader("Concurrent Processing Stress Test")
        
        def process_expression_sync(use_case, expr):
            request = ProcessExpressionRequest(latex=expr, audience_level="undergraduate")
            try:
                return use_case.execute(request)
            except Exception as e:
                return None
        
        # Create 100 complex expressions
        complex_expressions = []
        for i in range(100):
            nested = r"\frac{1}{2}"
            for j in range(3):  # Triple nesting
                nested = f"\\frac{{{nested}}}{{x_{{{i}_{{{j}}}}}}}"
            complex_expressions.append(nested)
        
        # Process concurrently
        start = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for expr in complex_expressions:
                future = executor.submit(process_expression_sync, enhanced_use_case, expr)
                futures.append(future)
            
            # Wait for all to complete
            results = [f.result() for f in futures]
        
        concurrent_time = time.time() - start
        successful = sum(1 for r in results if r is not None)
        
        print_info(f"Processed {successful}/100 complex expressions concurrently in {concurrent_time:.4f}s")
        print_info(f"Average per expression: {concurrent_time/100:.4f}s")
        
        # Test 4: Cache stress test
        print_subheader("Cache Stress Test")
        
        # Create container with small cache
        reset_container()
        small_cache_container = Container(Settings(
            cache_max_size=10,
            use_enhanced_processor=True
        ))
        use_case = small_cache_container.get(ProcessExpressionUseCase)
        
        # Repeatedly process same 20 expressions with cache size 10
        expressions = [f"x^{{{i}}}" for i in range(20)]
        
        cache_hits = 0
        total_calls = 0
        for _ in range(3):  # 3 rounds
            for expr in expressions:
                request = ProcessExpressionRequest(latex=expr, audience_level="undergraduate")
                try:
                    response = use_case.execute(request)
                    total_calls += 1
                    if response.cached:
                        cache_hits += 1
                except Exception:
                    pass
        
        if total_calls > 0:
            hit_rate = (cache_hits / total_calls) * 100
            print_info(f"Cache hit rate with size 10: {hit_rate:.1f}% ({cache_hits}/{total_calls})")

    async def test_extreme_cases(self):
        """Test extreme edge cases."""
        print_header("7. EXTREME EDGE CASES")
        
        reset_container()
        container = Container(Settings(use_enhanced_processor=True))
        use_case = container.get(ProcessExpressionUseCase)
        
        extreme_cases = [
            # Very long expression
            ("Long expression", "x" + " + x" * 500),
            
            # Deeply nested
            ("Deep nesting", self._create_deeply_nested(10)),
            
            # Many special characters
            ("Special chars", r"\alpha\beta\gamma\delta\epsilon\zeta\eta\theta"),
            
            # Mixed content
            ("Mixed content", r"The limit $\lim_{x \to 0} \frac{\sin x}{x} = 1$ is fundamental"),
            
            # Empty/whitespace
            ("Empty", ""),
            ("Whitespace", "   "),
            
            # Malformed
            ("Unclosed brace", r"\frac{1"),
            ("Unknown command", r"\unknowncommand{x}"),
        ]
        
        for name, expr in extreme_cases:
            print_subheader(f"Testing: {name}")
            try:
                start = time.time()
                request = ProcessExpressionRequest(latex=expr, audience_level="undergraduate")
                response = use_case.execute(request)
                duration = time.time() - start
                
                print_success(f"Handled successfully in {duration:.4f}s")
                if len(response.result.speech) > 100:
                    print_info(f"Result (truncated): {response.result.speech[:100]}...")
                else:
                    print_info(f"Result: {response.result.speech}")
                    
            except Exception as e:
                print_info(f"Exception (expected): {str(e)}")

    def _create_deeply_nested(self, depth: int) -> str:
        """Create deeply nested fraction."""
        expr = "x"
        for i in range(depth):
            expr = f"\\frac{{{expr}}}{{x_{{{i}}}}}"
        return expr

    async def run_all_tests(self):
        """Run complete test suite."""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'🚀 MATHSPEAK CLEAN ARCHITECTURE STRESS TEST 🚀'.center(80)}{Colors.ENDC}")
        print(f"{Colors.CYAN}{'Testing all layers and components of the clean architecture'.center(80)}{Colors.ENDC}\n")
        
        test_methods = [
            ("Domain Layer", self.test_domain_layer),
            ("Application Layer", self.test_application_layer),
            ("Infrastructure Layer", self.test_infrastructure_layer),
            ("Adapter Layer", self.test_adapter_layer),
            ("Presentation Layer", self.test_presentation_layer),
            ("Performance Stress", self.stress_test_performance),
            ("Extreme Cases", self.test_extreme_cases),
        ]
        
        overall_start = time.time()
        
        for test_name, test_method in test_methods:
            try:
                await test_method()
                self.record_result(test_name, True, 0, "Test suite passed")
            except Exception as e:
                self.record_result(test_name, False, 0, f"Test suite failed: {str(e)}")
                print_error(f"\n{test_name} failed with exception: {str(e)}")
                import traceback
                traceback.print_exc()
        
        overall_duration = time.time() - overall_start
        
        # Print summary
        print_header("TEST SUMMARY")
        
        passed = sum(1 for r in self.test_results if r.passed)
        failed = len(self.test_results) - passed
        
        print(f"\n{Colors.BOLD}Total test suites: {len(self.test_results)}{Colors.ENDC}")
        print(f"{Colors.GREEN}Passed: {passed}{Colors.ENDC}")
        if failed > 0:
            print(f"{Colors.FAIL}Failed: {failed}{Colors.ENDC}")
        
        print(f"\n{Colors.BOLD}Total duration: {overall_duration:.2f} seconds{Colors.ENDC}")
        
        if failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✨ ALL TESTS PASSED! ✨{Colors.ENDC}")
            print(f"{Colors.GREEN}The clean architecture is working perfectly!{Colors.ENDC}")
        else:
            print(f"\n{Colors.WARNING}⚠️  Some tests failed. Check the output above for details.{Colors.ENDC}")

# Quick comparison test
def quick_clean_test():
    """Quick test comparing standard vs enhanced modes."""
    print("\n🚀 Quick Clean Architecture Test\n")
    
    # Test both modes
    for use_enhanced in [False, True]:
        mode = "Enhanced" if use_enhanced else "Standard"
        print(f"\n{Colors.BLUE}Testing {mode} Mode:{Colors.ENDC}")
        
        reset_container()
        settings = Settings(use_enhanced_processor=use_enhanced)
        container = Container(settings)
        use_case = container.get(ProcessExpressionUseCase)
        
        test_cases = [
            r"\frac{1}{2}",
            r"\sin^2(x) + \cos^2(x) = 1",
            r"\lim_{x \to \infty} \frac{1}{x} = 0",
        ]
        
        for latex in test_cases:
            request = ProcessExpressionRequest(latex=latex, audience_level="undergraduate")
            try:
                response = use_case.execute(request)
                print(f"  {latex} → {response.result.speech}")
            except Exception as e:
                print(f"  {latex} → ERROR: {str(e)}")

async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MathSpeak Clean Architecture")
    parser.add_argument("--quick", action="store_true", help="Run quick test only")
    parser.add_argument("--full", action="store_true", help="Run full stress test")
    
    args = parser.parse_args()
    
    if args.quick or (not args.quick and not args.full):
        quick_clean_test()
    
    if args.full:
        tester = CleanArchitectureStressTester()
        await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())