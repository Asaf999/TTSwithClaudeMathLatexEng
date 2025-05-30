#!/usr/bin/env python3
"""
Test Natural Speech
===================

Comprehensive test of professor-style natural speech.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager


async def test_natural_speech():
    """Test various mathematical expressions for natural speech"""
    
    # Initialize engine
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=True,
        prefer_offline_tts=False  # Use online for best quality
    )
    
    # Test expressions with expected natural speech
    test_cases = [
        # Basic subscripts - NO UNDERSCORE!
        ("$x_0$", "x naught"),
        ("$x_1$", "x sub 1"),
        ("$a_{ij}$", "a i j"),
        ("$A_{23}$", "A 2 3"),
        
        # Powers
        ("$x^2$", "x squared"),
        ("$x^3$", "x cubed"),
        ("$x^n$", "x to the n"),
        ("$e^x$", "e to the x"),
        ("$e^{-x^2}$", "e to the minus x squared"),
        
        # Derivatives
        ("$f'(x)$", "f prime of x"),
        ("$f''(x)$", "f double prime of x"),
        ("$\\frac{df}{dx}$", "d f d x"),
        ("$\\frac{\\partial f}{\\partial x}$", "partial f partial x"),
        
        # Integrals
        ("$\\int_0^1 x^2 dx$", "the integral from 0 to 1 of x squared d x"),
        ("$\\int_{-\\infty}^{\\infty} e^{-x^2} dx$", "the integral from negative infinity to infinity of e to the minus x squared d x"),
        
        # Limits
        ("$\\lim_{x \\to 0} \\frac{\\sin x}{x}$", "the limit as x approaches 0 of sine x over x"),
        ("$\\lim_{n \\to \\infty} (1 + \\frac{1}{n})^n$", "the limit as n approaches infinity of 1 plus 1 over n to the n"),
        
        # Sums
        ("$\\sum_{n=1}^{\\infty} \\frac{1}{n^2}$", "the sum from n equals 1 to infinity of 1 over n squared"),
        ("$\\sum_{i=1}^{n} i$", "the sum from i equals 1 to n of i"),
        
        # Mathematical structures
        ("$\\pi_1(S^1) \\cong \\mathbb{Z}$", "pi 1 of S 1 is isomorphic to Z"),
        ("$f: X \\to Y$", "f maps X to Y"),
        ("$x \\in \\mathbb{R}$", "x is in R"),
        ("$A \\subset B$", "A is a subset of B"),
        
        # Greek letters
        ("$\\alpha + \\beta = \\gamma$", "alpha plus beta equals gamma"),
        ("$\\Delta x$", "Delta x"),
        ("$\\epsilon > 0$", "epsilon greater than 0"),
        
        # Common expressions
        ("$\\forall x \\in \\mathbb{R}$", "for all x in R"),
        ("$\\exists y$", "there exists y"),
        ("$P \\implies Q$", "P implies Q"),
        ("$\\therefore x = 2$", "therefore x equals 2"),
        
        # Matrix elements
        ("The element $A_{ij}$", "The element A i j"),
        ("Matrix entry $B_{23}$", "Matrix entry B 2 3"),
    ]
    
    print("🧪 Testing Natural Professor-Style Speech")
    print("=" * 60)
    
    success = 0
    for expr, expected in test_cases:
        result = engine.process_latex(expr)
        
        # Check if natural
        has_underscore = "underscore" in result.processed.lower()
        has_backslash = "backslash" in result.processed.lower()
        
        status = "✅" if not (has_underscore or has_backslash) else "❌"
        
        print(f"\n{status} Input: {expr}")
        print(f"   Output: {result.processed}")
        print(f"   Expected: {expected}")
        
        if not (has_underscore or has_backslash):
            success += 1
    
    print(f"\n📊 Results: {success}/{len(test_cases)} sound natural")
    
    # Test a full expression
    print("\n🎯 Full Expression Test:")
    full_expr = "The solution to $\\int_0^1 x^2 dx$ is $\\frac{x^3}{3}\\bigg|_0^1 = \\frac{1}{3}$"
    result = engine.process_latex(full_expr)
    print(f"Input: {full_expr}")
    print(f"Output: {result.processed}")
    
    # Generate audio sample
    print("\n🔊 Generating audio sample...")
    audio_file = "natural_speech_test.mp3"
    success = await engine.speak_expression(result, output_file=audio_file)
    if success:
        print(f"✅ Audio saved to: {audio_file}")


if __name__ == "__main__":
    asyncio.run(test_natural_speech())