#!/usr/bin/env python3
"""
Test Suite for Manifolds Domain Processor
=========================================

Comprehensive tests for differential geometry and manifolds notation.
Tests follow Test-Driven Development (TDD) principles.
"""

import pytest
from typing import List, Set

from mathspeak.domains.manifolds import (
    ManifoldsProcessor,
    ManifoldsVocabulary,
    ManifoldsContext
)


# ===========================
# Test Fixtures
# ===========================

@pytest.fixture
def processor():
    """Create a ManifoldsProcessor instance for testing."""
    return ManifoldsProcessor()


@pytest.fixture
def vocabulary():
    """Create a ManifoldsVocabulary instance for testing."""
    return ManifoldsVocabulary()


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

class TestManifoldsVocabulary:
    """Test the ManifoldsVocabulary class."""
    
    @pytest.mark.parametrize("latex_input,expected_keywords", [
        # Basic manifold notation
        ("M", ["manifold M"]),
        ("N", ["manifold N"]),
        ("\\mathcal{M}", ["manifold script M"]),
        ("\\dim M", ["dimension of M"]),
        ("\\dim M = n", ["dimension of M equals n"]),
        ("n\\text{-manifold}", ["n manifold"]),
        
        # Charts and atlases
        ("(U, \\phi)", ["chart U phi"]),
        ("\\phi: U \\to \\mathbb{R}^n", ["phi from U to R n"]),
        ("\\mathcal{A}", ["atlas script A"]),
        ("\\{(U_\\alpha, \\phi_\\alpha)\\}", ["collection of charts"]),
        
        # Smooth maps
        ("C^\\infty", ["C infinity", "smooth"]),
        ("C^k", ["C k"]),
        ("f: M \\to N", ["f from M to N"]),
        ("M \\cong N", ["M is diffeomorphic to N"]),
        ("\\partial M", ["boundary of M"]),
        
        # Tangent spaces
        ("T_p M", ["tangent space to M at p"]),
        ("T_p^* M", ["cotangent space to M at p"]),
        ("TM", ["tangent bundle of M"]),
        ("T^*M", ["cotangent bundle of M"]),
        ("\\frac{\\partial}{\\partial x^i}", ["partial over partial x i"]),
        ("dx^i", ["d x i"]),
        
        # Vector fields
        ("X \\in \\mathfrak{X}(M)", ["X is a vector field on M"]),
        ("\\Gamma(TM)", ["sections of the tangent bundle"]),
        ("[X,Y]", ["Lie bracket of X and Y"]),
        ("\\mathcal{L}_X Y", ["Lie derivative of Y with respect to X"]),
        ("X^i \\frac{\\partial}{\\partial x^i}", ["X i partial over partial x i"]),
        
        # Differential forms
        ("\\Omega^k(M)", ["space of k forms on M"]),
        ("\\omega", ["omega"]),
        ("dx^i \\wedge dx^j", ["d x i wedge d x j"]),
        ("d\\omega", ["d omega"]),
        ("d^2 = 0", ["d squared equals zero"]),
        ("\\int_M \\omega", ["integral over M of omega"]),
        ("\\int_{\\partial M} \\omega", ["integral over boundary M of omega"]),
        
        # Lie groups
        ("GL(n, \\mathbb{R})", ["general linear group n R"]),
        ("SL(n, \\mathbb{R})", ["special linear group n R"]),
        ("SO(n)", ["special orthogonal group n"]),
        ("SU(n)", ["special unitary group n"]),
        ("\\mathfrak{g}", ["Lie algebra g"]),
        ("\\exp: \\mathfrak{g} \\to G", ["exponential map from g to G"]),
        ("[A,B]", ["Lie bracket A B", "commutator"]),
        
        # Riemannian geometry
        ("(M,g)", ["Riemannian manifold M with metric g"]),
        ("g_{ij}", ["metric components g i j"]),
        ("ds^2", ["line element"]),
        ("\\nabla", ["nabla", "covariant derivative"]),
        ("\\Gamma^k_{ij}", ["Christoffel symbol"]),
        ("\\nabla_{\\dot{\\gamma}} \\dot{\\gamma} = 0", ["geodesic equation"]),
        ("R^l_{ijk}", ["Riemann curvature tensor"]),
    ])
    def test_direct_vocabulary_terms(self, processor, latex_input, expected_keywords):
        """Test direct vocabulary replacements."""
        result = processor.process(latex_input)
        assert_spoken_contains(result.processed, expected_keywords)
    
    def test_lambda_vocabulary_terms(self, processor):
        """Test lambda-based vocabulary terms."""
        # Test vector field components
        result = processor.process("X = X^i \\frac{\\partial}{\\partial x^i}")
        assert_spoken_contains(result.processed, ["X equals X i partial over partial x i"])
        
        # Test differential form components
        result = processor.process("\\omega = \\omega_{ij} dx^i \\wedge dx^j")
        assert_spoken_contains(result.processed, ["omega equals omega i j d x i wedge d x j"])
        
        # Test metric tensor
        result = processor.process("ds^2 = g_{ij} dx^i dx^j")
        assert_spoken_contains(result.processed, ["line element equals g i j d x i d x j"])


# ===========================
# Pattern Tests
# ===========================

class TestManifoldsPatterns:
    """Test pattern matching in manifolds domain."""
    
    @pytest.mark.parametrize("latex_input,expected_keywords", [
        # Smooth structure patterns
        ("M has a smooth structure", ["smooth structure"]),
        ("The differentiable structure on M", ["differentiable structure"]),
        
        # Tangent bundle patterns
        ("The tangent bundle TM", ["tangent bundle"]),
        ("Elements of T_p M", ["tangent space to M at p"]),
        
        # Differential forms patterns
        ("A differential k-form", ["differential", "k form"]),
        ("The exterior derivative d", ["exterior derivative"]),
        
        # Lie group patterns
        ("G is a Lie group", ["Lie group"]),
        ("The Lie algebra \\mathfrak{g}", ["Lie algebra"]),
        
        # Connection patterns
        ("The Levi-Civita connection", ["Levi Civita connection"]),
        ("Parallel transport along \\gamma", ["parallel transport"]),
    ])
    def test_general_patterns(self, processor, latex_input, expected_keywords):
        """Test general pattern recognition."""
        result = processor.process(latex_input)
        assert_spoken_contains(result.processed, expected_keywords)


# ===========================
# Context Detection Tests
# ===========================

class TestManifoldsSubContextDetection:
    """Test sub-context detection in manifolds domain."""
    
    @pytest.mark.parametrize("text,expected_context", [
        ("Let M be a smooth manifold with charts", ManifoldsContext.BASIC_MANIFOLDS),
        ("The tangent space T_p M", ManifoldsContext.TANGENT_BUNDLES),
        ("For vector fields X and Y", ManifoldsContext.VECTOR_FIELDS),
        ("Consider the differential form \\omega", ManifoldsContext.DIFFERENTIAL_FORMS),
        ("G is a Lie group with Lie algebra", ManifoldsContext.LIE_THEORY),
        ("The Riemannian metric g defines", ManifoldsContext.RIEMANNIAN),
        ("The covariant derivative \\nabla", ManifoldsContext.CONNECTIONS),
    ])
    def test_sub_context_detection(self, processor, text, expected_context):
        """Test that sub-contexts are correctly detected."""
        detected_context = processor.detect_subcontext(text)
        assert detected_context == expected_context


# ===========================
# Integration Tests
# ===========================

class TestManifoldsProcessing:
    """Test complete processing of manifolds expressions."""
    
    def test_smooth_manifold_definition(self, processor):
        """Test processing of smooth manifold definition."""
        latex = "A smooth manifold M is a topological space with an atlas \\mathcal{A} = \\{(U_\\alpha, \\phi_\\alpha)\\}"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "smooth manifold M",
            "topological space",
            "atlas",
            "collection of charts"
        ])
    
    def test_tangent_bundle_description(self, processor):
        """Test processing of tangent bundle description."""
        latex = "The tangent bundle TM = \\bigsqcup_{p \\in M} T_p M with projection \\pi: TM \\to M"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "tangent bundle",
            "disjoint union",
            "tangent space to M at p",
            "projection pi from tangent bundle of M to M"
        ])
    
    def test_lie_bracket_computation(self, processor):
        """Test processing of Lie bracket computation."""
        latex = "For vector fields X, Y, the Lie bracket [X,Y] = XY - YX as derivations"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "vector fields",
            "Lie bracket of X and Y",
            "X Y minus Y X",
            "derivations"
        ])
    
    def test_differential_form_integration(self, processor):
        """Test processing of differential form integration."""
        latex = "By Stokes' theorem: \\int_M d\\omega = \\int_{\\partial M} \\omega"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "Stokes theorem",
            "integral over M of d omega",
            "integral over boundary M of omega"
        ])
    
    def test_riemannian_metric_expression(self, processor):
        """Test processing of Riemannian metric."""
        latex = "The metric tensor g_{ij} defines the line element ds^2 = g_{ij} dx^i dx^j"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "metric tensor g i j",
            "line element",
            "g i j d x i d x j"
        ])


# ===========================
# Special Rules Tests
# ===========================

class TestManifoldsSpecialRules:
    """Test special processing rules for manifolds."""
    
    def test_einstein_summation_clarification(self, processor):
        """Test clarification of Einstein summation convention."""
        latex = "We have X = X^i \\frac{\\partial}{\\partial x^i} (Einstein summation implied)"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "X equals X i partial over partial x i",
            "Einstein summation implied"
        ])
    
    def test_famous_theorem_emphasis(self, processor):
        """Test emphasis on famous theorems."""
        latex = "By the Gauss-Bonnet theorem, \\int_M K dA = 2\\pi\\chi(M)"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, ["Gauss Bonnet theorem"])


# ===========================
# Edge Cases Tests
# ===========================

class TestManifoldsEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_input(self, processor):
        """Test handling of empty input."""
        result = processor.process("")
        assert result.processed == ""
    
    def test_non_manifolds_input(self, processor):
        """Test that non-manifolds content is passed through."""
        latex = "The probability P(A|B) = \\frac{P(B|A)P(A)}{P(B)}"
        result = processor.process(latex)
        # Should not contain manifolds-specific terminology
        assert_spoken_not_contains(result.processed, ["manifold", "tangent", "Lie"])
    
    def test_mixed_notation(self, processor):
        """Test handling of mixed mathematical notation."""
        latex = "On the manifold M, solve \\frac{\\partial u}{\\partial t} = \\Delta u"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, ["manifold M"])
        assert_spoken_contains(result.processed, ["partial u over partial t"])


# ===========================
# M.Sc. Level Notation Tests
# ===========================

class TestManifoldsAdvancedNotation:
    """Test advanced M.Sc. level manifolds notation."""
    
    @pytest.mark.parametrize("latex_input,expected_keywords", [
        # Advanced differential geometry
        ("The holonomy group Hol_p(\\nabla)", ["holonomy group"]),
        ("The curvature 2-form \\Omega = d\\omega + \\omega \\wedge \\omega", ["curvature 2 form"]),
        
        # Characteristic classes
        ("The Chern class c_1(E)", ["Chern class c 1 of E"]),
        ("The Pontryagin class p_k(TM)", ["Pontryagin class"]),
        
        # Advanced Lie theory
        ("The adjoint representation Ad: G \\to GL(\\mathfrak{g})", ["adjoint representation"]),
        ("The Killing form B(X,Y) = \\text{tr}(ad_X \\circ ad_Y)", ["Killing form"]),
        
        # Symplectic geometry
        ("A symplectic manifold (M, \\omega) with \\omega closed", ["symplectic manifold"]),
        ("The Poisson bracket \\{f,g\\}", ["Poisson bracket"]),
        
        # Index theory
        ("The Atiyah-Singer index theorem", ["Atiyah Singer index theorem"]),
        ("The Dirac operator D", ["Dirac operator"]),
    ])
    def test_advanced_notation(self, processor, latex_input, expected_keywords):
        """Test processing of advanced manifolds notation."""
        result = processor.process(latex_input)
        assert_spoken_contains(result.processed, expected_keywords)


# ===========================
# Performance Tests
# ===========================

class TestManifoldsPerformance:
    """Test performance characteristics."""
    
    def test_large_expression_performance(self, processor):
        """Test that large expressions are processed efficiently."""
        import time
        
        # Create a large expression with many manifolds terms
        large_expr = " + ".join([
            f"\\int_{{M_{i}}} \\omega_{i} \\wedge \\eta_{i}"
            for i in range(50)
        ])
        
        start_time = time.time()
        result = processor.process(large_expr)
        elapsed_time = time.time() - start_time
        
        # Should process in reasonable time (less than 1 second)
        assert elapsed_time < 1.0
        assert len(result.processed) > 0


# ===========================
# Theorem Tests
# ===========================

class TestManifoldsTheorems:
    """Test processing of manifolds theorems."""
    
    def test_stokes_theorem(self, processor):
        """Test Stokes' theorem processing."""
        latex = "Stokes' Theorem: For a differential form \\omega, \\int_M d\\omega = \\int_{\\partial M} \\omega"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "Stokes Theorem",
            "differential form omega",
            "integral over M of d omega equals integral over boundary M of omega"
        ])
    
    def test_gauss_bonnet_theorem(self, processor):
        """Test Gauss-Bonnet theorem processing."""
        latex = "The Gauss-Bonnet theorem states \\int_M K dA + \\int_{\\partial M} k_g ds = 2\\pi \\chi(M)"
        result = processor.process(latex)
        
        assert_spoken_contains(result.processed, [
            "Gauss Bonnet theorem",
            "integral",
            "2 pi chi of M"
        ])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])