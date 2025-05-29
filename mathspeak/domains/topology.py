#!/usr/bin/env python3
"""
Topology Domain Processor for Mathematical Text-to-Speech
========================================================

Complete processor for topology notation including:
- Point-set topology with all separation axioms
- Compactness and connectedness variations
- Metric, uniform, and proximity spaces
- Algebraic topology (fundamental groups, homology, cohomology)
- Differential topology and manifolds
- Fiber bundles and covering spaces
- CW complexes and specialized topics

This processor handles ALL topology notation with professor-quality pronunciation.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Topology Context Types
# ===========================

class TopologyContext(Enum):
    """Specific topology contexts for fine-grained processing"""
    POINT_SET = "point_set"
    ALGEBRAIC = "algebraic"
    DIFFERENTIAL = "differential"
    METRIC_SPACES = "metric_spaces"
    GENERAL = "general"

@dataclass
class TopologyTerm:
    """Represents a topology term with pronunciation hints"""
    latex: str
    spoken: str
    context: TopologyContext
    emphasis: bool = False
    add_article: bool = True  # Whether to add "the" before term

# ===========================
# Comprehensive Topology Vocabulary
# ===========================

class TopologyVocabulary:
    """Complete topology vocabulary with natural pronunciations"""
    
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
        """Build comprehensive topology vocabulary"""
        vocab = {}
        
        # ===== POINT-SET TOPOLOGY =====
        
        # Basic structures
        vocab.update({
            r'\\tau': 'tau',
            r'\\mathcal{T}': 'the topology script T',
            r'(X,\\tau)': 'the topological space X with topology tau',
            r'(X,\\mathcal{T})': 'the topological space X with topology script T',
            r'\\mathcal{B}': 'the base script B',
            r'\\mathcal{S}': 'the subbase script S',
            r'\\mathcal{U}': 'the open cover script U',
            r'\\mathcal{N}': 'the neighborhood system script N',
            r'\\mathcal{F}': 'the filter script F',
        })
        
        # Separation axioms (complete T₀ through T₆)
        vocab.update({
            r'T_0': 'T naught',
            r'T_1': 'T one',
            r'T_2': 'T two',
            r'T_\{2\\frac\{1\}\{2\}\}': 'T two and a half',
            r'T_3': 'T three',
            r'T_\{3\\frac\{1\}\{2\}\}': 'T three and a half',
            r'T_4': 'T four',
            r'T_5': 'T five',
            r'T_6': 'T six',
            r'T_0\\text{-space}': 'T naught space',
            r'T_1\\text{-space}': 'T one space',
            r'T_2\\text{-space}': 'Hausdorff space',
            r'\\text{Kolmogorov}': 'Kolmogorov',
            r'\\text{Fréchet}': 'Fréchet',
            r'\\text{Hausdorff}': 'Hausdorff',
            r'\\text{Urysohn}': 'Urysohn',
            r'\\text{regular}': 'regular',
            r'\\text{completely regular}': 'completely regular',
            r'\\text{Tychonoff}': 'Tychonoff',
            r'\\text{normal}': 'normal',
            r'\\text{completely normal}': 'completely normal',
            r'\\text{perfectly normal}': 'perfectly normal',
        })
        
        # Compactness variations
        vocab.update({
            r'\\text{compact}': 'compact',
            r'\\text{sequentially compact}': 'sequentially compact',
            r'\\text{countably compact}': 'countably compact',
            r'\\text{locally compact}': 'locally compact',
            r'\\text{$\\sigma$-compact}': 'sigma-compact',
            r'\\text{Lindelöf}': 'Lindelöf',
            r'\\text{paracompact}': 'paracompact',
            r'\\text{metacompact}': 'metacompact',
            r'\\text{orthocompact}': 'orthocompact',
            r'\\text{pseudocompact}': 'pseudocompact',
            r'\\text{realcompact}': 'realcompact',
            r'\\text{$k$-space}': 'k-space',
            r'\\text{hemicompact}': 'hemicompact',
        })
        
        # Connectedness types
        vocab.update({
            r'\\text{connected}': 'connected',
            r'\\text{path-connected}': 'path-connected',
            r'\\text{arcwise connected}': 'arcwise connected',
            r'\\text{locally connected}': 'locally connected',
            r'\\text{locally path-connected}': 'locally path-connected',
            r'\\text{simply connected}': 'simply connected',
            r'\\text{contractible}': 'contractible',
            r'\\text{totally disconnected}': 'totally disconnected',
            r'\\text{zero-dimensional}': 'zero-dimensional',
            r'\\text{extremally disconnected}': 'extremally disconnected',
            r'\\text{hyperconnected}': 'hyperconnected',
            r'\\text{ultraconnected}': 'ultraconnected',
        })
        
        # Topological operations
        vocab.update({
            r'\\overline{([^}]+)}': lambda m: f"the closure of {self._process_nested(m.group(1))}",
            r'\\bar{([^}]+)}': lambda m: f"the closure of {self._process_nested(m.group(1))}",
            r'\\text{cl}\\(([^)]+)\\)': lambda m: f"the closure of {self._process_nested(m.group(1))}",
            r'\\text{int}\\(([^)]+)\\)': lambda m: f"the interior of {self._process_nested(m.group(1))}",
            r'\\text{Int}\\(([^)]+)\\)': lambda m: f"the interior of {self._process_nested(m.group(1))}",
            r'([^\\s]+)^\\circ': lambda m: f"the interior of {m.group(1)}",
            r'\\partial ([A-Z])': lambda m: f"the boundary of {m.group(1)}",
            r'\\text{bd}\\(([^)]+)\\)': lambda m: f"the boundary of {self._process_nested(m.group(1))}",
            r'\\text{Bd}\\(([^)]+)\\)': lambda m: f"the boundary of {self._process_nested(m.group(1))}",
            r'\\text{fr}\\(([^)]+)\\)': lambda m: f"the frontier of {self._process_nested(m.group(1))}",
            r'([A-Z])\'': lambda m: f"the derived set of {m.group(1)}",
            r'\\text{Lim}\\(([^)]+)\\)': lambda m: f"the limit points of {self._process_nested(m.group(1))}",
            r'\\text{Iso}\\(([^)]+)\\)': lambda m: f"the isolated points of {self._process_nested(m.group(1))}",
        })
        
        # ===== ALGEBRAIC TOPOLOGY =====
        
        # Fundamental groups and homotopy
        vocab.update({
            r'\\pi_0\\(([^)]+)\\)': lambda m: f"pi naught of {self._process_nested(m.group(1))}",
            r'\\pi_1\\(([^)]+)\\)': lambda m: f"the fundamental group of {self._process_nested(m.group(1))}",
            r'\\pi_1\\(([^,]+),([^)]+)\\)': lambda m: f"the fundamental group of {self._process_nested(m.group(1))} based at {self._process_nested(m.group(2))}",
            r'\\pi_n\\(([^)]+)\\)': lambda m: f"the n-th homotopy group of {self._process_nested(m.group(1))}",
            r'\\pi_([0-9]+)\\(([^)]+)\\)': lambda m: f"the {self._ordinal(m.group(1))} homotopy group of {self._process_nested(m.group(2))}",
            r'\\pi_\\*\\(([^)]+)\\)': lambda m: f"the homotopy groups of {self._process_nested(m.group(1))}",
            r'\\Omega X': 'the loop space of X',
            r'\\Omega_x X': 'the based loop space at x in X',
            r'\\text{Map}\\(([^,]+),([^)]+)\\)': lambda m: f"the mapping space from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))}",
            r'\\simeq': 'is homotopy equivalent to',
            r'\\sim': 'is homotopic to',
            r'f \\simeq g': 'f is homotopic to g',
            r'X \\simeq Y': 'X is homotopy equivalent to Y',
        })
        
        # Homology and cohomology
        vocab.update({
            r'H_n\\(([^)]+)\\)': lambda m: f"the n-th homology group of {self._process_nested(m.group(1))}",
            r'H_([0-9]+)\\(([^)]+)\\)': lambda m: f"the {self._ordinal(m.group(1))} homology group of {self._process_nested(m.group(2))}",
            r'H_n\\(([^;]+);([^)]+)\\)': lambda m: f"the n-th homology of {self._process_nested(m.group(1))} with coefficients in {self._process_nested(m.group(2))}",
            r'H^n\\(([^)]+)\\)': lambda m: f"the n-th cohomology group of {self._process_nested(m.group(1))}",
            r'H^([0-9]+)\\(([^)]+)\\)': lambda m: f"the {self._ordinal(m.group(1))} cohomology group of {self._process_nested(m.group(2))}",
            r'\\tilde{H}_n\\(([^)]+)\\)': lambda m: f"the n-th reduced homology of {self._process_nested(m.group(1))}",
            r'\\tilde{H}^n\\(([^)]+)\\)': lambda m: f"the n-th reduced cohomology of {self._process_nested(m.group(1))}",
            r'\\text{Tor}_n': 'Tor n',
            r'\\text{Ext}^n': 'Ext n',
            r'\\chi\\(([^)]+)\\)': lambda m: f"the Euler characteristic of {self._process_nested(m.group(1))}",
            r'\\text{rank}\\(H_n\\(X\\)\\)': 'the rank of the n-th homology of X',
            r'b_n\\(X\\)': 'the n-th Betti number of X',
            r'b_([0-9]+)\\(X\\)': lambda m: f"the {self._ordinal(m.group(1))} Betti number of X",
        })
        
        # Covering spaces
        vocab.update({
            r'\\tilde{([^}]+)}': lambda m: f"tilde {self._process_nested(m.group(1))}",
            r'p\\colon \\tilde{X} \\to X': 'p from tilde X to X',
            r'p: \\tilde{X} \\to X': 'p from tilde X to X',
            r'\\text{Cov}\\(([^)]+)\\)': lambda m: f"the category of covering spaces of {self._process_nested(m.group(1))}",
            r'\\text{Deck}\\(([^)]+)\\)': lambda m: f"the deck transformation group of {self._process_nested(m.group(1))}",
            r'\\text{Aut}\\(([^)]+)\\)': lambda m: f"the automorphism group of {self._process_nested(m.group(1))}",
            r'p^{-1}\\(([^)]+)\\)': lambda m: f"the fiber over {self._process_nested(m.group(1))}",
            r'\\text{ev}_x': 'the evaluation map at x',
            r'\\hat{X}': 'the universal cover of X',
        })
        
        # ===== METRIC AND UNIFORM SPACES =====
        
        vocab.update({
            r'd\\(([^,]+),([^)]+)\\)': lambda m: f"the distance from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))}",
            r'd_X\\(([^,]+),([^)]+)\\)': lambda m: f"the distance in X from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))}",
            r'\\rho\\(([^,]+),([^)]+)\\)': lambda m: f"rho of {self._process_nested(m.group(1))} and {self._process_nested(m.group(2))}",
            r'B\\(([^,]+),([^)]+)\\)': lambda m: f"the open ball centered at {self._process_nested(m.group(1))} with radius {self._process_nested(m.group(2))}",
            r'B_r\\(([^)]+)\\)': lambda m: f"the ball of radius r centered at {self._process_nested(m.group(1))}",
            r'\\overline{B}\\(([^,]+),([^)]+)\\)': lambda m: f"the closed ball centered at {self._process_nested(m.group(1))} with radius {self._process_nested(m.group(2))}",
            r'S\\(([^,]+),([^)]+)\\)': lambda m: f"the sphere centered at {self._process_nested(m.group(1))} with radius {self._process_nested(m.group(2))}",
            r'\\text{diam}\\(([^)]+)\\)': lambda m: f"the diameter of {self._process_nested(m.group(1))}",
            r'\\text{dist}\\(([^,]+),([^)]+)\\)': lambda m: f"the distance from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))}",
            r'\\text{Lip}\\(f\\)': 'the Lipschitz constant of f',
            r'\\text{osc}\\(f,x\\)': 'the oscillation of f at x',
        })
        
        # ===== SPACES AND CONSTRUCTIONS =====
        
        # Products and quotients
        vocab.update({
            r'X \\times Y': 'X cross Y',
            r'\\prod_{i \\in I} X_i': 'the product over i in I of X sub i',
            r'\\prod X_i': 'the product of X sub i',
            r'\\coprod X_i': 'the coproduct of X sub i',
            r'\\bigsqcup X_i': 'the disjoint union of X sub i',
            r'X \\sqcup Y': 'X disjoint union Y',
            r'X/A': 'X mod A',
            r'X/\\sim': 'X mod the equivalence relation',
            r'X \\vee Y': 'X wedge Y',
            r'\\bigvee X_i': 'the wedge sum of X sub i',
            r'X \\cup Y': 'X union Y',
            r'X \\cap Y': 'X intersect Y',
            r'X \\setminus Y': 'X minus Y',
            r'X - Y': 'X minus Y',
            r'X \\subset Y': 'X is a subset of Y',
            r'X \\subseteq Y': 'X is a subset of or equal to Y',
            r'X \\subsetneq Y': 'X is a proper subset of Y',
        })
        
        # Standard spaces
        vocab.update({
            r'\\mathbb{R}': 'the real line',
            r'\\mathbb{R}^n': 'n-dimensional Euclidean space',
            r'\\mathbb{R}^([0-9]+)': lambda m: f"{self._number_name(m.group(1))}-dimensional Euclidean space",
            r'\\mathbb{C}': 'the complex plane',
            r'\\mathbb{C}^n': 'n-dimensional complex space',
            r'\\mathbb{H}': 'the quaternions',
            r'\\mathbb{S}^n': 'the n-sphere',
            r'S^n': 'the n-sphere',
            r'S^([0-9]+)': lambda m: f"the {self._number_name(m.group(1))}-sphere",
            r'D^n': 'the n-disk',
            r'B^n': 'the n-ball',
            r'I': 'the unit interval',
            r'I^n': 'the n-cube',
            r'\\mathbb{T}^n': 'the n-torus',
            r'T^n': 'the n-torus',
            r'\\mathbb{RP}^n': 'real projective n-space',
            r'\\mathbb{CP}^n': 'complex projective n-space',
            r'\\mathbb{HP}^n': 'quaternionic projective n-space',
            r'K(\\pi,n)': 'an Eilenberg-MacLane space of type pi comma n',
            r'K(G,n)': 'an Eilenberg-MacLane space with group G in degree n',
        })
        
        # ===== FIBER BUNDLES AND VECTOR BUNDLES =====
        
        vocab.update({
            r'E \\to B': 'E over B',
            r'\\pi: E \\to B': 'the projection pi from E to B',
            r'E \\xrightarrow{\\pi} B': 'E maps to B via pi',
            r'F \\hookrightarrow E \\to B': 'the fiber bundle with fiber F, total space E, and base B',
            r'\\xi': 'the bundle xi',
            r'\\eta': 'the bundle eta',
            r'TM': 'the tangent bundle of M',
            r'T\\*M': 'the cotangent bundle of M',
            r'T_p M': 'the tangent space to M at p',
            r'T\\*_p M': 'the cotangent space to M at p',
            r'\\Lambda^k T\\*M': 'the k-th exterior power of the cotangent bundle',
            r'\\text{rank}\\(\\xi\\)': 'the rank of the bundle xi',
            r'\\gamma^n': 'the universal n-plane bundle',
            r'\\text{Vect}_n\\(X\\)': 'the set of n-dimensional vector bundles over X',
            r'\\text{Prin}_G\\(X\\)': 'the set of principal G-bundles over X',
        })
        
        # ===== CW COMPLEXES =====
        
        vocab.update({
            r'X^{\\(n\\)}': 'the n-skeleton of X',
            r'X^n': 'X to the n',  # Context-dependent
            r'e^n': 'an n-cell',
            r'e^n_\\alpha': 'the n-cell e alpha',
            r'\\text{sk}_n\\(X\\)': 'the n-skeleton of X',
            r'\\phi_\\alpha: S^{n-1} \\to X^{\\(n-1\\)}': 'the attaching map phi alpha from the n minus 1 sphere to the n minus 1 skeleton',
            r'X \\cup_f e^n': 'X with an n-cell attached via f',
            r'\\text{CW}': 'CW',
            r'\\Delta^n': 'the standard n-simplex',
            r'\\partial \\Delta^n': 'the boundary of the n-simplex',
        })
        
        # ===== SPECIAL NOTATION =====
        
        vocab.update({
            r'\\cong': 'is isomorphic to',
            r'\\approx': 'is homeomorphic to',
            r'\\equiv': 'is equivalent to',
            r'\\hookrightarrow': 'embeds into',
            r'\\twoheadrightarrow': 'surjects onto',
            r'\\xrightarrow{f}': 'maps via f to',
            r'\\xleftarrow{g}': 'receives via g from',
            r'f_\\*': 'f subscript star',
            r'f^\\*': 'f superscript star',
            r'f_!': 'f shriek',
            r'f^!': 'f upper shriek',
            r'\\text{id}': 'the identity',
            r'\\text{Id}': 'the identity',
            r'1_X': 'the identity on X',
            r'\\text{incl}': 'the inclusion',
            r'\\iota': 'iota',
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements"""
        patterns = [
            # Continuous functions
            (r'f\s*:\s*X\s*\\to\s*Y\s+is\s+continuous',
             'f from X to Y is continuous'),
            (r'([f-h])\s*:\s*([A-Z])\s*\\to\s*([A-Z])\s+is\s+continuous',
             lambda m: f"{m.group(1)} from {m.group(2)} to {m.group(3)} is continuous"),
            
            # Open/closed sets
            (r'([A-Z])\s+is\s+open\s+in\s+([A-Z])',
             lambda m: f"{m.group(1)} is open in {m.group(2)}"),
            (r'([A-Z])\s+is\s+closed\s+in\s+([A-Z])',
             lambda m: f"{m.group(1)} is closed in {m.group(2)}"),
            (r'([A-Z])\s+is\s+clopen',
             lambda m: f"{m.group(1)} is clopen"),
            
            # Neighborhoods
            (r'([A-Z])\s+is\s+a\s+neighborhood\s+of\s+([a-z])',
             lambda m: f"{m.group(1)} is a neighborhood of {m.group(2)}"),
            (r'\\mathcal{N}\\(([^)]+)\\)',
             lambda m: f"the neighborhood system of {self._process_nested(m.group(1))}"),
            
            # Density
            (r'([A-Z])\s+is\s+dense\s+in\s+([A-Z])',
             lambda m: f"{m.group(1)} is dense in {m.group(2)}"),
            (r'([A-Z])\s+is\s+nowhere\s+dense',
             lambda m: f"{m.group(1)} is nowhere dense"),
            
            # Convergence
            (r'([a-z])_n\s*\\to\s*([a-z])',
             lambda m: f"{m.group(1)} sub n converges to {m.group(2)}"),
            (r'\\{([a-z])_n\\}\s*\\to\s*([a-z])',
             lambda m: f"the sequence {m.group(1)} sub n converges to {m.group(2)}"),
            
            # Quotient maps
            (r'q\s*:\s*X\s*\\to\s*X/\\sim',
             'q from X to X mod the equivalence relation'),
            (r'the\s+quotient\s+map\s+q\s*:\s*X\s*\\to\s*Y',
             'the quotient map q from X to Y'),
            
            # Homotopies
            (r'F\s*:\s*X\s*\\times\s*I\s*\\to\s*Y',
             'F from X cross I to Y'),
            (r'H\s*:\s*([A-Z])\s*\\times\s*I\s*\\to\s*([A-Z])',
             lambda m: f"H from {m.group(1)} cross I to {m.group(2)}"),
            
            # Retractions
            (r'r\s*:\s*X\s*\\to\s*A\s+is\s+a\s+retraction',
             'r from X to A is a retraction'),
            (r'([A-Z])\s+is\s+a\s+retract\s+of\s+([A-Z])',
             lambda m: f"{m.group(1)} is a retract of {m.group(2)}"),
            (r'([A-Z])\s+is\s+a\s+deformation\s+retract\s+of\s+([A-Z])',
             lambda m: f"{m.group(1)} is a deformation retract of {m.group(2)}"),
            
            # Fibrations and cofibrations
            (r'p\s*:\s*E\s*\\to\s*B\s+is\s+a\s+fibration',
             'p from E to B is a fibration'),
            (r'i\s*:\s*A\s*\\to\s*X\s+is\s+a\s+cofibration',
             'i from A to X is a cofibration'),
            
            # Group actions
            (r'G\s+acts\s+on\s+X',
             'G acts on X'),
            (r'G\s*\\times\s*X\s*\\to\s*X',
             'G cross X to X'),
            (r'the\s+orbit\s+space\s+X/G',
             'the orbit space X mod G'),
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
# Main Topology Processor
# ===========================

class TopologyProcessor:
    """Main processor for topology domain"""
    
    def __init__(self):
        self.vocabulary = TopologyVocabulary()
        self.context = TopologyContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_definitions': True,
            'expand_abbreviations': True,
            'add_clarifications': True,
        }
        
        logger.info("Topology processor initialized with complete vocabulary")
    
    def detect_subcontext(self, text: str) -> TopologyContext:
        """Detect specific topology subcontext"""
        text_lower = text.lower()
        
        # Check for algebraic topology
        if any(term in text_lower for term in ['fundamental group', 'homology', 'homotopy', 'covering space']):
            return TopologyContext.ALGEBRAIC
        
        # Check for differential topology
        if any(term in text_lower for term in ['manifold', 'tangent', 'smooth', 'differential']):
            return TopologyContext.DIFFERENTIAL
        
        # Check for metric spaces
        if any(term in text_lower for term in ['metric', 'distance', 'cauchy', 'complete']):
            return TopologyContext.METRIC_SPACES
        
        # Default to point-set
        if any(term in text_lower for term in ['open', 'closed', 'compact', 'hausdorff']):
            return TopologyContext.POINT_SET
        
        return TopologyContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process topology text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"Topology subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special topology rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process topology text"""
        # Normalize common variations
        normalizations = [
            (r'top\.\s+space', 'topological space'),
            (r'cts\.\s+', 'continuous '),
            (r'nbd\b', 'neighborhood'),
            (r'nbhd\b', 'neighborhood'),
            (r'cpt\b', 'compact'),
            (r'conn\.\s+', 'connected '),
            (r'homeo\.\s+', 'homeomorphic '),
            (r'equiv\.\s+', 'equivalent '),
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply topology vocabulary replacements"""
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
        """Apply special topology-specific rules"""
        
        # Add clarifications for potentially ambiguous terms
        if self.special_rules['add_clarifications']:
            clarifications = [
                (r'\bcompact\b(?!\s+Hausdorff)', 'compact'),  # Don't repeat if "compact Hausdorff"
                (r'\bnormal\b(?!\s+space)', 'normal'),
                (r'\bregular\b(?!\s+space)', 'regular'),
            ]
            
            for pattern, term in clarifications:
                # Check context to avoid over-clarification
                if self.context == TopologyContext.POINT_SET:
                    text = re.sub(pattern, f"{term}", text)
        
        # Emphasize key theorems
        theorem_patterns = [
            (r'Urysohn\'s\s+Lemma', 'Urysohn\'s Lemma'),
            (r'Tietze\s+Extension\s+Theorem', 'the Tietze Extension Theorem'),
            (r'Tychonoff\'s\s+Theorem', 'Tychonoff\'s Theorem'),
            (r'Stone-Čech\s+compactification', 'the Stone-Čech compactification'),
            (r'Alexandroff\s+compactification', 'the Alexandroff one-point compactification'),
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
            'domain': 'topology',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_topology_processor():
    """Comprehensive test of topology processor"""
    processor = TopologyProcessor()
    
    test_cases = [
        # Point-set topology
        "Let $(X, \\tau)$ be a topological space. A subset $A \\subseteq X$ is closed if $X \\setminus A \\in \\tau$.",
        "A space $X$ is $T_2$ if for any $x \\neq y$, there exist disjoint open sets $U, V$ with $x \\in U$, $y \\in V$.",
        "The closure of $A$ is $\\overline{A} = \\cap\\{C : A \\subseteq C, C \\text{ closed}\\}$.",
        
        # Compactness
        "A space is compact if every open cover has a finite subcover.",
        "Every compact Hausdorff space is normal.",
        "The Tychonoff theorem states that the product of compact spaces is compact.",
        
        # Algebraic topology
        "$\\pi_1(S^1) \\cong \\mathbb{Z}$",
        "For $n \\geq 2$, $\\pi_1(S^n) = 0$, so $S^n$ is simply connected.",
        "The fundamental group $\\pi_1(X \\vee Y, x_0) \\cong \\pi_1(X, x_0) * \\pi_1(Y, y_0)$.",
        
        # Homology
        "$H_n(S^k) \\cong \\mathbb{Z}$ if $n = k$ and $0$ otherwise.",
        "The Euler characteristic is $\\chi(X) = \\sum_{n=0}^{\\infty} (-1)^n b_n(X)$.",
        
        # Covering spaces
        "Let $p: \\tilde{X} \\to X$ be a covering map with $\\tilde{X}$ path-connected.",
        "The deck transformation group $\\text{Deck}(\\tilde{X}/X) \\cong \\pi_1(X)/p_*(\\pi_1(\\tilde{X}))$.",
        
        # Metric spaces
        "In a metric space $(X,d)$, the open ball is $B(x,r) = \\{y \\in X : d(x,y) < r\\}$.",
        "A sequence $\\{x_n\\}$ is Cauchy if $\\forall \\epsilon > 0 \\, \\exists N$ such that $d(x_n, x_m) < \\epsilon$ for $n,m > N$.",
    ]
    
    print("Testing Topology Processor")
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
    test_topology_processor()