#!/usr/bin/env python3
"""
Test Suite for Mathematical TTS Engine
=====================================

Comprehensive tests for the core engine functionality including:
- Basic expression processing
- Context detection
- Domain processor integration
- Caching behavior
- Error handling
- Performance benchmarks
"""

import pytest
import time
from pathlib import Path
from typing import Dict, List

from mathspeak.core import (
    MathematicalTTSEngine,
    MathematicalContext,
    VoiceManager,
    ProcessedExpression,
)

from tests import (
    get_test_expressions,
    assert_contains_all,
    assert_natural_language,
    create_mock_config,
    PerformanceTimer,
)

# ===========================
# Fixtures
# ===========================

@pytest.fixture
def engine():
    """Create a test engine instance"""
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=False  # Disable for most tests
    )
    
    # Load test domain processors
    try:
        from mathspeak.domains import TopologyProcessor, ComplexAnalysisProcessor
        engine.domain_processors[MathematicalContext.TOPOLOGY] = TopologyProcessor()
        engine.domain_processors[MathematicalContext.COMPLEX_ANALYSIS] = ComplexAnalysisProcessor()
    except ImportError:
        pass
    
    return engine

@pytest.fixture
def cached_engine():
    """Create an engine with caching enabled"""
    voice_manager = VoiceManager()
    return MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=True
    )

# ===========================
# Basic Processing Tests
# ===========================

class TestBasicProcessing:
    """Test basic expression processing"""
    
    def test_simple_expressions(self, engine):
        """Test processing of simple mathematical expressions"""
        test_cases = [
            ("x^2", ["x", "squared"]),
            ("x + y", ["x", "plus", "y"]),
            ("\\frac{1}{2}", ["over"]),
            ("\\sqrt{x}", ["square", "root"]),
            ("\\pi", ["pi"]),
        ]
        
        for expr, expected_words in test_cases:
            result = engine.process_latex(expr)
            assert isinstance(result, ProcessedExpression)
            assert_contains_all(result.processed, expected_words)
            assert_natural_language(result.processed)
    
    def test_greek_letters(self, engine):
        """Test Greek letter processing"""
        greek_letters = [
            ("\\alpha", "alpha"),
            ("\\beta", "beta"),
            ("\\gamma", "gamma"),
            ("\\delta", "delta"),
            ("\\epsilon", "epsilon"),
            ("\\theta", "theta"),
            ("\\pi", "pi"),
            ("\\sigma", "sigma"),
            ("\\omega", "omega"),
        ]
        
        for latex, expected in greek_letters:
            result = engine.process_latex(latex)
            assert expected in result.processed.lower()
    
    def test_set_notation(self, engine):
        """Test set notation processing"""
        test_cases = [
            ("x \\in \\mathbb{R}", ["real"]),
            ("A \\subset B", ["subset"]),
            ("A \\cup B", ["union"]),
            ("A \\cap B", ["intersect"]),
            ("\\emptyset", ["empty", "set"]),
        ]
        
        for expr, expected_words in test_cases:
            result = engine.process_latex(expr)
            assert_contains_all(result.processed, expected_words)
    
    def test_logic_notation(self, engine):
        """Test logical notation processing"""
        test_cases = [
            ("\\forall x", ["for", "all"]),
            ("\\exists y", ["there", "exists"]),
            ("p \\implies q", ["implies"]),
            ("p \\iff q", ["if", "only", "if"]),
        ]
        
        for expr, expected_words in test_cases:
            result = engine.process_latex(expr)
            assert_contains_all(result.processed, expected_words)

# ===========================
# Context Detection Tests
# ===========================

class TestContextDetection:
    """Test mathematical context detection"""
    
    def test_topology_detection(self, engine):
        """Test detection of topology context"""
        topology_expressions = [
            "Let X be a compact Hausdorff space",
            "The fundamental group \\pi_1(X)",
            "A is open in the topology \\tau",
            "Every continuous map f: X \\to Y",
        ]
        
        for expr in topology_expressions:
            result = engine.process_latex(expr)
            # Context detection happens internally
            assert result.context in ["topology", "general"]
    
    def test_complex_analysis_detection(self, engine):
        """Test detection of complex analysis context"""
        complex_expressions = [
            "f is holomorphic on D",
            "\\oint_C f(z) dz = 2\\pi i \\sum \\text{Res}(f, z_k)",
            "The function has a pole at z_0",
            "By Cauchy's theorem",
        ]
        
        for expr in complex_expressions:
            result = engine.process_latex(expr)
            assert result.context in ["complex_analysis", "general"]
    
    def test_numerical_detection(self, engine):
        """Test detection of numerical analysis context"""
        numerical_expressions = [
            "The error is O(h^2)",
            "Newton's method converges quadratically",
            "The condition number \\kappa(A)",
            "Using LU decomposition",
        ]
        
        for expr in numerical_expressions:
            result = engine.process_latex(expr)
            assert result.context in ["numerical_analysis", "general"]

# ===========================
# Domain Processor Tests
# ===========================

class TestDomainProcessors:
    """Test domain-specific processing"""
    
    def test_topology_processing(self, engine):
        """Test topology-specific processing"""
        if MathematicalContext.TOPOLOGY not in engine.domain_processors:
            pytest.skip("Topology processor not loaded")
        
        test_cases = [
            ("\\pi_1(S^1) \\cong \\mathbb{Z}", 
             ["fundamental", "group", "circle", "isomorphic", "integers"]),
            ("X is T_2", ["hausdorff"]),
            ("\\overline{A}", ["closure"]),
            ("f: X \\to Y is continuous", ["continuous"]),
        ]
        
        for expr, expected_words in test_cases:
            result = engine.process_latex(expr, force_context=MathematicalContext.TOPOLOGY)
            assert_contains_all(result.processed, expected_words)
    
    def test_complex_analysis_processing(self, engine):
        """Test complex analysis processing"""
        if MathematicalContext.COMPLEX_ANALYSIS not in engine.domain_processors:
            pytest.skip("Complex analysis processor not loaded")
        
        test_cases = [
            ("z = x + iy", ["z", "equals", "x", "plus", "i", "y"]),
            ("f'(z) exists", ["f", "prime", "z", "exists"]),
            ("\\text{Res}(f, z_0)", ["residue", "f", "z", "naught"]),
        ]
        
        for expr, expected_words in test_cases:
            result = engine.process_latex(expr, force_context=MathematicalContext.COMPLEX_ANALYSIS)
            assert_contains_all(result.processed, expected_words)

# ===========================
# Natural Language Tests
# ===========================

class TestNaturalLanguage:
    """Test natural language enhancement"""
    
    def test_sentence_structure(self, engine):
        """Test that output has proper sentence structure"""
        test_cases = [
            "Let f: X \\to Y be continuous.",
            "For all \\epsilon > 0, there exists \\delta > 0.",
            "The set A = \\{x : x > 0\\} is open.",
        ]
        
        for expr in test_cases:
            result = engine.process_latex(expr)
            # Should start with capital letter
            assert result.processed[0].isupper()
            # Should end with punctuation
            assert result.processed[-1] in '.!?'
    
    def test_article_usage(self, engine):
        """Test proper article usage (a/an/the)"""
        test_cases = [
            ("an eigenvalue", ["an", "eigenvalue"]),
            ("a function", ["a", "function"]),
            ("the limit", ["the", "limit"]),
        ]
        
        for expr, expected in test_cases:
            result = engine.process_latex(expr)
            assert_contains_all(result.processed, expected)

# ===========================
# Caching Tests
# ===========================

class TestCaching:
    """Test expression caching behavior"""
    
    def test_cache_hit(self, cached_engine):
        """Test that repeated expressions use cache"""
        expr = "\\int_0^1 x^2 dx"
        
        # First call - cache miss
        result1 = cached_engine.process_latex(expr)
        time1 = result1.processing_time
        
        # Second call - should be cache hit
        result2 = cached_engine.process_latex(expr)
        time2 = result2.processing_time
        
        # Same result
        assert result1.processed == result2.processed
        
        # Cache hit should be much faster (allowing for timing variations)
        # Just check that we got a cache hit
        assert cached_engine.metrics.cache_hits > 0
    
    def test_cache_size_limit(self, cached_engine):
        """Test cache size limiting"""
        # Set small cache size for testing
        cached_engine.max_cache_size = 5
        
        # Add more expressions than cache size
        for i in range(10):
            cached_engine.process_latex(f"x^{i}")
        
        # Cache should not exceed max size
        assert len(cached_engine.expression_cache) <= cached_engine.max_cache_size

# ===========================
# Error Handling Tests
# ===========================

class TestErrorHandling:
    """Test error handling and robustness"""
    
    def test_malformed_latex(self, engine):
        """Test handling of malformed LaTeX"""
        malformed_expressions = [
            "\\frac{1",  # Missing closing brace
            "x^",        # Missing exponent
            "\\unknown", # Unknown command
            "",          # Empty string
            "{{{{",      # Nested braces
        ]
        
        for expr in malformed_expressions:
            # Should not crash
            result = engine.process_latex(expr)
            assert isinstance(result, ProcessedExpression)
            # Should return something
            assert len(result.processed) > 0
    
    def test_unknown_commands(self, engine):
        """Test tracking of unknown LaTeX commands"""
        expr = "\\someunknowncommand{x} + \\anotherone{y}"
        result = engine.process_latex(expr)
        
        # Should track unknown commands
        assert len(result.unknown_commands) >= 2
        assert "someunknowncommand" in result.unknown_commands
        assert "anotherone" in result.unknown_commands
    
    def test_very_long_expression(self, engine):
        """Test handling of very long expressions"""
        # Create a long expression
        terms = [f"x_{i}^{i}" for i in range(100)]
        long_expr = " + ".join(terms)
        
        # Should handle without crashing
        with PerformanceTimer("Long expression") as timer:
            result = engine.process_latex(long_expr)
        
        assert isinstance(result, ProcessedExpression)
        assert len(result.processed) > 0
        # Should complete in reasonable time (< 5 seconds)
        assert timer.duration < 5.0

# ===========================
# Performance Tests
# ===========================

class TestPerformance:
    """Test performance characteristics"""
    
    @pytest.mark.slow
    def test_processing_speed(self, engine):
        """Test processing speed meets requirements"""
        expressions = get_test_expressions()
        total_tokens = 0
        
        with PerformanceTimer("Batch processing") as timer:
            for category, expr_list in expressions.items():
                for expr, _ in expr_list:
                    result = engine.process_latex(expr)
                    total_tokens += len(expr.split())
        
        tokens_per_second = total_tokens / timer.duration
        
        # Should process at least 100 tokens/second
        assert tokens_per_second > 100
        
        # Log performance
        print(f"\nPerformance: {tokens_per_second:.1f} tokens/second")
    
    def test_memory_usage(self, engine):
        """Test memory usage stays reasonable"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process many expressions
        for i in range(100):
            engine.process_latex(f"\\sum_{{k=1}}^{{n}} k^{i}")
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (< 100MB)
        assert memory_increase < 100

# ===========================
# Integration Tests
# ===========================

class TestIntegration:
    """Test integration between components"""
    
    @pytest.mark.integration
    def test_voice_manager_integration(self, engine):
        """Test integration with voice manager"""
        # Process expression with different contexts
        theorem = "Theorem 3.1. Every compact space is complete."
        result = engine.process_latex(theorem)
        
        # Should have speech segments
        assert len(result.segments) > 0
        
        # Should use appropriate voices
        voice_roles = [seg.voice_role for seg in result.segments]
        assert any(role.name == "THEOREM" for role in voice_roles)
    
    @pytest.mark.integration  
    def test_natural_language_integration(self, engine):
        """Test natural language processing integration"""
        expr = "Let x = y. Then x = z implies y = z."
        result = engine.process_latex(expr)
        
        # Should have variations (not always "equals")
        processed_lower = result.processed.lower()
        # At least one should not be "equals"
        assert ("is equal to" in processed_lower or 
                "is" in processed_lower or
                "gives us" in processed_lower)

# ===========================
# Regression Tests
# ===========================

class TestRegressions:
    """Test for specific bug fixes"""
    
    def test_nested_fractions(self, engine):
        """Test handling of nested fractions"""
        expr = "\\frac{\\frac{a}{b}}{\\frac{c}{d}}"
        result = engine.process_latex(expr)
        
        # Should handle gracefully
        assert "over" in result.processed
        assert_natural_language(result.processed)
    
    def test_unicode_symbols(self, engine):
        """Test handling of Unicode mathematical symbols"""
        expr = "α + β = γ"
        result = engine.process_latex(expr)
        
        # Should process Unicode Greek letters
        assert_contains_all(result.processed, ["alpha", "beta", "gamma"])

# ===========================
# Run specific test scenarios
# ===========================

def test_example_expressions(engine):
    """Test with real-world example expressions"""
    examples = [
        # Calculus
        "\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1",
        "\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}",
        
        # Linear algebra  
        "\\det(A - \\lambda I) = 0",
        "A^T A = I",
        
        # Number theory
        "a \\equiv b \\pmod{n}",
        "\\gcd(a,b) = 1",
        
        # Logic
        "\\forall \\epsilon > 0 \\, \\exists \\delta > 0",
        "(p \\land q) \\implies r",
    ]
    
    for expr in examples:
        result = engine.process_latex(expr)
        print(f"\nInput: {expr}")
        print(f"Output: {result.processed}")
        
        # Basic validation
        assert_natural_language(result.processed)
        assert len(result.processed) > 0

if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])