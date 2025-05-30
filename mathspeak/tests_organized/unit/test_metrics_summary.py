#!/usr/bin/env python3
"""
Generate visual test metrics summary
"""

import json
from pathlib import Path

def generate_metrics_summary():
    """Generate a visual summary of test metrics"""
    
    # Load test results
    report_file = Path("test_output/comprehensive_test_report.json")
    if report_file.exists():
        with open(report_file) as f:
            report = json.load(f)
    else:
        print("No test report found!")
        return
    
    # Create visual summary
    summary = report['summary']
    total = summary['total_tests']
    passed = summary['passed']
    failed = summary['failed']
    
    print("\n" + "="*60)
    print("MATHSPEAK COMPREHENSIVE TEST METRICS")
    print("="*60)
    
    # Test results bar chart
    print("\nTest Results:")
    pass_pct = int((passed/total) * 50)
    fail_pct = 50 - pass_pct
    print(f"Pass [{passed:3d}] |{'█' * pass_pct}{' ' * fail_pct}| [{failed:3d}] Fail")
    print(f"            {summary['success_rate']*100:5.1f}% Success Rate")
    
    # Performance metrics
    perf = report['performance']
    print(f"\nPerformance:")
    print(f"  Average Duration: {perf['average_duration']:.3f}s")
    print(f"  Min/Max Duration: {perf['min_duration']:.3f}s / {perf['max_duration']:.3f}s")
    
    # Resource usage
    res = report['resources']
    print(f"\nResource Usage:")
    print(f"  CPU Average: {res['average_cpu_percent']:.1f}%")
    print(f"  Memory Peak: {res['max_memory_mb']:.1f}MB")
    
    # Domain coverage
    print("\nDomain Coverage:")
    domains = report['domain_coverage']
    for domain, count in sorted(domains.items()):
        status = "✓" if count > 0 else "✗"
        print(f"  {status} {domain:<20} {count} tests passed")
    
    # TTS Engines
    print("\nTTS Engine Status:")
    engines = report['tts_engine_stats']
    for engine, stats in engines.items():
        status = "✓" if stats.get('available') else "✗"
        print(f"  {status} {engine}")
    
    # Top errors
    print(f"\nTop Errors ({len(report['errors'])} total):")
    for i, err in enumerate(report['errors'][:5], 1):
        print(f"  {i}. {err['test'][:40]}")
        print(f"     {err['error'][:50]}...")
    
    # Overall assessment
    print("\n" + "-"*60)
    if summary['success_rate'] > 0.95:
        print("✨ ASSESSMENT: Production Ready")
    elif summary['success_rate'] > 0.80:
        print("⚠️  ASSESSMENT: Needs Minor Fixes")
    elif summary['success_rate'] > 0.50:
        print("⚠️  ASSESSMENT: Needs Major Improvements")
    else:
        print("❌ ASSESSMENT: Critical Issues - Not Ready")
    print("-"*60)

if __name__ == "__main__":
    generate_metrics_summary()