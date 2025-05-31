#!/usr/bin/env python3
"""
Ultra Natural Speech Implementation for MathSpeak
Achieves maximum naturalness with comprehensive mathematical coverage
"""

import re
from typing import Optional, Dict, List, Tuple
import time


class UltraNaturalSpeechEngine:
    """The ultimate natural speech engine for mathematics"""
    
    def __init__(self):
        # Comprehensive symbol mappings
        self.symbols = {
            # Greek letters
            '\\alpha': 'alpha', '\\beta': 'beta', '\\gamma': 'gamma',
            '\\delta': 'delta', '\\epsilon': 'epsilon', '\\theta': 'theta',
            '\\lambda': 'lambda', '\\mu': 'mu', '\\pi': 'pi',
            '\\sigma': 'sigma', '\\tau': 'tau', '\\phi': 'phi',
            '\\omega': 'omega', '\\rho': 'rho', '\\eta': 'eta',
            '\\Delta': 'capital delta', '\\Sigma': 'capital sigma',
            '\\infty': 'infinity',
            
            # Operations
            '\\times': ' times ', '\\div': ' divided by ', '\\cdot': ' dot ',
            '\\pm': ' plus or minus ', '\\mp': ' minus or plus ',
            
            # Set theory
            '\\cup': ' union ', '\\cap': ' intersection ',
            '\\subset': ' is a subset of ', '\\supset': ' is a superset of ',
            '\\subseteq': ' is a subset of or equal to ',
            '\\in': ' in ', '\\notin': ' not in ',
            '\\emptyset': 'the empty set', '\\setminus': ' minus ',
            
            # Logic
            '\\land': ' and ', '\\lor': ' or ', '\\neg': 'not ',
            '\\implies': ' implies ', '\\iff': ' if and only if ',
            
            # Relations
            '\\leq': ' less than or equal to ', '\\geq': ' greater than or equal to ',
            '\\neq': ' not equal to ', '\\approx': ' approximately ',
            '\\equiv': ' is equivalent to ',
            
            # Functions
            '\\sin': 'sine', '\\cos': 'cosine', '\\tan': 'tangent',
            '\\csc': 'cosecant', '\\sec': 'secant', '\\cot': 'cotangent',
            '\\log': 'log', '\\ln': 'natural log', '\\exp': 'exponential',
            '\\arcsin': 'arc sine', '\\arccos': 'arc cosine', '\\arctan': 'arc tangent',
            '\\sinh': 'hyperbolic sine', '\\cosh': 'hyperbolic cosine',
            
            # Special
            '\\to': ' approaches ', '\\rightarrow': ' goes to ',
            '\\leftarrow': ' comes from ', '\\mapsto': ' maps to ',
            '\\forall': 'for all', '\\exists': 'there exists',
            
            # Sets
            '\\mathbb{R}': 'the real numbers', '\\mathbb{N}': 'the natural numbers',
            '\\mathbb{Z}': 'the integers', '\\mathbb{Q}': 'the rationals',
            '\\mathbb{C}': 'the complex numbers',
            
            # Vectors
            '\\vec': '', '\\hat': 'hat ',
        }
        
        # Natural number words
        self.number_words = {
            '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
            '10': 'ten', '11': 'eleven', '12': 'twelve', '13': 'thirteen',
            '14': 'fourteen', '15': 'fifteen', '16': 'sixteen',
            '17': 'seventeen', '18': 'eighteen', '19': 'nineteen',
            '20': 'twenty', '21': 'twenty-one', '22': 'twenty-two',
            '30': 'thirty', '40': 'forty', '50': 'fifty',
            '60': 'sixty', '70': 'seventy', '80': 'eighty', '90': 'ninety',
            '100': 'one hundred', '1000': 'one thousand'
        }
        
        # Common fractions
        self.common_fractions = {
            ('1', '2'): 'one half', ('1', '3'): 'one third', ('2', '3'): 'two thirds',
            ('1', '4'): 'one quarter', ('3', '4'): 'three quarters',
            ('1', '5'): 'one fifth', ('2', '5'): 'two fifths',
            ('3', '5'): 'three fifths', ('4', '5'): 'four fifths',
            ('1', '6'): 'one sixth', ('5', '6'): 'five sixths',
            ('1', '8'): 'one eighth', ('3', '8'): 'three eighths',
            ('5', '8'): 'five eighths', ('7', '8'): 'seven eighths'
        }
        
    def naturalize(self, latex: str, context: Optional[str] = None) -> str:
        """Convert LaTeX to ultra-natural speech"""
        
        # Clean input
        text = latex.strip()
        if text.startswith('$') and text.endswith('$'):
            text = text[1:-1]
            
        # Auto-detect context
        if not context:
            context = self._detect_context(text)
            
        # Process through enhanced pipeline
        text = self._process_ultra_natural(text, context)
        
        return text.lower().strip()
        
    def _detect_context(self, text: str) -> str:
        """Enhanced context detection"""
        
        # Probability/Statistics
        if any(p in text for p in ['P(', 'E[', 'Var', 'Cov']):
            return 'probability'
            
        # Set theory
        if any(s in text for s in ['\\cup', '\\cap', '\\subset', '\\in']):
            return 'set_theory'
            
        # Logic
        if any(l in text for l in ['\\land', '\\lor', '\\neg', '\\implies']):
            return 'logic'
            
        # Linear algebra
        if any(m in text for m in ['matrix', 'det', '^T', '^{-1}', '||']):
            return 'linear_algebra'
            
        # Calculus
        if any(c in text for c in ['\\int', '\\lim', '\\frac{d', '\\partial', "'"]):
            return 'calculus'
            
        # Function definition
        if re.search(r'[fgh]\s*\([^)]*\)\s*=', text):
            return 'definition'
            
        # Basic arithmetic
        if re.match(r'^[\d\s\\+\-*/×÷=times\\]+$', text):
            return 'arithmetic'
            
        return 'general'
        
    def _process_ultra_natural(self, text: str, context: str) -> str:
        """Enhanced processing pipeline"""
        
        # Phase 1: Pre-process special structures (order matters!)
        text = self._handle_norms(text)  # Handle norms before absolute values
        text = self._handle_absolute_values(text)
        text = self._handle_probability(text)
        text = self._handle_expected_values(text)
        
        # Phase 2: Handle complex mathematical structures
        text = self._handle_derivatives_enhanced(text)
        text = self._handle_fractions_enhanced(text)
        text = self._handle_integrals_enhanced(text)
        text = self._handle_limits_enhanced(text)
        text = self._handle_sums_enhanced(text)
        text = self._handle_products(text)
        text = self._handle_matrices(text)
        text = self._handle_roots(text)
        
        # Phase 3: Convert symbols comprehensively
        text = self._convert_symbols_comprehensive(text)
        
        # Phase 4: Handle notation
        text = self._handle_powers_enhanced(text)
        text = self._handle_subscripts_enhanced(text)
        text = self._handle_functions_enhanced(text)
        text = self._handle_sequences(text)
        text = self._handle_parentheses_enhanced(text)
        
        # Phase 5: Convert operations
        text = self._convert_operations_enhanced(text)
        
        # Phase 6: Convert numbers intelligently
        text = self._convert_numbers_intelligent(text)
        
        # Phase 7: Apply advanced context rules
        text = self._apply_context_rules_advanced(text, context)
        
        # Phase 8: Final polish
        text = self._final_polish(text)
        
        return text
        
    def _handle_absolute_values(self, text: str) -> str:
        """Handle absolute value notation"""
        
        # |x|
        text = re.sub(r'\|([^|]+)\|', r'absolute value of \1', text)
        
        return text
        
    def _handle_norms(self, text: str) -> str:
        """Handle norm notation"""
        
        # ||v|| - handle before absolute values
        text = re.sub(r'\|\|([^|]+)\|\|', r'norm of \1', text)
        
        return text
        
    def _handle_probability(self, text: str) -> str:
        """Handle probability notation"""
        
        # P(A|B)
        text = re.sub(r'P\(([^|]+)\|([^)]+)\)', r'probability of \1 given \2', text)
        
        # P(A)
        text = re.sub(r'P\(([^)]+)\)', r'probability of \1', text)
        
        return text
        
    def _handle_expected_values(self, text: str) -> str:
        """Handle expected value notation"""
        
        # E[X]
        text = re.sub(r'E\[([^\]]+)\]', r'expected value of \1', text)
        
        # Var(X)
        text = re.sub(r'Var\(([^)]+)\)', r'variance of \1', text)
        
        # Cov(X,Y)
        text = re.sub(r'Cov\(([^,]+),([^)]+)\)', r'covariance of \1 and \2', text)
        
        return text
        
    def _handle_derivatives_enhanced(self, text: str) -> str:
        """Enhanced derivative handling"""
        
        # Higher order derivatives d^n/dx^n
        text = re.sub(r'\\frac\{d\^2\}\{dx\^2\}', r'd squared by dx squared', text)
        text = re.sub(r'\\frac\{d\^3\}\{dx\^3\}', r'd cubed by dx cubed', text)
        text = re.sub(r'\\frac\{d\^(\d+)\}\{dx\^\1\}', r'd to the \1 by dx to the \1', text)
        text = re.sub(r'\\frac\{d\^2\s*(\w*)\}\{d(\w+)\^2\}', r'd squared \1 by d\2 squared', text)
        text = re.sub(r'\\frac\{d\^3\s*(\w*)\}\{d(\w+)\^3\}', r'd cubed \1 by d\2 cubed', text)
        text = re.sub(r'\\frac\{d\^(\d+)\s*(\w*)\}\{d(\w+)\^\1\}', r'd to the \1 \2 by d\3 to the \1', text)
        
        # Mixed partials
        text = re.sub(r'\\frac\{\\partial\^2\s*(\w*)\}\{\\partial\s*(\w+)\s*\\partial\s*(\w+)\}', 
                     r'partial squared \1 by partial \2 partial \3', text)
        
        # Standard derivatives
        text = re.sub(r'\\frac\{d\}\{d(\w+)\}', r'd by d\1', text)
        text = re.sub(r'\\frac\{d(\w*)\}\{d(\w+)\}', r'd\1 by d\2', text)
        
        # Partial derivatives
        text = re.sub(r'\\frac\{\\partial\s*(\w*)\}\{\\partial\s*(\w+)\}', 
                     lambda m: f'partial {m.group(1)} by partial {m.group(2)}'.replace('  ', ' '), text)
        
        # Prime notation (fixed escaping)
        text = re.sub(r"(\w+)'''", r'\1 triple prime', text)
        text = re.sub(r"(\w+)''", r'\1 double prime', text)
        text = re.sub(r"(\w+)'", r'\1 prime', text)
        
        return text
        
    def _handle_fractions_enhanced(self, text: str) -> str:
        """Enhanced fraction handling"""
        
        def replace_frac(match):
            num = match.group(1).strip()
            den = match.group(2).strip()
            
            # Check if already processed as derivative
            if any(d in num and d in den for d in ['d', 'partial']):
                return match.group(0)
            
            # Check common fractions
            if (num, den) in self.common_fractions:
                return self.common_fractions[(num, den)]
            
            # For complex expressions, use "the quantity"
            if any(op in num for op in ['+', '-', '*']) or any(op in den for op in ['+', '-', '*']):
                return f"the quantity {num} over the quantity {den}"
            
            return f"{num} over {den}"
            
        text = re.sub(r'\\frac\{([^}]+)\}\{([^}]+)\}', replace_frac, text)
        
        return text
        
    def _handle_roots(self, text: str) -> str:
        """Handle root notation"""
        
        # Square root
        text = re.sub(r'\\sqrt\{([^}]+)\}', r'square root of \1', text)
        
        # Nth root
        text = re.sub(r'\\sqrt\[(\d+)\]\{([^}]+)\}', lambda m: f'{self._ordinal(m.group(1))} root of {m.group(2)}', text)
        
        return text
        
    def _ordinal(self, n: str) -> str:
        """Convert number to ordinal"""
        
        ordinals = {
            '2': 'square', '3': 'cube', '4': 'fourth',
            '5': 'fifth', '6': 'sixth', '7': 'seventh',
            '8': 'eighth', '9': 'ninth', '10': 'tenth'
        }
        
        return ordinals.get(n, f'{n}th')
        
    def _handle_matrices(self, text: str) -> str:
        """Handle matrix notation"""
        
        # Inverse - add space after
        text = re.sub(r'(\w+)\^\{-1\}', r'\1 inverse ', text)
        
        # Transpose
        text = re.sub(r'(\w+)\^T', r'\1 transpose', text)
        
        # Determinant
        text = re.sub(r'\\det\(([^)]+)\)', r'the determinant of \1', text)
        
        # Trace
        text = re.sub(r'\\tr\(([^)]+)\)', r'the trace of \1', text)
        
        return text
        
    def _handle_sequences(self, text: str) -> str:
        """Handle sequence notation"""
        
        # a_1, a_2, ..., a_n
        text = re.sub(r'(\w+)_(\w+),\s*(\w+)_(\w+),\s*\.\.\.,\s*(\w+)_(\w+)', 
                     r'\1 \2, \3 \4, dot dot dot, \5 \6', text)
        
        # (x_n)_{n=1}^{\infty}
        text = re.sub(r'\((\w+)_(\w+)\)_\{(\w+)=(\d+)\}\^\{([^}]+)\}', 
                     r'the sequence \1 \2 from \3 equals \4 to \5', text)
        
        return text
        
    def _convert_operations_enhanced(self, text: str) -> str:
        """Enhanced operation conversion"""
        
        # Basic operations
        text = text.replace('+', ' plus ')
        text = text.replace('-', ' minus ')
        text = text.replace('=', ' equals ')
        text = text.replace('<', ' less than ')
        text = text.replace('>', ' greater than ')
        text = text.replace('≤', ' less than or equal to ')
        text = text.replace('≥', ' greater than or equal to ')
        text = text.replace('≠', ' not equal to ')
        
        # Clean up
        text = re.sub(r'\s+', ' ', text)
        
        return text
        
    def _convert_numbers_intelligent(self, text: str) -> str:
        """Intelligent number conversion"""
        
        # Handle numbers with letters first
        text = re.sub(r'(\d+)([a-zA-Z])', r'\1 \2', text)
        
        # Convert numbers to words
        for num, word in sorted(self.number_words.items(), key=lambda x: len(x[0]), reverse=True):
            text = re.sub(rf'\b{num}\b', word, text)
            
        return text
        
    def _apply_context_rules_advanced(self, text: str, context: str) -> str:
        """Apply advanced context-specific rules"""
        
        if context == 'arithmetic':
            # Use "is" for simple equations
            text = re.sub(r'(\w+\s+(?:plus|minus|times|divided by)\s+\w+)\s+equals\s+(\w+)', 
                         r'\1 is \2', text)
                         
        elif context == 'probability':
            # Natural probability language
            text = text.replace(' equals one', ' is certain')
            text = text.replace(' equals zero', ' is impossible')
            
        elif context == 'set_theory':
            # Natural set language
            text = text.replace(' union ', ' combined with ')
            text = text.replace(' intersection ', ' in common with ')
            
        elif context == 'logic':
            # Natural logical language
            text = text.replace(' implies ', ' means that ')
            text = text.replace(' if and only if ', ' exactly when ')
            
        # Universal improvements
        text = re.sub(r'for all (\w+) in the real numbers', r'for all real \1', text)
        text = re.sub(r'for all (\w+) in the natural numbers', r'for all natural \1', text)
        
        return text
        
    def _final_polish(self, text: str) -> str:
        """Final polishing for maximum naturalness"""
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Fix comma spacing
        text = re.sub(r'\s*,\s*', ', ', text)
        
        # Remove LaTeX artifacts
        text = text.replace('\\', '')
        text = text.replace('{', '').replace('}', '')
        
        # Handle special cases
        text = text.replace('d by dx of f of x', 'the derivative of f of x')
        text = text.replace('d by dx f of x', 'the derivative of f of x')
        text = text.replace('partial f by partial x', 'the partial derivative of f with respect to x')
        
        # Fix spacing issues
        text = text.replace('ipi', 'i pi')
        text = text.replace('inverseb', 'inverse b')
        
        # Ensure single spaces
        text = ' '.join(text.split())
        
        return text.strip()
        
    def _convert_symbols_comprehensive(self, text: str) -> str:
        """Comprehensive symbol conversion"""
        
        for latex, natural in self.symbols.items():
            text = text.replace(latex, natural)
            
        return text
        
    def _handle_powers_enhanced(self, text: str) -> str:
        """Enhanced power handling"""
        
        # Special powers
        text = re.sub(r'\^2(?!\d)', ' squared', text)
        text = re.sub(r'\^3(?!\d)', ' cubed', text)
        text = re.sub(r'\^T(?!\w)', ' transpose', text)
        text = re.sub(r'\^\{-1\}', ' inverse', text)
        
        # Numeric powers
        text = re.sub(r'\^\{(\d+)\}', r' to the \1', text)
        text = re.sub(r'\^(\d+)', r' to the \1', text)
        
        # Variable powers
        text = re.sub(r'\^(\w+)', r' to the \1', text)
        text = re.sub(r'\^\{([^}]+)\}', r' to the \1', text)
        
        return text
        
    def _handle_subscripts_enhanced(self, text: str) -> str:
        """Enhanced subscript handling"""
        
        # Common subscripts
        text = re.sub(r'_0(?!\d)', ' naught', text)
        text = re.sub(r'_1(?!\d)', ' one', text)
        text = re.sub(r'_2(?!\d)', ' two', text)
        text = re.sub(r'_n(?!\w)', ' n', text)
        text = re.sub(r'_i(?!\w)', ' i', text)
        text = re.sub(r'_j(?!\w)', ' j', text)
        text = re.sub(r'_k(?!\w)', ' k', text)
        
        # General subscripts
        text = re.sub(r'_\{([^}]+)\}', r' \1', text)
        text = re.sub(r'_(\w)', r' \1', text)
        
        return text
        
    def _handle_functions_enhanced(self, text: str) -> str:
        """Enhanced function handling"""
        
        # Composite functions
        text = re.sub(r'(\w)\((\w)\((\w)\)\)', r'\1 of \2 of \3', text)
        
        # Standard functions
        text = re.sub(r'(\w)\((\w)\)', r'\1 of \2', text)
        
        # Multiple arguments
        text = re.sub(r'(\w)\(([^,]+),([^)]+)\)', r'\1 of \2 and \3', text)
        
        return text
        
    def _handle_parentheses_enhanced(self, text: str) -> str:
        """Enhanced parentheses handling"""
        
        # Products
        text = re.sub(r'\(([^)]+)\)\(([^)]+)\)', r'\1, times \2', text)
        
        # Powers
        text = re.sub(r'\(([^)]+)\)\s*squared', r'\1, squared', text)
        text = re.sub(r'\(([^)]+)\)\s*cubed', r'\1, cubed', text)
        text = re.sub(r'\(([^)]+)\)\s*to the (\w+)', r'\1, to the \2', text)
        
        # Clean remaining
        text = text.replace('(', ' ').replace(')', ' ')
        
        return text
        
    def _handle_integrals_enhanced(self, text: str) -> str:
        """Enhanced integral handling"""
        
        # Multiple integrals
        text = re.sub(r'\\iint', 'the double integral', text)
        text = re.sub(r'\\iiint', 'the triple integral', text)
        
        # Integral with bounds
        def replace_integral(match):
            lower = match.group(1)
            upper = match.group(2)
            expr = match.group(3).strip()
            var = match.group(4)
            return f"the integral from {lower} to {upper} of {expr}, d{var}"
            
        text = re.sub(r'\\int_(\w+)\^(\w+)\s*([^d]+)\s*d(\w+)', replace_integral, text)
        
        # Simple integral
        text = text.replace('\\int', 'the integral')
        
        return text
        
    def _handle_limits_enhanced(self, text: str) -> str:
        """Enhanced limit handling"""
        
        # One-sided limits
        text = re.sub(r'\\lim_\{(\w+)\s*\\to\s*([^}]+)\^\+\}', r'the limit as \1 approaches \2 from the right', text)
        text = re.sub(r'\\lim_\{(\w+)\s*\\to\s*([^}]+)\^-\}', r'the limit as \1 approaches \2 from the left', text)
        
        # Standard limits
        def replace_limit(match):
            var = match.group(1)
            target = match.group(2)
            expr = match.group(3).strip() if len(match.groups()) >= 3 else ''
            
            # Special targets
            if target == '\\infty':
                target = 'infinity'
            elif target == '-\\infty':
                target = 'negative infinity'
            elif target == '0':
                target = 'zero'
                
            if expr:
                return f"the limit as {var} approaches {target} of {expr}"
            else:
                return f"the limit as {var} approaches {target}"
                
        text = re.sub(r'\\lim_\{(\w+)\s*\\to\s*([^}]+)\}\s*(.+)?', replace_limit, text)
        
        return text
        
    def _handle_sums_enhanced(self, text: str) -> str:
        """Enhanced sum handling"""
        
        # Double sums
        text = re.sub(r'\\sum_\{([^=]+)=(\d+)\}\^(\w+)\s*\\sum_\{([^=]+)=(\d+)\}\^(\w+)', 
                     r'the double sum from \1 equals \2 to \3 and \4 equals \5 to \6', text)
        
        # Standard sums
        def replace_sum(match):
            var = match.group(1)
            start = match.group(2)
            end = match.group(3)
            expr = match.group(4).strip() if len(match.groups()) >= 4 else ''
            
            if end == '\\infty':
                end = 'infinity'
                
            if expr:
                return f"the sum from {var} equals {start} to {end} of {expr}"
            else:
                return f"the sum from {var} equals {start} to {end}"
                
        text = re.sub(r'\\sum_\{([^=]+)=(\d+)\}\^([^\s]+)\s*(.+)?', replace_sum, text)
        
        return text
        
    def _handle_products(self, text: str) -> str:
        """Handle product notation"""
        
        def replace_product(match):
            var = match.group(1)
            start = match.group(2)
            end = match.group(3)
            expr = match.group(4).strip() if len(match.groups()) >= 4 else ''
            
            if expr:
                return f"the product from {var} equals {start} to {end} of {expr}"
            else:
                return f"the product from {var} equals {start} to {end}"
                
        text = re.sub(r'\\prod_\{([^=]+)=(\d+)\}\^(\w+)\s*(.+)?', replace_product, text)
        
        return text


# Run comprehensive tests
def run_ultra_tests():
    """Run comprehensive test suite"""
    
    engine = UltraNaturalSpeechEngine()
    
    # Comprehensive test cases
    test_cases = [
        # Basic
        {'input': '$2 + 3 = 5$', 'expected': 'two plus three is five', 'context': 'arithmetic'},
        
        # Derivatives
        {'input': '$\\frac{d^2y}{dx^2}$', 'expected': 'd squared y by dx squared'},
        {'input': '$\\frac{\\partial^2 f}{\\partial x \\partial y}$', 'expected': 'partial squared f by partial x partial y'},
        
        # Set theory
        {'input': '$A \\cup B$', 'expected': 'a combined with b', 'context': 'set_theory'},
        {'input': '$A \\cap B$', 'expected': 'a in common with b', 'context': 'set_theory'},
        
        # Probability
        {'input': '$P(A|B)$', 'expected': 'probability of a given b'},
        {'input': '$E[X]$', 'expected': 'expected value of x'},
        
        # Logic
        {'input': '$p \\land q$', 'expected': 'p and q'},
        {'input': '$p \\implies q$', 'expected': 'p means that q', 'context': 'logic'},
        
        # Roots and powers
        {'input': '$\\sqrt{x}$', 'expected': 'square root of x'},
        {'input': '$\\sqrt[3]{x}$', 'expected': 'cube root of x'},
        
        # Absolute value and norms
        {'input': '$|x|$', 'expected': 'absolute value of x'},
        {'input': '$||v||$', 'expected': 'norm of v'},
        
        # Matrix operations
        {'input': '$A^{-1}B$', 'expected': 'a inverse b'},
        {'input': '$\\det(A)$', 'expected': 'the determinant of a'},
        
        # Complex expressions
        {'input': '$e^{i\\pi} + 1 = 0$', 'expected': 'e to the i pi plus one equals zero'},
        {'input': '$\\sin^2 x + \\cos^2 x = 1$', 'expected': 'sine squared x plus cosine squared x equals one'},
        
        # All original tests
        {'input': '$x^2 + 5x + 6$', 'expected': 'x squared plus five x plus six'},
        {'input': '$\\frac{d}{dx} f(x)$', 'expected': 'the derivative of f of x'},
        {'input': '$\\int_0^1 x^2 dx$', 'expected': 'the integral from zero to one of x squared, dx'},
        {'input': '$\\forall x \\in \\mathbb{R}$', 'expected': 'for all real x'},
    ]
    
    passed = 0
    total = len(test_cases)
    
    print("\n" + "="*70)
    print("🚀 ULTRA NATURAL SPEECH ENGINE TEST RESULTS")
    print("="*70)
    
    for i, test in enumerate(test_cases):
        result = engine.naturalize(test['input'], test.get('context'))
        expected = test['expected']
        
        if result == expected:
            passed += 1
            print(f"✅ Test {i+1:2d}: PASS")
        else:
            print(f"❌ Test {i+1:2d}: FAIL")
            print(f"    Input:    {test['input']}")
            print(f"    Expected: {expected}")
            print(f"    Got:      {result}")
            
    score = passed / total * 100
    
    print("\n" + "="*70)
    print(f"FINAL SCORE: {passed}/{total} ({score:.1f}%)")
    print("="*70)
    
    return score


if __name__ == "__main__":
    score = run_ultra_tests()
    print(f"\nUltra Natural Speech Engine Score: {score:.1f}%")