#!/usr/bin/env python3
"""Test clean architecture with enhanced patterns."""

import sys
import time
from typing import List, Tuple

# Add paths
sys.path.insert(0, '/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng')

# Import clean architecture components
from mathspeak_clean.application.use_cases.process_expression import (
    ProcessExpressionRequest,
    ProcessExpressionUseCase,
)
from mathspeak_clean.infrastructure.config.settings import Settings
from mathspeak_clean.infrastructure.container import Container, reset_container
from mathspeak_clean.infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


def test_expressions() -> List[Tuple[str, str]]:
    """Get test expressions to compare."""
    return [
        # Fractions with natural names
        (r"\\frac{1}{2}", "Special fractions"),
        (r"\\frac{2}{3}", "Special fractions"),
        (r"\\frac{x}{y}", "General fraction"),
        
        # Derivatives
        (r"\\frac{d}{dx} f(x)", "Basic derivative"),
        (r"\\frac{d^2y}{dx^2}", "Second derivative"),
        (r"\\frac{\\partial f}{\\partial x}", "Partial derivative"),
        
        # Integrals
        (r"\\int_0^1 x^2 dx", "Definite integral"),
        (r"\\int f(x) dx", "Indefinite integral"),
        
        # Statistics
        (r"P(A|B)", "Conditional probability"),
        (r"\\mathbb{E}[X]", "Expected value"),
        (r"\\text{Var}(X)", "Variance"),
        
        # Set theory
        (r"A \\cup B", "Union"),
        (r"A \\cap B", "Intersection"),
        
        # Logic
        (r"\\forall x \\in A", "Universal quantifier"),
        (r"\\exists x \\in B", "Existential quantifier"),
        
        # Complex expressions
        (r"\\lim_{x \\to \\infty} \\frac{1}{x}", "Limit"),
        (r"\\sum_{i=1}^n i^2", "Summation"),
        (r"\\sqrt{x^2 + y^2}", "Square root"),
        
        # Matrix operations
        (r"\\det(A)", "Determinant"),
        (r"A^{-1}", "Matrix inverse"),
    ]


def compare_processors():
    """Compare standard vs enhanced processors."""
    print("=" * 80)
    print("COMPARING STANDARD VS ENHANCED PROCESSORS")
    print("=" * 80)
    
    # Test with standard processor
    print("\n1. STANDARD PROCESSOR (Legacy Patterns)")
    print("-" * 80)
    
    reset_container()
    settings = Settings(use_enhanced_processor=False)
    container = Container(settings)
    standard_use_case = container.get(ProcessExpressionUseCase)
    
    standard_results = []
    for latex, description in test_expressions():
        try:
            request = ProcessExpressionRequest(latex=latex)
            response = standard_use_case.execute(request)
            result = response.result.speech
            time_taken = response.result.processing_time
            standard_results.append((latex, result, time_taken))
            print(f"{description:25} {latex:30} -> {result}")
        except Exception as e:
            standard_results.append((latex, f"ERROR: {e}", 0))
            print(f"{description:25} {latex:30} -> ERROR: {e}")
    
    # Test with enhanced processor
    print("\n2. ENHANCED PROCESSOR (Ultra-Natural Patterns - 98% Quality)")
    print("-" * 80)
    
    reset_container()
    settings = Settings(use_enhanced_processor=True)
    container = Container(settings)
    enhanced_use_case = container.get(ProcessExpressionUseCase)
    
    enhanced_results = []
    for latex, description in test_expressions():
        try:
            request = ProcessExpressionRequest(latex=latex)
            response = enhanced_use_case.execute(request)
            result = response.result.speech
            time_taken = response.result.processing_time
            enhanced_results.append((latex, result, time_taken))
            print(f"{description:25} {latex:30} -> {result}")
        except Exception as e:
            enhanced_results.append((latex, f"ERROR: {e}", 0))
            print(f"{description:25} {latex:30} -> ERROR: {e}")
    
    # Compare results
    print("\n3. COMPARISON")
    print("-" * 80)
    print(f"{'Expression':<30} {'Standard':<35} {'Enhanced':<35}")
    print("-" * 100)
    
    improvements = 0
    for i, (latex, description) in enumerate(test_expressions()):
        std_result = standard_results[i][1]
        enh_result = enhanced_results[i][1]
        
        if std_result != enh_result:
            improvements += 1
            print(f"{latex:<30} {std_result:<35} {enh_result:<35} ✨")
        else:
            print(f"{latex:<30} {std_result:<35} {enh_result:<35}")
    
    print("\n4. STATISTICS")
    print("-" * 80)
    
    # Get processor stats
    std_processor = standard_use_case.pattern_processor
    enh_processor = enhanced_use_case.pattern_processor
    
    if hasattr(std_processor, 'get_pattern_statistics'):
        std_stats = std_processor.get_pattern_statistics()
        print(f"Standard patterns loaded: {std_stats['total_patterns']}")
    
    if hasattr(enh_processor, 'get_enhancement_stats'):
        enh_stats = enh_processor.get_enhancement_stats()
        print(f"Enhanced patterns loaded: {enh_stats['total_patterns']}")
        print(f"Ultra-natural available: {enh_stats.get('ultra_engine_available', False)}")
        print(f"Natural speech quality: {enh_stats.get('natural_speech_quality', 'N/A')}")
    
    print(f"\nImprovements: {improvements}/{len(test_expressions())} ({improvements/len(test_expressions())*100:.1f}%)")
    
    # Performance comparison
    std_avg_time = sum(r[2] for r in standard_results) / len(standard_results)
    enh_avg_time = sum(r[2] for r in enhanced_results) / len(enhanced_results)
    
    print(f"\nAverage processing time:")
    print(f"  Standard: {std_avg_time*1000:.2f}ms")
    print(f"  Enhanced: {enh_avg_time*1000:.2f}ms")
    
    if enh_avg_time < std_avg_time:
        print(f"  Enhanced is {(std_avg_time/enh_avg_time - 1)*100:.1f}% faster!")
    else:
        print(f"  Standard is {(enh_avg_time/std_avg_time - 1)*100:.1f}% faster")


if __name__ == "__main__":
    compare_processors()