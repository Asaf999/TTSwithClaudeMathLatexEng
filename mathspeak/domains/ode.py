#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ordinary Differential Equations (ODE) Domain Processor for Mathematical Text-to-Speech
=====================================================================================

Complete processor for ordinary differential equations notation including:
- Basic ODEs (first/second order, IVP, BVP)
- First-order ODEs (separable, linear, exact, Bernoulli, Riccati, etc.)
- Second-order linear ODEs (homogeneous, non-homogeneous, characteristic equations)
- Higher-order ODEs and systems
- Series solutions and special functions
- Laplace transforms and operational methods
- Systems of ODEs and matrix methods
- Existence/uniqueness theorems
- Qualitative theory and dynamical systems
- Phase plane analysis and stability
- Numerical methods for ODEs

This processor handles ALL ODE notation with professor-quality pronunciation.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# ODE Context Types
# ===========================

class ODEContext(Enum):
    """Specific ODE contexts for fine-grained processing"""
    BASIC_ODE = "basic_ode"
    FIRST_ORDER = "first_order"
    SECOND_ORDER = "second_order"
    HIGHER_ORDER = "higher_order"
    SYSTEMS = "systems"
    LAPLACE = "laplace"
    SERIES_SOLUTIONS = "series_solutions"
    QUALITATIVE = "qualitative"
    NUMERICAL = "numerical"
    GENERAL = "general"

@dataclass
class ODETerm:
    """Represents an ODE term with pronunciation hints"""
    latex: str
    spoken: str
    context: ODEContext
    emphasis: bool = False
    add_article: bool = True  # Whether to add "the" before term

# ===========================
# Comprehensive ODE Vocabulary
# ===========================

class ODEVocabulary:
    """Complete ODE vocabulary with natural pronunciations"""
    
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
        """Build comprehensive ODE vocabulary"""
        vocab = {}
        
        # ===== BASIC ODE NOTATION =====
        
        # Derivatives and differential operators
        vocab.update({
            r'\\frac{dy}{dx}': 'd y d x',
            r'\\frac{d^2y}{dx^2}': 'd squared y d x squared',
            r'\\frac{d^ny}{dx^n}': 'd to the n y d x to the n',
            r'\\frac{d^([0-9]+)y}{dx^([0-9]+)}': lambda m: f'd to the {self._ordinal(m.group(1))} y d x to the {m.group(2)}',
            r"y'": 'y prime',
            r"y''": 'y double prime',
            r"y'''": 'y triple prime',
            r"y\\'": 'y prime',
            r"y\\'\\'": 'y double prime',
            r"y\\'\\'\\'": 'y triple prime',
            r'y^{\\prime}': 'y prime',
            r'y^{\\prime\\prime}': 'y double prime',
            r'y^{\\prime\\prime\\prime}': 'y triple prime',
            r'y^{\(([0-9]+)\)}': lambda m: f'y superscript {m.group(1)}',
            r'\\dot{y}': 'y dot',
            r'\\ddot{y}': 'y double dot',
            r'\\dot{x}': 'x dot',
            r'\\ddot{x}': 'x double dot',
            r'D': 'the differential operator D',
            r'D^2': 'D squared',
            r'D^n': 'D to the n',
            r'\\mathcal{D}': 'the differential operator script D',
            r'\\nabla': 'nabla',
            r'\\Delta': 'the Laplacian',
        })
        
        # Basic ODE forms
        vocab.update({
            r'y\' = f\(x,y\)': 'y prime equals f of x y',
            r'y\'\' = f\(x,y,y\'\)': 'y double prime equals f of x y y prime',
            r'F\(x,y,y\',\\ldots,y^{\(n\)}\) = 0': 'F of x y y prime up to y n equals zero',
            r'a_n\(x\)y^{\(n\)} \+ \\cdots \+ a_1\(x\)y\' \+ a_0\(x\)y = f\(x\)': 'a n of x times y n plus dot dot dot plus a 1 of x times y prime plus a 0 of x times y equals f of x',
            r'y\(x_0\) = y_0': 'y of x naught equals y naught',
            r'y\'\(x_0\) = y_1': 'y prime of x naught equals y one',
            r'y\(a\) = \\alpha': 'y of a equals alpha',
            r'y\(b\) = \\beta': 'y of b equals beta',
        })
        
        # ODE types
        vocab.update({
            r'\\text{ODE}': 'O D E',
            r'\\text{IVP}': 'initial value problem',
            r'\\text{BVP}': 'boundary value problem',
            r'\\text{linear}': 'linear',
            r'\\text{nonlinear}': 'nonlinear',
            r'\\text{homogeneous}': 'homogeneous',
            r'\\text{non-homogeneous}': 'non-homogeneous',
            r'\\text{autonomous}': 'autonomous',
            r'\\text{non-autonomous}': 'non-autonomous',
            r'\\text{order}': 'order',
            r'\\text{degree}': 'degree',
        })
        
        # ===== FIRST-ORDER ODEs =====
        
        # Separable equations
        vocab.update({
            r'\\frac{dy}{dx} = g\(x\)h\(y\)': 'd y d x equals g of x times h of y',
            r'\\int \\frac{dy}{h\(y\)} = \\int g\(x\)dx': 'integral d y over h of y equals integral g of x d x',
            r'M\(x\)dx \+ N\(y\)dy = 0': 'M of x d x plus N of y d y equals zero',
            r'\\text{separable}': 'separable',
            r'\\text{variables separable}': 'variables separable',
        })
        
        # Linear first-order
        vocab.update({
            r'y\' \+ P\(x\)y = Q\(x\)': 'y prime plus P of x y equals Q of x',
            r'\\frac{dy}{dx} \+ P\(x\)y = Q\(x\)': 'd y d x plus P of x y equals Q of x',
            r'\\mu\(x\) = e^{\\int P\(x\)dx}': 'mu of x equals e to the integral P of x d x',
            r'\\text{integrating factor}': 'integrating factor',
            r'ye^{\\int P\(x\)dx} = \\int Q\(x\)e^{\\int P\(x\)dx}dx': 'y times e to the integral P of x d x equals integral Q of x times e to the integral P of x d x d x',
        })
        
        # Exact equations
        vocab.update({
            r'M\(x,y\)dx \+ N\(x,y\)dy = 0': 'M of x y d x plus N of x y d y equals zero',
            r'\\frac{\\partial M}{\\partial y} = \\frac{\\partial N}{\\partial x}': 'partial M partial y equals partial N partial x',
            r'\\text{exact}': 'exact',
            r'\\text{exact differential}': 'exact differential',
            r'\\exists \\Phi: d\\Phi = Mdx \+ Ndy': 'there exists Phi such that d Phi equals M d x plus N d y',
            r'\\Phi\(x,y\) = C': 'Phi of x y equals C',
        })
        
        # Special types
        vocab.update({
            r'\\text{Bernoulli}': 'Bernoulli',
            r'y\' \+ P\(x\)y = Q\(x\)y^n': 'y prime plus P of x y equals Q of x y to the n',
            r'\\text{Riccati}': 'Riccati',
            r'y\' = P\(x\)y^2 \+ Q\(x\)y \+ R\(x\)': 'y prime equals P of x y squared plus Q of x y plus R of x',
            r'\\text{Clairaut}': 'Clairaut',
            r'y = xy\' \+ f\(y\'\)': 'y equals x y prime plus f of y prime',
            r'\\text{Lagrange}': 'Lagrange',
            r'y = xf\(y\'\) \+ g\(y\'\)': 'y equals x f of y prime plus g of y prime',
        })
        
        # ===== SECOND-ORDER LINEAR ODEs =====
        
        # General forms
        vocab.update({
            r'y\'\' \+ p\(x\)y\' \+ q\(x\)y = 0': 'y double prime plus p of x y prime plus q of x y equals zero',
            r'y\'\' \+ p\(x\)y\' \+ q\(x\)y = f\(x\)': 'y double prime plus p of x y prime plus q of x y equals f of x',
            r'a\(x\)y\'\' \+ b\(x\)y\' \+ c\(x\)y = 0': 'a of x y double prime plus b of x y prime plus c of x y equals zero',
            r'\\text{Wronskian}': 'Wronskian',
            r'W\(y_1,y_2\) = \\begin{vmatrix} y_1 & y_2 \\\\ y_1\' & y_2\' \\end{vmatrix}': 'W of y 1 y 2 equals the determinant of y 1 y 2 y 1 prime y 2 prime',
            r'W = y_1 y_2\' - y_1\' y_2': 'W equals y 1 y 2 prime minus y 1 prime y 2',
        })
        
        # Constant coefficients
        vocab.update({
            r'ay\'\' \+ by\' \+ cy = 0': 'a y double prime plus b y prime plus c y equals zero',
            r'ar^2 \+ br \+ c = 0': 'a r squared plus b r plus c equals zero',
            r'\\text{characteristic equation}': 'characteristic equation',
            r'\\text{auxiliary equation}': 'auxiliary equation',
            r'r = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}': 'r equals negative b plus or minus square root of b squared minus 4 a c over 2 a',
            r'y = c_1 e^{r_1 x} \+ c_2 e^{r_2 x}': 'y equals c 1 e to the r 1 x plus c 2 e to the r 2 x',
            r'y = e^{\\alpha x}\(c_1 \\cos \\beta x \+ c_2 \\sin \\beta x\)': 'y equals e to the alpha x times c 1 cosine beta x plus c 2 sine beta x',
            r'y = \(c_1 \+ c_2 x\)e^{rx}': 'y equals c 1 plus c 2 x times e to the r x',
        })
        
        # Method of undetermined coefficients
        vocab.update({
            r'y_p': 'y particular',
            r'y_c': 'y complementary',
            r'y = y_c \+ y_p': 'y equals y complementary plus y particular',
            r'\\text{undetermined coefficients}': 'undetermined coefficients',
            r'\\text{method of annihilators}': 'method of annihilators',
            r'\\text{operator method}': 'operator method',
        })
        
        # Variation of parameters
        vocab.update({
            r'\\text{variation of parameters}': 'variation of parameters',
            r'y_p = u_1\(x\)y_1 \+ u_2\(x\)y_2': 'y particular equals u 1 of x y 1 plus u 2 of x y 2',
            r'u_1\' = -\\frac{y_2 f\(x\)}{W}': 'u 1 prime equals negative y 2 f of x over W',
            r'u_2\' = \\frac{y_1 f\(x\)}{W}': 'u 2 prime equals y 1 f of x over W',
        })
        
        # ===== SERIES SOLUTIONS =====
        
        # Power series
        vocab.update({
            r'y = \\sum_{n=0}^{\\infty} a_n x^n': 'y equals sum from n equals 0 to infinity a n x to the n',
            r'y = \\sum_{n=0}^{\\infty} a_n \(x-x_0\)^n': 'y equals sum from n equals 0 to infinity a n times x minus x naught to the n',
            r'\\text{radius of convergence}': 'radius of convergence',
            r'\\text{ordinary point}': 'ordinary point',
            r'\\text{singular point}': 'singular point',
            r'\\text{regular singular point}': 'regular singular point',
            r'\\text{irregular singular point}': 'irregular singular point',
        })
        
        # Frobenius method
        vocab.update({
            r'\\text{Frobenius}': 'Frobenius',
            r'y = x^r \\sum_{n=0}^{\\infty} a_n x^n': 'y equals x to the r times sum from n equals 0 to infinity a n x to the n',
            r'y = \(x-x_0\)^r \\sum_{n=0}^{\\infty} a_n \(x-x_0\)^n': 'y equals x minus x naught to the r times sum a n x minus x naught to the n',
            r'\\text{indicial equation}': 'indicial equation',
            r'r\(r-1\) \+ p_0 r \+ q_0 = 0': 'r times r minus 1 plus p naught r plus q naught equals zero',
        })
        
        # Special functions
        vocab.update({
            r'\\text{Bessel}': 'Bessel',
            r'J_n\(x\)': 'J sub n of x',
            r'Y_n\(x\)': 'Y sub n of x',
            r'J_\\nu\(x\)': 'J sub nu of x',
            r'Y_\\nu\(x\)': 'Y sub nu of x',
            r'I_\\nu\(x\)': 'I sub nu of x',
            r'K_\\nu\(x\)': 'K sub nu of x',
            r'\\text{Legendre}': 'Legendre',
            r'P_n\(x\)': 'P sub n of x',
            r'Q_n\(x\)': 'Q sub n of x',
            r'\\text{Hermite}': 'Hermite',
            r'H_n\(x\)': 'H sub n of x',
            r'\\text{Laguerre}': 'Laguerre',
            r'L_n\(x\)': 'L sub n of x',
            r'\\text{Chebyshev}': 'Chebyshev',
            r'T_n\(x\)': 'T sub n of x',
            r'U_n\(x\)': 'U sub n of x',
            r'\\text{hypergeometric}': 'hypergeometric',
            r'_2F_1': 'two F one',
            r'\\text{Airy}': 'Airy',
            r'\\text{Ai}\(x\)': 'Airy Ai of x',
            r'\\text{Bi}\(x\)': 'Airy Bi of x',
        })
        
        # ===== LAPLACE TRANSFORMS =====
        
        # Basic transforms
        vocab.update({
            r'\\mathcal{L}': 'the Laplace transform',
            r'\\mathcal{L}\\{f\(t\)\\}': 'Laplace transform of f of t',
            r'\\mathcal{L}\\{f\\}': 'Laplace transform of f',
            r'F\(s\) = \\mathcal{L}\\{f\(t\)\\}': 'F of s equals Laplace transform of f of t',
            r'F\(s\) = \\int_0^\\infty e^{-st} f\(t\) dt': 'F of s equals integral from 0 to infinity e to the minus s t f of t d t',
            r'\\mathcal{L}^{-1}': 'the inverse Laplace transform',
            r'\\mathcal{L}^{-1}\\{F\(s\)\\}': 'inverse Laplace transform of F of s',
            r'f\(t\) = \\mathcal{L}^{-1}\\{F\(s\)\\}': 'f of t equals inverse Laplace transform of F of s',
        })
        
        # Transform properties
        vocab.update({
            r'\\mathcal{L}\\{f\'\(t\)\\} = sF\(s\) - f\(0\)': 'Laplace of f prime of t equals s F of s minus f of 0',
            r'\\mathcal{L}\\{f\'\'\(t\)\\} = s^2F\(s\) - sf\(0\) - f\'\(0\)': 'Laplace of f double prime equals s squared F of s minus s f of 0 minus f prime of 0',
            r'\\mathcal{L}\\{t^n f\(t\)\\} = \(-1\)^n F^{\(n\)}\(s\)': 'Laplace of t to the n f of t equals minus 1 to the n F n of s',
            r'\\mathcal{L}\\{e^{at}f\(t\)\\} = F\(s-a\)': 'Laplace of e to the a t f of t equals F of s minus a',
            r'\\mathcal{L}\\{u\(t-a\)f\(t-a\)\\} = e^{-as}F\(s\)': 'Laplace of unit step at a times f of t minus a equals e to the minus a s F of s',
        })
        
        # Special functions
        vocab.update({
            r'u\(t\)': 'the unit step function',
            r'u\(t-a\)': 'the unit step at a',
            r'\\delta\(t\)': 'the Dirac delta function',
            r'\\delta\(t-a\)': 'the Dirac delta at a',
            r'H\(t\)': 'the Heaviside function',
            r'H\(t-a\)': 'the Heaviside function at a',
        })
        
        # ===== SYSTEMS OF ODEs =====
        
        # Matrix notation
        vocab.update({
            r'\\mathbf{x}\' = \\mathbf{A}\\mathbf{x}': 'x vector prime equals A x vector',
            r'\\mathbf{x}\' = \\mathbf{A}\\mathbf{x} \+ \\mathbf{f}\(t\)': 'x vector prime equals A x vector plus f vector of t',
            r'\\frac{d\\mathbf{x}}{dt} = \\mathbf{A}\\mathbf{x}': 'd x vector d t equals A x vector',
            r'\\mathbf{x}\(t\) = e^{\\mathbf{A}t}\\mathbf{x}_0': 'x vector of t equals e to the A t x vector naught',
            r'\\mathbf{x} = \\begin{pmatrix} x_1 \\\\ x_2 \\\\ \\vdots \\\\ x_n \\end{pmatrix}': 'x vector equals the column vector x 1 x 2 up to x n',
        })
        
        # Eigenvalues and eigenvectors
        vocab.update({
            r'\\det\(\\mathbf{A} - \\lambda \\mathbf{I}\) = 0': 'determinant of A minus lambda I equals zero',
            r'\\mathbf{A}\\mathbf{v} = \\lambda \\mathbf{v}': 'A v equals lambda v',
            r'\\lambda': 'lambda',
            r'\\lambda_1, \\lambda_2, \\ldots, \\lambda_n': 'lambda 1 lambda 2 up to lambda n',
            r'\\mathbf{v}_1, \\mathbf{v}_2, \\ldots, \\mathbf{v}_n': 'v 1 v 2 up to v n',
            r'\\text{eigenvalue}': 'eigenvalue',
            r'\\text{eigenvector}': 'eigenvector',
            r'\\text{characteristic polynomial}': 'characteristic polynomial',
        })
        
        # Fundamental matrix
        vocab.update({
            r'\\mathbf{\\Phi}\(t\)': 'the fundamental matrix Phi of t',
            r'\\mathbf{\\Phi}\'\(t\) = \\mathbf{A}\\mathbf{\\Phi}\(t\)': 'Phi prime of t equals A Phi of t',
            r'\\mathbf{\\Phi}\(0\) = \\mathbf{I}': 'Phi of 0 equals the identity',
            r'\\mathbf{x}\(t\) = \\mathbf{\\Phi}\(t\)\\mathbf{c}': 'x of t equals Phi of t times c',
        })
        
        # ===== EXISTENCE AND UNIQUENESS =====
        
        vocab.update({
            r'\\text{Lipschitz}': 'Lipschitz',
            r'\\text{Lipschitz continuous}': 'Lipschitz continuous',
            r'\|f\(x,y_1\) - f\(x,y_2\)\| \\leq L\|y_1 - y_2\|': 'absolute value f of x y 1 minus f of x y 2 less than or equal to L times absolute value y 1 minus y 2',
            r'\\text{Picard}': 'Picard',
            r'\\text{Picard iteration}': 'Picard iteration',
            r'y_{n\+1}\(x\) = y_0 \+ \\int_{x_0}^x f\(t,y_n\(t\)\)dt': 'y n plus 1 of x equals y naught plus integral from x naught to x f of t y n of t d t',
            r'\\text{Peano}': 'Peano',
            r'\\text{Cauchy-Peano}': 'Cauchy-Peano',
            r'\\text{existence}': 'existence',
            r'\\text{uniqueness}': 'uniqueness',
            r'\\text{Banach fixed point}': 'Banach fixed point',
            r'\\text{contraction mapping}': 'contraction mapping',
        })
        
        # ===== QUALITATIVE THEORY =====
        
        # Phase plane
        vocab.update({
            r'\\text{phase plane}': 'phase plane',
            r'\\text{phase portrait}': 'phase portrait',
            r'\\text{trajectory}': 'trajectory',
            r'\\text{orbit}': 'orbit',
            r'\\text{integral curve}': 'integral curve',
            r'\\text{solution curve}': 'solution curve',
            r'\\text{isocline}': 'isocline',
            r'\\text{nullcline}': 'nullcline',
            r'\\text{direction field}': 'direction field',
            r'\\text{slope field}': 'slope field',
        })
        
        # Equilibrium and stability
        vocab.update({
            r'\\text{equilibrium}': 'equilibrium',
            r'\\text{equilibrium point}': 'equilibrium point',
            r'\\text{critical point}': 'critical point',
            r'\\text{fixed point}': 'fixed point',
            r'\\text{stable}': 'stable',
            r'\\text{unstable}': 'unstable',
            r'\\text{asymptotically stable}': 'asymptotically stable',
            r'\\text{Lyapunov stable}': 'Lyapunov stable',
            r'\\text{neutrally stable}': 'neutrally stable',
            r'\\text{node}': 'node',
            r'\\text{saddle}': 'saddle',
            r'\\text{focus}': 'focus',
            r'\\text{spiral}': 'spiral',
            r'\\text{center}': 'center',
            r'\\text{sink}': 'sink',
            r'\\text{source}': 'source',
        })
        
        # Lyapunov theory
        vocab.update({
            r'\\text{Lyapunov}': 'Lyapunov',
            r'\\text{Lyapunov function}': 'Lyapunov function',
            r'V\(\\mathbf{x}\)': 'V of x',
            r'V\(\\mathbf{x}\) > 0': 'V of x greater than zero',
            r'\\dot{V} \\leq 0': 'V dot less than or equal to zero',
            r'\\text{LaSalle}': 'LaSalle',
            r'\\text{invariant set}': 'invariant set',
        })
        
        # Bifurcations
        vocab.update({
            r'\\text{bifurcation}': 'bifurcation',
            r'\\text{saddle-node}': 'saddle-node',
            r'\\text{transcritical}': 'transcritical',
            r'\\text{pitchfork}': 'pitchfork',
            r'\\text{Hopf}': 'Hopf',
            r'\\text{period-doubling}': 'period-doubling',
            r'\\text{limit cycle}': 'limit cycle',
            r'\\text{Poincaré-Bendixson}': 'Poincaré-Bendixson',
        })
        
        # ===== NUMERICAL METHODS =====
        
        vocab.update({
            r'\\text{Euler}': 'Euler',
            r'y_{n\+1} = y_n \+ hf\(x_n,y_n\)': 'y n plus 1 equals y n plus h f of x n y n',
            r'\\text{Runge-Kutta}': 'Runge-Kutta',
            r'\\text{RK4}': 'R K 4',
            r'\\text{Adams-Bashforth}': 'Adams-Bashforth',
            r'\\text{Adams-Moulton}': 'Adams-Moulton',
            r'\\text{predictor-corrector}': 'predictor-corrector',
            r'\\text{step size}': 'step size',
            r'\\text{truncation error}': 'truncation error',
            r'\\text{round-off error}': 'round-off error',
            r'\\text{stiff}': 'stiff',
            r'\\text{stability region}': 'stability region',
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements for ODEs"""
        patterns = [
            # General ODE statements
            (r'is\s+an?\s+ODE\s+of\s+order\s+([0-9]+)',
             lambda m: f'is an O D E of order {self._number_name(m.group(1))}'),
            (r'([0-9]+)(?:st|nd|rd|th)-order\s+ODE',
             lambda m: f'{self._ordinal(m.group(1))}-order O D E'),
            (r'the\s+ODE\s+has\s+a\s+unique\s+solution',
             'the O D E has a unique solution'),
            
            # Solution descriptions
            (r'y\s*=\s*y\(x\)\s+is\s+a\s+solution',
             'y equals y of x is a solution'),
            (r'the\s+general\s+solution\s+is',
             'the general solution is'),
            (r'the\s+particular\s+solution\s+is',
             'the particular solution is'),
            (r'satisfies\s+the\s+initial\s+conditions',
             'satisfies the initial conditions'),
            (r'satisfies\s+the\s+boundary\s+conditions',
             'satisfies the boundary conditions'),
            
            # Method descriptions
            (r'solve\s+by\s+separation\s+of\s+variables',
             'solve by separation of variables'),
            (r'using\s+an\s+integrating\s+factor',
             'using an integrating factor'),
            (r'by\s+the\s+method\s+of\s+undetermined\s+coefficients',
             'by the method of undetermined coefficients'),
            (r'using\s+variation\s+of\s+parameters',
             'using variation of parameters'),
            (r'apply\s+the\s+Laplace\s+transform',
             'apply the Laplace transform'),
            
            # Equation types
            (r'is\s+a\s+linear\s+equation',
             'is a linear equation'),
            (r'is\s+a\s+nonlinear\s+equation',
             'is a nonlinear equation'),
            (r'is\s+separable',
             'is separable'),
            (r'is\s+exact',
             'is exact'),
            (r'is\s+a\s+Bernoulli\s+equation',
             'is a Bernoulli equation'),
            (r'is\s+a\s+Riccati\s+equation',
             'is a Riccati equation'),
            
            # Characteristic equation
            (r'the\s+characteristic\s+equation\s+is\s*r\^2\s*\+\s*([0-9]+)r\s*\+\s*([0-9]+)\s*=\s*0',
             lambda m: f'the characteristic equation is r squared plus {m.group(1)} r plus {m.group(2)} equals zero'),
            (r'has\s+roots\s*r_1\s*=\s*([0-9]+)\s*,\s*r_2\s*=\s*([0-9]+)',
             lambda m: f'has roots r 1 equals {m.group(1)}, r 2 equals {m.group(2)}'),
            (r'has\s+repeated\s+root\s*r\s*=\s*([0-9]+)',
             lambda m: f'has repeated root r equals {m.group(1)}'),
            (r'has\s+complex\s+roots',
             'has complex roots'),
            
            # Series solutions
            (r'has\s+a\s+power\s+series\s+solution',
             'has a power series solution'),
            (r'x\s*=\s*0\s+is\s+an?\s+ordinary\s+point',
             'x equals 0 is an ordinary point'),
            (r'x\s*=\s*0\s+is\s+a\s+regular\s+singular\s+point',
             'x equals 0 is a regular singular point'),
            (r'use\s+the\s+Frobenius\s+method',
             'use the Frobenius method'),
            
            # Stability
            (r'the\s+equilibrium\s+is\s+stable',
             'the equilibrium is stable'),
            (r'the\s+equilibrium\s+is\s+unstable',
             'the equilibrium is unstable'),
            (r'is\s+asymptotically\s+stable',
             'is asymptotically stable'),
            (r'has\s+a\s+stable\s+node\s+at',
             'has a stable node at'),
            (r'has\s+a\s+saddle\s+point\s+at',
             'has a saddle point at'),
            (r'has\s+a\s+center\s+at',
             'has a center at'),
            
            # Systems
            (r'the\s+system\s+has\s+eigenvalues',
             'the system has eigenvalues'),
            (r'the\s+fundamental\s+matrix\s+is',
             'the fundamental matrix is'),
            (r'is\s+a\s+homogeneous\s+system',
             'is a homogeneous system'),
            (r'is\s+a\s+non-homogeneous\s+system',
             'is a non-homogeneous system'),
            
            # Existence and uniqueness
            (r'satisfies\s+the\s+Lipschitz\s+condition',
             'satisfies the Lipschitz condition'),
            (r'by\s+the\s+existence\s+and\s+uniqueness\s+theorem',
             'by the existence and uniqueness theorem'),
            (r'has\s+a\s+unique\s+solution\s+on',
             'has a unique solution on'),
            
            # Numerical methods
            (r'using\s+Euler\'s\s+method\s+with\s+step\s+size\s*h\s*=\s*([0-9.]+)',
             lambda m: f'using Euler\'s method with step size h equals {m.group(1)}'),
            (r'apply\s+the\s+Runge-Kutta\s+method',
             'apply the Runge-Kutta method'),
            (r'the\s+truncation\s+error\s+is\s+O\(h\^([0-9]+)\)',
             lambda m: f'the truncation error is O of h to the {self._ordinal(m.group(1))}'),
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
        # Basic processing for nested content
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
            (r'\\to', 'to'),
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
# Main ODE Processor
# ===========================

class ODEProcessor:
    """Main processor for ordinary differential equations domain"""
    
    def __init__(self):
        self.vocabulary = ODEVocabulary()
        self.context = ODEContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_definitions': True,
            'expand_abbreviations': True,
            'add_clarifications': True,
        }
        
        logger.info("ODE processor initialized with complete vocabulary")
    
    def detect_subcontext(self, text: str) -> ODEContext:
        """Detect specific ODE subcontext"""
        text_lower = text.lower()
        
        # Check for Laplace transforms
        if any(term in text_lower for term in ['laplace', 'transform', '\\mathcal{l}']):
            return ODEContext.LAPLACE
        
        # Check for systems
        if any(term in text_lower for term in ['system', 'matrix', 'eigenvalue', 'eigenvector']):
            return ODEContext.SYSTEMS
        
        # Check for numerical methods
        if any(term in text_lower for term in ['euler', 'runge-kutta', 'adams', 'numerical']):
            return ODEContext.NUMERICAL
        
        # Check for qualitative/dynamical
        if any(term in text_lower for term in ['phase', 'stability', 'equilibrium', 'bifurcation', 'lyapunov']):
            return ODEContext.QUALITATIVE
        
        # Check for series solutions
        if any(term in text_lower for term in ['series', 'frobenius', 'bessel', 'legendre']):
            return ODEContext.SERIES_SOLUTIONS
        
        # Check for second-order
        if any(term in text_lower for term in ['second order', 'second-order', "y''", 'characteristic equation']):
            return ODEContext.SECOND_ORDER
        
        # Check for first-order
        if any(term in text_lower for term in ['first order', 'first-order', "y'", 'separable', 'exact', 'linear']):
            return ODEContext.FIRST_ORDER
        
        # Check for higher-order
        if any(term in text_lower for term in ['higher order', 'higher-order', 'third order', 'fourth order']):
            return ODEContext.HIGHER_ORDER
        
        # Default to basic ODE
        if any(term in text_lower for term in ['ode', 'differential equation', 'ivp', 'bvp']):
            return ODEContext.BASIC_ODE
        
        return ODEContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process ODE text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"ODE subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special ODE rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process ODE text"""
        # Normalize common variations
        normalizations = [
            (r'diff\.\s*eq\.', 'differential equation'),
            (r'DE\b', 'differential equation'),
            (r'ODE\b', 'O D E'),
            (r'PDE\b', 'P D E'),
            (r'IVP\b', 'initial value problem'),
            (r'BVP\b', 'boundary value problem'),
            (r'char\.\s*eq\.', 'characteristic equation'),
            (r'gen\.\s*sol\.', 'general solution'),
            (r'part\.\s*sol\.', 'particular solution'),
            (r'homo\.\s*', 'homogeneous '),
            (r'non-homo\.\s*', 'non-homogeneous '),
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply ODE vocabulary replacements"""
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
        """Apply special ODE-specific rules"""
        
        # Add clarifications for potentially ambiguous terms
        if self.special_rules['add_clarifications']:
            clarifications = [
                (r'\border\b(?!\s+of|\s+equation)', 'order'),
                (r'\bdegree\b(?!\s+of|\s+equation)', 'degree'),
                (r'\blinear\b(?!\s+equation|\s+ODE)', 'linear'),
                (r'\bhomogeneous\b(?!\s+equation|\s+ODE)', 'homogeneous'),
            ]
            
            for pattern, term in clarifications:
                # Check context to avoid over-clarification
                if self.context in [ODEContext.BASIC_ODE, ODEContext.FIRST_ORDER, ODEContext.SECOND_ORDER]:
                    text = re.sub(pattern, f"{term}", text)
        
        # Emphasize key theorems and methods
        theorem_patterns = [
            (r'Picard-Lindel�f\s+theorem', 'the Picard-Lindel�f theorem'),
            (r'Cauchy-Lipschitz\s+theorem', 'the Cauchy-Lipschitz theorem'),
            (r'Peano\s+existence\s+theorem', 'the Peano existence theorem'),
            (r'Sturm-Liouville\s+theory', 'Sturm-Liouville theory'),
            (r'Floquet\s+theory', 'Floquet theory'),
            (r'Poincar�-Bendixson\s+theorem', 'the Poincar�-Bendixson theorem'),
            (r'Hartman-Grobman\s+theorem', 'the Hartman-Grobman theorem'),
            (r'stable\s+manifold\s+theorem', 'the stable manifold theorem'),
        ]
        
        for pattern, replacement in theorem_patterns:
            text = re.sub(pattern, f"{{EMPHASIS}}{replacement}{{/EMPHASIS}}", text, flags=re.IGNORECASE)
        
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
            'domain': 'ode',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_ode_processor():
    """Comprehensive test of ODE processor"""
    processor = ODEProcessor()
    
    test_cases = [
        # Basic ODEs
        "Consider the ODE $\\frac{dy}{dx} = f(x,y)$ with initial condition $y(x_0) = y_0$.",
        "The second-order ODE $y'' + p(x)y' + q(x)y = 0$ is homogeneous.",
        "For the BVP $y'' = f(x)$ with $y(a) = \\alpha$, $y(b) = \\beta$.",
        
        # First-order ODEs
        "The equation $\\frac{dy}{dx} = g(x)h(y)$ is separable.",
        "Solve $y' + P(x)y = Q(x)$ using integrating factor $\\mu(x) = e^{\\int P(x)dx}$.",
        "$M(x,y)dx + N(x,y)dy = 0$ is exact if $\\frac{\\partial M}{\\partial y} = \\frac{\\partial N}{\\partial x}$.",
        "The Bernoulli equation $y' + P(x)y = Q(x)y^n$ becomes linear after substitution.",
        
        # Second-order linear ODEs
        "For $ay'' + by' + cy = 0$, the characteristic equation is $ar^2 + br + c = 0$.",
        "When $r = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$, we have distinct real roots.",
        "The general solution is $y = c_1 e^{r_1 x} + c_2 e^{r_2 x}$ for distinct roots.",
        "For complex roots $r = \\alpha \\pm i\\beta$: $y = e^{\\alpha x}(c_1 \\cos \\beta x + c_2 \\sin \\beta x)$.",
        
        # Series solutions
        "Near ordinary point $x_0$, seek $y = \\sum_{n=0}^{\\infty} a_n (x-x_0)^n$.",
        "For regular singular point, use Frobenius: $y = x^r \\sum_{n=0}^{\\infty} a_n x^n$.",
        "Bessel's equation: $x^2y'' + xy' + (x^2 - \\nu^2)y = 0$ has solutions $J_\\nu(x)$, $Y_\\nu(x)$.",
        
        # Laplace transforms
        "$\\mathcal{L}\\{f(t)\\} = F(s) = \\int_0^\\infty e^{-st} f(t) dt$ defines the transform.",
        "$\\mathcal{L}\\{f''(t)\\} = s^2F(s) - sf(0) - f'(0)$ for derivatives.",
        "The shifted function: $\\mathcal{L}\\{u(t-a)f(t-a)\\} = e^{-as}F(s)$.",
        
        # Systems of ODEs
        "The system $\\mathbf{x}' = \\mathbf{A}\\mathbf{x}$ has solution $\\mathbf{x}(t) = e^{\\mathbf{A}t}\\mathbf{x}_0$.",
        "Find eigenvalues from $\\det(\\mathbf{A} - \\lambda \\mathbf{I}) = 0$.",
        "The fundamental matrix $\\mathbf{\\Phi}(t)$ satisfies $\\mathbf{\\Phi}'(t) = \\mathbf{A}\\mathbf{\\Phi}(t)$.",
        
        # Qualitative theory
        "The equilibrium $(x^*, y^*)$ is stable if all eigenvalues have negative real parts.",
        "Phase portrait shows a saddle point when eigenvalues have opposite signs.",
        "By Lyapunov's theorem, if $V(\\mathbf{x}) > 0$ and $\\dot{V} \\leq 0$, equilibrium is stable.",
        
        # Numerical methods
        "Euler's method: $y_{n+1} = y_n + hf(x_n,y_n)$ with step size $h$.",
        "RK4 has truncation error $O(h^5)$ per step.",
        "For stiff equations, use implicit methods for stability.",
        
        # Complex examples
        "The Riccati equation $y' = P(x)y^2 + Q(x)y + R(x)$ becomes linear if particular solution known.",
        "Van der Pol oscillator: $\\ddot{x} - \\mu(1-x^2)\\dot{x} + x = 0$ exhibits limit cycles.",
    ]
    
    print("Testing ODE Processor")
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
    test_ode_processor()