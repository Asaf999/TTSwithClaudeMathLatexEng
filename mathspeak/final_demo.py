#!/usr/bin/env python3
"""
MathSpeak Final Demo
====================

Demonstrates the complete natural speech system.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager


async def final_demo():
    """Run final demo of natural mathematical speech"""
    
    print("🎓 MathSpeak - Natural Mathematical Speech Demo")
    print("=" * 60)
    print("Speaking mathematics like a real professor!\n")
    
    # Initialize
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=True,
        prefer_offline_tts=False
    )
    
    # Demo expressions
    demos = [
        ("Basic Algebra", "$f(x) = x^2 + 3x + 1$"),
        ("Derivatives", "$f'(x) = \\frac{d}{dx}(x^2 + 3x + 1) = 2x + 3$"),
        ("Integrals", "$\\int_0^1 x^2 dx = \\frac{x^3}{3}\\bigg|_0^1 = \\frac{1}{3}$"),
        ("Limits", "$\\lim_{x \\to 0} \\frac{\\sin x}{x} = 1$"),
        ("Series", "$e^x = \\sum_{n=0}^{\\infty} \\frac{x^n}{n!}$"),
        ("Matrix Elements", "The element $A_{ij}$ of the matrix $A$"),
        ("Topology", "$\\pi_1(S^1) \\cong \\mathbb{Z}$"),
        ("Complex Analysis", "$\\oint_C \\frac{f(z)}{z-a} dz = 2\\pi i f(a)$"),
        ("Logic", "$\\forall \\epsilon > 0 \\, \\exists \\delta > 0 : |x-a| < \\delta \\implies |f(x)-f(a)| < \\epsilon$"),
        ("ODE", "$\\frac{d^2y}{dx^2} + p(x)\\frac{dy}{dx} + q(x)y = 0$"),
    ]
    
    audio_files = []
    
    for title, expr in demos:
        print(f"\n📐 {title}")
        print(f"   LaTeX: {expr}")
        
        # Process
        result = engine.process_latex(expr)
        print(f"   Speech: \"{result.processed}\"")
        
        # Generate audio
        audio_file = f"demo_{title.lower().replace(' ', '_')}.mp3"
        success = await engine.speak_expression(result, output_file=audio_file)
        
        if success:
            audio_files.append(audio_file)
            print(f"   ✅ Audio: {audio_file}")
        else:
            print(f"   ❌ Failed to generate audio")
    
    print(f"\n\n✨ Demo complete! Generated {len(audio_files)} audio files.")
    print("\nKey improvements:")
    print("✅ No more 'underscore' - uses natural subscript pronunciation")
    print("✅ Powers sound natural: 'x squared', 'x cubed', 'x to the n'")
    print("✅ Derivatives: 'f prime of x', 'd f d x'")
    print("✅ Integrals: 'the integral from a to b'")
    print("✅ Greek letters pronounced naturally")
    print("✅ Mathematical notation spoken like a professor would")
    
    # Cleanup
    engine.shutdown()


if __name__ == "__main__":
    # Run without warnings
    import warnings
    warnings.filterwarnings("ignore")
    
    asyncio.run(final_demo())