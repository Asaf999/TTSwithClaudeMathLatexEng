#!/usr/bin/env python3
"""
Combinatorics Domain Processor for Mathematical Text-to-Speech
============================================================

Complete processor for combinatorics notation including:
- Counting principles (permutations, combinations, arrangements)
- Graph theory (vertices, edges, paths, cycles, trees)
- Generating functions (ordinary and exponential)
- Recurrence relations and sequences
- Inclusion-exclusion principle
- Partitions and Young tableaux
- Posets and lattices
- Design theory and block designs

This processor handles ALL combinatorics notation with professor-quality pronunciation.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Combinatorics Context Types
# ===========================

class CombinatoricsContext(Enum):
    """Specific combinatorics contexts for fine-grained processing"""
    COUNTING = "counting"
    GRAPH_THEORY = "graph_theory"
    GENERATING_FUNCTIONS = "generating_functions"
    RECURRENCE = "recurrence"
    PARTITIONS = "partitions"
    DESIGNS = "designs"
    POSETS = "posets"
    GENERAL = "general"

@dataclass
class CombinatoricsTerm:
    """Represents a combinatorics term with pronunciation hints"""
    latex: str
    spoken: str
    context: CombinatoricsContext
    emphasis: bool = False
    add_article: bool = True

# ===========================
# Comprehensive Combinatorics Vocabulary
# ===========================

class CombinatoricsVocabulary:
    """Complete combinatorics vocabulary with natural pronunciations"""
    
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
        """Build comprehensive combinatorics vocabulary"""
        vocab = {}
        
        # ===== BASIC COUNTING =====
        
        vocab.update({
            r'n!': 'n factorial',
            r'([0-9]+)!': lambda m: f'{m.group(1)} factorial',
            r'([a-z])!': lambda m: f'{m.group(1)} factorial',
            r'\\binom{n}{k}': 'n choose k',
            r'\\binom{([^}]+)}{([^}]+)}': lambda m: f'{self._process_nested(m.group(1))} choose {self._process_nested(m.group(2))}',
            r'\\dbinom{([^}]+)}{([^}]+)}': lambda m: f'{self._process_nested(m.group(1))} choose {self._process_nested(m.group(2))}',
            r'C\\(([^,]+),([^)]+)\\)': lambda m: f'{self._process_nested(m.group(1))} choose {self._process_nested(m.group(2))}',
            r'C_([^,]+)^([^\\s]+)': lambda m: f'{self._process_nested(m.group(1))} choose {self._process_nested(m.group(2))}',
            r'P\\(([^,]+),([^)]+)\\)': lambda m: f'the number of permutations of {self._process_nested(m.group(1))} taken {self._process_nested(m.group(2))} at a time',
            r'P_([^,]+)^([^\\s]+)': lambda m: f'the number of permutations of {self._process_nested(m.group(1))} taken {self._process_nested(m.group(2))} at a time',
            r'\\frac{n!}{k!\\(n-k\\)!}': 'n factorial over k factorial times n minus k factorial',
            r'\\frac{n!}{\\(n-k\\)!}': 'n factorial over n minus k factorial',
        })
        
        # ===== STIRLING NUMBERS =====
        
        vocab.update({
            r'S\\(([^,]+),([^)]+)\\)': lambda m: f'Stirling number of the second kind {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}',
            r's\\(([^,]+),([^)]+)\\)': lambda m: f'Stirling number of the first kind {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}',
            r'\\left\\{([^}]+) \\atop ([^}]+)\\right\\}': lambda m: f'Stirling number of the second kind {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}',
            r'\\left\\[([^}]+) \\atop ([^}]+)\\right\\]': lambda m: f'Stirling number of the first kind {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}',
            r'\\genfrac{\\{}{\\}}{0pt}{}{([^}]+)}{([^}]+)}': lambda m: f'Stirling number of the second kind {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}',
            r'\\genfrac{\\[}{\\]}{0pt}{}{([^}]+)}{([^}]+)}': lambda m: f'Stirling number of the first kind {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}',
        })
        
        # ===== BELL AND CATALAN NUMBERS =====
        
        vocab.update({
            r'B_n': 'the n-th Bell number',
            r'B_([0-9]+)': lambda m: f'the {self._ordinal(m.group(1))} Bell number',
            r'C_n': 'the n-th Catalan number',
            r'C_([0-9]+)': lambda m: f'the {self._ordinal(m.group(1))} Catalan number',
            r'\\text{Cat}_n': 'the n-th Catalan number',
            r'\\text{Cat}_([0-9]+)': lambda m: f'the {self._ordinal(m.group(1))} Catalan number',
            r'\\frac{1}{n+1}\\binom{2n}{n}': 'one over n plus 1 times 2n choose n',
        })
        
        # ===== FIBONACCI AND LUCAS NUMBERS =====
        
        vocab.update({
            r'F_n': 'the n-th Fibonacci number',
            r'F_([0-9]+)': lambda m: f'the {self._ordinal(m.group(1))} Fibonacci number',
            r'L_n': 'the n-th Lucas number',
            r'L_([0-9]+)': lambda m: f'the {self._ordinal(m.group(1))} Lucas number',
            r'\\text{Fib}\\(n\\)': 'the n-th Fibonacci number',
            r'\\text{Fib}\\(([0-9]+)\\)': lambda m: f'the {self._ordinal(m.group(1))} Fibonacci number',
            r'\\phi': 'phi',
            r'\\varphi': 'phi',
            r'\\frac{1+\\sqrt{5}}{2}': 'one plus square root of 5 over 2',
        })
        
        # ===== GRAPH THEORY =====
        
        vocab.update({
            r'G = \\(V, E\\)': 'G equals the graph with vertex set V and edge set E',
            r'G = \\(V\\(G\\), E\\(G\\)\\)': 'G equals the graph with vertex set V of G and edge set E of G',
            r'V\\(G\\)': 'the vertex set of G',
            r'E\\(G\\)': 'the edge set of G',
            r'\\|V\\(G\\)\\|': 'the number of vertices in G',
            r'\\|E\\(G\\)\\|': 'the number of edges in G',
            r'\\|V\\|': 'the number of vertices',
            r'\\|E\\|': 'the number of edges',
            r'v\\(G\\)': 'the number of vertices in G',
            r'e\\(G\\)': 'the number of edges in G',
            r'n\\(G\\)': 'the order of G',
            r'm\\(G\\)': 'the size of G',
            r'\\deg\\(v\\)': 'the degree of vertex v',
            r'\\deg_G\\(v\\)': 'the degree of vertex v in G',
            r'd\\(v\\)': 'the degree of vertex v',
            r'\\delta\\(G\\)': 'the minimum degree of G',
            r'\\Delta\\(G\\)': 'the maximum degree of G',
            r'\\text{deg}\\(v\\)': 'the degree of vertex v',
        })
        
        # ===== GRAPH STRUCTURES =====
        
        vocab.update({
            r'K_n': 'the complete graph on n vertices',
            r'K_([0-9]+)': lambda m: f'the complete graph on {m.group(1)} vertices',
            r'K_{([^}]+)}': lambda m: f'the complete graph on {self._process_nested(m.group(1))} vertices',
            r'K_{([^,]+),([^}]+)}': lambda m: f'the complete bipartite graph K {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}',
            r'C_n': 'the cycle on n vertices',
            r'C_([0-9]+)': lambda m: f'the cycle on {m.group(1)} vertices',
            r'P_n': 'the path on n vertices',
            r'P_([0-9]+)': lambda m: f'the path on {m.group(1)} vertices',
            r'W_n': 'the wheel graph on n vertices',
            r'W_([0-9]+)': lambda m: f'the wheel graph on {m.group(1)} vertices',
            r'Q_n': 'the n-dimensional hypercube',
            r'Q_([0-9]+)': lambda m: f'the {m.group(1)}-dimensional hypercube',
            r'S_n': 'the star graph on n vertices',
            r'S_([0-9]+)': lambda m: f'the star graph on {m.group(1)} vertices',
        })
        
        # ===== GRAPH PROPERTIES =====
        
        vocab.update({
            r'\\chi\\(G\\)': 'the chromatic number of G',
            r'\\alpha\\(G\\)': 'the independence number of G',
            r'\\omega\\(G\\)': 'the clique number of G',
            r'\\kappa\\(G\\)': 'the connectivity of G',
            r'\\lambda\\(G\\)': 'the edge connectivity of G',
            r'\\text{girth}\\(G\\)': 'the girth of G',
            r'\\text{diam}\\(G\\)': 'the diameter of G',
            r'\\text{rad}\\(G\\)': 'the radius of G',
            r'd_G\\(u,v\\)': 'the distance from u to v in G',
            r'd\\(u,v\\)': 'the distance from u to v',
            r'\\text{dist}_G\\(u,v\\)': 'the distance from u to v in G',
            r'\\text{dist}\\(u,v\\)': 'the distance from u to v',
            r'\\text{connected}': 'connected',
            r'\\text{bipartite}': 'bipartite',
            r'\\text{planar}': 'planar',
            r'\\text{Eulerian}': 'Eulerian',
            r'\\text{Hamiltonian}': 'Hamiltonian',
        })
        
        # ===== TREES AND FORESTS =====
        
        vocab.update({
            r'T': 'the tree T',
            r'\\text{tree}': 'tree',
            r'\\text{forest}': 'forest',
            r'\\text{leaf}': 'leaf',
            r'\\text{leaves}': 'leaves',
            r'\\text{spanning tree}': 'spanning tree',
            r'\\text{MST}': 'minimum spanning tree',
            r'\\text{root}': 'root',
            r'\\text{parent}': 'parent',
            r'\\text{child}': 'child',
            r'\\text{ancestor}': 'ancestor',
            r'\\text{descendant}': 'descendant',
            r'\\text{height}': 'height',
            r'\\text{depth}': 'depth',
            r'\\text{binary tree}': 'binary tree',
            r'\\tau\\(G\\)': 'the number of spanning trees of G',
        })
        
        # ===== GENERATING FUNCTIONS =====
        
        vocab.update({
            r'G\\(x\\)': 'the generating function G of x',
            r'F\\(x\\)': 'the generating function F of x',
            r'A\\(x\\)': 'the generating function A of x',
            r'\\sum_{n=0}^\\infty a_n x^n': 'the sum from n equals 0 to infinity of a sub n times x to the n',
            r'\\sum_{n \\geq 0} a_n x^n': 'the sum over n greater than or equal to 0 of a sub n times x to the n',
            r'\\frac{1}{1-x}': 'one over one minus x',
            r'\\frac{1}{\\(1-x\\)^k}': 'one over one minus x to the k',
            r'\\frac{1}{\\(1-x\\)^([0-9]+)}': lambda m: f'one over one minus x to the {m.group(1)}',
            r'\\text{OGF}': 'ordinary generating function',
            r'\\text{EGF}': 'exponential generating function',
            r'\\sum_{n=0}^\\infty a_n \\frac{x^n}{n!}': 'the sum from n equals 0 to infinity of a sub n times x to the n over n factorial',
            r'e^x': 'e to the x',
            r'\\exp\\(x\\)': 'the exponential of x',
        })
        
        # ===== PARTITIONS =====
        
        vocab.update({
            r'p\\(n\\)': 'the number of partitions of n',
            r'p\\(([0-9]+)\\)': lambda m: f'the number of partitions of {m.group(1)}',
            r'p\\(n,k\\)': 'the number of partitions of n into k parts',
            r'p\\(([^,]+),([^)]+)\\)': lambda m: f'the number of partitions of {self._process_nested(m.group(1))} into {self._process_nested(m.group(2))} parts',
            r'q\\(n\\)': 'the number of partitions of n into distinct parts',
            r'q\\(([0-9]+)\\)': lambda m: f'the number of partitions of {m.group(1)} into distinct parts',
            r'\\lambda \\vdash n': 'lambda is a partition of n',
            r'\\lambda = \\(\\lambda_1, \\lambda_2, \\ldots, \\lambda_k\\)': 'lambda equals the partition lambda 1 comma lambda 2 comma dot dot dot comma lambda k',
            r'\\ell\\(\\lambda\\)': 'the length of the partition lambda',
            r'\\|\\lambda\\|': 'the size of the partition lambda',
            r'\\text{Young diagram}': 'Young diagram',
            r'\\text{Young tableau}': 'Young tableau',
            r'\\text{hook length}': 'hook length',
        })
        
        # ===== POSETS AND LATTICES =====
        
        vocab.update({
            r'\\(P, \\leq\\)': 'the poset P with order relation less than or equal to',
            r'\\text{poset}': 'poset',
            r'\\text{partially ordered set}': 'partially ordered set',
            r'\\text{chain}': 'chain',
            r'\\text{antichain}': 'antichain',
            r'\\text{maximal element}': 'maximal element',
            r'\\text{minimal element}': 'minimal element',
            r'\\text{greatest element}': 'greatest element',
            r'\\text{least element}': 'least element',
            r'\\text{upper bound}': 'upper bound',
            r'\\text{lower bound}': 'lower bound',
            r'\\text{supremum}': 'supremum',
            r'\\text{infimum}': 'infimum',
            r'\\text{lattice}': 'lattice',
            r'\\text{Boolean lattice}': 'Boolean lattice',
            r'\\text{distributive lattice}': 'distributive lattice',
            r'\\text{Möbius function}': 'Möbius function',
            r'\\mu\\(x,y\\)': 'the Möbius function mu of x comma y',
            r'\\text{incidence algebra}': 'incidence algebra',
        })
        
        # ===== DESIGN THEORY =====
        
        vocab.update({
            r'\\text{BIBD}': 'balanced incomplete block design',
            r'\\(v,k,\\lambda\\)\\text{-design}': 'v comma k comma lambda design',
            r'\\(([^,]+),([^,]+),([^)]+)\\)\\text{-design}': lambda m: f'{self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))} comma {self._process_nested(m.group(3))} design',
            r'\\text{Steiner system}': 'Steiner system',
            r'S\\(([^,]+),([^,]+),([^)]+)\\)': lambda m: f'Steiner system S {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))} comma {self._process_nested(m.group(3))}',
            r'\\text{Latin square}': 'Latin square',
            r'\\text{orthogonal Latin squares}': 'orthogonal Latin squares',
            r'\\text{mutually orthogonal Latin squares}': 'mutually orthogonal Latin squares',
            r'\\text{MOLS}': 'mutually orthogonal Latin squares',
            r'\\text{block design}': 'block design',
            r'\\text{incidence matrix}': 'incidence matrix',
        })
        
        # ===== INCLUSION-EXCLUSION =====
        
        vocab.update({
            r'\\left\\|\\bigcup_{i=1}^n A_i\\right\\|': 'the cardinality of the union from i equals 1 to n of A sub i',
            r'\\sum_{i=1}^n \\|A_i\\|': 'the sum from i equals 1 to n of the cardinality of A sub i',
            r'\\sum_{1 \\leq i < j \\leq n} \\|A_i \\cap A_j\\|': 'the sum over 1 less than or equal to i less than j less than or equal to n of the cardinality of A sub i intersect A sub j',
            r'\\text{inclusion-exclusion}': 'inclusion-exclusion principle',
            r'\\text{PIE}': 'principle of inclusion-exclusion',
            r'\\sum_{k=0}^n \\(-1\\)^k': 'the sum from k equals 0 to n of negative 1 to the k',
        })
        
        # ===== RECURRENCE RELATIONS =====
        
        vocab.update({
            r'a_n = a_{n-1} + a_{n-2}': 'a sub n equals a sub n minus 1 plus a sub n minus 2',
            r'a_n = c_1 a_{n-1} + c_2 a_{n-2} + \\cdots + c_k a_{n-k}': 'a sub n equals c 1 times a sub n minus 1 plus c 2 times a sub n minus 2 plus dot dot dot plus c k times a sub n minus k',
            r'\\text{characteristic equation}': 'characteristic equation',
            r'\\text{characteristic polynomial}': 'characteristic polynomial',
            r'x^k - c_1 x^{k-1} - c_2 x^{k-2} - \\cdots - c_k = 0': 'x to the k minus c 1 times x to the k minus 1 minus c 2 times x to the k minus 2 minus dot dot dot minus c k equals 0',
            r'\\text{generating function method}': 'generating function method',
            r'\\text{initial conditions}': 'initial conditions',
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements"""
        patterns = [
            # Counting principles
            (r'\\text{There are } ([^\\s]+) \\text{ ways to choose } ([^\\s]+) \\text{ objects from } ([^\\s]+)',
             lambda m: f'There are {self._process_nested(m.group(1))} ways to choose {self._process_nested(m.group(2))} objects from {self._process_nested(m.group(3))}'),
            (r'\\text{The number of permutations of } n \\text{ objects is } n!',
             'The number of permutations of n objects is n factorial'),
            (r'\\text{The number of combinations of } n \\text{ objects taken } k \\text{ at a time is } \\binom{n}{k}',
             'The number of combinations of n objects taken k at a time is n choose k'),
            
            # Graph theory theorems
            (r'\\text{Handshaking Lemma}',
             'the Handshaking Lemma'),
            (r'\\sum_{v \\in V} \\deg\\(v\\) = 2\\|E\\|',
             'the sum over v in V of the degree of v equals 2 times the number of edges'),
            (r'\\text{Euler\'s formula}: v - e + f = 2',
             'Euler\'s formula: v minus e plus f equals 2'),
            (r'\\text{A graph is bipartite if and only if it contains no odd cycles}',
             'A graph is bipartite if and only if it contains no odd cycles'),
            
            # Generating functions
            (r'\\text{The generating function for the sequence } \\{a_n\\} \\text{ is } \\sum_{n=0}^\\infty a_n x^n',
             'The generating function for the sequence a sub n is the sum from n equals 0 to infinity of a sub n times x to the n'),
            (r'\\left\\[x^n\\right\\] F\\(x\\)',
             'the coefficient of x to the n in F of x'),
            
            # Catalan number formulas
            (r'C_n = \\frac{1}{n+1} \\binom{2n}{n}',
             'C sub n equals one over n plus 1 times 2n choose n'),
            (r'C_n = \\sum_{i=0}^{n-1} C_i C_{n-1-i}',
             'C sub n equals the sum from i equals 0 to n minus 1 of C sub i times C sub n minus 1 minus i'),
            
            # Stirling numbers
            (r'S\\(n+1,k\\) = k \\cdot S\\(n,k\\) + S\\(n,k-1\\)',
             'Stirling number of the second kind n plus 1 comma k equals k times Stirling number of the second kind n comma k plus Stirling number of the second kind n comma k minus 1'),
            
            # Bell numbers
            (r'B_{n+1} = \\sum_{k=0}^n \\binom{n}{k} B_k',
             'Bell number n plus 1 equals the sum from k equals 0 to n of n choose k times Bell number k'),
            
            # Inclusion-exclusion
            (r'\\left\\|\\bigcup_{i=1}^n A_i\\right\\| = \\sum_{k=1}^n \\(-1\\)^{k-1} \\sum_{\\|S\\|=k} \\left\\|\\bigcap_{i \\in S} A_i\\right\\|',
             'the cardinality of the union from i equals 1 to n of A sub i equals the sum from k equals 1 to n of negative 1 to the k minus 1 times the sum over subsets S of size k of the cardinality of the intersection over i in S of A sub i'),
            
            # Fibonacci
            (r'F_n = F_{n-1} + F_{n-2}',
             'Fibonacci number n equals Fibonacci number n minus 1 plus Fibonacci number n minus 2'),
            (r'F_n = \\frac{\\phi^n - \\psi^n}{\\sqrt{5}}',
             'Fibonacci number n equals phi to the n minus psi to the n over square root of 5'),
            
            # Partitions
            (r'\\text{The number of partitions of } n \\text{ into odd parts equals the number of partitions into distinct parts}',
             'The number of partitions of n into odd parts equals the number of partitions into distinct parts'),
            (r'\\prod_{n=1}^\\infty \\frac{1}{1-x^n} = \\sum_{n=0}^\\infty p\\(n\\) x^n',
             'the product from n equals 1 to infinity of one over one minus x to the n equals the sum from n equals 0 to infinity of p of n times x to the n'),
            
            # Ramsey theory
            (r'R\\(([^,]+),([^)]+)\\)',
             lambda m: f'Ramsey number R {self._process_nested(m.group(1))} comma {self._process_nested(m.group(2))}'),
            (r'\\text{Ramsey\'s theorem}',
             'Ramsey\'s theorem'),
            
            # Chromatic polynomial
            (r'P_G\\(k\\)',
             'the chromatic polynomial of G evaluated at k'),
            (r'\\chi\\(G\\) = \\min\\{k : P_G\\(k\\) > 0\\}',
             'the chromatic number of G equals the minimum k such that the chromatic polynomial of G at k is positive'),
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
            (r'\\emptyset', 'the empty set'),
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

# ===========================
# Main Combinatorics Processor
# ===========================

class CombinatoricsProcessor:
    """Main processor for combinatorics domain"""
    
    def __init__(self):
        self.vocabulary = CombinatoricsVocabulary()
        self.context = CombinatoricsContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_theorems': True,
            'clarify_notation': True,
            'expand_formulas': True,
        }
        
        logger.info("Combinatorics processor initialized with complete vocabulary")
    
    def detect_subcontext(self, text: str) -> CombinatoricsContext:
        """Detect specific combinatorics subcontext"""
        text_lower = text.lower()
        
        # Check for counting
        if any(term in text_lower for term in ['permutation', 'combination', 'choose', 'factorial']):
            return CombinatoricsContext.COUNTING
        
        # Check for graph theory
        if any(term in text_lower for term in ['graph', 'vertex', 'edge', 'tree', 'cycle']):
            return CombinatoricsContext.GRAPH_THEORY
        
        # Check for generating functions
        if any(term in text_lower for term in ['generating function', 'ogf', 'egf']):
            return CombinatoricsContext.GENERATING_FUNCTIONS
        
        # Check for recurrence
        if any(term in text_lower for term in ['recurrence', 'fibonacci', 'characteristic']):
            return CombinatoricsContext.RECURRENCE
        
        # Check for partitions
        if any(term in text_lower for term in ['partition', 'young', 'tableau']):
            return CombinatoricsContext.PARTITIONS
        
        # Check for designs
        if any(term in text_lower for term in ['design', 'bibd', 'steiner', 'latin square']):
            return CombinatoricsContext.DESIGNS
        
        # Check for posets
        if any(term in text_lower for term in ['poset', 'lattice', 'partial order']):
            return CombinatoricsContext.POSETS
        
        return CombinatoricsContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process combinatorics text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"Combinatorics subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special combinatorics rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process combinatorics text"""
        # Normalize common variations
        normalizations = [
            (r'\\text{comb}\\(([^,]+),([^)]+)\\)', r'\\binom{\1}{\2}'),
            (r'\\text{perm}\\(([^,]+),([^)]+)\\)', r'P(\1,\2)'),
            (r'n\\text{P}k', 'P(n,k)'),
            (r'n\\text{C}k', r'\\binom{n}{k}'),
            (r'\\text{Ch}\\(([^,]+),([^)]+)\\)', r'\\binom{\1}{\2}'),
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply combinatorics vocabulary replacements"""
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
        """Apply special combinatorics-specific rules"""
        
        # Emphasize important theorems
        if self.special_rules['emphasize_theorems']:
            theorem_patterns = [
                (r'Handshaking Lemma', 'the Handshaking Lemma'),
                (r'Euler\'s formula', 'Euler\'s formula'),
                (r'Ramsey\'s theorem', 'Ramsey\'s theorem'),
                (r'Inclusion-Exclusion Principle', 'the Inclusion-Exclusion Principle'),
                (r'Pigeonhole Principle', 'the Pigeonhole Principle'),
                (r'Burnside\'s Lemma', 'Burnside\'s Lemma'),
                (r'Pólya Enumeration', 'Pólya Enumeration'),
            ]
            
            for pattern, replacement in theorem_patterns:
                text = re.sub(pattern, f"{{EMPHASIS}}{replacement}{{/EMPHASIS}}", text, flags=re.IGNORECASE)
        
        # Add clarifications for potentially ambiguous notation
        if self.special_rules['clarify_notation']:
            if self.context == CombinatoricsContext.GRAPH_THEORY:
                # Clarify when C_n might refer to cycle vs. other meanings
                text = re.sub(r'\bC_([0-9]+)\b(?!.*choose)', r'the cycle C sub \1', text)
                text = re.sub(r'\bK_([0-9]+)\b', r'the complete graph K sub \1', text)
                text = re.sub(r'\bP_([0-9]+)\b(?!.*permutation)', r'the path P sub \1', text)
        
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
            'domain': 'combinatorics',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_combinatorics_processor():
    """Comprehensive test of combinatorics processor"""
    processor = CombinatoricsProcessor()
    
    test_cases = [
        # Basic counting
        r"The number of ways to choose $k$ objects from $n$ is $\binom{n}{k} = \frac{n!}{k!(n-k)!}$",
        r"There are $n!$ permutations of $n$ distinct objects.",
        r"The number of permutations of $n$ objects taken $k$ at a time is $P(n,k) = \frac{n!}{(n-k)!}$",
        
        # Stirling numbers
        r"Stirling numbers of the second kind satisfy $S(n+1,k) = k \cdot S(n,k) + S(n,k-1)$",
        r"The number of ways to partition $n$ objects into $k$ non-empty subsets is $S(n,k)$",
        
        # Bell and Catalan numbers
        r"The $n$-th Bell number is $B_n = \sum_{k=0}^n S(n,k)$",
        r"The $n$-th Catalan number is $C_n = \frac{1}{n+1}\binom{2n}{n}$",
        r"Catalan numbers satisfy the recurrence $C_n = \sum_{i=0}^{n-1} C_i C_{n-1-i}$",
        
        # Graph theory
        r"A graph $G = (V,E)$ with $|V| = n$ vertices and $|E| = m$ edges satisfies $\sum_{v \in V} \deg(v) = 2m$",
        r"The complete graph $K_n$ has $\binom{n}{2}$ edges",
        r"A tree on $n$ vertices has exactly $n-1$ edges",
        r"The chromatic number $\chi(G)$ is the minimum number of colors needed to color the vertices",
        
        # Generating functions
        r"The generating function for the Fibonacci sequence is $\frac{x}{1-x-x^2}$",
        r"The exponential generating function for Bell numbers is $\sum_{n=0}^\infty B_n \frac{x^n}{n!} = e^{e^x-1}$",
        r"The coefficient of $x^n$ in $(1+x)^k$ is $\binom{k}{n}$",
        
        # Partitions
        r"The number of partitions of $n$ is denoted $p(n)$",
        r"Euler's theorem: the number of partitions of $n$ into odd parts equals the number into distinct parts",
        r"A Young diagram represents a partition graphically",
        
        # Inclusion-exclusion
        r"By inclusion-exclusion, $\left|\bigcup_{i=1}^n A_i\right| = \sum_{k=1}^n (-1)^{k-1} \sum_{|S|=k} \left|\bigcap_{i \in S} A_i\right|$",
        
        # Ramsey theory
        r"Ramsey's theorem: for any $r,s$, there exists $R(r,s)$ such that any 2-coloring of $K_{R(r,s)}$ contains a monochromatic $K_r$ or $K_s$",
        
        # Design theory
        r"A $(v,k,\lambda)$-design is a collection of $k$-subsets (blocks) of a $v$-set such that every pair appears in exactly $\lambda$ blocks",
        r"A Steiner system $S(t,k,v)$ is a $t$-$(v,k,1)$ design",
    ]
    
    print("Testing Combinatorics Processor")
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
    test_combinatorics_processor()