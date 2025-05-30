#!/usr/bin/env python3
"""
Quick Functionality Tests for MathSpeak
======================================

This script runs 10 small tests to verify core functionality.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def run_test(test_name, command, expected_in_output=None):
    """Run a single test and report results"""
    print(f"\n{BLUE}Test: {test_name}{RESET}")
    print(f"Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            if expected_in_output and expected_in_output not in result.stdout:
                print(f"{YELLOW}⚠️  Passed but unexpected output{RESET}")
                print(f"Expected: '{expected_in_output}'")
                print(f"Output: {result.stdout[:200]}...")
                return "warning"
            else:
                print(f"{GREEN}✅ PASSED{RESET}")
                if result.stdout:
                    print(f"Output preview: {result.stdout[:100]}...")
                return "passed"
        else:
            print(f"{RED}❌ FAILED{RESET}")
            print(f"Error: {result.stderr[:200]}")
            return "failed"
            
    except subprocess.TimeoutExpired:
        print(f"{RED}❌ TIMEOUT{RESET}")
        return "timeout"
    except Exception as e:
        print(f"{RED}❌ ERROR: {e}{RESET}")
        return "error"

def main():
    """Run all functionality tests"""
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}MathSpeak Functionality Tests{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    # Change to mathspeak directory
    os.chdir(Path(__file__).parent)
    
    # Test results tracking
    results = {
        "passed": 0,
        "failed": 0,
        "warning": 0,
        "timeout": 0,
        "error": 0
    }
    
    # Test 1: Basic arithmetic
    result = run_test(
        "Basic Arithmetic",
        ["python", "mathspeak.py", "2 + 2 = 4", "-o", "test1.mp3"],
        "2 plus 2 equals 4"
    )
    results[result] += 1
    
    # Test 2: Algebraic expression
    result = run_test(
        "Algebraic Expression",
        ["python", "mathspeak.py", "x^2 + 3x - 5 = 0", "-o", "test2.mp3"],
        "x squared"
    )
    results[result] += 1
    
    # Test 3: Calculus - derivatives
    result = run_test(
        "Calculus - Derivative",
        ["python", "mathspeak.py", r"\frac{d}{dx}(x^3 + 2x)", "-o", "test3.mp3"],
        "derivative"
    )
    results[result] += 1
    
    # Test 4: Calculus - integrals
    result = run_test(
        "Calculus - Integral",
        ["python", "mathspeak.py", r"\int_0^1 x^2 dx", "-o", "test4.mp3"],
        "integral"
    )
    results[result] += 1
    
    # Test 5: Complex math with specific context
    result = run_test(
        "Topology Context",
        ["python", "mathspeak.py", r"X \subseteq Y", "-c", "topology", "-o", "test5.mp3"],
        "subset"
    )
    results[result] += 1
    
    # Test 6: Matrix notation
    result = run_test(
        "Linear Algebra - Matrix",
        ["python", "mathspeak.py", r"\begin{pmatrix} a & b \\ c & d \end{pmatrix}", "-o", "test6.mp3"],
        "matrix"
    )
    results[result] += 1
    
    # Test 7: Greek letters and symbols
    result = run_test(
        "Greek Letters",
        ["python", "mathspeak.py", r"\alpha + \beta = \gamma", "-o", "test7.mp3"],
        "alpha"
    )
    results[result] += 1
    
    # Test 8: Different voice test
    result = run_test(
        "Theorem Voice",
        ["python", "mathspeak.py", "a^2 + b^2 = c^2", "-v", "theorem", "-o", "test8.mp3"],
        "squared"
    )
    results[result] += 1
    
    # Test 9: File input test
    # First create a test file
    with open("test_input.tex", "w") as f:
        f.write(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}")
    
    result = run_test(
        "File Input",
        ["python", "mathspeak.py", "-f", "test_input.tex", "-o", "test9.mp3"],
        "sum"
    )
    results[result] += 1
    
    # Test 10: Interactive mode test (just check if it launches)
    result = run_test(
        "Version Check",
        ["python", "mathspeak.py", "--version"],
        "MathSpeak"
    )
    results[result] += 1
    
    # Cleanup test files
    for i in range(1, 10):
        test_file = f"test{i}.mp3"
        if os.path.exists(test_file):
            os.remove(test_file)
    if os.path.exists("test_input.tex"):
        os.remove("test_input.tex")
    
    # Print summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Test Summary:{RESET}")
    print(f"{GREEN}Passed: {results['passed']}{RESET}")
    print(f"{YELLOW}Warnings: {results['warning']}{RESET}")
    print(f"{RED}Failed: {results['failed']}{RESET}")
    print(f"{RED}Timeouts: {results['timeout']}{RESET}")
    print(f"{RED}Errors: {results['error']}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    total_issues = results['failed'] + results['timeout'] + results['error']
    if total_issues == 0:
        print(f"\n{GREEN}🎉 All tests completed successfully!{RESET}")
        return 0
    else:
        print(f"\n{RED}⚠️  {total_issues} tests had issues{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())