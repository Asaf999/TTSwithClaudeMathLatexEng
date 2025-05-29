#!/usr/bin/env python3
"""
Test Suite for the Topology Domain Processor (mathspeak.domains.topology)
========================================================================

Ensures comprehensive coverage for topology notation processing,
from undergraduate basics to M.Sc. level concepts.
"""

import pytest
import re # For more complex assertion needs if any

# Module to be tested
from mathspeak.domains.topology import (
    TopologyProcessor,
    TopologyContext,
    TopologyVocabulary,
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
    """Provides a TopologyProcessor instance for testing (module scope for efficiency)."""
    return TopologyProcessor()

@pytest.fixture(scope="module")
def vocabulary():
    """Provides a TopologyVocabulary instance for testing (module scope)."""
    return TopologyVocabulary()

# --- Test Classes ---

class TestTopologyVocabulary:
    """Tests for the TopologyVocabulary component."""

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Basic Structures
        (r"\\tau", ["tau"]),
        (r"\\mathcal{T}", ["topology script T"]),
        (r"(X,\\tau)", ["topological space X with topology tau"]),
        (r"\\mathcal{B}", ["base script B"]),
        (r"\\mathcal{S}", ["subbase script S"]),
        (r"\\mathcal{U}", ["open cover script U"]),
        (r"\\mathcal{N}", ["neighborhood system script N"]),
        (r"\\mathcal{F}", ["filter script F"]),

        # Separation Axioms
        (r"T_0", ["T naught"]),
        (r"T_1", ["T one"]),
        (r"T_2", ["T two"]),
        (r"T_{2\\frac{1}{2}}", ["T two and a half"]),
        (r"T_3", ["T three"]),
        (r"T_{3\\frac{1}{2}}", ["T three and a half"]),
        (r"T_4", ["T four"]),
        (r"T_5", ["T five"]),
        (r"T_6", ["T six"]),
        (r"T_0\\text{-space}", ["T naught space"]),
        (r"T_1\\text{-space}", ["T one space"]),
        (r"T_2\\text{-space}", ["Hausdorff space"]), # As per topology.py
        (r"\\text{Kolmogorov}", ["Kolmogorov"]),
        (r"\\text{Fréchet}", ["Fréchet"]),
        (r"\\text{Hausdorff}", ["Hausdorff"]),
        (r"\\text{Urysohn}", ["Urysohn"]),
        (r"\\text{regular}", ["regular"]),
        (r"\\text{completely regular}", ["completely regular"]),
        (r"\\text{Tychonoff}", ["Tychonoff"]),
        (r"\\text{normal}", ["normal"]),
        (r"\\text{completely normal}", ["completely normal"]),
        (r"\\text{perfectly normal}", ["perfectly normal"]),

        # Compactness Variations
        (r"\\text{compact}", ["compact"]),
        (r"\\text{sequentially compact}", ["sequentially compact"]),
        (r"\\text{countably compact}", ["countably compact"]),
        (r"\\text{locally compact}", ["locally compact"]),
        (r"\\text{$\\sigma$-compact}", ["sigma-compact"]),
        (r"\\text{Lindelöf}", ["Lindelöf"]),
        (r"\\text{paracompact}", ["paracompact"]),

        # Connectedness Types
        (r"\\text{connected}", ["connected"]),
        (r"\\text{path-connected}", ["path-connected"]),
        (r"\\text{locally connected}", ["locally connected"]),
        (r"\\text{simply connected}", ["simply connected"]),
        (r"\\text{contractible}", ["contractible"]),
        (r"\\text{totally disconnected}", ["totally disconnected"]),

        # Algebraic Topology - Fundamental Groups
        (r"\\Omega X", ["loop space of X"]),
        (r"\\simeq", ["is homotopy equivalent to"]),
        (r"f \\sim g", ["f is homotopic to g"]),

        # Algebraic Topology - Homology/Cohomology
        (r"\\text{Tor}_n", ["Tor n"]),
        (r"\\text{Ext}^n", ["Ext n"]),

        # Covering Spaces
        (r"p: \\tilde{X} \\to X", ["p from tilde X to X"]),
        (r"\\hat{X}", ["universal cover of X"]),

        # Metric and Uniform Spaces
        (r"\\text{Lip}\\(f\\)", ["Lipschitz constant of f"]),

        # Products and Quotients
        (r"X \\times Y", ["X cross Y"]),
        (r"X \\sqcup Y", ["X disjoint union Y"]),
        (r"X/A", ["X mod A"]),
        (r"X \\vee Y", ["X wedge Y"]),
        (r"X \\subset Y", ["X is a subset of Y"]),

        # Standard Spaces
        (r"\\mathbb{R}", ["real line"]),
        (r"S^1", ["1-sphere"]), # "the 1-sphere"
        (r"D^n", ["n-disk"]),
        (r"I", ["unit interval"]),
        (r"\\mathbb{RP}^n", ["real projective n-space"]),
        (r"\\mathbb{CP}^2", ["complex projective 2-space"]),


        # Fiber Bundles
        (r"E \\to B", ["E over B"]),
        (r"TM", ["tangent bundle of M"]),
        (r"T\\*M", ["cotangent bundle of M"]),

        # CW Complexes
        (r"e^n", ["n-cell"]),
        (r"\\text{CW}", ["CW"]),
        (r"\\Delta^n", ["standard n-simplex"]),

        # Special Notation
        (r"\\cong", ["is isomorphic to"]),
        (r"\\approx", ["is homeomorphic to"]), # Often used for homeo in topology
        (r"\\hookrightarrow", ["embeds into"]),
        (r"\\twoheadrightarrow", ["surjects onto"]),
        (r"\\text{id}", ["identity"]),
        (r"\\iota", ["iota"]),
    ])
    def test_direct_vocabulary_terms(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, arg, expected_keywords", [
        (r"\\overline{{A}}", "A", ["closure of A"]),
        (r"\\overline{{X \\cup Y}}", "X \\cup Y", ["closure of X union Y"]),
        (r"\\text{cl}(U)", "U", ["closure of U"]),
        (r"\\text{int}(V)", "V", ["interior of V"]),
        (r"S^\\circ", "S", ["interior of S"]), # Test the alternative interior notation
        (r"\\partial M", "M", ["boundary of M"]),
        (r"N'", "N", ["derived set of N"]),
    ])
    def test_operator_lambda_terms(self, processor, latex_input, arg, expected_keywords):
        # For these, the lambda usually processes the argument.
        # We are testing if the overall structure is correct.
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, group_arg, expected_keywords_parts", [
        (r"\\pi_1(X)", "X", ["fundamental group of X"]),
        (r"\\pi_0(Y)", "Y", ["pi naught of Y"]),
        (r"\\pi_3(Z)", "Z", ["third homotopy group of Z"]), # Uses _ordinal
        (r"\\pi_n(K)", "K", ["n-th homotopy group of K"]),
        (r"\\pi_*(S^2)", "S^2", ["homotopy groups of the 2-sphere"]),
    ])
    def test_homotopy_group_lambda_terms(self, processor, latex_input, group_arg, expected_keywords_parts):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords_parts)

    @pytest.mark.parametrize("latex_input, space_arg, coeff_arg, expected_keywords_parts", [
        (r"H_2(X)", "X", None, ["second homology group of X"]),
        (r"H_n(Y)", "Y", None, ["n-th homology group of Y"]),
        (r"H_0(A; \\mathbb{Z})", "A", "\\mathbb{Z}", ["zeroth homology of A with coefficients in Z"]),
        (r"H^3(B)", "B", None, ["third cohomology group of B"]),
        (r"H^m(C; G)", "C", "G", ["m-th cohomology of C with coefficients in G"]),
        (r"\\tilde{H}_1(S^1)", "S^1", None, ["first reduced homology of the 1-sphere"]),
        (r"\\chi(K)", "K", None, ["Euler characteristic of K"]),
        (r"b_2(M)", "M", None, ["second Betti number of M"]),
    ])
    def test_homology_cohomology_lambda_terms(self, processor, latex_input, space_arg, coeff_arg, expected_keywords_parts):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords_parts)

    @pytest.mark.parametrize("latex_input, arg1, arg2, expected_keywords", [
        (r"d(x,y)", "x,y", ["distance from x to y"]),
        (r"\\rho(a,b)", "a,b", ["rho of a and b"]),
        (r"B(p, \\epsilon)", "p, \\epsilon", ["open ball centered at p with radius epsilon"]),
        (r"\\overline{B}(z_0, r)", "z_0, r", ["closed ball centered at z naught with radius r"]),
        (r"S(0,1)", "0,1", ["sphere centered at 0 with radius 1"]),
    ])
    def test_metric_space_lambda_terms(self, processor, latex_input, arg1, arg2, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, n_val, expected_keywords", [
         (r"\\mathbb{R}^3", "3", ["3-dimensional Euclidean space", "three-dimensional"]),
         (r"S^2", "2", ["2-sphere", "two-sphere"]),
         (r"\\mathbb{CP}^4", "4", ["complex projective 4-space", "four-space"]),
    ])
    def test_numbered_spaces_lambda(self, processor, latex_input, n_val, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords, all_must_be_present=False) # Allow for slight variations

    @pytest.mark.parametrize("number_str, expected_ordinal", [
        ("0", "zeroth"), ("1", "first"), ("2", "second"), ("3", "third"),
        ("4", "fourth"), ("5", "fifth"), ("10", "tenth"), ("11", "11-th"), ("23", "23rd")
    ])
    def test_ordinal_conversion(self, vocabulary, number_str, expected_ordinal):
        # Note: The current _ordinal in topology.py only goes up to 10.
        # This test reflects that, but for full M.Sc. scope, _ordinal might need expansion.
        if int(number_str) <= 10 or number_str in vocabulary._ordinal_map: # Accessing internal for test
            assert vocabulary._ordinal(number_str) == expected_ordinal
        elif number_str.endswith('1') and not number_str.endswith('11'):
             assert vocabulary._ordinal(number_str) == f"{number_str}st"
        elif number_str.endswith('2') and not number_str.endswith('12'):
             assert vocabulary._ordinal(number_str) == f"{number_str}nd"
        elif number_str.endswith('3') and not number_str.endswith('13'):
             assert vocabulary._ordinal(number_str) == f"{number_str}rd"
        else:
            assert vocabulary._ordinal(number_str) == f"{number_str}th"


    @pytest.mark.parametrize("number_str, expected_name", [
        ("1", "one"), ("2", "two"), ("7", "seven"), ("10", "ten"), ("11", "11")
    ])
    def test_number_name_conversion(self, vocabulary, number_str, expected_name):
        # Similar to _ordinal, _number_name in topology.py is limited.
        if int(number_str) <=10 :
            assert vocabulary._number_name(number_str) == expected_name
        else:
            assert vocabulary._number_name(number_str) == number_str


class TestTopologyPatterns:
    """Tests for the regex patterns defined for general topological phrases."""
    @pytest.mark.parametrize("latex_input, expected_keywords", [
        ("f:X\\to Y is continuous", ["f from X to Y is continuous"]),
        ("g : A \\to B is continuous", ["g from A to B is continuous"]),
        ("U is open in X", ["U is open in X"]),
        ("F is closed in Y", ["F is closed in Y"]),
        ("K is clopen", ["K is clopen"]),
        ("N is a neighborhood of x", ["N is a neighborhood of x"]),
        ("D is dense in X", ["D is dense in X"]),
        ("S is nowhere dense", ["S is nowhere dense"]),
        ("x_n \\to x", ["x sub n converges to x"]),
        ("The sequence {y_k} \\to y", ["sequence y sub k converges to y"]),
        ("The quotient map q: X \\to Y", ["quotient map q from X to Y"]),
        ("H: M \\times I \\to N is a homotopy", ["H from M cross I to N", "homotopy"]),
        ("r: X \\to A is a retraction", ["r from X to A is a retraction"]),
        ("A is a retract of X", ["A is a retract of X"]),
        ("A is a deformation retract of X", ["A is a deformation retract of X"]),
        ("p: E \\to B is a fibration", ["p from E to B is a fibration"]),
        ("The group G acts on X", ["group G acts on X"]),
        ("The orbit space is X/G", ["orbit space X mod G"]),
    ])
    def test_general_patterns(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)


class TestTopologySubContextDetection:
    @pytest.mark.parametrize("latex_input, expected_context_enum", [
        ("A space X is compact if every open cover has a finite subcover.", TopologyContext.POINT_SET),
        ("The fundamental group \\pi_1(S^1) \\cong \\mathbb{Z}.", TopologyContext.ALGEBRAIC),
        ("A smooth manifold M with its tangent bundle TM.", TopologyContext.DIFFERENTIAL),
        ("The distance d(x,y) in a metric space (X,d).", TopologyContext.METRIC_SPACES),
        ("Consider the set of real numbers \\mathbb{R} with the usual topology.", TopologyContext.POINT_SET), # More specific than GENERAL
        ("Homology group H_n(X; G) is a key invariant.", TopologyContext.ALGEBRAIC),
        ("A vector bundle E \\to B has fibers that are vector spaces.", TopologyContext.DIFFERENTIAL), # Or ALGEBRAIC depending on usage
        ("A CW complex is built by attaching cells e^n.", TopologyContext.ALGEBRAIC),
        ("This is a general mathematical statement not specific to topology.", TopologyContext.GENERAL),
    ])
    def test_sub_context_detection(self, processor, latex_input, expected_context_enum):
        assert processor.detect_subcontext(latex_input) == expected_context_enum


class TestTopologyProcessing:
    """End-to-end tests for TopologyProcessor.process()."""

    def test_separation_axiom_processing(self, processor):
        latex = "A space is $T_1$ if for distinct points $x, y$, there is an open set $U$ containing $x$ but not $y$."
        spoken_text = processor.process(latex)
        expected = ["T one", "distinct points", "open set", "containing x but not y"]
        assert_spoken_contains(spoken_text, expected)
        assert "A space is" in spoken_text # Check for natural start

    def test_compactness_definition_processing(self, processor):
        latex = "A topological space $X$ is compact if every open cover $\\mathcal{U}$ of $X$ has a finite subcover."
        spoken_text = processor.process(latex)
        expected = ["topological space X is compact", "every open cover script U of X", "finite subcover"]
        assert_spoken_contains(spoken_text, expected)

    def test_fundamental_group_notation_processing(self, processor):
        latex = "The fundamental group of the circle $S^1$ is $\\pi_1(S^1) \\cong \\mathbb{Z}$."
        spoken_text = processor.process(latex)
        expected = ["fundamental group", "circle", "S one", "pi one of", "isomorphic to", "the integers"]
        assert_spoken_contains(spoken_text, expected)

    def test_homology_statement_processing(self, processor):
        latex = "The $n$-th homology group $H_n(X; G)$ captures $n$-dimensional holes with $G$-coefficients."
        spoken_text = processor.process(latex)
        expected = ["n-th homology group", "H sub n of X with coefficients in G", "n-dimensional holes", "G-coefficients"]
        assert_spoken_contains(spoken_text, expected)

    def test_metric_space_definition(self, processor):
        latex = "A metric space $(M, d)$ consists of a set $M$ and a metric $d: M \\times M \\to \\mathbb{R}_{\ge 0}$."
        spoken_text = processor.process(latex)
        expected = ["metric space", "M comma d", "set M", "metric d from M cross M to", "non-negative real numbers"] # R_>=0 might need specific handling
        assert_spoken_contains(spoken_text, expected)


class TestTopologySpecialRules:
    """Tests for specific rules like theorem emphasis."""
    @pytest.mark.parametrize("theorem_name_latex, theorem_name_spoken_emphasized_parts", [
        ("Urysohn's Lemma", ["Urysohn's Lemma"]),
        ("Tietze Extension Theorem", ["Tietze Extension Theorem"]),
        ("Tychonoff's Theorem", ["Tychonoff's Theorem"]),
        ("The Stone-Čech compactification", ["Stone-Čech compactification"]),
    ])
    def test_theorem_emphasis(self, processor, theorem_name_latex, theorem_name_spoken_emphasized_parts):
        # This test assumes that the NLP layer or VoiceManager handles {{EMPHASIS}} tags.
        # The processor itself just adds the tags.
        latex = f"An important result is {theorem_name_latex}."
        spoken_text = processor.process(latex)

        # Check if the original name is present (possibly modified by NLP later)
        # and that emphasis markers were added by the domain processor.
        # This is a bit tricky as the final output depends on other layers.
        # For now, we check if the processor's output contains the markers.
        # This might need adjustment based on how {{EMPHASIS}} is handled.
        
        # A simple check:
        processed_by_domain = processor._apply_special_rules(theorem_name_latex) # Test the rule directly
        assert "{{EMPHASIS}}" in processed_by_domain
        assert "{{/EMPHASIS}}" in processed_by_domain
        for part in theorem_name_spoken_emphasized_parts:
             assert part.lower() in processed_by_domain.lower().replace("{{emphasis}}", "").replace("{{/emphasis}}", "")


class TestTopologyEdgeCases:
    """Tests for edge cases and robustness."""
    def test_empty_input(self, processor):
        assert processor.process("") == ""

    def test_whitespace_input(self, processor):
        assert processor.process("   ") == "" # Or " " depending on cleanup

    def test_non_topological_input(self, processor):
        latex = "This is a simple sentence with no topology."
        spoken_text = processor.process(latex)
        # Should ideally pass through mostly unchanged or with basic NLP.
        # For domain processor, it might just return it as is if no patterns match.
        assert "simple sentence" in spoken_text.lower()
        assert processor.detect_subcontext(latex) == TopologyContext.GENERAL

    def test_mixed_content_prioritization(self, processor):
        # Example: A statement that has both point-set and algebraic terms
        latex = "Let $X$ be a compact space. Its fundamental group $\\pi_1(X)$ is finitely generated."
        spoken_text = processor.process(latex)
        assert_spoken_contains(spoken_text, ["compact space", "fundamental group", "pi one of X", "finitely generated"])
        # Check which context gets detected (might be POINT_SET or ALGEBRAIC depending on keyword strength)
        detected_context = processor.detect_subcontext(latex)
        assert detected_context in [TopologyContext.POINT_SET, TopologyContext.ALGEBRAIC]


class TestTopologyMScLevelNotation:
    """Tests specifically targeting M.Sc. level notation."""

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Homology/Cohomology
        (r"The Mayer-Vietoris sequence relates $H_n(A \\cup B)$ to $H_n(A)$, $H_n(B)$, and $H_n(A \\cap B)$.",
         ["Mayer-Vietoris sequence", "H sub n of A union B"]),
        (r"The cup product $H^p(X;R) \\times H^q(X;R) \\to H^{p+q}(X;R)$.",
         ["cup product", "H super p of X with coefficients in R", "H super q", "H super p plus q"]),
        (r"Poincaré duality states $H^k(M) \\cong H_{n-k}(M)$ for an $n$-manifold $M$.",
         ["Poincaré duality", "H super k of M", "H sub n minus k of M", "n-manifold M"]),

        # Fiber Bundles
        (r"A principal $G$-bundle $P \\to X$ has a free right $G$-action.",
         ["principal G-bundle", "P over X", "free right G-action"]),
        (r"The tangent bundle $TM$ of a smooth manifold $M$.",
         ["tangent bundle TM", "smooth manifold M"]),
        (r"A section $s: B \\to E$ such that $\\pi \\circ s = \\text{id}_B$.",
         ["section s from B to E", "pi composed with s equals the identity on B"]),

        # CW Complexes
        (r"A CW complex $X$ is built by attaching $n$-cells $e^n_\\alpha$ via maps $\\phi_\\alpha: S^{n-1} \\to X^{(n-1)}$.",
         ["CW complex X", "attaching n-cells e alpha", "maps phi alpha from S n minus 1 to", "n minus 1 skeleton"]),
        (r"The cellular homology $C_n^{CW}(X) = H_n(X^{(n)}, X^{(n-1)})$.",
         ["cellular homology", "C CW sub n of X", "H sub n of X n, X n minus 1"]),

        # Covering Spaces Advanced
        (r"The universal cover $\\hat{X}$ is unique up to isomorphism.",
         ["universal cover", "X hat", "unique up to isomorphism"]),
        (r"The group of deck transformations $\\text{Deck}(\\tilde{p})$ acts freely on $\\tilde{X}$.",
         ["group of deck transformations", "Deck of p tilde", "acts freely on X tilde"]),
    ])
    def test_msc_notation(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)