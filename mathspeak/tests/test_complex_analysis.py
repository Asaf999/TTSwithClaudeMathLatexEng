#!/usr/bin/env python3
"""
Test Suite for the Complex Analysis Domain Processor (mathspeak.domains.complex_analysis)
=======================================================================================

Ensures comprehensive coverage for complex analysis notation processing,
from undergraduate basics to M.Sc. level concepts.
"""

import pytest
import re # For more complex assertion needs if any

# Module to be tested
from mathspeak.domains.complex_analysis import (
    ComplexAnalysisProcessor,
    ComplexContext,
    ComplexAnalysisVocabulary,
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
    """Provides a ComplexAnalysisProcessor instance for testing (module scope)."""
    return ComplexAnalysisProcessor()

@pytest.fixture(scope="module")
def vocabulary():
    """Provides a ComplexAnalysisVocabulary instance for testing (module scope)."""
    return ComplexAnalysisVocabulary()

# --- Test Classes ---

class TestComplexAnalysisVocabulary:
    """Tests for the ComplexAnalysisVocabulary component."""

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Basic Complex Numbers
        (r"z", ["z"]),
        (r"w", ["w"]),
        (r"\\mathbb{C}", ["complex numbers"]),
        (r"i", ["i"]),
        (r"j", ["j"]), # Engineering notation
        (r"z = x + iy", ["z equals x plus i y"]),
        (r"z = re^{i\\theta}", ["z equals r e to the i theta"]),
        (r"z = r\\text{cis}\\theta", ["z equals r cis theta"]),
        (r"\\text{Re}(z)", ["real part of z"]), # Note: (z) vs \(z\)
        (r"\\text{Im}(z)", ["imaginary part of z"]),
        (r"\\Re(z)", ["real part of z"]),
        (r"\\Im(z)", ["imaginary part of z"]),
        (r"|z|", ["modulus of z"]),
        (r"\\text{arg}(z)", ["argument of z"]),
        (r"\\text{Arg}(z)", ["principal argument of z"]),
        (r"\\bar{z}", ["z bar"]),
        (r"\\overline{z}", ["z conjugate"]),
        (r"z^*", ["z star"]),
        (r"z \\cdot w", ["z times w"]),
        (r"z/w", ["z over w"]),
        (r"z^n", ["z to the n"]),
        (r"\\sqrt[n]{z}", ["n-th root of z"]),
        (r"1/z", ["one over z"]),

        # Holomorphic Functions
        (r"\\text{holomorphic}", ["holomorphic"]),
        (r"\\text{analytic}", ["analytic"]),
        (r"\\text{meromorphic}", ["meromorphic"]),
        (r"\\text{entire}", ["entire"]),
        (r"\\text{biholomorphic}", ["biholomorphic"]),
        (r"\\text{conformal}", ["conformal"]),
        (r"f'(z)", ["f prime of z"]), # Note: \(z\) vs (z)
        (r"f''(z)", ["f double prime of z"]),
        (r"\\frac{df}{dz}", ["d f d z"]),
        (r"\\frac{\\partial f}{\\partial z}", ["partial f partial z"]),
        (r"\\frac{\\partial f}{\\partial \\bar{z}}", ["partial f partial z bar"]),
        (r"u_x = v_y", ["u sub x equals v sub y"]),
        (r"u_y = -v_x", ["u sub y equals negative v sub x"]),
        (r"f \\in H(D)", ["f is in the space of holomorphic functions on D"]),

        # Contour Integration
        (r"\\gamma", ["gamma"]),
        (r"\\Gamma", ["capital gamma"]),
        (r"C", ["C"]), # Simple C
        (r"\\partial D", ["boundary of D"]),
        (r"\\text{simple closed curve}", ["simple closed curve"]),
        (r"\\text{positively oriented}", ["positively oriented"]),
        (r"\\text{counterclockwise}", ["counterclockwise"]),
        (r"\\text{parametrized by}", ["parametrized by"]),

        # Residue Theory
        (r"\\text{simple pole}", ["simple pole"]),
        (r"\\text{pole of order } n", ["pole of order n"]), # Space after order
        (r"\\text{essential singularity}", ["essential singularity"]),
        (r"\\text{removable singularity}", ["removable singularity"]),
        (r"\\text{isolated singularity}", ["isolated singularity"]),
        (r"\\text{branch point}", ["branch point"]),
        (r"\\text{branch cut}", ["branch cut"]),

        # Special Functions
        (r"e^z", ["e to the z"]),
        (r"\\exp(z)", ["exponential of z"]),
        (r"\\log z", ["log z"]),
        (r"\\ln z", ["natural log of z"]),
        (r"\\text{Log} z", ["principal logarithm of z"]),
        (r"\\sin z", ["sine z"]),
        (r"\\cos z", ["cosine z"]),
        (r"\\tan z", ["tangent z"]),
        (r"\\sinh z", ["hyperbolic sine z"]),
        (r"\\cosh z", ["hyperbolic cosine z"]),
        (r"\\tanh z", ["hyperbolic tangent z"]),
        (r"\\sin^{-1} z", ["inverse sine of z"]),
        (r"\\arcsin z", ["arc sine z"]),
        (r"z^\\alpha", ["z to the alpha"]),
        (r"z^{1/n}", ["n-th root of z"]),
        (r"\\sqrt{z}", ["square root of z"]),
        (r"e^{i\\pi}", ["e to the i pi"]),
        (r"e^{2\\pi i}", ["e to the two pi i"]),

        # Series Expansions
        (r"\\text{radius of convergence}", ["radius of convergence"]),
        (r"\\text{annulus of convergence}", ["annulus of convergence"]),

        # Conformal Mappings
        (r"\\text{Möbius transformation}", ["Möbius transformation"]),
        (r"\\text{linear fractional transformation}", ["linear fractional transformation"]),
        (r"\\text{angle-preserving}", ["angle-preserving"]),
        (r"\\text{univalent}", ["univalent"]),

        # Complex Integration Theorems
        (r"\\text{Cauchy's theorem}", ["Cauchy's theorem"]),
        (r"\\text{Cauchy's integral formula}", ["Cauchy's integral formula"]),
        (r"\\text{Cauchy's residue theorem}", ["Cauchy's residue theorem"]),
        (r"\\text{Morera's theorem}", ["Morera's theorem"]),
        (r"\\text{Liouville's theorem}", ["Liouville's theorem"]),
        (r"\\text{Maximum modulus principle}", ["Maximum modulus principle"]),
        (r"\\text{Rouché's theorem}", ["Rouché's theorem"]),
    ])
    def test_direct_vocabulary_terms(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, arg, expected_keywords", [
        (r"\\text{Re}(w)", "w", ["real part of w"]),
        (r"\\text{Im}(z+1)", "z+1", ["imaginary part of z plus 1"]),
        (r"|z-z_0|", "z-z_0", ["modulus of z minus z naught"]),
        (r"\\text{arg}(e^{i\\phi})", "e^{i\\phi}", ["argument of e to the i phi"]),
        (r"\\overline{w+z}", "w+z", ["conjugate of w plus z"]),
        (r"f^{(n)}(z_0)", "z_0", ["n-th derivative of f at z naught"]), # Assuming f^(n) is handled
        (r"\\text{Res}(g, a+ib)", "g, a+ib", ["residue of g at a plus i b"]),
    ])
    def test_lambda_vocabulary_terms(self, processor, latex_input, arg, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        (r"\\oint_\\gamma f(z)dz", ["contour integral over gamma", "f of z d z"]),
        (r"\\oint_C g(w) dw", ["contour integral over C", "g of w d w"]),
        (r"\\int_\\Gamma h(zeta) d\\zeta", ["integral along capital gamma", "h of zeta d zeta"]),
        (r"\\oint_{\|z\|=R} \\frac{1}{z} dz", ["contour integral over the circle of radius R", "1 over z d z"]),
        (r"\\gamma: [0,1] \\to \\mathbb{C}", ["gamma from the interval 0 1 to C"]),
        (r"\\gamma(t) = z_0 + Re^{it}", ["gamma of t equals z naught plus R e to the i t"]),
    ])
    def test_contour_integration_vocab(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        (r"\\sum_{n=0}^\\infty a_n (z-z_0)^n", ["sum from n equals 0 to infinity", "a sub n times z minus z naught to the n"]),
        (r"\\sum_{n=-\\infty}^\\infty c_n (z-a)^n", ["sum from n equals negative infinity to infinity", "c sub n times z minus a to the n"]),
        (r"R = \\frac{1}{\\limsup_{n\\to\\infty} \\sqrt[n]{\|a_n\|}}", ["R equals one over", "limit superior as n goes to infinity", "n-th root of the modulus of a sub n"]),
    ])
    def test_series_expansion_vocab(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        (r"w = f(z)", ["w equals f of z"]),
        (r"f: D \\to D'", ["f maps D to D prime"]),
        (r"f(z) = \\frac{az + b}{cz + d}", ["f of z equals a z plus b over c z plus d"]),
        (r"z \\mapsto z^2", ["z maps to z squared"]),
    ])
    def test_conformal_mapping_vocab(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        (r"f(z_0) = \\frac{1}{2\\pi i} \\oint_\\gamma \\frac{f(w)}{w-z_0}dw", ["f of z naught equals one over two pi i", "contour integral over gamma", "f of w over w minus z naught d w"]),
        (r"f^{(n)}(a) = \\frac{n!}{2\\pi i} \\oint_C \\frac{f(z)}{(z-a)^{n+1}}dz", ["n-th derivative of f at a equals n factorial over two pi i", "f of z over z minus a to the n plus 1 d z"]),
    ])
    def test_integration_theorem_formulas_vocab(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)


class TestComplexAnalysisPatterns:
    """Tests for the regex patterns defined for general complex analysis phrases."""
    @pytest.mark.parametrize("latex_input, expected_keywords", [
        ("Let $z = r(\\cos\\theta + i\\sin\\theta)$ be its polar form.", ["z equals r times cosine theta plus i sine theta", "polar form"]),
        ("If $f$ is holomorphic on $D$, then it is analytic.", ["f is holomorphic on D", "analytic"]),
        ("Assume $f$ has a pole at $z_0$ of order $m$.", ["f has a pole at z naught", "order m"]),
        ("By Cauchy's Residue Theorem, $\\oint_C f(z)dz = 2\\pi i\\sum\\text{Res}$.", ["Cauchy's Residue Theorem", "contour integral over C", "f of z d z equals two pi i times the sum of residues"]),
        ("The condition $\\frac{\\partial f}{\\partial \\bar{z}} = 0$ is equivalent to the Cauchy-Riemann equations.", ["partial f partial z bar equals zero", "Cauchy-Riemann equations"]),
        ("The principal branch of the logarithm has a branch cut along the negative real axis.", ["principal branch", "logarithm", "branch cut along the negative real axis"]),
        ("The winding number $n(\\gamma, z_0)$ counts how many times $\\gamma$ winds around $z_0$.", ["winding number n of gamma about z naught", "winds around z naught"]),
    ])
    def test_general_patterns(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)


class TestComplexAnalysisSubContextDetection:
    @pytest.mark.parametrize("latex_input, expected_context_enum", [
        ("Let $z = x+iy$. The modulus is $|z|=\\sqrt{x^2+y^2}$.", ComplexContext.BASIC_COMPLEX),
        ("A function $f(z)$ is holomorphic if it is complex differentiable.", ComplexContext.HOLOMORPHIC),
        ("Evaluate the contour integral $\\oint_C \\frac{1}{z} dz$.", ComplexContext.INTEGRATION),
        ("The function $f(z) = 1/z$ has a simple pole at $z=0$ with $\\text{Res}(f,0)=1$.", ComplexContext.RESIDUES),
        ("The map $w = 1/z$ is a conformal mapping.", ComplexContext.CONFORMAL),
        ("The principal branch of $\\log z$ is usually taken for $-\\pi < \\text{Arg} z \\leq \\pi$.", ComplexContext.SPECIAL_FUNCTIONS),
        ("The Laurent series for $f(z)$ around $z_0$ is $\\sum_{n=-\\infty}^{\\infty} a_n (z-z_0)^n$.", ComplexContext.SERIES),
        ("This is a general mathematical statement about functions.", ComplexContext.GENERAL),
    ])
    def test_sub_context_detection(self, processor, latex_input, expected_context_enum):
        assert processor.detect_subcontext(latex_input) == expected_context_enum


class TestComplexAnalysisProcessing:
    """End-to-end tests for ComplexAnalysisProcessor.process()."""

    def test_cauchy_riemann_equations_processing(self, processor):
        latex = "The Cauchy-Riemann equations are $\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y}$ and $\\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}$."
        spoken_text = processor.process(latex)
        expected = [
            "Cauchy-Riemann equations",
            "partial u partial x equals partial v partial y",
            "partial u partial y equals negative partial v partial x"
        ]
        assert_spoken_contains(spoken_text, expected)

    def test_residue_theorem_application(self, processor):
        latex = "To evaluate $\\int_{-\\infty}^{\\infty} R(x) dx$, we use $\\oint_C R(z) dz = 2\\pi i \\sum \\text{Res}(R, z_k)$."
        spoken_text = processor.process(latex)
        expected = [
            "evaluate", "integral from negative infinity to infinity of R of x d x",
            "contour integral over C of R of z d z equals two pi i", "sum of the residues of R at z sub k"
        ]
        assert_spoken_contains(spoken_text, expected)

    def test_laurent_series_description(self, processor):
        latex = "A function $f(z)$ analytic in an annulus $r < |z-z_0| < R$ has a Laurent series $\\sum_{n=-\\infty}^{\\infty} a_n (z-z_0)^n$."
        spoken_text = processor.process(latex)
        expected = [
            "function f of z analytic in an annulus", "r is less than the modulus of z minus z naught which is less than R",
            "Laurent series", "sum from n equals negative infinity to infinity of a sub n times z minus z naught to the n"
        ]
        assert_spoken_contains(spoken_text, expected)


class TestComplexAnalysisSpecialRules:
    """Tests for specific rules like theorem emphasis or branch cut clarifications."""

    @pytest.mark.parametrize("theorem_name_latex, theorem_name_spoken", [
        ("Cauchy's theorem states that...", "Cauchy's theorem"),
        ("By Cauchy's integral formula, we have...", "Cauchy's integral formula"),
        ("The residue theorem implies...", "residue theorem"),
        ("Liouville's theorem is fundamental.", "Liouville's theorem"),
        ("The maximum modulus principle applies here.", "maximum modulus principle"),
    ])
    def test_theorem_emphasis(self, processor, theorem_name_latex, theorem_name_spoken):
        # Assuming the processor's _apply_special_rules adds emphasis markers
        # and the NLP layer (or a simple replace for testing) handles them.
        processor.special_rules['emphasize_theorems'] = True # Ensure rule is active for test
        spoken_text = processor.process(theorem_name_latex)

        # Check if the emphasis markers are present around the theorem name in the processed text
        # This is a simplified check; actual emphasis might be handled by voice manager.
        # We check if the processor's output contains the markers.
        processed_by_domain_rule = processor._apply_special_rules(theorem_name_spoken)
        assert "{{EMPHASIS}}" in processed_by_domain_rule
        assert "{{/EMPHASIS}}" in processed_by_domain_rule
        assert theorem_name_spoken.lower() in processed_by_domain_rule.lower().replace("{{emphasis}}", "").replace("{{/emphasis}}", "")

    def test_branch_cut_clarification(self, processor):
        processor.special_rules['clarify_branch_cuts'] = True
        latex = "The function $\\log z$ has a branch cut."
        spoken_text = processor.process(latex)
        assert_spoken_contains(spoken_text, ["branch cut", "function is discontinuous"])

    def test_integration_expansion(self, processor):
        processor.special_rules['expand_integration'] = True
        latex = "The contour is positively oriented."
        spoken_text = processor.process(latex)
        assert_spoken_contains(spoken_text, ["positively oriented", "counterclockwise"])


class TestComplexAnalysisEdgeCases:
    """Tests for edge cases and robustness."""
    def test_empty_input(self, processor):
        assert processor.process("") == ""

    def test_whitespace_input(self, processor):
        assert processor.process("   ") == "" # Or " " depending on cleanup

    def test_non_complex_analysis_input(self, processor):
        latex = "This is a simple sentence about algebra: x + y = 1."
        spoken_text = processor.process(latex)
        assert "simple sentence about algebra" in spoken_text.lower()
        assert processor.detect_subcontext(latex) == ComplexContext.GENERAL


class TestComplexAnalysisMScLevelNotation:
    """Tests specifically targeting M.Sc. level notation."""

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Argument Principle
        (r"By the Argument Principle, $\\frac{1}{2\\pi i} \\oint_C \\frac{f'(z)}{f(z)} dz = N - P$.",
         ["Argument Principle", "one over two pi i", "contour integral over C", "f prime of z over f of z d z", "N minus P"]),
        # Rouché's Theorem
        (r"Rouché's Theorem: If $|g(z)| < |f(z)|$ on $C$, then $f$ and $f+g$ have the same number of zeros inside $C$.",
         ["Rouché's Theorem", "modulus of g of z is less than modulus of f of z on C", "f and f plus g have the same number of zeros inside C"]),
        # Analytic Continuation
        (r"The analytic continuation of $f(z)$ along a path $\\gamma$.",
         ["analytic continuation", "f of z along a path gamma"]),
        # Riemann Surfaces (basic mention)
        (r"The Riemann surface for $\\sqrt{z}$ has two sheets.",
         ["Riemann surface", "square root of z", "two sheets"]),
        # Infinite Products
        (r"An infinite product $\\prod_{n=1}^\\infty (1+a_n)$ converges if...",
         ["infinite product", "product from n equals 1 to infinity of 1 plus a sub n", "converges if"]),
        # Gamma Function (as a complex function)
        (r"The Gamma function $\\Gamma(z) = \\int_0^\\infty t^{z-1}e^{-t} dt$ for $\\text{Re}(z) > 0$.",
         ["Gamma function", "capital gamma of z equals", "integral from 0 to infinity of t to the z minus 1 e to the negative t d t", "real part of z is greater than 0"]),
        # Elliptic Functions (basic mention)
        (r"An elliptic function is a doubly periodic meromorphic function.",
         ["elliptic function", "doubly periodic meromorphic function"]),
    ])
    def test_msc_notation(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)