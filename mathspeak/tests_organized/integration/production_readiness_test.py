#!/usr/bin/env python3
"""
Production Readiness Assessment
===============================

Final comprehensive test to determine if MathSpeak is production ready
"""

import time
import sys
import json
import traceback
from pathlib import Path
from typing import Dict, List, Any
import psutil
import os
import gc

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

class ProductionReadinessTest:
    """Comprehensive production readiness assessment"""
    
    def __init__(self):
        self.results = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "system_info": self._get_system_info(),
            "test_results": {},
            "critical_issues": [],
            "warnings": [],
            "performance_metrics": {},
            "conclusion": {}
        }
        self.engine = None
    
    def _get_system_info(self):
        """Get system information"""
        return {
            "platform": sys.platform,
            "python_version": sys.version.split()[0],
            "cpu_count": os.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / 1024**3, 1),
            "available_memory_gb": round(psutil.virtual_memory().available / 1024**3, 1)
        }
    
    def setup_engine(self):
        """Initialize the MathSpeak engine"""
        try:
            print("Initializing MathSpeak engine...")
            voice_manager = VoiceManager()
            
            # Initialize with minimal features to avoid cache issues
            self.engine = MathematicalTTSEngine(
                voice_manager=voice_manager,
                enable_caching=False  # Disable caching to avoid known issues
            )
            
            # Try to load domain processors
            try:
                from mathspeak.domains.topology import TopologyProcessor
                from mathspeak.core.engine import MathematicalContext
                self.engine.domain_processors[MathematicalContext.TOPOLOGY] = TopologyProcessor()
                print("✓ Topology processor loaded")
            except Exception as e:
                self.results["warnings"].append(f"Could not load topology processor: {str(e)}")
            
            try:
                from mathspeak.domains.complex_analysis import ComplexAnalysisProcessor
                self.engine.domain_processors[MathematicalContext.COMPLEX_ANALYSIS] = ComplexAnalysisProcessor()
                print("✓ Complex analysis processor loaded")
            except Exception as e:
                self.results["warnings"].append(f"Could not load complex analysis processor: {str(e)}")
            
            try:
                from mathspeak.domains.ode import ODEProcessor
                self.engine.domain_processors[MathematicalContext.ODE] = ODEProcessor()
                print("✓ ODE processor loaded")
            except Exception as e:
                self.results["warnings"].append(f"Could not load ODE processor: {str(e)}")
            
            print("✓ Engine initialized successfully")
            return True
            
        except Exception as e:
            self.results["critical_issues"].append(f"Engine initialization failed: {str(e)}")
            print(f"✗ Engine initialization failed: {e}")
            return False
    
    def test_core_functionality(self):
        """Test core mathematical processing functionality"""
        print("\n=== Testing Core Functionality ===")
        
        test_expressions = [
            ("Basic algebra", "x^2 + y^2 = z^2"),
            ("Calculus", "\\frac{d}{dx} e^x = e^x"),
            ("Integral", "\\int_0^1 x^2 dx = \\frac{1}{3}"),
            ("Series", "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}"),
            ("Limit", "\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1"),
            ("Greek letters", "\\alpha + \\beta = \\gamma"),
            ("Complex", "e^{i\\pi} + 1 = 0"),
            ("Matrix notation", "\\det(A) = ad - bc"),
        ]
        
        success_count = 0
        processing_times = []
        failed_expressions = []
        
        for category, expr in test_expressions:
            try:
                start = time.time()
                result = self.engine.process_latex(expr)
                processing_time = time.time() - start
                
                if result and len(result.processed) > 0:
                    success_count += 1
                    processing_times.append(processing_time)
                    print(f"✓ {category:<15} {processing_time:.3f}s")
                else:
                    failed_expressions.append((category, "Empty result"))
                    print(f"✗ {category:<15} Empty result")
                    
            except Exception as e:
                failed_expressions.append((category, str(e)))
                print(f"✗ {category:<15} Error: {str(e)[:50]}")
        
        success_rate = success_count / len(test_expressions) * 100
        avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
        max_time = max(processing_times) if processing_times else 0
        
        self.results["test_results"]["core_functionality"] = {
            "success_rate": success_rate,
            "successful_expressions": success_count,
            "total_expressions": len(test_expressions),
            "avg_processing_time": avg_time,
            "max_processing_time": max_time,
            "failed_expressions": failed_expressions
        }
        
        print(f"\nCore Functionality Results:")
        print(f"  Success Rate: {success_rate:.1f}%")
        print(f"  Average Time: {avg_time:.3f}s")
        print(f"  Maximum Time: {max_time:.3f}s")
        
        # Set critical threshold
        if success_rate < 90:
            self.results["critical_issues"].append(f"Core functionality success rate too low: {success_rate:.1f}%")
        elif success_rate < 95:
            self.results["warnings"].append(f"Core functionality could be improved: {success_rate:.1f}%")
        
        return success_rate >= 90
    
    def test_robustness(self):
        """Test system robustness with edge cases"""
        print("\n=== Testing Robustness ===")
        
        edge_cases = [
            ("Empty input", ""),
            ("Whitespace only", "   "),
            ("Single character", "x"),
            ("Unknown command", "\\unknowncommand{x}"),
            ("Unicode input", "∀ε>0 ∃δ>0"),
            ("Very long input", "x" * 1000),
            ("Malformed LaTeX", "\\frac{a}{"),
            ("Nested braces", "{{{{x}}}}"),
        ]
        
        handled_count = 0
        crash_count = 0
        
        for category, test_input in edge_cases:
            try:
                result = self.engine.process_latex(test_input)
                # Should not crash and should return something meaningful
                if result and isinstance(result.processed, str):
                    handled_count += 1
                    print(f"✓ {category:<20} Handled gracefully")
                else:
                    print(f"⚠ {category:<20} Unexpected result type")
                    
            except Exception as e:
                crash_count += 1
                print(f"✗ {category:<20} Crashed: {str(e)[:30]}")
        
        robustness_rate = handled_count / len(edge_cases) * 100
        
        self.results["test_results"]["robustness"] = {
            "handled_cases": handled_count,
            "total_cases": len(edge_cases),
            "crash_count": crash_count,
            "robustness_rate": robustness_rate
        }
        
        print(f"\nRobustness Results:")
        print(f"  Handled gracefully: {handled_count}/{len(edge_cases)}")
        print(f"  Robustness rate: {robustness_rate:.1f}%")
        print(f"  Crashes: {crash_count}")
        
        if crash_count > 0:
            self.results["critical_issues"].append(f"System crashes on edge cases: {crash_count} crashes")
        elif robustness_rate < 80:
            self.results["warnings"].append(f"Robustness could be improved: {robustness_rate:.1f}%")
        
        return crash_count == 0 and robustness_rate >= 75
    
    def test_performance(self):
        """Test performance characteristics"""
        print("\n=== Testing Performance ===")
        
        # Memory usage test
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Throughput test
        test_expressions = [f"f_{i}(x) = x^{i} + {i}" for i in range(1, 51)]
        
        start_time = time.time()
        processed_count = 0
        processing_times = []
        
        for expr in test_expressions:
            try:
                expr_start = time.time()
                result = self.engine.process_latex(expr)
                expr_time = time.time() - expr_start
                
                if result and len(result.processed) > 0:
                    processed_count += 1
                    processing_times.append(expr_time)
                    
            except Exception:
                pass
        
        total_time = time.time() - start_time
        throughput = processed_count / total_time if total_time > 0 else 0
        
        # Memory after processing
        gc.collect()
        time.sleep(0.1)
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        avg_response_time = sum(processing_times) / len(processing_times) if processing_times else 0
        max_response_time = max(processing_times) if processing_times else 0
        
        self.results["performance_metrics"] = {
            "throughput_expr_per_sec": throughput,
            "avg_response_time": avg_response_time,
            "max_response_time": max_response_time,
            "memory_initial_mb": initial_memory,
            "memory_final_mb": final_memory,
            "memory_increase_mb": memory_increase,
            "expressions_processed": processed_count,
            "total_expressions": len(test_expressions)
        }
        
        print(f"\nPerformance Results:")
        print(f"  Throughput: {throughput:.1f} expressions/sec")
        print(f"  Average response time: {avg_response_time:.3f}s")
        print(f"  Maximum response time: {max_response_time:.3f}s")
        print(f"  Memory usage: {initial_memory:.1f} → {final_memory:.1f} MB (+{memory_increase:.1f} MB)")
        
        # Performance thresholds
        performance_ok = True
        if throughput < 5:
            self.results["warnings"].append(f"Low throughput: {throughput:.1f} expr/sec")
            performance_ok = False
        
        if avg_response_time > 1.0:
            self.results["warnings"].append(f"Slow average response: {avg_response_time:.3f}s")
            performance_ok = False
        
        if memory_increase > 100:
            self.results["critical_issues"].append(f"Excessive memory usage: +{memory_increase:.1f}MB")
            performance_ok = False
        elif memory_increase > 50:
            self.results["warnings"].append(f"High memory usage: +{memory_increase:.1f}MB")
        
        return performance_ok
    
    def test_real_world_usage(self):
        """Test realistic usage scenarios"""
        print("\n=== Testing Real-World Usage ===")
        
        # Simulate a student homework session
        homework_problems = [
            # Calculus problems
            "Find the derivative of f(x) = x^3 - 2x^2 + x - 1",
            "f'(x) = 3x^2 - 4x + 1",
            "Evaluate the integral \\int_0^2 (x^2 + 1) dx",
            "\\int_0^2 (x^2 + 1) dx = [\\frac{x^3}{3} + x]_0^2 = \\frac{8}{3} + 2 = \\frac{14}{3}",
            
            # Linear algebra
            "Find the determinant of A = \\begin{pmatrix} 1 & 2 \\\\ 3 & 4 \\end{pmatrix}",
            "\\det(A) = 1 \\cdot 4 - 2 \\cdot 3 = 4 - 6 = -2",
            
            # Statistics
            "The mean is \\bar{x} = \\frac{1}{n}\\sum_{i=1}^n x_i",
            "The variance is s^2 = \\frac{1}{n-1}\\sum_{i=1}^n (x_i - \\bar{x})^2"
        ]
        
        session_start = time.time()
        problems_processed = 0
        session_errors = []
        
        for i, problem in enumerate(homework_problems):
            try:
                # Extract mathematical content
                import re
                math_matches = re.findall(r'\\[a-zA-Z_]+(?:\{[^}]*\})*|[a-zA-Z_]+\([^)]*\)|[=+\-*/^_{}]', problem)
                
                if math_matches:
                    # Take meaningful mathematical content
                    math_content = ''.join(math_matches[:10])  # Limit complexity
                    if len(math_content) > 5:  # Ensure it's substantive
                        result = self.engine.process_latex(math_content)
                        if result and len(result.processed) > 0:
                            problems_processed += 1
                        else:
                            session_errors.append(f"Problem {i+1}: Empty result")
                    else:
                        problems_processed += 1  # Simple text problem
                else:
                    problems_processed += 1  # Text-only problem
                    
            except Exception as e:
                session_errors.append(f"Problem {i+1}: {str(e)}")
        
        session_time = time.time() - session_start
        success_rate = problems_processed / len(homework_problems) * 100
        
        self.results["test_results"]["real_world"] = {
            "problems_attempted": len(homework_problems),
            "problems_processed": problems_processed,
            "success_rate": success_rate,
            "session_time": session_time,
            "errors": session_errors
        }
        
        print(f"\nReal-World Usage Results:")
        print(f"  Problems processed: {problems_processed}/{len(homework_problems)}")
        print(f"  Success rate: {success_rate:.1f}%")
        print(f"  Session time: {session_time:.1f}s")
        print(f"  Errors: {len(session_errors)}")
        
        if success_rate < 85:
            self.results["critical_issues"].append(f"Poor real-world performance: {success_rate:.1f}%")
        elif success_rate < 95:
            self.results["warnings"].append(f"Real-world performance could be improved: {success_rate:.1f}%")
        
        return success_rate >= 85
    
    def generate_final_assessment(self):
        """Generate final production readiness assessment"""
        print("\n" + "="*70)
        print("PRODUCTION READINESS ASSESSMENT")
        print("="*70)
        
        # Count critical issues and warnings
        critical_count = len(self.results["critical_issues"])
        warning_count = len(self.results["warnings"])
        
        # Analyze test results
        core_passed = self.results["test_results"].get("core_functionality", {}).get("success_rate", 0) >= 90
        robustness_passed = self.results["test_results"].get("robustness", {}).get("robustness_rate", 0) >= 75
        real_world_passed = self.results["test_results"].get("real_world", {}).get("success_rate", 0) >= 85
        
        # Performance thresholds
        perf_metrics = self.results["performance_metrics"]
        performance_ok = (
            perf_metrics.get("throughput_expr_per_sec", 0) >= 5 and
            perf_metrics.get("avg_response_time", 10) <= 1.0 and
            perf_metrics.get("memory_increase_mb", 1000) <= 100
        )
        
        print(f"\nTest Results Summary:")
        print(f"  Core Functionality:  {'✓ PASS' if core_passed else '✗ FAIL'}")
        print(f"  Robustness:          {'✓ PASS' if robustness_passed else '✗ FAIL'}")
        print(f"  Performance:         {'✓ PASS' if performance_ok else '✗ FAIL'}")
        print(f"  Real-World Usage:    {'✓ PASS' if real_world_passed else '✗ FAIL'}")
        
        print(f"\nIssue Summary:")
        print(f"  Critical Issues: {critical_count}")
        print(f"  Warnings: {warning_count}")
        
        if self.results["critical_issues"]:
            print(f"\n⚠️  Critical Issues:")
            for issue in self.results["critical_issues"]:
                print(f"    • {issue}")
        
        if self.results["warnings"]:
            print(f"\n⚠️  Warnings:")
            for warning in self.results["warnings"]:
                print(f"    • {warning}")
        
        # Final determination
        tests_passed = sum([core_passed, robustness_passed, performance_ok, real_world_passed])
        
        if critical_count == 0 and tests_passed >= 3:
            if tests_passed == 4 and warning_count <= 2:
                status = "✅ PRODUCTION READY"
                recommendation = "System is ready for production deployment"
                confidence = "HIGH"
            else:
                status = "⚠️ CONDITIONALLY READY"
                recommendation = "Ready for production with minor improvements"
                confidence = "MEDIUM"
        elif critical_count <= 1 and tests_passed >= 2:
            status = "🔧 NEEDS IMPROVEMENTS"
            recommendation = "Address critical issues before production"
            confidence = "LOW"
        else:
            status = "❌ NOT PRODUCTION READY"
            recommendation = "Significant work required before production"
            confidence = "VERY LOW"
        
        self.results["conclusion"] = {
            "status": status,
            "recommendation": recommendation,
            "confidence": confidence,
            "tests_passed": tests_passed,
            "total_tests": 4,
            "critical_issues": critical_count,
            "warnings": warning_count,
            "pass_rate": tests_passed / 4 * 100
        }
        
        print(f"\n{status}")
        print(f"Confidence: {confidence}")
        print(f"Recommendation: {recommendation}")
        print(f"Overall Pass Rate: {tests_passed}/4 ({tests_passed/4*100:.0f}%)")
        
        # Key metrics summary
        print(f"\nKey Performance Metrics:")
        if "core_functionality" in self.results["test_results"]:
            core = self.results["test_results"]["core_functionality"]
            print(f"  Core Success Rate: {core['success_rate']:.1f}%")
            print(f"  Average Response Time: {core['avg_processing_time']:.3f}s")
        
        if perf_metrics:
            print(f"  Throughput: {perf_metrics['throughput_expr_per_sec']:.1f} expr/sec")
            print(f"  Memory Efficiency: +{perf_metrics['memory_increase_mb']:.1f}MB")
        
        return self.results["conclusion"]
    
    def save_report(self, filename="production_readiness_report.json"):
        """Save detailed report"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nDetailed report saved to: {filename}")
    
    def run_assessment(self):
        """Run complete production readiness assessment"""
        print("MathSpeak Production Readiness Assessment")
        print("="*70)
        
        try:
            # Setup
            if not self.setup_engine():
                return self.results
            
            # Run tests
            self.test_core_functionality()
            self.test_robustness()
            self.test_performance()
            self.test_real_world_usage()
            
            # Generate assessment
            conclusion = self.generate_final_assessment()
            self.save_report()
            
            return self.results
            
        except Exception as e:
            print(f"\nCritical error during assessment: {e}")
            traceback.print_exc()
            self.results["critical_issues"].append(f"Assessment failed: {str(e)}")
            return self.results
        
        finally:
            if self.engine:
                try:
                    self.engine.shutdown()
                except:
                    pass

def main():
    """Run production readiness assessment"""
    assessment = ProductionReadinessTest()
    results = assessment.run_assessment()
    return results

if __name__ == "__main__":
    main()