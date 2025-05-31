#!/usr/bin/env python3
"""
Comprehensive stress test comparing MathSpeak original engine vs enhanced version
Phase 1: Original engine (patterns_v2)
Phase 2: Enhanced engine (mathspeak_enhancement)
"""

import sys
import time
import json
import os
from datetime import datetime
import traceback
import psutil
import gc

# Add paths
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng')

# Import engines
from mathspeak.core.patterns_v2 import process_math_to_speech, AudienceLevel
from mathspeak.core.engine import MathematicalTTSEngine

# Test categories
TEST_CATEGORIES = {
    "Basic Operations": [
        ("2 + 2", "2 plus 2"),
        ("x - y", "x minus y"),
        ("3 \\times 4", "3 times 4"),
        ("\\frac{a}{b}", "a over b"),
        ("x^2", "x squared"),
        ("\\sqrt{x}", "square root of x"),
    ],
    
    "Complex Fractions": [
        ("\\frac{\\frac{a}{b}}{\\frac{c}{d}}", "a over b all over c over d"),
        ("\\frac{x + y}{z - w}", "x plus y over z minus w"),
        ("\\frac{\\sin x}{\\cos x}", "sine x over cosine x"),
    ],
    
    "Integrals": [
        ("\\int_0^1 x dx", "integral from 0 to 1 x dx"),
        ("\\int\\int_D f(x,y) dA", "double integral over D f of x y dA"),
        ("\\oint_C \\mathbf{F} \\cdot d\\mathbf{r}", "contour integral over C F dot dr"),
    ],
    
    "Derivatives": [
        ("\\frac{d}{dx} f(x)", "derivative with respect to x f of x"),
        ("\\frac{\\partial^2 f}{\\partial x^2}", "second partial derivative of f with respect to x"),
        ("\\nabla f", "gradient of f"),
    ],
    
    "Matrices": [
        ("\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}", "matrix a b c d"),
        ("\\det(A)", "determinant of A"),
        ("A^{-1}", "A inverse"),
    ],
    
    "Greek Letters": [
        ("\\alpha + \\beta", "alpha plus beta"),
        ("\\sum_{i=1}^n \\lambda_i", "sum from i equals 1 to n lambda i"),
        ("\\Omega(n)", "big omega of n"),
    ],
    
    "Special Functions": [
        ("\\sin(\\pi/2)", "sine of pi over 2"),
        ("e^{i\\theta}", "e to the i theta"),
        ("\\ln(x)", "natural log of x"),
    ],
    
    "Set Theory": [
        ("A \\cup B", "A union B"),
        ("X \\cap Y", "X intersect Y"),
        ("\\mathbb{R}", "the real numbers"),
    ],
    
    "Logic": [
        ("P \\land Q", "P and Q"),
        ("\\forall x \\in A", "for all x in A"),
        ("\\exists y", "there exists y"),
    ],
    
    "Statistics": [
        ("\\mathbb{E}[X]", "expected value of X"),
        ("\\text{Var}(X)", "variance of X"),
        ("P(A|B)", "probability of A given B"),
    ]
}

# Devil test cases (subset for stress testing)
DEVIL_TESTS = [
    ("\\frac{\\frac{\\frac{a}{b}}{\\frac{c}{d}}}{\\frac{\\frac{e}{f}}{\\frac{g}{h}}}", 
     "a over b all over c over d all over e over f all over g over h"),
    ("\\int_{\\int_0^1 f(x)dx}^{\\int_0^2 g(x)dx} h(t) dt",
     "integral from integral from 0 to 1 f of x dx to integral from 0 to 2 g of x dx h of t dt"),
    ("\\sum_{\\substack{i=1\\\\j=1}}^{\\substack{n\\\\m}} a_{i,j}",
     "sum from i equals 1 j equals 1 to n m a i j"),
    ("\\mathcal{F}[f](\\omega) = \\int_{-\\infty}^{\\infty} f(t) e^{-i\\omega t} dt",
     "script F of f of omega equals integral from negative infinity to infinity f of t e to the negative i omega t dt"),
]

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / 1024 / 1024

def test_expression(engine_func, latex, expected, engine_name):
    """Test a single expression"""
    start_time = time.time()
    start_memory = get_memory_usage()
    
    try:
        if engine_name == "patterns_v2":
            result = engine_func(latex, AudienceLevel.UNDERGRADUATE)
        else:  # MathematicalTTSEngine
            result = engine_func.process_latex(latex)
            if hasattr(result, 'processed'):
                result = result.processed
            else:
                result = str(result)
        
        end_time = time.time()
        end_memory = get_memory_usage()
        
        # Normalize for comparison
        result_normalized = result.strip().lower()
        expected_normalized = expected.strip().lower()
        
        match = result_normalized == expected_normalized
        
        return {
            'latex': latex,
            'expected': expected,
            'result': result,
            'match': match,
            'time': end_time - start_time,
            'memory_delta': end_memory - start_memory,
            'error': None
        }
        
    except Exception as e:
        end_time = time.time()
        return {
            'latex': latex,
            'expected': expected,
            'result': None,
            'match': False,
            'time': end_time - start_time,
            'memory_delta': 0,
            'error': str(e)
        }

def run_stress_test(engine_func, engine_name, test_cases):
    """Run stress test on an engine"""
    print(f"\n{'='*80}")
    print(f"STRESS TESTING: {engine_name}")
    print(f"{'='*80}")
    
    results = {
        'engine': engine_name,
        'timestamp': datetime.now().isoformat(),
        'categories': {},
        'devil_tests': [],
        'summary': {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'total_time': 0,
            'avg_time': 0,
            'max_time': 0,
            'min_time': float('inf'),
            'memory_usage': 0
        }
    }
    
    # Test by category
    for category, tests in TEST_CATEGORIES.items():
        print(f"\n{category}:")
        category_results = []
        
        for latex, expected in tests:
            result = test_expression(engine_func, latex, expected, engine_name)
            category_results.append(result)
            
            # Update summary
            results['summary']['total'] += 1
            results['summary']['total_time'] += result['time']
            
            if result['match']:
                results['summary']['passed'] += 1
                print(f"  ✅ {latex[:30]}... ({result['time']:.3f}s)")
            elif result['error']:
                results['summary']['errors'] += 1
                print(f"  ❌ {latex[:30]}... ERROR: {result['error']}")
            else:
                results['summary']['failed'] += 1
                print(f"  ❌ {latex[:30]}... MISMATCH")
                print(f"     Expected: {expected}")
                print(f"     Got: {result['result']}")
            
            # Track time stats
            if result['time'] > results['summary']['max_time']:
                results['summary']['max_time'] = result['time']
            if result['time'] < results['summary']['min_time']:
                results['summary']['min_time'] = result['time']
        
        results['categories'][category] = category_results
    
    # Test devil cases
    print(f"\nDevil Tests:")
    for latex, expected in DEVIL_TESTS:
        result = test_expression(engine_func, latex, expected, engine_name)
        results['devil_tests'].append(result)
        
        if result['match']:
            print(f"  ✅ Devil test passed ({result['time']:.3f}s)")
        else:
            print(f"  ❌ Devil test failed")
    
    # Calculate final stats
    if results['summary']['total'] > 0:
        results['summary']['avg_time'] = results['summary']['total_time'] / results['summary']['total']
        results['summary']['success_rate'] = results['summary']['passed'] / results['summary']['total'] * 100
    
    results['summary']['memory_usage'] = get_memory_usage()
    
    # Performance test
    print(f"\nPerformance Test (100 iterations):")
    perf_start = time.time()
    for _ in range(100):
        if engine_name == "patterns_v2":
            engine_func("\\frac{x^2 + 2x + 1}{x - 1}", AudienceLevel.UNDERGRADUATE)
        else:
            engine_func.process_latex("\\frac{x^2 + 2x + 1}{x - 1}")
    perf_end = time.time()
    perf_time = perf_end - perf_start
    results['summary']['perf_100_iterations'] = perf_time
    print(f"  100 iterations: {perf_time:.3f}s ({perf_time/100:.4f}s per iteration)")
    
    return results

def main():
    """Main stress test function"""
    print("🚀 MATHSPEAK COMPREHENSIVE STRESS TEST")
    print("="*80)
    
    # Initialize engines
    print("Initializing engines...")
    engine = MathematicalTTSEngine()
    
    # Phase 1: Original patterns_v2
    print("\n" + "="*80)
    print("PHASE 1: ORIGINAL ENGINE (patterns_v2)")
    print("="*80)
    phase1_results = run_stress_test(process_math_to_speech, "patterns_v2", TEST_CATEGORIES)
    
    # Garbage collection between phases
    gc.collect()
    time.sleep(1)
    
    # Phase 2: Enhanced engine
    print("\n" + "="*80)
    print("PHASE 2: ENHANCED ENGINE (MathematicalTTSEngine)")
    print("="*80)
    phase2_results = run_stress_test(engine, "MathematicalTTSEngine", TEST_CATEGORIES)
    
    # Generate comparison report
    print("\n" + "="*80)
    print("COMPARISON REPORT")
    print("="*80)
    
    # Summary comparison
    print("\nSUMMARY:")
    print(f"{'Metric':<30} {'Original':<20} {'Enhanced':<20} {'Difference':<20}")
    print("-"*90)
    
    metrics = [
        ('Total Tests', 'total', lambda x: f"{x}"),
        ('Passed', 'passed', lambda x: f"{x}"),
        ('Failed', 'failed', lambda x: f"{x}"),
        ('Errors', 'errors', lambda x: f"{x}"),
        ('Success Rate', 'success_rate', lambda x: f"{x:.1f}%"),
        ('Avg Time per Test', 'avg_time', lambda x: f"{x:.4f}s"),
        ('Max Time', 'max_time', lambda x: f"{x:.4f}s"),
        ('Min Time', 'min_time', lambda x: f"{x:.4f}s"),
        ('100 Iterations Time', 'perf_100_iterations', lambda x: f"{x:.3f}s"),
        ('Memory Usage', 'memory_usage', lambda x: f"{x:.1f}MB"),
    ]
    
    for label, key, formatter in metrics:
        val1 = phase1_results['summary'].get(key, 0)
        val2 = phase2_results['summary'].get(key, 0)
        
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
            if key == 'success_rate':
                diff = f"{val2 - val1:+.1f}%"
            elif key in ['avg_time', 'max_time', 'min_time']:
                diff = f"{val2 - val1:+.4f}s ({(val2/val1 - 1)*100:+.1f}%)"
            elif key == 'memory_usage':
                diff = f"{val2 - val1:+.1f}MB"
            else:
                diff = f"{val2 - val1:+d}"
        else:
            diff = "N/A"
        
        print(f"{label:<30} {formatter(val1):<20} {formatter(val2):<20} {diff:<20}")
    
    # Category breakdown
    print("\nCATEGORY BREAKDOWN:")
    print(f"{'Category':<25} {'Original Pass':<15} {'Enhanced Pass':<15} {'Improvement':<15}")
    print("-"*70)
    
    for category in TEST_CATEGORIES.keys():
        orig_results = phase1_results['categories'][category]
        enh_results = phase2_results['categories'][category]
        
        orig_pass = sum(1 for r in orig_results if r['match'])
        enh_pass = sum(1 for r in enh_results if r['match'])
        total = len(orig_results)
        
        print(f"{category:<25} {orig_pass}/{total} ({orig_pass/total*100:.0f}%){'':<5} "
              f"{enh_pass}/{total} ({enh_pass/total*100:.0f}%){'':<5} "
              f"{'+' if enh_pass > orig_pass else ''}{enh_pass - orig_pass}")
    
    # Devil tests comparison
    print("\nDEVIL TESTS:")
    orig_devil_pass = sum(1 for r in phase1_results['devil_tests'] if r['match'])
    enh_devil_pass = sum(1 for r in phase2_results['devil_tests'] if r['match'])
    total_devil = len(phase1_results['devil_tests'])
    
    print(f"Original: {orig_devil_pass}/{total_devil} ({orig_devil_pass/total_devil*100:.0f}%)")
    print(f"Enhanced: {enh_devil_pass}/{total_devil} ({enh_devil_pass/total_devil*100:.0f}%)")
    
    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"stress_test_report_{timestamp}.json"
    
    with open(report_file, 'w') as f:
        json.dump({
            'phase1': phase1_results,
            'phase2': phase2_results,
            'comparison': {
                'timestamp': datetime.now().isoformat(),
                'improvements': {
                    'success_rate': phase2_results['summary']['success_rate'] - phase1_results['summary']['success_rate'],
                    'speed_ratio': phase1_results['summary']['avg_time'] / phase2_results['summary']['avg_time'],
                    'error_reduction': phase1_results['summary']['errors'] - phase2_results['summary']['errors']
                }
            }
        }, f, indent=2)
    
    print(f"\nDetailed report saved to: {report_file}")
    
    # Key findings
    print("\n" + "="*80)
    print("KEY FINDINGS:")
    print("="*80)
    
    print("\n1. ACCURACY:")
    if phase2_results['summary']['success_rate'] > phase1_results['summary']['success_rate']:
        print(f"   ✅ Enhanced version improved accuracy by {phase2_results['summary']['success_rate'] - phase1_results['summary']['success_rate']:.1f}%")
    else:
        print(f"   ⚠️  Original version has better accuracy")
    
    print("\n2. PERFORMANCE:")
    speed_ratio = phase1_results['summary']['avg_time'] / phase2_results['summary']['avg_time']
    if speed_ratio > 1:
        print(f"   ✅ Enhanced version is {speed_ratio:.2f}x faster")
    else:
        print(f"   ⚠️  Original version is {1/speed_ratio:.2f}x faster")
    
    print("\n3. STABILITY:")
    if phase2_results['summary']['errors'] < phase1_results['summary']['errors']:
        print(f"   ✅ Enhanced version has {phase1_results['summary']['errors'] - phase2_results['summary']['errors']} fewer errors")
    else:
        print(f"   ⚠️  Original version is more stable")
    
    print("\n4. MEMORY EFFICIENCY:")
    mem_diff = phase2_results['summary']['memory_usage'] - phase1_results['summary']['memory_usage']
    if abs(mem_diff) < 50:
        print(f"   ✅ Both versions have similar memory usage (~{abs(mem_diff):.1f}MB difference)")
    elif mem_diff < 0:
        print(f"   ✅ Enhanced version uses {abs(mem_diff):.1f}MB less memory")
    else:
        print(f"   ⚠️  Enhanced version uses {mem_diff:.1f}MB more memory")
    
    print("\n" + "="*80)
    print("STRESS TEST COMPLETE!")
    print("="*80)

if __name__ == "__main__":
    main()