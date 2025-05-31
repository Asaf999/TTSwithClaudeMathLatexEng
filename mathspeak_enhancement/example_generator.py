"""
Example generator for natural speech patterns
Creates 1000 examples per cycle showing robotic vs natural speech
"""

import json
from typing import Dict, List, Tuple
from pathlib import Path
import random


class ExampleGenerator:
    """Generate natural vs robotic speech examples"""
    
    def __init__(self, cycle: int):
        self.cycle = cycle
        self.total_examples = 1000
        
        # Category distribution
        self.categories = {
            'basic_arithmetic': 50,
            'algebra': 100,
            'calculus': 150,
            'linear_algebra': 100,
            'differential_equations': 80,
            'complex_analysis': 80,
            'topology': 70,
            'set_theory_logic': 70,
            'statistics_probability': 100,
            'number_theory': 50,
            'abstract_algebra': 50,
            'real_analysis': 50,
            'numerical_methods': 50
        }
        
    def generate_initial_examples(self) -> Dict:
        """Generate comprehensive initial examples"""
        examples = {}
        
        for category, count in self.categories.items():
            print(f"   Generating {count} {category} examples...")
            examples[category] = self._generate_category_examples(category, count)
            
        return examples
        
    def generate_from_results(self, prev_results: Dict) -> Dict:
        """Generate examples based on previous cycle results"""
        examples = {}
        
        # Adjust distribution based on performance
        adjusted_dist = self._adjust_distribution(prev_results)
        
        for category, count in adjusted_dist.items():
            examples[category] = self._generate_category_examples(category, count)
            
        return examples
        
    def _adjust_distribution(self, results: Dict) -> Dict:
        """Adjust example distribution to focus on weak areas"""
        if not results or 'categories' not in results:
            return self.categories
            
        adjusted = {}
        total_redistributed = 0
        
        # Find categories that need more examples
        for category, original_count in self.categories.items():
            if category in results['categories']:
                score = results['categories'][category]['average_score']
                
                if score < 0.98:
                    # Increase examples for weak categories
                    boost = int(original_count * (1 - score) * 2)
                    adjusted[category] = original_count + boost
                    total_redistributed += boost
                else:
                    # Reduce examples for strong categories
                    reduction = int(original_count * 0.3)
                    adjusted[category] = original_count - reduction
                    total_redistributed -= reduction
            else:
                adjusted[category] = original_count
                
        # Ensure we still have 1000 total
        scale = self.total_examples / sum(adjusted.values())
        for category in adjusted:
            adjusted[category] = int(adjusted[category] * scale)
            
        return adjusted
        
    def _generate_category_examples(self, category: str, count: int) -> List[Dict]:
        """Generate examples for a specific category"""
        
        generators = {
            'basic_arithmetic': self._generate_arithmetic_examples,
            'algebra': self._generate_algebra_examples,
            'calculus': self._generate_calculus_examples,
            'linear_algebra': self._generate_linear_algebra_examples,
            'differential_equations': self._generate_de_examples,
            'complex_analysis': self._generate_complex_examples,
            'topology': self._generate_topology_examples,
            'set_theory_logic': self._generate_logic_examples,
            'statistics_probability': self._generate_stats_examples,
            'number_theory': self._generate_number_theory_examples,
            'abstract_algebra': self._generate_abstract_algebra_examples,
            'real_analysis': self._generate_real_analysis_examples,
            'numerical_methods': self._generate_numerical_examples
        }
        
        if category in generators:
            return generators[category](count)
        else:
            return []
            
    def _generate_arithmetic_examples(self, count: int) -> List[Dict]:
        """Generate basic arithmetic examples"""
        examples = []
        
        # Simple addition
        examples.append({
            'latex': '$2 + 3 = 5$',
            'robotic': 'two plus three equals five',
            'natural': 'two plus three is five',
            'principle': 'Use "is" for simple equalities',
            'context': 'basic_calculation'
        })
        
        # Fraction addition
        examples.append({
            'latex': '$\\frac{1}{2} + \\frac{1}{3} = \\frac{5}{6}$',
            'robotic': 'one over two plus one over three equals five over six',
            'natural': 'one half plus one third equals five sixths',
            'principle': 'Use natural fraction names when possible',
            'context': 'fraction_arithmetic'
        })
        
        # Mixed numbers
        examples.append({
            'latex': '$2\\frac{3}{4}$',
            'robotic': 'two and three over four',
            'natural': 'two and three quarters',
            'principle': 'Natural reading of mixed numbers',
            'context': 'mixed_number'
        })
        
        # Multiplication
        examples.append({
            'latex': '$3 \\times 4 = 12$',
            'robotic': 'three times four equals twelve',
            'natural': 'three times four is twelve',
            'principle': 'Use "is" for simple results',
            'context': 'multiplication'
        })
        
        # Division
        examples.append({
            'latex': '$15 \\div 3 = 5$',
            'robotic': 'fifteen divided by three equals five',
            'natural': 'fifteen divided by three is five',
            'principle': 'Consistent use of "is"',
            'context': 'division'
        })
        
        # Generate more variations
        for i in range(5, count):
            examples.append(self._generate_arithmetic_variation(i))
            
        return examples[:count]
        
    def _generate_algebra_examples(self, count: int) -> List[Dict]:
        """Generate algebra examples"""
        examples = []
        
        # Quadratic expression
        examples.append({
            'latex': '$x^2 + 5x + 6$',
            'robotic': 'x to the power of two plus five x plus six',
            'natural': 'x squared plus five x plus six',
            'principle': 'Use "squared" for power of 2',
            'context': 'polynomial'
        })
        
        # Factored form
        examples.append({
            'latex': '$(x+2)(x+3)$',
            'robotic': 'open parenthesis x plus two close parenthesis open parenthesis x plus three close parenthesis',
            'natural': 'x plus two, times x plus three',
            'principle': 'Implied multiplication with pause',
            'context': 'factored_form'
        })
        
        # Equation solving
        examples.append({
            'latex': '$x^2 - 4 = 0$',
            'robotic': 'x to the power of two minus four equals zero',
            'natural': 'x squared minus four equals zero',
            'principle': 'Consistent squared notation',
            'context': 'equation'
        })
        
        # Absolute value
        examples.append({
            'latex': '$|x - 3| < 5$',
            'robotic': 'absolute value of x minus three is less than five',
            'natural': 'the absolute value of x minus three is less than five',
            'principle': 'Add article for flow',
            'context': 'inequality'
        })
        
        # Complex expression
        examples.append({
            'latex': '$\\frac{x^2 - 1}{x + 1} = x - 1$',
            'robotic': 'x squared minus one over x plus one equals x minus one',
            'natural': 'x squared minus one, over x plus one, equals x minus one',
            'principle': 'Strategic pauses for clarity',
            'context': 'rational_expression'
        })
        
        # Generate variations
        for i in range(5, count):
            examples.append(self._generate_algebra_variation(i))
            
        return examples[:count]
        
    def _generate_calculus_examples(self, count: int) -> List[Dict]:
        """Generate calculus examples"""
        examples = []
        
        # Basic derivative
        examples.append({
            'latex': '$\\frac{d}{dx} f(x)$',
            'robotic': 'd over d x f of x',
            'natural': 'd by d x of f of x',
            'principle': 'Use "by" for derivatives',
            'context': 'derivative'
        })
        
        # Prime notation
        examples.append({
            'latex': "$f'(x) = 2x$",
            'robotic': 'f prime of x equals two x',
            'natural': 'f prime of x equals two x',
            'principle': 'Prime notation is already natural',
            'context': 'derivative_prime'
        })
        
        # Definite integral
        examples.append({
            'latex': '$\\int_0^1 x^2 dx$',
            'robotic': 'integral from zero to one of x squared d x',
            'natural': 'the integral from zero to one of x squared, d x',
            'principle': 'Add article and pause before dx',
            'context': 'definite_integral'
        })
        
        # Limit
        examples.append({
            'latex': '$\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$',
            'robotic': 'limit as x goes to zero of sine x over x equals one',
            'natural': 'the limit as x approaches zero of sine x over x equals one',
            'principle': 'Use "approaches" instead of "goes to"',
            'context': 'limit'
        })
        
        # Partial derivative
        examples.append({
            'latex': '$\\frac{\\partial f}{\\partial x}$',
            'robotic': 'partial f over partial x',
            'natural': 'partial f by partial x',
            'principle': 'Consistent "by" for derivatives',
            'context': 'partial_derivative'
        })
        
        # Chain rule
        examples.append({
            'latex': '$\\frac{d}{dx}[f(g(x))] = f\'(g(x)) \\cdot g\'(x)$',
            'robotic': 'd over d x of f of g of x equals f prime of g of x times g prime of x',
            'natural': 'd by d x of f of g of x equals f prime of g of x, times g prime of x',
            'principle': 'Natural pauses in complex expressions',
            'context': 'chain_rule'
        })
        
        # Generate more variations
        for i in range(6, count):
            examples.append(self._generate_calculus_variation(i))
            
        return examples[:count]
        
    def _generate_linear_algebra_examples(self, count: int) -> List[Dict]:
        """Generate linear algebra examples"""
        examples = []
        
        # Matrix
        examples.append({
            'latex': '$\\begin{pmatrix} a & b \\\\ c & d \\end{pmatrix}$',
            'robotic': 'matrix with entries a b c d',
            'natural': 'the two by two matrix with entries a, b, c, d',
            'principle': 'Specify dimensions and pause between entries',
            'context': 'matrix'
        })
        
        # Vector
        examples.append({
            'latex': '$\\vec{v} = \\langle 1, 2, 3 \\rangle$',
            'robotic': 'vector v equals one two three',
            'natural': 'vector v equals one, two, three',
            'principle': 'Pause between components',
            'context': 'vector'
        })
        
        # Dot product
        examples.append({
            'latex': '$\\vec{a} \\cdot \\vec{b}$',
            'robotic': 'vector a dot vector b',
            'natural': 'a dot b',
            'principle': 'Omit redundant "vector" in operations',
            'context': 'dot_product'
        })
        
        # Determinant
        examples.append({
            'latex': '$\\det(A) = 0$',
            'robotic': 'determinant of A equals zero',
            'natural': 'the determinant of A equals zero',
            'principle': 'Add article for better flow',
            'context': 'determinant'
        })
        
        # Eigenvalue
        examples.append({
            'latex': '$A\\vec{v} = \\lambda\\vec{v}$',
            'robotic': 'A vector v equals lambda vector v',
            'natural': 'A v equals lambda v',
            'principle': 'Simplified vector notation in equations',
            'context': 'eigenvalue'
        })
        
        # Generate variations
        for i in range(5, count):
            examples.append(self._generate_linear_algebra_variation(i))
            
        return examples[:count]
        
    def _generate_de_examples(self, count: int) -> List[Dict]:
        """Generate differential equations examples"""
        examples = []
        
        # First order ODE
        examples.append({
            'latex': "$y' + p(x)y = q(x)$",
            'robotic': 'y prime plus p of x y equals q of x',
            'natural': 'y prime plus p of x times y equals q of x',
            'principle': 'Make multiplication explicit when needed',
            'context': 'first_order_ode'
        })
        
        # Second order ODE
        examples.append({
            'latex': "$y'' + 2y' + y = 0$",
            'robotic': 'y double prime plus two y prime plus y equals zero',
            'natural': 'y double prime plus two y prime plus y equals zero',
            'principle': 'Already natural for standard forms',
            'context': 'second_order_ode'
        })
        
        # Generate more
        for i in range(2, count):
            examples.append(self._generate_de_variation(i))
            
        return examples[:count]
        
    def _generate_complex_examples(self, count: int) -> List[Dict]:
        """Generate complex analysis examples"""
        examples = []
        
        # Complex number
        examples.append({
            'latex': '$z = 3 + 4i$',
            'robotic': 'z equals three plus four i',
            'natural': 'z equals three plus four i',
            'principle': 'Standard complex notation is natural',
            'context': 'complex_number'
        })
        
        # Euler's formula
        examples.append({
            'latex': '$e^{i\\theta} = \\cos\\theta + i\\sin\\theta$',
            'robotic': 'e to the i theta equals cosine theta plus i sine theta',
            'natural': 'e to the i theta equals cosine theta plus i sine theta',
            'principle': 'Standard transcendental reading',
            'context': 'eulers_formula'
        })
        
        # Generate more
        for i in range(2, count):
            examples.append(self._generate_complex_variation(i))
            
        return examples[:count]
        
    def _generate_topology_examples(self, count: int) -> List[Dict]:
        """Generate topology examples"""
        examples = []
        
        # Open set
        examples.append({
            'latex': '$U \\subset X$ is open',
            'robotic': 'U subset X is open',
            'natural': 'U is an open subset of X',
            'principle': 'Rearrange for natural English',
            'context': 'open_set'
        })
        
        # Homeomorphism
        examples.append({
            'latex': '$X \\cong Y$',
            'robotic': 'X is homeomorphic to Y',
            'natural': 'X is homeomorphic to Y',
            'principle': 'Technical terms remain unchanged',
            'context': 'homeomorphism'
        })
        
        # Generate more
        for i in range(2, count):
            examples.append(self._generate_topology_variation(i))
            
        return examples[:count]
        
    def _generate_logic_examples(self, count: int) -> List[Dict]:
        """Generate logic and set theory examples"""
        examples = []
        
        # Implication
        examples.append({
            'latex': '$p \\implies q$',
            'robotic': 'p implies q',
            'natural': 'p implies q',
            'principle': 'Logic symbols read naturally',
            'context': 'implication'
        })
        
        # Universal quantifier
        examples.append({
            'latex': '$\\forall x \\in \\mathbb{R}$',
            'robotic': 'for all x in R',
            'natural': 'for all x in the real numbers',
            'principle': 'Expand set names naturally',
            'context': 'quantifier'
        })
        
        # Set operations
        examples.append({
            'latex': '$A \\cup B$',
            'robotic': 'A union B',
            'natural': 'A union B',
            'principle': 'Set operations are already natural',
            'context': 'set_union'
        })
        
        # Generate more
        for i in range(3, count):
            examples.append(self._generate_logic_variation(i))
            
        return examples[:count]
        
    def _generate_stats_examples(self, count: int) -> List[Dict]:
        """Generate statistics examples"""
        examples = []
        
        # Expectation
        examples.append({
            'latex': '$E[X] = \\mu$',
            'robotic': 'E of X equals mu',
            'natural': 'the expected value of X equals mu',
            'principle': 'Expand statistical notation',
            'context': 'expectation'
        })
        
        # Probability
        examples.append({
            'latex': '$P(A|B)$',
            'robotic': 'P of A given B',
            'natural': 'the probability of A given B',
            'principle': 'Make probability explicit',
            'context': 'conditional_probability'
        })
        
        # Normal distribution
        examples.append({
            'latex': '$X \\sim N(\\mu, \\sigma^2)$',
            'robotic': 'X tilde N mu sigma squared',
            'natural': 'X follows a normal distribution with mean mu and variance sigma squared',
            'principle': 'Expand distribution notation fully',
            'context': 'distribution'
        })
        
        # Generate more
        for i in range(3, count):
            examples.append(self._generate_stats_variation(i))
            
        return examples[:count]
        
    # Helper methods for generating variations
    def _generate_arithmetic_variation(self, index: int) -> Dict:
        """Generate arithmetic variation"""
        operations = ['+', '-', '\\times', '\\div']
        op = random.choice(operations)
        a = random.randint(1, 20)
        b = random.randint(1, 20)
        
        if op == '+':
            result = a + b
            op_word = 'plus'
        elif op == '-':
            result = a - b
            op_word = 'minus'
        elif op == '\\times':
            result = a * b
            op_word = 'times'
        else:
            result = a // b
            op_word = 'divided by'
            
        return {
            'latex': f'${a} {op} {b} = {result}$',
            'robotic': f'{self._number_to_word(a)} {op_word} {self._number_to_word(b)} equals {self._number_to_word(result)}',
            'natural': f'{self._number_to_word(a)} {op_word} {self._number_to_word(b)} is {self._number_to_word(result)}',
            'principle': 'Consistent use of "is" for simple arithmetic',
            'context': 'arithmetic'
        }
        
    def _generate_algebra_variation(self, index: int) -> Dict:
        """Generate algebra variation"""
        templates = [
            {
                'latex': '$x^{n} + {a}x + {b}$',
                'robotic': 'x to the power of {n} plus {a} x plus {b}',
                'natural': 'x to the {n_word} plus {a} x plus {b}',
                'principle': 'Use ordinal for general powers'
            },
            {
                'latex': '$(x - {a})(x + {b})$',
                'robotic': 'open parenthesis x minus {a} close parenthesis open parenthesis x plus {b} close parenthesis',
                'natural': 'x minus {a}, times x plus {b}',
                'principle': 'Pause replaces parenthesis mention'
            }
        ]
        
        template = random.choice(templates)
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        n = random.randint(3, 5)
        
        return {
            'latex': template['latex'].format(a=a, b=b, n=n),
            'robotic': template['robotic'].format(a=a, b=b, n=n),
            'natural': template['natural'].format(a=a, b=b, n=n, n_word=self._ordinal(n)),
            'principle': template['principle'],
            'context': 'algebra'
        }
        
    def _generate_calculus_variation(self, index: int) -> Dict:
        """Generate calculus variation"""
        templates = [
            {
                'latex': '$\\int_{{a}}^{{b}} {func} dx$',
                'robotic': 'integral from {a} to {b} of {func_word} d x',
                'natural': 'the integral from {a} to {b} of {func_word}, d x',
                'principle': 'Article and pause pattern'
            },
            {
                'latex': '$\\lim_{{x \\to {a}}} {func}$',
                'robotic': 'limit as x goes to {a} of {func_word}',
                'natural': 'the limit as x approaches {a} of {func_word}',
                'principle': 'Use "approaches" for limits'
            }
        ]
        
        funcs = [
            ('x^2', 'x squared'),
            ('\\sin x', 'sine x'),
            ('e^x', 'e to the x'),
            ('\\ln x', 'natural log x')
        ]
        
        template = random.choice(templates)
        func, func_word = random.choice(funcs)
        a = random.randint(0, 5)
        b = random.randint(a + 1, 10)
        
        return {
            'latex': template['latex'].format(a=a, b=b, func=func),
            'robotic': template['robotic'].format(a=a, b=b, func_word=func_word),
            'natural': template['natural'].format(a=a, b=b, func_word=func_word),
            'principle': template['principle'],
            'context': 'calculus'
        }
        
    def _generate_linear_algebra_variation(self, index: int) -> Dict:
        """Generate linear algebra variation"""
        size = random.choice(['2', '3', 'n'])
        
        if size == 'n':
            size_word = 'n by n'
        else:
            size_word = f'{size} by {size}'
            
        return {
            'latex': f'$A \\in \\mathbb{{R}}^{{{size} \\times {size}}}$',
            'robotic': f'A in R {size} times {size}',
            'natural': f'A is an {size_word} real matrix',
            'principle': 'Natural description of matrix spaces',
            'context': 'matrix_space'
        }
        
    def _generate_de_variation(self, index: int) -> Dict:
        """Generate differential equation variation"""
        order = random.choice(['first', 'second'])
        
        if order == 'first':
            return {
                'latex': "$y' = f(x, y)$",
                'robotic': 'y prime equals f of x y',
                'natural': 'y prime equals f of x and y',
                'principle': 'Use "and" for multiple function arguments',
                'context': 'differential_equation'
            }
        else:
            return {
                'latex': "$y'' + p(x)y' + q(x)y = 0$",
                'robotic': 'y double prime plus p of x y prime plus q of x y equals zero',
                'natural': 'y double prime plus p of x times y prime plus q of x times y equals zero',
                'principle': 'Explicit multiplication in ODEs',
                'context': 'second_order_ode'
            }
            
    def _generate_complex_variation(self, index: int) -> Dict:
        """Generate complex analysis variation"""
        real = random.randint(-5, 5)
        imag = random.randint(-5, 5)
        
        if imag >= 0:
            sign = '+'
        else:
            sign = '-'
            imag = abs(imag)
            
        return {
            'latex': f'$z = {real} {sign} {imag}i$',
            'robotic': f'z equals {self._number_to_word(real)} {sign} {self._number_to_word(imag)} i',
            'natural': f'z equals {self._number_to_word(real)} {sign} {self._number_to_word(imag)} i',
            'principle': 'Complex numbers already read naturally',
            'context': 'complex_number'
        }
        
    def _generate_topology_variation(self, index: int) -> Dict:
        """Generate topology variation"""
        concepts = [
            {
                'latex': '$\\partial A$',
                'robotic': 'partial A',
                'natural': 'the boundary of A',
                'principle': 'Use descriptive terms for topology'
            },
            {
                'latex': '$\\overline{A}$',
                'robotic': 'A bar',
                'natural': 'the closure of A',
                'principle': 'Topological notation expansion'
            }
        ]
        
        return random.choice(concepts)
        
    def _generate_logic_variation(self, index: int) -> Dict:
        """Generate logic variation"""
        quantifiers = [
            ('\\forall', 'for all'),
            ('\\exists', 'there exists')
        ]
        
        quant_symbol, quant_word = random.choice(quantifiers)
        
        return {
            'latex': f'${quant_symbol} x : P(x)$',
            'robotic': f'{quant_word} x such that P of x',
            'natural': f'{quant_word} x such that P of x',
            'principle': 'Logic notation is mostly natural',
            'context': 'logic'
        }
        
    def _generate_stats_variation(self, index: int) -> Dict:
        """Generate statistics variation"""
        distributions = [
            ('\\text{Binomial}(n, p)', 'binomial with parameters n and p'),
            ('\\text{Poisson}(\\lambda)', 'Poisson with parameter lambda'),
            ('\\text{Exp}(\\lambda)', 'exponential with rate lambda')
        ]
        
        dist_latex, dist_natural = random.choice(distributions)
        
        return {
            'latex': f'$X \\sim {dist_latex}$',
            'robotic': f'X tilde {dist_latex}',
            'natural': f'X follows a {dist_natural}',
            'principle': 'Expand distribution notation completely',
            'context': 'probability_distribution'
        }
        
    def _generate_number_theory_examples(self, count: int) -> List[Dict]:
        """Generate number theory examples"""
        examples = []
        
        examples.append({
            'latex': '$\\gcd(a, b) = d$',
            'robotic': 'g c d of a b equals d',
            'natural': 'the greatest common divisor of a and b equals d',
            'principle': 'Expand abbreviations',
            'context': 'number_theory'
        })
        
        # Generate variations
        for i in range(1, count):
            examples.append({
                'latex': f'${random.randint(2, 20)} \\equiv {random.randint(0, 9)} \\pmod{{{random.randint(2, 10)}}}$',
                'robotic': 'congruent to mod',
                'natural': 'is congruent to... modulo...',
                'principle': 'Natural modular arithmetic reading',
                'context': 'modular_arithmetic'
            })
            
        return examples[:count]
        
    def _generate_abstract_algebra_examples(self, count: int) -> List[Dict]:
        """Generate abstract algebra examples"""
        examples = []
        
        examples.append({
            'latex': '$G/H$',
            'robotic': 'G over H',
            'natural': 'G mod H',
            'principle': 'Use "mod" for quotient groups',
            'context': 'quotient_group'
        })
        
        for i in range(1, count):
            examples.append(self._generate_abstract_variation(i))
            
        return examples[:count]
        
    def _generate_real_analysis_examples(self, count: int) -> List[Dict]:
        """Generate real analysis examples"""
        examples = []
        
        examples.append({
            'latex': '$\\{x_n\\} \\to x$',
            'robotic': 'x n converges to x',
            'natural': 'the sequence x n converges to x',
            'principle': 'Make sequence explicit',
            'context': 'convergence'
        })
        
        for i in range(1, count):
            examples.append(self._generate_analysis_variation(i))
            
        return examples[:count]
        
    def _generate_numerical_examples(self, count: int) -> List[Dict]:
        """Generate numerical methods examples"""
        examples = []
        
        examples.append({
            'latex': '$x_{n+1} = x_n - \\frac{f(x_n)}{f\'(x_n)}$',
            'robotic': 'x sub n plus one equals x sub n minus f of x sub n over f prime of x sub n',
            'natural': 'x n plus one equals x n minus f of x n over f prime of x n',
            'principle': 'Simplified subscript reading',
            'context': 'newton_method'
        })
        
        for i in range(1, count):
            examples.append(self._generate_numerical_variation(i))
            
        return examples[:count]
        
    def _generate_abstract_variation(self, index: int) -> Dict:
        """Generate abstract algebra variation"""
        return {
            'latex': '$[G:H] = n$',
            'robotic': 'G colon H equals n',
            'natural': 'the index of H in G equals n',
            'principle': 'Descriptive reading of notation',
            'context': 'group_index'
        }
        
    def _generate_analysis_variation(self, index: int) -> Dict:
        """Generate real analysis variation"""
        return {
            'latex': '$\\sup A$',
            'robotic': 'sup A',
            'natural': 'the supremum of A',
            'principle': 'Expand abbreviated terms',
            'context': 'supremum'
        }
        
    def _generate_numerical_variation(self, index: int) -> Dict:
        """Generate numerical methods variation"""
        return {
            'latex': '$O(h^2)$',
            'robotic': 'O of h squared',
            'natural': 'order h squared',
            'principle': 'Natural big-O notation',
            'context': 'complexity'
        }
        
    def _number_to_word(self, n: int) -> str:
        """Convert number to word form"""
        # Simple implementation for small numbers
        words = {
            0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four',
            5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine',
            10: 'ten', 11: 'eleven', 12: 'twelve', 13: 'thirteen',
            14: 'fourteen', 15: 'fifteen', 16: 'sixteen', 17: 'seventeen',
            18: 'eighteen', 19: 'nineteen', 20: 'twenty'
        }
        
        if n in words:
            return words[n]
        elif n < 100:
            tens = n // 10
            ones = n % 10
            tens_words = {2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty',
                         6: 'sixty', 7: 'seventy', 8: 'eighty', 9: 'ninety'}
            if ones == 0:
                return tens_words[tens]
            else:
                return f'{tens_words[tens]}-{words[ones]}'
        else:
            return str(n)
            
    def _ordinal(self, n: int) -> str:
        """Convert number to ordinal form"""
        if n == 2:
            return 'squared'
        elif n == 3:
            return 'cubed'
        else:
            suffix = 'th'
            if n % 10 == 1 and n != 11:
                suffix = 'st'
            elif n % 10 == 2 and n != 12:
                suffix = 'nd'
            elif n % 10 == 3 and n != 13:
                suffix = 'rd'
            return f'{n}{suffix}'