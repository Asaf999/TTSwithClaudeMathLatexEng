#!/usr/bin/env python3
"""
Complex Analysis Domain Processor for Mathematical Text-to-Speech
================================================================

Complete processor for complex analysis notation including:
- Complex numbers and operations
- Holomorphic and meromorphic functions
- Contour integration and residue theory
- Conformal mappings
- Special functions (exp, log, trig)
- Branch cuts and Riemann surfaces
- Power series and Laurent expansions

This processor provides natural pronunciation for all undergraduate and
graduate-level complex analysis.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Complex Analysis Contexts
# ===========================

class ComplexContext(Enum):
    """Specific complex analysis contexts"""
    BASIC_COMPLEX = "basic_complex"
    HOLOMORPHIC = "holomorphic"
    INTEGRATION = "integration"
    RESIDUES = "residues"
    CONFORMAL = "conformal"
    SPECIAL_FUNCTIONS = "special_functions"
    SERIES = "series"
    GENERAL = "general"

@dataclass
class ComplexTerm:
    """Represents a complex analysis term with pronunciation"""
    latex: str
    spoken: str
    context: ComplexContext
    emphasis: bool = False
    add_article: bool = True

# ===========================
# Complex Analysis Vocabulary
# ===========================

class ComplexAnalysisVocabulary:
    """Complete complex analysis vocabulary with natural pronunciations"""
    
    def __init__(self):
        self.terms = self._build_vocabulary()
        self.patterns = self._build_patterns()
        self.compiled_patterns = self._compile_patterns()
    
    def _build_vocabulary(self) -> Dict[str, Union[str, Callable]]:
        """Build comprehensive complex analysis vocabulary"""
        vocab = {}
        
        # ===== BASIC COMPLEX NUMBERS =====
        
        vocab.update({
            # Complex number notation
            r'z': 'z',
            r'w': 'w',
            r'\\mathbb{C}': 'the complex numbers',
            r'i': 'i',
            r'j': 'j',  # Engineering notation
            r'z = x + iy': 'z equals x plus i y',
            r'z = re^{i\\theta}': 'z equals r e to the i theta',
            r'z = r\\text{cis}\\theta': 'z equals r cis theta',
            
            # Real and imaginary parts
            r'\\text{Re}\\(z\\)': 'the real part of z',
            r'\\text{Im}\\(z\\)': 'the imaginary part of z',
            r'\\Re\\(z\\)': 'the real part of z',
            r'\\Im\\(z\\)': 'the imaginary part of z',
            r'\\text{Re}\\(([^)]+)\\)': lambda m: f"the real part of {self._process_nested(m.group(1))}",
            r'\\text{Im}\\(([^)]+)\\)': lambda m: f"the imaginary part of {self._process_nested(m.group(1))}",
            
            # Modulus and argument
            r'\|z\|': 'the modulus of z',
            r'\|([^|]+)\|': lambda m: f"the modulus of {self._process_nested(m.group(1))}",
            r'\\text{arg}\\(z\\)': 'the argument of z',
            r'\\text{Arg}\\(z\\)': 'the principal argument of z',
            r'\\arg\\(z\\)': 'the argument of z',
            r'\\text{arg}\\(([^)]+)\\)': lambda m: f"the argument of {self._process_nested(m.group(1))}",
            
            # Complex conjugate
            r'\\bar{z}': 'z bar',
            r'\\overline{z}': 'z conjugate',
            r'z^\\*': 'z star',
            r'\\bar{([^}]+)}': lambda m: f"{self._process_nested(m.group(1))} bar",
            r'\\overline{([^}]+)}': lambda m: f"the conjugate of {self._process_nested(m.group(1))}",
            
            # Complex operations
            r'z \\cdot w': 'z times w',
            r'z/w': 'z over w',
            r'z^n': 'z to the n',
            r'\\sqrt[n]{z}': 'the n-th root of z',
            r'1/z': 'one over z',
        })
        
        # ===== HOLOMORPHIC FUNCTIONS =====
        
        vocab.update({
            # Function types
            r'\\text{holomorphic}': 'holomorphic',
            r'\\text{analytic}': 'analytic',
            r'\\text{meromorphic}': 'meromorphic',
            r'\\text{entire}': 'entire',
            r'\\text{biholomorphic}': 'biholomorphic',
            r'\\text{conformal}': 'conformal',
            
            # Derivatives
            r'f\'\\(z\\)': 'f prime of z',
            r'f\'\'\\(z\\)': 'f double prime of z',
            r'f^{\\(n\\)}\\(z\\)': 'the n-th derivative of f at z',
            r'\\frac{df}{dz}': 'd f d z',
            r'\\frac{\\partial f}{\\partial z}': 'partial f partial z',
            r'\\frac{\\partial f}{\\partial \\bar{z}}': 'partial f partial z bar',
            
            # Cauchy-Riemann equations
            r'\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y}': 
                'partial u partial x equals partial v partial y',
            r'\\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}': 
                'partial u partial y equals negative partial v partial x',
            r'u_x = v_y': 'u sub x equals v sub y',
            r'u_y = -v_x': 'u sub y equals negative v sub x',
            
            # Holomorphic conditions
            r'f \\text{ is holomorphic on } D': 'f is holomorphic on D',
            r'f \\in H\\(D\\)': 'f is in the space of holomorphic functions on D',
            r'f: D \\to \\mathbb{C}': 'f from D to C',
        })
        
        # ===== CONTOUR INTEGRATION =====
        
        vocab.update({
            # Contour types
            r'\\gamma': 'gamma',
            r'\\Gamma': 'capital gamma',
            r'C': 'C',
            r'\\partial D': 'the boundary of D',
            r'\\text{simple closed curve}': 'simple closed curve',
            r'\\text{positively oriented}': 'positively oriented',
            r'\\text{counterclockwise}': 'counterclockwise',
            
            # Contour integrals
            r'\\oint_\\gamma f\\(z\\)\\,dz': 'the contour integral over gamma of f of z d z',
            r'\\oint_C f\\(z\\)\\,dz': 'the contour integral over C of f of z d z',
            r'\\int_\\gamma f\\(z\\)\\,dz': 'the integral along gamma of f of z d z',
            r'\\oint_{\\partial D} f\\(z\\)\\,dz': 'the contour integral over the boundary of D of f of z d z',
            r'\\oint_{\|z\|=r} f\\(z\\)\\,dz': 'the contour integral over the circle of radius r of f of z d z',
            
            # Path notation
            r'\\gamma: \[a,b\] \\to \\mathbb{C}': 'gamma from the interval a b to C',
            r'\\gamma\\(t\\) = z_0 + re^{it}': 'gamma of t equals z naught plus r e to the i t',
            r'\\text{parametrized by}': 'parametrized by',
        })
        
        # ===== RESIDUE THEORY =====
        
        vocab.update({
            # Residues
            r'\\text{Res}\\(f, z_0\\)': 'the residue of f at z naught',
            r'\\text{Res}\\(f, a\\)': 'the residue of f at a',
            r'\\text{Res}_{z=z_0} f\\(z\\)': 'the residue of f of z at z equals z naught',
            r'\\text{Res}\\(([^,]+), ([^)]+)\\)': 
                lambda m: f"the residue of {self._process_nested(m.group(1))} at {self._process_nested(m.group(2))}",
            
            # Poles and singularities
            r'\\text{simple pole}': 'simple pole',
            r'\\text{pole of order } n': 'pole of order n',
            r'\\text{essential singularity}': 'essential singularity',
            r'\\text{removable singularity}': 'removable singularity',
            r'\\text{isolated singularity}': 'isolated singularity',
            r'\\text{branch point}': 'branch point',
            r'\\text{branch cut}': 'branch cut',
            
            # Residue theorem
            r'2\\pi i \\sum \\text{Res}\\(f, z_k\\)': 'two pi i times the sum of the residues of f at z sub k',
            r'\\sum_{k=1}^n \\text{Res}\\(f, z_k\\)': 'the sum from k equals 1 to n of the residue of f at z sub k',
        })
        
        # ===== SPECIAL FUNCTIONS =====
        
        vocab.update({
            # Exponential and logarithm
            r'e^z': 'e to the z',
            r'\\exp\\(z\\)': 'exponential of z',
            r'\\log z': 'log z',
            r'\\ln z': 'natural log of z',
            r'\\text{Log} z': 'the principal logarithm of z',
            r'\\log\\(z\\)': 'log of z',
            r'\\text{Log}\\(z\\)': 'the principal logarithm of z',
            
            # Trigonometric functions
            r'\\sin z': 'sine z',
            r'\\cos z': 'cosine z',
            r'\\tan z': 'tangent z',
            r'\\sinh z': 'hyperbolic sine z',
            r'\\cosh z': 'hyperbolic cosine z',
            r'\\tanh z': 'hyperbolic tangent z',
            
            # Inverse functions
            r'\\sin^{-1} z': 'inverse sine of z',
            r'\\cos^{-1} z': 'inverse cosine of z',
            r'\\arcsin z': 'arc sine z',
            r'\\arccos z': 'arc cosine z',
            r'\\text{Arcsin} z': 'the principal arc sine of z',
            
            # Power functions
            r'z^\\alpha': 'z to the alpha',
            r'z^{1/n}': 'the n-th root of z',
            r'\\sqrt{z}': 'square root of z',
            r'(-1)^z': 'negative one to the z',
            
            # Special values
            r'e^{i\\pi}': 'e to the i pi',
            r'e^{2\\pi i}': 'e to the two pi i',
            r'e^{i\\pi/2}': 'e to the i pi over 2',
        })
        
        # ===== SERIES EXPANSIONS =====
        
        vocab.update({
            # Taylor series
            r'\\sum_{n=0}^\\infty a_n \\(z-z_0\\)^n': 
                'the sum from n equals 0 to infinity of a sub n times z minus z naught to the n',
            r'f\\(z\\) = \\sum_{n=0}^\\infty \\frac{f^{\\(n\\)}\\(z_0\\)}{n!}\\(z-z_0\\)^n':
                'f of z equals the Taylor series of f centered at z naught',
            
            # Laurent series
            r'\\sum_{n=-\\infty}^\\infty a_n \\(z-z_0\\)^n':
                'the sum from n equals negative infinity to infinity of a sub n times z minus z naught to the n',
            r'\\sum_{n=-\\infty}^{-1} a_n \\(z-z_0\\)^n':
                'the principal part of the Laurent series',
            r'\\sum_{n=0}^\\infty a_n \\(z-z_0\\)^n':
                'the regular part of the Laurent series',
            
            # Convergence
            r'R = \\frac{1}{\\limsup_{n\\to\\infty} \\sqrt[n]{\|a_n\|}}':
                'R equals one over the limit superior as n goes to infinity of the n-th root of the modulus of a sub n',
            r'\|z-z_0\| < R': 'the modulus of z minus z naught is less than R',
            r'\\text{radius of convergence}': 'radius of convergence',
            r'\\text{annulus of convergence}': 'annulus of convergence',
        })
        
        # ===== CONFORMAL MAPPINGS =====
        
        vocab.update({
            # Mapping types
            r'w = f\\(z\\)': 'w equals f of z',
            r'f: D \\to D\'': 'f maps D to D prime',
            r'\\text{M\\"obius transformation}': 'Möbius transformation',
            r'\\text{linear fractional transformation}': 'linear fractional transformation',
            r'f\\(z\\) = \\frac{az + b}{cz + d}': 'f of z equals a z plus b over c z plus d',
            
            # Mapping properties
            r'f\'\\(z\\) \\neq 0': 'f prime of z is not zero',
            r'\\text{angle-preserving}': 'angle-preserving',
            r'\\text{orientation-preserving}': 'orientation-preserving',
            r'\\text{biholomorphic}': 'biholomorphic',
            r'\\text{univalent}': 'univalent',
            
            # Special mappings
            r'z \\mapsto z^2': 'z maps to z squared',
            r'z \\mapsto e^z': 'z maps to e to the z',
            r'z \\mapsto \\frac{1}{z}': 'z maps to one over z',
            r'z \\mapsto \\frac{z-i}{z+i}': 'z maps to z minus i over z plus i',
        })
        
        # ===== COMPLEX INTEGRATION THEOREMS =====
        
        vocab.update({
            # Theorem names
            r'\\text{Cauchy\'s theorem}': "Cauchy's theorem",
            r'\\text{Cauchy\'s integral formula}': "Cauchy's integral formula",
            r'\\text{Cauchy\'s residue theorem}': "Cauchy's residue theorem",
            r'\\text{Morera\'s theorem}': "Morera's theorem",
            r'\\text{Liouville\'s theorem}': "Liouville's theorem",
            r'\\text{Maximum modulus principle}': 'Maximum modulus principle',
            r'\\text{Rouché\'s theorem}': "Rouché's theorem",
            
            # Formulas
            r'f\\(z\\) = \\frac{1}{2\\pi i} \\oint_\\gamma \\frac{f\\(w\\)}{w-z}\\,dw':
                'f of z equals one over two pi i times the contour integral over gamma of f of w over w minus z d w',
            r'f^{\\(n\\)}\\(z\\) = \\frac{n!}{2\\pi i} \\oint_\\gamma \\frac{f\\(w\\)}{\\(w-z\\)^{n+1}}\\,dw':
                'the n-th derivative of f at z equals n factorial over two pi i times the contour integral over gamma of f of w over w minus z to the n plus 1 d w',
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements for complex analysis"""
        patterns = [
            # Complex number expressions
            (r'z\s*=\s*x\s*\+\s*iy',
             'z equals x plus i y'),
            (r'z\s*=\s*r\s*e\^{i\\theta}',
             'z equals r e to the i theta'),
            (r'z\s*=\s*r\\(\\cos\\theta\s*\+\s*i\\sin\\theta\\)',
             'z equals r times cosine theta plus i sine theta'),
            
            # Holomorphic conditions
            (r'f\s+is\s+holomorphic\s+on\s+([A-Z])',
             lambda m: f"f is holomorphic on {m.group(1)}"),
            (r'f\s+is\s+analytic\s+at\s+z_0',
             'f is analytic at z naught'),
            (r'f\s+has\s+a\s+pole\s+at\s+z_0',
             'f has a pole at z naught'),
            
            # Integration statements
            (r'\\oint_C\s*f\\(z\\)\\,dz\s*=\s*0',
             'the contour integral over C of f of z d z equals zero'),
            (r'\\oint_\\gamma\s*f\\(z\\)\\,dz\s*=\s*2\\pi i\\sum\\text{Res}',
             'the contour integral over gamma of f of z d z equals two pi i times the sum of residues'),
            
            # Cauchy-Riemann in different forms
            (r'\\frac{\\partial f}{\\partial \\bar{z}}\s*=\s*0',
             'partial f partial z bar equals zero'),
            (r'f_z\s*=\s*0',
             'f sub z equals zero'),
            (r'f_{\\bar{z}}\s*=\s*0',
             'f sub z bar equals zero'),
            
            # Complex differentiation
            (r'f\'\\(z_0\\)\s*=\s*\\lim_{z\\to z_0}\\frac{f\\(z\\)-f\\(z_0\\)}{z-z_0}',
             'f prime of z naught equals the limit as z approaches z naught of f of z minus f of z naught over z minus z naught'),
            
            # Branch cuts
            (r'\\text{branch cut along the negative real axis}',
             'branch cut along the negative real axis'),
            (r'\\text{principal branch}',
             'principal branch'),
            (r'-\\pi < \\arg z \\leq \\pi',
             'negative pi is less than arg z which is less than or equal to pi'),
            
            # Convergence regions
            (r'\|z-z_0\|\s*<\s*R',
             'the modulus of z minus z naught is less than R'),
            (r'r\s*<\s*\|z-z_0\|\s*<\s*R',
             'r is less than the modulus of z minus z naught which is less than R'),
            
            # Winding number
            (r'n\\(\\gamma, z_0\\)',
             'the winding number of gamma about z naught'),
            (r'\\text{Ind}_\\gamma\\(z_0\\)',
             'the index of gamma at z naught'),
        ]
        
        return patterns
    
    def _compile_patterns(self) -> List[Tuple[re.Pattern, Union[str, Callable]]]:
        """Compile patterns for efficiency"""
        compiled = []
        
        # Compile vocabulary patterns
        for pattern, replacement in self.terms.items():
            try:
                compiled.append((re.compile(pattern), replacement))
            except re.error as e:
                logger.warning(f"Failed to compile pattern {pattern}: {e}")
        
        # Compile larger patterns
        for pattern, replacement in self.patterns:
            try:
                compiled.append((re.compile(pattern), replacement))
            except re.error as e:
                logger.warning(f"Failed to compile pattern {pattern}: {e}")
        
        return compiled
    
    def _process_nested(self, content: str) -> str:
        """Process nested mathematical content"""
        content = content.strip()
        
        # Handle common nested patterns
        replacements = [
            (r'z_0', 'z naught'),
            (r'z_k', 'z sub k'),
            (r'z_n', 'z sub n'),
            (r'w', 'w'),
            (r'\\mathbb{C}', 'C'),
            (r'_([0-9])', r' sub \1'),
            (r'\^([0-9])', r' to the \1'),
            (r'\^n', ' to the n'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        return content

# ===========================
# Main Complex Analysis Processor
# ===========================

class ComplexAnalysisProcessor:
    """Main processor for complex analysis domain"""
    
    def __init__(self):
        self.vocabulary = ComplexAnalysisVocabulary()
        self.context = ComplexContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_theorems': True,
            'clarify_branch_cuts': True,
            'expand_integration': True,
        }
        
        logger.info("Complex analysis processor initialized")
    
    def detect_subcontext(self, text: str) -> ComplexContext:
        """Detect specific complex analysis subcontext"""
        text_lower = text.lower()
        
        # Check for integration context
        if any(term in text_lower for term in ['contour', 'integral', '∮', 'oint']):
            return ComplexContext.INTEGRATION
        
        # Check for residue theory
        if any(term in text_lower for term in ['residue', 'pole', 'singularit']):
            return ComplexContext.RESIDUES
        
        # Check for holomorphic functions
        if any(term in text_lower for term in ['holomorphic', 'analytic', 'cauchy-riemann']):
            return ComplexContext.HOLOMORPHIC
        
        # Check for special functions
        if any(term in text_lower for term in ['log', 'exp', 'branch']):
            return ComplexContext.SPECIAL_FUNCTIONS
        
        # Check for series
        if any(term in text_lower for term in ['taylor', 'laurent', 'series']):
            return ComplexContext.SERIES
        
        # Check for conformal mappings
        if any(term in text_lower for term in ['conformal', 'möbius', 'biholomorphic']):
            return ComplexContext.CONFORMAL
        
        # Default to basic complex
        if any(term in text_lower for term in ['complex', 'imaginary', 'real part']):
            return ComplexContext.BASIC_COMPLEX
        
        return ComplexContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process complex analysis text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"Complex analysis subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special complex analysis rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process complex analysis text"""
        # Normalize common variations
        normalizations = [
            (r'holo\.\s+', 'holomorphic '),
            (r'mero\.\s+', 'meromorphic '),
            (r'C-R\s+', 'Cauchy-Riemann '),
            (r'\\mathrm{d}z', 'dz'),  # Normalize differential
            (r'\\,dz', ' dz'),  # Remove thin space before dz
            (r'\\text{d}z', 'dz'),
            (r'\\mathop{}\s*d', 'd'),  # Clean up differential operators
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply complex analysis vocabulary replacements"""
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
        """Apply special complex analysis rules"""
        
        # Emphasize key theorems
        if self.special_rules['emphasize_theorems']:
            theorem_patterns = [
                (r"Cauchy's\s+theorem", "{{EMPHASIS}}Cauchy's theorem{{/EMPHASIS}}"),
                (r"Cauchy's\s+integral\s+formula", "{{EMPHASIS}}Cauchy's integral formula{{/EMPHASIS}}"),
                (r"residue\s+theorem", "{{EMPHASIS}}residue theorem{{/EMPHASIS}}"),
                (r"Liouville's\s+theorem", "{{EMPHASIS}}Liouville's theorem{{/EMPHASIS}}"),
                (r"maximum\s+modulus\s+principle", "{{EMPHASIS}}maximum modulus principle{{/EMPHASIS}}"),
            ]
            
            for pattern, replacement in theorem_patterns:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Clarify branch cuts
        if self.special_rules['clarify_branch_cuts']:
            if 'branch' in text.lower():
                # Add clarification about branch cuts
                text = re.sub(
                    r'(branch cut)',
                    r'\1 {{CLARIFY}}(a line where the function is discontinuous){{/CLARIFY}}',
                    text,
                    count=1,
                    flags=re.IGNORECASE
                )
        
        # Expand integration notation
        if self.special_rules['expand_integration']:
            # Make contour direction explicit
            text = re.sub(
                r'(positively oriented)',
                r'\1 {{CLARIFY}}(counterclockwise){{/CLARIFY}}',
                text
            )
        
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
        
        # Handle emphasis and clarification markers
        text = re.sub(r'\{\{EMPHASIS\}\}', '', text)
        text = re.sub(r'\{\{/EMPHASIS\}\}', '', text)
        text = re.sub(r'\{\{CLARIFY\}\}', ', ', text)
        text = re.sub(r'\{\{/CLARIFY\}\}', ',', text)
        
        # Clean up spacing around mathematical terms
        text = re.sub(r'\s+d\s*z\b', ' d z', text)
        text = re.sub(r'\s+d\s*w\b', ' d w', text)
        
        return text
    
    def get_context_info(self) -> Dict[str, Any]:
        """Get information about current processing context"""
        return {
            'domain': 'complex_analysis',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_complex_analysis_processor():
    """Comprehensive test of complex analysis processor"""
    processor = ComplexAnalysisProcessor()
    
    test_cases = [
        # Basic complex numbers
        "Let $z = x + iy$ where $x, y \\in \\mathbb{R}$.",
        "$|z|^2 = z\\bar{z} = x^2 + y^2$",
        "$\\arg(z) = \\arctan(y/x)$ for $x > 0$",
        
        # Holomorphic functions
        "A function $f$ is holomorphic if $\\frac{\\partial f}{\\partial \\bar{z}} = 0$.",
        "The Cauchy-Riemann equations: $u_x = v_y$ and $u_y = -v_x$",
        "$f'(z) = \\lim_{h \\to 0} \\frac{f(z+h) - f(z)}{h}$",
        
        # Contour integration
        "$\\oint_C f(z)\\,dz = 2\\pi i \\sum \\text{Res}(f, z_k)$",
        "By Cauchy's theorem, $\\oint_\\gamma f(z)\\,dz = 0$ for holomorphic $f$.",
        
        # Residues and poles
        "$\\text{Res}(f, z_0) = \\frac{1}{2\\pi i} \\oint_{|z-z_0|=\\epsilon} f(z)\\,dz$",
        "$f$ has a pole of order $n$ at $z_0$ if $(z-z_0)^n f(z)$ has a removable singularity.",
        
        # Special functions
        "$\\log z = \\ln|z| + i\\arg(z)$ with branch cut along the negative real axis",
        "$e^{i\\pi} = -1$ (Euler's identity)",
        
        # Series expansions
        "$f(z) = \\sum_{n=0}^\\infty a_n(z-z_0)^n$ converges for $|z-z_0| < R$",
        "Laurent series: $f(z) = \\sum_{n=-\\infty}^\\infty a_n(z-z_0)^n$",
        
        # Conformal mappings
        "The map $w = \\frac{z-i}{z+i}$ maps the upper half-plane to the unit disk.",
        "$f$ is conformal if $f'(z) \\neq 0$",
    ]
    
    print("Testing Complex Analysis Processor")
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
    test_complex_analysis_processor()