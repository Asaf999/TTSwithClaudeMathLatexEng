#!/usr/bin/env python3
"""
Demo script showcasing natural mathematical speech
"""

import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

async def demo_natural_speech():
    """Demonstrate the natural mathematical speech capabilities"""
    
    # Initialize engine
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=False,
        prefer_offline_tts=False  # Use online TTS for best quality
    )
    
    # Demo expressions showcasing natural speech
    demos = [
        ("Basic Subscripts and Superscripts", [
            "$x_1 + x_2 = x_3$",
            "$a^2 + b^2 = c^2$",
            "$e^{i\\pi} + 1 = 0$",
        ]),
        
        ("Matrix Elements", [
            "$A_{ij} = \\sum_{k=1}^n B_{ik} C_{kj}$",
            "The element $M_{23}$ is in row 2, column 3",
        ]),
        
        ("Natural Fractions", [
            "$\\frac{1}{2} + \\frac{1}{3} = \\frac{5}{6}$",
            "$\\sin(\\frac{\\pi}{4}) = \\frac{\\sqrt{2}}{2}$",
        ]),
        
        ("Calculus with Natural Differentials", [
            "$\\frac{dy}{dx} = 2x$",
            "$\\int_0^1 x^2 dx = \\frac{1}{3}$",
            "$\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}$",
        ]),
        
        ("Advanced Mathematics", [
            "$\\pi_1(S^1) \\cong \\mathbb{Z}$",
            "$\\lim_{n \\to \\infty} (1 + \\frac{1}{n})^n = e$",
            "$\\forall \\epsilon > 0 \\, \\exists \\delta > 0$ such that $|x - a| < \\delta \\implies |f(x) - f(a)| < \\epsilon$",
        ]),
    ]
    
    print("🎓 MathSpeak Natural Speech Demo")
    print("=" * 60)
    print("This demo showcases how MathSpeak converts mathematical")
    print("expressions into natural, professor-quality speech.")
    print("=" * 60)
    
    for category, expressions in demos:
        print(f"\n📚 {category}")
        print("-" * 40)
        
        for expr in expressions:
            print(f"\nExpression: {expr}")
            
            # Process
            result = engine.process_latex(expr)
            print(f"Speech: {result.processed}")
            
            # Generate audio file
            filename = f"demo_{category.lower().replace(' ', '_')}_{abs(hash(expr)) % 10000}.mp3"
            await engine.speak_expression(result, output_file=filename)
            print(f"Audio saved: {filename}")
    
    print("\n" + "=" * 60)
    print("✅ Demo complete! Audio files have been generated.")
    print("\nKey improvements demonstrated:")
    print("• Subscripts: 'x sub 1' instead of 'x underscore 1'")
    print("• Superscripts: 'x squared', 'x cubed', 'x to the n'")
    print("• Fractions: 'one half', 'three fourths', 'a over b'")
    print("• Differentials: 'd x' instead of 'dx'")
    print("• Matrix elements: 'A i j' for natural flow")
    print("• Greek letters with subscripts: 'pi sub 1'")
    
    engine.shutdown()

if __name__ == "__main__":
    asyncio.run(demo_natural_speech())