#!/usr/bin/env python3
"""
Edge Case Tests for MathSpeak
=============================

Tests edge cases and error handling.
"""

import os
import sys
import subprocess
from pathlib import Path

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def run_edge_test(test_name, command, should_fail=False):
    """Run an edge case test"""
    print(f"\n{BLUE}Edge Test: {test_name}{RESET}")
    print(f"Command: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        
        if should_fail:
            if result.returncode != 0:
                print(f"{GREEN}✅ PASSED (correctly failed){RESET}")
                return True
            else:
                print(f"{RED}❌ FAILED (should have failed but didn't){RESET}")
                return False
        else:
            if result.returncode == 0:
                print(f"{GREEN}✅ PASSED{RESET}")
                return True
            else:
                print(f"{RED}❌ FAILED{RESET}")
                print(f"Error: {result.stderr[:200]}")
                return False
                
    except subprocess.TimeoutExpired:
        print(f"{YELLOW}⚠️  TIMEOUT{RESET}")
        return False
    except Exception as e:
        print(f"{RED}❌ ERROR: {e}{RESET}")
        return False

def main():
    """Run edge case tests"""
    print(f"{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}MathSpeak Edge Case Tests{RESET}")
    print(f"{BLUE}{'='*60}{RESET}")
    
    os.chdir(Path(__file__).parent)
    passed = 0
    total = 0
    
    # Test 1: Empty expression
    total += 1
    if run_edge_test(
        "Empty Expression",
        ["python", "mathspeak.py", "", "-o", "edge1.mp3"]
    ):
        passed += 1
    
    # Test 2: Very long expression
    total += 1
    long_expr = r"\sum_{i=1}^{100} \frac{x^i}{i!} + " * 20
    if run_edge_test(
        "Very Long Expression",
        ["python", "mathspeak.py", long_expr, "-o", "edge2.mp3"]
    ):
        passed += 1
    
    # Test 3: Invalid LaTeX
    total += 1
    if run_edge_test(
        "Invalid LaTeX",
        ["python", "mathspeak.py", r"\invalid{command}", "-o", "edge3.mp3"]
    ):
        passed += 1
    
    # Test 4: Special characters
    total += 1
    if run_edge_test(
        "Special Characters",
        ["python", "mathspeak.py", "∀x ∈ ℝ: x² ≥ 0", "-o", "edge4.mp3"]
    ):
        passed += 1
    
    # Test 5: Nested expressions
    total += 1
    if run_edge_test(
        "Deeply Nested",
        ["python", "mathspeak.py", r"\frac{\frac{\frac{a}{b}}{c}}{d}", "-o", "edge5.mp3"]
    ):
        passed += 1
    
    # Test 6: Mixed languages
    total += 1
    if run_edge_test(
        "Mixed Content",
        ["python", "mathspeak.py", "Let x = 5, then x² = 25", "-o", "edge6.mp3"]
    ):
        passed += 1
    
    # Test 7: Complex matrix
    total += 1
    if run_edge_test(
        "Complex Matrix",
        ["python", "mathspeak.py", r"\begin{bmatrix} 1 & 2 & 3 \\ 4 & 5 & 6 \\ 7 & 8 & 9 \end{bmatrix}", "-o", "edge7.mp3"]
    ):
        passed += 1
    
    # Test 8: Multiple equations
    total += 1
    if run_edge_test(
        "Multiple Equations",
        ["python", "mathspeak.py", r"x + y = 5 \\ 2x - y = 1", "-o", "edge8.mp3"]
    ):
        passed += 1
    
    # Test 9: Batch processing with empty file
    total += 1
    with open("empty_batch.txt", "w") as f:
        f.write("")
    if run_edge_test(
        "Empty Batch File",
        ["python", "mathspeak.py", "--batch", "empty_batch.txt"]
    ):
        passed += 1
    os.remove("empty_batch.txt")
    
    # Test 10: Non-existent file
    total += 1
    if run_edge_test(
        "Non-existent File",
        ["python", "mathspeak.py", "-f", "does_not_exist.tex"],
        should_fail=True
    ):
        passed += 1
    
    # Cleanup
    for i in range(1, 9):
        edge_file = f"edge{i}.mp3"
        if os.path.exists(edge_file):
            os.remove(edge_file)
    
    # Summary
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{BLUE}Edge Case Test Summary:{RESET}")
    print(f"Total: {total}")
    print(f"{GREEN}Passed: {passed}{RESET}")
    print(f"{RED}Failed: {total - passed}{RESET}")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    print(f"{BLUE}{'='*60}{RESET}")
    
    if passed == total:
        print(f"\n{GREEN}🎉 All edge case tests passed!{RESET}")
        return 0
    else:
        print(f"\n{YELLOW}⚠️  Some edge cases need attention{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())