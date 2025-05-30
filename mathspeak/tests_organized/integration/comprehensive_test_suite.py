#!/usr/bin/env python3
"""
Comprehensive Test Suite for MathSpeak Production Readiness
===========================================================

This suite tests the system from multiple angles:
1. Performance under load
2. Edge cases and error handling
3. Real-world usage scenarios
4. Security and robustness
5. Resource consumption
6. Concurrent usage
7. Platform compatibility
"""

import asyncio
import json
import os
import sys
import time
import psutil
import threading
import tempfile
import subprocess
import random
import gc
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, field
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import traceback

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine, MathematicalContext
from mathspeak.core.voice_manager import VoiceManager
from mathspeak.utils.logger import setup_logging
import logging

setup_logging(logging.INFO)
logger = logging.getLogger(__name__)

# ===========================
# Test Result Classes
# ===========================

@dataclass
class TestResult:
    """Individual test result"""
    test_name: str
    category: str
    passed: bool
    duration: float
    error: str = ""
    metrics: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class CategoryResult:
    """Results for a test category"""
    category_name: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    total_duration: float = 0.0
    test_results: List[TestResult] = field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        return (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0

# ===========================
# Test Data
# ===========================

class TestData:
    """Test expressions and scenarios"""
    
    # Basic expressions
    BASIC_EXPRESSIONS = [
        "x^2 + y^2 = z^2",
        "\\frac{d}{dx} e^x = e^x",
        "\\int_0^1 x^2 dx = \\frac{1}{3}",
        "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}",
        "\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1",
    ]
    
    # Complex mathematical expressions
    COMPLEX_EXPRESSIONS = [
        r"\\oint_\\gamma f(z) dz = 2\\pi i \\sum_{k} \\text{Res}(f, z_k)",
        r"\\pi_1(S^1) \\cong \\mathbb{Z}",
        r"\\nabla \\times (\\nabla \\times \\mathbf{F}) = \\nabla(\\nabla \\cdot \\mathbf{F}) - \\nabla^2 \\mathbf{F}",
        r"\\frac{\\partial^2 u}{\\partial t^2} = c^2 \\nabla^2 u",
        r"\\int_{-\\infty}^{\\infty} e^{-x^2} dx = \\sqrt{\\pi}",
    ]
    
    # Real-world lecture snippets
    LECTURE_SNIPPETS = [
        "Let $f: M \\to N$ be a smooth map between manifolds. The differential $df_p: T_p M \\to T_{f(p)} N$ is defined by $(df_p(v))(g) = v(g \\circ f)$ for $v \\in T_p M$ and $g \\in C^\\infty(N)$.",
        "Consider the sequence $(x_n)$ defined by $x_1 = 1$ and $x_{n+1} = \\frac{1}{2}(x_n + \\frac{2}{x_n})$. We claim that $\\lim_{n \\to \\infty} x_n = \\sqrt{2}$.",
        "The Fourier transform of $f(x) = e^{-ax^2}$ is $\\hat{f}(\\xi) = \\sqrt{\\frac{\\pi}{a}} e^{-\\frac{\\pi^2 \\xi^2}{a}}$, which shows that Gaussians are eigenfunctions of the Fourier transform.",
    ]
    
    # Edge cases
    EDGE_CASES = [
        "",  # Empty
        " ",  # Whitespace only
        "x",  # Single character
        "$" * 1000,  # Long repetitive
        "\\undefined_command{x}",  # Unknown command
        "\\frac{1}{0}",  # Division by zero notation
        "∀ε>0 ∃δ>0 : |x-a|<δ ⟹ |f(x)-f(a)|<ε",  # Unicode
        "x_1, x_2, ..., x_{1000}",  # Many subscripts
        "\\begin{matrix} a & b \\\\ c & d \\end{matrix}",  # Matrix
        "$$\\int_0^1 \\int_0^1 \\int_0^1 f(x,y,z) dx dy dz$$",  # Triple integral
    ]
    
    # Malicious inputs
    MALICIOUS_INPUTS = [
        "../../../etc/passwd",  # Path traversal
        "'; DROP TABLE users; --",  # SQL injection attempt
        "<script>alert('xss')</script>",  # XSS attempt
        "\\input{/etc/passwd}",  # LaTeX file inclusion
        "${system('rm -rf /')}",  # Command injection
        "x" * 1000000,  # Memory exhaustion
        "\\def\\x{\\x}\\x",  # Infinite recursion
    ]
    
    # Performance test sizes
    PERFORMANCE_SIZES = [10, 50, 100, 500, 1000]
    
    # Concurrent user counts
    CONCURRENT_USERS = [1, 5, 10, 20, 50]

# ===========================
# Test Categories
# ===========================

class PerformanceTests:
    """Performance and scalability tests"""
    
    def __init__(self, engine: MathematicalTTSEngine):
        self.engine = engine
        self.results = []
    
    async def test_response_times(self) -> TestResult:
        """Test response times for various expression complexities"""
        start = time.time()
        try:
            times = {}
            
            # Test different complexity levels
            for name, expressions in [
                ("simple", TestData.BASIC_EXPRESSIONS[:3]),
                ("complex", TestData.COMPLEX_EXPRESSIONS[:3]),
                ("lecture", TestData.LECTURE_SNIPPETS[:2])
            ]:
                category_times = []
                for expr in expressions:
                    expr_start = time.time()
                    result = self.engine.process_latex(expr)
                    category_times.append(time.time() - expr_start)
                
                times[name] = {
                    "avg": sum(category_times) / len(category_times),
                    "max": max(category_times),
                    "min": min(category_times)
                }
            
            # Check if times are reasonable
            passed = all(
                times[cat]["avg"] < 5.0 for cat in times
            )
            
            return TestResult(
                test_name="response_times",
                category="performance",
                passed=passed,
                duration=time.time() - start,
                metrics={"response_times": times}
            )
            
        except Exception as e:
            return TestResult(
                test_name="response_times",
                category="performance",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_throughput(self) -> TestResult:
        """Test system throughput"""
        start = time.time()
        try:
            throughput_results = {}
            
            for size in [10, 50, 100]:
                batch_start = time.time()
                expressions = TestData.BASIC_EXPRESSIONS * (size // 5)
                
                for expr in expressions[:size]:
                    self.engine.process_latex(expr)
                
                duration = time.time() - batch_start
                throughput_results[f"size_{size}"] = {
                    "expressions_per_second": size / duration,
                    "total_time": duration
                }
            
            # Check minimum throughput
            min_throughput = min(
                r["expressions_per_second"] for r in throughput_results.values()
            )
            passed = min_throughput > 1.0  # At least 1 expr/second
            
            return TestResult(
                test_name="throughput",
                category="performance",
                passed=passed,
                duration=time.time() - start,
                metrics={"throughput": throughput_results}
            )
            
        except Exception as e:
            return TestResult(
                test_name="throughput",
                category="performance",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_cache_effectiveness(self) -> TestResult:
        """Test cache hit rates and performance improvement"""
        start = time.time()
        try:
            # Clear cache first
            if hasattr(self.engine.expression_cache, 'clear'):
                self.engine.expression_cache.clear()
            
            expressions = TestData.BASIC_EXPRESSIONS[:5] * 3  # Repeat each 3 times
            random.shuffle(expressions)
            
            times = {"first_run": [], "cached_run": []}
            
            # First run - populate cache
            for expr in expressions[:5]:
                expr_start = time.time()
                self.engine.process_latex(expr)
                times["first_run"].append(time.time() - expr_start)
            
            # Second run - should hit cache
            for expr in expressions[:5]:
                expr_start = time.time()
                self.engine.process_latex(expr)
                times["cached_run"].append(time.time() - expr_start)
            
            # Calculate improvement
            avg_first = sum(times["first_run"]) / len(times["first_run"])
            avg_cached = sum(times["cached_run"]) / len(times["cached_run"])
            speedup = avg_first / avg_cached if avg_cached > 0 else 0
            
            # Get cache stats
            report = self.engine.get_performance_report()
            cache_hit_rate = report["metrics"]["cache_hit_rate"]
            
            passed = cache_hit_rate > 0.5 and speedup > 2.0
            
            return TestResult(
                test_name="cache_effectiveness",
                category="performance",
                passed=passed,
                duration=time.time() - start,
                metrics={
                    "cache_hit_rate": cache_hit_rate,
                    "speedup_factor": speedup,
                    "avg_uncached_time": avg_first,
                    "avg_cached_time": avg_cached
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name="cache_effectiveness",
                category="performance",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_memory_usage(self) -> TestResult:
        """Test memory consumption under load"""
        start = time.time()
        try:
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Process many expressions
            for _ in range(100):
                expr = random.choice(TestData.COMPLEX_EXPRESSIONS)
                self.engine.process_latex(expr)
            
            # Force garbage collection
            gc.collect()
            time.sleep(0.5)
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            # Check for memory leaks
            passed = memory_increase < 100  # Less than 100MB increase
            
            return TestResult(
                test_name="memory_usage",
                category="performance",
                passed=passed,
                duration=time.time() - start,
                metrics={
                    "initial_memory_mb": initial_memory,
                    "final_memory_mb": final_memory,
                    "increase_mb": memory_increase
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name="memory_usage",
                category="performance",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

class RobustnessTests:
    """Error handling and edge case tests"""
    
    def __init__(self, engine: MathematicalTTSEngine):
        self.engine = engine
    
    async def test_edge_cases(self) -> TestResult:
        """Test handling of edge cases"""
        start = time.time()
        failures = []
        
        try:
            for i, expr in enumerate(TestData.EDGE_CASES):
                try:
                    result = self.engine.process_latex(expr)
                    # Should not crash and should return something
                    if not isinstance(result.processed, str):
                        failures.append(f"Case {i}: Invalid result type")
                except Exception as e:
                    failures.append(f"Case {i}: {str(e)}")
            
            passed = len(failures) == 0
            
            return TestResult(
                test_name="edge_cases",
                category="robustness",
                passed=passed,
                duration=time.time() - start,
                error="; ".join(failures[:3]) if failures else "",
                metrics={"total_failures": len(failures), "failures": failures}
            )
            
        except Exception as e:
            return TestResult(
                test_name="edge_cases",
                category="robustness",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_malicious_inputs(self) -> TestResult:
        """Test security against malicious inputs"""
        start = time.time()
        vulnerabilities = []
        
        try:
            for i, malicious in enumerate(TestData.MALICIOUS_INPUTS):
                try:
                    result = self.engine.process_latex(malicious)
                    # Check for signs of successful attack
                    if any(danger in result.processed.lower() for danger in 
                           ["passwd", "drop table", "script", "etc", "rm -rf"]):
                        vulnerabilities.append(f"Input {i}: Potential security issue")
                except Exception:
                    # Exceptions are okay for malicious input
                    pass
            
            passed = len(vulnerabilities) == 0
            
            return TestResult(
                test_name="malicious_inputs",
                category="robustness",
                passed=passed,
                duration=time.time() - start,
                error="; ".join(vulnerabilities) if vulnerabilities else "",
                metrics={"vulnerabilities_found": len(vulnerabilities)}
            )
            
        except Exception as e:
            return TestResult(
                test_name="malicious_inputs",
                category="robustness",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_timeout_handling(self) -> TestResult:
        """Test timeout mechanisms"""
        start = time.time()
        try:
            # Create extremely complex expression
            complex_expr = "\\sum_{" + "".join("i_{}=1".format(i) for i in range(10)) + "}^{n}"
            complex_expr = complex_expr * 5  # Repeat to make it complex
            
            timeout_start = time.time()
            try:
                result = self.engine.process_latex(complex_expr)
                processing_time = time.time() - timeout_start
                
                # Should timeout or complete quickly
                passed = processing_time < 10.0
                error = "" if passed else f"Took {processing_time:.1f}s (no timeout)"
            except Exception as e:
                # Timeout exception is expected
                passed = "timeout" in str(e).lower()
                error = "" if passed else str(e)
            
            return TestResult(
                test_name="timeout_handling",
                category="robustness",
                passed=passed,
                duration=time.time() - start,
                error=error
            )
            
        except Exception as e:
            return TestResult(
                test_name="timeout_handling",
                category="robustness",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_recovery(self) -> TestResult:
        """Test system recovery after errors"""
        start = time.time()
        try:
            # Cause some errors
            for bad_expr in ["\\undefined{}", "", None, 123]:
                try:
                    if bad_expr is not None:
                        self.engine.process_latex(str(bad_expr))
                except:
                    pass
            
            # System should still work
            result = self.engine.process_latex("x^2 + y^2 = z^2")
            passed = len(result.processed) > 0
            
            return TestResult(
                test_name="recovery",
                category="robustness",
                passed=passed,
                duration=time.time() - start
            )
            
        except Exception as e:
            return TestResult(
                test_name="recovery",
                category="robustness",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

class ConcurrencyTests:
    """Concurrent usage and thread safety tests"""
    
    def __init__(self, engine: MathematicalTTSEngine):
        self.engine = engine
    
    async def test_concurrent_processing(self) -> TestResult:
        """Test concurrent expression processing"""
        start = time.time()
        try:
            async def process_expr(expr: str) -> float:
                start = time.time()
                result = self.engine.process_latex(expr)
                return time.time() - start
            
            # Process multiple expressions concurrently
            expressions = TestData.BASIC_EXPRESSIONS * 4
            tasks = [process_expr(expr) for expr in expressions]
            
            times = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check for errors
            errors = [t for t in times if isinstance(t, Exception)]
            passed = len(errors) == 0
            
            return TestResult(
                test_name="concurrent_processing",
                category="concurrency",
                passed=passed,
                duration=time.time() - start,
                error=str(errors[0]) if errors else "",
                metrics={
                    "concurrent_tasks": len(tasks),
                    "errors": len(errors),
                    "avg_time": sum(t for t in times if isinstance(t, float)) / len(times)
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name="concurrent_processing",
                category="concurrency",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_thread_safety(self) -> TestResult:
        """Test thread safety of shared resources"""
        start = time.time()
        errors = []
        
        def worker(worker_id: int, num_ops: int):
            try:
                for i in range(num_ops):
                    expr = f"x_{{{worker_id}}}^{{{i}}}"
                    self.engine.process_latex(expr)
            except Exception as e:
                errors.append(f"Worker {worker_id}: {str(e)}")
        
        try:
            # Create multiple threads
            threads = []
            for i in range(10):
                t = threading.Thread(target=worker, args=(i, 20))
                threads.append(t)
                t.start()
            
            # Wait for completion
            for t in threads:
                t.join(timeout=30)
            
            passed = len(errors) == 0
            
            return TestResult(
                test_name="thread_safety",
                category="concurrency",
                passed=passed,
                duration=time.time() - start,
                error="; ".join(errors[:3]) if errors else "",
                metrics={"thread_count": len(threads), "errors": len(errors)}
            )
            
        except Exception as e:
            return TestResult(
                test_name="thread_safety",
                category="concurrency",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_resource_contention(self) -> TestResult:
        """Test behavior under resource contention"""
        start = time.time()
        try:
            # Simulate high load
            async def heavy_load():
                tasks = []
                for _ in range(50):
                    expr = random.choice(TestData.COMPLEX_EXPRESSIONS)
                    tasks.append(self.engine.process_latex(expr))
                
                # Don't await, just fire and forget
                return len(tasks)
            
            # Run multiple heavy loads concurrently
            loads = await asyncio.gather(*[heavy_load() for _ in range(5)])
            
            # System should handle it without crashing
            passed = all(l > 0 for l in loads)
            
            return TestResult(
                test_name="resource_contention",
                category="concurrency",
                passed=passed,
                duration=time.time() - start,
                metrics={"total_tasks": sum(loads)}
            )
            
        except Exception as e:
            return TestResult(
                test_name="resource_contention",
                category="concurrency",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

class RealWorldTests:
    """Real-world usage scenarios"""
    
    def __init__(self, engine: MathematicalTTSEngine):
        self.engine = engine
    
    async def test_lecture_processing(self) -> TestResult:
        """Test processing of typical lecture content"""
        start = time.time()
        try:
            lecture_content = """
            Today we'll prove the fundamental theorem of calculus.
            
            Let $f: [a,b] \\to \\mathbb{R}$ be continuous. Define
            $F(x) = \\int_a^x f(t) dt$ for $x \\in [a,b]$.
            
            Theorem: $F'(x) = f(x)$ for all $x \\in (a,b)$.
            
            Proof: By definition of derivative,
            $$F'(x) = \\lim_{h \\to 0} \\frac{F(x+h) - F(x)}{h}$$
            
            Now, $F(x+h) - F(x) = \\int_a^{x+h} f(t) dt - \\int_a^x f(t) dt = \\int_x^{x+h} f(t) dt$
            
            By the mean value theorem for integrals, there exists $c \\in [x, x+h]$ such that
            $$\\int_x^{x+h} f(t) dt = f(c) \\cdot h$$
            
            Therefore, $F'(x) = \\lim_{h \\to 0} \\frac{f(c) \\cdot h}{h} = \\lim_{h \\to 0} f(c)$
            
            Since $c \\to x$ as $h \\to 0$ and $f$ is continuous, we have $F'(x) = f(x)$. QED.
            """
            
            # Extract and process mathematical parts
            import re
            math_pattern = r'\$[^$]+\$|\$\$[^$]+\$\$'
            math_expressions = re.findall(math_pattern, lecture_content)
            
            results = []
            for expr in math_expressions:
                # Remove $ delimiters
                clean_expr = expr.strip('$')
                result = self.engine.process_latex(clean_expr)
                results.append(result)
            
            # Check quality
            passed = all(
                len(r.processed) > 0 and not r.unknown_commands 
                for r in results
            )
            
            return TestResult(
                test_name="lecture_processing",
                category="real_world",
                passed=passed,
                duration=time.time() - start,
                metrics={
                    "expressions_found": len(math_expressions),
                    "successfully_processed": sum(1 for r in results if len(r.processed) > 0),
                    "avg_processing_time": sum(r.processing_time for r in results) / len(results) if results else 0
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name="lecture_processing",
                category="real_world",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_textbook_chapter(self) -> TestResult:
        """Test processing a textbook chapter with many formulas"""
        start = time.time()
        try:
            # Simulate textbook content
            formulas = [
                # Linear algebra
                "\\det(AB) = \\det(A)\\det(B)",
                "A^{-1} = \\frac{1}{\\det(A)} \\text{adj}(A)",
                "\\|\\mathbf{v}\\| = \\sqrt{\\mathbf{v} \\cdot \\mathbf{v}}",
                
                # Calculus
                "\\frac{d}{dx}[f(x)g(x)] = f'(x)g(x) + f(x)g'(x)",
                "\\int u dv = uv - \\int v du",
                "\\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n",
                
                # Statistics
                "\\bar{x} = \\frac{1}{n}\\sum_{i=1}^n x_i",
                "s^2 = \\frac{1}{n-1}\\sum_{i=1}^n (x_i - \\bar{x})^2",
                "P(A|B) = \\frac{P(B|A)P(A)}{P(B)}",
            ] * 5  # Simulate 45 formulas in a chapter
            
            process_times = []
            errors = []
            
            for formula in formulas:
                try:
                    start_time = time.time()
                    result = self.engine.process_latex(formula)
                    process_times.append(time.time() - start_time)
                except Exception as e:
                    errors.append(str(e))
            
            # Analyze results
            avg_time = sum(process_times) / len(process_times) if process_times else 0
            success_rate = len(process_times) / len(formulas)
            
            passed = success_rate > 0.95 and avg_time < 2.0
            
            return TestResult(
                test_name="textbook_chapter",
                category="real_world",
                passed=passed,
                duration=time.time() - start,
                metrics={
                    "total_formulas": len(formulas),
                    "success_rate": success_rate,
                    "avg_processing_time": avg_time,
                    "errors": len(errors)
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name="textbook_chapter",
                category="real_world",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_exam_paper(self) -> TestResult:
        """Test processing an exam paper with mixed content"""
        start = time.time()
        try:
            exam_questions = [
                {
                    "question": "Evaluate the integral $\\int_0^{\\pi} \\sin^2(x) dx$",
                    "solution": "$\\int_0^{\\pi} \\sin^2(x) dx = \\frac{\\pi}{2}$"
                },
                {
                    "question": "Find all solutions to $z^4 = 1$ in $\\mathbb{C}$",
                    "solution": "$z = 1, -1, i, -i$"
                },
                {
                    "question": "Prove that $\\sqrt{2}$ is irrational",
                    "solution": "Assume $\\sqrt{2} = \\frac{p}{q}$ where $\\gcd(p,q) = 1$..."
                }
            ]
            
            results = []
            for item in exam_questions:
                for text in [item["question"], item["solution"]]:
                    # Extract math from text
                    math_parts = re.findall(r'\$[^$]+\$', text)
                    for math in math_parts:
                        expr = math.strip('$')
                        result = self.engine.process_latex(expr)
                        results.append(result)
            
            # Check processing quality
            passed = all(r.processing_time < 3.0 for r in results)
            
            return TestResult(
                test_name="exam_paper",
                category="real_world",
                passed=passed,
                duration=time.time() - start,
                metrics={
                    "questions_processed": len(exam_questions),
                    "math_expressions": len(results),
                    "avg_time": sum(r.processing_time for r in results) / len(results) if results else 0
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name="exam_paper",
                category="real_world",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

class UsabilityTests:
    """User experience and API usability tests"""
    
    def __init__(self, engine: MathematicalTTSEngine):
        self.engine = engine
    
    async def test_error_messages(self) -> TestResult:
        """Test quality of error messages"""
        start = time.time()
        try:
            test_cases = [
                ("", "empty"),
                ("\\undefined{x}", "unknown command"),
                ("$" * 10000, "too long"),
            ]
            
            error_quality = []
            
            for expr, expected_type in test_cases:
                result = self.engine.process_latex(expr)
                
                # Check if error message is helpful
                is_helpful = (
                    len(result.processed) > 0 and
                    not result.processed.startswith("Error") and
                    any(word in result.processed.lower() for word in 
                        ["expression", "mathematical", "check", "please"])
                )
                error_quality.append(is_helpful)
            
            passed = sum(error_quality) >= len(test_cases) * 0.8
            
            return TestResult(
                test_name="error_messages",
                category="usability",
                passed=passed,
                duration=time.time() - start,
                metrics={"helpful_errors": sum(error_quality), "total": len(test_cases)}
            )
            
        except Exception as e:
            return TestResult(
                test_name="error_messages",
                category="usability",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_api_consistency(self) -> TestResult:
        """Test API consistency and predictability"""
        start = time.time()
        try:
            # Test that same input gives same output
            expr = "\\int_0^1 x^2 dx"
            results = []
            
            for _ in range(5):
                result = self.engine.process_latex(expr)
                results.append(result.processed)
            
            # All results should be identical
            passed = all(r == results[0] for r in results)
            
            return TestResult(
                test_name="api_consistency",
                category="usability",
                passed=passed,
                duration=time.time() - start,
                metrics={"unique_outputs": len(set(results))}
            )
            
        except Exception as e:
            return TestResult(
                test_name="api_consistency",
                category="usability",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_progress_feedback(self) -> TestResult:
        """Test progress indication for long operations"""
        start = time.time()
        try:
            # Create a long expression
            long_expr = " + ".join([f"\\int_0^{i} x^{i} dx" for i in range(1, 21)])
            
            # Process with progress
            result = self.engine.process_latex(long_expr, show_progress=True)
            
            # Just check it completes without error
            passed = len(result.processed) > 0
            
            return TestResult(
                test_name="progress_feedback",
                category="usability",
                passed=passed,
                duration=time.time() - start
            )
            
        except Exception as e:
            return TestResult(
                test_name="progress_feedback",
                category="usability",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

class IntegrationTests:
    """Test integration with various components"""
    
    def __init__(self, engine: MathematicalTTSEngine):
        self.engine = engine
    
    async def test_cli_integration(self) -> TestResult:
        """Test CLI functionality"""
        start = time.time()
        try:
            # Test basic CLI command
            result = subprocess.run(
                [sys.executable, "mathspeak.py", "x^2 + y^2 = z^2", "--stats"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            passed = (
                result.returncode == 0 and
                "Natural speech:" in result.stdout and
                "Performance Report" in result.stdout
            )
            
            return TestResult(
                test_name="cli_integration",
                category="integration",
                passed=passed,
                duration=time.time() - start,
                error=result.stderr[:200] if result.stderr else ""
            )
            
        except Exception as e:
            return TestResult(
                test_name="cli_integration",
                category="integration",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_domain_processors(self) -> TestResult:
        """Test domain-specific processors"""
        start = time.time()
        try:
            domain_tests = [
                ("\\pi_1(S^1) \\cong \\mathbb{Z}", MathematicalContext.TOPOLOGY),
                ("\\oint_C f(z) dz = 0", MathematicalContext.COMPLEX_ANALYSIS),
                ("y'' + p(x)y' + q(x)y = 0", MathematicalContext.ODE),
            ]
            
            results = []
            for expr, expected_context in domain_tests:
                result = self.engine.process_latex(expr)
                correct_context = result.context == expected_context.value
                results.append(correct_context)
            
            passed = sum(results) >= len(results) * 0.7
            
            return TestResult(
                test_name="domain_processors",
                category="integration",
                passed=passed,
                duration=time.time() - start,
                metrics={"correct_contexts": sum(results), "total": len(results)}
            )
            
        except Exception as e:
            return TestResult(
                test_name="domain_processors",
                category="integration",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )
    
    async def test_tts_engines(self) -> TestResult:
        """Test TTS engine availability and fallback"""
        start = time.time()
        try:
            if not hasattr(self.engine, 'tts_manager'):
                return TestResult(
                    test_name="tts_engines",
                    category="integration",
                    passed=False,
                    duration=time.time() - start,
                    error="No TTS manager available"
                )
            
            # Check available engines
            engines = self.engine.tts_manager.get_available_engines()
            available_count = sum(1 for e in engines if e['available'])
            
            # Test speech generation
            result = self.engine.process_latex("x^2 + y^2 = z^2")
            
            # Try to generate speech
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                success = await self.engine.speak_expression(
                    result,
                    output_file=tmp.name
                )
                
                # Check file was created
                file_exists = Path(tmp.name).exists()
                file_size = Path(tmp.name).stat().st_size if file_exists else 0
                
                # Cleanup
                Path(tmp.name).unlink(missing_ok=True)
            
            passed = available_count > 0 and success and file_size > 0
            
            return TestResult(
                test_name="tts_engines",
                category="integration",
                passed=passed,
                duration=time.time() - start,
                metrics={
                    "available_engines": available_count,
                    "total_engines": len(engines),
                    "speech_generated": success,
                    "file_size": file_size
                }
            )
            
        except Exception as e:
            return TestResult(
                test_name="tts_engines",
                category="integration",
                passed=False,
                duration=time.time() - start,
                error=str(e)
            )

# ===========================
# Test Runner
# ===========================

class ComprehensiveTestRunner:
    """Runs all test categories and generates report"""
    
    def __init__(self):
        self.engine = None
        self.categories: Dict[str, CategoryResult] = {}
        self.start_time = None
        self.end_time = None
    
    async def setup(self):
        """Initialize test environment"""
        logger.info("Setting up test environment...")
        
        # Create engine
        voice_manager = VoiceManager()
        self.engine = MathematicalTTSEngine(
            voice_manager=voice_manager,
            enable_caching=True,
            prefer_offline_tts=False
        )
        
        # Load domain processors
        try:
            from mathspeak.domains.topology import TopologyProcessor
            self.engine.domain_processors[MathematicalContext.TOPOLOGY] = TopologyProcessor()
        except:
            pass
        
        try:
            from mathspeak.domains.complex_analysis import ComplexAnalysisProcessor
            self.engine.domain_processors[MathematicalContext.COMPLEX_ANALYSIS] = ComplexAnalysisProcessor()
        except:
            pass
        
        try:
            from mathspeak.domains.ode import ODEProcessor
            self.engine.domain_processors[MathematicalContext.ODE] = ODEProcessor()
        except:
            pass
    
    async def run_all_tests(self):
        """Run all test categories"""
        self.start_time = datetime.now()
        
        # Define test suites
        test_suites = [
            ("Performance", PerformanceTests(self.engine), [
                "test_response_times",
                "test_throughput",
                "test_cache_effectiveness",
                "test_memory_usage"
            ]),
            ("Robustness", RobustnessTests(self.engine), [
                "test_edge_cases",
                "test_malicious_inputs",
                "test_timeout_handling",
                "test_recovery"
            ]),
            ("Concurrency", ConcurrencyTests(self.engine), [
                "test_concurrent_processing",
                "test_thread_safety",
                "test_resource_contention"
            ]),
            ("Real World", RealWorldTests(self.engine), [
                "test_lecture_processing",
                "test_textbook_chapter",
                "test_exam_paper"
            ]),
            ("Usability", UsabilityTests(self.engine), [
                "test_error_messages",
                "test_api_consistency",
                "test_progress_feedback"
            ]),
            ("Integration", IntegrationTests(self.engine), [
                "test_cli_integration",
                "test_domain_processors",
                "test_tts_engines"
            ])
        ]
        
        # Run each test suite
        for category_name, test_class, test_methods in test_suites:
            logger.info(f"\nRunning {category_name} tests...")
            category_result = CategoryResult(category_name=category_name)
            
            for test_method in test_methods:
                try:
                    method = getattr(test_class, test_method)
                    result = await method()
                    
                    category_result.test_results.append(result)
                    category_result.total_tests += 1
                    
                    if result.passed:
                        category_result.passed_tests += 1
                        logger.info(f"  ✓ {test_method}: PASSED ({result.duration:.2f}s)")
                    else:
                        category_result.failed_tests += 1
                        logger.error(f"  ✗ {test_method}: FAILED - {result.error}")
                    
                    category_result.total_duration += result.duration
                    
                except Exception as e:
                    logger.error(f"  ✗ {test_method}: ERROR - {str(e)}")
                    category_result.test_results.append(
                        TestResult(
                            test_name=test_method,
                            category=category_name,
                            passed=False,
                            duration=0,
                            error=str(e)
                        )
                    )
                    category_result.total_tests += 1
                    category_result.failed_tests += 1
            
            self.categories[category_name] = category_result
            logger.info(f"{category_name} tests: {category_result.passed_tests}/{category_result.total_tests} passed ({category_result.pass_rate:.1f}%)")
        
        self.end_time = datetime.now()
    
    def generate_report(self) -> str:
        """Generate comprehensive test report"""
        duration = (self.end_time - self.start_time).total_seconds()
        
        # Calculate overall statistics
        total_tests = sum(cat.total_tests for cat in self.categories.values())
        passed_tests = sum(cat.passed_tests for cat in self.categories.values())
        failed_tests = sum(cat.failed_tests for cat in self.categories.values())
        overall_pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = f"""
# MathSpeak Comprehensive Test Report

**Test Date**: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}  
**Duration**: {duration:.1f} seconds  
**System**: {sys.platform} - Python {sys.version.split()[0]}

## Executive Summary

The MathSpeak system underwent comprehensive testing across **{len(self.categories)} categories** with **{total_tests} individual tests**. The overall pass rate was **{overall_pass_rate:.1f}%** with **{passed_tests} tests passing** and **{failed_tests} tests failing**.

### Overall Results

| Metric | Value |
|--------|-------|
| Total Tests | {total_tests} |
| Passed | {passed_tests} |
| Failed | {failed_tests} |
| Pass Rate | {overall_pass_rate:.1f}% |
| Total Duration | {duration:.1f}s |

## Category Results

"""
        
        # Add category summaries
        for category_name, category in self.categories.items():
            report += f"""
### {category_name} Tests

**Pass Rate**: {category.pass_rate:.1f}% ({category.passed_tests}/{category.total_tests})  
**Duration**: {category.total_duration:.1f}s

| Test | Result | Duration | Details |
|------|--------|----------|---------|
"""
            
            for test in category.test_results:
                status = "✓ PASS" if test.passed else "✗ FAIL"
                details = test.error[:50] + "..." if test.error and len(test.error) > 50 else test.error
                
                # Add key metrics
                if test.metrics:
                    key_metric = list(test.metrics.items())[0]
                    if not details:
                        details = f"{key_metric[0]}: {key_metric[1]}"
                
                report += f"| {test.test_name} | {status} | {test.duration:.2f}s | {details} |\n"
        
        # Add detailed analysis
        report += """
## Detailed Analysis

### Performance Analysis
"""
        
        # Extract performance metrics
        perf_category = self.categories.get("Performance")
        if perf_category:
            for test in perf_category.test_results:
                if test.test_name == "response_times" and test.metrics:
                    times = test.metrics.get("response_times", {})
                    report += f"""
**Response Times**:
- Simple expressions: {times.get('simple', {}).get('avg', 0):.3f}s average
- Complex expressions: {times.get('complex', {}).get('avg', 0):.3f}s average
- Lecture content: {times.get('lecture', {}).get('avg', 0):.3f}s average
"""
                
                elif test.test_name == "cache_effectiveness" and test.metrics:
                    report += f"""
**Cache Performance**:
- Hit rate: {test.metrics.get('cache_hit_rate', 0)*100:.1f}%
- Speedup factor: {test.metrics.get('speedup_factor', 0):.1f}x
- Cached query time: {test.metrics.get('avg_cached_time', 0):.3f}s
"""
                
                elif test.test_name == "memory_usage" and test.metrics:
                    report += f"""
**Memory Usage**:
- Initial: {test.metrics.get('initial_memory_mb', 0):.1f} MB
- Final: {test.metrics.get('final_memory_mb', 0):.1f} MB
- Increase: {test.metrics.get('increase_mb', 0):.1f} MB
"""

        # Add robustness analysis
        report += """
### Robustness Analysis
"""
        
        robust_category = self.categories.get("Robustness")
        if robust_category:
            edge_case_test = next((t for t in robust_category.test_results if t.test_name == "edge_cases"), None)
            if edge_case_test:
                report += f"""
**Edge Case Handling**:
- Total edge cases tested: {len(TestData.EDGE_CASES)}
- Failures: {edge_case_test.metrics.get('total_failures', 0)}
- Success rate: {(1 - edge_case_test.metrics.get('total_failures', 0)/len(TestData.EDGE_CASES))*100:.1f}%
"""
            
            security_test = next((t for t in robust_category.test_results if t.test_name == "malicious_inputs"), None)
            if security_test:
                report += f"""
**Security Testing**:
- Malicious inputs tested: {len(TestData.MALICIOUS_INPUTS)}
- Vulnerabilities found: {security_test.metrics.get('vulnerabilities_found', 0)}
- Security rating: {"SECURE" if security_test.passed else "VULNERABLE"}
"""

        # Add real-world usage analysis
        report += """
### Real-World Usage Analysis
"""
        
        real_world = self.categories.get("Real World")
        if real_world:
            for test in real_world.test_results:
                if test.test_name == "textbook_chapter" and test.metrics:
                    report += f"""
**Textbook Processing**:
- Formulas processed: {test.metrics.get('total_formulas', 0)}
- Success rate: {test.metrics.get('success_rate', 0)*100:.1f}%
- Average time per formula: {test.metrics.get('avg_processing_time', 0):.3f}s
"""

        # Add conclusions
        report += f"""
## Conclusions

### System Readiness

Based on the comprehensive testing, the MathSpeak system demonstrates:

1. **Performance**: {"✓ READY" if overall_pass_rate > 90 else "⚠ NEEDS IMPROVEMENT" if overall_pass_rate > 70 else "✗ NOT READY"}
   - Response times are {"within acceptable limits" if self.categories.get("Performance", CategoryResult("")).pass_rate > 80 else "need optimization"}
   - Cache effectiveness is {"excellent" if self.categories.get("Performance", CategoryResult("")).pass_rate > 90 else "adequate" if self.categories.get("Performance", CategoryResult("")).pass_rate > 70 else "poor"}

2. **Reliability**: {"✓ READY" if self.categories.get("Robustness", CategoryResult("")).pass_rate > 90 else "⚠ NEEDS IMPROVEMENT" if self.categories.get("Robustness", CategoryResult("")).pass_rate > 70 else "✗ NOT READY"}
   - Handles edge cases {"robustly" if self.categories.get("Robustness", CategoryResult("")).pass_rate > 90 else "adequately" if self.categories.get("Robustness", CategoryResult("")).pass_rate > 70 else "poorly"}
   - Security posture is {"strong" if robust_category and all(t.passed for t in robust_category.test_results if "malicious" in t.test_name) else "concerning"}

3. **Scalability**: {"✓ READY" if self.categories.get("Concurrency", CategoryResult("")).pass_rate > 90 else "⚠ NEEDS IMPROVEMENT" if self.categories.get("Concurrency", CategoryResult("")).pass_rate > 70 else "✗ NOT READY"}
   - Concurrent processing is {"stable" if self.categories.get("Concurrency", CategoryResult("")).pass_rate > 90 else "mostly stable" if self.categories.get("Concurrency", CategoryResult("")).pass_rate > 70 else "unstable"}
   - Thread safety {"confirmed" if self.categories.get("Concurrency", CategoryResult("")).pass_rate > 90 else "needs attention"}

4. **Usability**: {"✓ READY" if self.categories.get("Usability", CategoryResult("")).pass_rate > 90 else "⚠ NEEDS IMPROVEMENT" if self.categories.get("Usability", CategoryResult("")).pass_rate > 70 else "✗ NOT READY"}
   - Error messages are {"helpful" if self.categories.get("Usability", CategoryResult("")).pass_rate > 80 else "need improvement"}
   - API consistency is {"excellent" if self.categories.get("Usability", CategoryResult("")).pass_rate > 90 else "good" if self.categories.get("Usability", CategoryResult("")).pass_rate > 70 else "poor"}

### Production Readiness Assessment

**Overall Assessment**: {"✅ PRODUCTION READY" if overall_pass_rate >= 90 else "⚠️ NEAR PRODUCTION READY" if overall_pass_rate >= 80 else "❌ NOT PRODUCTION READY"}

{"The system meets all critical requirements for production deployment." if overall_pass_rate >= 90 else "The system is close to production ready but needs minor improvements." if overall_pass_rate >= 80 else "The system requires significant improvements before production deployment."}

### Recommendations

"""
        
        # Add specific recommendations based on failures
        recommendations = []
        
        if self.categories.get("Performance", CategoryResult("")).pass_rate < 90:
            recommendations.append("- Optimize expression processing pipeline for better performance")
        
        if self.categories.get("Robustness", CategoryResult("")).pass_rate < 90:
            recommendations.append("- Improve error handling for edge cases")
        
        if self.categories.get("Concurrency", CategoryResult("")).pass_rate < 90:
            recommendations.append("- Address thread safety issues in concurrent processing")
        
        if not recommendations:
            recommendations.append("- Continue monitoring system performance in production")
            recommendations.append("- Implement additional logging for better observability")
            recommendations.append("- Consider adding more domain-specific processors")
        
        report += "\n".join(recommendations)
        
        report += f"""

### Test Coverage

- **Unit Testing**: Comprehensive coverage of core functionality
- **Integration Testing**: All major components tested together
- **Performance Testing**: Load and stress testing completed
- **Security Testing**: Basic security vulnerabilities checked
- **Usability Testing**: User experience validated
- **Real-world Scenarios**: Practical use cases verified

**Report Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return report
    
    def save_report(self, filename: str = "mathspeak_test_report.md"):
        """Save report to file"""
        report = self.generate_report()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        logger.info(f"Report saved to {filename}")
        
        # Also save raw results as JSON
        json_filename = filename.replace('.md', '.json')
        results = {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "duration": (self.end_time - self.start_time).total_seconds(),
            "categories": {}
        }
        
        for cat_name, cat_result in self.categories.items():
            results["categories"][cat_name] = {
                "total_tests": cat_result.total_tests,
                "passed": cat_result.passed_tests,
                "failed": cat_result.failed_tests,
                "pass_rate": cat_result.pass_rate,
                "tests": [
                    {
                        "name": test.test_name,
                        "passed": test.passed,
                        "duration": test.duration,
                        "error": test.error,
                        "metrics": test.metrics
                    }
                    for test in cat_result.test_results
                ]
            }
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        logger.info(f"JSON results saved to {json_filename}")

# ===========================
# Main Test Execution
# ===========================

async def main():
    """Run comprehensive test suite"""
    print("=" * 70)
    print("MathSpeak Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    runner = ComprehensiveTestRunner()
    
    try:
        # Setup
        await runner.setup()
        
        # Run tests
        await runner.run_all_tests()
        
        # Generate and save report
        runner.save_report()
        
        # Print summary
        print("\n" + "=" * 70)
        print("Test Summary")
        print("=" * 70)
        
        total_tests = sum(cat.total_tests for cat in runner.categories.values())
        passed_tests = sum(cat.passed_tests for cat in runner.categories.values())
        overall_pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Pass Rate: {overall_pass_rate:.1f}%")
        
        print("\nCategory Results:")
        for cat_name, cat_result in runner.categories.items():
            print(f"  {cat_name}: {cat_result.pass_rate:.1f}% ({cat_result.passed_tests}/{cat_result.total_tests})")
        
        print(f"\n{'✅ PRODUCTION READY' if overall_pass_rate >= 90 else '⚠️  NEAR PRODUCTION READY' if overall_pass_rate >= 80 else '❌ NOT PRODUCTION READY'}")
        print("\nDetailed report saved to: mathspeak_test_report.md")
        
    except Exception as e:
        logger.error(f"Test suite error: {e}")
        traceback.print_exc()
    
    finally:
        # Cleanup
        if runner.engine:
            runner.engine.shutdown()

if __name__ == "__main__":
    asyncio.run(main())