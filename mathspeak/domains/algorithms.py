#!/usr/bin/env python3
"""
Algorithms Domain Processor for Mathematical Text-to-Speech
==========================================================

Complete processor for algorithms and computer science notation including:
- Big O notation and complexity analysis
- Data structures (arrays, trees, graphs, heaps)
- Algorithm pseudocode and notation
- Sorting and searching algorithms
- Dynamic programming and recurrence relations
- Graph algorithms (shortest paths, MST, flows)
- Computational complexity theory
- Machine learning and optimization

This processor handles ALL algorithms notation with professor-quality pronunciation.
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable, Any
from dataclasses import dataclass
from collections import OrderedDict
from enum import Enum

logger = logging.getLogger(__name__)

# ===========================
# Algorithms Context Types
# ===========================

class AlgorithmsContext(Enum):
    """Specific algorithms contexts for fine-grained processing"""
    COMPLEXITY = "complexity"
    DATA_STRUCTURES = "data_structures"
    SORTING = "sorting"
    GRAPHS = "graphs"
    DYNAMIC_PROGRAMMING = "dynamic_programming"
    MACHINE_LEARNING = "machine_learning"
    OPTIMIZATION = "optimization"
    GENERAL = "general"

@dataclass
class AlgorithmsTerm:
    """Represents an algorithms term with pronunciation hints"""
    latex: str
    spoken: str
    context: AlgorithmsContext
    emphasis: bool = False
    add_article: bool = True

# ===========================
# Comprehensive Algorithms Vocabulary
# ===========================

class AlgorithmsVocabulary:
    """Complete algorithms vocabulary with natural pronunciations"""
    
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
        """Build comprehensive algorithms vocabulary"""
        vocab = {}
        
        # ===== BIG O NOTATION AND COMPLEXITY =====
        
        vocab.update({
            r'O\\(([^)]+)\\)': lambda m: f"big O of {self._process_nested(m.group(1))}",
            r'\\mathcal{O}\\(([^)]+)\\)': lambda m: f"big O of {self._process_nested(m.group(1))}",
            r'o\\(([^)]+)\\)': lambda m: f"little o of {self._process_nested(m.group(1))}",
            r'\\Omega\\(([^)]+)\\)': lambda m: f"big omega of {self._process_nested(m.group(1))}",
            r'\\omega\\(([^)]+)\\)': lambda m: f"little omega of {self._process_nested(m.group(1))}",
            r'\\Theta\\(([^)]+)\\)': lambda m: f"big theta of {self._process_nested(m.group(1))}",
            r'\\theta\\(([^)]+)\\)': lambda m: f"little theta of {self._process_nested(m.group(1))}",
            r'O\\(1\\)': 'big O of 1',
            r'O\\(n\\)': 'big O of n',
            r'O\\(n^2\\)': 'big O of n squared',
            r'O\\(n^([0-9]+)\\)': lambda m: f"big O of n to the {m.group(1)}",
            r'O\\(\\log n\\)': 'big O of log n',
            r'O\\(n \\log n\\)': 'big O of n log n',
            r'O\\(2^n\\)': 'big O of 2 to the n',
            r'O\\(n!\\)': 'big O of n factorial',
            r'\\text{polynomial time}': 'polynomial time',
            r'\\text{exponential time}': 'exponential time',
            r'\\text{NP-complete}': 'NP-complete',
            r'\\text{NP-hard}': 'NP-hard',
            r'\\mathbf{P}': 'P',
            r'\\mathbf{NP}': 'NP',
            r'\\mathbf{PSPACE}': 'PSPACE',
            r'\\mathbf{EXPTIME}': 'EXPTIME',
        })
        
        # ===== ALGORITHM NOTATION =====
        
        vocab.update({
            r'\\textbf{Algorithm}': 'Algorithm',
            r'\\textbf{Input}': 'Input',
            r'\\textbf{Output}': 'Output',
            r'\\textbf{begin}': 'begin',
            r'\\textbf{end}': 'end',
            r'\\textbf{if}': 'if',
            r'\\textbf{then}': 'then',
            r'\\textbf{else}': 'else',
            r'\\textbf{while}': 'while',
            r'\\textbf{do}': 'do',
            r'\\textbf{for}': 'for',
            r'\\textbf{to}': 'to',
            r'\\textbf{return}': 'return',
            r'\\textbf{function}': 'function',
            r'\\textbf{procedure}': 'procedure',
            r'\\gets': 'gets',
            r'\\leftarrow': 'gets',
            r'\\rightarrow': 'returns',
            r'\\text{and}': 'and',
            r'\\text{or}': 'or',
            r'\\text{not}': 'not',
            r'\\text{true}': 'true',
            r'\\text{false}': 'false',
            r'\\text{nil}': 'nil',
            r'\\text{null}': 'null',
        })
        
        # ===== DATA STRUCTURES =====
        
        vocab.update({
            r'\\text{array}': 'array',
            r'\\text{list}': 'list',
            r'\\text{stack}': 'stack',
            r'\\text{queue}': 'queue',
            r'\\text{deque}': 'deque',
            r'\\text{priority queue}': 'priority queue',
            r'\\text{heap}': 'heap',
            r'\\text{binary heap}': 'binary heap',
            r'\\text{min-heap}': 'min-heap',
            r'\\text{max-heap}': 'max-heap',
            r'\\text{binary tree}': 'binary tree',
            r'\\text{BST}': 'binary search tree',
            r'\\text{binary search tree}': 'binary search tree',
            r'\\text{AVL tree}': 'AVL tree',
            r'\\text{red-black tree}': 'red-black tree',
            r'\\text{B-tree}': 'B-tree',
            r'\\text{trie}': 'trie',
            r'\\text{hash table}': 'hash table',
            r'\\text{hash map}': 'hash map',
            r'\\text{dictionary}': 'dictionary',
            r'\\text{set}': 'set',
            r'\\text{multiset}': 'multiset',
            r'\\text{disjoint set}': 'disjoint set',
            r'\\text{union-find}': 'union-find',
        })
        
        # ===== ARRAY AND LIST OPERATIONS =====
        
        vocab.update({
            r'A\\[([^\\]]+)\\]': lambda m: f"A at index {self._process_nested(m.group(1))}",
            r'([A-Z])\\[([^\\]]+)\\]': lambda m: f"{m.group(1)} at index {self._process_nested(m.group(2))}",
            r'\\text{length}\\(([^)]+)\\)': lambda m: f"the length of {self._process_nested(m.group(1))}",
            r'\\|([A-Z])\\|': lambda m: f"the size of {m.group(1)}",
            r'\\text{size}\\(([^)]+)\\)': lambda m: f"the size of {self._process_nested(m.group(1))}",
            r'\\text{push}\\(([^)]+)\\)': lambda m: f"push {self._process_nested(m.group(1))}",
            r'\\text{pop}\\(\\)': 'pop',
            r'\\text{enqueue}\\(([^)]+)\\)': lambda m: f"enqueue {self._process_nested(m.group(1))}",
            r'\\text{dequeue}\\(\\)': 'dequeue',
            r'\\text{insert}\\(([^,]+),([^)]+)\\)': lambda m: f"insert {self._process_nested(m.group(1))} at {self._process_nested(m.group(2))}",
            r'\\text{delete}\\(([^)]+)\\)': lambda m: f"delete {self._process_nested(m.group(1))}",
            r'\\text{search}\\(([^)]+)\\)': lambda m: f"search for {self._process_nested(m.group(1))}",
            r'\\text{find}\\(([^)]+)\\)': lambda m: f"find {self._process_nested(m.group(1))}",
        })
        
        # ===== TREE OPERATIONS =====
        
        vocab.update({
            r'\\text{root}': 'root',
            r'\\text{parent}\\(([^)]+)\\)': lambda m: f"the parent of {self._process_nested(m.group(1))}",
            r'\\text{left}\\(([^)]+)\\)': lambda m: f"the left child of {self._process_nested(m.group(1))}",
            r'\\text{right}\\(([^)]+)\\)': lambda m: f"the right child of {self._process_nested(m.group(1))}",
            r'\\text{children}\\(([^)]+)\\)': lambda m: f"the children of {self._process_nested(m.group(1))}",
            r'\\text{leaf}': 'leaf',
            r'\\text{height}\\(([^)]+)\\)': lambda m: f"the height of {self._process_nested(m.group(1))}",
            r'\\text{depth}\\(([^)]+)\\)': lambda m: f"the depth of {self._process_nested(m.group(1))}",
            r'\\text{inorder}': 'inorder',
            r'\\text{preorder}': 'preorder',
            r'\\text{postorder}': 'postorder',
            r'\\text{level-order}': 'level-order',
            r'\\text{DFS}': 'depth-first search',
            r'\\text{BFS}': 'breadth-first search',
        })
        
        # ===== SORTING ALGORITHMS =====
        
        vocab.update({
            r'\\text{bubble sort}': 'bubble sort',
            r'\\text{insertion sort}': 'insertion sort',
            r'\\text{selection sort}': 'selection sort',
            r'\\text{merge sort}': 'merge sort',
            r'\\text{quick sort}': 'quick sort',
            r'\\text{heap sort}': 'heap sort',
            r'\\text{counting sort}': 'counting sort',
            r'\\text{radix sort}': 'radix sort',
            r'\\text{bucket sort}': 'bucket sort',
            r'\\text{stable sort}': 'stable sort',
            r'\\text{in-place sort}': 'in-place sort',
            r'\\text{comparison-based}': 'comparison-based',
            r'\\text{non-comparison}': 'non-comparison',
            r'\\text{partition}': 'partition',
            r'\\text{pivot}': 'pivot',
            r'\\text{merge}': 'merge',
            r'\\text{heapify}': 'heapify',
        })
        
        # ===== GRAPH ALGORITHMS =====
        
        vocab.update({
            r'\\text{DFS}\\(([^)]+)\\)': lambda m: f"depth-first search from {self._process_nested(m.group(1))}",
            r'\\text{BFS}\\(([^)]+)\\)': lambda m: f"breadth-first search from {self._process_nested(m.group(1))}",
            r'\\text{Dijkstra}': 'Dijkstra\'s algorithm',
            r'\\text{Bellman-Ford}': 'Bellman-Ford algorithm',
            r'\\text{Floyd-Warshall}': 'Floyd-Warshall algorithm',
            r'\\text{Kruskal}': 'Kruskal\'s algorithm',
            r'\\text{Prim}': 'Prim\'s algorithm',
            r'\\text{Ford-Fulkerson}': 'Ford-Fulkerson algorithm',
            r'\\text{MST}': 'minimum spanning tree',
            r'\\text{shortest path}': 'shortest path',
            r'\\text{single source}': 'single source',
            r'\\text{all pairs}': 'all pairs',
            r'\\text{max flow}': 'maximum flow',
            r'\\text{min cut}': 'minimum cut',
            r'\\text{strongly connected}': 'strongly connected',
            r'\\text{topological sort}': 'topological sort',
            r'\\text{cycle detection}': 'cycle detection',
            r'd\\[([^\\]]+)\\]': lambda m: f"distance to {self._process_nested(m.group(1))}",
            r'\\text{dist}\\[([^\\]]+)\\]': lambda m: f"distance to {self._process_nested(m.group(1))}",
            r'\\text{prev}\\[([^\\]]+)\\]': lambda m: f"previous vertex for {self._process_nested(m.group(1))}",
        })
        
        # ===== DYNAMIC PROGRAMMING =====
        
        vocab.update({
            r'\\text{DP}': 'dynamic programming',
            r'\\text{dp}\\[([^\\]]+)\\]': lambda m: f"DP table at {self._process_nested(m.group(1))}",
            r'\\text{memo}\\[([^\\]]+)\\]': lambda m: f"memoization table at {self._process_nested(m.group(1))}",
            r'\\text{optimal substructure}': 'optimal substructure',
            r'\\text{overlapping subproblems}': 'overlapping subproblems',
            r'\\text{memoization}': 'memoization',
            r'\\text{tabulation}': 'tabulation',
            r'\\text{bottom-up}': 'bottom-up',
            r'\\text{top-down}': 'top-down',
            r'\\text{LCS}': 'longest common subsequence',
            r'\\text{LIS}': 'longest increasing subsequence',
            r'\\text{edit distance}': 'edit distance',
            r'\\text{knapsack}': 'knapsack',
            r'\\text{coin change}': 'coin change',
            r'\\text{matrix chain}': 'matrix chain multiplication',
        })
        
        # ===== MACHINE LEARNING =====
        
        vocab.update({
            r'\\text{ML}': 'machine learning',
            r'\\text{AI}': 'artificial intelligence',
            r'\\text{neural network}': 'neural network',
            r'\\text{NN}': 'neural network',
            r'\\text{CNN}': 'convolutional neural network',
            r'\\text{RNN}': 'recurrent neural network',
            r'\\text{LSTM}': 'long short-term memory',
            r'\\text{GRU}': 'gated recurrent unit',
            r'\\text{gradient descent}': 'gradient descent',
            r'\\text{SGD}': 'stochastic gradient descent',
            r'\\text{backpropagation}': 'backpropagation',
            r'\\text{learning rate}': 'learning rate',
            r'\\alpha': 'alpha',
            r'\\eta': 'eta',
            r'\\text{epoch}': 'epoch',
            r'\\text{batch}': 'batch',
            r'\\text{mini-batch}': 'mini-batch',
            r'\\text{loss function}': 'loss function',
            r'\\text{cost function}': 'cost function',
            r'\\text{objective function}': 'objective function',
            r'\\text{activation function}': 'activation function',
            r'\\text{ReLU}': 'ReLU',
            r'\\text{sigmoid}': 'sigmoid',
            r'\\text{tanh}': 'tanh',
            r'\\text{softmax}': 'softmax',
        })
        
        # ===== OPTIMIZATION =====
        
        vocab.update({
            r'\\text{minimize}': 'minimize',
            r'\\text{maximize}': 'maximize',
            r'\\text{subject to}': 'subject to',
            r'\\text{s.t.}': 'subject to',
            r'\\text{constraint}': 'constraint',
            r'\\text{objective}': 'objective',
            r'\\text{feasible}': 'feasible',
            r'\\text{optimal}': 'optimal',
            r'\\text{local minimum}': 'local minimum',
            r'\\text{global minimum}': 'global minimum',
            r'\\text{convex}': 'convex',
            r'\\text{concave}': 'concave',
            r'\\text{linear programming}': 'linear programming',
            r'\\text{LP}': 'linear programming',
            r'\\text{quadratic programming}': 'quadratic programming',
            r'\\text{QP}': 'quadratic programming',
            r'\\text{integer programming}': 'integer programming',
            r'\\text{IP}': 'integer programming',
            r'\\text{simplex method}': 'simplex method',
            r'\\nabla f': 'the gradient of f',
            r'\\nabla^2 f': 'the Hessian of f',
            r'\\text{Hessian}': 'Hessian',
        })
        
        # ===== RANDOMIZED ALGORITHMS =====
        
        vocab.update({
            r'\\text{randomized}': 'randomized',
            r'\\text{Las Vegas}': 'Las Vegas',
            r'\\text{Monte Carlo}': 'Monte Carlo',
            r'\\text{expected time}': 'expected time',
            r'\\text{with high probability}': 'with high probability',
            r'\\text{w.h.p.}': 'with high probability',
            r'\\mathbb{E}\\[([^\\]]+)\\]': lambda m: f"the expected value of {self._process_nested(m.group(1))}",
            r'\\text{Pr}\\[([^\\]]+)\\]': lambda m: f"the probability of {self._process_nested(m.group(1))}",
            r'\\text{uniform random}': 'uniform random',
            r'\\text{hash function}': 'hash function',
            r'\\text{collision}': 'collision',
            r'\\text{load factor}': 'load factor',
        })
        
        # ===== AMORTIZED ANALYSIS =====
        
        vocab.update({
            r'\\text{amortized}': 'amortized',
            r'\\text{aggregate method}': 'aggregate method',
            r'\\text{accounting method}': 'accounting method',
            r'\\text{potential method}': 'potential method',
            r'\\text{credit}': 'credit',
            r'\\text{potential function}': 'potential function',
            r'\\Phi': 'phi',
            r'\\text{amortized cost}': 'amortized cost',
        })
        
        return vocab
    
    def _build_patterns(self) -> List[Tuple[str, Union[str, Callable]]]:
        """Build pattern-based replacements"""
        patterns = [
            # Algorithm complexity statements
            (r'\\text{The running time of } ([^\\s]+) \\text{ is } O\\(([^)]+)\\)',
             lambda m: f'The running time of {self._process_nested(m.group(1))} is big O of {self._process_nested(m.group(2))}'),
            (r'\\text{The space complexity is } O\\(([^)]+)\\)',
             lambda m: f'The space complexity is big O of {self._process_nested(m.group(1))}'),
            
            # Algorithm pseudocode patterns
            (r'\\textbf{for } ([^\\s]+) \\gets ([^\\s]+) \\textbf{ to } ([^\\s]+)',
             lambda m: f'for {self._process_nested(m.group(1))} from {self._process_nested(m.group(2))} to {self._process_nested(m.group(3))}'),
            (r'\\textbf{while } ([^\\s]+) \\textbf{ do}',
             lambda m: f'while {self._process_nested(m.group(1))} do'),
            (r'\\textbf{if } ([^\\s]+) \\textbf{ then}',
             lambda m: f'if {self._process_nested(m.group(1))} then'),
            
            # Data structure operations
            (r'\\text{Insert } ([^\\s]+) \\text{ into } ([^\\s]+)',
             lambda m: f'Insert {self._process_nested(m.group(1))} into {self._process_nested(m.group(2))}'),
            (r'\\text{Delete } ([^\\s]+) \\text{ from } ([^\\s]+)',
             lambda m: f'Delete {self._process_nested(m.group(1))} from {self._process_nested(m.group(2))}'),
            (r'\\text{Search for } ([^\\s]+) \\text{ in } ([^\\s]+)',
             lambda m: f'Search for {self._process_nested(m.group(1))} in {self._process_nested(m.group(2))}'),
            
            # Graph algorithm patterns
            (r'\\text{Run DFS from vertex } ([^\\s]+)',
             lambda m: f'Run depth-first search from vertex {self._process_nested(m.group(1))}'),
            (r'\\text{Run BFS from vertex } ([^\\s]+)',
             lambda m: f'Run breadth-first search from vertex {self._process_nested(m.group(1))}'),
            (r'\\text{The shortest path from } ([^\\s]+) \\text{ to } ([^\\s]+) \\text{ has length } ([^\\s]+)',
             lambda m: f'The shortest path from {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))} has length {self._process_nested(m.group(3))}'),
            
            # Sorting patterns
            (r'\\text{Sort the array } ([^\\s]+) \\text{ using } ([^\\s]+)',
             lambda m: f'Sort the array {self._process_nested(m.group(1))} using {self._process_nested(m.group(2))}'),
            (r'\\text{Merge } ([^\\s]+) \\text{ and } ([^\\s]+)',
             lambda m: f'Merge {self._process_nested(m.group(1))} and {self._process_nested(m.group(2))}'),
            (r'\\text{Partition around pivot } ([^\\s]+)',
             lambda m: f'Partition around pivot {self._process_nested(m.group(1))}'),
            
            # Dynamic programming patterns
            (r'\\text{Let } dp\\[([^\\]]+)\\] \\text{ be the optimal solution for subproblem } ([^\\s]+)',
             lambda m: f'Let DP at {self._process_nested(m.group(1))} be the optimal solution for subproblem {self._process_nested(m.group(2))}'),
            (r'dp\\[([^\\]]+)\\] = \\max\\{([^}]+)\\}',
             lambda m: f'DP at {self._process_nested(m.group(1))} equals the maximum of {self._process_nested(m.group(2))}'),
            (r'dp\\[([^\\]]+)\\] = \\min\\{([^}]+)\\}',
             lambda m: f'DP at {self._process_nested(m.group(1))} equals the minimum of {self._process_nested(m.group(2))}'),
            
            # Machine learning patterns
            (r'\\text{Train the model on } ([^\\s]+) \\text{ for } ([^\\s]+) \\text{ epochs}',
             lambda m: f'Train the model on {self._process_nested(m.group(1))} for {self._process_nested(m.group(2))} epochs'),
            (r'\\text{The loss is } ([^\\s]+)',
             lambda m: f'The loss is {self._process_nested(m.group(1))}'),
            (r'\\text{Update weights: } w \\gets w - \\alpha \\nabla f',
             'Update weights: w gets w minus alpha times the gradient of f'),
            
            # Amortized analysis
            (r'\\text{The amortized cost per operation is } O\\(([^)]+)\\)',
             lambda m: f'The amortized cost per operation is big O of {self._process_nested(m.group(1))}'),
            (r'\\text{Total cost over } n \\text{ operations is } O\\(([^)]+)\\)',
             lambda m: f'Total cost over n operations is big O of {self._process_nested(m.group(1))}'),
            
            # Complexity theory
            (r'\\text{Problem } ([^\\s]+) \\text{ is in } \\mathbf{NP}',
             lambda m: f'Problem {self._process_nested(m.group(1))} is in NP'),
            (r'\\text{Reduce } ([^\\s]+) \\text{ to } ([^\\s]+)',
             lambda m: f'Reduce {self._process_nested(m.group(1))} to {self._process_nested(m.group(2))}'),
            (r'([^\\s]+) \\leq_P ([^\\s]+)',
             lambda m: f'{self._process_nested(m.group(1))} reduces to {self._process_nested(m.group(2))} in polynomial time'),
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
            (r'\\log', 'log'),
            (r'\\sqrt{([^}]+)}', r'square root of \1'),
            (r'_([0-9])', r' sub \1'),
            (r'\^([0-9])', r' to the \1'),
            (r'\\infty', 'infinity'),
            (r'\\leq', 'less than or equal to'),
            (r'\\geq', 'greater than or equal to'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        return content

# ===========================
# Main Algorithms Processor
# ===========================

class AlgorithmsProcessor:
    """Main processor for algorithms domain"""
    
    def __init__(self):
        self.vocabulary = AlgorithmsVocabulary()
        self.context = AlgorithmsContext.GENERAL
        
        # Special handling rules
        self.special_rules = {
            'emphasize_algorithms': True,
            'clarify_complexity': True,
            'expand_pseudocode': True,
        }
        
        logger.info("Algorithms processor initialized with complete vocabulary")
    
    def detect_subcontext(self, text: str) -> AlgorithmsContext:
        """Detect specific algorithms subcontext"""
        text_lower = text.lower()
        
        # Check for complexity analysis
        if any(term in text_lower for term in ['big o', 'complexity', 'running time', 'space']):
            return AlgorithmsContext.COMPLEXITY
        
        # Check for data structures
        if any(term in text_lower for term in ['array', 'list', 'tree', 'heap', 'stack', 'queue']):
            return AlgorithmsContext.DATA_STRUCTURES
        
        # Check for sorting
        if any(term in text_lower for term in ['sort', 'merge', 'quick', 'heap', 'bubble']):
            return AlgorithmsContext.SORTING
        
        # Check for graph algorithms
        if any(term in text_lower for term in ['graph', 'vertex', 'edge', 'dijkstra', 'dfs', 'bfs']):
            return AlgorithmsContext.GRAPHS
        
        # Check for dynamic programming
        if any(term in text_lower for term in ['dynamic programming', 'dp', 'memoization', 'optimal']):
            return AlgorithmsContext.DYNAMIC_PROGRAMMING
        
        # Check for machine learning
        if any(term in text_lower for term in ['neural', 'learning', 'gradient', 'loss']):
            return AlgorithmsContext.MACHINE_LEARNING
        
        # Check for optimization
        if any(term in text_lower for term in ['minimize', 'maximize', 'linear programming', 'simplex']):
            return AlgorithmsContext.OPTIMIZATION
        
        return AlgorithmsContext.GENERAL
    
    def process(self, text: str) -> str:
        """Process algorithms text with complete notation handling"""
        # Detect subcontext
        self.context = self.detect_subcontext(text)
        logger.debug(f"Algorithms subcontext: {self.context.value}")
        
        # Pre-process for common patterns
        text = self._preprocess(text)
        
        # Apply vocabulary replacements
        text = self._apply_vocabulary(text)
        
        # Apply special algorithms rules
        text = self._apply_special_rules(text)
        
        # Post-process for clarity
        text = self._postprocess(text)
        
        return text
    
    def _preprocess(self, text: str) -> str:
        """Pre-process algorithms text"""
        # Normalize common variations
        normalizations = [
            (r'O\\(([^)]+)\\)', r'O(\1)'),  # Normalize O notation
            (r'\\Theta\\(([^)]+)\\)', r'�(\1)'),
            (r'\\Omega\\(([^)]+)\\)', r'�(\1)'),
            (r'\\text{alg}\\b', 'algorithm'),
            (r'\\text{proc}\\b', 'procedure'),
            (r'\\text{func}\\b', 'function'),
            (r'\\gets', '�'),
            (r'\\leftarrow', '�'),
        ]
        
        for pattern, replacement in normalizations:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _apply_vocabulary(self, text: str) -> str:
        """Apply algorithms vocabulary replacements"""
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
        """Apply special algorithms-specific rules"""
        
        # Emphasize important algorithms
        if self.special_rules['emphasize_algorithms']:
            algorithm_patterns = [
                (r'Dijkstra\'s algorithm', 'Dijkstra\'s algorithm'),
                (r'Floyd-Warshall algorithm', 'Floyd-Warshall algorithm'),
                (r'Bellman-Ford algorithm', 'Bellman-Ford algorithm'),
                (r'Kruskal\'s algorithm', 'Kruskal\'s algorithm'),
                (r'Prim\'s algorithm', 'Prim\'s algorithm'),
                (r'merge sort', 'merge sort'),
                (r'quick sort', 'quick sort'),
                (r'heap sort', 'heap sort'),
            ]
            
            for pattern, replacement in algorithm_patterns:
                text = re.sub(pattern, f"{{EMPHASIS}}{replacement}{{/EMPHASIS}}", text, flags=re.IGNORECASE)
        
        # Add clarifications for complexity notation
        if self.special_rules['clarify_complexity'] and self.context == AlgorithmsContext.COMPLEXITY:
            # Clarify common complexity classes
            text = re.sub(r'O\\(n\\)', 'big O of n which is linear time', text)
            text = re.sub(r'O\\(n^2\\)', 'big O of n squared which is quadratic time', text)
            text = re.sub(r'O\\(\\log n\\)', 'big O of log n which is logarithmic time', text)
        
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
            'domain': 'algorithms',
            'subcontext': self.context.value,
            'vocabulary_size': len(self.vocabulary.terms),
            'pattern_count': len(self.vocabulary.patterns),
        }

# ===========================
# Testing Functions
# ===========================

def test_algorithms_processor():
    """Comprehensive test of algorithms processor"""
    processor = AlgorithmsProcessor()
    
    test_cases = [
        # Complexity analysis
        r"The running time of merge sort is $O(n \log n)$ in the worst case.",
        r"Binary search has $O(\log n)$ time complexity and $O(1)$ space complexity.",
        r"The problem is in $\mathbf{NP}$ but not known to be in $\mathbf{P}$.",
        
        # Data structures
        r"Insert element $x$ into the binary search tree $T$.",
        r"The height of a balanced binary tree is $O(\log n)$.",
        r"A hash table provides $O(1)$ expected time for search, insert, and delete.",
        
        # Sorting algorithms
        r"Quick sort partitions the array around a pivot element.",
        r"Merge sort divides the array into two halves and recursively sorts them.",
        r"Heap sort builds a max-heap and repeatedly extracts the maximum.",
        
        # Graph algorithms
        r"Run Dijkstra's algorithm from source vertex $s$ to find shortest paths.",
        r"DFS explores as far as possible before backtracking.",
        r"BFS visits all vertices at distance $k$ before visiting vertices at distance $k+1$.",
        r"Kruskal's algorithm finds the MST by adding edges in order of increasing weight.",
        
        # Dynamic programming
        r"Let $dp[i][j]$ be the optimal solution for the subproblem with items $1$ to $i$ and capacity $j$.",
        r"The recurrence relation is $dp[i][j] = \max\{dp[i-1][j], dp[i-1][j-w_i] + v_i\}$.",
        r"Use memoization to avoid recomputing overlapping subproblems.",
        
        # Machine learning
        r"Train the neural network using gradient descent with learning rate $\alpha = 0.01$.",
        r"The loss function is $L(w) = \frac{1}{2} \sum_{i=1}^n (y_i - f(x_i))^2$.",
        r"Update weights: $w \leftarrow w - \alpha \nabla L(w)$.",
        
        # Pseudocode
        r"$\textbf{for } i \gets 1 \textbf{ to } n \textbf{ do}$",
        r"$\textbf{while } \text{queue is not empty} \textbf{ do}$",
        r"$\textbf{if } A[i] > A[j] \textbf{ then}$ swap $A[i]$ and $A[j]$",
        
        # Amortized analysis
        r"The amortized cost per operation is $O(1)$ using the potential method.",
        r"Although individual operations may be expensive, the total cost over $n$ operations is $O(n)$.",
        
        # Optimization
        r"Minimize $f(x)$ subject to $g(x) \leq 0$ and $h(x) = 0$.",
        r"The simplex method solves linear programming problems in polynomial time on average.",
        r"Use gradient descent to find a local minimum of the objective function.",
    ]
    
    print("Testing Algorithms Processor")
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
    test_algorithms_processor()