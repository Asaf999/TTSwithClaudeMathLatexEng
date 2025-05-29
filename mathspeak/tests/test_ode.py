#!/usr/bin/env python3
"""
Test Suite for ODE Domain Processor
===================================

Comprehensive tests for ordinary differential equations notation.
Tests follow Test-Driven Development (TDD) principles.
"""

import pytest
from typing import List

from mathspeak.domains.ode import (
    ODEProcessor,
    ODEVocabulary,
    ODEContext
)


# ===========================
# Test Fixtures
# ===========================

@pytest.fixture
def processor():
    """Create an ODEProcessor instance for testing."""
    return ODEProcessor()


@pytest.fixture
def vocabulary():
    """Create an ODEVocabulary instance for testing."""
    return ODEVocabulary()


# ===========================
# Helper Functions
# ===========================

def assert_spoken_contains(spoken_text: str, expected_keywords: List[str]) -> None:
    """Assert that spoken text contains all expected keywords."""
    spoken_lower = spoken_text.lower()
    missing_keywords = [kw for kw in expected_keywords if kw.lower() not in spoken_lower]
    assert not missing_keywords, f"Keywords {missing_keywords} not found in '{spoken_text}'"


def assert_spoken_not_contains(spoken_text: str, unwanted_keywords: List[str]) -> None:
    """Assert that spoken text does not contain unwanted keywords."""
    spoken_lower = spoken_text.lower()
    present_keywords = [kw for kw in unwanted_keywords if kw.lower() in spoken_lower]
    assert not present_keywords, f"Unwanted keywords {present_keywords} found in '{spoken_text}'"


# ===========================
# Vocabulary Tests
# ===========================

class TestODEVocabulary:
    """Test the ODEVocabulary class."""
    
    @pytest.mark.parametrize("latex_input,expected_keywords", [
        # Basic derivative notation
        ("y'", ["y prime"]),
        ("y''", ["y double prime"]),
        ("\\dot{y}", ["y dot"]),
        ("\\ddot{y}", ["y double dot"]),
        ("\\frac{dy}{dx}", ["d y over d x"]),
        ("\\frac{d^2y}{dx^2}", ["d squared y over d x squared"]),
        ("y^{(n)}", ["y to the n"]),
        
        # ODE types
        ("\\text{ODE}", ["O D E", "ordinary differential equation"]),
        ("\\text{IVP}", ["initial value problem"]),
        ("\\text{BVP}", ["boundary value problem"]),
        
        # First-order forms
        ("y' = f(x,y)", ["y prime equals f of x y"]),
        ("y' + p(x)y = q(x)", ["y prime plus p of x y equals q of x"]),
        ("M(x,y)dx + N(x,y)dy = 0", ["M of x y d x plus N of x y d y equals zero"]),
        
        # Second-order forms
        ("y'' + p(x)y' + q(x)y = 0", ["y double prime plus", "homogeneous"]),
        ("ar^2 + br + c = 0", ["characteristic equation"]),
        
        # Laplace transforms
        ("\\mathcal{L}\\{f(t)\\}", ["Laplace transform of f of t"]),
        ("\\mathcal{L}^{-1}\\{F(s)\\}", ["inverse Laplace transform of F of s"]),
        ("u_c(t)", ["unit step function at c"]),
        ("\\delta(t-c)", ["Dirac delta function at c"]),
        
        # Systems
        ("\\mathbf{x}' = A\\mathbf{x}", ["x prime equals A x"]),
        ("\\Phi(t)", ["fundamental matrix"]),
        ("e^{At}", ["exponential of A t", "matrix exponential"]),
        
        # Special functions
        ("J_n(x)", ["Bessel function J n of x"]),
        ("Y_n(x)", ["Bessel function Y n of x"]),
        ("P_n(x)", ["Legendre polynomial P n of x"]),
        
        # Qualitative theory
        ("\\mathbf{x}_0", ["equilibrium point", "critical point"]),
        ("\\text{stable}", ["stable"]),
        ("\\text{unstable}", ["unstable"]),
        ("\\text{saddle}", ["saddle point"]),
        ("\\text{limit cycle}", ["limit cycle"]),
    ])
    def test_direct_vocabulary_terms(self, processor, latex_input, expected_keywords):
        """Test direct vocabulary replacements."""
        result = processor.process(latex_input)
        assert_spoken_contains(result.processed, expected_keywords)
    
    def test_wronskian_notation(self, processor):
        """Test Wronskian notation."""
        result = processor.process("W(y_1, y_2) = \\begin{vmatrix} y_1 & y_2 \\\\ y_1' & y_2' \\end{vmatrix}")
        assert_spoken_contains(result.processed, ["Wronskian", "y 1", "y 2"])
    
    def test_phase_portrait_terms(self, processor):
        """Test phase portrait terminology."""
        result = processor.process("The phase portrait shows a stable spiral")
        assert_spoken_contains(result.processed, ["phase portrait", "stable spiral"])


# ===========================
# Pattern Tests
# ===========================

class TestODEPatterns:
    """Test pattern matching in ODE domain."""
    
    @pytest.mark.parametrize("latex_input,expected_keywords", [
        # Method descriptions
        ("Use separation of variables", ["separation of variables"]),
        ("Apply the integrating factor", ["integrating factor"]),
        ("By variation of parameters", ["variation of parameters"]),
        
        # Series solutions
        ("Find the power series solution", ["power series solution"]),
        ("Use the Frobenius method", ["Frobenius method"]),
        
        # Existence theorems
        ("By Picard-Lindelöf theorem", ["Picard", "Lindelof", "theorem"]),
        ("The Lipschitz condition", ["Lipschitz condition"]),
        
        # Stability
        ("is asymptotically stable", ["asymptotically stable"]),
        ("Lyapunov stability", ["Lyapunov stability"]),
    ])
    def test_general_patterns(self, processor, latex_input, expected_keywords):
        """Test general pattern recognition."""
        result = processor.process(latex_input)
        assert_spoken_contains(result.processed, expected_keywords)


# ===========================
# Context Detection Tests
# ===========================

class TestODESubContextDetection:
    """Test sub-context detection in ODE domain."""
    
    @pytest.mark.parametrize("text,expected_context", [
        ("Solve the first-order linear equation", ODEContext.FIRST_ORDER),
        ("The second-order homogeneous equation", ODEContext.SECOND_ORDER),
        ("Consider the system \\mathbf{x}' = A\\mathbf{x}", ODEContext.SYSTEMS),
        ("Take the Laplace transform", ODEContext.LAPLACE),
        ("Find the power series solution", ODEContext.SERIES_SOLUTIONS),
        ("Analyze the phase portrait", ODEContext.QUALITATIVE),
        ("Using Euler's method", ODEContext.NUMERICAL),
    ])
    def test_sub_context_detection(self, processor, text, expected_context):
        """Test that sub-contexts are correctly detected."""
        detected_context = processor.detect_subcontext(text)
        assert detected_context == expected_context


# ===========================
# Integration Tests
# ===========================

class TestODEProcessing:
    """Test complete processing of ODE expressions."""
    
    def test_first_order_linear_ode(self, processor):
        """Test processing of first-order linear ODE."""
        latex = "Solve y' + p(x)y = q(x) using the integrating factor \\mu(x) = e^{\\int p(x)dx}"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "y prime plus p of x y equals q of x",
            "integrating factor",
            "mu of x equals e to the integral of p of x d x"
        ])
    
    def test_second_order_characteristic_equation(self, processor):
        """Test processing of characteristic equation."""
        latex = "For y'' + 3y' + 2y = 0, the characteristic equation is r^2 + 3r + 2 = 0"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "y double prime plus 3 y prime plus 2 y equals zero",
            "characteristic equation",
            "r squared plus 3 r plus 2 equals zero"
        ])
    
    def test_laplace_transform_solution(self, processor):
        """Test Laplace transform method."""
        latex = "Taking \\mathcal{L}\\{y'' + 4y\\} = s^2Y(s) - sy(0) - y'(0) + 4Y(s)"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "Laplace transform",
            "y double prime plus 4 y",
            "s squared Y of s minus s y of zero minus y prime of zero plus 4 Y of s"
        ])
    
    def test_system_eigenvalue_analysis(self, processor):
        """Test system eigenvalue analysis."""
        latex = "For \\mathbf{x}' = A\\mathbf{x}, find eigenvalues \\lambda where \\det(A - \\lambda I) = 0"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "x prime equals A x",
            "eigenvalues lambda",
            "determinant of A minus lambda I equals zero"
        ])


# ===========================
# Special Rules Tests
# ===========================

class TestODESpecialRules:
    """Test special processing rules for ODEs."""
    
    def test_famous_equation_emphasis(self, processor):
        """Test emphasis on famous equations."""
        latex = "The Bessel equation x^2y'' + xy' + (x^2 - n^2)y = 0"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, ["Bessel equation"])
    
    def test_existence_theorem_clarification(self, processor):
        """Test clarification of existence theorems."""
        latex = "By the Picard-Lindelöf theorem, the IVP has a unique solution"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "Picard", "Lindelof", "theorem",
            "initial value problem", "unique solution"
        ])


# ===========================
# Edge Cases Tests
# ===========================

class TestODEEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_input(self, processor):
        """Test handling of empty input."""
        result = processor.process("")
        assert result.processed == ""
    
    def test_non_ode_input(self, processor):
        """Test that non-ODE content is passed through."""
        latex = "The integral \\int_0^1 x^2 dx = \\frac{1}{3}"
        result = processor.process(latex)
        # Should not contain ODE-specific terminology
        assert_spoken_not_contains(result.processed, ["differential equation", "y prime"])
    
    def test_mixed_notation(self, processor):
        """Test handling of mixed mathematical notation."""
        latex = "The ODE y' = ky has solution y = Ce^{kx} where C \\in \\mathbb{R}"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, ["O D E", "y prime equals k y"])
        assert_spoken_contains(result.processed, ["C e to the k x"])


# ===========================
# M.Sc. Level Notation Tests
# ===========================

class TestODEAdvancedNotation:
    """Test advanced M.Sc. level ODE notation."""
    
    @pytest.mark.parametrize("latex_input,expected_keywords", [
        # Sturm-Liouville theory
        ("The Sturm-Liouville operator L[y] = -\\frac{d}{dx}(p(x)\\frac{dy}{dx}) + q(x)y", 
         ["Sturm Liouville operator"]),
        
        # Green's functions
        ("The Green's function G(x,t) satisfies LG = \\delta(x-t)", 
         ["Green's function", "delta"]),
        
        # Floquet theory
        ("By Floquet's theorem, solutions have the form y(t) = e^{\\mu t}p(t)", 
         ["Floquet", "theorem"]),
        
        # Bifurcation theory
        ("A Hopf bifurcation occurs at \\mu = \\mu_0", 
         ["Hopf bifurcation"]),
        
        # Hamiltonian systems
        ("The Hamiltonian system \\dot{q} = \\frac{\\partial H}{\\partial p}, \\dot{p} = -\\frac{\\partial H}{\\partial q}", 
         ["Hamiltonian system"]),
    ])
    def test_advanced_notation(self, processor, latex_input, expected_keywords):
        """Test processing of advanced ODE notation."""
        result = processor.process(latex_input)
        assert_spoken_contains(result.processed, expected_keywords)


# ===========================
# Performance Tests
# ===========================

class TestODEPerformance:
    """Test performance characteristics."""
    
    def test_large_system_performance(self, processor):
        """Test that large systems are processed efficiently."""
        import time
        
        # Create a large system of ODEs
        large_system = "\\begin{cases}\n" + "\n".join([
            f"x_{i}' = a_{{i1}}x_1 + a_{{i2}}x_2 + \\cdots + a_{{i{50}}}x_{{50}}"
            for i in range(1, 51)
        ]) + "\n\\end{cases}"
        
        start_time = time.time()
        result = processor.process(large_system)
        elapsed_time = time.time() - start_time
        
        # Should process in reasonable time
        assert elapsed_time < 2.0
        assert len(result.processed) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])