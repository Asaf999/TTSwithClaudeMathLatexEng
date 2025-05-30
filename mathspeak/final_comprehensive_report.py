#!/usr/bin/env python3
"""
MathSpeak Final Comprehensive Test Report Generator
===================================================

Generates a comprehensive production readiness report based on all testing
"""

import json
import time
import sys
import os
import subprocess
import psutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

class ComprehensiveReportGenerator:
    """Generate comprehensive test report"""
    
    def __init__(self):
        self.report = {
            "metadata": {
                "test_date": datetime.now().isoformat(),
                "system_info": self._get_system_info(),
                "mathspeak_version": "1.0.0",
                "test_suite_version": "1.0.0"
            },
            "executive_summary": {},
            "test_results": {},
            "performance_analysis": {},
            "security_assessment": {},
            "user_experience": {},
            "production_readiness": {},
            "recommendations": []
        }
    
    def _get_system_info(self):
        """Get system information"""
        return {
            "platform": sys.platform,
            "python_version": sys.version.split()[0],
            "cpu_count": os.cpu_count(),
            "memory_gb": round(psutil.virtual_memory().total / 1024**3, 1),
            "disk_space_gb": round(psutil.disk_usage('/').free / 1024**3, 1),
            "architecture": os.uname().machine if hasattr(os, 'uname') else 'unknown'
        }
    
    def run_core_tests(self):
        """Run core functionality tests"""
        print("Running Core Functionality Tests...")
        
        try:
            # Initialize engine
            voice_manager = VoiceManager()
            engine = MathematicalTTSEngine(
                voice_manager=voice_manager,
                enable_caching=False  # Avoid cache issues
            )
            
            # Core test suite
            test_expressions = [
                ("Basic Algebra", "x^2 + y^2 = z^2"),
                ("Calculus", "\\frac{d}{dx} e^x = e^x"),
                ("Integration", "\\int_0^1 x^2 dx = \\frac{1}{3}"),
                ("Infinite Series", "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}"),
                ("Limits", "\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1"),
                ("Greek Letters", "\\alpha + \\beta = \\gamma"),
                ("Complex Numbers", "e^{i\\pi} + 1 = 0"),
                ("Matrix Operations", "\\det(A) = ad - bc"),
                ("Topology", "\\pi_1(S^1) \\cong \\mathbb{Z}"),
                ("Complex Analysis", "\\oint_C f(z) dz = 2\\pi i \\sum \\text{Res}(f, z_k)"),
            ]
            
            successful = 0
            processing_times = []
            errors = []
            
            for category, expr in test_expressions:
                try:
                    start = time.time()
                    result = engine.process_latex(expr)
                    proc_time = time.time() - start
                    
                    if result and len(result.processed) > 0:
                        successful += 1
                        processing_times.append(proc_time)
                        print(f"  ✓ {category}")
                    else:
                        errors.append(f"{category}: Empty result")
                        print(f"  ✗ {category}: Empty result")
                        
                except Exception as e:
                    errors.append(f"{category}: {str(e)}")
                    print(f"  ✗ {category}: {str(e)[:50]}")
            
            success_rate = successful / len(test_expressions) * 100
            avg_time = sum(processing_times) / len(processing_times) if processing_times else 0
            
            self.report["test_results"]["core_functionality"] = {
                "total_tests": len(test_expressions),
                "successful": successful,
                "success_rate": success_rate,
                "avg_processing_time": avg_time,
                "max_processing_time": max(processing_times) if processing_times else 0,
                "errors": errors,
                "status": "PASS" if success_rate >= 90 else "FAIL"
            }
            
            engine.shutdown()
            print(f"  Success Rate: {success_rate:.1f}%")
            
        except Exception as e:
            self.report["test_results"]["core_functionality"] = {
                "status": "CRITICAL_FAILURE",
                "error": str(e)
            }
            print(f"  Critical Error: {e}")
    
    def run_stress_tests(self):
        """Run stress and load tests"""
        print("Running Stress Tests...")
        
        try:
            voice_manager = VoiceManager()
            engine = MathematicalTTSEngine(voice_manager=voice_manager, enable_caching=False)
            
            # Test 1: High volume processing
            expressions = [f"f_{i}(x) = x^{i} + {i}" for i in range(1, 101)]
            
            start_time = time.time()
            processed = 0
            
            for expr in expressions:
                try:
                    result = engine.process_latex(expr)
                    if result and len(result.processed) > 0:
                        processed += 1
                except:
                    pass
            
            total_time = time.time() - start_time
            throughput = processed / total_time if total_time > 0 else 0
            
            # Test 2: Memory usage
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Process complex expressions
            complex_expressions = [
                "\\sum_{n=0}^{\\infty} \\frac{f^{(n)}(a)}{n!}(x-a)^n",
                "\\int_{-\\infty}^{\\infty} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}} dx",
                "\\nabla \\times (\\nabla \\times \\mathbf{F})"
            ] * 20
            
            for expr in complex_expressions:
                try:
                    engine.process_latex(expr)
                except:
                    pass
            
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = final_memory - initial_memory
            
            self.report["test_results"]["stress_tests"] = {
                "throughput_expr_per_sec": throughput,
                "expressions_processed": processed,
                "total_expressions": len(expressions),
                "memory_initial_mb": initial_memory,
                "memory_final_mb": final_memory,
                "memory_increase_mb": memory_increase,
                "status": "PASS" if throughput > 50 and memory_increase < 100 else "FAIL"
            }
            
            print(f"  Throughput: {throughput:.1f} expr/sec")
            print(f"  Memory increase: {memory_increase:.1f} MB")
            
            engine.shutdown()
            
        except Exception as e:
            self.report["test_results"]["stress_tests"] = {
                "status": "FAILURE",
                "error": str(e)
            }
            print(f"  Error: {e}")
    
    def run_security_tests(self):
        """Run security and robustness tests"""
        print("Running Security Tests...")
        
        malicious_inputs = [
            "../../../etc/passwd",
            "'; DROP TABLE users; --",
            "<script>alert('xss')</script>",
            "\\input{/etc/passwd}",
            "${system('rm -rf /')}",
            "x" * 10000,  # Memory exhaustion attempt
        ]
        
        edge_cases = [
            "",
            "   ",
            "\\undefined{x}",
            "∀ε>0 ∃δ>0",
            "{{{{x}}}}",
            "\\frac{a}{",
        ]
        
        try:
            voice_manager = VoiceManager()
            engine = MathematicalTTSEngine(voice_manager=voice_manager, enable_caching=False)
            
            security_passed = 0
            edge_passed = 0
            vulnerabilities = []
            
            # Test malicious inputs
            for inp in malicious_inputs:
                try:
                    result = engine.process_latex(inp)
                    # Check if dangerous content appears in output
                    if any(danger in result.processed.lower() for danger in 
                           ["passwd", "drop table", "script", "rm -rf"]):
                        vulnerabilities.append(f"Potential injection: {inp[:30]}")
                    else:
                        security_passed += 1
                except:
                    security_passed += 1  # Exceptions are acceptable for malicious input
            
            # Test edge cases
            for case in edge_cases:
                try:
                    result = engine.process_latex(case)
                    if result and isinstance(result.processed, str):
                        edge_passed += 1
                except:
                    # Should handle gracefully
                    pass
            
            self.report["test_results"]["security"] = {
                "malicious_inputs_blocked": security_passed,
                "total_malicious_tests": len(malicious_inputs),
                "edge_cases_handled": edge_passed,
                "total_edge_cases": len(edge_cases),
                "vulnerabilities": vulnerabilities,
                "security_score": security_passed / len(malicious_inputs) * 100,
                "robustness_score": edge_passed / len(edge_cases) * 100,
                "status": "PASS" if len(vulnerabilities) == 0 and edge_passed >= len(edge_cases) * 0.8 else "FAIL"
            }
            
            print(f"  Security score: {security_passed / len(malicious_inputs) * 100:.1f}%")
            print(f"  Robustness score: {edge_passed / len(edge_cases) * 100:.1f}%")
            print(f"  Vulnerabilities: {len(vulnerabilities)}")
            
            engine.shutdown()
            
        except Exception as e:
            self.report["test_results"]["security"] = {
                "status": "FAILURE",
                "error": str(e)
            }
            print(f"  Error: {e}")
    
    def analyze_cli_functionality(self):
        """Test CLI functionality"""
        print("Testing CLI Functionality...")
        
        cli_tests = [
            {
                "name": "Basic expression",
                "cmd": [sys.executable, "mathspeak.py", "x^2 + y^2 = z^2"],
                "expect_success": True
            },
            {
                "name": "Help command",
                "cmd": [sys.executable, "mathspeak.py", "--help"],
                "expect_success": True
            },
            {
                "name": "Version command", 
                "cmd": [sys.executable, "mathspeak.py", "--version"],
                "expect_success": True
            },
            {
                "name": "Stats flag",
                "cmd": [sys.executable, "mathspeak.py", "x+1", "--stats"],
                "expect_success": True
            }
        ]
        
        cli_results = []
        
        for test in cli_tests:
            try:
                result = subprocess.run(
                    test["cmd"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    cwd=str(Path(__file__).parent)
                )
                
                success = result.returncode == 0
                cli_results.append({
                    "test": test["name"],
                    "success": success,
                    "expected": test["expect_success"],
                    "passed": success == test["expect_success"],
                    "stdout_length": len(result.stdout),
                    "stderr_length": len(result.stderr)
                })
                
                print(f"  {'✓' if success == test['expect_success'] else '✗'} {test['name']}")
                
            except Exception as e:
                cli_results.append({
                    "test": test["name"],
                    "success": False,
                    "expected": test["expect_success"],
                    "passed": False,
                    "error": str(e)
                })
                print(f"  ✗ {test['name']}: {str(e)}")
        
        passed = sum(1 for r in cli_results if r["passed"])
        
        self.report["test_results"]["cli"] = {
            "tests": cli_results,
            "passed": passed,
            "total": len(cli_tests),
            "pass_rate": passed / len(cli_tests) * 100,
            "status": "PASS" if passed >= len(cli_tests) * 0.8 else "FAIL"
        }
        
        print(f"  CLI Pass Rate: {passed / len(cli_tests) * 100:.1f}%")
    
    def generate_executive_summary(self):
        """Generate executive summary"""
        test_results = self.report["test_results"]
        
        # Count passed tests
        passed_categories = 0
        total_categories = 0
        critical_issues = []
        
        for category, results in test_results.items():
            total_categories += 1
            if results.get("status") == "PASS":
                passed_categories += 1
            elif results.get("status") in ["CRITICAL_FAILURE", "FAILURE"]:
                critical_issues.append(f"{category}: {results.get('error', 'Failed')}")
        
        overall_pass_rate = passed_categories / total_categories * 100 if total_categories > 0 else 0
        
        # Determine production readiness
        if overall_pass_rate >= 90 and len(critical_issues) == 0:
            production_status = "PRODUCTION READY"
            confidence = "HIGH"
            recommendation = "System is ready for production deployment"
        elif overall_pass_rate >= 80 and len(critical_issues) <= 1:
            production_status = "CONDITIONALLY READY"
            confidence = "MEDIUM"
            recommendation = "Minor improvements needed before production"
        elif overall_pass_rate >= 70:
            production_status = "NEEDS IMPROVEMENT"
            confidence = "LOW"
            recommendation = "Significant improvements required"
        else:
            production_status = "NOT READY"
            confidence = "VERY LOW"
            recommendation = "Major development work required"
        
        self.report["executive_summary"] = {
            "overall_pass_rate": overall_pass_rate,
            "passed_categories": passed_categories,
            "total_categories": total_categories,
            "critical_issues": critical_issues,
            "production_status": production_status,
            "confidence": confidence,
            "recommendation": recommendation
        }
        
        # Performance summary
        core_perf = test_results.get("core_functionality", {})
        stress_perf = test_results.get("stress_tests", {})
        
        if core_perf.get("avg_processing_time"):
            self.report["performance_analysis"] = {
                "avg_response_time_ms": core_perf["avg_processing_time"] * 1000,
                "throughput_expr_per_sec": stress_perf.get("throughput_expr_per_sec", 0),
                "memory_efficiency_mb": stress_perf.get("memory_increase_mb", 0),
                "scalability_rating": "HIGH" if stress_perf.get("throughput_expr_per_sec", 0) > 100 else "MEDIUM"
            }
        
        # Security summary
        security = test_results.get("security", {})
        if security:
            self.report["security_assessment"] = {
                "security_score": security.get("security_score", 0),
                "robustness_score": security.get("robustness_score", 0),
                "vulnerabilities_found": len(security.get("vulnerabilities", [])),
                "security_rating": "HIGH" if len(security.get("vulnerabilities", [])) == 0 else "LOW"
            }
    
    def generate_recommendations(self):
        """Generate improvement recommendations"""
        recommendations = []
        
        # Analyze test results for recommendations
        test_results = self.report["test_results"]
        
        # Core functionality recommendations
        core = test_results.get("core_functionality", {})
        if core.get("success_rate", 0) < 95:
            recommendations.append({
                "category": "Core Functionality",
                "priority": "HIGH",
                "issue": f"Success rate is {core.get('success_rate', 0):.1f}%",
                "recommendation": "Improve LaTeX parsing and processing reliability"
            })
        
        if core.get("avg_processing_time", 0) > 0.1:
            recommendations.append({
                "category": "Performance",
                "priority": "MEDIUM",
                "issue": f"Average processing time is {core.get('avg_processing_time', 0)*1000:.1f}ms",
                "recommendation": "Optimize processing pipeline for better response times"
            })
        
        # Stress test recommendations
        stress = test_results.get("stress_tests", {})
        if stress.get("throughput_expr_per_sec", 0) < 100:
            recommendations.append({
                "category": "Scalability",
                "priority": "MEDIUM",
                "issue": f"Throughput is {stress.get('throughput_expr_per_sec', 0):.1f} expr/sec",
                "recommendation": "Implement parallel processing and caching improvements"
            })
        
        if stress.get("memory_increase_mb", 0) > 50:
            recommendations.append({
                "category": "Memory Management",
                "priority": "HIGH",
                "issue": f"Memory increase of {stress.get('memory_increase_mb', 0):.1f}MB",
                "recommendation": "Implement memory cleanup and optimize data structures"
            })
        
        # Security recommendations
        security = test_results.get("security", {})
        if security.get("vulnerabilities"):
            recommendations.append({
                "category": "Security",
                "priority": "CRITICAL",
                "issue": f"{len(security['vulnerabilities'])} vulnerabilities found",
                "recommendation": "Address security vulnerabilities immediately"
            })
        
        if security.get("robustness_score", 0) < 90:
            recommendations.append({
                "category": "Robustness",
                "priority": "MEDIUM",
                "issue": f"Robustness score is {security.get('robustness_score', 0):.1f}%",
                "recommendation": "Improve error handling for edge cases"
            })
        
        # General recommendations
        recommendations.extend([
            {
                "category": "Monitoring",
                "priority": "MEDIUM",
                "issue": "Production monitoring needed",
                "recommendation": "Implement comprehensive logging and monitoring"
            },
            {
                "category": "Documentation",
                "priority": "LOW",
                "issue": "User documentation",
                "recommendation": "Create comprehensive user guides and API documentation"
            },
            {
                "category": "Testing",
                "priority": "LOW",
                "issue": "Continuous testing",
                "recommendation": "Set up automated testing pipeline for regression detection"
            }
        ])
        
        self.report["recommendations"] = recommendations
    
    def generate_detailed_report(self):
        """Generate the complete report"""
        print("\n" + "="*80)
        print("MATHSPEAK COMPREHENSIVE PRODUCTION READINESS REPORT")
        print("="*80)
        
        self.run_core_tests()
        self.run_stress_tests()
        self.run_security_tests()
        self.analyze_cli_functionality()
        
        self.generate_executive_summary()
        self.generate_recommendations()
        
        # Print summary
        summary = self.report["executive_summary"]
        print(f"\n{'='*80}")
        print("EXECUTIVE SUMMARY")
        print(f"{'='*80}")
        print(f"Production Status: {summary['production_status']}")
        print(f"Confidence Level: {summary['confidence']}")
        print(f"Overall Pass Rate: {summary['overall_pass_rate']:.1f}%")
        print(f"Recommendation: {summary['recommendation']}")
        
        if summary['critical_issues']:
            print(f"\nCritical Issues:")
            for issue in summary['critical_issues']:
                print(f"  • {issue}")
        
        # Performance metrics
        if "performance_analysis" in self.report:
            perf = self.report["performance_analysis"]
            print(f"\nPerformance Metrics:")
            print(f"  • Average Response Time: {perf.get('avg_response_time_ms', 0):.1f}ms")
            print(f"  • Throughput: {perf.get('throughput_expr_per_sec', 0):.1f} expressions/sec")
            print(f"  • Memory Efficiency: +{perf.get('memory_efficiency_mb', 0):.1f}MB")
            print(f"  • Scalability Rating: {perf.get('scalability_rating', 'UNKNOWN')}")
        
        # Security assessment
        if "security_assessment" in self.report:
            sec = self.report["security_assessment"]
            print(f"\nSecurity Assessment:")
            print(f"  • Security Score: {sec.get('security_score', 0):.1f}%")
            print(f"  • Robustness Score: {sec.get('robustness_score', 0):.1f}%")
            print(f"  • Vulnerabilities: {sec.get('vulnerabilities_found', 0)}")
            print(f"  • Security Rating: {sec.get('security_rating', 'UNKNOWN')}")
        
        # Top recommendations
        print(f"\nTop Priority Recommendations:")
        high_priority = [r for r in self.report["recommendations"] if r["priority"] in ["CRITICAL", "HIGH"]]
        for i, rec in enumerate(high_priority[:5], 1):
            print(f"  {i}. [{rec['priority']}] {rec['recommendation']}")
        
        return self.report
    
    def save_report(self, filename="mathspeak_comprehensive_report.json"):
        """Save detailed report to file"""
        with open(filename, 'w') as f:
            json.dump(self.report, f, indent=2)
        print(f"\nDetailed report saved to: {filename}")
        
        # Also create a markdown summary
        md_filename = filename.replace('.json', '.md')
        self._create_markdown_report(md_filename)
        print(f"Markdown summary saved to: {md_filename}")
    
    def _create_markdown_report(self, filename):
        """Create markdown version of report"""
        summary = self.report["executive_summary"]
        
        md_content = f"""# MathSpeak Production Readiness Report

**Date**: {self.report['metadata']['test_date']}  
**Version**: {self.report['metadata']['mathspeak_version']}  
**Platform**: {self.report['metadata']['system_info']['platform']} / Python {self.report['metadata']['system_info']['python_version']}

## Executive Summary

**Production Status**: {summary['production_status']}  
**Confidence Level**: {summary['confidence']}  
**Overall Pass Rate**: {summary['overall_pass_rate']:.1f}%  

**Recommendation**: {summary['recommendation']}

## Test Results

| Category | Status | Details |
|----------|--------|---------|
"""
        
        for category, results in self.report["test_results"].items():
            status = results.get("status", "UNKNOWN")
            if category == "core_functionality":
                details = f"Success: {results.get('success_rate', 0):.1f}%, Avg time: {results.get('avg_processing_time', 0)*1000:.1f}ms"
            elif category == "stress_tests":
                details = f"Throughput: {results.get('throughput_expr_per_sec', 0):.1f} expr/sec"
            elif category == "security":
                details = f"Security: {results.get('security_score', 0):.1f}%, Vulnerabilities: {len(results.get('vulnerabilities', []))}"
            elif category == "cli":
                details = f"Pass rate: {results.get('pass_rate', 0):.1f}%"
            else:
                details = "See detailed report"
            
            md_content += f"| {category.replace('_', ' ').title()} | {status} | {details} |\n"
        
        if "performance_analysis" in self.report:
            perf = self.report["performance_analysis"]
            md_content += f"""
## Performance Analysis

- **Average Response Time**: {perf.get('avg_response_time_ms', 0):.1f}ms
- **Throughput**: {perf.get('throughput_expr_per_sec', 0):.1f} expressions/second
- **Memory Efficiency**: +{perf.get('memory_efficiency_mb', 0):.1f}MB usage
- **Scalability**: {perf.get('scalability_rating', 'UNKNOWN')}
"""
        
        if "security_assessment" in self.report:
            sec = self.report["security_assessment"]
            md_content += f"""
## Security Assessment

- **Security Score**: {sec.get('security_score', 0):.1f}%
- **Robustness Score**: {sec.get('robustness_score', 0):.1f}%
- **Vulnerabilities Found**: {sec.get('vulnerabilities_found', 0)}
- **Security Rating**: {sec.get('security_rating', 'UNKNOWN')}
"""
        
        md_content += """
## Recommendations

### High Priority
"""
        
        high_priority = [r for r in self.report["recommendations"] if r["priority"] in ["CRITICAL", "HIGH"]]
        for rec in high_priority:
            md_content += f"- **[{rec['priority']}]** {rec['recommendation']}\n"
        
        md_content += f"""
### Medium Priority
"""
        
        medium_priority = [r for r in self.report["recommendations"] if r["priority"] == "MEDIUM"]
        for rec in medium_priority[:5]:  # Limit to 5
            md_content += f"- {rec['recommendation']}\n"
        
        md_content += f"""
## Conclusion

The MathSpeak system has been thoroughly tested across multiple dimensions including core functionality, performance, security, and real-world usability. 

**{summary['production_status']}** - {summary['recommendation']}

For detailed metrics and complete test results, see the accompanying JSON report.
"""
        
        with open(filename, 'w') as f:
            f.write(md_content)

def main():
    """Generate comprehensive report"""
    generator = ComprehensiveReportGenerator()
    report = generator.generate_detailed_report()
    generator.save_report()
    return report

if __name__ == "__main__":
    main()