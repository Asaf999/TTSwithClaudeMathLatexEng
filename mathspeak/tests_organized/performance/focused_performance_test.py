#!/usr/bin/env python3
"""
Focused Performance and Stress Test
====================================

Tests the core system functionality under various conditions
"""

import time
import sys
import psutil
import os
import gc
from pathlib import Path
from typing import List, Dict, Any
import json
import random

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

class FocusedTester:
    """Focused testing of core functionality"""
    
    def __init__(self):
        self.engine = None
        self.results = {
            "system_info": self._get_system_info(),
            "performance": {},
            "robustness": {},
            "real_world": {},
            "errors": []
        }
    
    def _get_system_info(self):
        """Get system information"""
        return {
            "platform": sys.platform,
            "python_version": sys.version,
            "cpu_count": os.cpu_count(),
            "memory_mb": round(psutil.virtual_memory().total / 1024 / 1024),
            "disk_free_gb": round(psutil.disk_usage('/').free / 1024 / 1024 / 1024)
        }
    
    def setup(self):
        """Initialize system"""
        print("Setting up MathSpeak engine...")
        voice_manager = VoiceManager()
        self.engine = MathematicalTTSEngine(
            voice_manager=voice_manager,
            enable_caching=True,
            prefer_offline_tts=False
        )
        print("✓ Engine initialized")
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        print("\n1. Testing Basic Functionality")
        print("-" * 40)
        
        basic_expressions = [
            "x^2 + y^2 = z^2",
            "\\int_0^1 x^2 dx",
            "\\sum_{n=1}^{\\infty} \\frac{1}{n^2}",
            "\\lim_{x \\to 0} \\frac{\\sin x}{x}",
            "\\frac{d}{dx} e^x = e^x"
        ]
        
        success_count = 0
        total_time = 0
        response_times = []
        
        for expr in basic_expressions:
            try:
                start = time.time()
                result = self.engine.process_latex(expr)
                processing_time = time.time() - start
                
                response_times.append(processing_time)
                total_time += processing_time
                
                if len(result.processed) > 0:
                    success_count += 1
                    print(f"  ✓ {expr[:30]:<30} {processing_time:.3f}s")
                else:
                    print(f"  ✗ {expr[:30]:<30} Empty result")
                    
            except Exception as e:
                print(f"  ✗ {expr[:30]:<30} Error: {str(e)[:30]}")
                self.results["errors"].append({"test": "basic", "expr": expr, "error": str(e)})
        
        success_rate = success_count / len(basic_expressions) * 100
        avg_time = sum(response_times) / len(response_times) if response_times else 0
        
        self.results["performance"]["basic"] = {
            "success_rate": success_rate,
            "avg_response_time": avg_time,
            "max_response_time": max(response_times) if response_times else 0,
            "min_response_time": min(response_times) if response_times else 0,
            "total_expressions": len(basic_expressions)
        }
        
        print(f"\n  Success Rate: {success_rate:.1f}%")
        print(f"  Average Time: {avg_time:.3f}s")
        print(f"  Status: {'✓ PASS' if success_rate >= 90 else '✗ FAIL'}")
    
    def test_cache_performance(self):
        """Test caching effectiveness"""
        print("\n2. Testing Cache Performance")
        print("-" * 40)
        
        test_expr = "\\int_0^1 x^3 e^{-x} dx"
        
        # First run (populate cache)
        first_times = []
        for i in range(5):
            start = time.time()
            self.engine.process_latex(test_expr)
            first_times.append(time.time() - start)
        
        # Second run (should hit cache)
        second_times = []
        for i in range(5):
            start = time.time()
            self.engine.process_latex(test_expr)
            second_times.append(time.time() - start)
        
        avg_first = sum(first_times) / len(first_times)
        avg_second = sum(second_times) / len(second_times)
        speedup = avg_first / avg_second if avg_second > 0 else 0
        
        # Get cache stats
        report = self.engine.get_performance_report()
        cache_hit_rate = report.get("metrics", {}).get("cache_hit_rate", 0)
        
        self.results["performance"]["cache"] = {
            "first_run_avg": avg_first,
            "cached_run_avg": avg_second,
            "speedup_factor": speedup,
            "cache_hit_rate": cache_hit_rate
        }
        
        print(f"  First run avg:  {avg_first:.3f}s")
        print(f"  Cached run avg: {avg_second:.3f}s")
        print(f"  Speedup factor: {speedup:.1f}x")
        print(f"  Cache hit rate: {cache_hit_rate*100:.1f}%")
        print(f"  Status: {'✓ PASS' if speedup > 2 else '✗ FAIL'}")
    
    def test_memory_usage(self):
        """Test memory consumption"""
        print("\n3. Testing Memory Usage")
        print("-" * 40)
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process many expressions
        expressions = [
            f"\\int_0^{i} x^{i} dx = \\frac{{{i+1}}}{{2^{i+1}}}"
            for i in range(1, 101)
        ]
        
        for expr in expressions[:50]:  # Test first 50
            try:
                self.engine.process_latex(expr)
            except:
                pass
        
        # Force garbage collection
        gc.collect()
        time.sleep(0.5)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        self.results["performance"]["memory"] = {
            "initial_mb": initial_memory,
            "final_mb": final_memory,
            "increase_mb": memory_increase,
            "expressions_processed": 50
        }
        
        print(f"  Initial memory: {initial_memory:.1f} MB")
        print(f"  Final memory:   {final_memory:.1f} MB")
        print(f"  Memory increase: {memory_increase:.1f} MB")
        print(f"  Status: {'✓ PASS' if memory_increase < 50 else '✗ FAIL'}")
    
    def test_edge_cases(self):
        """Test edge case handling"""
        print("\n4. Testing Edge Cases")
        print("-" * 40)
        
        edge_cases = [
            ("", "empty"),
            ("   ", "whitespace"),
            ("x", "single_char"),
            ("\\undefined{x}", "unknown_command"),
            ("$"*100, "repetitive"),
            ("x_1 + x_2 + ... + x_100", "many_subscripts"),
            ("∀ε>0 ∃δ>0", "unicode"),
            ("\\begin{matrix} a & b \\\\ c & d \\end{matrix}", "matrix")
        ]
        
        success_count = 0
        
        for expr, case_type in edge_cases:
            try:
                result = self.engine.process_latex(expr)
                if isinstance(result.processed, str):
                    success_count += 1
                    print(f"  ✓ {case_type:<15} Handled")
                else:
                    print(f"  ✗ {case_type:<15} Invalid result")
            except Exception as e:
                print(f"  ✗ {case_type:<15} Error: {str(e)[:30]}")
                self.results["errors"].append({"test": "edge", "case": case_type, "error": str(e)})
        
        success_rate = success_count / len(edge_cases) * 100
        self.results["robustness"]["edge_cases"] = {
            "success_rate": success_rate,
            "total_cases": len(edge_cases)
        }
        
        print(f"\n  Success Rate: {success_rate:.1f}%")
        print(f"  Status: {'✓ PASS' if success_rate >= 80 else '✗ FAIL'}")
    
    def test_complex_expressions(self):
        """Test complex mathematical expressions"""
        print("\n5. Testing Complex Expressions")
        print("-" * 40)
        
        complex_expressions = [
            "\\oint_C \\frac{f(z)}{z-a} dz = 2\\pi i f(a)",
            "\\nabla \\times (\\nabla \\times \\mathbf{F}) = \\nabla(\\nabla \\cdot \\mathbf{F}) - \\nabla^2 \\mathbf{F}",
            "\\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n",
            "\\int_{-\\infty}^{\\infty} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}} dx = \\sigma\\sqrt{2\\pi}",
            "\\det(A) = \\sum_{\\sigma \\in S_n} \\text{sgn}(\\sigma) \\prod_{i=1}^n a_{i,\\sigma(i)}"
        ]
        
        success_count = 0
        processing_times = []
        unknown_commands_total = 0
        
        for expr in complex_expressions:
            try:
                start = time.time()
                result = self.engine.process_latex(expr)
                processing_time = time.time() - start
                
                processing_times.append(processing_time)
                unknown_commands_total += len(result.unknown_commands)
                
                if len(result.processed) > 0:
                    success_count += 1
                    print(f"  ✓ Complex expr {len(processing_times)} - {processing_time:.3f}s")
                    if result.unknown_commands:
                        print(f"    Unknown: {', '.join(result.unknown_commands[:3])}")
                else:
                    print(f"  ✗ Complex expr {len(processing_times)} - Empty result")
                    
            except Exception as e:
                print(f"  ✗ Complex expr - Error: {str(e)[:50]}")
                self.results["errors"].append({"test": "complex", "error": str(e)})
        
        success_rate = success_count / len(complex_expressions) * 100
        avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
        
        self.results["performance"]["complex"] = {
            "success_rate": success_rate,
            "avg_processing_time": avg_time,
            "max_processing_time": max(processing_times) if processing_times else 0,
            "unknown_commands_avg": unknown_commands_total / len(complex_expressions)
        }
        
        print(f"\n  Success Rate: {success_rate:.1f}%")
        print(f"  Average Time: {avg_time:.3f}s")
        print(f"  Avg Unknown Commands: {unknown_commands_total / len(complex_expressions):.1f}")
        print(f"  Status: {'✓ PASS' if success_rate >= 80 and avg_time < 5 else '✗ FAIL'}")
    
    def test_throughput(self):
        """Test system throughput"""
        print("\n6. Testing Throughput")
        print("-" * 40)
        
        # Generate test expressions
        expressions = [
            f"f_{i}(x) = x^{i} + {i}x + {i**2}"
            for i in range(1, 51)
        ]
        
        start_time = time.time()
        success_count = 0
        
        for expr in expressions:
            try:
                result = self.engine.process_latex(expr)
                if len(result.processed) > 0:
                    success_count += 1
            except:
                pass
        
        total_time = time.time() - start_time
        throughput = success_count / total_time
        
        self.results["performance"]["throughput"] = {
            "expressions_per_second": throughput,
            "total_expressions": len(expressions),
            "success_count": success_count,
            "total_time": total_time
        }
        
        print(f"  Processed: {success_count}/{len(expressions)} expressions")
        print(f"  Total time: {total_time:.1f}s")
        print(f"  Throughput: {throughput:.1f} expr/sec")
        print(f"  Status: {'✓ PASS' if throughput > 5 else '✗ FAIL'}")
    
    def test_real_world_scenario(self):
        """Test realistic usage scenario"""
        print("\n7. Testing Real-World Scenario")
        print("-" * 40)
        
        # Simulate a student working through calculus problems
        calculus_problems = [
            "Find \\frac{d}{dx}[x^3 + 2x^2 - x + 1]",
            "3x^2 + 4x - 1",
            "Evaluate \\int_0^2 (x^2 + 1) dx",
            "\\left[\\frac{x^3}{3} + x\\right]_0^2 = \\frac{8}{3} + 2 - 0 = \\frac{14}{3}",
            "Find the limit: \\lim_{x \\to 0} \\frac{\\sin x}{x}",
            "Using L'Hôpital's rule: \\lim_{x \\to 0} \\frac{\\cos x}{1} = 1"
        ]
        
        scenario_start = time.time()
        problems_solved = 0
        total_thinking_time = 0
        
        for i, problem in enumerate(calculus_problems):
            # Simulate student thinking time
            thinking_time = random.uniform(0.1, 0.5)
            time.sleep(thinking_time)
            total_thinking_time += thinking_time
            
            try:
                # Extract math from problem text
                import re
                math_parts = re.findall(r'\\[^\\s]+(?:\{[^}]*\})*|[a-zA-Z_][a-zA-Z0-9_]*(?:\([^)]*\))?', problem)
                
                if math_parts:
                    # Process the mathematical content
                    math_expr = " ".join(math_parts[:3])  # Take first few mathematical parts
                    result = self.engine.process_latex(math_expr)
                    
                    if len(result.processed) > 0:
                        problems_solved += 1
                        print(f"  ✓ Problem {i+1}: Processed")
                    else:
                        print(f"  ✗ Problem {i+1}: Empty result")
                else:
                    # No math found, treat as solved
                    problems_solved += 1
                    print(f"  ✓ Problem {i+1}: Text only")
                    
            except Exception as e:
                print(f"  ✗ Problem {i+1}: Error - {str(e)[:30]}")
        
        scenario_time = time.time() - scenario_start - total_thinking_time
        success_rate = problems_solved / len(calculus_problems) * 100
        
        self.results["real_world"]["student_session"] = {
            "problems_attempted": len(calculus_problems),
            "problems_solved": problems_solved,
            "success_rate": success_rate,
            "processing_time": scenario_time,
            "avg_time_per_problem": scenario_time / len(calculus_problems)
        }
        
        print(f"\n  Problems solved: {problems_solved}/{len(calculus_problems)}")
        print(f"  Success rate: {success_rate:.1f}%")
        print(f"  Processing time: {scenario_time:.1f}s")
        print(f"  Status: {'✓ PASS' if success_rate >= 85 else '✗ FAIL'}")
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "="*60)
        print("MATHSPEAK FOCUSED TEST SUMMARY")
        print("="*60)
        
        # Overall statistics
        basic_pass = self.results["performance"]["basic"]["success_rate"] >= 90
        cache_pass = self.results["performance"]["cache"]["speedup_factor"] > 2
        memory_pass = self.results["performance"]["memory"]["increase_mb"] < 50
        edge_pass = self.results["robustness"]["edge_cases"]["success_rate"] >= 80
        complex_pass = (self.results["performance"]["complex"]["success_rate"] >= 80 and 
                       self.results["performance"]["complex"]["avg_processing_time"] < 5)
        throughput_pass = self.results["performance"]["throughput"]["expressions_per_second"] > 5
        real_world_pass = self.results["real_world"]["student_session"]["success_rate"] >= 85
        
        passed_tests = sum([basic_pass, cache_pass, memory_pass, edge_pass, 
                           complex_pass, throughput_pass, real_world_pass])
        total_tests = 7
        pass_rate = passed_tests / total_tests * 100
        
        print(f"\nTest Results:")
        print(f"  1. Basic Functionality:    {'✓ PASS' if basic_pass else '✗ FAIL'}")
        print(f"  2. Cache Performance:      {'✓ PASS' if cache_pass else '✗ FAIL'}")
        print(f"  3. Memory Usage:           {'✓ PASS' if memory_pass else '✗ FAIL'}")
        print(f"  4. Edge Case Handling:     {'✓ PASS' if edge_pass else '✗ FAIL'}")
        print(f"  5. Complex Expressions:    {'✓ PASS' if complex_pass else '✗ FAIL'}")
        print(f"  6. System Throughput:      {'✓ PASS' if throughput_pass else '✗ FAIL'}")
        print(f"  7. Real-World Scenario:    {'✓ PASS' if real_world_pass else '✗ FAIL'}")
        
        print(f"\nOverall Pass Rate: {pass_rate:.1f}% ({passed_tests}/{total_tests})")
        
        # Production readiness assessment
        if pass_rate >= 90:
            status = "✅ PRODUCTION READY"
            assessment = "System meets all critical requirements"
        elif pass_rate >= 80:
            status = "⚠️ NEAR PRODUCTION READY"
            assessment = "Minor improvements needed"
        elif pass_rate >= 70:
            status = "🔧 NEEDS WORK"
            assessment = "Significant improvements required"
        else:
            status = "❌ NOT READY"
            assessment = "Major issues must be resolved"
        
        print(f"\nProduction Readiness: {status}")
        print(f"Assessment: {assessment}")
        
        # Key metrics
        print(f"\nKey Performance Metrics:")
        print(f"  Average Response Time: {self.results['performance']['basic']['avg_response_time']:.3f}s")
        print(f"  Cache Speedup: {self.results['performance']['cache']['speedup_factor']:.1f}x")
        print(f"  Memory Efficiency: {self.results['performance']['memory']['increase_mb']:.1f}MB increase")
        print(f"  System Throughput: {self.results['performance']['throughput']['expressions_per_second']:.1f} expr/sec")
        print(f"  Error Count: {len(self.results['errors'])}")
        
        self.results["summary"] = {
            "pass_rate": pass_rate,
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "production_ready": pass_rate >= 90,
            "status": status,
            "assessment": assessment
        }
        
        return self.results
    
    def save_results(self, filename="focused_test_results.json"):
        """Save results to file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed results saved to: {filename}")
    
    def run_all_tests(self):
        """Run all tests"""
        try:
            self.test_basic_functionality()
            self.test_cache_performance()
            self.test_memory_usage()
            self.test_edge_cases()
            self.test_complex_expressions()
            self.test_throughput()
            self.test_real_world_scenario()
            
            results = self.generate_summary()
            self.save_results()
            return results
            
        finally:
            if self.engine:
                self.engine.shutdown()


def main():
    """Run focused test suite"""
    print("MathSpeak Focused Performance Test")
    print("=" * 60)
    
    tester = FocusedTester()
    tester.setup()
    results = tester.run_all_tests()
    
    return results


if __name__ == "__main__":
    main()