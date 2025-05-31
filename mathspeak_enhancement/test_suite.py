"""
Automated naturalness test suite with intelligent metrics
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass
import numpy as np
from datetime import datetime
import sys
sys.path.append('..')

from mathspeak import MathSpeak


@dataclass
class NaturalnessMetrics:
    fluency_score: float          # 0-1: Natural flow
    brevity_score: float          # 0-1: Appropriate conciseness  
    clarity_score: float          # 0-1: Unambiguous
    context_score: float          # 0-1: Context-appropriate
    professor_score: float        # 0-1: Sounds like a professor
    
    @property
    def overall_score(self) -> float:
        return np.mean([
            self.fluency_score,
            self.brevity_score,
            self.clarity_score,
            self.context_score,
            self.professor_score
        ])


class NaturalnessTestSuite:
    """
    Comprehensive test suite for natural speech patterns
    """
    
    def __init__(self, cycle: int):
        self.cycle = cycle
        self.mathspeak = MathSpeak()
        self.results = {}
        
    def run_all_tests(self) -> Dict:
        """Run all naturalness tests automatically"""
        
        print(f"\n🧪 Running naturalness tests for Cycle {self.cycle}...")
        
        results = {
            'cycle': self.cycle,
            'timestamp': datetime.now().isoformat(),
            'categories': {},
            'overall_score': 0,
            'total_tests': 0,
            'passed_tests': 0
        }
        
        # Load examples from markdown file
        examples = self.load_examples_from_markdown()
        
        # Test each category
        for category, category_examples in examples.items():
            print(f"   Testing {category}... ", end='', flush=True)
            category_results = self.test_category(category, category_examples)
            results['categories'][category] = category_results
            results['total_tests'] += len(category_examples)
            results['passed_tests'] += category_results['passed']
            print(f"✓ ({category_results['pass_rate']:.1%} pass rate)")
            
        # Calculate overall metrics
        results['overall_score'] = self.calculate_overall_score(results)
        results['pass_rate'] = results['passed_tests'] / results['total_tests'] if results['total_tests'] > 0 else 0
        
        # Save results
        self.save_results(results)
        
        return results
        
    def load_examples_from_markdown(self) -> Dict:
        """Load examples from the markdown file"""
        examples = {}
        current_category = None
        
        md_path = Path(f'examples/cycle_{self.cycle}_examples.md')
        if not md_path.exists():
            # Generate examples if not exists
            from example_generator_md import MarkdownExampleGenerator
            generator = MarkdownExampleGenerator(self.cycle)
            generator.generate_cycle_examples()
            
        with open(md_path, 'r') as f:
            content = f.read()
            
        # Parse markdown to extract examples
        sections = content.split('## ')
        
        for section in sections:
            if section.strip():
                lines = section.strip().split('\n')
                header = lines[0].strip()
                
                # Check if this is a category section
                if any(cat in header.lower() for cat in ['arithmetic', 'algebra', 'calculus', 'linear algebra', 
                                                         'differential equations', 'complex analysis', 'topology',
                                                         'logic', 'statistics', 'number theory', 'abstract algebra',
                                                         'real analysis', 'numerical methods']):
                    
                    # Extract category name
                    category = header.split('(')[0].strip().lower().replace(' ', '_')
                    examples[category] = []
                    
                    # Parse examples from section
                    example_blocks = section.split('### Example')
                    
                    for block in example_blocks[1:]:  # Skip header
                        example = self.parse_example_block(block)
                        if example:
                            examples[category].append(example)
                            
        return examples
        
    def parse_example_block(self, block: str) -> Dict:
        """Parse a single example block from markdown"""
        try:
            lines = block.strip().split('\n')
            example = {}
            
            for line in lines:
                if line.startswith('**LaTeX**:'):
                    # Extract LaTeX between backticks
                    match = re.search(r'`([^`]+)`', line)
                    if match:
                        example['latex'] = match.group(1)
                        
                elif line.startswith('**❌ ROBOTIC**:'):
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        example['robotic'] = match.group(1)
                        
                elif line.startswith('**✅ NATURAL**:'):
                    match = re.search(r'"([^"]+)"', line)
                    if match:
                        example['natural'] = match.group(1)
                        
                elif line.startswith('**💡'):
                    example['principle'] = line.split(':', 1)[1].strip() if ':' in line else ''
                    
            return example if all(k in example for k in ['latex', 'natural']) else None
            
        except Exception:
            return None
            
    def test_category(self, category: str, examples: List[Dict]) -> Dict:
        """Test all examples in a category"""
        
        passed = 0
        failed = 0
        scores = []
        failures = []
        
        for example in examples:
            score = self.test_single_example(example)
            scores.append(score)
            
            if score.overall_score >= 0.98:
                passed += 1
            else:
                failed += 1
                actual_output = self.get_actual_output(example['latex'])
                failures.append({
                    'latex': example['latex'],
                    'expected': example['natural'],
                    'actual': actual_output,
                    'score': score,
                    'issues': self.diagnose_issues(score, example, actual_output)
                })
                
        return {
            'passed': passed,
            'failed': failed,
            'pass_rate': passed / (passed + failed) if (passed + failed) > 0 else 0,
            'average_score': np.mean([s.overall_score for s in scores]) if scores else 0,
            'score_breakdown': {
                'fluency': np.mean([s.fluency_score for s in scores]) if scores else 0,
                'brevity': np.mean([s.brevity_score for s in scores]) if scores else 0,
                'clarity': np.mean([s.clarity_score for s in scores]) if scores else 0,
                'context': np.mean([s.context_score for s in scores]) if scores else 0,
                'professor': np.mean([s.professor_score for s in scores]) if scores else 0
            },
            'common_issues': self.analyze_common_issues(failures),
            'worst_examples': sorted(failures, key=lambda x: x['score'].overall_score)[:10] if failures else []
        }
        
    def test_single_example(self, example: Dict) -> NaturalnessMetrics:
        """Test a single example for naturalness"""
        
        actual = self.get_actual_output(example['latex'])
        expected = example['natural']
        
        return NaturalnessMetrics(
            fluency_score=self.measure_fluency(actual, expected),
            brevity_score=self.measure_brevity(actual, expected),
            clarity_score=self.measure_clarity(actual, expected),
            context_score=self.measure_context_appropriateness(actual, expected, example),
            professor_score=self.measure_professor_likeness(actual, expected)
        )
        
    def get_actual_output(self, latex: str) -> str:
        """Get actual MathSpeak output"""
        try:
            return self.mathspeak.speak(latex)
        except Exception as e:
            return f"ERROR: {str(e)}"
            
    def measure_fluency(self, actual: str, expected: str) -> float:
        """
        Measure speech fluency:
        - Natural word ordering
        - Appropriate pauses (commas)
        - No awkward repetitions
        - Smooth transitions
        """
        score = 1.0
        
        # Check for awkward repetitions
        words = actual.lower().split()
        for i in range(len(words) - 1):
            if words[i] == words[i + 1] and words[i] not in ['the', 'a', 'of']:
                score -= 0.1
                
        # Check for natural pauses (commas)
        expected_commas = expected.count(',')
        actual_commas = actual.count(',')
        if abs(expected_commas - actual_commas) > 1:
            score -= 0.1 * abs(expected_commas - actual_commas)
            
        # Check for word order similarity
        expected_words = expected.lower().split()
        actual_words = actual.lower().split()
        
        # Use Levenshtein distance for word order
        distance = self.levenshtein_distance(expected_words, actual_words)
        max_len = max(len(expected_words), len(actual_words))
        if max_len > 0:
            score -= (distance / max_len) * 0.5
            
        return max(0, min(1, score))
        
    def measure_brevity(self, actual: str, expected: str) -> float:
        """
        Measure appropriate brevity:
        - No unnecessary words
        - No overly verbose descriptions
        - Appropriate level of detail
        """
        score = 1.0
        
        # Check length ratio
        len_ratio = len(actual) / len(expected) if len(expected) > 0 else 1
        if len_ratio > 1.3:  # Too verbose
            score -= (len_ratio - 1.3) * 0.5
        elif len_ratio < 0.7:  # Too brief
            score -= (0.7 - len_ratio) * 0.5
            
        # Check for verbose patterns
        verbose_patterns = [
            'to the power of two',  # Should be "squared"
            'to the power of three',  # Should be "cubed"
            'open parenthesis', 'close parenthesis',  # Should be implicit
            'subscript', 'superscript'  # Should be natural
        ]
        
        for pattern in verbose_patterns:
            if pattern in actual.lower():
                score -= 0.1
                
        return max(0, min(1, score))
        
    def measure_clarity(self, actual: str, expected: str) -> float:
        """
        Measure clarity:
        - Unambiguous pronunciation
        - Clear mathematical structure
        - Proper grouping
        """
        score = 1.0
        
        # Check for ambiguous patterns
        ambiguous_patterns = [
            r'(\w+)\s+(\w+)\s+over',  # Unclear fraction grouping
            r'plus\s+\w+\s+times',  # Unclear operation precedence
            r'equals\s+\w+\s+\w+\s+equals',  # Multiple equals confusion
        ]
        
        for pattern in ambiguous_patterns:
            if re.search(pattern, actual.lower()):
                score -= 0.15
                
        # Check for clear mathematical keywords
        math_keywords = ['integral', 'derivative', 'limit', 'sum', 'product']
        for keyword in math_keywords:
            if keyword in expected.lower() and keyword not in actual.lower():
                score -= 0.1
                
        return max(0, min(1, score))
        
    def measure_context_appropriateness(self, actual: str, expected: str, example: Dict) -> float:
        """
        Measure context appropriateness:
        - Appropriate for mathematical context
        - Correct formality level
        - Domain-specific conventions
        """
        score = 1.0
        
        context = example.get('context', '')
        
        # Check equation vs expression reading
        if '=' in example['latex']:
            if 'equals' in expected and 'is' in actual:
                # Using "is" where "equals" expected
                if context not in ['basic_calculation', 'arithmetic']:
                    score -= 0.2
            elif 'is' in expected and 'equals' in actual:
                # Using "equals" where "is" expected
                if context in ['basic_calculation', 'arithmetic']:
                    score -= 0.2
                    
        # Check for appropriate article usage
        if 'the' in expected.lower():
            the_count_expected = expected.lower().count('the')
            the_count_actual = actual.lower().count('the')
            if abs(the_count_expected - the_count_actual) > 1:
                score -= 0.1 * abs(the_count_expected - the_count_actual)
                
        return max(0, min(1, score))
        
    def measure_professor_likeness(self, actual: str, expected: str) -> float:
        """
        Measure professor-like speech:
        - Natural mathematical phrasing
        - Pedagogical clarity
        - Standard conventions
        """
        score = 1.0
        
        # Professor phrases that should appear
        professor_phrases = [
            ('for all', 'for every'),
            ('there exists', 'exists'),
            ('such that', 'so that'),
            ('if and only if', 'iff'),
            ('which gives us', 'which gives'),
            ('notice that', 'note that')
        ]
        
        for good_phrase, bad_phrase in professor_phrases:
            if good_phrase in expected.lower() and bad_phrase in actual.lower():
                score -= 0.1
                
        # Check for natural mathematical reading
        if actual == expected:
            score = 1.0  # Perfect match
        elif self.normalize_speech(actual) == self.normalize_speech(expected):
            score = 0.95  # Minor differences
            
        return max(0, min(1, score))
        
    def normalize_speech(self, text: str) -> str:
        """Normalize speech for comparison"""
        # Remove extra spaces, lowercase, remove punctuation
        text = re.sub(r'\s+', ' ', text.lower().strip())
        text = re.sub(r'[,.]', '', text)
        return text
        
    def levenshtein_distance(self, s1: List[str], s2: List[str]) -> int:
        """Calculate Levenshtein distance between word lists"""
        if len(s1) < len(s2):
            return self.levenshtein_distance(s2, s1)
            
        if len(s2) == 0:
            return len(s1)
            
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
            
        return previous_row[-1]
        
    def diagnose_issues(self, score: NaturalnessMetrics, example: Dict, actual: str) -> List[str]:
        """Diagnose specific issues with the output"""
        issues = []
        
        if score.fluency_score < 0.9:
            issues.append("Unnatural flow or awkward pauses")
            
        if score.brevity_score < 0.9:
            if 'to the power of' in actual:
                issues.append("Using 'to the power of' instead of 'squared/cubed'")
            elif 'parenthesis' in actual:
                issues.append("Explicitly mentioning parentheses")
            else:
                issues.append("Too verbose or missing conciseness")
                
        if score.clarity_score < 0.9:
            issues.append("Ambiguous or unclear pronunciation")
            
        if score.context_score < 0.9:
            if '=' in example['latex'] and 'is' in actual and 'equals' in example['natural']:
                issues.append("Using 'is' instead of 'equals' in formal context")
            else:
                issues.append("Context-inappropriate reading")
                
        if score.professor_score < 0.9:
            issues.append("Doesn't sound professorial")
            
        return issues
        
    def analyze_common_issues(self, failures: List[Dict]) -> Dict:
        """Analyze common patterns in failures"""
        if not failures:
            return {}
            
        issue_counts = {}
        for failure in failures:
            for issue in failure['issues']:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
                
        # Sort by frequency
        sorted_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'top_issues': sorted_issues[:5],
            'total_unique_issues': len(issue_counts),
            'most_common_issue': sorted_issues[0] if sorted_issues else None
        }
        
    def calculate_overall_score(self, results: Dict) -> float:
        """Calculate weighted overall score"""
        if not results['categories']:
            return 0
            
        scores = []
        weights = []
        
        # Weight by number of examples in each category
        for category, data in results['categories'].items():
            score = data['average_score']
            weight = data['passed'] + data['failed']
            scores.append(score)
            weights.append(weight)
            
        if sum(weights) == 0:
            return 0
            
        # Weighted average
        return sum(s * w for s, w in zip(scores, weights)) / sum(weights)
        
    def save_results(self, results: Dict):
        """Save test results"""
        results_path = Path(f'results/cycle_{self.cycle}_test_results.json')
        results_path.parent.mkdir(exist_ok=True)
        
        with open(results_path, 'w') as f:
            json.dump(results, f, indent=2)
            
        # Also save a summary
        summary_path = Path(f'results/cycle_{self.cycle}_test_summary.txt')
        with open(summary_path, 'w') as f:
            f.write(f"Cycle {self.cycle} Test Summary\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Overall Score: {results['overall_score']:.2%}\n")
            f.write(f"Pass Rate: {results['pass_rate']:.2%}\n\n")
            f.write("Category Scores:\n")
            for cat, data in results['categories'].items():
                f.write(f"  {cat}: {data['average_score']:.2%} ({data['pass_rate']:.2%} pass rate)\n")