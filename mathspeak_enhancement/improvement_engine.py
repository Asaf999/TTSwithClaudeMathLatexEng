"""
Intelligent improvement engine that automatically implements fixes
based on test results without human intervention
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
import ast
import sys
sys.path.append('..')


class ImprovementEngine:
    """
    Automatically analyzes failures and implements improvements
    """
    
    def __init__(self, cycle: int, test_results: Dict):
        self.cycle = cycle
        self.test_results = test_results
        self.improvements_made = []
        
    def analyze_and_fix(self) -> List[Dict]:
        """Analyze test results and generate fixes"""
        
        print(f"\n🔧 Analyzing failures and generating improvements...")
        
        improvements = []
        
        # Analyze each category's failures
        for category, data in self.test_results['categories'].items():
            if data['average_score'] < 0.98:
                print(f"   Analyzing {category} (score: {data['average_score']:.2%})...")
                
                # Get common issues in this category
                if 'common_issues' in data and data['common_issues']:
                    top_issues = data['common_issues'].get('top_issues', [])
                    
                    for issue, count in top_issues[:3]:  # Fix top 3 issues
                        improvement = self.generate_improvement_for_issue(
                            issue, category, data['worst_examples']
                        )
                        if improvement:
                            improvements.append(improvement)
                            
        print(f"   Generated {len(improvements)} improvements")
        return improvements
        
    def generate_improvement_for_issue(self, issue: str, category: str, examples: List[Dict]) -> Dict:
        """Generate specific improvement for an issue"""
        
        improvement = {
            'issue': issue,
            'category': category,
            'type': self.classify_issue(issue),
            'examples': examples[:3],  # Use worst 3 examples
            'fix': None
        }
        
        # Generate fix based on issue type
        if "to the power of" in issue.lower():
            improvement['fix'] = self.fix_power_notation()
        elif "parenthes" in issue.lower():
            improvement['fix'] = self.fix_parenthesis_notation()
        elif "is' instead of 'equals" in issue.lower():
            improvement['fix'] = self.fix_equals_vs_is()
        elif "verbose" in issue.lower():
            improvement['fix'] = self.fix_verbosity()
        elif "flow" in issue.lower():
            improvement['fix'] = self.fix_flow_issues()
        elif "unclear" in issue.lower() or "ambiguous" in issue.lower():
            improvement['fix'] = self.fix_clarity_issues()
        elif "professor" in issue.lower():
            improvement['fix'] = self.fix_professor_style()
        else:
            improvement['fix'] = self.generate_generic_fix(issue, examples)
            
        return improvement
        
    def classify_issue(self, issue: str) -> str:
        """Classify the type of issue"""
        issue_lower = issue.lower()
        
        if any(word in issue_lower for word in ['power', 'squared', 'cubed']):
            return 'power_notation'
        elif 'parenthes' in issue_lower:
            return 'parenthesis'
        elif any(word in issue_lower for word in ['equals', 'is']):
            return 'equality'
        elif any(word in issue_lower for word in ['verbose', 'brief']):
            return 'brevity'
        elif any(word in issue_lower for word in ['flow', 'pause']):
            return 'fluency'
        elif any(word in issue_lower for word in ['unclear', 'ambiguous']):
            return 'clarity'
        elif 'professor' in issue_lower:
            return 'style'
        else:
            return 'other'
            
    def apply_improvements(self, improvements: List[Dict]) -> List[Dict]:
        """Apply improvements to MathSpeak codebase"""
        
        print(f"\n🔨 Applying {len(improvements)} improvements to codebase...")
        
        applied = []
        
        for i, improvement in enumerate(improvements):
            print(f"   Applying improvement {i+1}/{len(improvements)}: {improvement['issue'][:50]}...")
            
            if improvement['fix']:
                success = self.apply_single_improvement(improvement)
                if success:
                    applied.append(improvement)
                    print(f"     ✓ Applied successfully")
                else:
                    print(f"     ⚠ Failed to apply")
                    
        print(f"   Successfully applied {len(applied)} improvements")
        return applied
        
    def apply_single_improvement(self, improvement: Dict) -> bool:
        """Apply a single improvement to the codebase"""
        
        fix = improvement['fix']
        if not fix:
            return False
            
        try:
            if fix['type'] == 'pattern_update':
                return self.update_pattern_file(fix)
            elif fix['type'] == 'processor_update':
                return self.update_processor(fix)
            elif fix['type'] == 'engine_update':
                return self.update_engine(fix)
            else:
                return False
        except Exception as e:
            print(f"       Error applying fix: {e}")
            return False
            
    def fix_power_notation(self) -> Dict:
        """Fix power notation issues (squared, cubed, etc.)"""
        return {
            'type': 'pattern_update',
            'file': 'mathspeak/core/patterns.py',
            'updates': [
                {
                    'pattern': r'\^2\b',
                    'old': 'to the power of two',
                    'new': 'squared',
                    'context': 'power'
                },
                {
                    'pattern': r'\^3\b',
                    'old': 'to the power of three',
                    'new': 'cubed',
                    'context': 'power'
                },
                {
                    'pattern': r'\^\{2\}',
                    'old': 'to the power of two',
                    'new': 'squared',
                    'context': 'power'
                },
                {
                    'pattern': r'\^\{3\}',
                    'old': 'to the power of three',
                    'new': 'cubed',
                    'context': 'power'
                }
            ]
        }
        
    def fix_parenthesis_notation(self) -> Dict:
        """Fix explicit parenthesis mentions"""
        return {
            'type': 'processor_update',
            'file': 'mathspeak/core/engine.py',
            'function': 'process_parentheses',
            'updates': [
                {
                    'description': 'Remove explicit parenthesis mentions',
                    'code': '''
def process_parentheses(self, expr: str) -> str:
    """Process parentheses with natural pauses instead of explicit mentions"""
    # Replace (x+1)^2 with "x plus one, squared"
    expr = re.sub(r'\\(([^)]+)\\)\\^(\\d+)', r'\\1, to the power of \\2', expr)
    expr = re.sub(r'\\(([^)]+)\\)\\^\\{(\\d+)\\}', r'\\1, to the power of \\2', expr)
    
    # Replace (a+b)(c+d) with "a plus b, times c plus d"
    expr = re.sub(r'\\)\\s*\\(', r', times ', expr)
    
    # Remove remaining parentheses
    expr = expr.replace('(', '').replace(')', '')
    
    return expr
'''
                }
            ]
        }
        
    def fix_equals_vs_is(self) -> Dict:
        """Fix equals vs is usage"""
        return {
            'type': 'processor_update',
            'file': 'mathspeak/core/engine.py',
            'function': 'process_equality',
            'updates': [
                {
                    'description': 'Context-aware equals vs is',
                    'code': '''
def process_equality(self, expr: str, context: str = None) -> str:
    """Process equality with context awareness"""
    # Simple arithmetic uses "is"
    if context in ['arithmetic', 'basic_calculation'] or self.is_simple_arithmetic(expr):
        expr = expr.replace(' equals ', ' is ')
    # Function definitions keep "equals"
    elif 'f(' in expr or 'g(' in expr or 'h(' in expr:
        expr = expr.replace(' is ', ' equals ')
    # Default based on complexity
    elif self.count_operations(expr) <= 2:
        expr = expr.replace(' equals ', ' is ')
        
    return expr
    
def is_simple_arithmetic(self, expr: str) -> bool:
    """Check if expression is simple arithmetic"""
    # Check for only numbers and basic operations
    cleaned = re.sub(r'[0-9+\\-*/=\\s]', '', expr)
    return len(cleaned) == 0
    
def count_operations(self, expr: str) -> int:
    """Count number of operations in expression"""
    ops = ['+', '-', '*', '/', '^', '=']
    return sum(expr.count(op) for op in ops)
'''
                }
            ]
        }
        
    def fix_verbosity(self) -> Dict:
        """Fix verbose patterns"""
        return {
            'type': 'pattern_update',
            'file': 'mathspeak/core/patterns.py',
            'updates': [
                {
                    'pattern': r'\\frac\{1\}\{2\}',
                    'old': 'one over two',
                    'new': 'one half',
                    'context': 'fraction'
                },
                {
                    'pattern': r'\\frac\{1\}\{3\}',
                    'old': 'one over three',
                    'new': 'one third',
                    'context': 'fraction'
                },
                {
                    'pattern': r'\\frac\{1\}\{4\}',
                    'old': 'one over four',
                    'new': 'one quarter',
                    'context': 'fraction'
                },
                {
                    'pattern': r'\\frac\{2\}\{3\}',
                    'old': 'two over three',
                    'new': 'two thirds',
                    'context': 'fraction'
                },
                {
                    'pattern': r'\\frac\{3\}\{4\}',
                    'old': 'three over four',
                    'new': 'three quarters',
                    'context': 'fraction'
                }
            ]
        }
        
    def fix_flow_issues(self) -> Dict:
        """Fix flow and pause issues"""
        return {
            'type': 'processor_update',
            'file': 'mathspeak/core/engine.py',
            'function': 'add_natural_pauses',
            'updates': [
                {
                    'description': 'Add natural pauses for better flow',
                    'code': '''
def add_natural_pauses(self, text: str) -> str:
    """Add natural pauses for better flow"""
    # Add pause before dx in integrals
    text = re.sub(r'(\\w)\\s+d\\s*(\\w)', r'\\1, d\\2', text)
    
    # Add pause in complex fractions
    text = re.sub(r'(\\w+\\s+[+-]\\s+\\w+)\\s+over\\s+', r'\\1, over ', text)
    
    # Add pause before "times" in products
    text = re.sub(r'(\\w+)\\s+times\\s+', r'\\1, times ', text)
    
    # Add "the" for better flow
    text = re.sub(r'^(integral|limit|sum|product)\\s+', r'the \\1 ', text)
    
    return text
'''
                }
            ]
        }
        
    def fix_clarity_issues(self) -> Dict:
        """Fix clarity and ambiguity issues"""
        return {
            'type': 'processor_update',
            'file': 'mathspeak/core/engine.py',
            'function': 'clarify_ambiguous',
            'updates': [
                {
                    'description': 'Clarify ambiguous expressions',
                    'code': '''
def clarify_ambiguous(self, text: str) -> str:
    """Clarify potentially ambiguous expressions"""
    # Clarify nested operations
    text = re.sub(r'(\\w+)\\s+(\\w+)\\s+over\\s+(\\w+)\\s+(\\w+)', 
                  r'\\1 \\2, over \\3 \\4', text)
    
    # Clarify function arguments
    text = re.sub(r'f of (\\w+)\\s+(\\w+)', r'f of \\1 and \\2', text)
    
    # Add "the" before mathematical objects
    objects = ['derivative', 'integral', 'limit', 'sum', 'product', 
               'determinant', 'matrix', 'vector']
    for obj in objects:
        text = re.sub(f'\\b{obj}\\b', f'the {obj}', text)
        
    return text
'''
                }
            ]
        }
        
    def fix_professor_style(self) -> Dict:
        """Fix professor-style speech patterns"""
        return {
            'type': 'pattern_update',
            'file': 'mathspeak/core/patterns.py',
            'updates': [
                {
                    'pattern': r'\\forall',
                    'old': 'for all',
                    'new': 'for every',
                    'context': 'quantifier'
                },
                {
                    'pattern': r'\\to\\s*\\infty',
                    'old': 'goes to infinity',
                    'new': 'approaches infinity',
                    'context': 'limit'
                },
                {
                    'pattern': r'\\to\\s*0',
                    'old': 'goes to zero',
                    'new': 'approaches zero',
                    'context': 'limit'
                },
                {
                    'pattern': 'dx$',
                    'old': 'd x',
                    'new': ', d x',
                    'context': 'integral'
                }
            ]
        }
        
    def generate_generic_fix(self, issue: str, examples: List[Dict]) -> Dict:
        """Generate a generic fix based on examples"""
        
        # Analyze patterns in failures
        patterns = []
        for ex in examples[:3]:
            if 'expected' in ex and 'actual' in ex:
                expected = ex['expected']
                actual = ex['actual']
                
                # Find differences
                if expected and actual:
                    diff = self.find_key_differences(expected, actual)
                    patterns.extend(diff)
                    
        if not patterns:
            return None
            
        # Generate fix based on most common pattern
        most_common = max(set(patterns), key=patterns.count)
        
        return {
            'type': 'pattern_update',
            'file': 'mathspeak/core/patterns.py',
            'updates': [
                {
                    'pattern': most_common[0] if isinstance(most_common, tuple) else most_common,
                    'old': most_common[1] if isinstance(most_common, tuple) and len(most_common) > 1 else '',
                    'new': most_common[2] if isinstance(most_common, tuple) and len(most_common) > 2 else '',
                    'context': 'generic'
                }
            ]
        }
        
    def find_key_differences(self, expected: str, actual: str) -> List[Tuple[str, str, str]]:
        """Find key differences between expected and actual"""
        differences = []
        
        # Simple word replacements
        exp_words = expected.split()
        act_words = actual.split()
        
        for i, (e, a) in enumerate(zip(exp_words, act_words)):
            if e != a:
                # Create a pattern for this difference
                pattern = f'\\b{re.escape(a)}\\b'
                differences.append((pattern, a, e))
                
        return differences
        
    def update_pattern_file(self, fix: Dict) -> bool:
        """Update pattern file with fixes"""
        try:
            file_path = Path(f'../{fix["file"]}')
            
            if not file_path.exists():
                # Create patterns file if it doesn't exist
                file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(self.generate_patterns_template())
                    
            # Read current content
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Apply updates
            for update in fix['updates']:
                # Add or update pattern
                pattern_str = f"    (r'{update['pattern']}', '{update['new']}'),"
                
                # Check if pattern already exists
                if update['old'] in content:
                    content = content.replace(
                        f"'{update['old']}'",
                        f"'{update['new']}'"
                    )
                else:
                    # Add new pattern
                    context_section = f"# {update['context']} patterns"
                    if context_section in content:
                        # Insert after context section
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if context_section in line:
                                # Find next pattern list
                                for j in range(i+1, len(lines)):
                                    if 'patterns = [' in lines[j] or 'PATTERNS = {' in lines[j]:
                                        lines.insert(j+1, pattern_str)
                                        break
                                break
                        content = '\n'.join(lines)
                    else:
                        # Add to general patterns
                        content = self.add_pattern_to_content(content, pattern_str)
                        
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(content)
                
            return True
            
        except Exception as e:
            print(f"Error updating pattern file: {e}")
            return False
            
    def update_processor(self, fix: Dict) -> bool:
        """Update processor with new function"""
        try:
            file_path = Path(f'../{fix["file"]}')
            
            if not file_path.exists():
                return False
                
            # Read current content
            with open(file_path, 'r') as f:
                content = f.read()
                
            # Add or update function
            for update in fix['updates']:
                func_name = fix['function']
                new_code = update['code']
                
                # Check if function exists
                if f'def {func_name}' in content:
                    # Replace existing function
                    content = self.replace_function(content, func_name, new_code)
                else:
                    # Add new function
                    content = self.add_function(content, new_code)
                    
            # Write updated content
            with open(file_path, 'w') as f:
                f.write(content)
                
            return True
            
        except Exception as e:
            print(f"Error updating processor: {e}")
            return False
            
    def update_engine(self, fix: Dict) -> bool:
        """Update engine with fixes"""
        return self.update_processor(fix)  # Same process
        
    def generate_patterns_template(self) -> str:
        """Generate a template for patterns file"""
        return '''"""
Mathematical expression patterns for natural speech
Auto-generated by improvement engine
"""

import re

# Basic patterns
BASIC_PATTERNS = [
    # Powers
    (r'\\^2\\b', 'squared'),
    (r'\\^3\\b', 'cubed'),
    (r'\\^\\{2\\}', 'squared'),
    (r'\\^\\{3\\}', 'cubed'),
    
    # Fractions
    (r'\\\\frac\\{1\\}\\{2\\}', 'one half'),
    (r'\\\\frac\\{1\\}\\{3\\}', 'one third'),
    (r'\\\\frac\\{1\\}\\{4\\}', 'one quarter'),
    
    # Operations
    (r'\\+', 'plus'),
    (r'-', 'minus'),
    (r'\\\\times', 'times'),
    (r'\\\\div', 'divided by'),
]

# Advanced patterns
ADVANCED_PATTERNS = [
    # Derivatives
    (r'\\\\frac\\{d\\}\\{dx\\}', 'd by d x'),
    (r'\\\\frac\\{\\\\partial\\}\\{\\\\partial x\\}', 'partial by partial x'),
    
    # Integrals
    (r'\\\\int', 'the integral'),
    (r'\\\\sum', 'the sum'),
    (r'\\\\prod', 'the product'),
    
    # Limits
    (r'\\\\lim', 'the limit'),
    (r'\\\\to', 'approaches'),
]

def apply_patterns(text: str, patterns: list) -> str:
    """Apply patterns to text"""
    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text)
    return text
'''
        
    def add_pattern_to_content(self, content: str, pattern_str: str) -> str:
        """Add pattern to content"""
        # Find a good place to insert
        if 'BASIC_PATTERNS = [' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if 'BASIC_PATTERNS = [' in line:
                    # Find the end of the list
                    for j in range(i+1, len(lines)):
                        if ']' in lines[j] and not lines[j].strip().startswith('#'):
                            lines.insert(j, pattern_str)
                            break
                    break
            return '\n'.join(lines)
        else:
            # Just append
            return content + '\n' + pattern_str
            
    def replace_function(self, content: str, func_name: str, new_code: str) -> str:
        """Replace existing function with new code"""
        try:
            # Parse the AST
            tree = ast.parse(content)
            
            # Find the function
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == func_name:
                    # Get line numbers
                    start_line = node.lineno - 1
                    end_line = node.end_lineno
                    
                    # Replace in content
                    lines = content.split('\n')
                    
                    # Remove old function
                    del lines[start_line:end_line]
                    
                    # Insert new function
                    new_lines = new_code.strip().split('\n')
                    for i, line in enumerate(new_lines):
                        lines.insert(start_line + i, line)
                        
                    return '\n'.join(lines)
                    
        except Exception:
            # Fallback: simple text replacement
            # Find function start
            func_start = content.find(f'def {func_name}')
            if func_start == -1:
                return content
                
            # Find function end (next def or class)
            func_end = content.find('\ndef ', func_start + 1)
            if func_end == -1:
                func_end = content.find('\nclass ', func_start + 1)
            if func_end == -1:
                func_end = len(content)
                
            # Replace
            return content[:func_start] + new_code.strip() + content[func_end:]
            
    def add_function(self, content: str, new_code: str) -> str:
        """Add new function to content"""
        # Find a good place to insert (after imports, before classes)
        lines = content.split('\n')
        insert_pos = 0
        
        # Skip imports and module docstring
        in_docstring = False
        for i, line in enumerate(lines):
            if line.strip().startswith('"""') or line.strip().startswith("'''"):
                in_docstring = not in_docstring
            elif not in_docstring:
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    insert_pos = i + 1
                elif line.strip().startswith('class '):
                    # Insert before first class
                    insert_pos = i
                    break
                elif line.strip() and not line.strip().startswith('#'):
                    # Insert after imports
                    if insert_pos == 0:
                        insert_pos = i
                        
        # Insert the new function
        new_lines = ['', ''] + new_code.strip().split('\n') + ['', '']
        for i, line in enumerate(new_lines):
            lines.insert(insert_pos + i, line)
            
        return '\n'.join(lines)