"""
Main enhancement loop - runs 20 cycles of improvement
Transforms MathSpeak into professor-quality natural speech
"""

import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import sys
sys.path.append('..')

from example_generator import ExampleGenerator
from test_suite import NaturalnessTestSuite
from improvement_engine import ImprovementEngine
from validator import ImprovementValidator
from adaptive_generator import AdaptiveExampleGenerator


class MathSpeakEnhancementOrchestrator:
    """
    Orchestrates the 20-cycle enhancement process
    """
    
    def __init__(self):
        self.cycles_completed = 0
        self.target_score = 0.98
        self.max_cycles = 20
        self.results_history = []
        
    def run_enhancement_process(self):
        """Run the complete 20-cycle enhancement"""
        
        print("🚀 Starting MathSpeak Natural Speech Enhancement")
        print("=" * 60)
        print(f"Target: {self.target_score:.0%} naturalness across all domains")
        print(f"Process: {self.max_cycles} iterative improvement cycles")
        print("=" * 60)
        
        start_time = time.time()
        
        for cycle in range(1, self.max_cycles + 1):
            cycle_start = time.time()
            print(f"\n🔄 CYCLE {cycle}/{self.max_cycles}")
            print("-" * 50)
            
            # Stage 1: Generate examples
            print("\n📝 Stage 1: Generating 1000 natural speech examples...")
            examples = self.generate_examples(cycle)
            print(f"   ✓ Generated {len(examples)} examples across all domains")
            
            # Stage 2: Create and run tests
            print("\n🧪 Stage 2: Running comprehensive naturalness tests...")
            test_results = self.run_tests(cycle, examples)
            self.print_test_summary(test_results)
            
            # Check if target met
            if test_results['overall_score'] >= self.target_score:
                print(f"\n🎉 Target achieved in cycle {cycle}!")
                print(f"   Final score: {test_results['overall_score']:.2%}")
                if cycle == self.max_cycles:
                    break
            else:
                print(f"\n📊 Current score: {test_results['overall_score']:.2%}")
                print(f"   Gap to target: {(self.target_score - test_results['overall_score']):.2%}")
            
            # Stage 3: Implement improvements
            print("\n🔧 Stage 3: Implementing pattern improvements...")
            improvements = self.implement_improvements(cycle, test_results)
            print(f"   ✓ Applied {improvements['count']} improvements")
            
            # Stage 4: Validate improvements
            print("\n✅ Stage 4: Validating improvements...")
            validation_results = self.validate_improvements(cycle)
            
            if validation_results['passed']:
                print(f"   ✓ Validation passed! New score: {validation_results['score']:.2%}")
            else:
                print(f"   ⚠️  Validation shows more work needed: {validation_results['score']:.2%}")
            
            # Stage 5: Generate next examples (adaptive)
            if cycle < self.max_cycles:
                print("\n📊 Stage 5: Generating adaptive examples for next cycle...")
                self.generate_adaptive_examples(cycle, test_results)
                print("   ✓ Next cycle examples ready")
                
            # Save cycle summary
            self.save_cycle_summary(cycle, test_results, validation_results)
            
            cycle_time = time.time() - cycle_start
            print(f"\n⏱️  Cycle {cycle} completed in {cycle_time:.1f} seconds")
            
            # Progress tracking
            self.results_history.append({
                'cycle': cycle,
                'score': validation_results['score'],
                'improvements': improvements['count'],
                'time': cycle_time
            })
            
        total_time = time.time() - start_time
        print(f"\n🏁 Enhancement process complete!")
        print(f"   Total time: {total_time/60:.1f} minutes")
        self.generate_final_report()
        
    def generate_examples(self, cycle: int) -> Dict:
        """Generate 1000 examples for the cycle"""
        generator = ExampleGenerator(cycle)
        
        if cycle == 1:
            # Initial examples - comprehensive coverage
            examples = generator.generate_initial_examples()
        else:
            # Use previous results to guide generation
            prev_results = self.load_previous_results(cycle - 1)
            examples = generator.generate_from_results(prev_results)
            
        # Save examples
        examples_path = Path(f'examples/cycle_{cycle}_examples.json')
        examples_path.parent.mkdir(exist_ok=True)
        
        with open(examples_path, 'w') as f:
            json.dump(examples, f, indent=2)
            
        return examples
        
    def run_tests(self, cycle: int, examples: Dict) -> Dict:
        """Run comprehensive naturalness tests"""
        test_suite = NaturalnessTestSuite(cycle)
        test_suite.load_examples(examples)
        
        results = test_suite.run_all_tests()
        
        # Save detailed results
        results_path = Path(f'results/cycle_{cycle}_results.json')
        results_path.parent.mkdir(exist_ok=True)
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
            
        return results
        
    def implement_improvements(self, cycle: int, test_results: Dict) -> Dict:
        """Implement improvements based on test results"""
        engine = ImprovementEngine(cycle, test_results)
        
        # Analyze failures and generate fixes
        improvements = engine.analyze_and_fix()
        
        # Apply improvements to MathSpeak codebase
        applied = engine.apply_improvements(improvements)
        
        # Save improvement log
        log_path = Path(f'improvements/cycle_{cycle}_improvements.json')
        log_path.parent.mkdir(exist_ok=True)
        
        with open(log_path, 'w') as f:
            json.dump({
                'cycle': cycle,
                'improvements': improvements,
                'applied': applied,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
            
        return {'count': len(applied), 'details': applied}
        
    def validate_improvements(self, cycle: int) -> Dict:
        """Validate that improvements work correctly"""
        validator = ImprovementValidator(cycle)
        
        # Re-run tests on updated codebase
        validation_results = validator.validate_cycle()
        
        return validation_results
        
    def generate_adaptive_examples(self, cycle: int, test_results: Dict):
        """Generate examples for next cycle based on current results"""
        adaptive_gen = AdaptiveExampleGenerator()
        
        # Focus on weak areas
        next_examples = adaptive_gen.generate_next_cycle_examples(
            cycle + 1, 
            test_results
        )
        
        # Save for next cycle
        next_path = Path(f'examples/cycle_{cycle + 1}_examples_preview.json')
        with open(next_path, 'w') as f:
            json.dump(next_examples, f, indent=2)
            
    def save_cycle_summary(self, cycle: int, test_results: Dict, validation: Dict):
        """Save summary of the cycle"""
        summary = {
            'cycle': cycle,
            'timestamp': datetime.now().isoformat(),
            'test_results': {
                'overall_score': test_results['overall_score'],
                'category_scores': {
                    cat: data['average_score'] 
                    for cat, data in test_results['categories'].items()
                }
            },
            'validation': validation,
            'improvements_applied': len(test_results.get('improvements', [])),
            'target_score': self.target_score,
            'target_met': validation['score'] >= self.target_score
        }
        
        summary_path = Path(f'results/cycle_{cycle}_summary.json')
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
            
    def print_test_summary(self, results: Dict):
        """Print a summary of test results"""
        print(f"   Overall Score: {results['overall_score']:.2%}")
        print("   Category Breakdown:")
        
        for category, data in results['categories'].items():
            score = data['average_score']
            status = "✅" if score >= self.target_score else "❌"
            print(f"     {status} {category}: {score:.2%}")
            
    def load_previous_results(self, cycle: int) -> Dict:
        """Load results from previous cycle"""
        results_path = Path(f'results/cycle_{cycle}_results.json')
        
        if results_path.exists():
            with open(results_path, 'r') as f:
                return json.load(f)
        return {}
        
    def generate_final_report(self):
        """Generate comprehensive final report"""
        report = {
            'enhancement_summary': {
                'total_cycles': len(self.results_history),
                'final_score': self.results_history[-1]['score'] if self.results_history else 0,
                'total_improvements': sum(r['improvements'] for r in self.results_history),
                'target_achieved': self.results_history[-1]['score'] >= self.target_score if self.results_history else False
            },
            'progress_history': self.results_history,
            'category_evolution': self.track_category_progress(),
            'key_improvements': self.identify_key_improvements(),
            'remaining_issues': self.identify_remaining_issues()
        }
        
        # Save report
        report_path = Path('results/final_enhancement_report.json')
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        # Print summary
        print("\n" + "=" * 60)
        print("📊 FINAL ENHANCEMENT REPORT")
        print("=" * 60)
        print(f"Total Cycles: {report['enhancement_summary']['total_cycles']}")
        print(f"Final Score: {report['enhancement_summary']['final_score']:.2%}")
        print(f"Total Improvements: {report['enhancement_summary']['total_improvements']}")
        print(f"Target Achieved: {'✅ Yes' if report['enhancement_summary']['target_achieved'] else '❌ No'}")
        
    def track_category_progress(self) -> Dict:
        """Track progress by category across cycles"""
        progress = {}
        
        for cycle in range(1, len(self.results_history) + 1):
            results_path = Path(f'results/cycle_{cycle}_results.json')
            if results_path.exists():
                with open(results_path, 'r') as f:
                    results = json.load(f)
                    for cat, data in results['categories'].items():
                        if cat not in progress:
                            progress[cat] = []
                        progress[cat].append({
                            'cycle': cycle,
                            'score': data['average_score']
                        })
                        
        return progress
        
    def identify_key_improvements(self) -> List[Dict]:
        """Identify the most impactful improvements"""
        key_improvements = []
        
        for cycle in range(1, len(self.results_history) + 1):
            imp_path = Path(f'improvements/cycle_{cycle}_improvements.json')
            if imp_path.exists():
                with open(imp_path, 'r') as f:
                    data = json.load(f)
                    if 'improvements' in data:
                        for imp in data['improvements'][:3]:  # Top 3 per cycle
                            key_improvements.append({
                                'cycle': cycle,
                                'improvement': imp
                            })
                            
        return key_improvements
        
    def identify_remaining_issues(self) -> List[Dict]:
        """Identify any remaining issues"""
        last_results_path = Path(f'results/cycle_{len(self.results_history)}_results.json')
        
        if last_results_path.exists():
            with open(last_results_path, 'r') as f:
                results = json.load(f)
                
            issues = []
            for cat, data in results['categories'].items():
                if data['average_score'] < self.target_score:
                    issues.append({
                        'category': cat,
                        'score': data['average_score'],
                        'gap': self.target_score - data['average_score'],
                        'common_issues': data.get('common_issues', [])
                    })
                    
            return sorted(issues, key=lambda x: x['gap'], reverse=True)
            
        return []


if __name__ == "__main__":
    orchestrator = MathSpeakEnhancementOrchestrator()
    orchestrator.run_enhancement_process()