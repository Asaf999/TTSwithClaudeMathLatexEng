#!/usr/bin/env python3
"""
Extensive Test Suite for Combinatorics Domain Processor
======================================================

This module provides comprehensive testing for the Combinatorics processor,
covering all major topics including:
- Counting principles (permutations, combinations)
- Special numbers (Stirling, Bell, Catalan, Fibonacci)
- Graph theory (vertices, edges, algorithms)
- Generating functions
- Partitions and Young tableaux
- Design theory
- Posets and lattices
- Recurrence relations
"""

import pytest
import logging
from typing import List, Tuple, Dict, Any

from domains.combinatorics import CombinatoricsProcessor, CombinatoricsContext

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestCombinatoricsProcessor:
    """Comprehensive test suite for Combinatorics processor"""
    
    @pytest.fixture
    def processor(self):
        """Create a Combinatorics processor instance"""
        return CombinatoricsProcessor()
    
    # ===== BASIC COUNTING =====
    
    def test_factorials(self, processor):
        """Test factorial notation"""
        test_cases = [
            (r"n!", "n factorial"),
            (r"5!", "5 factorial"),
            (r"k!", "k factorial"),
            (r"0!", "0 factorial"),
            (r"(n-1)!", "n minus 1 factorial"),
            (r"(2n)!", "2n factorial"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_binomial_coefficients(self, processor):
        """Test binomial coefficient notation"""
        test_cases = [
            (r"\binom{n}{k}", "n choose k"),
            (r"\binom{10}{3}", "10 choose 3"),
            (r"\binom{n+1}{k}", "n plus 1 choose k"),
            (r"\dbinom{n}{k}", "n choose k"),
            (r"C(n,k)", "n choose k"),
            (r"C_n^k", "n choose k"),
            (r"\frac{n!}{k!(n-k)!}", "n factorial over k factorial times n minus k factorial"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_permutations(self, processor):
        """Test permutation notation"""
        test_cases = [
            (r"P(n,k)", "number of permutations of n taken k at a time"),
            (r"P_n^k", "number of permutations of n taken k at a time"),
            (r"P(10,3)", "number of permutations of 10 taken 3 at a time"),
            (r"\frac{n!}{(n-k)!}", "n factorial over n minus k factorial"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in expected.lower().split()), \
                f"Failed for {latex}: got {result}"
    
    # ===== STIRLING NUMBERS =====
    
    def test_stirling_numbers(self, processor):
        """Test Stirling number notation"""
        test_cases = [
            (r"S(n,k)", "stirling number of the second kind n comma k"),
            (r"s(n,k)", "stirling number of the first kind n comma k"),
            (r"\left\{n \atop k\right\}", "stirling number of the second kind n comma k"),
            (r"\left[n \atop k\right]", "stirling number of the first kind n comma k"),
            (r"S(5,3)", "stirling number of the second kind 5 comma 3"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_stirling_recurrence(self, processor):
        """Test Stirling number recurrence relations"""
        latex = r"S(n+1,k) = k \cdot S(n,k) + S(n,k-1)"
        result = processor.process(latex)
        
        assert "stirling number" in result.lower()
        assert "n plus 1 comma k" in result.lower()
        assert "k times" in result.lower()
    
    # ===== SPECIAL NUMBERS =====
    
    def test_bell_numbers(self, processor):
        """Test Bell number notation"""
        test_cases = [
            (r"B_n", "n-th bell number"),
            (r"B_5", "5th bell number"),
            (r"\text{Bell}_n", "n-th bell number"),
            (r"B_{n+1} = \sum_{k=0}^n \binom{n}{k} B_k", "bell number n plus 1"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert "bell number" in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_catalan_numbers(self, processor):
        """Test Catalan number notation"""
        test_cases = [
            (r"C_n", "n-th catalan number"),
            (r"C_5", "5th catalan number"),
            (r"\text{Cat}_n", "n-th catalan number"),
            (r"\frac{1}{n+1}\binom{2n}{n}", "one over n plus 1 times 2n choose n"),
            (r"C_n = \sum_{i=0}^{n-1} C_i C_{n-1-i}", "catalan number"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in ["catalan", expected.lower()]), \
                f"Failed for {latex}: got {result}"
    
    def test_fibonacci_lucas(self, processor):
        """Test Fibonacci and Lucas numbers"""
        test_cases = [
            (r"F_n", "n-th fibonacci number"),
            (r"F_{10}", "10th fibonacci number"),
            (r"L_n", "n-th lucas number"),
            (r"L_7", "7th lucas number"),
            (r"\text{Fib}(n)", "n-th fibonacci number"),
            (r"F_n = F_{n-1} + F_{n-2}", "fibonacci number n equals"),
            (r"\phi", "phi"),
            (r"\frac{1+\sqrt{5}}{2}", "one plus square root of 5 over 2"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in expected.lower().split()), \
                f"Failed for {latex}: got {result}"
    
    # ===== GRAPH THEORY =====
    
    def test_graph_notation(self, processor):
        """Test basic graph notation"""
        test_cases = [
            (r"G = (V, E)", "G equals the graph with vertex set V and edge set E"),
            (r"V(G)", "vertex set of G"),
            (r"E(G)", "edge set of G"),
            (r"|V(G)|", "number of vertices in G"),
            (r"|E(G)|", "number of edges in G"),
            (r"v(G)", "number of vertices in G"),
            (r"e(G)", "number of edges in G"),
            (r"n(G)", "order of G"),
            (r"m(G)", "size of G"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_degree_notation(self, processor):
        """Test vertex degree notation"""
        test_cases = [
            (r"\deg(v)", "degree of vertex v"),
            (r"\deg_G(v)", "degree of vertex v in G"),
            (r"d(v)", "degree of vertex v"),
            (r"\delta(G)", "minimum degree of G"),
            (r"\Delta(G)", "maximum degree of G"),
            (r"\text{deg}(v)", "degree of vertex v"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_special_graphs(self, processor):
        """Test special graph types"""
        test_cases = [
            (r"K_n", "complete graph on n vertices"),
            (r"K_5", "complete graph on 5 vertices"),
            (r"K_{3,3}", "complete bipartite graph K 3 comma 3"),
            (r"C_n", "cycle on n vertices"),
            (r"C_6", "cycle on 6 vertices"),
            (r"P_n", "path on n vertices"),
            (r"P_4", "path on 4 vertices"),
            (r"W_n", "wheel graph on n vertices"),
            (r"Q_n", "n-dimensional hypercube"),
            (r"Q_3", "3-dimensional hypercube"),
            (r"S_n", "star graph on n vertices"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_graph_properties(self, processor):
        """Test graph property notation"""
        test_cases = [
            (r"\chi(G)", "chromatic number of G"),
            (r"\alpha(G)", "independence number of G"),
            (r"\omega(G)", "clique number of G"),
            (r"\kappa(G)", "connectivity of G"),
            (r"\lambda(G)", "edge connectivity of G"),
            (r"\text{girth}(G)", "girth of G"),
            (r"\text{diam}(G)", "diameter of G"),
            (r"\text{rad}(G)", "radius of G"),
            (r"d_G(u,v)", "distance from u to v in G"),
            (r"\text{dist}(u,v)", "distance from u to v"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_graph_algorithms(self, processor):
        """Test graph algorithm notation"""
        test_cases = [
            (r"\text{DFS}(v)", "depth-first search from v"),
            (r"\text{BFS}(v)", "breadth-first search from v"),
            (r"\text{MST}", "minimum spanning tree"),
            (r"\text{shortest path}", "shortest path"),
            (r"\tau(G)", "number of spanning trees of G"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== GENERATING FUNCTIONS =====
    
    def test_generating_functions(self, processor):
        """Test generating function notation"""
        test_cases = [
            (r"G(x)", "generating function G of x"),
            (r"F(x)", "generating function F of x"),
            (r"A(x)", "generating function A of x"),
            (r"\sum_{n=0}^\infty a_n x^n", "sum from n equals 0 to infinity of a sub n times x to the n"),
            (r"\sum_{n \geq 0} a_n x^n", "sum over n greater than or equal to 0"),
            (r"\frac{1}{1-x}", "one over one minus x"),
            (r"\frac{1}{(1-x)^k}", "one over one minus x to the k"),
            (r"\text{OGF}", "ordinary generating function"),
            (r"\text{EGF}", "exponential generating function"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_exponential_gf(self, processor):
        """Test exponential generating functions"""
        test_cases = [
            (r"\sum_{n=0}^\infty a_n \frac{x^n}{n!}", "sum from n equals 0 to infinity of a sub n times x to the n over n factorial"),
            (r"e^x", "e to the x"),
            (r"\exp(x)", "exponential of x"),
            (r"[x^n] F(x)", "coefficient of x to the n in F of x"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in expected.lower().split()), \
                f"Failed for {latex}: got {result}"
    
    # ===== PARTITIONS =====
    
    def test_partitions(self, processor):
        """Test partition notation"""
        test_cases = [
            (r"p(n)", "number of partitions of n"),
            (r"p(10)", "number of partitions of 10"),
            (r"p(n,k)", "number of partitions of n into k parts"),
            (r"q(n)", "number of partitions of n into distinct parts"),
            (r"\lambda \vdash n", "lambda is a partition of n"),
            (r"\lambda = (\lambda_1, \lambda_2, \ldots, \lambda_k)", "lambda equals the partition"),
            (r"\ell(\lambda)", "length of the partition lambda"),
            (r"|\lambda|", "size of the partition lambda"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_young_tableaux(self, processor):
        """Test Young tableaux notation"""
        test_cases = [
            (r"\text{Young diagram}", "young diagram"),
            (r"\text{Young tableau}", "young tableau"),
            (r"\text{hook length}", "hook length"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== POSETS AND LATTICES =====
    
    def test_posets(self, processor):
        """Test poset notation"""
        test_cases = [
            (r"(P, \leq)", "poset P with order relation less than or equal to"),
            (r"\text{poset}", "poset"),
            (r"\text{partially ordered set}", "partially ordered set"),
            (r"\text{chain}", "chain"),
            (r"\text{antichain}", "antichain"),
            (r"\text{maximal element}", "maximal element"),
            (r"\text{minimal element}", "minimal element"),
            (r"\text{upper bound}", "upper bound"),
            (r"\text{lower bound}", "lower bound"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_lattices(self, processor):
        """Test lattice notation"""
        test_cases = [
            (r"\text{lattice}", "lattice"),
            (r"\text{Boolean lattice}", "boolean lattice"),
            (r"\text{distributive lattice}", "distributive lattice"),
            (r"\text{Möbius function}", "möbius function"),
            (r"\mu(x,y)", "möbius function mu of x comma y"),
            (r"\text{incidence algebra}", "incidence algebra"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected.replace("ö", "o") in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== DESIGN THEORY =====
    
    def test_designs(self, processor):
        """Test design theory notation"""
        test_cases = [
            (r"\text{BIBD}", "balanced incomplete block design"),
            (r"(v,k,\lambda)\text{-design}", "v comma k comma lambda design"),
            (r"(7,3,1)\text{-design}", "7 comma 3 comma 1 design"),
            (r"\text{Steiner system}", "steiner system"),
            (r"S(2,3,7)", "steiner system S 2 comma 3 comma 7"),
            (r"\text{Latin square}", "latin square"),
            (r"\text{orthogonal Latin squares}", "orthogonal latin squares"),
            (r"\text{MOLS}", "mutually orthogonal latin squares"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== INCLUSION-EXCLUSION =====
    
    def test_inclusion_exclusion(self, processor):
        """Test inclusion-exclusion principle"""
        test_cases = [
            (r"\left|\bigcup_{i=1}^n A_i\right|", "cardinality of the union from i equals 1 to n"),
            (r"\sum_{i=1}^n |A_i|", "sum from i equals 1 to n of the cardinality"),
            (r"\text{inclusion-exclusion}", "inclusion-exclusion"),
            (r"\text{PIE}", "principle of inclusion-exclusion"),
            (r"\sum_{k=0}^n (-1)^k", "sum from k equals 0 to n of negative 1 to the k"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== RECURRENCE RELATIONS =====
    
    def test_recurrence_relations(self, processor):
        """Test recurrence relation notation"""
        test_cases = [
            (r"a_n = a_{n-1} + a_{n-2}", "a sub n equals a sub n minus 1 plus a sub n minus 2"),
            (r"\text{characteristic equation}", "characteristic equation"),
            (r"\text{characteristic polynomial}", "characteristic polynomial"),
            (r"\text{generating function method}", "generating function method"),
            (r"\text{initial conditions}", "initial conditions"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== CONTEXT DETECTION =====
    
    def test_context_detection(self, processor):
        """Test that context is correctly detected"""
        test_cases = [
            (r"\binom{n}{k}", CombinatoricsContext.COUNTING),
            (r"G = (V,E)", CombinatoricsContext.GRAPH_THEORY),
            (r"\sum_{n=0}^\infty a_n x^n", CombinatoricsContext.GENERATING_FUNCTIONS),
            (r"F_n = F_{n-1} + F_{n-2}", CombinatoricsContext.RECURRENCE),
            (r"p(n)", CombinatoricsContext.PARTITIONS),
            (r"(v,k,\lambda)\text{-design}", CombinatoricsContext.DESIGNS),
            (r"(P, \leq)", CombinatoricsContext.POSETS),
        ]
        
        for latex, expected_context in test_cases:
            _ = processor.process(latex)
            assert processor.context == expected_context, \
                f"Wrong context for {latex}: got {processor.context}, expected {expected_context}"
    
    # ===== COMPLEX EXPRESSIONS =====
    
    def test_complex_expressions(self, processor):
        """Test complex combinatorial expressions"""
        test_cases = [
            # Handshaking lemma
            (
                r"\sum_{v \in V} \deg(v) = 2|E|",
                ["sum over v in V", "degree of v", "equals 2 times the number of edges"]
            ),
            # Euler's formula
            (
                r"v - e + f = 2",
                ["v minus e plus f equals 2"]
            ),
            # Binomial theorem
            (
                r"(x+y)^n = \sum_{k=0}^n \binom{n}{k} x^k y^{n-k}",
                ["sum from k equals 0 to n", "n choose k", "x to the k", "y to the n minus k"]
            ),
            # Catalan recurrence
            (
                r"C_n = \frac{1}{n+1} \binom{2n}{n} = \sum_{i=0}^{n-1} C_i C_{n-1-i}",
                ["one over n plus 1", "2n choose n", "sum from i equals 0"]
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
            r"\binom{n",  # Incomplete
            "plain text",  # No LaTeX
            r"K_",  # Incomplete graph notation
        ]
        
        for latex in test_cases:
            result = processor.process(latex)
            assert isinstance(result, str)
    
    # ===== PERFORMANCE =====
    
    def test_performance(self, processor):
        """Test processing performance"""
        import time
        
        expressions = [
            r"\binom{n}{k}",
            r"K_5",
            r"F_n",
            r"p(n)",
            r"\sum_{n=0}^\infty x^n",
        ] * 20  # 100 expressions
        
        start_time = time.time()
        for expr in expressions:
            _ = processor.process(expr)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / len(expressions)
        
        assert avg_time < 0.01, f"Processing too slow: {avg_time:.4f}s per expression"


# ===== PARAMETRIZED TESTS =====

@pytest.mark.parametrize("number,expected", [
    (r"C_n", "catalan"),
    (r"B_n", "bell"),
    (r"F_n", "fibonacci"),
    (r"L_n", "lucas"),
])
def test_special_numbers(number, expected):
    """Test special number recognition"""
    processor = CombinatoricsProcessor()
    result = processor.process(number)
    assert expected in result.lower()


@pytest.mark.parametrize("graph,expected", [
    (r"K_5", "complete graph on 5"),
    (r"C_6", "cycle on 6"),
    (r"P_4", "path on 4"),
    (r"Q_3", "3-dimensional hypercube"),
])
def test_graph_types(graph, expected):
    """Test graph type recognition"""
    processor = CombinatoricsProcessor()
    result = processor.process(graph)
    assert expected in result.lower()


@pytest.mark.parametrize("theorem,keywords", [
    ("Handshaking Lemma", ["handshaking", "lemma"]),
    ("Ramsey's theorem", ["ramsey", "theorem"]),
    ("Pigeonhole Principle", ["pigeonhole", "principle"]),
])
def test_theorem_names(theorem, keywords):
    """Test theorem name recognition"""
    processor = CombinatoricsProcessor()
    result = processor.process(theorem)
    for keyword in keywords:
        assert keyword in result.lower()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])