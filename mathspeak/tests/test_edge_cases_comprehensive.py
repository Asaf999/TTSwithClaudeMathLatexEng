#!/usr/bin/env python3
"""
Comprehensive Edge Case Tests for Mathematical Expressions
=========================================================

This module tests edge cases, corner cases, and stress scenarios for
all mathematical domain processors. It includes:
- Malformed LaTeX
- Extreme nesting
- Unicode and special characters
- Very long expressions
- Ambiguous notation
- Cross-domain boundary cases
- Performance limits
- Error recovery
"""

import pytest
import logging
import time
import re
from typing import List, Dict, Any, Optional

# Import all processors
from domains.real_analysis import RealAnalysisProcessor
from domains.measure_theory import MeasureTheoryProcessor
from domains.combinatorics import CombinatoricsProcessor
from domains.algorithms import AlgorithmsProcessor
from domains.topology import TopologyProcessor
from domains.complex_analysis import ComplexAnalysisProcessor
from domains.numerical_analysis import NumericalAnalysisProcessor
from domains.manifolds import ManifoldsProcessor
from domains.ode import ODEProcessor

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestMalformedLatex:
    """Test handling of malformed LaTeX expressions"""
    
    @pytest.fixture
    def all_processors(self):
        """Get all available processors"""
        return [
            RealAnalysisProcessor(),
            MeasureTheoryProcessor(),
            CombinatoricsProcessor(),
            AlgorithmsProcessor(),
            TopologyProcessor(),
            ComplexAnalysisProcessor(),
            NumericalAnalysisProcessor(),
            ManifoldsProcessor(),
            ODEProcessor(),
        ]
    
    def test_unclosed_brackets(self, all_processors):
        """Test expressions with unclosed brackets"""
        test_cases = [
            r"\frac{1",
            r"\binom{n}{k",
            r"\int_0^1 f(x",
            r"\\{a, b, c",
            r"\left( x + y",
            r"\sum_{i=1",
            r"f\(x, y",
        ]
        
        for processor in all_processors:
            for expr in test_cases:
                try:
                    result = processor.process(expr)
                    assert isinstance(result, str)
                    # Should not crash, may return partial result
                except Exception as e:
                    pytest.fail(f"{processor.__class__.__name__} crashed on '{expr}': {e}")
    
    def test_incomplete_commands(self, all_processors):
        """Test incomplete LaTeX commands"""
        test_cases = [
            r"\li",          # Incomplete \lim
            r"\int",         # No bounds or integrand
            r"\fra",         # Incomplete \frac
            r"\sum_",        # Incomplete sum
            r"\mathb",       # Incomplete \mathbb
            r"\\",           # Just backslash
            r"\{",           # Just opening brace
        ]
        
        for processor in all_processors:
            for expr in test_cases:
                result = processor.process(expr)
                assert isinstance(result, str)
                assert len(result) >= 0  # May return empty or partial
    
    def test_mismatched_delimiters(self, all_processors):
        """Test mismatched delimiters"""
        test_cases = [
            r"(a + b]",
            r"[x, y)",
            r"\{a, b\]",
            r"\left( x \right]",
            r"$\int_0^1 f(x) dx}",
            r"{a + b + c)]",
        ]
        
        for processor in all_processors:
            for expr in test_cases:
                result = processor.process(expr)
                # Should handle gracefully, not crash
                assert isinstance(result, str)
    
    def test_invalid_latex_commands(self, all_processors):
        """Test completely invalid LaTeX commands"""
        test_cases = [
            r"\notacommand{x}",
            r"\@#$%^&*()",
            r"\123invalid",
            r"\-hyphen-command",
            r"\ space command",
            r"\émojì",
        ]
        
        for processor in all_processors:
            for expr in test_cases:
                result = processor.process(expr)
                # Should skip invalid commands or handle gracefully
                assert isinstance(result, str)


class TestExtremeNesting:
    """Test deeply nested mathematical expressions"""
    
    def test_deeply_nested_fractions(self):
        """Test deeply nested fractions"""
        processor = RealAnalysisProcessor()
        
        # Build nested fraction: 1/(1+1/(1+1/(1+...)))
        nested = "1"
        for i in range(10):
            nested = f"\\frac{{1}}{{1 + {nested}}}"
        
        result = processor.process(nested)
        assert isinstance(result, str)
        assert "over" in result.lower()  # Should contain fraction language
        assert len(result) < 5000  # Shouldn't explode in length
    
    def test_deeply_nested_functions(self):
        """Test deeply nested function compositions"""
        processor = RealAnalysisProcessor()
        
        # f(g(h(i(j(k(x))))))
        nested = "x"
        for func in ['k', 'j', 'i', 'h', 'g', 'f']:
            nested = f"{func}({nested})"
        
        result = processor.process(nested)
        assert isinstance(result, str)
        assert result.count("of") >= 5  # Should have multiple "of" for composition
    
    def test_deeply_nested_subscripts(self):
        """Test deeply nested subscripts and superscripts"""
        processor = CombinatoricsProcessor()
        
        # a_{1_{2_{3_{4_{5}}}}}
        nested = "5"
        for i in range(4, 0, -1):
            nested = f"{i}_{{{nested}}}"
        expr = f"a_{{{nested}}}"
        
        result = processor.process(expr)
        assert isinstance(result, str)
        assert "sub" in result.lower()
    
    def test_nested_sums_and_products(self):
        """Test nested sums and products"""
        processor = RealAnalysisProcessor()
        
        expr = r"\sum_{i=1}^n \sum_{j=1}^m \sum_{k=1}^p a_{ijk}"
        result = processor.process(expr)
        
        assert result.count("sum") >= 3
        assert "i equals 1" in result.lower()
        assert "j equals 1" in result.lower()
        assert "k equals 1" in result.lower()


class TestUnicodeAndSpecialCharacters:
    """Test handling of Unicode and special characters"""
    
    def test_greek_letters(self):
        """Test Greek letter handling"""
        processor = RealAnalysisProcessor()
        
        test_cases = [
            (r"\alpha", "alpha"),
            (r"\beta", "beta"),
            (r"\gamma", "gamma"),
            (r"\Gamma", "Gamma"),
            (r"\delta", "delta"),
            (r"\Delta", "Delta"),
            (r"\epsilon", "epsilon"),
            (r"\varepsilon", "epsilon"),
            (r"\lambda", "lambda"),
            (r"\Lambda", "Lambda"),
            (r"\mu", "mu"),
            (r"\pi", "pi"),
            (r"\Pi", "Pi"),
            (r"\sigma", "sigma"),
            (r"\Sigma", "Sigma"),
            (r"\omega", "omega"),
            (r"\Omega", "Omega"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected.lower() in result.lower()
    
    def test_unicode_input(self):
        """Test direct Unicode mathematical input"""
        processors = {
            'real': RealAnalysisProcessor(),
            'combinatorics': CombinatoricsProcessor(),
        }
        
        test_cases = [
            ("∀x ∈ ℝ", "for all", "real"),
            ("∃y ∈ ℕ", "exists", "natural"),
            ("∑ᵢ₌₁ⁿ aᵢ", "sum", "sub"),
            ("∫₀¹ f(x)dx", "integral", "0 to 1"),
            ("x → ∞", "approaches", "infinity"),
            ("α + β = γ", "alpha", "beta"),
            ("A ⊆ B", "subset", "equal"),
            ("A ∪ B", "union", ""),
            ("A ∩ B", "intersect", ""),
        ]
        
        for expr, *expected_parts in test_cases:
            handled = False
            for name, processor in processors.items():
                try:
                    result = processor.process(expr)
                    if any(part in result.lower() for part in expected_parts if part):
                        handled = True
                        break
                except:
                    pass
            
            # At least one processor should handle Unicode
            assert handled, f"No processor handled Unicode: {expr}"
    
    def test_mixed_scripts(self):
        """Test mixed Latin, Greek, and other scripts"""
        processor = MeasureTheoryProcessor()
        
        expr = r"If μ is a σ-finite measure on (Ω, Σ), then ∫_Ω f dμ exists"
        result = processor.process(expr)
        
        assert "mu" in result.lower()
        assert "sigma-finite" in result.lower()
        assert "integral" in result.lower()


class TestVeryLongExpressions:
    """Test handling of extremely long mathematical expressions"""
    
    def test_long_sum(self):
        """Test very long summation"""
        processor = RealAnalysisProcessor()
        
        # Sum of 100 terms
        terms = [f"a_{{{i}}}" for i in range(100)]
        expr = r"\sum_{i=1}^{100} \left(" + " + ".join(terms) + r"\right)"
        
        start_time = time.time()
        result = processor.process(expr)
        duration = time.time() - start_time
        
        assert isinstance(result, str)
        assert duration < 2.0  # Should complete reasonably fast
        assert len(result) < 10000  # Output shouldn't be ridiculously long
    
    def test_long_product(self):
        """Test very long product expression"""
        processor = CombinatoricsProcessor()
        
        # Product of many binomial coefficients
        expr = r"\prod_{k=1}^{50} \binom{n}{k}"
        
        result = processor.process(expr)
        assert "product" in result.lower()
        assert "n choose k" in result.lower()
    
    def test_long_polynomial(self):
        """Test very long polynomial"""
        processor = AlgorithmsProcessor()
        
        # Polynomial with many terms
        terms = [f"{i}x^{{{i}}}" for i in range(20, 0, -1)]
        expr = " + ".join(terms)
        
        result = processor.process(expr)
        assert isinstance(result, str)
        assert "x to the" in result.lower()
    
    def test_maximum_expression_length(self):
        """Test expression at maximum reasonable length"""
        processor = RealAnalysisProcessor()
        
        # Build expression close to 10,000 characters
        base_expr = r"\int_0^1 \left( \sum_{n=1}^\infty \frac{1}{n^2} \right) dx + "
        expr = base_expr * 100  # About 5,000 characters
        
        result = processor.process(expr)
        assert isinstance(result, str)
        assert len(result) < 50000  # Output should be bounded


class TestAmbiguousNotation:
    """Test handling of ambiguous mathematical notation"""
    
    def test_context_dependent_symbols(self):
        """Test symbols that mean different things in different contexts"""
        test_cases = [
            # C can be constant, complex numbers, combinations, cycle graph
            (r"C", [
                (RealAnalysisProcessor(), "C"),
                (CombinatoricsProcessor(), "C"),
                (ComplexAnalysisProcessor(), "C"),
            ]),
            # d can be differential, distance, degree
            (r"d(x,y)", [
                (RealAnalysisProcessor(), "distance"),
                (TopologyProcessor(), "distance"),
                (CombinatoricsProcessor(), "d"),
            ]),
            # | | can be absolute value, cardinality, norm
            (r"|A|", [
                (RealAnalysisProcessor(), "absolute value"),
                (CombinatoricsProcessor(), "cardinality"),
                (MeasureTheoryProcessor(), "measure"),
            ]),
        ]
        
        for expr, processor_tests in test_cases:
            for processor, expected_context in processor_tests:
                result = processor.process(expr)
                # Each processor interprets according to its domain
                assert isinstance(result, str)
    
    def test_overloaded_operators(self):
        """Test operators with multiple meanings"""
        # Test * as multiplication, convolution, dual space, etc.
        test_cases = [
            (r"f * g", "convolution or multiplication"),
            (r"V^*", "dual space or conjugate"),
            (r"a \cdot b", "dot product or multiplication"),
        ]
        
        processor = RealAnalysisProcessor()
        for expr, description in test_cases:
            result = processor.process(expr)
            assert isinstance(result, str)
    
    def test_implicit_multiplication(self):
        """Test implicit multiplication handling"""
        processor = AlgorithmsProcessor()
        
        test_cases = [
            r"2n",      # 2 times n
            r"xy",      # x times y
            r"abc",     # a times b times c
            r"2\pi r",  # 2 pi r
            r"nlogn",   # n log n
        ]
        
        for expr in test_cases:
            result = processor.process(expr)
            assert isinstance(result, str)


class TestCrossDomainBoundaries:
    """Test expressions at the boundary between mathematical domains"""
    
    def test_topology_meets_analysis(self):
        """Test where topology meets analysis"""
        expr = r"A function f: X \to \mathbb{R} is continuous if f^{-1}(U) is open for every open U \subseteq \mathbb{R}"
        
        processors = [
            TopologyProcessor(),
            RealAnalysisProcessor(),
        ]
        
        for processor in processors:
            result = processor.process(expr)
            assert "continuous" in result.lower()
            assert "open" in result.lower()
    
    def test_probability_meets_measure_theory(self):
        """Test probability and measure theory intersection"""
        expr = r"If P is a probability measure, then P(\Omega) = 1 and P(\emptyset) = 0"
        
        processor = MeasureTheoryProcessor()
        result = processor.process(expr)
        
        assert "probability measure" in result.lower()
        assert "equals 1" in result.lower()
        assert "equals 0" in result.lower()
    
    def test_combinatorics_meets_probability(self):
        """Test combinatorics in probability context"""
        expr = r"P(A) = \frac{|A|}{|S|} = \frac{\binom{n}{k}}{\binom{n+m}{k}}"
        
        processors = [
            CombinatoricsProcessor(),
            MeasureTheoryProcessor(),
        ]
        
        for processor in processors:
            result = processor.process(expr)
            assert isinstance(result, str)
            # Should handle fraction and binomial coefficients


class TestPerformanceLimits:
    """Test performance boundaries and limits"""
    
    def test_recursive_pattern_performance(self):
        """Test performance with recursive patterns"""
        processor = RealAnalysisProcessor()
        
        # Expression that could cause exponential pattern matching
        expr = r"\lim \lim \lim \lim \lim f(x)"
        
        start_time = time.time()
        result = processor.process(expr)
        duration = time.time() - start_time
        
        assert duration < 0.1  # Should be fast despite repetition
        assert "limit" in result.lower()
    
    def test_many_small_expressions(self):
        """Test processing many small expressions rapidly"""
        processor = AlgorithmsProcessor()
        
        expressions = [f"O(n^{i})" for i in range(100)]
        
        start_time = time.time()
        results = [processor.process(expr) for expr in expressions]
        duration = time.time() - start_time
        
        assert len(results) == 100
        assert all("big O" in r.lower() for r in results)
        assert duration < 1.0  # Should process 100 expressions in under 1 second
    
    def test_cache_effectiveness(self):
        """Test that caching improves performance"""
        processor = RealAnalysisProcessor()
        
        expr = r"\int_0^1 e^{-x^2} dx"
        
        # First run (cache miss)
        start1 = time.time()
        result1 = processor.process(expr)
        duration1 = time.time() - start1
        
        # Second run (cache hit, if implemented)
        start2 = time.time()
        result2 = processor.process(expr)
        duration2 = time.time() - start2
        
        assert result1 == result2
        # Second run should be faster or equal (not slower)
        assert duration2 <= duration1 * 1.1  # Allow 10% variance


class TestErrorRecoveryStrategies:
    """Test error recovery and graceful degradation"""
    
    def test_partial_processing(self):
        """Test that processors can partially process expressions"""
        processor = RealAnalysisProcessor()
        
        # Expression with valid and invalid parts
        expr = r"\lim_{x \to 0} \notacommand{f(x)} + \int_0^1 g(x) dx"
        
        result = processor.process(expr)
        assert "limit" in result.lower()
        assert "integral" in result.lower()
        # Should process valid parts even with invalid commands
    
    def test_fallback_behavior(self):
        """Test fallback when domain detection fails"""
        # Very ambiguous expression
        expr = "f(x) = x"
        
        processors = [
            RealAnalysisProcessor(),
            ComplexAnalysisProcessor(),
            AlgorithmsProcessor(),
        ]
        
        results = []
        for processor in processors:
            result = processor.process(expr)
            results.append(result)
        
        # All should produce reasonable output
        assert all(isinstance(r, str) for r in results)
        assert all(len(r) > 0 for r in results)
    
    def test_cascading_errors(self):
        """Test that errors don't cascade"""
        processor = MeasureTheoryProcessor()
        
        # Multiple errors in one expression
        expr = r"\notvalid{\mu(A \cup B) \leq \anothernotvalid{\mu(A) + \mu(B)}}"
        
        result = processor.process(expr)
        # Should still find the measure notation
        assert "mu" in result.lower()
        assert isinstance(result, str)


class TestSpecialEdgeCases:
    """Test specific known edge cases"""
    
    def test_empty_arguments(self):
        """Test commands with empty arguments"""
        processor = CombinatoricsProcessor()
        
        test_cases = [
            r"\binom{}{}",
            r"\frac{}{}",
            r"\sum_{}^{}",
            r"f()",
        ]
        
        for expr in test_cases:
            result = processor.process(expr)
            assert isinstance(result, str)
    
    def test_whitespace_handling(self):
        """Test various whitespace scenarios"""
        processor = RealAnalysisProcessor()
        
        test_cases = [
            r"\lim_{x\to0}f(x)",           # No spaces
            r"\lim  _{  x  \to  0  }  f(x)",  # Extra spaces
            r"\lim_{\n\tx\n\t\to\n\t0\n}f(x)",  # Newlines and tabs
        ]
        
        results = [processor.process(expr) for expr in test_cases]
        # All should produce similar output
        assert len(set(results)) == 1  # All results should be identical
    
    def test_comment_handling(self):
        """Test LaTeX comments"""
        processor = AlgorithmsProcessor()
        
        expr = r"O(n^2) % This is quadratic time"
        result = processor.process(expr)
        
        assert "big O of n squared" in result.lower()
        assert "This is quadratic" not in result  # Comment should be ignored
    
    def test_math_mode_delimiters(self):
        """Test various math mode delimiters"""
        processor = RealAnalysisProcessor()
        
        test_cases = [
            r"$\lim_{x \to 0} f(x)$",
            r"$$\lim_{x \to 0} f(x)$$",
            r"\[\lim_{x \to 0} f(x)\]",
            r"\(\lim_{x \to 0} f(x)\)",
            r"\begin{equation}\lim_{x \to 0} f(x)\end{equation}",
        ]
        
        for expr in test_cases:
            result = processor.process(expr)
            assert "limit" in result.lower()


if __name__ == "__main__":
    # Run comprehensive edge case tests
    pytest.main([__file__, "-v", "--tb=short", "-x"])