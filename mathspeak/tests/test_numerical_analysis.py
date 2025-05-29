#!/usr/bin/env python3
"""
Test Suite for the Numerical Analysis Domain Processor (mathspeak.domains.numerical_analysis)
==========================================================================================

Ensures comprehensive coverage for numerical analysis notation processing,
from undergraduate basics to M.Sc. level concepts.
"""

import pytest
import re # For more complex assertion needs if any

# Module to be tested
from mathspeak.domains.numerical_analysis import (
    NumericalAnalysisProcessor,
    NumericalContext,
    NumericalAnalysisVocabulary,
)

# --- Helper Functions ---

def assert_spoken_contains(spoken_text, expected_keywords, all_must_be_present=True):
    """
    Asserts that expected keywords are in the spoken text (case-insensitive).
    If all_must_be_present is True, all keywords must be found.
    If all_must_be_present is False, at least one keyword must be found.
    """
    if isinstance(expected_keywords, str):
        expected_keywords = [expected_keywords]

    found_any = False
    missing_keywords = []

    for keyword in expected_keywords:
        if keyword.lower() in spoken_text.lower():
            found_any = True
        else:
            missing_keywords.append(keyword)

    if all_must_be_present:
        assert not missing_keywords, f"Keywords {missing_keywords} not found in '{spoken_text}'"
    else:
        assert found_any, f"None of the keywords {expected_keywords} found in '{spoken_text}'"

# --- Fixtures ---

@pytest.fixture(scope="module")
def processor():
    """Provides a NumericalAnalysisProcessor instance for testing (module scope)."""
    return NumericalAnalysisProcessor()

@pytest.fixture(scope="module")
def vocabulary():
    """Provides a NumericalAnalysisVocabulary instance for testing (module scope)."""
    return NumericalAnalysisVocabulary()

# --- Test Classes ---

class TestNumericalAnalysisVocabulary:
    """Tests for the NumericalAnalysisVocabulary component."""

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Error Analysis
        (r"O(h^n)", ["big O of h to the n"]),
        (r"O(h^2)", ["big O of h squared"]),
        (r"O(n \\log n)", ["big O of n log n"]),
        (r"O(1)", ["big O of 1"]),
        (r"\\Theta(N)", ["big theta of N"]), # Case for N
        (r"\\Omega(N^2)", ["big omega of N squared"]),
        (r"o(h^3)", ["little o of h cubed"]),
        (r"\\epsilon_{machine}", ["machine epsilon"]),
        (r"\\epsilon_{mach}", ["machine epsilon"]),
        (r"\\text{eps}", ["epsilon"]), # General epsilon
        (r"e_{abs}", ["absolute error"]),
        (r"e_{rel}", ["relative error"]),
        (r"\\|e\\|_\\infty", ["infinity norm of the error"]),
        (r"\\|e\\|_2", ["2-norm of the error"]),
        (r"\\text{linear convergence}", ["linear convergence"]),
        (r"\\text{quadratic convergence}", ["quadratic convergence"]),
        (r"\\text{superlinear convergence}", ["superlinear convergence"]),
        (r"\\text{order } p", ["order p"]),
        (r"\\kappa(A)", ["condition number of A"]),
        (r"\\text{cond}(B)", ["condition number of B"]), # Test with different matrix name
        (r"\\kappa_2(M)", ["2-norm condition number of M"]),
        (r"\\kappa_\\infty(N)", ["infinity-norm condition number of N"]),

        # Iterative Methods
        (r"x^{(k+1)}", ["x superscript k plus 1"]),
        (r"x^{(k)}", ["x superscript k"]),
        (r"x_k", ["x sub k"]),
        (r"x_{k+1}", ["x sub k plus 1"]),
        (r"\\text{iterate}", ["iterate"]),
        (r"\\text{iteration}", ["iteration"]),
        (r"\\text{Newton's method}", ["Newton's method"]),
        (r"\\text{Newton-Raphson}", ["Newton-Raphson method"]),
        (r"\\text{bisection method}", ["bisection method"]),
        (r"\\text{secant method}", ["secant method"]),
        (r"\\text{fixed-point iteration}", ["fixed-point iteration"]),
        (r"\\text{Jacobi method}", ["Jacobi method"]),
        (r"\\text{Gauss-Seidel}", ["Gauss-Seidel method"]),
        (r"\\text{SOR}", ["successive over-relaxation"]),
        (r"\\text{conjugate gradient}", ["conjugate gradient method"]),
        (r"\\text{GMRES}", ["GMRES"]),
        (r"\\|r_k\\| < \\epsilon", ["norm of the residual r sub k is less than epsilon"]),

        # Matrix Computations
        (r"A = LU", ["A equals L U"]),
        (r"A = QR", ["A equals Q R"]),
        (r"A = U\\Sigma V^T", ["A equals U Sigma V transpose"]),
        (r"A = U\\Sigma V^H", ["A equals U Sigma V Hermitian"]), # V^* is V^H
        (r"PA = LU", ["P A equals L U"]),
        (r"A = LL^T", ["A equals L L transpose"]), # Cholesky
        (r"\\text{upper triangular}", ["upper triangular"]),
        (r"\\text{lower triangular}", ["lower triangular"]),
        (r"\\text{diagonal}", ["diagonal"]),
        (r"\\text{tridiagonal}", ["tridiagonal"]),
        (r"\\text{sparse}", ["sparse"]),
        (r"\\text{dense}", ["dense"]),
        (r"\\text{symmetric}", ["symmetric"]),
        (r"\\text{positive definite}", ["positive definite"]),
        (r"\\text{orthogonal}", ["orthogonal"]),
        (r"\\text{unitary}", ["unitary"]),
        (r"A^{-1}", ["A inverse"]),
        (r"A^T", ["A transpose"]),
        (r"A^H", ["A Hermitian"]), # A^* is A^H
        (r"\\|A\\|_F", ["Frobenius norm of A"]),
        (r"\\|A\\|_1", ["1-norm of A"]),
        (r"\\lambda_{max}", ["lambda max"]),
        (r"\\lambda_{min}", ["lambda min"]),
        (r"\\lambda_i", ["lambda sub i"]),
        (r"\\text{eigenvalue}", ["eigenvalue"]),
        (r"\\text{eigenvector}", ["eigenvector"]),
        (r"\\text{spectrum}", ["spectrum"]),
        (r"\\rho(A)", ["spectral radius of A"]),

        # Interpolation
        (r"\\text{linear interpolation}", ["linear interpolation"]),
        (r"\\text{polynomial interpolation}", ["polynomial interpolation"]),
        (r"\\text{Lagrange interpolation}", ["Lagrange interpolation"]),
        (r"\\text{Newton interpolation}", ["Newton interpolation"]),
        (r"\\text{Hermite interpolation}", ["Hermite interpolation"]),
        (r"\\text{spline interpolation}", ["spline interpolation"]),
        (r"\\text{cubic spline}", ["cubic spline"]),
        (r"p_n(x)", ["p sub n of x"]),
        (r"L_k(x)", ["L sub k of x"]),
        (r"\\ell_j(y)", ["ell sub j of y"]), # Different var and index
        (r"\\pi_n", ["pi sub n"]),
        (r"f[x_0, x_1]", ["f bracket x naught comma x one bracket"]),
        (r"f[a, b, c]", ["f bracket a comma b comma c bracket"]),
        (r"\\text{divided difference}", ["divided difference"]),
        (r"\\|f - p_n\\|_\\infty", ["infinity norm of f minus p sub n"]),

        # Quadrature
        (r"\\text{trapezoidal rule}", ["trapezoidal rule"]),
        (r"\\text{Simpson's rule}", ["Simpson's rule"]),
        (r"\\text{midpoint rule}", ["midpoint rule"]),
        (r"\\text{Gaussian quadrature}", ["Gaussian quadrature"]),
        (r"\\text{Gauss-Legendre}", ["Gauss-Legendre quadrature"]),
        (r"\\text{composite rule}", ["composite rule"]),
        (r"\\text{adaptive quadrature}", ["adaptive quadrature"]),
        (r"Q_n(f)", ["Q sub n of f"]),
        (r"I(g)", ["I of g"]), # Different function name
        (r"w_i", ["w sub i"]),
        (r"x_j", ["x sub j"]), # Different index
        (r"\\text{weights}", ["weights"]),
        (r"\\text{nodes}", ["nodes"]),
        (r"E_n(f)", ["E sub n of f"]),

        # Finite Differences
        (r"\\Delta f_i", ["delta f sub i"]),
        (r"\\Delta_h g(y)", ["delta h g of y"]),
        (r"f_{i+1} - f_i", ["f sub i plus 1 minus f sub i"]),
        (r"\\nabla u_j", ["nabla u sub j"]),
        (r"g_k - g_{k-1}", ["g sub k minus g sub k minus 1"]),
        (r"\\delta y_m", ["delta y sub m"]),
        (r"\\text{stencil}", ["stencil"]),
        (r"\\text{5-point stencil}", ["five-point stencil"]),

        # Stability and Floating Point
        (r"\\text{stable}", ["stable"]),
        (r"\\text{unstable}", ["unstable"]),
        (r"\\text{conditionally stable}", ["conditionally stable"]),
        (r"\\text{backward stable}", ["backward stable"]),
        (r"fl(x)", ["floating-point representation of x"]),
        (r"\\text{round}(y)", ["round of y"]),
        (r"\\text{chop}(z)", ["chop of z"]),
        (r"\\text{ulp}", ["unit in the last place"]),
        (r"\\text{overflow}", ["overflow"]),
        (r"\\text{underflow}", ["underflow"]),
        (r"\\text{cancellation}", ["cancellation"]),
        (r"\\text{IEEE 754}", ["IEEE 754"]),
        (r"\\text{single precision}", ["single precision"]),
        (r"\\text{double precision}", ["double precision"]),
    ])
    def test_direct_vocabulary_terms(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        (r"x_{n+1} = x_n - \\frac{f(x_n)}{f'(x_n)}", ["x sub n plus 1 equals x sub n minus f of x sub n over f prime of x sub n"]),
        (r"x_{i+1} = g(x_i)", ["x sub i plus 1 equals g of x sub i"]),
        (r"\\|x_{k+1} - x_k\\| < \\text{tol}", ["norm of x sub k plus 1 minus x sub k is less than tolerance"]), # 'tol' is preprocessed
        (r"L_k(x) = \\prod_{j \\neq k} \\frac{x - x_j}{x_k - x_j}", ["L sub k of x equals the product over j not equal to k of x minus x sub j over x sub k minus x sub j"]),
        (r"\\int_a^b f(x)dx \\approx \\sum_{i=0}^n w_i f(x_i)", ["integral from a to b of f of x d x is approximately the sum from i equals 0 to n of w sub i times f of x sub i"]),
        (r"f'_i \\approx \\frac{f_{i+1} - f_i}{h}", ["f prime sub i is approximately f sub i plus 1 minus f sub i over h"]),
        (r"f''_j \\approx \\frac{f_{j+1} - 2f_j + f_{j-1}}{h^2}", ["f double prime sub j is approximately f sub j plus 1 minus 2 f sub j plus f sub j minus 1 over h squared"]),
    ])
    def test_lambda_vocabulary_terms(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)


class TestNumericalAnalysisPatterns:
    """Tests for the regex patterns defined for general numerical analysis phrases."""
    @pytest.mark.parametrize("latex_input, expected_keywords", [
        ("The sequence $x_k \\to x^*$ as $k \\to \\infty$.", ["x sub k converges to x star", "k goes to infinity"]),
        ("We know that $\\|x_k - x^*\\| \\leq C\\rho^k$.", ["norm of x sub k minus x star", "less than or equal to C times rho to the k"]),
        ("This method converges with order p.", ["converges with order p"]),
        ("The error bound is $\\|error\\| \\leq Ch^p$.", ["norm of the error", "less than or equal to C times h to the p"]),
        ("The relative error is defined as $\\frac{\\|x - \\tilde{x}\\|}{\\|x\\|}$.", ["relative error equals", "norm of x minus x tilde over the norm of x"]),
        ("The algorithm iterates for $k = 0, 1, 2, \\ldots, N$.", ["algorithm iterates for k equals 0, 1, 2, and so on, N"]), # Check "..."
        ("We repeat until convergence is achieved.", ["repeat until convergence"]),
        ("The loop continues while $\\|r_k\\| > tol$.", ["loop continues while the norm of r sub k is greater than tolerance"]),
        ("We need to solve $Ax = b$ for $x$.", ["solve A x equals b for x"]),
        ("Matrix $A \\in \\mathbb{R}^{m \\times n}$ is rectangular.", ["Matrix A is in R m by n", "rectangular"]),
        ("If $A$ is symmetric positive definite, Cholesky can be used.", ["A is symmetric positive definite", "Cholesky"]),
        ("This step requires $O(N^3)$ operations.", ["requires big O of N cubed operations"]),
        ("The storage is $O(N^2)$.", ["storage is big O of N squared"]),
        ("The finite difference operator $\\Delta_x^2 u$ approximates the second derivative.", ["delta x squared u", "approximates the second derivative"]),
        ("The stability condition is often related to the CFL condition.", ["stability condition", "CFL condition"]),
    ])
    def test_general_patterns(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)


class TestNumericalAnalysisSubContextDetection:
    @pytest.mark.parametrize("latex_input, expected_context_enum", [
        ("The local truncation error is $O(h^2)$.", NumericalContext.ERROR_ANALYSIS),
        ("Newton's method $x_{n+1} = x_n - f(x_n)/f'(x_n)$ is an iterative scheme.", NumericalContext.ITERATIVE_METHODS),
        ("The LU decomposition of $A$ is $A=LU$.", NumericalContext.MATRIX_COMPUTATIONS),
        ("Lagrange polynomial interpolation uses basis functions $L_k(x)$.", NumericalContext.INTERPOLATION),
        ("Simpson's rule for numerical quadrature is $\\int_a^b f(x)dx \\approx \\frac{h}{3}(\\ldots)$.", NumericalContext.QUADRATURE),
        ("The gradient descent algorithm is used for optimization.", NumericalContext.OPTIMIZATION),
        ("The Euler method $y_{i+1} = y_i + h f(t_i, y_i)$ solves ODEs.", NumericalContext.DIFFERENTIAL_EQUATIONS), # Assuming this context
        ("A general statement about computational mathematics.", NumericalContext.GENERAL),
    ])
    def test_sub_context_detection(self, processor, latex_input, expected_context_enum):
        assert processor.detect_subcontext(latex_input) == expected_context_enum


class TestNumericalAnalysisProcessing:
    """End-to-end tests for NumericalAnalysisProcessor.process()."""

    def test_newton_method_description(self, processor):
        latex = "Newton's method for finding a root of $f(x)=0$ is given by the iteration $x_{k+1} = x_k - \\frac{f(x_k)}{f'(x_k)}$, which exhibits quadratic convergence if $f'(x^*) \\neq 0$."
        spoken_text = processor.process(latex)
        expected = [
            "Newton's method", "finding a root of f of x equals 0", "iteration",
            "x sub k plus 1 equals x sub k minus f of x sub k over f prime of x sub k",
            "quadratic convergence", "f prime of x star is not equal to 0"
        ]
        assert_spoken_contains(spoken_text, expected)

    def test_matrix_factorization_and_error(self, processor):
        latex = "The $QR$ factorization $A=QR$ is used in solving least squares. The error is often $O(\\epsilon_{mach} \\kappa(A))$."
        spoken_text = processor.process(latex)
        expected = [
            "Q R factorization A equals Q R", "solving least squares",
            "error is often big O of machine epsilon times condition number of A"
        ]
        assert_spoken_contains(spoken_text, expected)

    def test_composite_quadrature_rule(self, processor):
        latex = "The composite trapezoidal rule for $\\int_a^b g(t)dt$ has an error term $E_n(g) = O(h^2)$."
        spoken_text = processor.process(latex)
        expected = [
            "composite trapezoidal rule", "integral from a to b of g of t d t",
            "error term E sub n of g equals big O of h squared"
        ]
        assert_spoken_contains(spoken_text, expected)


class TestNumericalAnalysisSpecialRules:
    """Tests for specific rules like stability emphasis or algorithm clarifications."""

    @pytest.mark.parametrize("stability_term_latex, stability_term_spoken", [
        ("The method is stable.", "stable"),
        ("This scheme is unstable.", "unstable"),
        ("The problem is ill-conditioned.", "ill-conditioned"),
        ("A well-conditioned matrix.", "well-conditioned"),
    ])
    def test_stability_emphasis(self, processor, stability_term_latex, stability_term_spoken):
        processor.special_rules['emphasize_stability'] = True
        spoken_text = processor.process(stability_term_latex)
        # Check if the emphasis markers are present around the term
        processed_by_domain_rule = processor._apply_special_rules(stability_term_spoken) # Test rule directly
        assert "{{EMPHASIS}}" in processed_by_domain_rule
        assert "{{/EMPHASIS}}" in processed_by_domain_rule
        assert stability_term_spoken.lower() in processed_by_domain_rule.lower().replace("{{emphasis}}","").replace("{{/emphasis}}","")


    def test_algorithm_clarification_newton(self, processor):
        processor.special_rules['clarify_algorithms'] = True
        latex = "We apply Newton's method."
        spoken_text = processor.process(latex)
        assert_spoken_contains(spoken_text, ["Newton's method", "for finding roots"])

    def test_complexity_expansion_cubic(self, processor):
        processor.special_rules['expand_complexity'] = True
        latex = "The cost is $O(N^3)$."
        spoken_text = processor.process(latex)
        assert_spoken_contains(spoken_text, ["big O of N cubed", "cubic time"])

    def test_complexity_expansion_nlogn(self, processor):
        processor.special_rules['expand_complexity'] = True
        latex = "Sorting takes $O(N \\log N)$ time."
        spoken_text = processor.process(latex)
        assert_spoken_contains(spoken_text, ["big O of N log N", "linearithmic time"])


    @pytest.mark.parametrize("convergence_term_latex, convergence_term_spoken", [
        ("The sequence converges rapidly.", "converges"),
        ("If it diverges, the method fails.", "diverges"),
        ("This indicates quadratic convergence.", "quadratic convergence"),
        ("We observe linear convergence.", "linear convergence"),
    ])
    def test_convergence_highlighting(self, processor, convergence_term_latex, convergence_term_spoken):
        processor.special_rules['highlight_convergence'] = True
        spoken_text = processor.process(convergence_term_latex)
        processed_by_domain_rule = processor._apply_special_rules(convergence_term_spoken)
        assert "{{EMPHASIS}}" in processed_by_domain_rule
        assert "{{/EMPHASIS}}" in processed_by_domain_rule
        assert convergence_term_spoken.lower() in processed_by_domain_rule.lower().replace("{{emphasis}}","").replace("{{/emphasis}}","")


class TestNumericalAnalysisEdgeCases:
    """Tests for edge cases and robustness."""
    def test_empty_input(self, processor):
        assert processor.process("") == ""

    def test_whitespace_input(self, processor):
        assert processor.process("   ") == "" # Or " "

    def test_non_numerical_analysis_input(self, processor):
        latex = "A statement from pure set theory: $A \\cup B = B \\cup A$."
        spoken_text = processor.process(latex)
        assert "pure set theory" in spoken_text.lower()
        assert processor.detect_subcontext(latex) == NumericalContext.GENERAL


class TestNumericalAnalysisMScLevelNotation:
    """Tests specifically targeting M.Sc. level notation."""

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Advanced Iterative Methods
        (r"The Conjugate Gradient method solves $Ax=b$ for symmetric positive-definite $A$.",
         ["Conjugate Gradient method", "solves A x equals b", "symmetric positive-definite A"]),
        (r"GMRES (Generalized Minimal Residual method) is for non-symmetric systems.",
         ["GMRES", "Generalized Minimal Residual method", "non-symmetric systems"]),
        (r"Preconditioning with $M^{-1}$ improves convergence of $M^{-1}Ax = M^{-1}b$.",
         ["Preconditioning with M inverse", "improves convergence", "M inverse A x equals M inverse b"]),

        # Eigenvalue Problems
        (r"The Power Iteration finds the dominant eigenvalue $\\lambda_{max}$.",
         ["Power Iteration", "dominant eigenvalue lambda max"]),
        (r"The QR algorithm with shifts computes all eigenvalues of $A$.", # Completed line
         ["Q R algorithm with shifts", "computes all eigenvalues of A"]),
        (r"Inverse iteration finds the eigenvalue closest to a shift $\\sigma$.",
         ["Inverse iteration", "eigenvalue closest to a shift sigma"]),

        # Numerical PDEs (Finite Element/Volume basics if implied by finite differences)
        (r"A finite element method (FEM) discretizes the domain into elements.",
         ["finite element method", "FEM", "discretizes the domain into elements"]),
        (r"The weak formulation is $\\int_\\Omega \\nabla u \\cdot \\nabla v dx = \\int_\\Omega f v dx$.",
         ["weak formulation", "integral over Omega of nabla u dot nabla v d x equals integral over Omega of f v d x"]),
        (r"The Courant-Friedrichs-Lewy (CFL) condition $\\frac{u \\Delta t}{\\Delta x} \\leq C_{max}$ is crucial for hyperbolic PDEs.",
         ["Courant-Friedrichs-Lewy", "CFL condition", "u delta t over delta x less than or equal to C max", "hyperbolic PDEs"]),

        # Advanced Quadrature
        (r"Clenshaw-Curtis quadrature is effective for smooth functions.",
         ["Clenshaw-Curtis quadrature", "smooth functions"]),
        (r"Monte Carlo integration estimates $\\int f d\\mu \\approx \\frac{1}{N} \\sum f(X_i)$ with error $O(N^{-1/2})$.",
         ["Monte Carlo integration", "integral f d mu approximately 1 over N sum f of X sub i", "error big O of N to the negative 1/2"]),

        # Approximation Theory
        (r"Best uniform approximation $p_n^*$ minimizes $\\|f-p_n\\|_\\infty$.",
         ["Best uniform approximation p n star", "minimizes infinity norm of f minus p sub n"]),
        (r"Chebyshev polynomials $T_n(x)$ are used for near-best approximation.",
         ["Chebyshev polynomials T sub n of x", "near-best approximation"]),
    ])
    def test_msc_notation(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)
