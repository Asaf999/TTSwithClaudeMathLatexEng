#!/usr/bin/env python3
"""
Numerical Analysis Domain Processor for Mathematical Text-to-Speech
==================================================================

Complete processor for numerical analysis notation including:
- Error analysis and convergence rates
- Iterative methods and algorithms
- Matrix computations (LU, QR, SVD)
- Interpolation and approximation
- Finite differences and quadrature
- Stability analysis
- Floating-point arithmetic

This processor handles all undergraduate and graduate numerical analysis notation
with clear pronunciation of algorithmic concepts.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Numerical Analysis Contexts
# ===========================

class NumericalContext(Enum):
    """Specific numerical analysis contexts"""
    ERROR_ANALYSIS = "error_analysis"
    ITERATIVE_METHODS = "iterative_methods"
    MATRIX_COMPUTATIONS = "matrix_computations"
    INTERPOLATION = "interpolation"
    QUADRATURE = "quadrature"
    DIFFERENTIAL_EQUATIONS = "differential_equations"
    OPTIMIZATION = "optimization"
    GENERAL = "general"

@dataclass
class NumericalTerm:
    """Represents a numerical analysis term with pronunciation"""
    latex: str
    spoken: str
    context: NumericalContext
    emphasis: bool = False
    add_clarification: bool = False

# ===========================
# Numerical Analysis Vocabulary
# ===========================

class NumericalAnalysisVocabulary:
    """Complete numerical analysis vocabulary with natural pronunciations"""
    
    def __init__(self):
        self.terms = self._build_vocabulary()
        self.patterns = self._build_patterns()
        self.compiled_patterns = self._compile_patterns()
    
    def _escape_for_both_backslashes(self, pattern: str) -> str:
        """Convert a pattern to match both single and double backslash versions"""
        # This handles the fact that sometimes LaTeX commands come with single \
        # and sometimes with double \\
        import re as regex
        
        # Find all LaTeX commands in the pattern (they start with \\)
        # Replace each \\command with a pattern that matches both \\ and \\\\
        def replace_command(match):
            cmd = match.group(0)
            # Extract just the command name without backslashes
            if cmd.startswith(r'\\'):
                cmd_name = cmd[2:]  # Remove the \\
            else:
                return cmd  # Not a LaTeX command
            
            # Return pattern that matches both single and double backslash versions
            return r'(?:\\\\|\\)' + regex.escape(cmd_name)
        
        # Replace all LaTeX commands
        pattern = regex.sub(r'\\\\[a-zA-Z]+', replace_command, pattern)
        
        return pattern
    
    def _build_vocabulary(self) -> Dict[str, Union[str, Callable]]:
        """Build comprehensive numerical analysis vocabulary"""
        vocab = {}
        
        # ===== ERROR ANALYSIS =====
        
        vocab.update({
            # Big O notation
            r'O\(h\^n\)': 'big O of h to the n',
            r'O\(h\^2\)': 'big O of h squared',
            r'O\(h\^4\)': 'big O of h to the fourth',
            r'O\(n\)': 'big O of n',
            r'O\(n\^2\)': 'big O of n squared',
            r'O\(n\s*\\log\s*n\)': 'big O of n log n',
            r'O\(1\)': 'big O of 1',
            r'O\(\\epsilon\)': 'big O of epsilon',
            
            # Other complexity notations
            r'\\Theta\(n\)': 'big theta of n',
            r'\\Omega\(n\)': 'big omega of n',
            r'o\(h\)': 'little o of h',
            
            # Error types
            r'\\epsilon_{machine}': 'machine epsilon',
            r'\\epsilon_{mach}': 'machine epsilon',
            r'\\text{eps}': 'epsilon',
            r'e_{abs}': 'absolute error',
            r'e_{rel}': 'relative error',
            r'\\|e\\|': 'the norm of the error',
            r'\\|e\\|_\\infty': 'the infinity norm of the error',
            r'\\|e\\|_2': 'the 2-norm of the error',
            
            # Convergence rates
            r'\\text{linear convergence}': 'linear convergence',
            r'\\text{quadratic convergence}': 'quadratic convergence',
            r'\\text{superlinear convergence}': 'superlinear convergence',
            r'\\text{order } p': 'order p',
            r'\\text{convergence rate}': 'convergence rate',
            
            # Condition numbers
            r'\\kappa\(A\)': 'the condition number of A',
            r'\\text{cond}\(A\)': 'the condition number of A',
            r'\\kappa_2\(A\)': 'the 2-norm condition number of A',
            r'\\kappa_\\infty\(A\)': 'the infinity-norm condition number of A',
        })
        
        # ===== ITERATIVE METHODS =====
        
        vocab.update({
            # General iteration
            r'x\^{\(k\+1\)}': 'x superscript k plus 1',
            r'x\^{\(k\)}': 'x superscript k',
            r'x_k': 'x sub k',
            r'x_{k\+1}': 'x sub k plus 1',
            r'\\text{iterate}': 'iterate',
            r'\\text{iteration}': 'iteration',
            
            # Specific methods
            r'\\text{Newton\'s method}': "Newton's method",
            r'\\text{Newton-Raphson}': 'Newton-Raphson method',
            r'\\text{bisection method}': 'bisection method',
            r'\\text{secant method}': 'secant method',
            r'\\text{fixed-point iteration}': 'fixed-point iteration',
            r'\\text{Jacobi method}': 'Jacobi method',
            r'\\text{Gauss-Seidel}': 'Gauss-Seidel method',
            r'\\text{SOR}': 'successive over-relaxation',
            r'\\text{conjugate gradient}': 'conjugate gradient method',
            r'\\text{GMRES}': 'GMRES',
            
            # Iteration formulas
            r'x_{n\+1} = x_n - \\frac{f\(x_n\)}{f\'\(x_n\)}':
                'x sub n plus 1 equals x sub n minus f of x sub n over f prime of x sub n',
            r'x_{n\+1} = g\(x_n\)': 'x sub n plus 1 equals g of x sub n',
            
            # Convergence criteria
            r'\\|x_{k\+1} - x_k\\| < \\epsilon':
                'the norm of x sub k plus 1 minus x sub k is less than epsilon',
            r'\\|f\(x_k\)\\| < \\epsilon':
                'the norm of f of x sub k is less than epsilon',
            r'\\|r_k\\| < \\epsilon':
                'the norm of the residual r sub k is less than epsilon',
        })
        
        # ===== MATRIX COMPUTATIONS =====
        
        vocab.update({
            # Matrix factorizations
            r'A = LU': 'A equals L U',
            r'A = QR': 'A equals Q R',
            r'A = U\\Sigma V\^T': 'A equals U Sigma V transpose',
            r'A = U\\Sigma V\^\*': 'A equals U Sigma V conjugate transpose',
            r'PA = LU': 'P A equals L U',
            r'A = LL\^T': 'A equals L L transpose',
            r'A = LDL\^T': 'A equals L D L transpose',
            
            # Matrix types
            r'\\text{upper triangular}': 'upper triangular',
            r'\\text{lower triangular}': 'lower triangular',
            r'\\text{diagonal}': 'diagonal',
            r'\\text{tridiagonal}': 'tridiagonal',
            r'\\text{banded}': 'banded',
            r'\\text{sparse}': 'sparse',
            r'\\text{dense}': 'dense',
            r'\\text{symmetric}': 'symmetric',
            r'\\text{positive definite}': 'positive definite',
            r'\\text{orthogonal}': 'orthogonal',
            r'\\text{unitary}': 'unitary',
            
            # Matrix operations
            r'A\^{-1}': 'A inverse',
            r'A\^T': 'A transpose',
            r'A\^\*': 'A conjugate transpose',
            r'A\^H': 'A Hermitian',
            r'\\|A\\|_2': 'the 2-norm of A',
            r'\\|A\\|_F': 'the Frobenius norm of A',
            r'\\|A\\|_\\infty': 'the infinity norm of A',
            r'\\|A\\|_1': 'the 1-norm of A',
            
            # Eigenvalues
            r'\\lambda_{max}': 'lambda max',
            r'\\lambda_{min}': 'lambda min',
            r'\\lambda_i': 'lambda sub i',
            r'\\text{eigenvalue}': 'eigenvalue',
            r'\\text{eigenvector}': 'eigenvector',
            r'\\text{spectrum}': 'spectrum',
            r'\\rho\(A\)': 'the spectral radius of A',
        })
        
        # ===== INTERPOLATION =====
        
        vocab.update({
            # Interpolation types
            r'\\text{linear interpolation}': 'linear interpolation',
            r'\\text{polynomial interpolation}': 'polynomial interpolation',
            r'\\text{Lagrange interpolation}': 'Lagrange interpolation',
            r'\\text{Newton interpolation}': 'Newton interpolation',
            r'\\text{Hermite interpolation}': 'Hermite interpolation',
            r'\\text{spline interpolation}': 'spline interpolation',
            r'\\text{cubic spline}': 'cubic spline',
            
            # Interpolation notation
            r'p_n\(x\)': 'p sub n of x',
            r'P_n': 'P sub n',
            r'L_k\(x\)': 'L sub k of x',
            r'\\ell_k\(x\)': 'ell sub k of x',
            r'\\pi_n': 'pi sub n',
            
            # Lagrange basis
            r'L_k\(x\) = \\prod_{j \\neq k} \\frac{x - x_j}{x_k - x_j}':
                'L sub k of x equals the product over j not equal to k of x minus x sub j over x sub k minus x sub j',
            
            # Newton divided differences
            r'f\[x_0, x_1\]': 'f bracket x naught comma x one bracket',
            r'f\[x_0, x_1, x_2\]': 'f bracket x naught comma x one comma x two bracket',
            r'\\text{divided difference}': 'divided difference',
            
            # Error bounds
            r'\\|f - p_n\\|_\\infty': 'the infinity norm of f minus p sub n',
            r'\\max_{x \\in \[a,b\]} \|f\(x\) - p_n\(x\)\|':
                'the maximum over x in the interval a b of the absolute value of f of x minus p sub n of x',
        })
        
        # ===== QUADRATURE =====
        
        vocab.update({
            # Quadrature rules
            r'\\text{trapezoidal rule}': 'trapezoidal rule',
            r'\\text{Simpson\'s rule}': "Simpson's rule",
            r'\\text{midpoint rule}': 'midpoint rule',
            r'\\text{Gaussian quadrature}': 'Gaussian quadrature',
            r'\\text{Gauss-Legendre}': 'Gauss-Legendre quadrature',
            r'\\text{Gauss-Chebyshev}': 'Gauss-Chebyshev quadrature',
            r'\\text{composite rule}': 'composite rule',
            r'\\text{adaptive quadrature}': 'adaptive quadrature',
            
            # Quadrature formulas
            r'\\int_a^b f\(x\)\\,dx \\approx \\sum_{i=0}^n w_i f\(x_i\)':
                'the integral from a to b of f of x d x is approximately the sum from i equals 0 to n of w sub i times f of x sub i',
            r'Q_n\(f\)': 'Q sub n of f',
            r'I\(f\)': 'I of f',
            
            # Weights and nodes
            r'w_i': 'w sub i',
            r'x_i': 'x sub i',
            r'\\text{weights}': 'weights',
            r'\\text{nodes}': 'nodes',
            r'\\text{quadrature points}': 'quadrature points',
            
            # Error estimates
            r'E_n\(f\)': 'E sub n of f',
            r'R_n\(f\)': 'R sub n of f',
            r'O\(h\^{2p\+2}\)': 'big O of h to the 2p plus 2',
        })
        
        # ===== FINITE DIFFERENCES =====
        
        vocab.update({
            # Forward differences
            r'\\Delta f_i': 'delta f sub i',
            r'\\Delta_h f\(x\)': 'delta h f of x',
            r'f_{i\+1} - f_i': 'f sub i plus 1 minus f sub i',
            
            # Backward differences
            r'\\nabla f_i': 'nabla f sub i',
            r'f_i - f_{i-1}': 'f sub i minus f sub i minus 1',
            
            # Central differences
            r'\\delta f_i': 'delta f sub i',
            r'\\frac{f_{i\+1} - f_{i-1}}{2h}':
                'f sub i plus 1 minus f sub i minus 1 over 2 h',
            
            # Derivative approximations
            r'f\'_i \\approx \\frac{f_{i\+1} - f_i}{h}':
                'f prime sub i is approximately f sub i plus 1 minus f sub i over h',
            r'f\'\'_i \\approx \\frac{f_{i\+1} - 2f_i \+ f_{i-1}}{h\^2}':
                'f double prime sub i is approximately f sub i plus 1 minus 2 f sub i plus f sub i minus 1 over h squared',
            
            # Stencils
            r'\\text{stencil}': 'stencil',
            r'\\text{5-point stencil}': 'five-point stencil',
            r'\\text{compact scheme}': 'compact scheme',
        })
        
        # ===== STABILITY AND FLOATING POINT =====
        
        vocab.update({
            # Stability
            r'\\text{stable}': 'stable',
            r'\\text{unstable}': 'unstable',
            r'\\text{conditionally stable}': 'conditionally stable',
            r'\\text{absolutely stable}': 'absolutely stable',
            r'\\text{backward stable}': 'backward stable',
            r'\\text{forward stable}': 'forward stable',
            r'\\text{stability region}': 'stability region',
            
            # Floating point
            r'fl\(x\)': 'floating-point representation of x',
            r'\\text{round}\(x\)': 'round of x',
            r'\\text{chop}\(x\)': 'chop of x',
            r'\\text{ulp}': 'unit in the last place',
            r'\\text{overflow}': 'overflow',
            r'\\text{underflow}': 'underflow',
            r'\\text{cancellation}': 'cancellation',
            r'\\text{IEEE 754}': 'IEEE 754',
            
            # Precision
            r'\\text{single precision}': 'single precision',
            r'\\text{double precision}': 'double precision',
            r'\\text{extended precision}': 'extended precision',
            r'\\text{arbitrary precision}': 'arbitrary precision',
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements for numerical analysis"""
        patterns = [
            # Convergence statements
            (r'x_k \\to x\^\* as k \\to \\infty',
             'x sub k converges to x star as k goes to infinity'),
            (r'\\|x_k - x\^\*\\| \\leq C\\rho\^k',
             'the norm of x sub k minus x star is less than or equal to C times rho to the k'),
            (r'converges with order p',
             'converges with order p'),
            
            # Error bounds
            (r'\\|error\\| \\leq Ch\^p',
             'the norm of the error is less than or equal to C times h to the p'),
            (r'relative error = \\frac{\\|x - \\tilde{x}\\|}{\\|x\\|}',
             'relative error equals the norm of x minus x tilde over the norm of x'),
            
            # Algorithm descriptions
            (r'for k = 0, 1, 2, \\ldots',
             'for k equals 0, 1, 2, and so on'),
            (r'repeat until convergence',
             'repeat until convergence'),
            (r'while \\|r_k\\| > tol',
             'while the norm of r sub k is greater than tolerance'),
            
            # Matrix patterns
            (r'solve Ax = b',
             'solve A x equals b'),
            (r'where A \\in \\mathbb{R}\^{n \\times n}',
             'where A is in R n by n'),
            (r'A is symmetric positive definite',
             'A is symmetric positive definite'),
            
            # Complexity expressions
            (r'requires O\(n\^3\) operations',
             'requires big O of n cubed operations'),
            (r'O\(n\^2\) storage',
             'big O of n squared storage'),
            
            # Finite difference operators
            (r'\\Delta_x\^2 u',
             'delta x squared u'),
            (r'\\frac{\\partial\^2 u}{\\partial x\^2}',
             'second partial of u with respect to x'),
            
            # Stability conditions
            (r'\\|\\lambda h\\| \\leq 1',
             'the absolute value of lambda h is less than or equal to 1'),
            (r'CFL condition',
             'CFL condition'),
            (r'von Neumann stability analysis',
             'von Neumann stability analysis'),
        ]
        
        return patterns
    
    def _compile_patterns(self) -> List[Tuple[re.Pattern, Union[str, Callable]]]:
        """Compile patterns for efficiency"""
        compiled = []
        
        # Compile vocabulary patterns
        for pattern, replacement in self.terms.items():
            try:
                # Check if pattern contains LaTeX commands (backslashes)
                if r'\\' in pattern:  # Pattern contains LaTeX commands
                    # Make pattern flexible for both single and double backslashes
                    flexible_pattern = self._escape_for_both_backslashes(pattern)
                    compiled.append((re.compile(flexible_pattern), replacement))
                else:
                    compiled.append((re.compile(pattern), replacement))
            except re.error as e:
                logger.warning(f"Failed to compile pattern {pattern}: {e}")
        
        # Compile larger patterns
        for pattern, replacement in self.patterns:
            try:
                if r'\\' in pattern:  # Pattern contains LaTeX commands
                    flexible_pattern = self._escape_for_both_backslashes(pattern)
                    compiled.append((re.compile(flexible_pattern), replacement))
                else:
                    compiled.append((re.compile(pattern), replacement))
            except re.error as e:
                logger.warning(f"Failed to compile pattern {pattern}: {e}")
        
        return compiled
    
    def _process_nested(self, content: str) -> str:
        """Process nested mathematical content"""
        content = content.strip()
        
        # Handle common nested patterns
        replacements = [
            (r'x_i', 'x sub i'),
            (r'x_k', 'x sub k'),
            (r'x_n', 'x sub n'),
            (r'h\^2', 'h squared'),
            (r'h\^n', 'h to the n'),
            (r'O\(', 'big O of '),
            (r'\\mathbb{R}', 'R'),
            (r'_([0-9])', r' sub \1'),
            (r'\^([0-9])', r' to the \1'),
            (r'\^\*', ' star'),
            (r'\\epsilon', 'epsilon'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        return content

# ===========================
# Main Numerical Analysis Processor
# ===========================

class NumericalAnalysisProcessor:
    """Main processor for numerical analysis domain"""
    
    def __init__(self):
        self.vocabulary = NumericalAnalysisVocabulary()
        self.context = NumericalContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_stability': True,
            'clarify_algorithms': True,
            'expand_complexity': True,
            'highlight_convergence': True,
        }
        
        logger.info("Numerical analysis processor initialized")
    
    def detect_subcontext(self, text: str) -> NumericalContext:
        """Detect specific numerical analysis subcontext"""
        text_lower = text.lower()
        
        # Check for error analysis
        if any(term in text_lower for term in ['error', 'condition number', 'machine epsilon', 'convergence']):
            return NumericalContext.ERROR_ANALYSIS
        
        # Check for iterative methods
        if any(term in text_lower for term in ['newton', 'iteration', 'jacobi', 'gauss-seidel', 'fixed point']):
            return NumericalContext.ITERATIVE_METHODS
        
        # Check for matrix computations
        if any(term in text_lower for term in ['matrix', 'eigenvalue', 'factorization', 'decomposition']):
            return NumericalContext.MATRIX_COMPUTATIONS
        
        # Check for interpolation
        if any(term in text_lower for term in ['interpolat', 'lagrange', 'spline', 'polynomial']):
            return NumericalContext.INTERPOLATION
        
        # Check for quadrature
        if any(term in text_lower for term in ['quadrature', 'integral', 'trapezoidal', 'simpson']):
            return NumericalContext.QUADRATURE
        
        # Check for optimization
        if any(term in text_lower for term in ['optimi', 'minimi', 'maximi', 'gradient']):
            return NumericalContext.OPTIMIZATION
        
        return NumericalContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process numerical analysis text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"Numerical analysis subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special numerical analysis rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process numerical analysis text"""
        # Normalize common variations
        normalizations = [
            (r'alg\.\s+', 'algorithm '),
            (r'eqn\.\s+', 'equation '),
            (r'approx\.\s+', 'approximately '),
            (r'tol\b', 'tolerance'),
            (r'iter\b', 'iteration'),
            (r'cond\b', 'condition'),
            (r'abs\.\s+error', 'absolute error'),
            (r'rel\.\s+error', 'relative error'),
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply numerical analysis vocabulary replacements"""
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
        """Apply special numerical analysis rules"""
        
        # Emphasize stability conditions
        if self.special_rules['emphasize_stability']:
            stability_patterns = [
                (r'(stable)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
                (r'(unstable)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
                (r'(ill-conditioned)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
                (r'(well-conditioned)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
            ]
            
            for pattern, replacement in stability_patterns:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Clarify algorithms
        if self.special_rules['clarify_algorithms']:
            if re.search(r'Newton|iteration|algorithm', text, re.IGNORECASE):
                # Add brief clarification for complex algorithms
                text = re.sub(
                    r"(Newton's method)",
                    r"\1 {{CLARIFY}}(for finding roots){{/CLARIFY}}",
                    text,
                    count=1
                )
        
        # Expand complexity notation
        if self.special_rules['expand_complexity']:
            # Make complexity more explicit
            text = re.sub(
                r'O\(n\^3\)',
                r'O(n^3) {{CLARIFY}}(cubic time){{/CLARIFY}}',
                text,
                count=1
            )
            text = re.sub(
                r'O\(n\s*log\s*n\)',
                r'O(n log n) {{CLARIFY}}(linearithmic time){{/CLARIFY}}',
                text,
                count=1
            )
        
        # Highlight convergence
        if self.special_rules['highlight_convergence']:
            convergence_patterns = [
                (r'(converges)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
                (r'(diverges)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
                (r'(quadratic convergence)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
                (r'(linear convergence)', r'{{EMPHASIS}}\1{{/EMPHASIS}}'),
            ]
            
            for pattern, replacement in convergence_patterns:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
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
        
        return text
    
    def get_context_info(self) -> Dict[str, Any]:
        """Get information about current processing context"""
        return {
            'domain': 'numerical_analysis',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_numerical_analysis_processor():
    """Comprehensive test of numerical analysis processor"""
    processor = NumericalAnalysisProcessor()
    
    test_cases = [
        # Error analysis
        "The error is $O(h^2)$ where $h$ is the step size.",
        "$\\kappa(A) = \\|A\\|\\|A^{-1}\\|$ is the condition number",
        "Machine epsilon $\\epsilon_{machine} \\approx 2.22 \\times 10^{-16}$",
        
        # Iterative methods
        "$x_{k+1} = x_k - \\frac{f(x_k)}{f'(x_k)}$ (Newton's method)",
        "The method converges with order $p = 2$ (quadratic convergence)",
        "Stop when $\\|x_{k+1} - x_k\\| < \\epsilon$",
        
        # Matrix computations
        "$A = LU$ where $L$ is lower triangular and $U$ is upper triangular",
        "$A = QR$ where $Q$ is orthogonal and $R$ is upper triangular",
        "The eigenvalues $\\lambda_i$ satisfy $\\det(A - \\lambda I) = 0$",
        
        # Interpolation
        "Lagrange interpolation: $p_n(x) = \\sum_{k=0}^n f(x_k)L_k(x)$",
        "$L_k(x) = \\prod_{j \\neq k} \\frac{x - x_j}{x_k - x_j}$",
        "The error is $\\|f - p_n\\|_\\infty \\leq \\frac{M_{n+1}}{(n+1)!}\\|\\omega_{n+1}\\|_\\infty$",
        
        # Quadrature
        "$\\int_a^b f(x)\\,dx \\approx \\sum_{i=0}^n w_i f(x_i)$",
        "Trapezoidal rule: $\\int_a^b f(x)\\,dx \\approx \\frac{h}{2}[f(a) + 2\\sum_{i=1}^{n-1} f(x_i) + f(b)]$",
        
        # Finite differences
        "$f'(x) \\approx \\frac{f(x+h) - f(x)}{h} + O(h)$",
        "$f''(x) \\approx \\frac{f(x+h) - 2f(x) + f(x-h)}{h^2} + O(h^2)$",
        
        # Stability
        "The method is stable if $\\|\\lambda h\\| \\leq 1$",
        "The algorithm is backward stable",
    ]
    
    print("Testing Numerical Analysis Processor")
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
    test_numerical_analysis_processor()