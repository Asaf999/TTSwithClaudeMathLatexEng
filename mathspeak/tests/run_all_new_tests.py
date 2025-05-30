#!/usr/bin/env python3
"""
Test Runner for All New Domain Tests
===================================

This script runs all the extensive tests for the newly implemented domains:
- Real Analysis
- Measure Theory
- Combinatorics  
- Algorithms

It also runs integration and edge case tests, providing a comprehensive
test report with coverage metrics and performance benchmarks.
"""

import sys
import time
import pytest
import logging
from pathlib import Path
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestRunner:
    """Orchestrates running all tests with reporting"""
    
    def __init__(self):
        self.test_files = {
            'Real Analysis': 'test_real_analysis.py',
            'Measure Theory': 'test_measure_theory.py',
            'Combinatorics': 'test_combinatorics.py',
            'Algorithms': 'test_algorithms.py',
            'Integration': 'test_new_domains_integration.py',
            'Edge Cases': 'test_edge_cases_comprehensive.py',
        }
        self.results = {}
        
    def run_all_tests(self, verbose=True):
        """Run all test suites"""
        logger.info("Starting comprehensive test suite for new domains")
        logger.info("=" * 70)
        
        total_start = time.time()
        total_passed = 0
        total_failed = 0
        
        for name, test_file in self.test_files.items():
            logger.info(f"\nRunning {name} tests...")
            start_time = time.time()
            
            # Run pytest for this test file
            args = [test_file]
            if verbose:
                args.extend(['-v', '--tb=short'])
            else:
                args.extend(['-q'])
            
            # Capture test results
            result = pytest.main(args)
            duration = time.time() - start_time
            
            # Store results
            self.results[name] = {
                'status': 'PASSED' if result == 0 else 'FAILED',
                'duration': duration,
                'exit_code': result
            }
            
            if result == 0:
                total_passed += 1
                logger.info(f"✓ {name} tests PASSED in {duration:.2f}s")
            else:
                total_failed += 1
                logger.error(f"✗ {name} tests FAILED in {duration:.2f}s")
        
        total_duration = time.time() - total_start
        
        # Print summary
        self._print_summary(total_passed, total_failed, total_duration)
        
        return total_failed == 0
    
    def run_specific_domain(self, domain: str, verbose=True):
        """Run tests for a specific domain"""
        if domain not in self.test_files:
            logger.error(f"Unknown domain: {domain}")
            logger.info(f"Available domains: {', '.join(self.test_files.keys())}")
            return False
        
        logger.info(f"Running {domain} tests...")
        test_file = self.test_files[domain]
        
        args = [test_file]
        if verbose:
            args.extend(['-v', '--tb=short'])
        
        result = pytest.main(args)
        return result == 0
    
    def run_performance_tests(self):
        """Run performance-focused tests"""
        logger.info("Running performance tests...")
        
        # Run tests with performance markers
        args = [
            '-v',
            '-k', 'performance',
            '--tb=short'
        ]
        
        result = pytest.main(args)
        return result == 0
    
    def run_coverage_analysis(self):
        """Run tests with coverage analysis"""
        logger.info("Running tests with coverage analysis...")
        
        try:
            import pytest_cov
        except ImportError:
            logger.error("pytest-cov not installed. Install with: pip install pytest-cov")
            return False
        
        args = [
            '--cov=domains',
            '--cov-report=term-missing',
            '--cov-report=html',
            '-v'
        ]
        args.extend(self.test_files.values())
        
        result = pytest.main(args)
        
        if result == 0:
            logger.info("Coverage report generated in htmlcov/index.html")
        
        return result == 0
    
    def _print_summary(self, passed: int, failed: int, duration: float):
        """Print test summary"""
        logger.info("\n" + "=" * 70)
        logger.info("TEST SUMMARY")
        logger.info("=" * 70)
        
        for name, result in self.results.items():
            status = "✓" if result['status'] == 'PASSED' else "✗"
            logger.info(f"{status} {name:20} {result['status']:8} ({result['duration']:.2f}s)")
        
        logger.info("-" * 70)
        logger.info(f"Total: {passed + failed} test suites")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Duration: {duration:.2f}s")
        logger.info("=" * 70)
        
        if failed == 0:
            logger.info("🎉 All tests passed!")
        else:
            logger.error(f"❌ {failed} test suite(s) failed")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run comprehensive tests for new MathSpeak domains"
    )
    parser.add_argument(
        '--domain',
        choices=['all', 'real_analysis', 'measure_theory', 'combinatorics', 
                 'algorithms', 'integration', 'edge_cases'],
        default='all',
        help='Specific domain to test (default: all)'
    )
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Reduce output verbosity'
    )
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Run with coverage analysis'
    )
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Run only performance tests'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick smoke tests only'
    )
    
    args = parser.parse_args()
    
    runner = TestRunner()
    success = True
    
    if args.coverage:
        success = runner.run_coverage_analysis()
    elif args.performance:
        success = runner.run_performance_tests()
    elif args.domain == 'all':
        success = runner.run_all_tests(verbose=not args.quiet)
    else:
        # Map command line domain to test name
        domain_map = {
            'real_analysis': 'Real Analysis',
            'measure_theory': 'Measure Theory',
            'combinatorics': 'Combinatorics',
            'algorithms': 'Algorithms',
            'integration': 'Integration',
            'edge_cases': 'Edge Cases',
        }
        success = runner.run_specific_domain(
            domain_map[args.domain],
            verbose=not args.quiet
        )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()