"""
Adaptive example generator - creates examples based on weak areas
"""

import json
from pathlib import Path
from typing import Dict, List
import random

from example_generator_md import MarkdownExampleGenerator


class AdaptiveExampleGenerator:
    """Generate examples based on what needs improvement"""
    
    def generate_next_cycle_examples(self, next_cycle: int, test_results: Dict) -> Dict:
        """
        Generate examples for next cycle focusing on weak areas
        """
        
        print(f"\n📊 Generating adaptive examples for Cycle {next_cycle}...")
        
        # Analyze where we're failing
        weak_areas = self.identify_weak_areas(test_results)
        
        if not weak_areas:
            print("   No weak areas identified - maintaining balanced distribution")
            # Just generate standard examples
            generator = MarkdownExampleGenerator(next_cycle)
            generator.generate_cycle_examples()
            return {}
            
        print(f"   Identified {len(weak_areas)} weak areas to focus on")
        
        # Generate focused examples
        self.generate_focused_examples(next_cycle, weak_areas)
        
        return {
            'weak_areas': weak_areas,
            'focus_categories': [area['category'] for area in weak_areas[:3]]
        }
        
    def identify_weak_areas(self, results: Dict) -> List[Dict]:
        """Identify areas needing more examples"""
        
        weak_areas = []
        
        for category, data in results['categories'].items():
            if data['average_score'] < 0.98:
                # Analyze specific failure patterns
                patterns = []
                
                if 'worst_examples' in data:
                    for ex in data['worst_examples'][:5]:
                        if 'issues' in ex:
                            patterns.extend(ex['issues'])
                            
                weak_areas.append({
                    'category': category,
                    'score': data['average_score'],
                    'gap': 0.98 - data['average_score'],
                    'patterns': list(set(patterns)),
                    'priority': (0.98 - data['average_score']) * 100,
                    'failure_count': data.get('failed', 0)
                })
                
        return sorted(weak_areas, key=lambda x: x['priority'], reverse=True)
        
    def generate_focused_examples(self, cycle: int, weak_areas: List[Dict]):
        """Generate examples focused on weak areas"""
        
        # Create a custom example distribution
        total_examples = 1000
        focused_examples = {}
        
        # Allocate 70% of examples to weak areas
        weak_allocation = int(total_examples * 0.7)
        remaining = total_examples - weak_allocation
        
        # Distribute among weak areas by priority
        total_priority = sum(area['priority'] for area in weak_areas)
        
        for area in weak_areas:
            category = area['category']
            if total_priority > 0:
                allocation = int(weak_allocation * (area['priority'] / total_priority))
            else:
                allocation = weak_allocation // len(weak_areas)
                
            focused_examples[category] = {
                'count': allocation,
                'focus_patterns': area['patterns'],
                'current_score': area['score']
            }
            
        # Generate the markdown file with focused examples
        self.generate_focused_markdown(cycle, focused_examples, weak_areas)
        
    def generate_focused_markdown(self, cycle: int, focused_examples: Dict, weak_areas: List[Dict]):
        """Generate markdown with focused examples"""
        
        output_path = Path(f'examples/cycle_{cycle}_examples.md')
        output_path.parent.mkdir(exist_ok=True)
        
        with open(output_path, 'w') as f:
            # Header
            f.write(f"# MathSpeak Natural Speech Examples - Cycle {cycle}\n\n")
            f.write("**Type**: Adaptive Generation\n")
            f.write(f"**Focus**: {len(weak_areas)} weak areas identified\n\n")
            
            # Weak areas summary
            f.write("## Focus Areas for This Cycle\n\n")
            for i, area in enumerate(weak_areas[:5], 1):
                f.write(f"{i}. **{area['category']}** (current: {area['score']:.2%}, gap: {area['gap']:.2%})\n")
                f.write(f"   - Issues: {', '.join(area['patterns'][:3])}\n")
                
            f.write("\n---\n\n")
            
            # Generate examples for each category
            for area in weak_areas:
                category = area['category']
                f.write(f"## {category.replace('_', ' ').title()}\n\n")
                f.write(f"*Current Score: {area['score']:.2%} | Target: 98% | Examples: {focused_examples.get(category, {}).get('count', 50)}*\n\n")
                
                # Generate targeted examples based on failure patterns
                examples = self.generate_targeted_examples(category, area['patterns'], 
                                                         focused_examples.get(category, {}).get('count', 50))
                
                for i, example in enumerate(examples, 1):
                    f.write(f"### Example {i}\n")
                    f.write(f"**LaTeX**: `{example['latex']}`  \n")
                    f.write(f"**❌ ROBOTIC**: \"{example['robotic']}\"  \n")
                    f.write(f"**✅ NATURAL**: \"{example['natural']}\"  \n")
                    f.write(f"**💡 INSIGHT**: {example['insight']}  \n")
                    f.write(f"**🎯 TARGETS**: {example['targets']}\n\n")
                    
            # Summary
            f.write("\n---\n\n")
            f.write("## Adaptive Generation Summary\n\n")
            f.write("This cycle's examples specifically target the identified weak areas:\n\n")
            for area in weak_areas[:5]:
                f.write(f"- **{area['category']}**: Focused on {', '.join(area['patterns'][:2])}\n")
                
    def generate_targeted_examples(self, category: str, patterns: List[str], count: int) -> List[Dict]:
        """Generate examples targeting specific patterns"""
        
        examples = []
        
        # Map patterns to example generators
        pattern_generators = {
            "Using 'to the power of' instead of 'squared/cubed'": self.gen_power_examples,
            "Explicitly mentioning parentheses": self.gen_parenthesis_examples,
            "Using 'is' instead of 'equals' in formal context": self.gen_equals_examples,
            "Too verbose or missing conciseness": self.gen_concise_examples,
            "Unnatural flow or awkward pauses": self.gen_flow_examples,
            "Ambiguous or unclear pronunciation": self.gen_clarity_examples,
            "Doesn't sound professorial": self.gen_professor_examples
        }
        
        # Generate examples for each pattern
        examples_per_pattern = max(5, count // len(patterns)) if patterns else count
        
        for pattern in patterns:
            for generator_key, generator_func in pattern_generators.items():
                if generator_key in pattern:
                    examples.extend(generator_func(category, examples_per_pattern))
                    break
            else:
                # Default examples if no specific generator
                examples.extend(self.gen_default_examples(category, pattern, examples_per_pattern))
                
        # Ensure we have exactly the right count
        if len(examples) < count:
            examples.extend(self.gen_default_examples(category, "general", count - len(examples)))
        elif len(examples) > count:
            examples = examples[:count]
            
        return examples
        
    def gen_power_examples(self, category: str, count: int) -> List[Dict]:
        """Generate examples for power notation issues"""
        examples = []
        
        # Common powers that should be natural
        powers = [
            (2, "squared"),
            (3, "cubed"),
            (4, "to the fourth"),
            (5, "to the fifth"),
            (-1, "to the minus one"),
            (-2, "to the minus two")
        ]
        
        for i in range(min(count, len(powers))):
            power, natural = powers[i]
            examples.append({
                'latex': f'$x^{{{power}}}$' if power != 2 else '$x^2$',
                'robotic': f'x to the power of {power}' if power in [2, 3] else f'x {natural}',
                'natural': f'x {natural}',
                'insight': f'Always use "{natural}" for x^{power}, never "to the power of"',
                'targets': 'Power notation naturalness'
            })
            
        return examples
        
    def gen_parenthesis_examples(self, category: str, count: int) -> List[Dict]:
        """Generate examples for parenthesis issues"""
        examples = []
        
        templates = [
            {
                'latex': '$(x+1)^2$',
                'robotic': 'open parenthesis x plus one close parenthesis squared',
                'natural': 'x plus one, squared',
                'insight': 'Pause replaces parenthesis mention'
            },
            {
                'latex': '$(a+b)(c+d)$',
                'robotic': 'open parenthesis a plus b close parenthesis open parenthesis c plus d close parenthesis',
                'natural': 'a plus b, times c plus d',
                'insight': 'Implied multiplication with strategic pauses'
            },
            {
                'latex': '$f(x+1)$',
                'robotic': 'f of open parenthesis x plus one close parenthesis',
                'natural': 'f of x plus one',
                'insight': 'Function arguments never need parenthesis mentions'
            }
        ]
        
        for i in range(min(count, len(templates))):
            ex = templates[i]
            ex['targets'] = 'Parenthesis handling'
            examples.append(ex)
            
        return examples
        
    def gen_equals_examples(self, category: str, count: int) -> List[Dict]:
        """Generate examples for equals vs is"""
        examples = []
        
        contexts = [
            {
                'latex': '$2 + 2 = 4$',
                'robotic': 'two plus two equals four',
                'natural': 'two plus two is four',
                'insight': 'Simple arithmetic uses "is"',
                'context': 'arithmetic'
            },
            {
                'latex': '$f(x) = x^2 + 1$',
                'robotic': 'f of x is x squared plus one',
                'natural': 'f of x equals x squared plus one',
                'insight': 'Function definitions use "equals"',
                'context': 'definition'
            },
            {
                'latex': '$\\int_0^1 x dx = \\frac{1}{2}$',
                'robotic': 'the integral from zero to one of x dx is one half',
                'natural': 'the integral from zero to one of x, dx, equals one half',
                'insight': 'Formal results use "equals"',
                'context': 'formal'
            }
        ]
        
        for i in range(min(count, len(contexts))):
            ex = contexts[i]
            ex['targets'] = 'Equals vs is context'
            examples.append(ex)
            
        return examples
        
    def gen_concise_examples(self, category: str, count: int) -> List[Dict]:
        """Generate examples for conciseness"""
        examples = []
        
        verbose_fixes = [
            {
                'latex': '$\\frac{1}{2}$',
                'robotic': 'one over two',
                'natural': 'one half',
                'insight': 'Use natural fraction names'
            },
            {
                'latex': '$\\det(A)$',
                'robotic': 'det of A',
                'natural': 'the determinant of A',
                'insight': 'Expand abbreviations but stay concise'
            },
            {
                'latex': '$x_n$',
                'robotic': 'x subscript n',
                'natural': 'x n',
                'insight': 'Drop "subscript" for simple indices'
            }
        ]
        
        for i in range(min(count, len(verbose_fixes))):
            ex = verbose_fixes[i]
            ex['targets'] = 'Conciseness'
            examples.append(ex)
            
        return examples
        
    def gen_flow_examples(self, category: str, count: int) -> List[Dict]:
        """Generate examples for flow issues"""
        examples = []
        
        flow_examples = [
            {
                'latex': '$\\int x^2 dx$',
                'robotic': 'integral x squared d x',
                'natural': 'the integral of x squared, d x',
                'insight': 'Add "the" and pause before dx'
            },
            {
                'latex': '$\\lim_{x \\to 0} f(x)$',
                'robotic': 'limit as x goes to zero of f of x',
                'natural': 'the limit as x approaches zero of f of x',
                'insight': 'Use "approaches" not "goes to"'
            }
        ]
        
        for i in range(min(count, len(flow_examples))):
            ex = flow_examples[i]
            ex['targets'] = 'Natural flow'
            examples.append(ex)
            
        return examples
        
    def gen_clarity_examples(self, category: str, count: int) -> List[Dict]:
        """Generate examples for clarity"""
        examples = []
        
        clarity_examples = [
            {
                'latex': '$x^2 + 2x + 1 = (x+1)^2$',
                'robotic': 'x squared plus two x plus one equals x plus one squared',
                'natural': 'x squared plus two x plus one equals x plus one, squared',
                'insight': 'Pause clarifies what is being squared'
            }
        ]
        
        for i in range(min(count, len(clarity_examples))):
            ex = clarity_examples[i]
            ex['targets'] = 'Clarity'
            examples.append(ex)
            
        return examples
        
    def gen_professor_examples(self, category: str, count: int) -> List[Dict]:
        """Generate professor-style examples"""
        examples = []
        
        professor_examples = [
            {
                'latex': '$\\forall x \\in \\mathbb{R}$',
                'robotic': 'for all x in R',
                'natural': 'for every x in the real numbers',
                'insight': 'Professors say "for every" and expand set names'
            }
        ]
        
        for i in range(min(count, len(professor_examples))):
            ex = professor_examples[i]
            ex['targets'] = 'Professor style'
            examples.append(ex)
            
        return examples
        
    def gen_default_examples(self, category: str, pattern: str, count: int) -> List[Dict]:
        """Generate default examples for a category"""
        examples = []
        
        for i in range(count):
            examples.append({
                'latex': f'$x_{{{i+1}}}$',
                'robotic': f'x subscript {i+1}',
                'natural': f'x {i+1}',
                'insight': 'Natural subscript reading',
                'targets': pattern
            })
            
        return examples