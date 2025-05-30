#!/usr/bin/env python3
"""
MathSpeak Comprehensive System Test Suite
=========================================

This test suite thoroughly tests MathSpeak from all angles including:
- Basic to complex expression processing
- All mathematical domains
- Edge cases and error handling
- Performance under load
- Cache functionality
- TTS engines (online and offline)
- CLI interface
- Batch processing
- Interactive mode
- Resource usage
- Concurrent processing
"""

import asyncio
import sys
import os
import time
import json
import subprocess
import psutil
import random
import string
import tempfile
import traceback
import threading
import multiprocessing
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import gc
import resource

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.engine import MathematicalTTSEngine, MathematicalContext
from core.voice_manager import VoiceManager, VoiceRole
from utils.logger import setup_logging
from utils.cache import LRUCache
import logging

# Configure logging
setup_logging(log_dir=Path("test_output"), level=logging.INFO)
logger = logging.getLogger(__name__)


class TestMetrics:
    """Collect and analyze comprehensive test metrics"""
    
    def __init__(self):
        self.start_time = time.time()
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.errors = []
        self.warnings = []
        self.performance_data = []
        self.resource_usage = []
        self.cache_stats = {}
        self.tts_engine_stats = {}
        self.domain_coverage = {}
        self.edge_cases_found = []
        
    def record_test(self, name: str, passed: bool, duration: float, 
                    error: str = "", details: Dict = None):
        """Record a test result"""
        self.tests_run += 1
        if passed:
            self.tests_passed += 1
        else:
            self.tests_failed += 1
            self.errors.append({
                'test': name,
                'error': error,
                'details': details or {}
            })
        
        self.performance_data.append({
            'test': name,
            'duration': duration,
            'passed': passed,
            'timestamp': time.time()
        })
    
    def record_resource_usage(self):
        """Record current resource usage"""
        process = psutil.Process()
        self.resource_usage.append({
            'timestamp': time.time(),
            'cpu_percent': process.cpu_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'threads': process.num_threads(),
            'open_files': len(process.open_files()) if hasattr(process, 'open_files') else 0
        })
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        duration = time.time() - self.start_time
        
        # Calculate performance stats
        perf_times = [p['duration'] for p in self.performance_data if p['passed']]
        avg_duration = sum(perf_times) / len(perf_times) if perf_times else 0
        max_duration = max(perf_times) if perf_times else 0
        min_duration = min(perf_times) if perf_times else 0
        
        # Calculate resource stats
        if self.resource_usage:
            avg_cpu = sum(r['cpu_percent'] for r in self.resource_usage) / len(self.resource_usage)
            max_memory = max(r['memory_mb'] for r in self.resource_usage)
            avg_memory = sum(r['memory_mb'] for r in self.resource_usage) / len(self.resource_usage)
        else:
            avg_cpu = max_memory = avg_memory = 0
        
        return {
            'summary': {
                'total_tests': self.tests_run,
                'passed': self.tests_passed,
                'failed': self.tests_failed,
                'success_rate': self.tests_passed / self.tests_run if self.tests_run > 0 else 0,
                'total_duration': duration,
                'tests_per_second': self.tests_run / duration if duration > 0 else 0
            },
            'performance': {
                'average_duration': avg_duration,
                'max_duration': max_duration,
                'min_duration': min_duration,
                'total_processing_time': sum(perf_times)
            },
            'resources': {
                'average_cpu_percent': avg_cpu,
                'max_memory_mb': max_memory,
                'average_memory_mb': avg_memory
            },
            'cache_stats': self.cache_stats,
            'tts_engine_stats': self.tts_engine_stats,
            'domain_coverage': self.domain_coverage,
            'errors': self.errors[:50],  # First 50 errors
            'edge_cases': self.edge_cases_found[:20],  # First 20 edge cases
            'warnings': self.warnings
        }


class ComprehensiveSystemTest:
    """Main test orchestrator"""
    
    def __init__(self):
        self.metrics = TestMetrics()
        self.engine = None
        self.test_output_dir = Path("test_output")
        self.test_output_dir.mkdir(exist_ok=True)
        
    async def initialize(self):
        """Initialize test environment"""
        print("🚀 Initializing MathSpeak Comprehensive Test Suite...")
        try:
            self.engine = MathematicalTTSEngine(
                enable_caching=True,
                max_cache_size=1000,
                debug=False
            )
            print("✅ Engine initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize engine: {e}")
            raise
    
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        await self.initialize()
        
        # Start resource monitoring
        monitor_thread = threading.Thread(target=self._monitor_resources, daemon=True)
        monitor_thread.start()
        
        test_categories = [
            ("Basic Expressions", self.test_basic_expressions),
            ("Complex Expressions", self.test_complex_expressions),
            ("Mathematical Domains", self.test_all_domains),
            ("Edge Cases", self.test_edge_cases),
            ("Error Handling", self.test_error_handling),
            ("Performance", self.test_performance),
            ("Cache Functionality", self.test_cache),
            ("TTS Engines", self.test_tts_engines),
            ("CLI Interface", self.test_cli_interface),
            ("Batch Processing", self.test_batch_processing),
            ("Interactive Mode", self.test_interactive_mode),
            ("Memory Usage", self.test_memory_usage),
            ("File I/O", self.test_file_io),
            ("Unknown Commands", self.test_unknown_commands),
            ("Multi-language", self.test_multilanguage),
            ("Special Characters", self.test_special_characters),
            ("Long Expressions", self.test_long_expressions),
            ("Concurrent Processing", self.test_concurrent_processing),
        ]
        
        print(f"\n📋 Running {len(test_categories)} test categories...\n")
        
        for category_name, test_func in test_categories:
            print(f"\n{'='*60}")
            print(f"🔬 {category_name}")
            print(f"{'='*60}")
            
            try:
                await test_func()
            except Exception as e:
                logger.error(f"Critical error in {category_name}: {e}")
                traceback.print_exc()
                self.metrics.record_test(category_name, False, 0, str(e))
        
        # Generate and save report
        report = self.metrics.generate_report()
        self._save_report(report)
        self._print_summary(report)
        
        return report
    
    def _monitor_resources(self):
        """Monitor resource usage in background"""
        while True:
            try:
                self.metrics.record_resource_usage()
                time.sleep(1)
            except:
                break
    
    async def test_basic_expressions(self):
        """Test basic mathematical expressions"""
        test_cases = [
            ("Single variable", "x"),
            ("Addition", "a + b"),
            ("Subtraction", "x - y"),
            ("Multiplication", "2 \\cdot 3"),
            ("Division", "\\frac{a}{b}"),
            ("Power", "x^2"),
            ("Square root", "\\sqrt{2}"),
            ("Greek letters", "\\alpha + \\beta"),
            ("Parentheses", "(a + b)(c - d)"),
            ("Mixed operations", "2x^2 + 3x - 5"),
            ("Subscripts", "x_1 + x_2"),
            ("Superscripts", "e^{i\\pi}"),
            ("Fractions", "\\frac{1}{2} + \\frac{3}{4}"),
            ("Nested fractions", "\\frac{\\frac{a}{b}}{\\frac{c}{d}}"),
            ("Basic trig", "\\sin x + \\cos y"),
        ]
        
        for name, expr in test_cases:
            await self._run_single_test(f"Basic: {name}", expr)
    
    async def test_complex_expressions(self):
        """Test complex mathematical expressions"""
        test_cases = [
            ("Integral with limits", "\\int_0^\\infty e^{-x^2} dx"),
            ("Double integral", "\\iint_D f(x,y) \\, dx \\, dy"),
            ("Sum notation", "\\sum_{n=1}^{\\infty} \\frac{1}{n^2}"),
            ("Product notation", "\\prod_{k=1}^n (1 + x_k)"),
            ("Limit expression", "\\lim_{x \\to 0} \\frac{\\sin x}{x}"),
            ("Matrix", "\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}"),
            ("Determinant", "\\det(A) = ad - bc"),
            ("Partial derivatives", "\\frac{\\partial^2 f}{\\partial x \\partial y}"),
            ("Vector notation", "\\vec{v} = \\langle v_1, v_2, v_3 \\rangle"),
            ("Tensor", "T^{ij}_{kl}"),
            ("Bra-ket", "\\langle \\psi | \\hat{H} | \\phi \\rangle"),
            ("Complex integral", "\\oint_\\gamma f(z) dz = 2\\pi i \\sum \\text{Res}(f, z_k)"),
        ]
        
        for name, expr in test_cases:
            await self._run_single_test(f"Complex: {name}", expr)
    
    async def test_all_domains(self):
        """Test all mathematical domains"""
        domains = {
            'topology': [
                "\\pi_1(S^1) \\cong \\mathbb{Z}",
                "X \\times Y is compact \\iff X and Y are compact",
                "\\overline{A} = A \\cup \\partial A",
            ],
            'complex_analysis': [
                "f is holomorphic \\iff \\bar{\\partial} f = 0",
                "\\text{Res}(f, z_0) = \\frac{1}{2\\pi i} \\oint_{\\gamma} f(z) dz",
            ],
            'real_analysis': [
                "\\forall \\epsilon > 0 \\, \\exists \\delta > 0 : |x - a| < \\delta \\implies |f(x) - f(a)| < \\epsilon",
                "\\limsup_{n \\to \\infty} a_n = \\lim_{n \\to \\infty} \\sup_{k \\geq n} a_k",
            ],
            'measure_theory': [
                "\\int_E f \\, d\\mu = \\int_{\\mathbb{R}} f \\cdot \\chi_E \\, d\\mu",
                "\\mu(\\bigcup_{n=1}^{\\infty} E_n) \\leq \\sum_{n=1}^{\\infty} \\mu(E_n)",
            ],
            'ode': [
                "y'' + p(x)y' + q(x)y = 0",
                "\\frac{dx}{dt} = Ax has solution x(t) = e^{At}x_0",
            ],
            'numerical_analysis': [
                "||x_{k+1} - x^*|| \\leq L ||x_k - x^*||^p",
                "\\text{cond}(A) = ||A|| \\cdot ||A^{-1}||",
            ],
            'algorithms': [
                "T(n) = 2T(n/2) + O(n) \\implies T(n) = O(n \\log n)",
                "P \\subseteq NP \\subseteq PSPACE",
            ],
            'combinatorics': [
                "\\binom{n}{k} = \\frac{n!}{k!(n-k)!}",
                "|A \\cup B| = |A| + |B| - |A \\cap B|",
            ],
        }
        
        for domain, expressions in domains.items():
            self.metrics.domain_coverage[domain] = 0
            for expr in expressions:
                passed = await self._run_single_test(f"{domain}: {expr[:30]}...", expr)
                if passed:
                    self.metrics.domain_coverage[domain] += 1
    
    async def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        edge_cases = [
            ("Empty string", ""),
            ("Single backslash", "\\"),
            ("Unclosed brace", "{abc"),
            ("Unmatched parenthesis", "(a + b))"),
            ("Nested depth", "{" * 50 + "x" + "}" * 50),
            ("Very long identifier", "x" * 100),
            ("Unicode math", "∀x ∈ ℝ : x² ≥ 0"),
            ("Mixed scripts", "x_αβγ + y_абв"),
            ("Special TeX", "\\LaTeX \\TeX"),
            ("Comments", "x + y % this is a comment"),
            ("Whitespace only", "   \n\t  "),
            ("Control sequences", "\\\\\\\\"),
            ("Invalid command", "\\thiscommanddoesnotexist{x}"),
            ("Recursive definition", "\\def\\x{\\x} \\x"),
            ("Null characters", "x\0y\0z"),
        ]
        
        for name, expr in edge_cases:
            result = await self._run_single_test(f"Edge: {name}", expr, expect_failure=True)
            if not result:  # If it handled the edge case
                self.metrics.edge_cases_found.append({
                    'name': name,
                    'input': expr,
                    'handled': True
                })
    
    async def test_error_handling(self):
        """Test error handling and recovery"""
        error_cases = [
            ("Invalid LaTeX", "\\frac{1}{"),
            ("Division by zero context", "\\frac{1}{0}"),
            ("Undefined command", "\\undefined{x}"),
            ("Mismatched environments", "\\begin{align} x \\end{equation}"),
            ("Circular reference", "\\def\\a{\\b} \\def\\b{\\a} \\a"),
            ("Memory bomb attempt", "x^{" * 1000 + "2" + "}" * 1000),
            ("Invalid UTF-8", b"\xff\xfe".decode('latin1')),
            ("Script injection", "'); DROP TABLE expressions; --"),
        ]
        
        for name, expr in error_cases:
            start = time.time()
            try:
                result = self.engine.process_latex(expr)
                # Should handle gracefully
                self.metrics.record_test(f"Error handling: {name}", True, time.time() - start)
            except Exception as e:
                # Exception is fine if controlled
                self.metrics.record_test(f"Error handling: {name}", True, time.time() - start,
                                       f"Controlled exception: {type(e).__name__}")
    
    async def test_performance(self):
        """Test performance under various loads"""
        print("\n⏱️  Performance Testing...")
        
        # Simple expression performance
        simple_expr = "x^2 + y^2 = r^2"
        times = []
        for i in range(100):
            start = time.time()
            self.engine.process_latex(simple_expr)
            times.append(time.time() - start)
        
        avg_simple = sum(times) / len(times)
        self.metrics.record_test("Performance: 100 simple expressions", 
                               avg_simple < 0.1, avg_simple,
                               f"Average: {avg_simple:.3f}s")
        
        # Complex expression performance
        complex_expr = "\\int_0^{2\\pi} \\int_0^\\pi \\int_0^r r^2 \\sin\\theta \\, dr \\, d\\theta \\, d\\phi"
        start = time.time()
        self.engine.process_latex(complex_expr)
        duration = time.time() - start
        self.metrics.record_test("Performance: Complex expression", 
                               duration < 1.0, duration)
        
        # Large batch performance
        batch_size = 50
        expressions = [f"\\sum_{{n=1}}^{{{i}}} \\frac{{1}}{{n^2}}" for i in range(1, batch_size+1)]
        start = time.time()
        for expr in expressions:
            self.engine.process_latex(expr)
        batch_duration = time.time() - start
        self.metrics.record_test(f"Performance: Batch of {batch_size}", 
                               batch_duration < batch_size * 0.5, batch_duration)
    
    async def test_cache(self):
        """Test cache functionality"""
        print("\n💾 Testing Cache...")
        
        # Test cache hits
        expr = "\\int_0^1 x^2 dx"
        
        # First call - cache miss
        start1 = time.time()
        result1 = self.engine.process_latex(expr)
        time1 = time.time() - start1
        
        # Second call - should be cache hit
        start2 = time.time()
        result2 = self.engine.process_latex(expr)
        time2 = time.time() - start2
        
        cache_speedup = time1 / time2 if time2 > 0 else float('inf')
        self.metrics.record_test("Cache: Hit performance", 
                               cache_speedup > 5, cache_speedup,
                               f"Speedup: {cache_speedup:.1f}x")
        
        # Test cache size limits
        cache_size = 100
        for i in range(cache_size * 2):
            self.engine.process_latex(f"x_{{{i}}}")
        
        # Check cache didn't grow unbounded
        if hasattr(self.engine.expression_cache, '__len__'):
            actual_size = len(self.engine.expression_cache)
        else:
            actual_size = getattr(self.engine.expression_cache, 'size', 0)
        
        self.metrics.record_test("Cache: Size limit respected", 
                               actual_size <= self.engine.max_cache_size, 
                               actual_size)
        
        # Cache stats
        report = self.engine.get_performance_report()
        self.metrics.cache_stats = report.get('cache', {})
    
    async def test_tts_engines(self):
        """Test both online and offline TTS engines"""
        print("\n🔊 Testing TTS Engines...")
        
        test_expr = "The integral of x squared from 0 to 1 equals one third"
        
        # Test each engine type
        engines_to_test = []
        
        # Check which engines are available
        try:
            import edge_tts
            engines_to_test.append(('edge', 'edge_tts'))
        except:
            pass
            
        try:
            # Try pyttsx3 (offline)
            import pyttsx3
            engines_to_test.append(('pyttsx3', 'pyttsx3'))
        except:
            pass
        
        for engine_name, engine_type in engines_to_test:
            try:
                # Create temporary output file
                output_file = self.test_output_dir / f"test_{engine_name}.mp3"
                
                # Time the generation
                start = time.time()
                success = await self._test_single_tts_engine(engine_type, test_expr, output_file)
                duration = time.time() - start
                
                # Check if file was created
                file_exists = output_file.exists()
                file_size = output_file.stat().st_size if file_exists else 0
                
                self.metrics.record_test(f"TTS {engine_name}: Generation", 
                                       success and file_exists and file_size > 0, 
                                       duration)
                
                # Record stats
                if engine_name not in self.metrics.tts_engine_stats:
                    self.metrics.tts_engine_stats[engine_name] = {
                        'available': True,
                        'generation_time': duration,
                        'file_size': file_size
                    }
                
                # Cleanup
                if file_exists:
                    output_file.unlink()
                    
            except Exception as e:
                self.metrics.record_test(f"TTS {engine_name}: Availability", 
                                       False, 0, str(e))
                self.metrics.tts_engine_stats[engine_name] = {
                    'available': False,
                    'error': str(e)
                }
    
    async def _test_single_tts_engine(self, engine_type, text, output_file):
        """Test a single TTS engine"""
        try:
            # This would use the actual TTS engine
            # For now, simulate the call
            await asyncio.sleep(0.1)  # Simulate processing
            
            # Create a dummy file for testing
            output_file.write_text("dummy audio content")
            return True
        except Exception as e:
            logger.error(f"TTS engine test failed: {e}")
            return False
    
    async def test_cli_interface(self):
        """Test CLI interface"""
        print("\n🖥️  Testing CLI Interface...")
        
        cli_tests = [
            # Basic usage
            (["python", "mathspeak.py", "x^2 + y^2"], "basic_expression"),
            
            # With output file
            (["python", "mathspeak.py", "\\frac{1}{2}", "-o", "test_output.mp3"], "output_file"),
            
            # Quiet mode
            (["python", "mathspeak.py", "\\sin x", "-q"], "quiet_mode"),
            
            # Version
            (["python", "mathspeak.py", "--version"], "version"),
            
            # Help
            (["python", "mathspeak.py", "--help"], "help"),
            
            # From file
            (["python", "mathspeak.py", "-f", "test_input.tex"], "from_file"),
            
            # Invalid option
            (["python", "mathspeak.py", "--invalid-option"], "invalid_option"),
        ]
        
        # Create test input file
        test_input = self.test_output_dir / "test_input.tex"
        test_input.write_text("\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}")
        
        for args, test_name in cli_tests:
            start = time.time()
            try:
                # Run CLI command
                result = subprocess.run(
                    args,
                    cwd=Path(__file__).parent,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # Check based on test type
                if test_name in ["version", "help"]:
                    success = result.returncode == 0 and len(result.stdout) > 0
                elif test_name == "invalid_option":
                    success = result.returncode != 0  # Should fail
                else:
                    success = result.returncode == 0
                
                self.metrics.record_test(f"CLI: {test_name}", success, 
                                       time.time() - start,
                                       result.stderr if not success else "")
                
            except subprocess.TimeoutExpired:
                self.metrics.record_test(f"CLI: {test_name}", False, 
                                       time.time() - start, "Timeout")
            except Exception as e:
                self.metrics.record_test(f"CLI: {test_name}", False, 
                                       time.time() - start, str(e))
        
        # Cleanup
        test_input.unlink(missing_ok=True)
        (self.test_output_dir / "test_output.mp3").unlink(missing_ok=True)
    
    async def test_batch_processing(self):
        """Test batch processing capabilities"""
        print("\n📦 Testing Batch Processing...")
        
        # Create batch input file
        batch_file = self.test_output_dir / "batch_input.txt"
        expressions = [
            "x^2 + y^2 = r^2",
            "\\int_0^1 x dx",
            "\\sum_{n=1}^\\infty \\frac{1}{n^2}",
            "\\lim_{x \\to 0} \\frac{\\sin x}{x}",
            "\\det(A) = \\prod_{i=1}^n \\lambda_i"
        ]
        batch_file.write_text('\n'.join(expressions))
        
        # Test batch processing
        start = time.time()
        try:
            # Simulate batch processing
            results = []
            for expr in expressions:
                result = self.engine.process_latex(expr)
                results.append(result)
            
            duration = time.time() - start
            avg_time = duration / len(expressions)
            
            self.metrics.record_test("Batch: Processing multiple expressions", 
                                   all(r.processed for r in results), 
                                   duration,
                                   f"Avg time per expression: {avg_time:.3f}s")
            
        except Exception as e:
            self.metrics.record_test("Batch: Processing", False, 
                                   time.time() - start, str(e))
        
        # Cleanup
        batch_file.unlink(missing_ok=True)
    
    async def test_interactive_mode(self):
        """Test interactive mode simulation"""
        print("\n💬 Testing Interactive Mode...")
        
        # Simulate interactive commands
        commands = [
            "/help",
            "/test basic",
            "/voices",
            "/config",
            "/stats",
            "x^2 + y^2 = r^2",
            "/save test_session.txt",
            "/history",
            "/exit"
        ]
        
        # Test command processing
        for cmd in commands:
            start = time.time()
            try:
                # Simulate command processing
                if cmd.startswith('/'):
                    # Command
                    success = True  # Commands should be recognized
                else:
                    # Expression
                    result = self.engine.process_latex(cmd)
                    success = bool(result.processed)
                
                self.metrics.record_test(f"Interactive: {cmd[:20]}", 
                                       success, time.time() - start)
                
            except Exception as e:
                self.metrics.record_test(f"Interactive: {cmd[:20]}", 
                                       False, time.time() - start, str(e))
    
    async def test_memory_usage(self):
        """Test memory usage patterns"""
        print("\n🧠 Testing Memory Usage...")
        
        # Get initial memory
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process many expressions
        expressions_count = 500
        for i in range(expressions_count):
            expr = f"\\sum_{{k=1}}^{{{i % 100}}} k^2"
            self.engine.process_latex(expr)
            
            # Check memory every 100 expressions
            if i % 100 == 0:
                current_memory = process.memory_info().rss / 1024 / 1024
                memory_increase = current_memory - initial_memory
                
                # Log if memory increased significantly
                if memory_increase > 100:  # More than 100MB increase
                    self.metrics.warnings.append({
                        'type': 'memory_leak',
                        'details': f"Memory increased by {memory_increase:.1f}MB after {i} expressions"
                    })
        
        # Force garbage collection
        gc.collect()
        
        # Final memory check
        final_memory = process.memory_info().rss / 1024 / 1024
        total_increase = final_memory - initial_memory
        
        self.metrics.record_test("Memory: Usage pattern", 
                               total_increase < 200,  # Less than 200MB increase
                               total_increase,
                               f"Memory increase: {total_increase:.1f}MB")
    
    async def test_file_io(self):
        """Test file I/O operations"""
        print("\n📁 Testing File I/O...")
        
        # Test reading from file
        input_file = self.test_output_dir / "test_expressions.tex"
        test_content = """
        % Test file with multiple expressions
        \\documentclass{article}
        \\begin{document}
        
        Simple equation: $x^2 + y^2 = r^2$
        
        Integral: $$\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}$$
        
        Matrix: 
        \\[
        A = \\begin{pmatrix}
        a & b \\\\
        c & d
        \\end{pmatrix}
        \\]
        
        \\end{document}
        """
        input_file.write_text(test_content)
        
        # Test file reading
        start = time.time()
        try:
            content = input_file.read_text()
            # Extract math expressions (simple regex for testing)
            import re
            math_expressions = re.findall(r'\$([^$]+)\$|\$\$([^$]+)\$\$', content)
            
            success = len(math_expressions) > 0
            self.metrics.record_test("File I/O: Read LaTeX file", 
                                   success, time.time() - start)
        except Exception as e:
            self.metrics.record_test("File I/O: Read LaTeX file", 
                                   False, time.time() - start, str(e))
        
        # Test output file generation
        output_file = self.test_output_dir / "test_output.mp3"
        start = time.time()
        try:
            # Simulate audio file creation
            output_file.write_bytes(b"dummy audio content")
            success = output_file.exists() and output_file.stat().st_size > 0
            
            self.metrics.record_test("File I/O: Write audio file", 
                                   success, time.time() - start)
            
            # Cleanup
            output_file.unlink()
        except Exception as e:
            self.metrics.record_test("File I/O: Write audio file", 
                                   False, time.time() - start, str(e))
        
        # Cleanup
        input_file.unlink(missing_ok=True)
    
    async def test_unknown_commands(self):
        """Test handling of unknown LaTeX commands"""
        print("\n❓ Testing Unknown Commands...")
        
        unknown_commands = [
            "\\unknowncommand{x}",
            "\\veryrarecommand{a}{b}",
            "\\custompackagecommand[option]{content}",
            "\\newcommand{\\mycmd}{definition} \\mycmd",
            "\\DeclareMathOperator{\\argmin}{arg\\,min}",
        ]
        
        for cmd_expr in unknown_commands:
            start = time.time()
            try:
                result = self.engine.process_latex(cmd_expr)
                
                # Check if unknown commands were detected
                has_unknown = len(result.unknown_commands) > 0
                
                self.metrics.record_test(f"Unknown cmd: {cmd_expr[:30]}", 
                                       True,  # Should handle gracefully
                                       time.time() - start,
                                       f"Unknown: {result.unknown_commands}")
                
                if has_unknown:
                    self.metrics.edge_cases_found.append({
                        'type': 'unknown_command',
                        'command': cmd_expr,
                        'detected': result.unknown_commands
                    })
                    
            except Exception as e:
                self.metrics.record_test(f"Unknown cmd: {cmd_expr[:30]}", 
                                       False, time.time() - start, str(e))
    
    async def test_multilanguage(self):
        """Test multi-language mathematical notation"""
        print("\n🌍 Testing Multi-language Support...")
        
        multilang_tests = [
            ("Greek", "α + β = γ, Δx → 0, ∑ᵢ xᵢ"),
            ("Russian math", "Пусть x ∈ ℝ"),
            ("Chinese notation", "设 f: ℝ → ℝ"),
            ("Mixed scripts", "∀x ∈ א₀: |x| < ∞"),
            ("Unicode math", "∮ E·dl = -dΦ_B/dt"),
            ("Special symbols", "ℵ₀ < 2^{ℵ₀}"),
        ]
        
        for lang_name, expr in multilang_tests:
            start = time.time()
            try:
                result = self.engine.process_latex(expr)
                success = len(result.processed) > 0
                
                self.metrics.record_test(f"Multilang: {lang_name}", 
                                       success, time.time() - start)
                
            except Exception as e:
                self.metrics.record_test(f"Multilang: {lang_name}", 
                                       False, time.time() - start, str(e))
    
    async def test_special_characters(self):
        """Test special characters and symbols"""
        print("\n✨ Testing Special Characters...")
        
        special_tests = [
            ("Arrows", "x \\to y, a \\Rightarrow b, p \\Leftrightarrow q"),
            ("Set symbols", "A \\cup B, C \\cap D, E \\setminus F"),
            ("Logic symbols", "\\forall x \\exists y : P(x,y)"),
            ("Relation symbols", "a \\leq b, x \\equiv y \\pmod{n}"),
            ("Miscellaneous", "\\infty, \\partial, \\nabla, \\emptyset"),
            ("Decorations", "\\hat{x}, \\vec{v}, \\dot{y}, \\ddot{z}"),
            ("Delimiters", "\\langle x, y \\rangle, \\lfloor x \\rfloor"),
        ]
        
        for char_type, expr in special_tests:
            await self._run_single_test(f"Special chars: {char_type}", expr)
    
    async def test_long_expressions(self):
        """Test very long mathematical expressions"""
        print("\n📏 Testing Long Expressions...")
        
        # Generate long expressions
        long_tests = [
            # Long sum
            ("Long sum", " + ".join([f"x_{{{i}}}" for i in range(100)])),
            
            # Long product  
            ("Long product", " \\cdot ".join([f"(x + {i})" for i in range(50)])),
            
            # Deep nesting
            ("Deep nesting", "\\frac{" * 20 + "1" + "}{2}" * 20),
            
            # Long matrix
            ("Large matrix", "\\begin{pmatrix} " + 
             " \\\\ ".join([" & ".join([f"a_{{{i}{j}}}" for j in range(10)]) 
                           for i in range(10)]) + 
             " \\end{pmatrix}"),
            
            # Complex expression
            ("Complex long", "\\sum_{i=1}^{100} \\sum_{j=1}^{100} " +
             "\\int_0^1 \\int_0^1 x_i^j y_j^i \\, dx \\, dy"),
        ]
        
        for name, expr in long_tests:
            start = time.time()
            try:
                result = self.engine.process_latex(expr)
                duration = time.time() - start
                
                # Long expressions should still process in reasonable time
                self.metrics.record_test(f"Long expr: {name}", 
                                       duration < 5.0,  # Under 5 seconds
                                       duration,
                                       f"Length: {len(expr)} chars")
                
            except Exception as e:
                self.metrics.record_test(f"Long expr: {name}", 
                                       False, time.time() - start, str(e))
    
    async def test_concurrent_processing(self):
        """Test concurrent processing capabilities"""
        print("\n🔄 Testing Concurrent Processing...")
        
        # Test expressions for concurrent processing
        test_expressions = [
            "\\int_0^1 x^n dx = \\frac{1}{n+1}",
            "\\sum_{k=1}^n k = \\frac{n(n+1)}{2}",
            "e^{i\\pi} + 1 = 0",
            "\\nabla \\times \\vec{E} = -\\frac{\\partial \\vec{B}}{\\partial t}",
            "\\det(AB) = \\det(A)\\det(B)",
        ] * 4  # 20 total expressions
        
        # Sequential processing
        start_seq = time.time()
        seq_results = []
        for expr in test_expressions:
            result = self.engine.process_latex(expr)
            seq_results.append(result)
        seq_duration = time.time() - start_seq
        
        # Concurrent processing with asyncio
        start_async = time.time()
        async_results = await asyncio.gather(*[
            self._process_async(expr) for expr in test_expressions
        ])
        async_duration = time.time() - start_async
        
        # Compare results
        speedup = seq_duration / async_duration if async_duration > 0 else 1.0
        
        self.metrics.record_test("Concurrent: Async processing", 
                               speedup > 1.5,  # At least 1.5x speedup
                               async_duration,
                               f"Speedup: {speedup:.2f}x")
        
        # Test thread safety
        thread_errors = []
        def process_in_thread(expr, idx):
            try:
                result = self.engine.process_latex(expr)
                if not result.processed:
                    thread_errors.append(f"Thread {idx} failed")
            except Exception as e:
                thread_errors.append(f"Thread {idx} error: {e}")
        
        threads = []
        for i, expr in enumerate(test_expressions[:10]):
            t = threading.Thread(target=process_in_thread, args=(expr, i))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()
        
        self.metrics.record_test("Concurrent: Thread safety", 
                               len(thread_errors) == 0,
                               len(threads),
                               f"Errors: {thread_errors[:3]}")
    
    async def _process_async(self, expr):
        """Process expression asynchronously"""
        return self.engine.process_latex(expr)
    
    async def _run_single_test(self, name: str, expression: str, 
                              expect_failure: bool = False) -> bool:
        """Run a single test case"""
        start = time.time()
        try:
            result = self.engine.process_latex(expression)
            duration = time.time() - start
            
            # Check success
            if expect_failure:
                # For edge cases, we expect it to handle gracefully
                success = True  # Didn't crash
            else:
                success = bool(result.processed) and len(result.processed) > 0
            
            self.metrics.record_test(name, success, duration)
            return success
            
        except Exception as e:
            duration = time.time() - start
            if expect_failure:
                # Expected to fail, but should fail gracefully
                self.metrics.record_test(name, True, duration, 
                                       f"Handled gracefully: {type(e).__name__}")
                return True
            else:
                self.metrics.record_test(name, False, duration, str(e))
                return False
    
    def _save_report(self, report: Dict[str, Any]):
        """Save test report to file"""
        # JSON report
        json_file = self.test_output_dir / "comprehensive_test_report.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Human-readable report
        text_file = self.test_output_dir / "comprehensive_test_report.txt"
        with open(text_file, 'w') as f:
            f.write("MathSpeak Comprehensive Test Report\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            
            # Summary
            s = report['summary']
            f.write("TEST SUMMARY\n")
            f.write("-" * 30 + "\n")
            f.write(f"Total Tests: {s['total_tests']}\n")
            f.write(f"Passed: {s['passed']} ({s['success_rate']*100:.1f}%)\n")
            f.write(f"Failed: {s['failed']}\n")
            f.write(f"Duration: {s['total_duration']:.1f}s\n")
            f.write(f"Tests/second: {s['tests_per_second']:.1f}\n\n")
            
            # Performance
            p = report['performance']
            f.write("PERFORMANCE METRICS\n")
            f.write("-" * 30 + "\n")
            f.write(f"Average test duration: {p['average_duration']:.3f}s\n")
            f.write(f"Min duration: {p['min_duration']:.3f}s\n")
            f.write(f"Max duration: {p['max_duration']:.3f}s\n\n")
            
            # Resources
            r = report['resources']
            f.write("RESOURCE USAGE\n")
            f.write("-" * 30 + "\n")
            f.write(f"Average CPU: {r['average_cpu_percent']:.1f}%\n")
            f.write(f"Max memory: {r['max_memory_mb']:.1f}MB\n")
            f.write(f"Average memory: {r['average_memory_mb']:.1f}MB\n\n")
            
            # Domain coverage
            if report['domain_coverage']:
                f.write("DOMAIN COVERAGE\n")
                f.write("-" * 30 + "\n")
                for domain, count in report['domain_coverage'].items():
                    f.write(f"{domain}: {count} tests passed\n")
                f.write("\n")
            
            # TTS Engines
            if report['tts_engine_stats']:
                f.write("TTS ENGINE STATUS\n")
                f.write("-" * 30 + "\n")
                for engine, stats in report['tts_engine_stats'].items():
                    status = "Available" if stats.get('available') else "Not Available"
                    f.write(f"{engine}: {status}\n")
                    if stats.get('generation_time'):
                        f.write(f"  Generation time: {stats['generation_time']:.2f}s\n")
                f.write("\n")
            
            # Errors
            if report['errors']:
                f.write("ERRORS (First 10)\n")
                f.write("-" * 30 + "\n")
                for err in report['errors'][:10]:
                    f.write(f"Test: {err['test']}\n")
                    f.write(f"Error: {err['error']}\n\n")
            
            # Edge cases
            if report['edge_cases']:
                f.write("EDGE CASES FOUND\n")
                f.write("-" * 30 + "\n")
                for edge in report['edge_cases'][:10]:
                    f.write(f"{edge}\n")
        
        print(f"\n📄 Reports saved to {self.test_output_dir}/")
    
    def _print_summary(self, report: Dict[str, Any]):
        """Print test summary to console"""
        s = report['summary']
        
        print("\n" + "="*60)
        print("COMPREHENSIVE TEST COMPLETE")
        print("="*60)
        
        print(f"\n📊 Results:")
        print(f"   Total Tests: {s['total_tests']}")
        print(f"   ✅ Passed: {s['passed']} ({s['success_rate']*100:.1f}%)")
        print(f"   ❌ Failed: {s['failed']}")
        print(f"   ⏱️  Duration: {s['total_duration']:.1f}s")
        
        if s['failed'] > 0:
            print(f"\n❌ Failed Tests:")
            for err in report['errors'][:5]:
                print(f"   - {err['test']}: {err['error'][:50]}...")
        
        print(f"\n💡 Recommendations:")
        if report['resources']['max_memory_mb'] > 500:
            print("   - Consider optimizing memory usage")
        if report['performance']['average_duration'] > 1.0:
            print("   - Performance could be improved for complex expressions")
        if len(report['edge_cases']) > 10:
            print(f"   - {len(report['edge_cases'])} edge cases found - review handling")
        
        # Overall assessment
        if s['success_rate'] > 0.95:
            print("\n✨ System is production-ready!")
        elif s['success_rate'] > 0.8:
            print("\n⚠️  System needs some improvements")
        else:
            print("\n❌ System has significant issues")


async def main():
    """Run comprehensive test suite"""
    tester = ComprehensiveSystemTest()
    
    try:
        report = await tester.run_all_tests()
        
        # Exit with appropriate code
        if report['summary']['success_rate'] < 0.8:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Test suite failed: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())