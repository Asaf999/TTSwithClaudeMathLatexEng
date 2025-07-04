#!/usr/bin/env python3
"""
Extensive Test Suite for Measure Theory Domain Processor
=======================================================

This module provides comprehensive testing for the Measure Theory processor,
covering all major topics including:
- Sigma-algebras and measurable spaces
- Measures (finite, sigma-finite, probability, signed)
- Integration theory (Lebesgue integral)
- Lp spaces and convergence
- Product measures and Fubini's theorem
- Radon-Nikodym theorem
- Maximal functions and inequalities
"""

import pytest
import logging
from typing import List, Tuple, Dict, Any

from domains.measure_theory import MeasureTheoryProcessor, MeasureTheoryContext

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class TestMeasureTheoryProcessor:
    """Comprehensive test suite for Measure Theory processor"""
    
    @pytest.fixture
    def processor(self):
        """Create a Measure Theory processor instance"""
        return MeasureTheoryProcessor()
    
    # ===== SIGMA-ALGEBRAS =====
    
    def test_sigma_algebras(self, processor):
        """Test sigma-algebra notation"""
        test_cases = [
            (r"\mathcal{A}", "sigma-algebra script A"),
            (r"\mathcal{B}", "sigma-algebra script B"),
            (r"\mathcal{F}", "sigma-algebra script F"),
            (r"\sigma(\mathcal{C})", "sigma-algebra generated by script C"),
            (r"\sigma(A_1, A_2, \ldots)", "sigma-algebra generated by"),
            (r"\mathcal{B}(\mathbb{R})", "Borel sigma-algebra on the reals"),
            (r"\mathcal{B}(\mathbb{R}^n)", "Borel sigma-algebra on R n"),
            (r"\mathcal{L}", "Lebesgue sigma-algebra"),
            (r"\mathcal{P}(X)", "power set of X"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_measurability(self, processor):
        """Test measurability notation"""
        test_cases = [
            (r"f \text{ is measurable}", "measurable"),
            (r"f \text{ is } \mathcal{A}/\mathcal{B}\text{-measurable}", "script A over script B measurable"),
            (r"f^{-1}(B) \in \mathcal{A}", "f inverse of B is in script A"),
            (r"\{x : f(x) > a\} \in \mathcal{A}", "the set of x such that f of x is greater than a"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== MEASURES =====
    
    def test_basic_measures(self, processor):
        """Test basic measure notation"""
        test_cases = [
            (r"\mu", "mu"),
            (r"\nu", "nu"),
            (r"\lambda", "lambda"),
            (r"\mu(A)", "mu of A"),
            (r"\nu(B)", "nu of B"),
            (r"m(E)", "measure of E"),
            (r"\text{Leb}(A)", "Lebesgue measure of A"),
            (r"\mu^*", "mu star"),
            (r"\text{outer measure}", "outer measure"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_special_measures(self, processor):
        """Test special types of measures"""
        test_cases = [
            (r"\text{Hausdorff measure}", "Hausdorff measure"),
            (r"\mathcal{H}^s", "Hausdorff s-measure"),
            (r"\mathcal{H}^2", "Hausdorff 2-measure"),
            (r"\text{counting measure}", "counting measure"),
            (r"\text{Dirac measure}", "Dirac measure"),
            (r"\delta_x", "Dirac delta at x"),
            (r"\delta_0", "Dirac delta at 0"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_measure_properties(self, processor):
        """Test measure property terminology"""
        test_cases = [
            (r"\text{finite measure}", "finite measure"),
            (r"\text{sigma-finite}", "sigma-finite"),
            (r"\text{probability measure}", "probability measure"),
            (r"\text{signed measure}", "signed measure"),
            (r"\text{complex measure}", "complex measure"),
            (r"\text{regular measure}", "regular measure"),
            (r"\text{Radon measure}", "Radon measure"),
            (r"\mu \ll \nu", "mu is absolutely continuous with respect to nu"),
            (r"\mu \perp \nu", "mu is singular with respect to nu"),
            (r"|\mu|", "total variation of mu"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== INTEGRATION =====
    
    def test_lebesgue_integration(self, processor):
        """Test Lebesgue integration notation"""
        test_cases = [
            (r"\int f d\mu", "integral of f with respect to mu"),
            (r"\int f d\nu", "integral of f with respect to nu"),
            (r"\int_X f d\mu", "integral over X of f with respect to mu"),
            (r"\int_E f d\mu", "integral over E of f with respect to mu"),
            (r"\int f dx", "Lebesgue integral of f with respect to x"),
            (r"\text{Lebesgue integral}", "Lebesgue integral"),
            (r"\text{simple function}", "simple function"),
            (r"\text{measurable function}", "measurable function"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_integration_formulas(self, processor):
        """Test integration formulas"""
        test_cases = [
            (
                r"\int \sum_{i=1}^n a_i \mathbf{1}_{A_i} d\mu = \sum_{i=1}^n a_i \mu(A_i)",
                ["integral", "indicator function", "sum"]
            ),
            (
                r"\int f d\mu = \lim_{n \to \infty} \int s_n d\mu",
                ["integral of f", "limit as n approaches infinity"]
            ),
        ]
        
        for latex, expected_parts in test_cases:
            result = processor.process(latex)
            for part in expected_parts:
                assert part in result.lower(), \
                    f"Missing '{part}' in result for {latex}: got {result}"
    
    # ===== LP SPACES =====
    
    def test_lp_spaces(self, processor):
        """Test Lp space notation"""
        test_cases = [
            (r"L^p(X)", "L p space on X"),
            (r"L^2(X)", "L 2 space on X"),
            (r"L^p(X, \mu)", "L p space on X with measure mu"),
            (r"L^\infty(X)", "L infinity space on X"),
            (r"L^1(X, \mu)", "L 1 space on X with measure mu"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_lp_norms(self, processor):
        """Test Lp norm notation"""
        test_cases = [
            (r"\|f\|_p", "L p norm of f"),
            (r"\|f\|_2", "L 2 norm of f"),
            (r"\|f\|_\infty", "L infinity norm of f"),
            (r"\|f\|_{L^p}", "L p norm of f"),
            (r"\|f\|_{L^\infty}", "L infinity norm of f"),
            (r"\text{esssup}", "essential supremum"),
            (r"\text{essinf}", "essential infimum"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_lp_norm_definition(self, processor):
        """Test Lp norm definitions"""
        latex = r"\|f\|_p = \left(\int |f|^p d\mu\right)^{1/p}"
        result = processor.process(latex)
        
        assert "L p norm of f" in result.lower()
        assert "integral" in result.lower()
        assert "to the p" in result.lower()
    
    # ===== CONVERGENCE THEOREMS =====
    
    def test_convergence_theorems(self, processor):
        """Test major convergence theorems"""
        test_cases = [
            (r"\text{Monotone Convergence Theorem}", "monotone convergence theorem"),
            (r"\text{MCT}", "monotone convergence theorem"),
            (r"\text{Dominated Convergence Theorem}", "dominated convergence theorem"),
            (r"\text{DCT}", "dominated convergence theorem"),
            (r"\text{Fatou's Lemma}", "fatou's lemma"),
            (r"\text{Lebesgue's Dominated Convergence}", "dominated convergence"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_convergence_types(self, processor):
        """Test types of convergence"""
        test_cases = [
            (r"f_n \to f \text{ a.e.}", "converges to f almost everywhere"),
            (r"f_n \to f \text{ in measure}", "converges to f in measure"),
            (r"f_n \to f \text{ in } L^p", "converges to f in L p"),
            (r"\|f_n - f\|_p \to 0", "converges to zero"),
            (r"\text{pointwise convergence}", "pointwise convergence"),
            (r"\text{uniform convergence}", "uniform convergence"),
            (r"\text{weak convergence}", "weak convergence"),
            (r"\text{weak* convergence}", "weak star convergence"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert any(exp in result.lower() for exp in expected.lower().split()), \
                f"Failed for {latex}: got {result}"
    
    # ===== PRODUCT MEASURES =====
    
    def test_product_measures(self, processor):
        """Test product measure notation"""
        test_cases = [
            (r"\mu \times \nu", "mu cross nu"),
            (r"\text{product measure}", "product measure"),
            (r"\text{Fubini's theorem}", "fubini's theorem"),
            (r"\text{Tonelli's theorem}", "tonelli's theorem"),
            (r"\text{Fubini-Tonelli}", "fubini-tonelli"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_iterated_integrals(self, processor):
        """Test iterated integral notation"""
        test_cases = [
            (
                r"\iint f(x,y) d\mu(x) d\nu(y)",
                "double integral of f of x comma y"
            ),
            (
                r"\int \int f(x,y) dy dx",
                "iterated integral of f of x comma y d y d x"
            ),
            (
                r"\int \int f(x,y) dx dy",
                "iterated integral of f of x comma y d x d y"
            ),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== RADON-NIKODYM =====
    
    def test_radon_nikodym(self, processor):
        """Test Radon-Nikodym theorem notation"""
        test_cases = [
            (r"\text{Radon-Nikodym theorem}", "radon-nikodym theorem"),
            (r"\text{Radon-Nikodym derivative}", "radon-nikodym derivative"),
            (r"\frac{d\mu}{d\nu}", "radon-nikodym derivative of mu with respect to nu"),
            (r"\frac{d\mu}{d\lambda}", "radon-nikodym derivative of mu with respect to lambda"),
            (r"\text{density}", "density"),
            (r"d\mu = h d\nu", "d mu equals h d nu"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_decompositions(self, processor):
        """Test measure decomposition theorems"""
        test_cases = [
            (r"\text{Lebesgue decomposition}", "lebesgue decomposition"),
            (r"\text{Jordan decomposition}", "jordan decomposition"),
            (r"\text{Hahn decomposition}", "hahn decomposition"),
            (r"\mu = \mu_{ac} + \mu_s", "mu equals mu absolute continuous plus mu singular"),
            (r"\mu^+", "mu positive"),
            (r"\mu^-", "mu negative"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== SET OPERATIONS =====
    
    def test_set_operations(self, processor):
        """Test set operation notation"""
        test_cases = [
            (r"\limsup_{n \to \infty} A_n", "limit superior of A sub n"),
            (r"\liminf_{n \to \infty} A_n", "limit inferior of A sub n"),
            (r"\bigcup_{n=1}^\infty A_n", "union from n equals 1 to infinity"),
            (r"\bigcap_{n=1}^\infty A_n", "intersection from n equals 1 to infinity"),
            (r"\bigsqcup_{n=1}^\infty A_n", "disjoint union from n equals 1 to infinity"),
            (r"A \triangle B", "A symmetric difference B"),
            (r"A^c", "A complement"),
            (r"A \setminus B", "A minus B"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_indicator_functions(self, processor):
        """Test indicator/characteristic function notation"""
        test_cases = [
            (r"\mathbf{1}_A", "indicator function of A"),
            (r"\mathbf{1}_E", "indicator function of E"),
            (r"\chi_A", "characteristic function of A"),
            (r"\chi_B", "characteristic function of B"),
            (r"\text{indicator function}", "indicator function"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== SPECIAL SETS =====
    
    def test_special_sets(self, processor):
        """Test special set terminology"""
        test_cases = [
            (r"\text{null set}", "null set"),
            (r"\text{negligible set}", "negligible set"),
            (r"\text{almost everywhere}", "almost everywhere"),
            (r"\text{a.e.}", "almost everywhere"),
            (r"\text{almost surely}", "almost surely"),
            (r"\text{a.s.}", "almost surely"),
            (r"\text{support}", "support"),
            (r"\text{supp}(f)", "support of f"),
            (r"\text{supp}(\mu)", "support of mu"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    def test_measure_types(self, processor):
        """Test measure type terminology"""
        test_cases = [
            (r"\text{atoms}", "atoms"),
            (r"\text{atomic measure}", "atomic measure"),
            (r"\text{non-atomic measure}", "non-atomic measure"),
            (r"\text{purely atomic}", "purely atomic"),
            (r"\text{diffuse measure}", "diffuse measure"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== MAXIMAL FUNCTIONS =====
    
    def test_maximal_functions(self, processor):
        """Test maximal function notation"""
        test_cases = [
            (r"\text{maximal function}", "maximal function"),
            (r"\text{Hardy-Littlewood maximal function}", "hardy-littlewood maximal function"),
            (r"Mf", "maximal function of f"),
            (r"M(g)", "maximal function of g"),
            (r"\text{covering lemma}", "covering lemma"),
            (r"\text{Vitali covering}", "vitali covering"),
            (r"\text{Besicovitch covering}", "besicovitch covering"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            assert expected in result.lower(), f"Failed for {latex}: got {result}"
    
    # ===== INEQUALITIES =====
    
    def test_inequalities(self, processor):
        """Test famous inequalities in measure theory"""
        test_cases = [
            (r"\text{Hölder's inequality}", "hölder's inequality"),
            (r"\text{Minkowski's inequality}", "minkowski's inequality"),
            (r"\text{Jensen's inequality}", "jensen's inequality"),
            (r"\text{Markov's inequality}", "markov's inequality"),
            (r"\text{Chebyshev's inequality}", "chebyshev's inequality"),
            (r"\text{Cauchy-Schwarz inequality}", "cauchy-schwarz inequality"),
        ]
        
        for latex, expected in test_cases:
            result = processor.process(latex)
            # Handle special characters
            assert expected.replace("ö", "o").lower() in result.lower() or expected in result.lower(), \
                f"Failed for {latex}: got {result}"
    
    # ===== CONTEXT DETECTION =====
    
    def test_context_detection(self, processor):
        """Test that context is correctly detected"""
        test_cases = [
            (r"\mathcal{A} \text{ is a } \sigma\text{-algebra}", MeasureTheoryContext.SIGMA_ALGEBRAS),
            (r"\mu(A) < \infty", MeasureTheoryContext.MEASURES),
            (r"\int f d\mu", MeasureTheoryContext.INTEGRATION),
            (r"L^p(X, \mu)", MeasureTheoryContext.LP_SPACES),
            (r"f_n \to f \text{ a.e.}", MeasureTheoryContext.CONVERGENCE),
            (r"\mu \times \nu", MeasureTheoryContext.PRODUCT_MEASURES),
            (r"\frac{d\mu}{d\nu}", MeasureTheoryContext.RADON_NIKODYM),
        ]
        
        for latex, expected_context in test_cases:
            _ = processor.process(latex)
            assert processor.context == expected_context, \
                f"Wrong context for {latex}: got {processor.context}, expected {expected_context}"
    
    # ===== COMPLEX EXPRESSIONS =====
    
    def test_complex_expressions(self, processor):
        """Test complex measure theory expressions"""
        test_cases = [
            # Measure definition
            (
                r"\mu(\bigcup_{i=1}^\infty A_i) = \sum_{i=1}^\infty \mu(A_i) \text{ for disjoint } A_i",
                ["union from i equals 1 to infinity", "sum from i equals 1 to infinity", "disjoint"]
            ),
            # Dominated convergence
            (
                r"\text{If } |f_n| \leq g \text{ and } f_n \to f \text{ a.e., then } \int f_n d\mu \to \int f d\mu",
                ["less than or equal to", "converges to f almost everywhere", "integral"]
            ),
            # Fubini's theorem
            (
                r"\int_{X \times Y} f d(\mu \times \nu) = \int_X \left(\int_Y f(x,y) d\nu(y)\right) d\mu(x)",
                ["mu cross nu", "integral", "d nu of y", "d mu of x"]
            ),
        ]
        
        for latex, expected_parts in test_cases:
            result = processor.process(latex)
            for part in expected_parts:
                assert part in result.lower(), \
                    f"Missing '{part}' in result for {latex}: got {result}"
    
    # ===== ERROR HANDLING =====
    
    def test_error_handling(self, processor):
        """Test handling of edge cases and errors"""
        test_cases = [
            "",  # Empty string
            r"\mu(",  # Incomplete
            r"\int",  # Incomplete integral
            "plain text without latex",  # Plain text
        ]
        
        for latex in test_cases:
            result = processor.process(latex)
            assert isinstance(result, str)
    
    # ===== PERFORMANCE =====
    
    def test_performance(self, processor):
        """Test processing performance"""
        import time
        
        expressions = [
            r"\int_X f d\mu",
            r"L^p(X, \mu)",
            r"\mu \ll \nu",
            r"f_n \to f \text{ a.e.}",
            r"\mathcal{B}(\mathbb{R})",
        ] * 20  # 100 expressions
        
        start_time = time.time()
        for expr in expressions:
            _ = processor.process(expr)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time = total_time / len(expressions)
        
        assert avg_time < 0.01, f"Processing too slow: {avg_time:.4f}s per expression"


# ===== INTEGRATION TESTS =====

class TestMeasureTheoryIntegration:
    """Integration tests with other components"""
    
    def test_with_tts_compatibility(self):
        """Test output compatibility with TTS engines"""
        processor = MeasureTheoryProcessor()
        
        test_cases = [
            r"\mu \ll \nu",
            r"\int_{\mathbb{R}} f d\lambda",
            r"L^2(\mathbb{R}, \lambda)",
        ]
        
        for latex in test_cases:
            result = processor.process(latex)
            # No special characters that break TTS
            assert all(ord(c) < 128 or c in "µλ" for c in result), \
                f"Non-ASCII characters found in: {result}"


# ===== PARAMETRIZED TESTS =====

@pytest.mark.parametrize("measure,name", [
    (r"\mu", "mu"),
    (r"\nu", "nu"),
    (r"\lambda", "lambda"),
    (r"\rho", "rho"),
])
def test_measure_symbols(measure, name):
    """Test measure symbol recognition"""
    processor = MeasureTheoryProcessor()
    result = processor.process(measure)
    assert name in result.lower()


@pytest.mark.parametrize("space,expected", [
    (r"\mathcal{B}(\mathbb{R})", "borel sigma-algebra"),
    (r"\mathcal{L}", "lebesgue sigma-algebra"),
    (r"L^1(X)", "L 1 space"),
    (r"L^2(X)", "L 2 space"),
    (r"L^\infty(X)", "L infinity space"),
])
def test_standard_spaces(space, expected):
    """Test standard space recognition"""
    processor = MeasureTheoryProcessor()
    result = processor.process(space)
    assert expected in result.lower()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])