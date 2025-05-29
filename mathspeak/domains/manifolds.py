#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manifolds and Differential Geometry Domain Processor for Mathematical Text-to-Speech
===================================================================================

Complete processor for differential geometry and manifolds notation including:
- Differentiable manifolds, charts, and atlases
- Tangent and cotangent spaces and bundles
- Vector fields and Lie brackets
- Differential forms and exterior calculus
- Connections and covariant derivatives
- Lie groups and Lie algebras
- Riemannian geometry basics
- Curvature tensors and geodesics

This processor handles ALL differential geometry notation with professor-quality pronunciation.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Manifolds Context Types
# ===========================

class ManifoldsContext(Enum):
    """Specific manifolds and differential geometry contexts"""
    BASIC_MANIFOLDS = "basic_manifolds"
    TANGENT_BUNDLES = "tangent_bundles"
    VECTOR_FIELDS = "vector_fields"
    DIFFERENTIAL_FORMS = "differential_forms"
    LIE_THEORY = "lie_theory"
    RIEMANNIAN = "riemannian"
    CONNECTIONS = "connections"
    GENERAL = "general"

@dataclass
class ManifoldsTerm:
    """Represents a manifolds term with pronunciation hints"""
    latex: str
    spoken: str
    context: ManifoldsContext
    emphasis: bool = False
    add_article: bool = True  # Whether to add "the" before term

# ===========================
# Comprehensive Manifolds Vocabulary
# ===========================

class ManifoldsVocabulary:
    """Complete manifolds and differential geometry vocabulary with natural pronunciations"""
    
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
        """Build comprehensive manifolds vocabulary"""
        vocab = {}
        
        # ===== BASIC MANIFOLDS AND STRUCTURES =====
        
        # Manifolds and spaces - NO single letter patterns!
        vocab.update({
            r'\\mathcal{M}': 'the manifold script M',
            r'\\mathcal{N}': 'the manifold script N',
            r'M\^n': 'the n-manifold M',
            r'M\^([0-9]+)': lambda m: f"the {self._number_name(m.group(1))}-manifold M",
            r'\(M,g\)': 'the Riemannian manifold M with metric g',
            r'\(M,\\omega\)': 'the symplectic manifold M with form omega',
            r'\(M,J\)': 'the complex manifold M with complex structure J',
            r'\\partial M': 'the boundary of M',
            r'\\text{Int}\(M\)': 'the interior of M',
            r'\\text{int}\(M\)': 'the interior of M',
        })
        
        # Charts and atlases
        vocab.update({
            r'\(U,\\phi\)': 'the chart U phi',
            r'\(U,\\varphi\)': 'the chart U varphi',
            r'\(U_\\alpha,\\phi_\\alpha\)': 'the chart U alpha phi alpha',
            r'\\{\(U_\\alpha,\\phi_\\alpha\)\\}': 'the atlas with charts U alpha phi alpha',
            r'\\mathcal{A}': 'the atlas script A',
            r'\\phi: U \\to \\mathbb{R}\^n': 'phi from U to R n',
            r'\\phi \\circ \\psi\^{-1}': 'phi composed with psi inverse',
            r'\\text{id}_U': 'the identity on U',
            r'C\^\\infty': 'C infinity',
            r'C\^k': 'C k',
            r'C\^([0-9]+)': lambda m: f"C {self._number_name(m.group(1))}",
            r'\\text{Diff}\(M\)': 'the diffeomorphism group of M',
            r'\\text{Diff}\^r\(M\)': 'the C r diffeomorphism group of M',
        })
        
        # Smooth maps
        vocab.update({
            r'f: M \\to N': 'f from M to N',
            r'F: M \\to N': 'F from M to N',
            r'\\text{smooth}': 'smooth',
            r'f \\in C\^\\infty\(M,N\)': 'f in C infinity from M to N',
            r'C\^\\infty\(M\)': 'C infinity of M',
            r'C\^\\infty\(M,N\)': 'C infinity from M to N',
            r'\\text{Hom}\(M,N\)': 'the smooth maps from M to N',
            r'f_\\*': 'f star',
            r'f\^\\*': 'f superscript star',
            r'\\text{rank}\(f\)': 'the rank of f',
            r'\\text{crit}\(f\)': 'the critical points of f',
            r'\\text{Crit}\(f\)': 'the critical set of f',
        })
        
        # ===== TANGENT AND COTANGENT SPACES =====
        
        # Tangent spaces
        vocab.update({
            r'T_p M': 'the tangent space to M at p',
            r'T_p': 'T sub p',
            r'TM': 'the tangent bundle of M',
            r'T M': 'the tangent bundle of M',
            r'T\\*M': 'the cotangent bundle of M',
            r'T\^\\* M': 'the cotangent bundle of M',
            r'T_p\\* M': 'the cotangent space to M at p',
            r'T\^\\*_p M': 'the cotangent space to M at p',
            r'\\pi: TM \\to M': 'the projection pi from T M to M',
            r'\\pi: T\\*M \\to M': 'the projection pi from T star M to M',
            r'T\^{\(r,s\)}M': 'the r s tensor bundle of M',
            r'T\^r_s M': 'the r s tensor bundle of M',
            r'\\Lambda\^k T\\*M': 'the k-th exterior power of T star M',
            r'\\Lambda\^k T_p\\* M': 'the k-th exterior power of T star p M',
            r'\\text{End}\(TM\)': 'the endomorphism bundle of T M',
        })
        
        # Tangent vectors and differentials
        vocab.update({
            r'v \\in T_p M': 'v in the tangent space to M at p',
            r'X_p': 'X at p',
            r'\\frac{\\partial}{\\partial x\^i}': 'partial over partial x i',
            r'\\partial_i': 'partial i',
            r'\\partial_{x\^i}': 'partial x i',
            r'dx\^i': 'd x i',
            r'df': 'the differential of f',
            r'd_p f': 'the differential of f at p',
            r'df_p': 'the differential of f at p',
            r'\(df\)_p': 'the differential of f at p',
            r'f_{\\*p}': 'f star at p',
            r'f_{\\*}': 'f star',
            r'\\text{ker}\(df_p\)': 'the kernel of d f at p',
        })
        
        # ===== VECTOR FIELDS =====
        
        vocab.update({
            # Remove single letter patterns X, Y, Z
            r'\\mathfrak{X}\(M\)': 'the vector fields on M',
            r'\\Gamma\(TM\)': 'the sections of T M',
            r'X \\in \\mathfrak{X}\(M\)': 'X in the vector fields on M',
            r'\\[X,Y\\]': 'the Lie bracket of X and Y',
            r'\\mathcal{L}_X Y': 'the Lie derivative of Y along X',
            r'\\mathcal{L}_X': 'the Lie derivative along X',
            r'\\phi_t': 'phi sub t',
            r'\\phi\^X_t': 'the flow of X at time t',
            r'\\text{exp}\(tX\)': 'the exponential of t X',
            r'\\text{div}\(X\)': 'the divergence of X',
            r'\\text{curl}\(X\)': 'the curl of X',
            r'X\^\\flat': 'X flat',
            r'\\omega\^\\sharp': 'omega sharp',
        })
        
        # Local expressions
        vocab.update({
            r'X = \\sum X\^i \\frac{\\partial}{\\partial x\^i}': 'X equals sum X i partial over partial x i',
            r'X = X\^i \\partial_i': 'X equals X i partial i',
            r'X\^i': 'X superscript i',
            r'X_i': 'X subscript i',
            r'\\{\\partial_i\\}': 'the coordinate basis partial i',
            r'\\{dx\^i\\}': 'the dual basis d x i',
        })
        
        # ===== DIFFERENTIAL FORMS =====
        
        # Basic forms
        vocab.update({
            r'\\omega': 'omega',
            r'\\alpha': 'alpha',
            r'\\beta': 'beta',
            r'\\eta': 'eta',
            r'\\theta': 'theta',
            r'\\Omega\^k\(M\)': 'the k-forms on M',
            r'\\Omega\^\\*\(M\)': 'the differential forms on M',
            r'\\omega \\in \\Omega\^k\(M\)': 'omega in the k-forms on M',
            r'dx\^i \\wedge dx\^j': 'd x i wedge d x j',
            r'\\wedge': 'wedge',
            r'\\omega \\wedge \\eta': 'omega wedge eta',
            r'\\iota_X \\omega': 'the interior product of X and omega',
            r'i_X \\omega': 'the interior product of X and omega',
            r'X \\lrcorner \\omega': 'X contracted with omega',
        })
        
        # Exterior derivative
        vocab.update({
            r'd\\omega': 'the exterior derivative of omega',
            r'd: \\Omega\^k \\to \\Omega\^{k\+1}': 'd from k-forms to k plus 1 forms',
            r'd\^2 = 0': 'd squared equals zero',
            r'\\text{ker}\(d\)': 'the kernel of d',
            r'\\text{im}\(d\)': 'the image of d',
            r'H\^k_{dR}\(M\)': 'the k-th de Rham cohomology of M',
            r'H\^\\*_{dR}\(M\)': 'the de Rham cohomology of M',
            r'\\[\\omega\\]': 'the cohomology class of omega',
            r'\\text{exact}': 'exact',
            r'\\text{closed}': 'closed',
            r'd\\omega = 0': 'd omega equals zero',
        })
        
        # Integration
        vocab.update({
            r'\\int_M \\omega': 'the integral of omega over M',
            r'\\int_C \\omega': 'the integral of omega over C',
            r'\\int_{\\partial M} \\omega': 'the integral of omega over the boundary of M',
            r'\\text{vol}_M': 'the volume form on M',
            r'dV': 'the volume element',
            r'dS': 'the surface element',
            r'\\text{Stokes}': 'Stokes',
            r'\\oint': 'the contour integral',
        })
        
        # ===== LIE GROUPS AND ALGEBRAS =====
        
        # Lie groups - Remove single G, H
        vocab.update({
            r'GL\(n,\\mathbb{R}\)': 'G L n R',
            r'SL\(n,\\mathbb{R}\)': 'S L n R',
            r'O\(n\)': 'O n',
            r'SO\(n\)': 'S O n',
            r'U\(n\)': 'U n',
            r'SU\(n\)': 'S U n',
            r'Sp\(2n,\\mathbb{R}\)': 'S p 2n R',
            r'\\text{Lie}\(G\)': 'the Lie algebra of G',
            r'T_e G': 'the tangent space to G at the identity',
            r'L_g': 'left translation by g',
            r'R_g': 'right translation by g',
            r'\\text{Ad}_g': 'the adjoint action of g',
            r'\\text{ad}_X': 'the adjoint representation of X',
        })
        
        # Lie algebras
        vocab.update({
            r'\\mathfrak{g}': 'the Lie algebra fraktur g',
            r'\\mathfrak{h}': 'the Lie algebra fraktur h',
            r'\\mathfrak{gl}\(n,\\mathbb{R}\)': 'fraktur g l n R',
            r'\\mathfrak{sl}\(n,\\mathbb{R}\)': 'fraktur s l n R',
            r'\\mathfrak{so}\(n\)': 'fraktur s o n',
            r'\\mathfrak{su}\(n\)': 'fraktur s u n',
            r'\\mathfrak{sp}\(2n,\\mathbb{R}\)': 'fraktur s p 2n R',
            r'\\[\\cdot,\\cdot\\]': 'the Lie bracket',
            r'\\text{Jac}\(X,Y,Z\)': 'the Jacobi identity of X Y Z',
            r'\\exp: \\mathfrak{g} \\to G': 'the exponential map from fraktur g to G',
            r'\\log: G \\to \\mathfrak{g}': 'the logarithm from G to fraktur g',
        })
        
        # ===== CONNECTIONS AND COVARIANT DERIVATIVES =====
        
        # Connections
        vocab.update({
            r'\\nabla': 'nabla',
            r'\\nabla_X Y': 'nabla X Y',
            r'\\nabla_X': 'nabla X',
            r'D_X Y': 'D sub X of Y',
            r'\\Gamma\^k_{ij}': 'Gamma k i j',
            r'\\Gamma': 'the Christoffel symbols',
            r'\\nabla_i': 'nabla i',
            r'\\nabla_{\\partial_i}': 'nabla partial i',
            r'\\text{Levi-Civita}': 'Levi-Civita',
            r'\\nabla\^{LC}': 'the Levi-Civita connection',
            r'\\nabla\^g': 'the metric connection',
            r'T\(X,Y\)': 'the torsion of X and Y',
            r'T\^\\nabla': 'the torsion tensor',
        })
        
        # Parallel transport
        vocab.update({
            r'P_\\gamma': 'the parallel transport along gamma',
            r'P_{s,t}': 'the parallel transport from s to t',
            r'\\tau_\\gamma': 'the parallel transport along gamma',
            r'\\frac{D}{dt}': 'D over d t',
            r'\\frac{DX}{dt} = 0': 'D X over d t equals zero',
            r'\\text{Hol}\(\\nabla\)': 'the holonomy group of nabla',
            r'\\text{Hol}_p\(\\nabla\)': 'the holonomy group of nabla at p',
        })
        
        # ===== RIEMANNIAN GEOMETRY =====
        
        # Metrics - Remove single g
        vocab.update({
            r'g_{ij}': 'g i j',
            r'g\^{ij}': 'g superscript i j',
            r'\\langle X,Y \\rangle': 'the inner product of X and Y',
            r'g\(X,Y\)': 'g of X and Y',
            r'g_p\(X,Y\)': 'g at p of X and Y',
            r'\\|X\\|': 'the norm of X',
            r'\\|X\\|_g': 'the g-norm of X',
            r'ds\^2': 'd s squared',
            r'ds\^2 = g_{ij} dx\^i dx\^j': 'd s squared equals g i j d x i d x j',
            r'\\text{Riem}\(M\)': 'the space of Riemannian metrics on M',
        })
        
        # Curvature - Remove single R, S, K, H
        vocab.update({
            r'\\text{Riem}': 'the Riemann tensor',
            r'R\(X,Y\)Z': 'R of X Y Z',
            r'R\^i_{jkl}': 'R i j k l',
            r'R_{ijkl}': 'R i j k l',
            r'\\text{Ric}': 'the Ricci tensor',
            r'\\text{Ric}\(X,Y\)': 'Ricci of X and Y',
            r'R_{ij}': 'R i j',
            r'\\text{Scal}': 'the scalar curvature',
            r'K\(\\sigma\)': 'K of the 2-plane sigma',
            r'\\kappa': 'the Gaussian curvature kappa',
        })
        
        # Geodesics
        vocab.update({
            r'\\gamma': 'gamma',
            r'\\gamma\(t\)': 'gamma of t',
            r'\\gamma: \[a,b\] \\to M': 'gamma from the interval a b to M',
            r'\\frac{D}{dt}\\dot{\\gamma} = 0': 'D over d t of gamma dot equals zero',
            r'\\nabla_{\\dot{\\gamma}} \\dot{\\gamma} = 0': 'nabla gamma dot gamma dot equals zero',
            r'\\text{exp}_p': 'the exponential map at p',
            r'\\text{exp}_p\(v\)': 'exp p of v',
            r'\\text{exp}: TM \\to M': 'the exponential map from T M to M',
            r'\\text{inj}\(p\)': 'the injectivity radius at p',
            r'\\text{cut}\(p\)': 'the cut locus of p',
            r'\\text{conj}\(p\)': 'the conjugate locus of p',
            r'd_g\(p,q\)': 'the geodesic distance from p to q',
        })
        
        # ===== SPECIAL STRUCTURES =====
        
        # Symplectic geometry
        vocab.update({
            r'\(M,\\omega\)': 'the symplectic manifold M omega',
            r'd\\omega = 0': 'd omega equals zero',
            r'\\omega\^n \\neq 0': 'omega to the n not equal to zero',
            r'\\{f,g\\}': 'the Poisson bracket of f and g',
            r'X_f': 'the Hamiltonian vector field of f',
            r'\\iota_{X_f} \\omega = df': 'interior product X f omega equals d f',
            r'\\text{Symp}\(M,\\omega\)': 'the symplectomorphism group of M omega',
        })
        
        # Complex structures
        vocab.update({
            r'J\^2 = -\\text{id}': 'J squared equals minus identity',
            r'N_J': 'the Nijenhuis tensor of J',
            r'T\^{1,0}M': 'the 1 0 tangent bundle',
            r'T\^{0,1}M': 'the 0 1 tangent bundle',
            r'\\bar{\\partial}': 'del bar',
            r'\\partial': 'del',
            r'\\partial \+ \\bar{\\partial}': 'del plus del bar',
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements for manifolds"""
        patterns = [
            # Smooth maps
            (r'([f-h])\s*:\s*M\s*\\to\s*N\s+is\s+smooth',
             lambda m: f"{m.group(1)} from M to N is smooth"),
            (r'([f-h])\s*:\s*([A-Z])\s*\\to\s*([A-Z])\s+is\s+a\s+diffeomorphism',
             lambda m: f"{m.group(1)} from {m.group(2)} to {m.group(3)} is a diffeomorphism"),
            
            # Submanifolds
            (r'([A-Z])\s+is\s+a\s+submanifold\s+of\s+([A-Z])',
             lambda m: f"{m.group(1)} is a submanifold of {m.group(2)}"),
            (r'([A-Z])\s+\\subset\s+([A-Z])\s+is\s+an\s+embedded\s+submanifold',
             lambda m: f"{m.group(1)} subset {m.group(2)} is an embedded submanifold"),
            
            # Vector fields
            (r'X\s+is\s+a\s+vector\s+field\s+on\s+M',
             'X is a vector field on M'),
            (r'([X-Z])\s+\\in\s+\\mathfrak{X}\(M\)',
             lambda m: f"{m.group(1)} is a vector field on M"),
            
            # Lie brackets
            (r'\\\[([X-Z]),\s*([X-Z])\\\]\s*=\s*0',
             lambda m: f"the bracket of {m.group(1)} and {m.group(2)} equals zero"),
            (r'\\\[([X-Z]),\s*([X-Z])\\\]\s*=\s*([X-Z])',
             lambda m: f"the bracket of {m.group(1)} and {m.group(2)} equals {m.group(3)}"),
            
            # Differential forms
            (r'\\omega\s+is\s+a\s+([0-9])-form',
             lambda m: f"omega is a {self._number_name(m.group(1))}-form"),
            (r'\\omega\s+is\s+closed',
             'omega is closed'),
            (r'\\omega\s+is\s+exact',
             'omega is exact'),
            
            # Tangent vectors
            (r'v\s+\\in\s+T_p\s*M',
             'v in the tangent space to M at p'),
            (r'([X-Z])_p\s+\\in\s+T_p\s*M',
             lambda m: f"{m.group(1)} at p in the tangent space to M at p"),
            
            # Connections
            (r'\\nabla\s+is\s+a\s+connection\s+on\s+TM',
             'nabla is a connection on T M'),
            (r'\\nabla\s+is\s+the\s+Levi-Civita\s+connection',
             'nabla is the Levi-Civita connection'),
            (r'\\nabla\s+is\s+flat',
             'nabla is flat'),
            (r'\\nabla\s+is\s+torsion-free',
             'nabla is torsion-free'),
            
            # Curvature
            (r'M\s+has\s+constant\s+curvature\s+([0-9]+)',
             lambda m: f"M has constant curvature {m.group(1)}"),
            (r'M\s+has\s+positive\s+curvature',
             'M has positive curvature'),
            (r'M\s+has\s+negative\s+curvature',
             'M has negative curvature'),
            (r'M\s+is\s+flat',
             'M is flat'),
            
            # Geodesics
            (r'\\gamma\s+is\s+a\s+geodesic',
             'gamma is a geodesic'),
            (r'\\gamma:\s*\\\[0,1\\\]\s*\\to\s*M\s+is\s+a\s+geodesic',
             'gamma from zero one to M is a geodesic'),
            
            # Bundle maps
            (r'F:\s*E\s*\\to\s*E\'\s+is\s+a\s+bundle\s+map',
             'F from E to E prime is a bundle map'),
            (r'\\phi:\s*TM\s*\\to\s*TN\s+covers\s+f',
             'phi from T M to T N covers f'),
            
            # Lie groups
            (r'G\s+acts\s+on\s+M',
             'G acts on M'),
            (r'G\s+acts\s+freely\s+on\s+M',
             'G acts freely on M'),
            (r'G\s+acts\s+transitively\s+on\s+M',
             'G acts transitively on M'),
            (r'M\s*=\s*G/H',
             'M equals G mod H'),
            
            # Orientability
            (r'M\s+is\s+orientable',
             'M is orientable'),
            (r'M\s+is\s+oriented',
             'M is oriented'),
            (r'M\s+is\s+non-orientable',
             'M is non-orientable'),
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
# Main Manifolds Processor
# ===========================

class ManifoldsProcessor:
    """Main processor for manifolds and differential geometry domain"""
    
    def __init__(self):
        self.vocabulary = ManifoldsVocabulary()
        self.context = ManifoldsContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_definitions': True,
            'expand_abbreviations': True,
            'add_clarifications': True,
        }
        
        logger.info("Manifolds processor initialized with complete vocabulary")
    
    def detect_subcontext(self, text: str) -> ManifoldsContext:
        """Detect specific manifolds subcontext"""
        text_lower = text.lower()
        
        # Check for Lie theory
        if any(term in text_lower for term in ['lie group', 'lie algebra', 'lie bracket', 'adjoint']):
            return ManifoldsContext.LIE_THEORY
        
        # Check for Riemannian geometry
        if any(term in text_lower for term in ['metric', 'curvature', 'geodesic', 'levi-civita']):
            return ManifoldsContext.RIEMANNIAN
        
        # Check for differential forms
        if any(term in text_lower for term in ['differential form', 'exterior', 'wedge', 'de rham']):
            return ManifoldsContext.DIFFERENTIAL_FORMS
        
        # Check for connections
        if any(term in text_lower for term in ['connection', 'covariant', 'parallel transport', 'christoffel']):
            return ManifoldsContext.CONNECTIONS
        
        # Check for vector fields
        if any(term in text_lower for term in ['vector field', 'lie derivative', 'flow']):
            return ManifoldsContext.VECTOR_FIELDS
        
        # Check for tangent bundles
        if any(term in text_lower for term in ['tangent', 'cotangent', 'bundle']):
            return ManifoldsContext.TANGENT_BUNDLES
        
        # Default to basic manifolds
        if any(term in text_lower for term in ['manifold', 'chart', 'atlas', 'smooth']):
            return ManifoldsContext.BASIC_MANIFOLDS
        
        return ManifoldsContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process manifolds text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"Manifolds subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special manifolds rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process manifolds text"""
        # Normalize common variations
        normalizations = [
            (r'diff\.\s+geom\.', 'differential geometry'),
            (r'mfd\b', 'manifold'),
            (r'diffeo\b', 'diffeomorphism'),
            (r'conn\.\s+', 'connection '),
            (r'curv\.\s+', 'curvature '),
            (r'cov\.\s+der\.', 'covariant derivative'),
            (r'tang\.\s+', 'tangent '),
            (r'vec\.\s+field', 'vector field'),
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply manifolds vocabulary replacements"""
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
        """Apply special manifolds-specific rules"""
        
        # Add clarifications for potentially ambiguous terms
        if self.special_rules['add_clarifications']:
            clarifications = [
                (r'\bsmooth\b(?!\s+map|\s+function)', 'smooth'),
                (r'\bflat\b(?!\s+connection)', 'flat'),
                (r'\bclosed\b(?!\s+form)', 'closed'),
            ]
            
            for pattern, term in clarifications:
                # Check context to avoid over-clarification
                if self.context in [ManifoldsContext.BASIC_MANIFOLDS, ManifoldsContext.DIFFERENTIAL_FORMS]:
                    text = re.sub(pattern, f"{term}", text)
        
        # Emphasize key theorems
        theorem_patterns = [
            (r'Frobenius\'?\s+theorem', 'Frobenius theorem'),
            (r'Darboux\'?\s+theorem', 'Darboux theorem'),
            (r'Poincare\s+lemma', 'the Poincare lemma'),
            (r'Hopf-Rinow\s+theorem', 'the Hopf-Rinow theorem'),
            (r'Gauss-Bonnet\s+theorem', 'the Gauss-Bonnet theorem'),
            (r'Nash\s+embedding\s+theorem', 'the Nash embedding theorem'),
            (r'Whitney\s+embedding\s+theorem', 'the Whitney embedding theorem'),
            (r'Sard\'?s\s+theorem', 'Sard\'s theorem'),
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
            'domain': 'manifolds',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_manifolds_processor():
    """Comprehensive test of manifolds processor"""
    processor = ManifoldsProcessor()
    
    test_cases = [
        # Basic manifolds
        "Let $M$ be a smooth $n$-manifold and $(U,\\phi)$ a chart around $p \\in M$.",
        "The transition function $\\phi \\circ \\psi^{-1}: \\psi(U \\cap V) \\to \\phi(U \\cap V)$ is $C^\\infty$.",
        "A map $f: M \\to N$ is smooth if $\\psi \\circ f \\circ \\phi^{-1}$ is smooth for all charts.",
        
        # Tangent spaces
        "$T_p M$ is the tangent space to $M$ at $p$, with basis $\\{\\frac{\\partial}{\\partial x^i}\\}_{i=1}^n$.",
        "The differential $df_p: T_p M \\to T_{f(p)} N$ is linear.",
        "For $v \\in T_p M$, we have $(f_*)_p(v) = df_p(v)$.",
        
        # Vector fields
        "A vector field $X \\in \\mathfrak{X}(M)$ assigns to each $p \\in M$ a vector $X_p \\in T_p M$.",
        "The Lie bracket $[X,Y] = XY - YX$ measures non-commutativity of vector fields.",
        "The flow $\\phi^X_t$ of $X$ satisfies $\\frac{d}{dt}\\phi^X_t(p) = X_{\\phi^X_t(p)}$.",
        
        # Differential forms
        "$\\omega \\in \\Omega^k(M)$ is a $k$-form, locally $\\omega = \\sum_{I} \\omega_I dx^I$.",
        "The exterior derivative $d: \\Omega^k \\to \\Omega^{k+1}$ satisfies $d^2 = 0$.",
        "$H^k_{dR}(M) = \\ker(d)/\\text{im}(d)$ is the $k$-th de Rham cohomology.",
        
        # Lie groups and algebras
        "For a Lie group $G$, the Lie algebra $\\mathfrak{g} = T_e G$ with bracket $[X,Y]$.",
        "$\\text{Ad}_g: \\mathfrak{g} \\to \\mathfrak{g}$ is the adjoint representation.",
        "The exponential map $\\exp: \\mathfrak{g} \\to G$ satisfies $\\exp(tX) = \\gamma_X(t)$.",
        
        # Connections
        "A connection $\\nabla$ on $TM$ satisfies $\\nabla_{fX}Y = f\\nabla_X Y$.",
        "The Christoffel symbols $\\Gamma^k_{ij}$ define $\\nabla_{\\partial_i} \\partial_j = \\Gamma^k_{ij} \\partial_k$.",
        "Parallel transport $P_\\gamma: T_{\\gamma(0)}M \\to T_{\\gamma(1)}M$ preserves inner products.",
        
        # Riemannian geometry
        "On $(M,g)$, the Levi-Civita connection $\\nabla^g$ is torsion-free and metric.",
        "The curvature tensor $R(X,Y)Z = \\nabla_X \\nabla_Y Z - \\nabla_Y \\nabla_X Z - \\nabla_{[X,Y]}Z$.",
        "A geodesic $\\gamma$ satisfies $\\nabla_{\\dot{\\gamma}} \\dot{\\gamma} = 0$.",
        
        # Complex examples
        "The scalar curvature $S = g^{ij}R_{ij}$ where $R_{ij} = R^k_{ikj}$.",
        "For a symplectic manifold $(M,\\omega)$, $d\\omega = 0$ and $\\omega^n \\neq 0$.",
    ]
    
    print("Testing Manifolds Processor")
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
    test_manifolds_processor()