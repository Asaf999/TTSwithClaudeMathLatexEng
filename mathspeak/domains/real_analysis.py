#!/usr/bin/env python3
"""
Real Analysis Domain Processor for Mathematical Text-to-Speech
============================================================

Complete processor for real analysis notation including:
- Limits and continuity (epsilon-delta definitions)
- Differentiation and integration
- Sequences and series convergence
- Metric space topology
- Function spaces and uniform convergence
- Measure theory connections

This processor handles ALL real analysis notation with professor-quality pronunciation.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Real Analysis Context Types
# ===========================

class RealAnalysisContext(Enum):
    """Specific real analysis contexts for fine-grained processing"""
    LIMITS = "limits"
    CONTINUITY = "continuity"
    DIFFERENTIATION = "differentiation"
    INTEGRATION = "integration"
    SEQUENCES = "sequences"
    SERIES = "series"
    FUNCTION_SPACES = "function_spaces"
    GENERAL = "general"

@dataclass
class RealAnalysisTerm:
    """Represents a real analysis term with pronunciation hints"""
    latex: str
    spoken: str
    context: RealAnalysisContext
    emphasis: bool = False
    add_article: bool = True

# ===========================
# Comprehensive Real Analysis Vocabulary
# ===========================

class RealAnalysisVocabulary:
    """Complete real analysis vocabulary with natural pronunciations"""
    
    def __init__(self):
        self.terms = self._build_vocabulary()
        self.patterns = self._build_patterns()
        self.compiled_patterns = self._compile_patterns()
    
    def _escape_for_both_backslashes(self, pattern: str) -> str:
        """Convert a pattern to match both single and double backslash versions"""
        import re as regex
        
        def replace_command(match):
            cmd = match.group(0)
            if cmd.startswith(r'\\'):
                cmd_name = cmd[2:]
            else:
                return cmd
            
            return r'(?:\\\\|\\)' + regex.escape(cmd_name)
        
        pattern = regex.sub(r'\\\\[a-zA-Z]+', replace_command, pattern)
        return pattern
        
    def _build_vocabulary(self) -> Dict[str, Union[str, Callable]]:
        """Build comprehensive real analysis vocabulary"""
        vocab = {}
        
        # ===== BASIC REAL NUMBERS AND SETS =====
        
        vocab.update({
            r'\\mathbb{R}': 'the real numbers',
            r'\\mathbb{R}^\\+': 'the positive real numbers',
            r'\\mathbb{R}^\\-': 'the negative real numbers',
            r'\\mathbb{R}_+': 'the non-negative real numbers',
            r'\\mathbb{R}_{++}': 'the strictly positive real numbers',
            r'\\mathbb{R}^n': 'n-dimensional real space',
            r'\\mathbb{R}^([0-9]+)': lambda m: f"{self._number_name(m.group(1))}-dimensional real space",
            r'\\mathbb{Q}': 'the rational numbers',
            r'\\mathbb{N}': 'the natural numbers',
            r'\\mathbb{Z}': 'the integers',
            r'\\mathbb{C}': 'the complex numbers',
            r'\\overline{\\mathbb{R}}': 'the extended real numbers',
            r'\\mathbb{R} \\cup \\{\\pm\\infty\\}': 'the extended real line',
        })
        
        # ===== LIMITS AND EPSILON-DELTA =====
        
        vocab.update({
            r'\\lim_{([^}]+)} ([^\\s]+)': lambda m: f"the limit as {self._process_nested(m.group(1))} of {self._process_nested(m.group(2))}",
            r'\\lim_\\{([^}]+)\\} ([^\\s]+)': lambda m: f"the limit as {self._process_nested(m.group(1))} of {self._process_nested(m.group(2))}",
            r'\\lim ([^\\s]+)': lambda m: f"the limit of {self._process_nested(m.group(1))}",
            r'\\limsup_{([^}]+)} ([^\\s]+)': lambda m: f"the limit superior as {self._process_nested(m.group(1))} of {self._process_nested(m.group(2))}",
            r'\\liminf_{([^}]+)} ([^\\s]+)': lambda m: f"the limit inferior as {self._process_nested(m.group(1))} of {self._process_nested(m.group(2))}",
            r'\\overline{\\lim}': 'limit superior',
            r'\\underline{\\lim}': 'limit inferior',
            r'\\epsilon': 'epsilon',
            r'\\varepsilon': 'epsilon',
            r'\\delta': 'delta',
            r'\\forall \\epsilon > 0': 'for all epsilon greater than zero',
            r'\\exists \\delta > 0': 'there exists delta greater than zero',
            r'\\forall \\epsilon > 0 \\, \\exists \\delta > 0': 'for all epsilon greater than zero there exists delta greater than zero',
            r'0 < \\|x - a\\| < \\delta': 'zero less than the absolute value of x minus a less than delta',
            r'\\|f\\(x\\) - L\\| < \\epsilon': 'the absolute value of f of x minus L is less than epsilon',
        })
        
        # ===== CONTINUITY =====
        
        vocab.update({
            r'f \\text{ is continuous at } a': 'f is continuous at a',
            r'f \\in C\\(([^)]+)\\)': lambda m: f"f is continuous on {self._process_nested(m.group(1))}",
            r'C\\(([^)]+)\\)': lambda m: f"the space of continuous functions on {self._process_nested(m.group(1))}",
            r'C^0\\(([^)]+)\\)': lambda m: f"the space of continuous functions on {self._process_nested(m.group(1))}",
            r'C^k\\(([^)]+)\\)': lambda m: f"the space of k times continuously differentiable functions on {self._process_nested(m.group(1))}",
            r'C^([0-9]+)\\(([^)]+)\\)': lambda m: f"the space of {self._number_name(m.group(1))} times continuously differentiable functions on {self._process_nested(m.group(2))}",
            r'C^\\infty\\(([^)]+)\\)': lambda m: f"the space of smooth functions on {self._process_nested(m.group(1))}",
            r'\\text{uniformly continuous}': 'uniformly continuous',
            r'\\text{Lipschitz continuous}': 'Lipschitz continuous',
            r'\\text{Holder continuous}': 'Holder continuous',
        })
        
        # ===== DIFFERENTIATION =====
        
        vocab.update({
            r"f'\\(([^)]+)\\)": lambda m: f"f prime of {self._process_nested(m.group(1))}",
            r"f''\\(([^)]+)\\)": lambda m: f"f double prime of {self._process_nested(m.group(1))}",
            r"f'''\\(([^)]+)\\)": lambda m: f"f triple prime of {self._process_nested(m.group(1))}",
            r"f^{\\(([0-9]+)\\)}\\(([^)]+)\\)": lambda m: f"the {self._ordinal(m.group(1))} derivative of f at {self._process_nested(m.group(2))}",
            r"\\frac{d}{dx}": 'the derivative with respect to x',
            r"\\frac{d}{dt}": 'the derivative with respect to t',
            r"\\frac{d([^}]+)}{d([^}]+)}": lambda m: f"the derivative of {self._process_nested(m.group(1))} with respect to {self._process_nested(m.group(2))}",
            r"\\frac{d^2}{dx^2}": 'the second derivative with respect to x',
            r"\\frac{d^([0-9]+)}{dx^\\1}": lambda m: f"the {self._ordinal(m.group(1))} derivative with respect to x",
            r"\\frac{\\partial}{\\partial x}": 'the partial derivative with respect to x',
            r"\\frac{\\partial ([^}]+)}{\\partial ([^}]+)}": lambda m: f"the partial derivative of {self._process_nested(m.group(1))} with respect to {self._process_nested(m.group(2))}",
            r"\\nabla f": 'the gradient of f',
            r"\\nabla": 'nabla',
            r"\\text{grad} f": 'the gradient of f',
        })
        
        # ===== INTEGRATION =====
        
        vocab.update({
            r'\\int ([^\\s]+) dx': lambda m: f"the integral of {self._process_nested(m.group(1))} with respect to x",
            r'\\int ([^\\s]+) dt': lambda m: f"the integral of {self._process_nested(m.group(1))} with respect to t",
            r'\\int ([^\\s]+) d([a-z])': lambda m: f"the integral of {self._process_nested(m.group(1))} with respect to {m.group(2)}",
            r'\\int_a^b ([^\\s]+) dx': lambda m: f"the integral from a to b of {self._process_nested(m.group(1))} with respect to x",
            r'\\int_([^\\s]+)^([^\\s]+) ([^\\s]+) d([a-z])': lambda m: f"the integral from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))} of {self._process_nested(m.group(3))} with respect to {m.group(4)}",
            r'\\int_([^\\s]+) ([^\\s]+) d([a-z])': lambda m: f"the integral over {self._process_nested(m.group(1))} of {self._process_nested(m.group(2))} with respect to {m.group(3)}",
            r'\\iint': 'the double integral',
            r'\\iiint': 'the triple integral',
            r'\\oint': 'the contour integral',
            r'F\'\\(x\\) = f\\(x\\)': 'F prime of x equals f of x',
            r'\\int f\\(x\\) dx = F\\(x\\) \\+ C': 'the integral of f of x d x equals F of x plus C',
        })
        
        # ===== SEQUENCES AND SERIES =====
        
        vocab.update({
            r'\\{([a-z])_n\\}': lambda m: f"the sequence {m.group(1)} sub n",
            r'\\{([a-z])_n\\}_{n=1}^\\infty': lambda m: f"the sequence {m.group(1)} sub n from n equals 1 to infinity",
            r'\\{([a-z])_n\\}_{n=([0-9]+)}^\\infty': lambda m: f"the sequence {m.group(1)} sub n from n equals {m.group(2)} to infinity",
            r'([a-z])_n \\to ([a-z])': lambda m: f"{m.group(1)} sub n converges to {m.group(2)}",
            r'([a-z])_n \\rightarrow ([a-z])': lambda m: f"{m.group(1)} sub n converges to {m.group(2)}",
            r'\\sum_{n=1}^\\infty ([^\\s]+)': lambda m: f"the sum from n equals 1 to infinity of {self._process_nested(m.group(1))}",
            r'\\sum_{n=([0-9]+)}^\\infty ([^\\s]+)': lambda m: f"the sum from n equals {m.group(1)} to infinity of {self._process_nested(m.group(2))}",
            r'\\sum_{k=1}^n ([^\\s]+)': lambda m: f"the sum from k equals 1 to n of {self._process_nested(m.group(1))}",
            r'\\prod_{n=1}^\\infty ([^\\s]+)': lambda m: f"the product from n equals 1 to infinity of {self._process_nested(m.group(1))}",
            r'\\text{converges}': 'converges',
            r'\\text{diverges}': 'diverges',
            r'\\text{absolutely convergent}': 'absolutely convergent',
            r'\\text{conditionally convergent}': 'conditionally convergent',
            r'\\text{Cauchy sequence}': 'Cauchy sequence',
            r'S_n = \\sum_{k=1}^n a_k': 'S sub n equals the sum from k equals 1 to n of a sub k',
        })
        
        # ===== FUNCTION SPACES AND NORMS =====
        
        vocab.update({
            r'L^p\\(([^)]+)\\)': lambda m: f"L p space on {self._process_nested(m.group(1))}",
            r'L^([0-9]+)\\(([^)]+)\\)': lambda m: f"L {m.group(1)} space on {self._process_nested(m.group(2))}",
            r'L^\\infty\\(([^)]+)\\)': lambda m: f"L infinity space on {self._process_nested(m.group(1))}",
            r'\\|f\\|_p': 'the L p norm of f',
            r'\\|f\\|_([0-9]+)': lambda m: f"the L {m.group(1)} norm of f",
            r'\\|f\\|_\\infty': 'the L infinity norm of f',
            r'\\|f\\|_{\\infty}': 'the supremum norm of f',
            # Fixed to prevent infinite recursion
            r'\\|([^|]+)\\|': lambda m: f"the norm of {m.group(1)}" if '|' not in m.group(1) else f"the norm of {m.group(1)}",
            r'\\sup_{x \\in ([^}]+)} \\|f\\(x\\)\\|': lambda m: f"the supremum over x in {self._process_nested(m.group(1))} of the norm of f of x",
            r'\\text{esssup}': 'essential supremum',
            r'\\text{ess sup}': 'essential supremum',
        })
        
        # ===== METRIC SPACES =====
        
        vocab.update({
            r'd\\(([^,]+),([^)]+)\\)': lambda m: f"the distance from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))}",
            r'B\\(([^,]+),([^)]+)\\)': lambda m: f"the open ball centered at {self._process_nested(m.group(1))} with radius {self._process_nested(m.group(2))}",
            r'\\overline{B}\\(([^,]+),([^)]+)\\)': lambda m: f"the closed ball centered at {self._process_nested(m.group(1))} with radius {self._process_nested(m.group(2))}",
            r'\\text{diam}\\(([^)]+)\\)': lambda m: f"the diameter of {self._process_nested(m.group(1))}",
            r'\\text{dist}\\(([^,]+),([^)]+)\\)': lambda m: f"the distance from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))}",
            r'\\text{complete}': 'complete',
            r'\\text{Banach space}': 'Banach space',
            r'\\text{Hilbert space}': 'Hilbert space',
        })
        
        # ===== INEQUALITIES AND ESTIMATES =====
        
        vocab.update({
            r'\\leq': 'is less than or equal to',
            r'\\geq': 'is greater than or equal to',
            r'\\ll': 'is much less than',
            r'\\gg': 'is much greater than',
            r'\\sim': 'is asymptotic to',
            r'\\asymp': 'is asymptotically equal to',
            r'\\lesssim': 'is less than or comparable to',
            r'\\gtrsim': 'is greater than or comparable to',
            r'O\\(([^)]+)\\)': lambda m: f"big O of {self._process_nested(m.group(1))}",
            r'o\\(([^)]+)\\)': lambda m: f"little o of {self._process_nested(m.group(1))}",
            r'\\Theta\\(([^)]+)\\)': lambda m: f"theta of {self._process_nested(m.group(1))}",
            r'\\Omega\\(([^)]+)\\)': lambda m: f"omega of {self._process_nested(m.group(1))}",
        })
        
        # ===== SPECIAL FUNCTIONS =====
        
        vocab.update({
            r'\\exp\\(([^)]+)\\)': lambda m: f"the exponential of {self._process_nested(m.group(1))}",
            r'\\log\\(([^)]+)\\)': lambda m: f"the logarithm of {self._process_nested(m.group(1))}",
            r'\\ln\\(([^)]+)\\)': lambda m: f"the natural logarithm of {self._process_nested(m.group(1))}",
            r'\\sin\\(([^)]+)\\)': lambda m: f"the sine of {self._process_nested(m.group(1))}",
            r'\\cos\\(([^)]+)\\)': lambda m: f"the cosine of {self._process_nested(m.group(1))}",
            r'\\tan\\(([^)]+)\\)': lambda m: f"the tangent of {self._process_nested(m.group(1))}",
            r'\\arcsin\\(([^)]+)\\)': lambda m: f"the arcsine of {self._process_nested(m.group(1))}",
            r'\\arccos\\(([^)]+)\\)': lambda m: f"the arccosine of {self._process_nested(m.group(1))}",
            r'\\arctan\\(([^)]+)\\)': lambda m: f"the arctangent of {self._process_nested(m.group(1))}",
            r'\\sinh\\(([^)]+)\\)': lambda m: f"the hyperbolic sine of {self._process_nested(m.group(1))}",
            r'\\cosh\\(([^)]+)\\)': lambda m: f"the hyperbolic cosine of {self._process_nested(m.group(1))}",
            r'\\tanh\\(([^)]+)\\)': lambda m: f"the hyperbolic tangent of {self._process_nested(m.group(1))}",
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements"""
        patterns = [
            # Epsilon-delta definitions
            (r'\\forall \\epsilon > 0 \\, \\exists \\delta > 0 \\text{ such that } 0 < \\|x - a\\| < \\delta \\Rightarrow \\|f\\(x\\) - L\\| < \\epsilon',
             'for all epsilon greater than zero there exists delta greater than zero such that if zero is less than the absolute value of x minus a which is less than delta then the absolute value of f of x minus L is less than epsilon'),
            
            # Uniform continuity
            (r'\\forall \\epsilon > 0 \\, \\exists \\delta > 0 \\text{ such that } \\|x - y\\| < \\delta \\Rightarrow \\|f\\(x\\) - f\\(y\\)\\| < \\epsilon',
             'for all epsilon greater than zero there exists delta greater than zero such that if the absolute value of x minus y is less than delta then the absolute value of f of x minus f of y is less than epsilon'),
            
            # Cauchy sequences
            (r'\\forall \\epsilon > 0 \\, \\exists N \\in \\mathbb{N} \\text{ such that } m, n > N \\Rightarrow \\|([a-z])_m - ([a-z])_n\\| < \\epsilon',
             lambda m: f'for all epsilon greater than zero there exists N in the natural numbers such that if m and n are greater than N then the absolute value of {m.group(1)} sub m minus {m.group(2)} sub n is less than epsilon'),
            
            # Convergence
            (r'([a-z])_n \\to ([a-z]) \\text{ as } n \\to \\infty',
             lambda m: f'{m.group(1)} sub n converges to {m.group(2)} as n approaches infinity'),
            (r'\\lim_{n \\to \\infty} ([a-z])_n = ([a-z])',
             lambda m: f'the limit as n approaches infinity of {m.group(1)} sub n equals {m.group(2)}'),
            
            # Series convergence tests
            (r'\\text{ratio test}', 'the ratio test'),
            (r'\\text{root test}', 'the root test'),
            (r'\\text{comparison test}', 'the comparison test'),
            (r'\\text{integral test}', 'the integral test'),
            (r'\\text{alternating series test}', 'the alternating series test'),
            
            # Fundamental theorems
            (r'\\text{Fundamental Theorem of Calculus}', 'the Fundamental Theorem of Calculus'),
            (r'\\text{Mean Value Theorem}', 'the Mean Value Theorem'),
            (r'\\text{Intermediate Value Theorem}', 'the Intermediate Value Theorem'),
            (r'\\text{Extreme Value Theorem}', 'the Extreme Value Theorem'),
            (r'\\text{Bolzano-Weierstrass Theorem}', 'the Bolzano-Weierstrass Theorem'),
            (r'\\text{Heine-Borel Theorem}', 'the Heine-Borel Theorem'),
            
            # Function properties
            (r'f \\text{ is bounded}', 'f is bounded'),
            (r'f \\text{ is unbounded}', 'f is unbounded'),
            (r'f \\text{ is monotonic}', 'f is monotonic'),
            (r'f \\text{ is increasing}', 'f is increasing'),
            (r'f \\text{ is decreasing}', 'f is decreasing'),
            (r'f \\text{ is strictly increasing}', 'f is strictly increasing'),
            (r'f \\text{ is strictly decreasing}', 'f is strictly decreasing'),
            
            # Supremum and infimum
            (r'\\sup ([A-Z])', lambda m: f'the supremum of {m.group(1)}'),
            (r'\\inf ([A-Z])', lambda m: f'the infimum of {m.group(1)}'),
            (r'\\max ([A-Z])', lambda m: f'the maximum of {m.group(1)}'),
            (r'\\min ([A-Z])', lambda m: f'the minimum of {m.group(1)}'),
            
            # Compactness
            (r'([A-Z]) \\text{ is compact}', lambda m: f'{m.group(1)} is compact'),
            (r'([A-Z]) \\text{ is relatively compact}', lambda m: f'{m.group(1)} is relatively compact'),
            (r'([A-Z]) \\text{ is precompact}', lambda m: f'{m.group(1)} is precompact'),
        ]
        
        return patterns
    
    def _compile_patterns(self) -> List[Tuple[re.Pattern, Union[str, Callable]]]:
        """Compile patterns for efficiency"""
        compiled = []
        
        # Compile vocabulary patterns
        for pattern, replacement in self.terms.items():
            try:
                if r'\\' in pattern:
                    flexible_pattern = self._escape_for_both_backslashes(pattern)
                    compiled.append((re.compile(flexible_pattern), replacement))
                else:
                    compiled.append((re.compile(pattern), replacement))
            except re.error as e:
                logger.warning(f"Failed to compile pattern {pattern}: {e}")
        
        # Compile larger patterns
        for pattern, replacement in self.patterns:
            try:
                if r'\\' in pattern:
                    flexible_pattern = self._escape_for_both_backslashes(pattern)
                    compiled.append((re.compile(flexible_pattern), replacement))
                else:
                    compiled.append((re.compile(pattern), replacement))
            except re.error as e:
                logger.warning(f"Failed to compile pattern {pattern}: {e}")
        
        return compiled
    
    def _process_nested(self, content: str) -> str:
        """Process nested mathematical content"""
        if content is None:
            return ""
        content = content.strip()
        
        # Handle common nested patterns
        replacements = [
            (r'\\mathbb{R}', 'R'),
            (r'\\mathbb{C}', 'C'),
            (r'\\mathbb{Z}', 'Z'),
            (r'\\mathbb{Q}', 'Q'),
            (r'\\mathbb{N}', 'N'),
            (r'_([0-9])', r' sub \1'),
            (r'\^([0-9])', r' to the \1'),
            (r'\\infty', 'infinity'),
            (r'\\to', 'approaches'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    def _ordinal(self, n: str) -> str:
        """Convert number to ordinal"""
        ordinals = {
            '0': 'zeroth', '1': 'first', '2': 'second', '3': 'third',
            '4': 'fourth', '5': 'fifth', '6': 'sixth', '7': 'seventh',
            '8': 'eighth', '9': 'ninth', '10': 'tenth'
        }
        return ordinals.get(n, f"{n}-th")
    
    def _number_name(self, n: str) -> str:
        """Convert number to word"""
        numbers = {
            '1': 'one', '2': 'two', '3': 'three', '4': 'four',
            '5': 'five', '6': 'six', '7': 'seven', '8': 'eight',
            '9': 'nine', '10': 'ten'
        }
        return numbers.get(n, n)

# ===========================
# Main Real Analysis Processor
# ===========================

class RealAnalysisProcessor:
    """Main processor for real analysis domain"""
    
    def __init__(self):
        self.vocabulary = RealAnalysisVocabulary()
        self.context = RealAnalysisContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_definitions': True,
            'expand_epsilon_delta': True,
            'clarify_convergence': True,
        }
        
        logger.info("Real analysis processor initialized with complete vocabulary")
    
    def detect_subcontext(self, text: str) -> RealAnalysisContext:
        """Detect specific real analysis subcontext"""
        text_lower = text.lower()
        
        # Check for limits
        if any(term in text_lower for term in ['limit', 'epsilon', 'delta', 'approaches']):
            return RealAnalysisContext.LIMITS
        
        # Check for continuity
        if any(term in text_lower for term in ['continuous', 'continuity', 'uniform']):
            return RealAnalysisContext.CONTINUITY
        
        # Check for differentiation
        if any(term in text_lower for term in ['derivative', 'differentiate', 'gradient', 'partial']):
            return RealAnalysisContext.DIFFERENTIATION
        
        # Check for integration
        if any(term in text_lower for term in ['integral', 'integrate', 'antiderivative']):
            return RealAnalysisContext.INTEGRATION
        
        # Check for sequences
        if any(term in text_lower for term in ['sequence', 'converge', 'cauchy']):
            return RealAnalysisContext.SEQUENCES
        
        # Check for series
        if any(term in text_lower for term in ['series', 'sum', 'convergence']):
            return RealAnalysisContext.SERIES
        
        # Check for function spaces
        if any(term in text_lower for term in ['banach', 'hilbert', 'norm', 'metric']):
            return RealAnalysisContext.FUNCTION_SPACES
        
        return RealAnalysisContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process real analysis text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"Real analysis subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special real analysis rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process real analysis text"""
        # Normalize common variations
        normalizations = [
            (r'cont\.\s+', 'continuous '),
            (r'diff\.\s+', 'differentiable '),
            (r'integ\.\s+', 'integrable '),
            (r'conv\.\s+', 'convergent '),
            (r'unif\.\s+', 'uniform '),
            (r'a\.e\.', 'almost everywhere'),
            (r'w\.r\.t\.', 'with respect to'),
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply real analysis vocabulary replacements"""
        # Sort patterns by length to handle longer patterns first
        sorted_patterns = sorted(self.vocabulary.compiled_patterns, 
                               key=lambda x: len(x[0].pattern), 
                               reverse=True)
        
        for pattern, replacement in sorted_patterns:
            if callable(replacement):
                text = pattern.sub(replacement, text)
            else:
                text = pattern.sub(replacement, text)
        
        return text
    
    def _apply_special_rules(self, text: str) -> str:
        """Apply special real analysis-specific rules"""
        
        # Emphasize important theorems
        if self.special_rules['emphasize_definitions']:
            theorem_patterns = [
                (r'Fundamental Theorem of Calculus', 'the Fundamental Theorem of Calculus'),
                (r'Mean Value Theorem', 'the Mean Value Theorem'),
                (r'Intermediate Value Theorem', 'the Intermediate Value Theorem'),
                (r'Extreme Value Theorem', 'the Extreme Value Theorem'),
                (r'Bolzano-Weierstrass Theorem', 'the Bolzano-Weierstrass Theorem'),
                (r'Heine-Borel Theorem', 'the Heine-Borel Theorem'),
            ]
            
            for pattern, replacement in theorem_patterns:
                text = re.sub(pattern, f"{{EMPHASIS}}{replacement}{{/EMPHASIS}}", text, flags=re.IGNORECASE)
        
        # Expand epsilon-delta definitions when detected
        if self.special_rules['expand_epsilon_delta'] and self.context == RealAnalysisContext.LIMITS:
            # Add natural language explanations for complex epsilon-delta statements
            if 'epsilon' in text.lower() and 'delta' in text.lower():
                text = re.sub(r'(\\forall \\epsilon.*?\\epsilon)', 
                             r'\1 which means that the function gets arbitrarily close to the limit', 
                             text)
        
        return text
    
    def _postprocess(self, text: str) -> str:
        """Post-process for natural speech"""
        # Fix any double articles
        text = re.sub(r'\bthe\s+the\b', 'the', text)
        text = re.sub(r'\ba\s+a\b', 'a', text)
        text = re.sub(r'\ba\s+an\b', 'an', text)
        text = re.sub(r'\ban\s+a\b', 'a', text)
        
        # Improve flow
        text = re.sub(r'\s+,\s+', ', ', text)
        text = re.sub(r'\s+\.\s+', '. ', text)
        
        # Handle emphasis markers
        text = re.sub(r'\{\{EMPHASIS\}\}', '', text)
        text = re.sub(r'\{\{/EMPHASIS\}\}', '', text)
        
        return text
    
    def get_context_info(self) -> Dict[str, Any]:
        """Get information about current processing context"""
        return {
            'domain': 'real_analysis',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_real_analysis_processor():
    """Comprehensive test of real analysis processor"""
    processor = RealAnalysisProcessor()
    
    test_cases = [
        # Limits and epsilon-delta
        r"$\lim_{x \to a} f(x) = L$ means $\forall \epsilon > 0 \, \exists \delta > 0$ such that $0 < |x - a| < \delta \Rightarrow |f(x) - L| < \epsilon$",
        r"A function $f$ is continuous at $a$ if $\lim_{x \to a} f(x) = f(a)$",
        r"$f$ is uniformly continuous on $[a,b]$ if $\forall \epsilon > 0 \, \exists \delta > 0$ such that $|x - y| < \delta \Rightarrow |f(x) - f(y)| < \epsilon$",
        
        # Derivatives
        r"$f'(a) = \lim_{h \to 0} \frac{f(a+h) - f(a)}{h}$",
        r"By the Mean Value Theorem, $\exists c \in (a,b)$ such that $f'(c) = \frac{f(b) - f(a)}{b - a}$",
        r"$\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)$ by the chain rule",
        
        # Integrals
        r"The Fundamental Theorem of Calculus states that $\frac{d}{dx} \int_a^x f(t) dt = f(x)$",
        r"$\int_a^b f(x) dx = F(b) - F(a)$ where $F'(x) = f(x)$",
        r"$\int_0^{\infty} e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$",
        
        # Sequences and series
        r"A sequence $\{a_n\}$ is Cauchy if $\forall \epsilon > 0 \, \exists N$ such that $m,n > N \Rightarrow |a_m - a_n| < \epsilon$",
        r"The series $\sum_{n=1}^{\infty} a_n$ converges if the sequence of partial sums $S_n = \sum_{k=1}^n a_k$ converges",
        r"By the ratio test, if $\lim_{n \to \infty} \left|\frac{a_{n+1}}{a_n}\right| < 1$, then $\sum a_n$ converges absolutely",
        
        # Function spaces
        r"$f \in L^p(\mathbb{R})$ if $\|f\|_p = \left(\int_{\mathbb{R}} |f(x)|^p dx\right)^{1/p} < \infty$",
        r"The space $C([a,b])$ of continuous functions on $[a,b]$ is a Banach space with the supremum norm",
        r"$\|f\|_{\infty} = \text{esssup}_{x \in \mathbb{R}} |f(x)|$",
        
        # Metric spaces
        r"In a metric space $(X,d)$, the open ball $B(x,r) = \{y \in X : d(x,y) < r\}$",
        r"A metric space is complete if every Cauchy sequence converges",
    ]
    
    print("Testing Real Analysis Processor")
    print("=" * 70)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input:  {test}")
        result = processor.process(test)
        print(f"Output: {result}")
        print(f"Context: {processor.context.value}")
    
    print("\nContext Info:")
    print(processor.get_context_info())

if __name__ == "__main__":
    test_real_analysis_processor()