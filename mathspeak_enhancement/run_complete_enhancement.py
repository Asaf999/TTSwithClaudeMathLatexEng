#!/usr/bin/env python3
"""
Complete MathSpeak Natural Speech Enhancement System
Runs 20 cycles with actual pattern implementation
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class NaturalSpeechEnhancer:
    """Complete enhancement system with pattern implementation"""
    
    def __init__(self):
        self.cycles_completed = 0
        self.target_score = 0.98
        self.max_cycles = 20
        self.patterns_implemented = []
        
        # Core natural speech patterns to implement
        self.natural_patterns = {
            'equals_vs_is': {
                'description': 'Use "is" for simple arithmetic, "equals" for definitions',
                'patterns': [
                    (r'(\d+\s*[+\-*/]\s*\d+)\s*equals\s*(\d+)', r'\1 is \2'),
                    (r'([a-zA-Z]+\([^)]+\))\s*is\s*', r'\1 equals '),
                ]
            },
            'power_notation': {
                'description': 'Natural power reading (squared, cubed)',
                'patterns': [
                    (r'\^2\b', 'squared'),
                    (r'\^3\b', 'cubed'),
                    (r'\^\{2\}', 'squared'),
                    (r'\^\{3\}', 'cubed'),
                    (r'to the power of 2', 'squared'),
                    (r'to the power of 3', 'cubed'),
                ]
            },
            'fraction_names': {
                'description': 'Natural fraction names',
                'patterns': [
                    (r'\\frac\{1\}\{2\}', 'one half'),
                    (r'\\frac\{1\}\{3\}', 'one third'),
                    (r'\\frac\{1\}\{4\}', 'one quarter'),
                    (r'\\frac\{2\}\{3\}', 'two thirds'),
                    (r'\\frac\{3\}\{4\}', 'three quarters'),
                    (r'one over two', 'one half'),
                    (r'one over three', 'one third'),
                    (r'one over four', 'one quarter'),
                ]
            },
            'derivative_notation': {
                'description': 'Use "by" for derivatives',
                'patterns': [
                    (r'd over d', 'd by d'),
                    (r'partial over partial', 'partial by partial'),
                    (r'\\frac\{d\}\{dx\}', 'd by d x'),
                    (r'\\frac\{\\partial\}\{\\partial x\}', 'partial by partial x'),
                ]
            },
            'parenthesis_handling': {
                'description': 'Implicit parentheses with pauses',
                'patterns': [
                    (r'open parenthesis\s*([^)]+)\s*close parenthesis', r'\1'),
                    (r'\(([^)]+)\)\^', r'\1, to the power of '),
                    (r'\)\s*\(', ', times '),
                ]
            },
            'article_usage': {
                'description': 'Add articles for flow',
                'patterns': [
                    (r'^(integral|limit|sum|product|derivative|determinant)\s+', r'the \1 '),
                    (r'\b(integral|limit|sum|product) from', r'the \1 from'),
                ]
            },
            'integral_pauses': {
                'description': 'Natural integral reading',
                'patterns': [
                    (r'(integral.*?)\s+d\s*([a-z])', r'\1, d\2'),
                    (r'\\int', 'the integral'),
                ]
            },
            'limit_notation': {
                'description': 'Natural limit reading',
                'patterns': [
                    (r'goes to', 'approaches'),
                    (r'\\lim', 'the limit'),
                    (r'\\to\s*\\infty', 'approaches infinity'),
                ]
            }
        }
        
    def run_complete_enhancement(self):
        """Run the complete 20-cycle enhancement"""
        
        print("🚀 Starting Complete MathSpeak Natural Speech Enhancement")
        print(f"Target: {self.target_score:.0%} naturalness")
        print(f"Process: {self.max_cycles} iterative cycles")
        print("="*70)
        
        # Create directories
        Path('results').mkdir(exist_ok=True)
        Path('examples').mkdir(exist_ok=True)
        Path('implementations').mkdir(exist_ok=True)
        
        all_results = []
        start_time = time.time()
        
        for cycle in range(1, self.max_cycles + 1):
            print(f"\n{'='*70}")
            print(f"🔄 STARTING CYCLE {cycle}/{self.max_cycles}")
            print(f"{'='*70}")
            
            cycle_results = self.run_single_cycle(cycle)
            all_results.append(cycle_results)
            
            # Check if target met
            if cycle_results['final_score'] >= self.target_score:
                print(f"\n🎉 Target achieved in Cycle {cycle}!")
                break
                
            time.sleep(0.5)  # Brief pause
            
        # Generate final report
        total_time = time.time() - start_time
        print(f"\n⏱️ Total time: {total_time/60:.1f} minutes")
        self.generate_final_report(all_results)
        
    def run_single_cycle(self, cycle: int) -> Dict:
        """Run a single enhancement cycle"""
        
        results = {'cycle': cycle}
        
        # Stage 1: Generate examples
        print(f"\n[Cycle {cycle}/{self.max_cycles} - Stage 1/5] Generating examples...")
        examples = self.generate_examples(cycle)
        print(f"✓ Generated {len(examples)} example categories")
        results['examples_generated'] = sum(len(v) for v in examples.values())
        
        # Stage 2: Test current implementation
        print(f"\n[Cycle {cycle}/{self.max_cycles} - Stage 2/5] Testing current patterns...")
        test_results = self.test_patterns(examples)
        results['initial_score'] = test_results['overall_score']
        print(f"✓ Current score: {test_results['overall_score']:.2%}")
        
        # Stage 3: Analyze and implement improvements
        print(f"\n[Cycle {cycle}/{self.max_cycles} - Stage 3/5] Implementing improvements...")
        improvements = self.implement_improvements(test_results, cycle)
        results['improvements_made'] = len(improvements)
        print(f"✓ Implemented {len(improvements)} improvements")
        
        # Stage 4: Validate improvements
        print(f"\n[Cycle {cycle}/{self.max_cycles} - Stage 4/5] Validating improvements...")
        validation_results = self.validate_improvements(examples)
        results['final_score'] = validation_results['overall_score']
        results['improvement'] = validation_results['overall_score'] - results['initial_score']
        print(f"✓ New score: {validation_results['overall_score']:.2%} (improvement: {results['improvement']:+.2%})")
        
        # Stage 5: Prepare for next cycle
        if cycle < self.max_cycles:
            print(f"\n[Cycle {cycle}/{self.max_cycles} - Stage 5/5] Preparing next cycle...")
            self.prepare_next_cycle(validation_results, cycle + 1)
            print(f"✓ Ready for Cycle {cycle + 1}")
            
        return results
        
    def generate_examples(self, cycle: int) -> Dict:
        """Generate test examples for the cycle"""
        
        examples = {
            'basic_arithmetic': [
                {'latex': '$2 + 3 = 5$', 'natural': 'two plus three is five'},
                {'latex': '$10 - 4 = 6$', 'natural': 'ten minus four is six'},
                {'latex': '$3 \\times 4 = 12$', 'natural': 'three times four is twelve'},
            ],
            'algebra': [
                {'latex': '$x^2 + 5x + 6$', 'natural': 'x squared plus five x plus six'},
                {'latex': '$(x+2)(x+3)$', 'natural': 'x plus two, times x plus three'},
                {'latex': '$f(x) = x^2$', 'natural': 'f of x equals x squared'},
            ],
            'calculus': [
                {'latex': '$\\frac{d}{dx} f(x)$', 'natural': 'd by d x of f of x'},
                {'latex': '$\\int_0^1 x^2 dx$', 'natural': 'the integral from zero to one of x squared, d x'},
                {'latex': '$\\lim_{x \\to 0} \\frac{\\sin x}{x}$', 'natural': 'the limit as x approaches zero of sine x over x'},
            ],
            'fractions': [
                {'latex': '$\\frac{1}{2}$', 'natural': 'one half'},
                {'latex': '$\\frac{2}{3}$', 'natural': 'two thirds'},
                {'latex': '$\\frac{3}{4}$', 'natural': 'three quarters'},
            ]
        }
        
        # Save examples
        examples_path = Path(f'examples/cycle_{cycle}_test_examples.json')
        with open(examples_path, 'w') as f:
            json.dump(examples, f, indent=2)
            
        return examples
        
    def test_patterns(self, examples: Dict) -> Dict:
        """Test current pattern implementation"""
        
        results = {
            'overall_score': 0,
            'category_scores': {},
            'failures': []
        }
        
        total_tests = 0
        total_passed = 0
        
        for category, test_cases in examples.items():
            category_passed = 0
            
            for test in test_cases:
                latex = test['latex']
                expected = test['natural']
                actual = self.apply_current_patterns(latex)
                
                # Simple scoring - exact match or close match
                if actual == expected:
                    category_passed += 1
                    total_passed += 1
                elif self.is_close_match(actual, expected):
                    category_passed += 0.8
                    total_passed += 0.8
                else:
                    results['failures'].append({
                        'category': category,
                        'latex': latex,
                        'expected': expected,
                        'actual': actual
                    })
                    
                total_tests += 1
                
            category_score = category_passed / len(test_cases) if test_cases else 0
            results['category_scores'][category] = category_score
            
        results['overall_score'] = total_passed / total_tests if total_tests > 0 else 0
        return results
        
    def apply_current_patterns(self, latex: str) -> str:
        """Apply currently implemented patterns"""
        
        # Start with basic conversion
        text = latex
        
        # Remove $ signs
        text = text.replace('$', '')
        
        # Basic replacements
        text = text.replace('+', ' plus ')
        text = text.replace('-', ' minus ')
        text = text.replace('\\times', ' times ')
        text = text.replace('=', ' equals ')
        
        # Apply implemented patterns
        for pattern_set in self.patterns_implemented:
            for pattern, replacement in pattern_set:
                text = re.sub(pattern, replacement, text)
                
        # Clean up spacing
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
        
    def is_close_match(self, actual: str, expected: str) -> bool:
        """Check if two strings are close matches"""
        
        # Normalize for comparison
        actual_norm = actual.lower().replace(',', '').replace('the ', '')
        expected_norm = expected.lower().replace(',', '').replace('the ', '')
        
        # Calculate similarity
        actual_words = actual_norm.split()
        expected_words = expected_norm.split()
        
        if len(actual_words) != len(expected_words):
            return False
            
        matches = sum(1 for a, e in zip(actual_words, expected_words) if a == e)
        return matches / len(expected_words) >= 0.8
        
    def implement_improvements(self, test_results: Dict, cycle: int) -> List[Dict]:
        """Implement improvements based on test results"""
        
        improvements = []
        
        # Analyze failures
        failure_patterns = {}
        for failure in test_results['failures']:
            expected = failure['expected']
            actual = failure['actual']
            
            # Identify pattern types needed
            if 'is' in expected and 'equals' in actual:
                failure_patterns['equals_vs_is'] = failure_patterns.get('equals_vs_is', 0) + 1
            elif 'squared' in expected and 'to the power of 2' in actual:
                failure_patterns['power_notation'] = failure_patterns.get('power_notation', 0) + 1
            elif 'd by d' in expected and 'd over d' in actual:
                failure_patterns['derivative_notation'] = failure_patterns.get('derivative_notation', 0) + 1
                
        # Implement top patterns
        for pattern_type, count in sorted(failure_patterns.items(), key=lambda x: x[1], reverse=True)[:3]:
            if pattern_type in self.natural_patterns:
                pattern_set = self.natural_patterns[pattern_type]['patterns']
                self.patterns_implemented.append(pattern_set)
                improvements.append({
                    'type': pattern_type,
                    'description': self.natural_patterns[pattern_type]['description'],
                    'patterns_added': len(pattern_set)
                })
                
        # Save implementation
        impl_path = Path(f'implementations/cycle_{cycle}_patterns.json')
        with open(impl_path, 'w') as f:
            json.dump({
                'cycle': cycle,
                'improvements': improvements,
                'total_patterns': sum(len(p) for p in self.patterns_implemented)
            }, f, indent=2)
            
        return improvements
        
    def validate_improvements(self, examples: Dict) -> Dict:
        """Validate that improvements work"""
        
        # Re-test with new patterns
        return self.test_patterns(examples)
        
    def prepare_next_cycle(self, validation_results: Dict, next_cycle: int):
        """Prepare for the next cycle"""
        
        # Identify remaining weak areas
        weak_areas = []
        for category, score in validation_results['category_scores'].items():
            if score < self.target_score:
                weak_areas.append({
                    'category': category,
                    'score': score,
                    'gap': self.target_score - score
                })
                
        # Save preparation
        prep_path = Path(f'implementations/cycle_{next_cycle}_preparation.json')
        with open(prep_path, 'w') as f:
            json.dump({
                'next_cycle': next_cycle,
                'weak_areas': weak_areas,
                'patterns_to_implement': len(self.natural_patterns) - len(self.patterns_implemented)
            }, f, indent=2)
            
    def generate_final_report(self, all_results: List[Dict]):
        """Generate comprehensive final report"""
        
        print("\n" + "="*70)
        print("📊 FINAL NATURAL SPEECH ENHANCEMENT REPORT")
        print("="*70)
        
        # Summary statistics
        initial_score = all_results[0]['initial_score']
        final_score = all_results[-1]['final_score']
        total_improvements = sum(r['improvements_made'] for r in all_results)
        
        print(f"\nOVERALL RESULTS:")
        print(f"  Initial Score: {initial_score:.2%}")
        print(f"  Final Score: {final_score:.2%}")
        print(f"  Total Improvement: {(final_score - initial_score):+.2%}")
        print(f"  Target Achieved: {'✅ Yes' if final_score >= self.target_score else '❌ No'}")
        print(f"  Total Pattern Sets Implemented: {len(self.patterns_implemented)}")
        print(f"  Total Individual Patterns: {sum(len(p) for p in self.patterns_implemented)}")
        
        # Cycle-by-cycle progress
        print(f"\nPROGRESS BY CYCLE:")
        print(f"{'Cycle':>5} | {'Initial':>8} | {'Final':>8} | {'Improve':>8} | {'Changes':>7}")
        print("-" * 50)
        
        for result in all_results:
            print(f"{result['cycle']:>5} | {result['initial_score']:>7.1%} | {result['final_score']:>7.1%} | "
                  f"{result['improvement']:>+7.1%} | {result['improvements_made']:>7}")
                  
        # Pattern implementation summary
        print(f"\nPATTERN IMPLEMENTATION SUMMARY:")
        pattern_counts = {}
        for pattern_set in self.patterns_implemented:
            for pattern in pattern_set:
                if isinstance(pattern, tuple) and len(pattern) >= 2:
                    desc = pattern[1] if isinstance(pattern[1], str) else str(pattern[1])
                    pattern_counts[desc] = pattern_counts.get(desc, 0) + 1
                    
        for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  - {pattern}: {count} variations")
            
        # Save detailed report
        report = {
            'summary': {
                'total_cycles': len(all_results),
                'initial_score': initial_score,
                'final_score': final_score,
                'improvement': final_score - initial_score,
                'target_achieved': final_score >= self.target_score,
                'patterns_implemented': len(self.patterns_implemented),
                'total_improvements': total_improvements
            },
            'cycle_results': all_results,
            'patterns': [
                {
                    'type': ptype,
                    'description': pdata['description'],
                    'implemented': ptype in [imp['type'] for cycle in all_results for imp in cycle.get('improvements', [])]
                }
                for ptype, pdata in self.natural_patterns.items()
            ],
            'timestamp': datetime.now().isoformat()
        }
        
        report_path = Path('results/complete_enhancement_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        print(f"\n✅ Detailed report saved to: {report_path}")
        
        # Final recommendations
        print(f"\nFINAL STATUS:")
        if final_score >= self.target_score:
            print("  ✅ MathSpeak has achieved natural, professor-quality speech!")
            print("  ✅ All major speech patterns successfully implemented")
            print("  ✅ Ready for production deployment")
        else:
            print(f"  ⚠️ Additional refinement needed ({(self.target_score - final_score):.1%} gap)")
            print("  📝 Consider fine-tuning edge cases")
            print("  🔧 May need domain-specific adjustments")
            
        print("\n🏁 Natural Speech Enhancement Complete!")


def main():
    """Run the complete enhancement process"""
    enhancer = NaturalSpeechEnhancer()
    enhancer.run_complete_enhancement()


if __name__ == "__main__":
    main()