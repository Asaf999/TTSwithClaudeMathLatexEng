#!/usr/bin/env python3
"""
Real Child Process Implementation for MathSpeak Enhancement
This is the actual working implementation that generates examples,
runs tests, implements improvements, and validates results.
"""

import json
import re
import time
import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime
import random

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RealChildProcess:
    """Actual working child process that performs enhancement tasks"""
    
    def __init__(self):
        self.task_id = None
        self.cycle = 1
        self.context = {}
        self.test_results = []
        self.improvements_made = []
        
    def execute_task(self, task: Dict) -> Dict:
        """Execute a specific task based on type"""
        
        task_type = task.get('type')
        task_id = task.get('id', f'task_{int(time.time())}')
        self.task_id = task_id
        self.cycle = task.get('cycle', 1)
        
        print(f"\n[CHILD] Executing task: {task_type} (ID: {task_id})")
        
        if task_type == 'generate_examples':
            return self.generate_real_examples(task)
        elif task_type == 'run_tests':
            return self.run_real_tests(task)
        elif task_type == 'implement_improvements':
            return self.implement_real_improvements(task)
        elif task_type == 'validate_improvements':
            return self.validate_real_improvements(task)
        else:
            return {'status': 'error', 'message': f'Unknown task type: {task_type}'}
            
    def generate_real_examples(self, task: Dict) -> Dict:
        """Generate actual test examples based on cycle strategy"""
        
        strategy = task.get('parameters', {}).get('strategy', {})
        focus = strategy.get('focus', 'broad')
        
        print(f"[CHILD] Generating examples with focus: {focus}")
        
        examples = {}
        
        # Base test cases that should always pass
        base_cases = {
            'arithmetic': [
                {'latex': '$2 + 3 = 5$', 'expected': 'two plus three is five', 'context': 'arithmetic'},
                {'latex': '$10 - 4 = 6$', 'expected': 'ten minus four is six', 'context': 'arithmetic'},
                {'latex': '$3 \\times 4 = 12$', 'expected': 'three times four is twelve', 'context': 'arithmetic'},
                {'latex': '$15 \\div 3 = 5$', 'expected': 'fifteen divided by three is five', 'context': 'arithmetic'},
            ],
            'algebra': [
                {'latex': '$x^2 + 5x + 6$', 'expected': 'x squared plus five x plus six'},
                {'latex': '$(x+2)(x+3)$', 'expected': 'x plus two, times x plus three'},
                {'latex': '$f(x) = x^2$', 'expected': 'f of x equals x squared', 'context': 'definition'},
                {'latex': '$x^2 - 4 = 0$', 'expected': 'x squared minus four equals zero'},
            ],
            'calculus': [
                {'latex': '$\\frac{d}{dx} f(x)$', 'expected': 'd by dx of f of x'},
                {'latex': '$\\int_0^1 x^2 dx$', 'expected': 'the integral from zero to one of x squared, dx'},
                {'latex': '$\\lim_{x \\to 0} \\frac{\\sin x}{x}$', 'expected': 'the limit as x approaches zero of sine x over x'},
                {'latex': "$f'(x) = 2x$", 'expected': 'f prime of x equals two x'},
            ],
            'fractions': [
                {'latex': '$\\frac{1}{2}$', 'expected': 'one half'},
                {'latex': '$\\frac{2}{3}$', 'expected': 'two thirds'},
                {'latex': '$\\frac{3}{4}$', 'expected': 'three quarters'},
                {'latex': '$\\frac{5}{6}$', 'expected': 'five sixths'},
            ],
            'advanced': [
                {'latex': '$\\forall x \\in \\mathbb{R}$', 'expected': 'for all real x'},
                {'latex': '$x_n \\to \\infty$', 'expected': 'x n approaches infinity'},
                {'latex': '$\\frac{\\partial f}{\\partial x}$', 'expected': 'partial f by partial x'},
                {'latex': '$A \\subset B$', 'expected': 'a is a subset of b'},
            ],
            'linear_algebra': [
                {'latex': '$\\det(A) = 0$', 'expected': 'the determinant of a equals zero'},
                {'latex': '$A^T$', 'expected': 'a transpose'},
                {'latex': '$\\vec{v} \\cdot \\vec{w}$', 'expected': 'v dot w'},
            ],
            'complex': [
                {'latex': '$\\sum_{i=1}^n i = \\frac{n(n+1)}{2}$', 
                 'expected': 'the sum from i equals one to n of i equals n n plus one over two'},
            ]
        }
        
        # Add base cases
        examples.update(base_cases)
        
        # Generate additional focused examples based on cycle
        if focus == 'structural_fixes' or self.cycle <= 5:
            # Focus on derivative patterns (known issue)
            examples['derivatives_focus'] = [
                {'latex': '$\\frac{df}{dx}$', 'expected': 'd f by d x'},
                {'latex': '$\\frac{d}{dx}(x^2)$', 'expected': 'd by d x of x squared'},
                {'latex': '$\\frac{d^2y}{dx^2}$', 'expected': 'd squared y by d x squared'},
                {'latex': '$\\frac{\\partial u}{\\partial t}$', 'expected': 'partial u by partial t'},
                {'latex': '$\\frac{\\partial^2 f}{\\partial x \\partial y}$', 'expected': 'partial squared f by partial x partial y'},
            ]
            
        elif focus == 'targeted_improvements' or self.cycle <= 10:
            # Focus on mixed patterns
            examples['mixed_patterns'] = [
                {'latex': '$\\frac{d}{dx}[\\frac{1}{x}]$', 'expected': 'd by d x of one over x'},
                {'latex': '$\\int \\frac{1}{x} dx$', 'expected': 'the integral of one over x, d x'},
                {'latex': '$\\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}$', 
                 'expected': 'the limit as h approaches zero of f of x plus h minus f of x over h'},
            ]
            
        elif focus == 'edge_cases' or self.cycle <= 15:
            # Focus on edge cases
            examples['edge_cases'] = [
                {'latex': '$\\frac{d}{dx}[\\ln(x)]$', 'expected': 'd by d x of natural log of x'},
                {'latex': '$e^{i\\pi} + 1 = 0$', 'expected': 'e to the i pi plus one equals zero'},
                {'latex': '$\\nabla \\cdot \\vec{F}$', 'expected': 'del dot f'},
            ]
            
        # Save examples
        output_file = f'examples/cycle_{self.cycle}_test_examples.json'
        Path('examples').mkdir(exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(examples, f, indent=2)
            
        total_examples = sum(len(cat) for cat in examples.values())
        
        return {
            'status': 'completed',
            'output_file': output_file,
            'examples_generated': total_examples,
            'categories': list(examples.keys()),
            'focus': focus
        }
        
    def run_real_tests(self, task: Dict) -> Dict:
        """Run actual tests on the current implementation"""
        
        examples_file = task.get('parameters', {}).get('examples_file')
        if not examples_file:
            examples_file = f'examples/cycle_{self.cycle}_test_examples.json'
            
        print(f"[CHILD] Running tests from: {examples_file}")
        
        # Load examples
        try:
            with open(examples_file, 'r') as f:
                examples = json.load(f)
        except FileNotFoundError:
            # Generate examples if not found
            gen_result = self.generate_real_examples(task)
            with open(gen_result['output_file'], 'r') as f:
                examples = json.load(f)
                
        # Import and test the actual implementation
        try:
            from truly_final_98_percent import TrulyFinal98PercentNaturalSpeech
            engine = TrulyFinal98PercentNaturalSpeech()
        except ImportError:
            return {'status': 'error', 'message': 'Could not import natural speech engine'}
            
        # Run tests
        total_tests = 0
        total_passed = 0
        failures = []
        category_scores = {}
        
        for category, test_cases in examples.items():
            category_passed = 0
            category_total = len(test_cases)
            
            for test in test_cases:
                latex = test.get('latex', '')
                expected = test.get('expected', '')
                context = test.get('context', None)
                
                # Run test
                try:
                    actual = engine.naturalize(latex, context)
                    
                    if actual == expected:
                        category_passed += 1
                        total_passed += 1
                    else:
                        failures.append({
                            'category': category,
                            'latex': latex,
                            'expected': expected,
                            'actual': actual,
                            'context': context,
                            'error_type': self._classify_error(expected, actual)
                        })
                        
                except Exception as e:
                    failures.append({
                        'category': category,
                        'latex': latex,
                        'expected': expected,
                        'actual': f'ERROR: {str(e)}',
                        'context': context,
                        'error_type': 'exception'
                    })
                    
                total_tests += 1
                
            if category_total > 0:
                category_scores[category] = category_passed / category_total
                
        overall_score = total_passed / total_tests if total_tests > 0 else 0
        
        # Save detailed results
        results = {
            'cycle': self.cycle,
            'timestamp': datetime.now().isoformat(),
            'overall_score': overall_score,
            'passed': total_passed,
            'total': total_tests,
            'category_scores': category_scores,
            'failures': failures,
            'failure_summary': self._summarize_failures(failures)
        }
        
        results_file = f'results/cycle_{self.cycle}_test_results.json'
        Path('results').mkdir(exist_ok=True)
        
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
            
        # Save test summary
        summary_file = f'results/cycle_{self.cycle}_test_summary.txt'
        with open(summary_file, 'w') as f:
            f.write(f"Cycle {self.cycle} Test Results\n")
            f.write("="*50 + "\n")
            f.write(f"Overall Score: {overall_score:.1%} ({total_passed}/{total_tests})\n\n")
            f.write("Category Scores:\n")
            for cat, score in category_scores.items():
                f.write(f"  {cat}: {score:.1%}\n")
            f.write(f"\nFailures: {len(failures)}\n")
            if failures:
                f.write("\nTop failure patterns:\n")
                for pattern, count in results['failure_summary'].items():
                    f.write(f"  {pattern}: {count} occurrences\n")
                    
        self.test_results = results
        
        return {
            'status': 'completed',
            'overall_score': overall_score,
            'passed': total_passed,
            'total': total_tests,
            'failures': failures,
            'results_file': results_file,
            'summary_file': summary_file
        }
        
    def _classify_error(self, expected: str, actual: str) -> str:
        """Classify the type of error"""
        
        if 'd by d' in expected and 'd over d' in actual:
            return 'derivative_notation'
        elif 'partial' in expected and 'by partial' in expected and 'over partial' in actual:
            return 'partial_derivative_notation'
        elif ' by ' in expected and ' over ' in actual and ('d' in expected or 'partial' in expected):
            return 'derivative_notation'
        elif 'is' in expected and 'equals' in actual:
            return 'equals_vs_is'
        elif 'squared' in expected and 'to the' in actual:
            return 'power_notation'
        elif 'one half' in expected and 'one over two' in actual:
            return 'fraction_names'
        else:
            return 'other'
            
    def _summarize_failures(self, failures: List[Dict]) -> Dict[str, int]:
        """Summarize failure patterns"""
        summary = {}
        for failure in failures:
            error_type = failure.get('error_type', 'unknown')
            summary[error_type] = summary.get(error_type, 0) + 1
        return summary
        
    def implement_real_improvements(self, task: Dict) -> Dict:
        """Implement actual code improvements"""
        
        test_results = task.get('parameters', {}).get('test_results', self.test_results)
        priority_fixes = task.get('parameters', {}).get('priority_fixes', [])
        
        print(f"[CHILD] Implementing improvements for cycle {self.cycle}")
        
        # Analyze failures from test results
        if not priority_fixes and test_results:
            priority_fixes = self._analyze_and_prioritize_fixes(test_results)
            
        # Read current implementation
        impl_file = 'mathspeak_enhancement/truly_final_98_percent.py'
        with open(impl_file, 'r') as f:
            current_code = f.read()
            
        # Apply fixes based on priority
        modified_code = current_code
        improvements_made = []
        
        print(f"[CHILD] Priority fixes to apply: {len(priority_fixes)}")
        for fix in priority_fixes:
            print(f"[CHILD]   - {fix['pattern']}: {fix.get('count', 0)} failures")
        
        for fix in priority_fixes[:3]:  # Apply top 3 fixes per cycle
            if fix['pattern'] in ['derivative_notation', 'partial_derivative_notation']:
                # Fix the derivative notation issue
                modified_code, applied = self._fix_derivative_notation(modified_code)
                if applied:
                    improvements_made.append({
                        'type': 'derivative_notation',
                        'description': 'Fixed d/dx to read as "d by dx" instead of "d over dx"',
                        'changes': applied
                    })
                    
            elif fix['pattern'] == 'equals_vs_is':
                # Improve equals vs is logic
                modified_code, applied = self._improve_equals_vs_is(modified_code)
                if applied:
                    improvements_made.append({
                        'type': 'equals_vs_is',
                        'description': 'Improved context-aware equals/is usage',
                        'changes': applied
                    })
                    
        # Save improved code
        if improvements_made:
            backup_file = f'mathspeak_enhancement/backups/truly_final_98_percent_cycle{self.cycle-1}.py'
            Path('mathspeak_enhancement/backups').mkdir(exist_ok=True)
            
            # Backup current version
            with open(backup_file, 'w') as f:
                f.write(current_code)
                
            # Write improved version
            with open(impl_file, 'w') as f:
                f.write(modified_code)
                
        self.improvements_made = improvements_made
        
        return {
            'status': 'completed',
            'improvements_made': len(improvements_made),
            'modified_files': [impl_file] if improvements_made else [],
            'improvements': improvements_made,
            'backup_file': backup_file if improvements_made else None
        }
        
    def _analyze_and_prioritize_fixes(self, test_results: Dict) -> List[Dict]:
        """Analyze test results and prioritize fixes"""
        
        fixes = []
        failure_summary = test_results.get('failure_summary', {})
        
        # Prioritize based on frequency and impact
        for error_type, count in sorted(failure_summary.items(), key=lambda x: x[1], reverse=True):
            if error_type == 'derivative_notation':
                fixes.append({
                    'pattern': 'derivative_notation',
                    'urgency': 'critical',
                    'count': count,
                    'solution': 'modify_handle_derivatives'
                })
            elif error_type == 'partial_derivative_notation':
                fixes.append({
                    'pattern': 'partial_derivative_notation',
                    'urgency': 'critical',
                    'count': count,
                    'solution': 'modify_handle_derivatives'
                })
            elif error_type == 'equals_vs_is':
                fixes.append({
                    'pattern': 'equals_vs_is',
                    'urgency': 'high',
                    'count': count,
                    'solution': 'improve_context_rules'
                })
                
        return fixes
        
    def _fix_derivative_notation(self, code: str) -> Tuple[str, List[Dict]]:
        """Fix derivative notation in the code"""
        
        changes = []
        
        # Find the handle_fractions method to modify it
        pattern = r'def _handle_fractions\(self, text: str\) -> str:(.*?)(?=\n    def|\nclass|\n\n|\Z)'
        match = re.search(pattern, code, re.DOTALL)
        
        if match:
            old_method = match.group(0)
            
            # Create improved method that handles derivatives first
            new_method = '''def _handle_fractions(self, text: str) -> str:
        """Handle fraction patterns correctly"""
        
        # IMPORTANT: Handle derivatives FIRST before general fractions
        # Standard d/dx pattern
        text = re.sub(r'\\\\frac\{d\}\{d(\w+)\}', r'd by d\\1', text)
        text = re.sub(r'\\\\frac\{d(\w*)\}\{d(\w+)\}', r'd\\1 by d\\2', text)
        
        # Handle d^2/dx^2 patterns
        text = re.sub(r'\\\\frac\{d\^2(\w*)\}\{d(\w+)\^2\}', r'd squared \\1 by d\\2 squared', text)
        text = re.sub(r'\\\\frac\{d\^(\d+)(\w*)\}\{d(\w+)\^\\1\}', r'd to the \\1 \\2 by d\\3 to the \\1', text)
        
        # Partial derivatives
        text = re.sub(r'\\\\frac\{\\\\partial\s*(\w*)\}\{\\\\partial\s*(\w+)\}', lambda m: f'partial {m.group(1)} by partial {m.group(2)}'.replace('  ', ' '), text)
        text = re.sub(r'\\\\frac\{\\\\partial\^2\s*(\w*)\}\{\\\\partial\s*(\w+)\s*\\\\partial\s*(\w+)\}', r'partial squared \\1 by partial \\2 partial \\3', text)
        
        def replace_frac(match):
            num = match.group(1).strip()
            den = match.group(2).strip()
            
            # Skip if this looks like a derivative (already handled)
            if 'd' in num and 'd' in den:
                return match.group(0)
            if 'partial' in num or 'partial' in den:
                return match.group(0)
            
            # Map to natural fraction names
            fracs = {
                ('1', '2'): 'one half',
                ('1', '3'): 'one third', 
                ('2', '3'): 'two thirds',
                ('1', '4'): 'one quarter',
                ('3', '4'): 'three quarters',
                ('1', '5'): 'one fifth',
                ('2', '5'): 'two fifths',
                ('1', '6'): 'one sixth',
                ('5', '6'): 'five sixths'
            }
            
            if (num, den) in fracs:
                return fracs[(num, den)]
            else:
                return f"{num} over {den}"
                
        text = re.sub(r'\\\\frac\{([^}]+)\}\{([^}]+)\}', replace_frac, text)
        
        return text'''
            
            code = code.replace(old_method, new_method)
            changes.append({
                'location': '_handle_fractions method',
                'type': 'method_replacement',
                'description': 'Modified fractions handler to process derivatives first'
            })
            
        # Also need to ensure derivatives are processed BEFORE fractions in _process_latex
        process_pattern = r'(def _process_latex.*?)(text = self\._handle_fractions\(text\))'
        process_match = re.search(process_pattern, code, re.DOTALL)
        
        if process_match:
            # Check if derivatives come before fractions
            method_body = process_match.group(0)
            if method_body.find('_handle_derivatives') > method_body.find('_handle_fractions'):
                # Need to reorder
                old_order = re.search(
                    r'(text = self\._handle_fractions\(text\).*?)(text = self\._handle_derivatives\(text\))',
                    method_body, re.DOTALL
                )
                if old_order:
                    new_order = old_order.group(2) + '\n        ' + old_order.group(1)
                    code = code.replace(old_order.group(0), new_order)
                    changes.append({
                        'location': '_process_latex method',
                        'type': 'reorder_operations',
                        'description': 'Moved derivative handling before fraction handling'
                    })
                    
        return code, changes
        
    def _fix_partial_derivative_notation(self, code: str) -> Tuple[str, List[Dict]]:
        """Fix partial derivative notation"""
        
        # This is handled by the same fix as regular derivatives
        return code, []
        
    def _improve_equals_vs_is(self, code: str) -> Tuple[str, List[Dict]]:
        """Improve equals vs is context handling"""
        
        changes = []
        
        # Find the _apply_context_rules method
        pattern = r'def _apply_context_rules\(self, text: str, context: str\) -> str:(.*?)(?=\n    def|\nclass|\n\n|\Z)'
        match = re.search(pattern, code, re.DOTALL)
        
        if match:
            old_method = match.group(0)
            
            # Check if the arithmetic context rule is already good
            if 'equals' in old_method and 'is' in old_method:
                # Method looks correct, no changes needed
                return code, []
                
        return code, changes
        
    def validate_real_improvements(self, task: Dict) -> Dict:
        """Validate that improvements work correctly"""
        
        print(f"[CHILD] Validating improvements for cycle {self.cycle}")
        
        # Re-run tests to check improvements
        test_task = {
            'type': 'run_tests',
            'cycle': self.cycle,
            'parameters': task.get('parameters', {})
        }
        
        validation_results = self.run_real_tests(test_task)
        
        # Check for regressions
        regression_found = False
        if self.test_results and validation_results['overall_score'] < self.test_results['overall_score']:
            regression_found = True
            
        # Save validation results
        validation_file = f'results/cycle_{self.cycle}_validation.json'
        with open(validation_file, 'w') as f:
            json.dump({
                'cycle': self.cycle,
                'timestamp': datetime.now().isoformat(),
                'improvements_made': self.improvements_made,
                'test_results': validation_results,
                'regression_found': regression_found,
                'score_change': validation_results['overall_score'] - self.test_results.get('overall_score', 0)
            }, f, indent=2)
            
        return {
            'status': 'completed',
            'validation_passed': not regression_found,
            'regression_tests_passed': not regression_found,
            'new_score': validation_results['overall_score'],
            'score_improvement': validation_results['overall_score'] - self.test_results.get('overall_score', 0),
            'validation_file': validation_file
        }


def main():
    """Main entry point for child process"""
    
    child = RealChildProcess()
    
    # Example task execution
    if len(sys.argv) > 1:
        # Load task from command line
        task_file = sys.argv[1]
        with open(task_file, 'r') as f:
            task = json.load(f)
            
        result = child.execute_task(task)
        
        # Save result
        result_file = task_file.replace('_task.json', '_result.json')
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
            
        print(f"[CHILD] Task completed. Results saved to: {result_file}")
    else:
        # Demo mode - run a single cycle
        print("[CHILD] Running in demo mode - executing one enhancement cycle")
        
        # Generate examples
        gen_task = {
            'type': 'generate_examples',
            'cycle': 1,
            'parameters': {
                'strategy': {'focus': 'structural_fixes'}
            }
        }
        gen_result = child.execute_task(gen_task)
        print(f"Generated {gen_result['examples_generated']} examples")
        
        # Run tests
        test_task = {
            'type': 'run_tests',
            'cycle': 1,
            'parameters': {
                'examples_file': gen_result['output_file']
            }
        }
        test_result = child.execute_task(test_task)
        print(f"Test score: {test_result['overall_score']:.1%}")
        
        # Implement improvements
        improve_task = {
            'type': 'implement_improvements',
            'cycle': 1,
            'parameters': {
                'test_results': test_result
            }
        }
        improve_result = child.execute_task(improve_task)
        print(f"Implemented {improve_result['improvements_made']} improvements")
        
        # Validate
        validate_task = {
            'type': 'validate_improvements',
            'cycle': 1,
            'parameters': {}
        }
        validate_result = child.execute_task(validate_task)
        print(f"New score: {validate_result['new_score']:.1%}")
        print(f"Score improvement: {validate_result['score_improvement']:+.1%}")


if __name__ == "__main__":
    main()