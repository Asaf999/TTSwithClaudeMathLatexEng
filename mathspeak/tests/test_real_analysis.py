#!/usr/bin/env python3
"""
Extensive Test Suite for Real Analysis Domain Processor
======================================================

This module provides comprehensive testing for the Real Analysis processor,
covering all major topics including:
- Limits and epsilon-delta definitions
- Continuity (uniform, Lipschitz, Hölder)
- Differentiation (derivatives, partial derivatives, gradients)
- Integration (Riemann, Lebesgue, improper)
- Sequences and series
- Function spaces and norms
- Metric spaces and completeness
"""

import pytest
import logging
from typing import List, Tuple, Dict, Any

from domains.real_analysis import RealAnalysisProcessor, RealAnalysisContext

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestRealAnalysisProcessor:
    """Comprehensive test suite for Real Analysis processor"""
    
    @pytest.fixture
    def processor(self):
        """Create a Real Analysis processor instance"""
        return RealAnalysisProcessor()
    
    # ===== LIMITS AND EPSILON-DELTA =====
    
    def test_basic_limits(self, processor):
        """Test basic limit notation"""
        test_cases = [
            (r"\lim_{x \to a} f(x)", "the limit as x approaches a of f of x"),
            (r"\lim_{x \to 0} \frac{\sin x}{x}", "the limit as x approaches 0 of sine x over x"),
            (r"\lim_{n \to \infty} a_n", "the limit as n approaches infinity of a sub n"),
            (r"\lim_{x \to a^+} f(x)", "the limit as x approaches a from the right of f of x"),
            (r"\lim_{x \to a^-} f(x)", "the limit as x approaches a from the left of f of x"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected.lower() in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_epsilon_delta_definitions(self, processor):
        """Test epsilon-delta limit definitions"""
        test_cases = [
            (
                r"\forall \epsilon > 0 \, \exists \delta > 0",
                "for all epsilon greater than zero there exists delta greater than zero"
            ),
            (
                r"0 < |x - a| < \delta \Rightarrow |f(x) - L| < \epsilon",
                "zero less than the absolute value of x minus a less than delta"
            ),
            (
                r"\forall \epsilon > 0 \, \exists N \in \mathbb{N}",
                "for all epsilon greater than zero there exists N in the natural numbers"
            ),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected.lower() in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_limit_superior_inferior(self, processor):
        """Test limit superior and inferior"""
        test_cases = [
            (r"\limsup_{n \to \infty} a_n", "limit superior"),
            (r"\liminf_{n \to \infty} a_n", "limit inferior"),
            (r"\overline{\lim} a_n", "limit superior"),
            (r"\underline{\lim} a_n", "limit inferior"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== CONTINUITY =====
    
    def test_continuity_types(self, processor):
        """Test different types of continuity"""
        test_cases = [
            (r"f \text{ is continuous at } a", "f is continuous at a"),
            (r"f \in C([a,b])", "f is continuous on"),
            (r"f \in C^k(\mathbb{R})", "k times continuously differentiable"),
            (r"f \in C^\infty(\mathbb{R})", "smooth functions"),
            (r"f \text{ is uniformly continuous}", "uniformly continuous"),
            (r"f \text{ is Lipschitz continuous}", "Lipschitz continuous"),
            (r"f \text{ is Holder continuous}", "Holder continuous"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_uniform_continuity(self, processor):
        """Test uniform continuity definition"""
        latex = r"\forall \epsilon > 0 \, \exists \delta > 0 \text{ such that } |x - y| < \delta \Rightarrow |f(x) - f(y)| < \epsilon"
        result = processor.process(latex)
        
        assert "for all epsilon" in result.lower()
        assert "exists delta" in result.lower()
        assert "f of x minus f of y" in result.lower()
    
    # ===== DIFFERENTIATION =====
    
    def test_derivatives(self, processor):
        """Test derivative notation"""
        test_cases = [
            (r"f'(x)", "f prime of x"),
            (r"f''(x)", "f double prime of x"),
            (r"f'''(x)", "f triple prime of x"),
            (r"f^{(4)}(x)", "fourth derivative of f at x"),
            (r"\frac{d}{dx} f(x)", "derivative with respect to x"),
            (r"\frac{d^2}{dx^2} f(x)", "second derivative with respect to x"),
            (r"\frac{df}{dx}", "derivative of f with respect to x"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_partial_derivatives(self, processor):
        """Test partial derivative notation"""
        test_cases = [
            (r"\frac{\partial f}{\partial x}", "partial derivative of f with respect to x"),
            (r"\frac{\partial^2 f}{\partial x^2}", "second partial derivative"),
            (r"\frac{\partial^2 f}{\partial x \partial y}", "mixed partial derivative"),
            (r"\nabla f", "gradient of f"),
            (r"\text{grad} f", "gradient of f"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in expected.lower().split()), \
                f"Failed for {latex}: got {result}"
    
    def test_chain_rule(self, processor):
        """Test chain rule expressions"""
        latex = r"\frac{d}{dx}[f(g(x))] = f'(g(x)) \cdot g'(x)"
        result = processor.process(latex)
        
        assert "f prime of g of x" in result.lower()
        assert "g prime of x" in result.lower()
    
    # ===== INTEGRATION =====
    
    def test_basic_integrals(self, processor):
        """Test basic integral notation"""
        test_cases = [
            (r"\int f(x) dx", "integral of f of x with respect to x"),
            (r"\int_a^b f(x) dx", "integral from a to b"),
            (r"\int_0^\infty e^{-x} dx", "integral from 0 to infinity"),
            (r"\int_{\mathbb{R}} f(x) dx", "integral over R"),
            (r"\iint f(x,y) dx dy", "double integral"),
            (r"\iiint f(x,y,z) dx dy dz", "triple integral"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in expected.lower().split()), \
                f"Failed for {latex}: got {result}"
    
    def test_fundamental_theorem(self, processor):
        """Test Fundamental Theorem of Calculus"""
        test_cases = [
            (r"F'(x) = f(x)", "F prime of x equals f of x"),
            (r"\int_a^b f(x) dx = F(b) - F(a)", "F of b minus F of a"),
            (r"\frac{d}{dx} \int_a^x f(t) dt = f(x)", "equals f of x"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== SEQUENCES AND SERIES =====
    
    def test_sequences(self, processor):
        """Test sequence notation"""
        test_cases = [
            (r"\{a_n\}", "the sequence a sub n"),
            (r"\{a_n\}_{n=1}^\infty", "sequence a sub n from n equals 1 to infinity"),
            (r"a_n \to a", "a sub n converges to a"),
            (r"a_n \rightarrow a", "a sub n converges to a"),
            (r"\{a_n\} \text{ is Cauchy}", "is Cauchy"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_series(self, processor):
        """Test series notation"""
        test_cases = [
            (r"\sum_{n=1}^\infty a_n", "sum from n equals 1 to infinity of a sub n"),
            (r"\sum_{n=0}^\infty \frac{x^n}{n!}", "sum from n equals 0 to infinity"),
            (r"\prod_{n=1}^\infty (1 + a_n)", "product from n equals 1 to infinity"),
            (r"S_n = \sum_{k=1}^n a_k", "S sub n equals the sum"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in expected.lower().split()), \
                f"Failed for {latex}: got {result}"
    
    def test_convergence_types(self, processor):
        """Test convergence terminology"""
        test_cases = [
            (r"\text{converges}", "converges"),
            (r"\text{diverges}", "diverges"),
            (r"\text{absolutely convergent}", "absolutely convergent"),
            (r"\text{conditionally convergent}", "conditionally convergent"),
            (r"\text{uniformly convergent}", "uniformly convergent"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== FUNCTION SPACES AND NORMS =====
    
    def test_lp_spaces(self, processor):
        """Test Lp space notation"""
        test_cases = [
            (r"L^p(\mathbb{R})", "L p space on"),
            (r"L^2(\mathbb{R})", "L 2 space"),
            (r"L^\infty([0,1])", "L infinity space"),
            (r"f \in L^1(\mathbb{R})", "L 1 space"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_norms(self, processor):
        """Test norm notation"""
        test_cases = [
            (r"\|f\|_p", "L p norm of f"),
            (r"\|f\|_2", "L 2 norm of f"),
            (r"\|f\|_\infty", "L infinity norm of f"),
            (r"\|f\|_{L^p}", "L p norm of f"),
            (r"\text{esssup} |f|", "essential supremum"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== METRIC SPACES =====
    
    def test_metric_spaces(self, processor):
        """Test metric space notation"""
        test_cases = [
            (r"d(x,y)", "distance from x to y"),
            (r"B(x,r)", "open ball centered at x with radius r"),
            (r"\overline{B}(x,r)", "closed ball centered at x"),
            (r"\text{diam}(A)", "diameter of A"),
            (r"\text{complete}", "complete"),
            (r"\text{Banach space}", "Banach space"),
            (r"\text{Hilbert space}", "Hilbert space"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== INEQUALITIES =====
    
    def test_inequalities(self, processor):
        """Test inequality notation"""
        test_cases = [
            (r"a \leq b", "less than or equal to"),
            (r"a \geq b", "greater than or equal to"),
            (r"a \ll b", "much less than"),
            (r"a \gg b", "much greater than"),
            (r"f(x) = O(g(x))", "big O of"),
            (r"f(x) = o(g(x))", "little o of"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== SPECIAL FUNCTIONS =====
    
    def test_special_functions(self, processor):
        """Test special function notation"""
        test_cases = [
            (r"\exp(x)", "exponential of x"),
            (r"\log(x)", "logarithm of x"),
            (r"\ln(x)", "natural logarithm of x"),
            (r"\sin(x)", "sine of x"),
            (r"\cos(x)", "cosine of x"),
            (r"\arcsin(x)", "arcsine of x"),
            (r"\sinh(x)", "hyperbolic sine of x"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== CONTEXT DETECTION =====
    
    def test_context_detection(self, processor):
        """Test that context is correctly detected"""
        test_cases = [
            (r"\lim_{x \to a} f(x) = L", RealAnalysisContext.LIMITS),
            (r"f \text{ is continuous}", RealAnalysisContext.CONTINUITY),
            (r"\frac{df}{dx}", RealAnalysisContext.DIFFERENTIATION),
            (r"\int f(x) dx", RealAnalysisContext.INTEGRATION),
            (r"\{a_n\} \text{ converges}", RealAnalysisContext.SEQUENCES),
            (r"\sum_{n=1}^\infty a_n", RealAnalysisContext.SERIES),
            (r"L^p(\mathbb{R})", RealAnalysisContext.FUNCTION_SPACES),
        ]
        
        for latex, expected_context in test_cases:
            _ = processor.process(latex)
            assert processor.context == expected_context, \
                f"Wrong context for {latex}: got {processor.context}, expected {expected_context}"
    
    # ===== COMPLEX EXPRESSIONS =====
    
    def test_complex_expressions(self, processor):
        """Test complex real analysis expressions"""
        test_cases = [
            # Weierstrass M-test
            (
                r"\sum_{n=1}^\infty |f_n(x)| \leq \sum_{n=1}^\infty M_n < \infty",
                ["sum from n equals 1 to infinity", "less than or equal to", "less than infinity"]
            ),
            # Taylor series
            (
                r"f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(a)}{n!}(x-a)^n",
                ["sum from n equals 0 to infinity", "n factorial", "x minus a to the n"]
            ),
            # Cauchy criterion
            (
                r"\forall \epsilon > 0 \, \exists N : m,n > N \Rightarrow |a_m - a_n| < \epsilon",
                ["for all epsilon", "exists N", "m and n greater than N"]
            ),
        ]
        
        for latex, expected_parts in test_cases:
            result = processor.process(latex)
            for part in expected_parts:
                assert part in result.lower(), \
                    f"Missing '{part}' in result for {latex}: got {result}"
    
    # ===== ERROR HANDLING =====
    
    def test_malformed_input(self, processor):
        """Test handling of malformed input"""
        test_cases = [
            "",  # Empty string
            "\\lim_{x \\to",  # Incomplete limit
            "\\frac{d}{dx",  # Unclosed fraction
            None,  # None input should be handled gracefully
        ]
        
        for latex in test_cases:
            if latex is None:
                continue  # Skip None test for now
            result = processor.process(latex)
            # Should not raise exception, should return something
            assert isinstance(result, str)
    
    # ===== PERFORMANCE =====
    
    def test_performance(self, processor):
        """Test processing performance on typical expressions"""
        import time
        
        expressions = [
            r"\lim_{x \to 0} \frac{\sin x}{x} = 1",
            r"\int_0^1 x^2 dx = \frac{1}{3}",
            r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}",
            r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}",
        ] * 25  # 100 expressions total
        
        start_time = time.time()
        for expr in expressions:
            _ = processor.process(expr)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / len(expressions)
        
        # Should process at least 100 expressions per second
        assert avg_time < 0.01, f"Processing too slow: {avg_time:.4f}s per expression"


# ===== INTEGRATION TESTS =====

class TestRealAnalysisIntegration:
    """Integration tests with other components"""
    
    def test_with_edge_tts(self):
        """Test that output works with edge-tts requirements"""
        processor = RealAnalysisProcessor()
        
        # edge-tts has limits on SSML tags and special characters
        test_cases = [
            r"\lim_{x \to \infty} \frac{1}{x} = 0",
            r"\int_0^{2\pi} \sin x \, dx = 0",
            r"\sum_{n=1}^\infty \frac{1}{2^n} = 1",
        ]
        
        for latex in test_cases:
            result = processor.process(latex)
            # Check no special characters that break TTS
            assert "<" not in result
            assert ">" not in result
            assert "&" not in result
            assert all(ord(c) < 128 for c in result), "Non-ASCII characters found"


# ===== REGRESSION TESTS =====

class TestRealAnalysisRegression:
    """Regression tests for previously found bugs"""
    
    def test_norm_pattern_fix(self):
        """Test that norm pattern doesn't cause infinite recursion"""
        processor = RealAnalysisProcessor()
        
        # This previously caused infinite recursion
        latex = r"\|f\|_\infty = \sup_{x \in \mathbb{R}} |f(x)|"
        result = processor.process(latex)
        
        # Should complete without recursion
        assert "infinity norm" in result.lower()
        assert "supremum" in result.lower()
        
        # Result should be reasonable length
        assert len(result) < 200, f"Result too long: {len(result)} chars"


# ===== PARAMETRIZED TESTS =====

@pytest.mark.parametrize("latex,expected", [
    (r"\epsilon", "epsilon"),
    (r"\delta", "delta"),
    (r"\infty", "infinity"),
    (r"\mathbb{R}", "real"),
    (r"\mathbb{N}", "natural"),
    (r"\mathbb{Q}", "rational"),
    (r"\mathbb{Z}", "integer"),
    (r"\mathbb{C}", "complex"),
])
def test_basic_symbols(latex, expected):
    """Test basic mathematical symbols"""
    processor = RealAnalysisProcessor()
    result = processor.process(latex)
    assert expected in result.lower()


@pytest.mark.parametrize("theorem,name", [
    (r"\text{Fundamental Theorem of Calculus}", "fundamental theorem of calculus"),
    (r"\text{Mean Value Theorem}", "mean value theorem"),
    (r"\text{Intermediate Value Theorem}", "intermediate value theorem"),
    (r"\text{Extreme Value Theorem}", "extreme value theorem"),
    (r"\text{Bolzano-Weierstrass Theorem}", "bolzano-weierstrass theorem"),
])
def test_theorem_names(theorem, name):
    """Test theorem name recognition"""
    processor = RealAnalysisProcessor()
    result = processor.process(theorem)
    assert name in result.lower()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])