#!/usr/bin/env python3
"""
Extensive Test Suite for Algorithms Domain Processor
===================================================

This module provides comprehensive testing for the Algorithms processor,
covering all major topics including:
- Big O notation and complexity analysis
- Data structures (arrays, trees, graphs, heaps)
- Algorithm pseudocode
- Sorting and searching algorithms
- Graph algorithms (DFS, BFS, shortest paths)
- Dynamic programming
- Machine learning notation
- Optimization problems
"""

import pytest
import logging
from typing import List, Tuple, Dict, Any

from domains.algorithms import AlgorithmsProcessor, AlgorithmsContext

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestAlgorithmsProcessor:
    """Comprehensive test suite for Algorithms processor"""
    
    @pytest.fixture
    def processor(self):
        """Create an Algorithms processor instance"""
        return AlgorithmsProcessor()
    
    # ===== BIG O NOTATION =====
    
    def test_big_o_notation(self, processor):
        """Test Big O notation"""
        test_cases = [
            (r"O(1)", "big O of 1"),
            (r"O(n)", "big O of n"),
            (r"O(n^2)", "big O of n squared"),
            (r"O(n^3)", "big O of n to the 3"),
            (r"O(\log n)", "big O of log n"),
            (r"O(n \log n)", "big O of n log n"),
            (r"O(2^n)", "big O of 2 to the n"),
            (r"O(n!)", "big O of n factorial"),
            (r"\mathcal{O}(n)", "big O of n"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_other_complexity_notations(self, processor):
        """Test other complexity notations"""
        test_cases = [
            (r"o(n)", "little o of n"),
            (r"\Omega(n)", "big omega of n"),
            (r"\omega(n)", "little omega of n"),
            (r"\Theta(n)", "big theta of n"),
            (r"\theta(n)", "little theta of n"),
            (r"O(n^2) + O(n)", "big O of n squared"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_complexity_classes(self, processor):
        """Test complexity class notation"""
        test_cases = [
            (r"\text{polynomial time}", "polynomial time"),
            (r"\text{exponential time}", "exponential time"),
            (r"\text{NP-complete}", "NP-complete"),
            (r"\text{NP-hard}", "NP-hard"),
            (r"\mathbf{P}", "P"),
            (r"\mathbf{NP}", "NP"),
            (r"\mathbf{PSPACE}", "PSPACE"),
            (r"\mathbf{EXPTIME}", "EXPTIME"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result, f"Failed for {latex}: got {result}"
    
    # ===== ALGORITHM NOTATION =====
    
    def test_pseudocode_keywords(self, processor):
        """Test pseudocode keywords"""
        test_cases = [
            (r"\textbf{Algorithm}", "Algorithm"),
            (r"\textbf{Input}", "Input"),
            (r"\textbf{Output}", "Output"),
            (r"\textbf{begin}", "begin"),
            (r"\textbf{end}", "end"),
            (r"\textbf{if}", "if"),
            (r"\textbf{then}", "then"),
            (r"\textbf{else}", "else"),
            (r"\textbf{while}", "while"),
            (r"\textbf{do}", "do"),
            (r"\textbf{for}", "for"),
            (r"\textbf{return}", "return"),
            (r"\textbf{function}", "function"),
            (r"\textbf{procedure}", "procedure"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result, f"Failed for {latex}: got {result}"
    
    def test_assignment_notation(self, processor):
        """Test assignment notation"""
        test_cases = [
            (r"x \gets 5", "x gets 5"),
            (r"x \leftarrow y", "x gets y"),
            (r"x \rightarrow y", "x returns y"),
            (r"\text{true}", "true"),
            (r"\text{false}", "false"),
            (r"\text{nil}", "nil"),
            (r"\text{null}", "null"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== DATA STRUCTURES =====
    
    def test_basic_data_structures(self, processor):
        """Test basic data structure terminology"""
        test_cases = [
            (r"\text{array}", "array"),
            (r"\text{list}", "list"),
            (r"\text{stack}", "stack"),
            (r"\text{queue}", "queue"),
            (r"\text{deque}", "deque"),
            (r"\text{priority queue}", "priority queue"),
            (r"\text{heap}", "heap"),
            (r"\text{binary heap}", "binary heap"),
            (r"\text{min-heap}", "min-heap"),
            (r"\text{max-heap}", "max-heap"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_tree_structures(self, processor):
        """Test tree data structures"""
        test_cases = [
            (r"\text{binary tree}", "binary tree"),
            (r"\text{BST}", "binary search tree"),
            (r"\text{binary search tree}", "binary search tree"),
            (r"\text{AVL tree}", "AVL tree"),
            (r"\text{red-black tree}", "red-black tree"),
            (r"\text{B-tree}", "B-tree"),
            (r"\text{trie}", "trie"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_hash_structures(self, processor):
        """Test hash-based data structures"""
        test_cases = [
            (r"\text{hash table}", "hash table"),
            (r"\text{hash map}", "hash map"),
            (r"\text{dictionary}", "dictionary"),
            (r"\text{set}", "set"),
            (r"\text{multiset}", "multiset"),
            (r"\text{disjoint set}", "disjoint set"),
            (r"\text{union-find}", "union-find"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== ARRAY AND LIST OPERATIONS =====
    
    def test_array_operations(self, processor):
        """Test array operation notation"""
        test_cases = [
            (r"A[i]", "A at index i"),
            (r"B[j]", "B at index j"),
            (r"A[i+1]", "A at index i plus 1"),
            (r"\text{length}(A)", "length of A"),
            (r"|A|", "size of A"),
            (r"\text{size}(A)", "size of A"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_stack_queue_operations(self, processor):
        """Test stack and queue operations"""
        test_cases = [
            (r"\text{push}(x)", "push x"),
            (r"\text{pop}()", "pop"),
            (r"\text{enqueue}(x)", "enqueue x"),
            (r"\text{dequeue}()", "dequeue"),
            (r"\text{insert}(x, i)", "insert x at i"),
            (r"\text{delete}(x)", "delete x"),
            (r"\text{search}(x)", "search for x"),
            (r"\text{find}(x)", "find x"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== TREE OPERATIONS =====
    
    def test_tree_operations(self, processor):
        """Test tree operation notation"""
        test_cases = [
            (r"\text{root}", "root"),
            (r"\text{parent}(v)", "parent of v"),
            (r"\text{left}(v)", "left child of v"),
            (r"\text{right}(v)", "right child of v"),
            (r"\text{children}(v)", "children of v"),
            (r"\text{leaf}", "leaf"),
            (r"\text{height}(T)", "height of T"),
            (r"\text{depth}(v)", "depth of v"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_tree_traversals(self, processor):
        """Test tree traversal notation"""
        test_cases = [
            (r"\text{inorder}", "inorder"),
            (r"\text{preorder}", "preorder"),
            (r"\text{postorder}", "postorder"),
            (r"\text{level-order}", "level-order"),
            (r"\text{DFS}", "depth-first search"),
            (r"\text{BFS}", "breadth-first search"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== SORTING ALGORITHMS =====
    
    def test_sorting_algorithms(self, processor):
        """Test sorting algorithm names"""
        test_cases = [
            (r"\text{bubble sort}", "bubble sort"),
            (r"\text{insertion sort}", "insertion sort"),
            (r"\text{selection sort}", "selection sort"),
            (r"\text{merge sort}", "merge sort"),
            (r"\text{quick sort}", "quick sort"),
            (r"\text{heap sort}", "heap sort"),
            (r"\text{counting sort}", "counting sort"),
            (r"\text{radix sort}", "radix sort"),
            (r"\text{bucket sort}", "bucket sort"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_sorting_properties(self, processor):
        """Test sorting property terminology"""
        test_cases = [
            (r"\text{stable sort}", "stable sort"),
            (r"\text{in-place sort}", "in-place sort"),
            (r"\text{comparison-based}", "comparison-based"),
            (r"\text{non-comparison}", "non-comparison"),
            (r"\text{partition}", "partition"),
            (r"\text{pivot}", "pivot"),
            (r"\text{merge}", "merge"),
            (r"\text{heapify}", "heapify"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== GRAPH ALGORITHMS =====
    
    def test_graph_traversals(self, processor):
        """Test graph traversal algorithms"""
        test_cases = [
            (r"\text{DFS}(v)", "depth-first search from v"),
            (r"\text{BFS}(v)", "breadth-first search from v"),
            (r"\text{DFS}(G)", "depth-first search from G"),
            (r"\text{BFS}(G)", "breadth-first search from G"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_shortest_path_algorithms(self, processor):
        """Test shortest path algorithms"""
        test_cases = [
            (r"\text{Dijkstra}", "dijkstra's algorithm"),
            (r"\text{Bellman-Ford}", "bellman-ford algorithm"),
            (r"\text{Floyd-Warshall}", "floyd-warshall algorithm"),
            (r"\text{shortest path}", "shortest path"),
            (r"\text{single source}", "single source"),
            (r"\text{all pairs}", "all pairs"),
            (r"d[v]", "distance to v"),
            (r"\text{dist}[u]", "distance to u"),
            (r"\text{prev}[v]", "previous vertex for v"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_spanning_tree_algorithms(self, processor):
        """Test spanning tree algorithms"""
        test_cases = [
            (r"\text{Kruskal}", "kruskal's algorithm"),
            (r"\text{Prim}", "prim's algorithm"),
            (r"\text{MST}", "minimum spanning tree"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_flow_algorithms(self, processor):
        """Test flow algorithms"""
        test_cases = [
            (r"\text{Ford-Fulkerson}", "ford-fulkerson algorithm"),
            (r"\text{max flow}", "maximum flow"),
            (r"\text{min cut}", "minimum cut"),
            (r"\text{strongly connected}", "strongly connected"),
            (r"\text{topological sort}", "topological sort"),
            (r"\text{cycle detection}", "cycle detection"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== DYNAMIC PROGRAMMING =====
    
    def test_dp_notation(self, processor):
        """Test dynamic programming notation"""
        test_cases = [
            (r"\text{DP}", "dynamic programming"),
            (r"\text{dp}[i]", "DP table at i"),
            (r"\text{dp}[i][j]", "DP table at i comma j"),
            (r"\text{memo}[n]", "memoization table at n"),
            (r"\text{optimal substructure}", "optimal substructure"),
            (r"\text{overlapping subproblems}", "overlapping subproblems"),
            (r"\text{memoization}", "memoization"),
            (r"\text{tabulation}", "tabulation"),
            (r"\text{bottom-up}", "bottom-up"),
            (r"\text{top-down}", "top-down"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_dp_problems(self, processor):
        """Test classic DP problems"""
        test_cases = [
            (r"\text{LCS}", "longest common subsequence"),
            (r"\text{LIS}", "longest increasing subsequence"),
            (r"\text{edit distance}", "edit distance"),
            (r"\text{knapsack}", "knapsack"),
            (r"\text{coin change}", "coin change"),
            (r"\text{matrix chain}", "matrix chain"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== MACHINE LEARNING =====
    
    def test_ml_basics(self, processor):
        """Test machine learning basic notation"""
        test_cases = [
            (r"\text{ML}", "machine learning"),
            (r"\text{AI}", "artificial intelligence"),
            (r"\text{neural network}", "neural network"),
            (r"\text{NN}", "neural network"),
            (r"\text{CNN}", "convolutional neural network"),
            (r"\text{RNN}", "recurrent neural network"),
            (r"\text{LSTM}", "long short-term memory"),
            (r"\text{GRU}", "gated recurrent unit"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_ml_optimization(self, processor):
        """Test ML optimization notation"""
        test_cases = [
            (r"\text{gradient descent}", "gradient descent"),
            (r"\text{SGD}", "stochastic gradient descent"),
            (r"\text{backpropagation}", "backpropagation"),
            (r"\text{learning rate}", "learning rate"),
            (r"\alpha", "alpha"),
            (r"\eta", "eta"),
            (r"\text{epoch}", "epoch"),
            (r"\text{batch}", "batch"),
            (r"\text{mini-batch}", "mini-batch"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_ml_functions(self, processor):
        """Test ML function notation"""
        test_cases = [
            (r"\text{loss function}", "loss function"),
            (r"\text{cost function}", "cost function"),
            (r"\text{objective function}", "objective function"),
            (r"\text{activation function}", "activation function"),
            (r"\text{ReLU}", "relu"),
            (r"\text{sigmoid}", "sigmoid"),
            (r"\text{tanh}", "tanh"),
            (r"\text{softmax}", "softmax"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== OPTIMIZATION =====
    
    def test_optimization_notation(self, processor):
        """Test optimization notation"""
        test_cases = [
            (r"\text{minimize}", "minimize"),
            (r"\text{maximize}", "maximize"),
            (r"\text{subject to}", "subject to"),
            (r"\text{s.t.}", "subject to"),
            (r"\text{constraint}", "constraint"),
            (r"\text{objective}", "objective"),
            (r"\text{feasible}", "feasible"),
            (r"\text{optimal}", "optimal"),
            (r"\text{local minimum}", "local minimum"),
            (r"\text{global minimum}", "global minimum"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_optimization_types(self, processor):
        """Test optimization problem types"""
        test_cases = [
            (r"\text{linear programming}", "linear programming"),
            (r"\text{LP}", "linear programming"),
            (r"\text{quadratic programming}", "quadratic programming"),
            (r"\text{QP}", "quadratic programming"),
            (r"\text{integer programming}", "integer programming"),
            (r"\text{IP}", "integer programming"),
            (r"\text{simplex method}", "simplex method"),
            (r"\nabla f", "gradient of f"),
            (r"\nabla^2 f", "hessian of f"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== RANDOMIZED ALGORITHMS =====
    
    def test_randomized_algorithms(self, processor):
        """Test randomized algorithm notation"""
        test_cases = [
            (r"\text{randomized}", "randomized"),
            (r"\text{Las Vegas}", "las vegas"),
            (r"\text{Monte Carlo}", "monte carlo"),
            (r"\text{expected time}", "expected time"),
            (r"\text{with high probability}", "with high probability"),
            (r"\text{w.h.p.}", "with high probability"),
            (r"\mathbb{E}[X]", "expected value of X"),
            (r"\text{Pr}[A]", "probability of A"),
            (r"\text{uniform random}", "uniform random"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_hashing(self, processor):
        """Test hashing notation"""
        test_cases = [
            (r"\text{hash function}", "hash function"),
            (r"\text{collision}", "collision"),
            (r"\text{load factor}", "load factor"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== AMORTIZED ANALYSIS =====
    
    def test_amortized_analysis(self, processor):
        """Test amortized analysis notation"""
        test_cases = [
            (r"\text{amortized}", "amortized"),
            (r"\text{aggregate method}", "aggregate method"),
            (r"\text{accounting method}", "accounting method"),
            (r"\text{potential method}", "potential method"),
            (r"\text{credit}", "credit"),
            (r"\text{potential function}", "potential function"),
            (r"\Phi", "phi"),
            (r"\text{amortized cost}", "amortized cost"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== CONTEXT DETECTION =====
    
    def test_context_detection(self, processor):
        """Test that context is correctly detected"""
        test_cases = [
            (r"O(n \log n)", AlgorithmsContext.COMPLEXITY),
            (r"\text{binary tree}", AlgorithmsContext.DATA_STRUCTURES),
            (r"\text{merge sort}", AlgorithmsContext.SORTING),
            (r"\text{DFS}(v)", AlgorithmsContext.GRAPHS),
            (r"\text{dp}[i][j]", AlgorithmsContext.DYNAMIC_PROGRAMMING),
            (r"\text{neural network}", AlgorithmsContext.MACHINE_LEARNING),
            (r"\text{minimize} f(x)", AlgorithmsContext.OPTIMIZATION),
        ]
        
        for latex, expected_context in test_cases:
            _ = processor.process(latex)
            assert processor.context == expected_context, \
                f"Wrong context for {latex}: got {processor.context}, expected {expected_context}"
    
    # ===== COMPLEX EXPRESSIONS =====
    
    def test_complex_expressions(self, processor):
        """Test complex algorithm expressions"""
        test_cases = [
            # Complexity statement
            (
                r"\text{The running time of merge sort is } O(n \log n)",
                ["running time", "merge sort", "big O of n log n"]
            ),
            # Pseudocode
            (
                r"\textbf{for } i \gets 1 \textbf{ to } n",
                ["for i from 1 to n"]
            ),
            # DP recurrence
            (
                r"dp[i][j] = \max\{dp[i-1][j], dp[i-1][j-w_i] + v_i\}",
                ["DP at i comma j", "equals the maximum"]
            ),
            # Graph algorithm
            (
                r"\text{Run DFS from vertex } s \text{ to find all reachable vertices}",
                ["depth-first search from vertex s"]
            ),
        ]
        
        for latex, expected_parts in test_cases:
            result = processor.process(latex)
            for part in expected_parts:
                assert part in result.lower(), \
                    f"Missing '{part}' in result for {latex}: got {result}"
    
    # ===== ERROR HANDLING =====
    
    def test_error_handling(self, processor):
        """Test handling of edge cases"""
        test_cases = [
            "",  # Empty
            r"O(",  # Incomplete
            r"\text{",  # Unclosed
            "plain text",  # No LaTeX
        ]
        
        for latex in test_cases:
            result = processor.process(latex)
            assert isinstance(result, str)
    
    # ===== PERFORMANCE =====
    
    def test_performance(self, processor):
        """Test processing performance"""
        import time
        
        expressions = [
            r"O(n \log n)",
            r"\text{binary tree}",
            r"A[i]",
            r"\text{DFS}(v)",
            r"dp[i][j]",
        ] * 20  # 100 expressions
        
        start_time = time.time()
        for expr in expressions:
            _ = processor.process(expr)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / len(expressions)
        
        assert avg_time < 0.01, f"Processing too slow: {avg_time:.4f}s per expression"


# ===== PARAMETRIZED TESTS =====

@pytest.mark.parametrize("complexity,expected", [
    (r"O(1)", "big O of 1"),
    (r"O(n)", "big O of n"),
    (r"O(n^2)", "big O of n squared"),
    (r"O(\log n)", "big O of log n"),
    (r"O(n!)", "big O of n factorial"),
])
def test_complexity_notation(complexity, expected):
    """Test complexity notation recognition"""
    processor = AlgorithmsProcessor()
    result = processor.process(complexity)
    assert expected in result.lower()


@pytest.mark.parametrize("algorithm,expected", [
    (r"\text{merge sort}", "merge sort"),
    (r"\text{Dijkstra}", "dijkstra"),
    (r"\text{DFS}", "depth-first search"),
    (r"\text{DP}", "dynamic programming"),
])
def test_algorithm_names(algorithm, expected):
    """Test algorithm name recognition"""
    processor = AlgorithmsProcessor()
    result = processor.process(algorithm)
    assert expected in result.lower()


@pytest.mark.parametrize("structure,expected", [
    (r"\text{binary tree}", "binary tree"),
    (r"\text{hash table}", "hash table"),
    (r"\text{heap}", "heap"),
    (r"\text{stack}", "stack"),
])
def test_data_structures(structure, expected):
    """Test data structure recognition"""
    processor = AlgorithmsProcessor()
    result = processor.process(structure)
    assert expected in result.lower()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])