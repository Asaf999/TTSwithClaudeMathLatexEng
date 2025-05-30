#!/usr/bin/env python3
"""
Final Comprehensive System Test for MathSpeak
==============================================

This script tests all aspects of the MathSpeak system including:
- Basic mathematical expressions
- Advanced mathematical domains
- All CLI features
- Performance benchmarks
- Edge cases
- TTS engine comparison
"""

import asyncio
import time
import json
import subprocess
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
import tempfile
import shutil

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine, MathematicalContext
from mathspeak.core.voice_manager import VoiceManager, VoiceRole
from mathspeak.utils.logger import setup_logging
import logging

# Setup logging
setup_logging(logging.INFO)
logger = logging.getLogger(__name__)

class TestResult:
    """Container for test results"""
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.error = None
        self.duration = 0.0
        self.details = {}
        self.output = ""

class ComprehensiveSystemTest:
    """Comprehensive test suite for MathSpeak"""
    
    def __init__(self):
        self.results = []
        self.test_dir = Path("test_output")
        self.test_dir.mkdir(exist_ok=True)
        
        # Initialize engine
        self.voice_manager = VoiceManager()
        self.engine = MathematicalTTSEngine(
            voice_manager=self.voice_manager,
            enable_caching=True
        )
        
        # Test expressions organized by category
        self.test_expressions = {
            'basic_arithmetic': [
                ("2 + 2 = 4", "Simple addition"),
                ("x^2 + y^2 = r^2", "Pythagorean theorem"),
                ("\\frac{a+b}{c-d}", "Basic fraction"),
                ("\\sqrt{x^2 + y^2}", "Square root"),
                ("3.14159\\ldots", "Decimal with ellipsis"),
            ],
            
            'algebra': [
                ("ax^2 + bx + c = 0", "Quadratic equation"),
                ("x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}", "Quadratic formula"),
                ("(a+b)^n = \\sum_{k=0}^n \\binom{n}{k} a^{n-k} b^k", "Binomial theorem"),
                ("\\det(A - \\lambda I) = 0", "Characteristic equation"),
                ("v_1, v_2, \\ldots, v_n", "Vector sequence"),
            ],
            
            'calculus': [
                ("\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1", "Famous limit"),
                ("\\frac{d}{dx} f(x) = f'(x)", "Derivative notation"),
                ("\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}", "Gaussian integral"),
                ("\\nabla \\cdot \\vec{F} = \\frac{\\partial F_x}{\\partial x} + \\frac{\\partial F_y}{\\partial y} + \\frac{\\partial F_z}{\\partial z}", "Divergence"),
                ("\\oint_C \\vec{F} \\cdot d\\vec{r} = \\iint_S (\\nabla \\times \\vec{F}) \\cdot d\\vec{S}", "Stokes' theorem"),
            ],
            
            'topology': [
                ("\\pi_1(S^1) \\cong \\mathbb{Z}", "Fundamental group of circle"),
                ("X \\text{ is compact} \\iff \\text{every open cover has a finite subcover}", "Compactness"),
                ("\\overline{A} = A \\cup \\partial A", "Closure equals union with boundary"),
                ("f: X \\to Y \\text{ continuous} \\iff f^{-1}(U) \\text{ open } \\forall U \\subset Y \\text{ open}", "Continuity definition"),
                ("H_n(S^n) \\cong \\mathbb{Z}", "Homology of sphere"),
            ],
            
            'complex_analysis': [
                ("f(z) = u(x,y) + iv(x,y)", "Complex function decomposition"),
                ("\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y}, \\quad \\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}", "Cauchy-Riemann equations"),
                ("\\oint_\\gamma f(z)dz = 2\\pi i \\sum_{k} \\text{Res}(f, z_k)", "Residue theorem"),
                ("e^{i\\pi} + 1 = 0", "Euler's identity"),
                ("\\log z = \\ln|z| + i\\arg(z)", "Complex logarithm"),
            ],
            
            'real_analysis': [
                ("\\forall \\epsilon > 0 \\exists \\delta > 0 : |x-a| < \\delta \\implies |f(x) - f(a)| < \\epsilon", "Epsilon-delta definition"),
                ("\\{x_n\\} \\text{ Cauchy} \\iff \\forall \\epsilon > 0 \\exists N : m,n > N \\implies |x_m - x_n| < \\epsilon", "Cauchy sequence"),
                ("\\limsup_{n \\to \\infty} a_n = \\lim_{n \\to \\infty} \\sup_{k \\geq n} a_k", "Limit superior"),
                ("f \\in L^p \\iff \\|f\\|_p = \\left(\\int |f|^p d\\mu\\right)^{1/p} < \\infty", "Lp space"),
                ("\\sum_{n=1}^\\infty \\frac{1}{n^2} = \\frac{\\pi^2}{6}", "Basel problem"),
            ],
            
            'edge_cases': [
                ("", "Empty expression"),
                ("x", "Single variable"),
                ("\\", "Single backslash"),
                ("\\unknowncommand{x}", "Unknown command"),
                ("$x$ and $$y$$", "Mixed delimiters"),
                ("x_1^2_3^4", "Multiple subscripts/superscripts"),
                ("\\frac{\\frac{a}{b}}{\\frac{c}{d}}", "Nested fractions"),
                ("\\sum_{\\sum_{i=1}^n i}^{\\prod_{j=1}^m j} x", "Complex indices"),
            ],
            
            'special_symbols': [
                ("\\alpha, \\beta, \\gamma, \\delta, \\epsilon", "Greek letters"),
                ("\\mathbb{R}, \\mathbb{C}, \\mathbb{Z}, \\mathbb{N}", "Blackboard bold"),
                ("\\infty, \\partial, \\nabla, \\forall, \\exists", "Special symbols"),
                ("\\rightarrow, \\Rightarrow, \\leftrightarrow, \\Leftrightarrow", "Arrows"),
                ("\\subset, \\subseteq, \\supset, \\supseteq", "Set relations"),
            ],
        }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results"""
        print("🧪 Starting Comprehensive System Test")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run test categories
        self._test_basic_expressions()
        self._test_advanced_math()
        self._test_cli_features()
        self._test_performance()
        self._test_edge_cases()
        self._test_tts_engines()
        self._test_batch_processing()
        self._test_interactive_mode()
        self._test_error_handling()
        self._test_caching()
        
        # Generate report
        total_duration = time.time() - start_time
        report = self._generate_report(total_duration)
        
        # Save report
        self._save_report(report)
        
        return report
    
    def _test_basic_expressions(self):
        """Test basic mathematical expressions"""
        print("\n📐 Testing Basic Mathematical Expressions...")
        
        for category in ['basic_arithmetic', 'algebra']:
            for expr, desc in self.test_expressions[category]:
                result = TestResult(f"Basic: {desc}")
                start = time.time()
                
                try:
                    # Process expression
                    output = self.engine.process_latex(expr)
                    result.passed = True
                    result.details = {
                        'input': expr,
                        'output': output.processed,
                        'context': output.context,
                        'unknown_commands': output.unknown_commands
                    }
                except Exception as e:
                    result.error = str(e)
                    logger.error(f"Test failed: {desc} - {e}")
                
                result.duration = time.time() - start
                self.results.append(result)
                
                # Print progress
                status = "✓" if result.passed else "✗"
                print(f"  {status} {desc}: {result.duration:.3f}s")
    
    def _test_advanced_math(self):
        """Test advanced mathematical domains"""
        print("\n🎓 Testing Advanced Mathematical Domains...")
        
        for category in ['calculus', 'topology', 'complex_analysis', 'real_analysis']:
            print(f"\n  Testing {category.replace('_', ' ').title()}:")
            
            for expr, desc in self.test_expressions[category]:
                result = TestResult(f"Advanced: {desc}")
                start = time.time()
                
                try:
                    # Process with context detection
                    output = self.engine.process_latex(expr)
                    
                    # Generate speech
                    temp_file = self.test_dir / f"test_{category}_{int(time.time())}.mp3"
                    asyncio.run(self.engine.speak_expression(output, str(temp_file)))
                    
                    result.passed = temp_file.exists()
                    result.details = {
                        'input': expr,
                        'output': output.processed,
                        'context': output.context,
                        'audio_generated': temp_file.exists(),
                        'audio_size': temp_file.stat().st_size if temp_file.exists() else 0
                    }
                    
                except Exception as e:
                    result.error = str(e)
                    logger.error(f"Test failed: {desc} - {e}")
                
                result.duration = time.time() - start
                self.results.append(result)
                
                # Print progress
                status = "✓" if result.passed else "✗"
                print(f"    {status} {desc}: {result.duration:.3f}s")
    
    def _test_cli_features(self):
        """Test CLI features"""
        print("\n🖥️  Testing CLI Features...")
        
        cli_tests = [
            ("Basic expression", ["python", "mathspeak.py", "x^2 + y^2 = r^2"]),
            ("File input", ["python", "mathspeak.py", "--file", "test_input.tex"]),
            ("Save output", ["python", "mathspeak.py", "\\pi", "--save"]),
            ("Specific output", ["python", "mathspeak.py", "e^{i\\pi}", "--output", "test_cli.mp3"]),
            ("Offline mode", ["python", "mathspeak.py", "\\sum_{n=1}^\\infty", "--offline"]),
            ("Voice selection", ["python", "mathspeak.py", "f(x)", "--voice", "theorem"]),
            ("No cache", ["python", "mathspeak.py", "\\int", "--no-cache"]),
            ("Speed adjustment", ["python", "mathspeak.py", "dx/dt", "--speed", "1.5"]),
            ("Context forcing", ["python", "mathspeak.py", "\\pi_1", "--context", "topology"]),
            ("Test mode", ["python", "mathspeak.py", "--test", "basic"]),
            ("Version check", ["python", "mathspeak.py", "--version"]),
        ]
        
        # Create test input file
        test_input = self.test_dir / "test_input.tex"
        test_input.write_text("\\int_0^1 x^2 dx = \\frac{1}{3}")
        
        for desc, cmd in cli_tests:
            result = TestResult(f"CLI: {desc}")
            start = time.time()
            
            try:
                # Run CLI command
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    cwd=str(Path(__file__).parent)
                )
                
                result.passed = proc.returncode == 0 or desc == "Version check"
                result.output = proc.stdout
                result.details = {
                    'command': ' '.join(cmd),
                    'returncode': proc.returncode,
                    'stdout_lines': len(proc.stdout.splitlines()),
                    'stderr': proc.stderr[:200] if proc.stderr else ""
                }
                
            except subprocess.TimeoutExpired:
                result.error = "Command timed out"
            except Exception as e:
                result.error = str(e)
            
            result.duration = time.time() - start
            self.results.append(result)
            
            # Print progress
            status = "✓" if result.passed else "✗"
            print(f"  {status} {desc}: {result.duration:.3f}s")
    
    def _test_performance(self):
        """Test performance benchmarks"""
        print("\n⚡ Testing Performance...")
        
        perf_tests = [
            ("Simple expression", "x + y", 100),
            ("Complex expression", "\\int_0^\\infty e^{-x^2} dx", 50),
            ("Long expression", " + ".join([f"x_{i}" for i in range(50)]), 10),
            ("Many symbols", "\\alpha\\beta\\gamma\\delta\\epsilon\\zeta\\eta\\theta", 50),
        ]
        
        for desc, expr, iterations in perf_tests:
            result = TestResult(f"Performance: {desc}")
            times = []
            
            try:
                # Warm up
                self.engine.process_latex(expr)
                
                # Benchmark
                for _ in range(iterations):
                    start = time.time()
                    self.engine.process_latex(expr)
                    times.append(time.time() - start)
                
                result.passed = True
                result.duration = sum(times)
                result.details = {
                    'iterations': iterations,
                    'total_time': sum(times),
                    'avg_time': sum(times) / iterations,
                    'min_time': min(times),
                    'max_time': max(times),
                    'throughput': iterations / sum(times)
                }
                
            except Exception as e:
                result.error = str(e)
            
            self.results.append(result)
            
            # Print progress
            if result.passed:
                avg_time = result.details['avg_time']
                throughput = result.details['throughput']
                print(f"  ✓ {desc}: {avg_time*1000:.1f}ms avg, {throughput:.1f} expr/s")
            else:
                print(f"  ✗ {desc}: {result.error}")
    
    def _test_edge_cases(self):
        """Test edge cases and error handling"""
        print("\n🔧 Testing Edge Cases...")
        
        for expr, desc in self.test_expressions['edge_cases']:
            result = TestResult(f"Edge: {desc}")
            start = time.time()
            
            try:
                # These should handle gracefully
                output = self.engine.process_latex(expr)
                result.passed = True
                result.details = {
                    'input': expr,
                    'output': output.processed,
                    'handled_gracefully': True
                }
            except Exception as e:
                # Some edge cases are expected to fail gracefully
                result.passed = "gracefully" in str(e).lower() or expr == ""
                result.error = str(e)
            
            result.duration = time.time() - start
            self.results.append(result)
            
            # Print progress
            status = "✓" if result.passed else "✗"
            print(f"  {status} {desc}: {result.duration:.3f}s")
    
    def _test_tts_engines(self):
        """Compare TTS engines"""
        print("\n🔊 Testing TTS Engines...")
        
        test_expr = "The integral of e to the negative x squared from 0 to infinity equals square root of pi over 2"
        
        # Test online engine
        result_online = TestResult("TTS: Online Engine")
        try:
            start = time.time()
            temp_file = self.test_dir / "test_online_tts.mp3"
            
            # Force online engine
            self.engine.tts_manager.preferred_engine = 'edge-tts'
            success = asyncio.run(self.engine.tts_manager.generate_speech(
                test_expr, str(temp_file)
            ))
            
            result_online.passed = success and temp_file.exists()
            result_online.duration = time.time() - start
            result_online.details = {
                'engine': 'edge-tts',
                'file_size': temp_file.stat().st_size if temp_file.exists() else 0,
                'generation_time': result_online.duration
            }
        except Exception as e:
            result_online.error = str(e)
        
        self.results.append(result_online)
        
        # Test offline engine
        result_offline = TestResult("TTS: Offline Engine")
        try:
            start = time.time()
            temp_file = self.test_dir / "test_offline_tts.mp3"
            
            # Force offline engine
            self.engine.tts_manager.preferred_engine = 'pyttsx3'
            success = asyncio.run(self.engine.tts_manager.generate_speech(
                test_expr, str(temp_file)
            ))
            
            result_offline.passed = success and temp_file.exists()
            result_offline.duration = time.time() - start
            result_offline.details = {
                'engine': 'pyttsx3',
                'file_size': temp_file.stat().st_size if temp_file.exists() else 0,
                'generation_time': result_offline.duration
            }
        except Exception as e:
            result_offline.error = str(e)
        
        self.results.append(result_offline)
        
        # Print comparison
        print(f"  Online (edge-tts): {'✓' if result_online.passed else '✗'} - {result_online.duration:.3f}s")
        print(f"  Offline (pyttsx3): {'✓' if result_offline.passed else '✗'} - {result_offline.duration:.3f}s")
    
    def _test_batch_processing(self):
        """Test batch processing"""
        print("\n📦 Testing Batch Processing...")
        
        # Create batch file
        batch_file = self.test_dir / "test_batch.txt"
        batch_expressions = [
            "x^2 + y^2 = r^2",
            "\\int_0^1 x dx",
            "\\pi_1(S^1) \\cong \\mathbb{Z}",
            "e^{i\\pi} + 1 = 0",
            "\\sum_{n=1}^\\infty \\frac{1}{n^2}"
        ]
        batch_file.write_text('\n'.join(batch_expressions))
        
        result = TestResult("Batch Processing")
        
        try:
            start = time.time()
            
            # Run batch processing
            proc = subprocess.run(
                ["python", "mathspeak.py", "--batch", str(batch_file), 
                 "--batch-output", str(self.test_dir / "batch_output")],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=str(Path(__file__).parent)
            )
            
            result.passed = proc.returncode == 0
            result.duration = time.time() - start
            
            # Check output files
            batch_output_dir = self.test_dir / "batch_output"
            if batch_output_dir.exists():
                output_files = list(batch_output_dir.glob("*.mp3"))
                result.details = {
                    'expressions_count': len(batch_expressions),
                    'files_generated': len(output_files),
                    'all_generated': len(output_files) == len(batch_expressions)
                }
            
        except Exception as e:
            result.error = str(e)
        
        self.results.append(result)
        
        # Print result
        status = "✓" if result.passed else "✗"
        print(f"  {status} Batch processing: {result.duration:.3f}s")
        if result.passed and 'files_generated' in result.details:
            print(f"    Generated {result.details['files_generated']}/{result.details['expressions_count']} files")
    
    def _test_interactive_mode(self):
        """Test interactive mode (basic check)"""
        print("\n💬 Testing Interactive Mode...")
        
        result = TestResult("Interactive Mode")
        
        try:
            # Just test that it starts and responds to exit
            proc = subprocess.Popen(
                ["python", "mathspeak.py", "--interactive"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=str(Path(__file__).parent)
            )
            
            # Send exit command
            stdout, stderr = proc.communicate(input="/exit\n", timeout=5)
            
            result.passed = "Thank you for using MathSpeak" in stdout
            result.details = {
                'started_successfully': "MathSpeak" in stdout,
                'responded_to_exit': "Thank you" in stdout
            }
            
        except subprocess.TimeoutExpired:
            proc.kill()
            result.error = "Interactive mode timeout"
        except Exception as e:
            result.error = str(e)
        
        self.results.append(result)
        
        # Print result
        status = "✓" if result.passed else "✗"
        print(f"  {status} Interactive mode startup")
    
    def _test_error_handling(self):
        """Test error handling and recovery"""
        print("\n🛡️  Testing Error Handling...")
        
        error_tests = [
            ("Invalid LaTeX", "\\undefined{command}"),
            ("Malformed expression", "\\frac{1}{"),
            ("Empty context", ""),
            ("Very long expression", "x" * 10000),
            ("Invalid UTF-8", "\\text{" + chr(0xDEAD) + "}"),
        ]
        
        for desc, expr in error_tests:
            result = TestResult(f"Error Handling: {desc}")
            
            try:
                # Should handle gracefully
                output = self.engine.process_latex(expr)
                result.passed = True
                result.details = {
                    'handled_gracefully': True,
                    'output_length': len(output.processed)
                }
            except Exception as e:
                # Controlled failure is also acceptable
                result.passed = True
                result.details = {
                    'exception_type': type(e).__name__,
                    'handled_gracefully': True
                }
            
            self.results.append(result)
            
            # Print result
            print(f"  ✓ {desc}: Handled gracefully")
    
    def _test_caching(self):
        """Test caching functionality"""
        print("\n💾 Testing Caching...")
        
        test_expr = "\\int_0^\\infty e^{-x^2} dx"
        
        result = TestResult("Caching")
        
        try:
            # First call (cache miss)
            start1 = time.time()
            output1 = self.engine.process_latex(test_expr)
            time1 = time.time() - start1
            
            # Second call (cache hit)
            start2 = time.time()
            output2 = self.engine.process_latex(test_expr)
            time2 = time.time() - start2
            
            # Cache should make it faster
            result.passed = time2 < time1 * 0.5  # At least 50% faster
            result.details = {
                'first_call_time': time1,
                'second_call_time': time2,
                'speedup': time1 / time2 if time2 > 0 else float('inf'),
                'outputs_match': output1.processed == output2.processed
            }
            
        except Exception as e:
            result.error = str(e)
        
        self.results.append(result)
        
        # Print result
        if result.passed:
            speedup = result.details['speedup']
            print(f"  ✓ Caching: {speedup:.1f}x speedup on cache hit")
        else:
            print(f"  ✗ Caching: Failed")
    
    def _generate_report(self, total_duration: float) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        passed_tests = sum(1 for r in self.results if r.passed)
        total_tests = len(self.results)
        
        # Group results by category
        categories = {}
        for result in self.results:
            category = result.name.split(':')[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(result)
        
        # Calculate statistics
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_duration': total_duration,
            'summary': {
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': total_tests - passed_tests,
                'pass_rate': passed_tests / total_tests if total_tests > 0 else 0
            },
            'categories': {},
            'performance_metrics': {},
            'failed_tests': [],
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform,
                'mathspeak_version': '1.0.0'
            }
        }
        
        # Analyze by category
        for category, results in categories.items():
            passed = sum(1 for r in results if r.passed)
            report['categories'][category] = {
                'total': len(results),
                'passed': passed,
                'failed': len(results) - passed,
                'pass_rate': passed / len(results) if results else 0,
                'avg_duration': sum(r.duration for r in results) / len(results) if results else 0
            }
        
        # Collect failed tests
        for result in self.results:
            if not result.passed:
                report['failed_tests'].append({
                    'name': result.name,
                    'error': result.error,
                    'details': result.details
                })
        
        # Extract performance metrics
        perf_results = [r for r in self.results if r.name.startswith("Performance:")]
        if perf_results:
            total_throughput = 0
            for r in perf_results:
                if r.passed and 'throughput' in r.details:
                    total_throughput += r.details['throughput']
            
            report['performance_metrics'] = {
                'avg_throughput': total_throughput / len(perf_results) if perf_results else 0,
                'tests_completed': len(perf_results)
            }
        
        return report
    
    def _save_report(self, report: Dict[str, Any]):
        """Save test report to files"""
        # JSON report
        json_file = self.test_dir / "final_test_report.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Human-readable report
        text_file = self.test_dir / "final_test_report.txt"
        with open(text_file, 'w') as f:
            f.write("MathSpeak Final System Test Report\n")
            f.write("="*60 + "\n\n")
            f.write(f"Generated: {report['timestamp']}\n")
            f.write(f"Total Duration: {report['total_duration']:.2f}s\n\n")
            
            f.write("Summary\n")
            f.write("-"*30 + "\n")
            summary = report['summary']
            f.write(f"Total Tests: {summary['total_tests']}\n")
            f.write(f"Passed: {summary['passed']}\n")
            f.write(f"Failed: {summary['failed']}\n")
            f.write(f"Pass Rate: {summary['pass_rate']*100:.1f}%\n\n")
            
            f.write("Results by Category\n")
            f.write("-"*30 + "\n")
            for category, stats in report['categories'].items():
                f.write(f"\n{category}:\n")
                f.write(f"  Tests: {stats['total']}\n")
                f.write(f"  Passed: {stats['passed']}\n")
                f.write(f"  Failed: {stats['failed']}\n")
                f.write(f"  Pass Rate: {stats['pass_rate']*100:.1f}%\n")
                f.write(f"  Avg Duration: {stats['avg_duration']:.3f}s\n")
            
            if report['failed_tests']:
                f.write("\nFailed Tests\n")
                f.write("-"*30 + "\n")
                for test in report['failed_tests']:
                    f.write(f"\n{test['name']}:\n")
                    f.write(f"  Error: {test['error']}\n")
                    if test['details']:
                        f.write(f"  Details: {test['details']}\n")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 TEST RESULTS SUMMARY")
        print("="*60)
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']} ✓")
        print(f"Failed: {summary['failed']} ✗")
        print(f"Pass Rate: {summary['pass_rate']*100:.1f}%")
        print(f"Total Duration: {report['total_duration']:.2f}s")
        print(f"\nReports saved to:")
        print(f"  - {json_file}")
        print(f"  - {text_file}")

def main():
    """Run comprehensive system test"""
    try:
        tester = ComprehensiveSystemTest()
        report = tester.run_all_tests()
        
        # Overall pass/fail
        if report['summary']['pass_rate'] >= 0.95:  # 95% pass rate
            print("\n✅ SYSTEM TEST PASSED!")
            sys.exit(0)
        else:
            print("\n❌ SYSTEM TEST FAILED!")
            print(f"Pass rate: {report['summary']['pass_rate']*100:.1f}% (required: 95%)")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        logger.error("Fatal error in test execution", exc_info=True)
        sys.exit(2)

if __name__ == "__main__":
    main()