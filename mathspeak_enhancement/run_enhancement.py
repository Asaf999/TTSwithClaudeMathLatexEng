#!/usr/bin/env python3
"""
Run the 20-cycle MathSpeak enhancement process
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all components
from mathspeak_enhancement.example_generator_md import MarkdownExampleGenerator
from mathspeak_enhancement.test_suite import NaturalnessTestSuite
from mathspeak_enhancement.improvement_engine import ImprovementEngine
from mathspeak_enhancement.validator import ImprovementValidator
from mathspeak_enhancement.adaptive_generator import AdaptiveExampleGenerator


def run_enhancement_cycle(cycle: int) -> dict:
    """Run a single enhancement cycle"""
    
    print(f"\n{'='*70}")
    print(f"🔄 STARTING CYCLE {cycle}/20")
    print(f"{'='*70}")
    
    results = {'cycle': cycle}
    
    # Stage 1: Generate examples
    print(f"\n[Cycle {cycle}/20 - Stage 1/5] Generating examples...")
    generator = MarkdownExampleGenerator(cycle)
    generator.generate_cycle_examples()
    print(f"✓ Generated 1000 examples for Cycle {cycle}")
    
    # Stage 2: Run tests
    print(f"\n[Cycle {cycle}/20 - Stage 2/5] Running naturalness tests...")
    test_suite = NaturalnessTestSuite(cycle)
    test_results = test_suite.run_all_tests()
    results['test_score'] = test_results['overall_score']
    results['test_pass_rate'] = test_results['pass_rate']
    print(f"✓ Overall score: {test_results['overall_score']:.2%}")
    
    # Check if target met
    if test_results['overall_score'] >= 0.98:
        print(f"🎉 Target achieved in Cycle {cycle}!")
        results['target_met'] = True
        return results
    
    # Stage 3: Implement improvements
    print(f"\n[Cycle {cycle}/20 - Stage 3/5] Implementing improvements...")
    improvement_engine = ImprovementEngine(cycle, test_results)
    improvements = improvement_engine.analyze_and_fix()
    applied = improvement_engine.apply_improvements(improvements)
    results['improvements_applied'] = len(applied)
    print(f"✓ Applied {len(applied)} improvements")
    
    # Stage 4: Validate improvements
    print(f"\n[Cycle {cycle}/20 - Stage 4/5] Validating improvements...")
    validator = ImprovementValidator(cycle)
    validation_results = validator.validate_cycle()
    results['validation_score'] = validation_results['score']
    results['improvement_delta'] = validation_results['improvement']
    print(f"✓ New score: {validation_results['score']:.2%} (improvement: {validation_results['improvement']:+.2%})")
    
    # Stage 5: Generate adaptive examples for next cycle
    if cycle < 20:
        print(f"\n[Cycle {cycle}/20 - Stage 5/5] Generating adaptive examples for next cycle...")
        adaptive_gen = AdaptiveExampleGenerator()
        adaptive_gen.generate_next_cycle_examples(cycle + 1, test_results)
        print(f"✓ Adaptive examples ready for Cycle {cycle + 1}")
    
    results['target_met'] = False
    return results


def generate_final_report(all_results: list):
    """Generate comprehensive final report"""
    
    print("\n" + "="*70)
    print("📊 FINAL ENHANCEMENT REPORT")
    print("="*70)
    
    # Overall summary
    initial_score = all_results[0]['test_score'] if all_results else 0
    final_score = all_results[-1]['validation_score'] if all_results else 0
    total_improvement = final_score - initial_score
    
    print(f"\nOVERALL RESULTS:")
    print(f"  Initial Score: {initial_score:.2%}")
    print(f"  Final Score: {final_score:.2%}")
    print(f"  Total Improvement: {total_improvement:+.2%}")
    print(f"  Target (98%) Achieved: {'✅ Yes' if final_score >= 0.98 else '❌ No'}")
    
    # Cycle-by-cycle progress
    print(f"\nPROGRESS BY CYCLE:")
    print(f"{'Cycle':>5} | {'Test Score':>10} | {'Valid Score':>11} | {'Improvement':>11} | {'Changes':>7}")
    print("-" * 60)
    
    for result in all_results:
        test_score = result.get('test_score', 0)
        valid_score = result.get('validation_score', test_score)
        improvement = result.get('improvement_delta', 0)
        changes = result.get('improvements_applied', 0)
        
        print(f"{result['cycle']:>5} | {test_score:>9.2%} | {valid_score:>10.2%} | {improvement:>+10.2%} | {changes:>7}")
    
    # Key improvements made
    print(f"\nKEY IMPROVEMENTS:")
    total_improvements = sum(r.get('improvements_applied', 0) for r in all_results)
    print(f"  Total improvements applied: {total_improvements}")
    
    # Category analysis
    print(f"\nCATEGORY PERFORMANCE:")
    
    # Load final validation results
    final_validation_path = Path(f"results/cycle_{len(all_results)}_validation.json")
    if final_validation_path.exists():
        with open(final_validation_path, 'r') as f:
            final_validation = json.load(f)
            
        category_scores = final_validation.get('category_scores', {})
        for category, score in sorted(category_scores.items(), key=lambda x: x[1]):
            status = "✅" if score >= 0.98 else "⚠️" if score >= 0.95 else "❌"
            print(f"  {status} {category}: {score:.2%}")
    
    # Save detailed report
    report = {
        'summary': {
            'total_cycles': len(all_results),
            'initial_score': initial_score,
            'final_score': final_score,
            'total_improvement': total_improvement,
            'target_achieved': final_score >= 0.98,
            'total_improvements_applied': total_improvements
        },
        'cycle_results': all_results,
        'timestamp': datetime.now().isoformat()
    }
    
    report_path = Path('results/final_enhancement_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
        
    print(f"\n✅ Detailed report saved to: {report_path}")
    
    # Final recommendations
    print(f"\nRECOMMENDATIONS:")
    if final_score >= 0.98:
        print("  ✅ MathSpeak has achieved professor-quality natural speech!")
        print("  ✅ Ready for production deployment")
    else:
        gap = 0.98 - final_score
        print(f"  ⚠️ Additional work needed to close {gap:.2%} gap")
        print("  📝 Consider manual review of remaining failure patterns")
        print("  🔧 May need domain-specific customizations")


def main():
    """Main enhancement loop"""
    
    print("🚀 Starting MathSpeak Natural Speech Enhancement")
    print(f"Target: 98% naturalness across all mathematical domains")
    print(f"Process: 20 iterative improvement cycles")
    
    # Create results directory
    Path('results').mkdir(exist_ok=True)
    Path('examples').mkdir(exist_ok=True)
    
    all_results = []
    start_time = time.time()
    
    # Run 20 cycles
    for cycle in range(1, 21):
        cycle_results = run_enhancement_cycle(cycle)
        all_results.append(cycle_results)
        
        # Check if target met early
        if cycle_results.get('target_met', False):
            print(f"\n🎉 Target achieved early in Cycle {cycle}!")
            break
            
        # Brief pause between cycles
        if cycle < 20:
            print(f"\n⏳ Preparing for Cycle {cycle + 1}...")
            time.sleep(1)
    
    # Generate final report
    total_time = time.time() - start_time
    print(f"\n⏱️ Total enhancement time: {total_time/60:.1f} minutes")
    
    generate_final_report(all_results)
    
    print("\n🏁 MathSpeak Enhancement Process Complete!")


if __name__ == "__main__":
    main()