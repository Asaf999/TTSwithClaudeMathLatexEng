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
        (r"(X,\\mathcal{T})", ["topological space X with topology script T"]),
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
        (r"\\text{metacompact}", ["metacompact"]),
        (r"\\text{orthocompact}", ["orthocompact"]),
        (r"\\text{pseudocompact}", ["pseudocompact"]),
        (r"\\text{realcompact}", ["realcompact"]),
        (r"\\text{$k$-space}", ["k-space"]),
        (r"\\text{hemicompact}", ["hemicompact"]),

        # Connectedness Types
        (r"\\text{connected}", ["connected"]),
        (r"\\text{path-connected}", ["path-connected"]),
        (r"\\text{arcwise connected}", ["arcwise connected"]),
        (r"\\text{locally connected}", ["locally connected"]),
        (r"\\text{locally path-connected}", ["locally path-connected"]),
        (r"\\text{simply connected}", ["simply connected"]),
        (r"\\text{contractible}", ["contractible"]),
        (r"\\text{totally disconnected}", ["totally disconnected"]),
        (r"\\text{zero-dimensional}", ["zero-dimensional"]),
        (r"\\text{extremally disconnected}", ["extremally disconnected"]),
        (r"\\text{hyperconnected}", ["hyperconnected"]),
        (r"\\text{ultraconnected}", ["ultraconnected"]),

        # Algebraic Topology - Fundamental Groups
        (r"\\Omega X", ["loop space of X"]),
        (r"\\Omega_x X", ["based loop space at x in X"]),
        (r"\\simeq", ["is homotopy equivalent to"]),
        (r"\\sim", ["is homotopic to"]),
        (r"f \\simeq g", ["f is homotopic to g"]),
        (r"X \\simeq Y", ["X is homotopy equivalent to Y"]),

        # Algebraic Topology - Homology/Cohomology
        (r"\\text{Tor}_n", ["Tor n"]),
        (r"\\text{Ext}^n", ["Ext n"]),

        # Covering Spaces
        (r"p\\colon \\tilde{X} \\to X", ["p from tilde X to X"]),
        (r"p: \\tilde{X} \\to X", ["p from tilde X to X"]),
        (r"\\text{ev}_x", ["evaluation map at x"]),
        (r"\\hat{X}", ["universal cover of X"]),

        # Metric and Uniform Spaces
        (r"\\text{Lip}\\(f\\)", ["Lipschitz constant of f"]),
        (r"\\text{osc}\\(f,x\\)", ["oscillation of f at x"]),

        # Products and Quotients
        (r"X \\times Y", ["X cross Y"]),
        (r"\\prod_{i \\in I} X_i", ["product over i in I of X sub i"]),
        (r"\\prod X_i", ["product of X sub i"]),
        (r"\\coprod X_i", ["coproduct of X sub i"]),
        (r"\\bigsqcup X_i", ["disjoint union of X sub i"]),
        (r"X \\sqcup Y", ["X disjoint union Y"]),
        (r"X/A", ["X mod A"]),
        (r"X/\\sim", ["X mod the equivalence relation"]),
        (r"X \\vee Y", ["X wedge Y"]),
        (r"\\bigvee X_i", ["wedge sum of X sub i"]),
        (r"X \\cup Y", ["X union Y"]),
        (r"X \\cap Y", ["X intersect Y"]),
        (r"X \\setminus Y", ["X minus Y"]),
        (r"X - Y", ["X minus Y"]),
        (r"X \\subset Y", ["X is a subset of Y"]),
        (r"X \\subseteq Y", ["X is a subset of or equal to Y"]),
        (r"X \\subsetneq Y", ["X is a proper subset of Y"]),

        # Standard Spaces
        (r"\\mathbb{R}", ["real line"]),
        (r"\\mathbb{R}^n", ["n-dimensional Euclidean space"]),
        (r"\\mathbb{C}", ["complex plane"]),
        (r"\\mathbb{C}^n", ["n-dimensional complex space"]),
        (r"\\mathbb{H}", ["quaternions"]),
        (r"\\mathbb{S}^n", ["n-sphere"]),
        (r"S^n", ["n-sphere"]),
        (r"S^1", ["1-sphere"]),
        (r"D^n", ["n-disk"]),
        (r"B^n", ["n-ball"]),
        (r"I", ["unit interval"]),
        (r"I^n", ["n-cube"]),
        (r"\\mathbb{T}^n", ["n-torus"]),
        (r"T^n", ["n-torus"]),
        (r"\\mathbb{RP}^n", ["real projective n-space"]),
        (r"\\mathbb{CP}^n", ["complex projective n-space"]),
        (r"\\mathbb{CP}^2", ["complex projective 2-space"]),
        (r"\\mathbb{HP}^n", ["quaternionic projective n-space"]),
        (r"K(\\pi,n)", ["Eilenberg-MacLane space of type pi comma n"]),
        (r"K(G,n)", ["Eilenberg-MacLane space with group G in degree n"]),


        # Fiber Bundles and Vector Bundles
        (r"E \\to B", ["E over B"]),
        (r"\\pi: E \\to B", ["projection pi from E to B"]),
        (r"E \\xrightarrow{\\pi} B", ["E maps to B via pi"]),
        (r"F \\hookrightarrow E \\to B", ["fiber bundle with fiber F, total space E, and base B"]),
        (r"\\xi", ["bundle xi"]),
        (r"\\eta", ["bundle eta"]),
        (r"TM", ["tangent bundle of M"]),
        (r"T\\*M", ["cotangent bundle of M"]),
        (r"T_p M", ["tangent space to M at p"]),
        (r"T\\*_p M", ["cotangent space to M at p"]),
        (r"\\Lambda^k T\\*M", ["k-th exterior power of the cotangent bundle"]),
        (r"\\text{rank}\\(\\xi\\)", ["rank of the bundle xi"]),
        (r"\\gamma^n", ["universal n-plane bundle"]),
        (r"\\text{Vect}_n\\(X\\)", ["set of n-dimensional vector bundles over X"]),
        (r"\\text{Prin}_G\\(X\\)", ["set of principal G-bundles over X"]),

        # CW Complexes
        (r"X^{\\(n\\)}", ["n-skeleton of X"]),
        (r"e^n", ["n-cell"]),
        (r"e^n_\\alpha", ["n-cell e alpha"]),
        (r"\\text{sk}_n\\(X\\)", ["n-skeleton of X"]),
        (r"\\phi_\\alpha: S^{n-1} \\to X^{\\(n-1\\)}", ["attaching map phi alpha from the n minus 1 sphere to the n minus 1 skeleton"]),
        (r"X \\cup_f e^n", ["X with an n-cell attached via f"]),
        (r"\\text{CW}", ["CW"]),
        (r"\\Delta^n", ["standard n-simplex"]),
        (r"\\partial \\Delta^n", ["boundary of the n-simplex"]),

        # Special Notation
        (r"\\cong", ["is isomorphic to"]),
        (r"\\approx", ["is homeomorphic to"]),
        (r"\\equiv", ["is equivalent to"]),
        (r"\\hookrightarrow", ["embeds into"]),
        (r"\\twoheadrightarrow", ["surjects onto"]),
        (r"\\xrightarrow{f}", ["maps via f to"]),
        (r"\\xleftarrow{g}", ["receives via g from"]),
        (r"f_\\*", ["f subscript star"]),
        (r"f^\\*", ["f superscript star"]),
        (r"f_!", ["f shriek"]),
        (r"f^!", ["f upper shriek"]),
        (r"\\text{id}", ["identity"]),
        (r"\\text{Id}", ["identity"]),
        (r"1_X", ["identity on X"]),
        (r"\\text{incl}", ["inclusion"]),
        (r"\\iota", ["iota"]),
    ])
    def test_direct_vocabulary_terms(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, arg, expected_keywords", [
        # Closure operators
        (r"\\overline{{A}}", "A", ["closure of A"]),
        (r"\\overline{{X \\cup Y}}", "X \\cup Y", ["closure of X union Y"]),
        (r"\\bar{{S}}", "S", ["closure of S"]),
        (r"\\text{cl}(U)", "U", ["closure of U"]),
        (r"\\text{cl}(A \\cap B)", "A \\cap B", ["closure of A intersect B"]),
        
        # Interior operators
        (r"\\text{int}(V)", "V", ["interior of V"]),
        (r"\\text{Int}(W)", "W", ["interior of W"]),
        (r"S^\\circ", "S", ["interior of S"]),
        
        # Boundary operators
        (r"\\partial M", "M", ["boundary of M"]),
        (r"\\text{bd}(K)", "K", ["boundary of K"]),
        (r"\\text{Bd}(L)", "L", ["boundary of L"]),
        (r"\\text{fr}(U)", "U", ["frontier of U"]),
        
        # Derived sets and limit points
        (r"N'", "N", ["derived set of N"]),
        (r"\\text{Lim}(E)", "E", ["limit points of E"]),
        (r"\\text{Iso}(F)", "F", ["isolated points of F"]),
    ])
    def test_operator_lambda_terms(self, processor, latex_input, arg, expected_keywords):
        # For these, the lambda usually processes the argument.
        # We are testing if the overall structure is correct.
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)

    @pytest.mark.parametrize("latex_input, group_arg, expected_keywords_parts", [
        (r"\\pi_1(X)", "X", ["fundamental group of X"]),
        (r"\\pi_1(X,x_0)", "X,x_0", ["fundamental group of X based at x naught"]),
        (r"\\pi_0(Y)", "Y", ["pi naught of Y"]),
        (r"\\pi_3(Z)", "Z", ["third homotopy group of Z"]), # Uses _ordinal
        (r"\\pi_7(S^4)", "S^4", ["seventh homotopy group of the 4-sphere"]),
        (r"\\pi_n(K)", "K", ["n-th homotopy group of K"]),
        (r"\\pi_*(S^2)", "S^2", ["homotopy groups of the 2-sphere"]),
        (r"\\text{Map}(X,Y)", "X,Y", ["mapping space from X to Y"]),
        (r"\\text{Map}(S^1, \\mathbb{R}^2)", "S^1,R^2", ["mapping space from the 1-sphere to 2-dimensional Euclidean space"]),
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

    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Covering space notation
        (r"\\tilde{X}", ["tilde X"]),
        (r"\\tilde{M}", ["tilde M"]),
        (r"p^{-1}(x)", ["fiber over x"]),
        (r"p^{-1}(U)", ["fiber over U"]),
        (r"\\text{Cov}(X)", ["category of covering spaces of X"]),
        (r"\\text{Deck}(p)", ["deck transformation group of p"]),
        (r"\\text{Deck}(\\tilde{X}/X)", ["deck transformation group of tilde X over X"]),
        (r"\\text{Aut}(\\tilde{X})", ["automorphism group of tilde X"]),
    ])
    def test_covering_space_lambda_terms(self, processor, latex_input, expected_keywords):
        spoken_text = processor.process(latex_input)
        assert_spoken_contains(spoken_text, expected_keywords)


class TestTopologyPatterns:
    """Tests for the regex patterns defined for general topological phrases."""
    @pytest.mark.parametrize("latex_input, expected_keywords", [
        # Continuous functions
        ("f:X\\to Y is continuous", ["f from X to Y is continuous"]),
        ("g : A \\to B is continuous", ["g from A to B is continuous"]),
        ("h : C \\to D is continuous", ["h from C to D is continuous"]),
        
        # Open/closed sets
        ("U is open in X", ["U is open in X"]),
        ("F is closed in Y", ["F is closed in Y"]),
        ("K is clopen", ["K is clopen"]),
        
        # Neighborhoods
        ("N is a neighborhood of x", ["N is a neighborhood of x"]),
        ("\\mathcal{N}(p)", ["neighborhood system of p"]),
        ("\\mathcal{N}(x_0)", ["neighborhood system of x naught"]),
        
        # Density
        ("D is dense in X", ["D is dense in X"]),
        ("S is nowhere dense", ["S is nowhere dense"]),
        
        # Convergence
        ("x_n \\to x", ["x sub n converges to x"]),
        ("\\{a_n\\} \\to a", ["sequence a sub n converges to a"]),
        ("The sequence {y_k} \\to y", ["sequence y sub k converges to y"]),
        
        # Quotient maps
        ("q : X \\to X/\\sim", ["q from X to X mod the equivalence relation"]),
        ("The quotient map q: X \\to Y", ["quotient map q from X to Y"]),
        
        # Homotopies
        ("F : X \\times I \\to Y", ["F from X cross I to Y"]),
        ("H: M \\times I \\to N is a homotopy", ["H from M cross I to N", "homotopy"]),
        
        # Retractions
        ("r: X \\to A is a retraction", ["r from X to A is a retraction"]),
        ("A is a retract of X", ["A is a retract of X"]),
        ("A is a deformation retract of X", ["A is a deformation retract of X"]),
        
        # Fibrations and cofibrations
        ("p: E \\to B is a fibration", ["p from E to B is a fibration"]),
        ("i : A \\to X is a cofibration", ["i from A to X is a cofibration"]),
        
        # Group actions
        ("G acts on X", ["G acts on X"]),
        ("G \\times X \\to X", ["G cross X to X"]),
        ("the orbit space X/G", ["orbit space X mod G"]),
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
        ("Alexandroff compactification", ["Alexandroff one-point compactification"]),
    ])
    def test_theorem_emphasis(self, processor, theorem_name_latex, theorem_name_spoken_emphasized_parts):
        # This test assumes that the NLP layer or VoiceManager handles {{EMPHASIS}} tags.
        # The processor itself just adds the tags.
        latex = f"An important result is {theorem_name_latex}."
        spoken_text = processor.process(latex)

        # Check if the theorem name is present in the output
        for part in theorem_name_spoken_emphasized_parts:
            assert part.lower() in spoken_text.lower()
        
        # Also test the special rules directly
        processed_by_rules = processor._apply_special_rules(theorem_name_latex)
        # The emphasis tags should be added for known theorems
        if "Lemma" in theorem_name_latex or "Theorem" in theorem_name_latex or "compactification" in theorem_name_latex:
            assert "{{EMPHASIS}}" in processed_by_rules or theorem_name_latex in processed_by_rules
    
    def test_context_info(self, processor):
        """Test the get_context_info method"""
        info = processor.get_context_info()
        assert info['domain'] == 'topology'
        assert 'subcontext' in info
        assert 'vocabulary_size' in info
        assert 'pattern_count' in info
        assert info['vocabulary_size'] > 100  # We have many vocabulary items
        assert info['pattern_count'] > 10  # We have many patterns


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
    
    def test_preprocessing_abbreviations(self, processor):
        """Test the _preprocess method's abbreviation expansion"""
        test_cases = [
            ("A top. space", "topological space"),
            ("cts. function", "continuous function"),
            ("nbd of x", "neighborhood of x"),
            ("nbhd of y", "neighborhood of y"),
            ("cpt set", "compact set"),
            ("conn. component", "connected component"),
            ("homeo. to", "homeomorphic to"),
            ("equiv. relation", "equivalent relation"),
        ]
        for input_text, expected_phrase in test_cases:
            result = processor.process(input_text)
            assert expected_phrase in result.lower()
    
    def test_double_article_cleanup(self, processor):
        """Test the _postprocess method's article cleanup"""
        # This tests internal processing that might create double articles
        test_cases = [
            ("the the topology", "the topology"),
            ("a a space", "a space"),
            ("a an open set", "an open set"),
            ("an a closed set", "a closed set"),
        ]
        for input_text, expected_clean in test_cases:
            # Process through _postprocess directly
            result = processor._postprocess(input_text)
            assert expected_clean in result
    
    def test_complex_nested_expressions(self, processor):
        """Test processing of deeply nested mathematical expressions"""
        latex = r"\\overline{\\text{cl}(\\text{int}(A \\cup B))}"
        spoken_text = processor.process(latex)
        # Should handle nested operations
        assert "closure" in spoken_text
        assert "interior" in spoken_text
        assert "union" in spoken_text
    
    def test_malformed_latex(self, processor):
        """Test handling of malformed LaTeX"""
        malformed_cases = [
            r"\\pi_1(X",  # Missing closing parenthesis
            r"\\overline{A",  # Missing closing brace
            r"\\text{int(A)}",  # Missing backslash before parenthesis
        ]
        for latex in malformed_cases:
            # Should not crash, but may not produce perfect output
            try:
                result = processor.process(latex)
                assert isinstance(result, str)
            except Exception as e:
                pytest.fail(f"Processor crashed on malformed input: {latex}\nError: {e}")


class TestTopologyInternalMethods:
    """Tests for internal methods of TopologyVocabulary."""
    
    def test_process_nested(self, vocabulary):
        """Test the _process_nested method for handling nested content"""
        test_cases = [
            (r"\\mathbb{R}", "R"),
            (r"\\mathbb{C}", "C"),
            (r"\\mathbb{Z}", "Z"),
            (r"\\mathbb{Q}", "Q"),
            (r"\\mathbb{N}", "N"),
            (r"X_1", "X sub 1"),
            (r"Y^2", "Y to the 2"),
            (r"\\mathbb{R}^n", "R to the n"),
            (r"X_i^j", "X sub i to the j"),
        ]
        for input_str, expected_output in test_cases:
            result = vocabulary._process_nested(input_str)
            assert expected_output in result
    
    def test_ordinal_edge_cases(self, vocabulary):
        """Test _ordinal with various numbers"""
        test_cases = [
            ("0", "zeroth"),
            ("1", "first"),
            ("2", "second"),
            ("3", "third"),
            ("4", "fourth"),
            ("5", "fifth"),
            ("6", "sixth"),
            ("7", "seventh"),
            ("8", "eighth"),
            ("9", "ninth"),
            ("10", "tenth"),
            ("11", "11-th"),
            ("21", "21-th"),
            ("100", "100-th"),
        ]
        for num_str, expected in test_cases:
            assert vocabulary._ordinal(num_str) == expected
    
    def test_number_name_edge_cases(self, vocabulary):
        """Test _number_name with various numbers"""
        test_cases = [
            ("1", "one"),
            ("2", "two"),
            ("3", "three"),
            ("4", "four"),
            ("5", "five"),
            ("6", "six"),
            ("7", "seven"),
            ("8", "eight"),
            ("9", "nine"),
            ("10", "ten"),
            ("11", "11"),
            ("20", "20"),
            ("100", "100"),
        ]
        for num_str, expected in test_cases:
            assert vocabulary._number_name(num_str) == expected


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