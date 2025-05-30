#!/usr/bin/env python3
"""
Test Anki Integration
====================

Simple test to verify MathSpeak Anki integration works.
"""

import asyncio
import sys
from pathlib import Path

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager


async def test_anki_audio_generation():
    """Test generating audio for typical Anki card expressions"""
    
    print("🧪 Testing MathSpeak Anki Integration")
    print("=" * 50)
    
    # Initialize engine
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=True,
        prefer_offline_tts=False
    )
    
    # Typical Anki card expressions
    test_cards = [
        {
            'front': 'What is the derivative of $x^2$?',
            'back': 'The derivative is $\\frac{d}{dx}x^2 = 2x$',
            'expressions': ['x^2', '\\frac{d}{dx}x^2 = 2x']
        },
        {
            'front': 'State the Pythagorean theorem',
            'back': '$a^2 + b^2 = c^2$ for a right triangle',
            'expressions': ['a^2 + b^2 = c^2']
        },
        {
            'front': 'What is $\\pi_1(S^1)$?',
            'back': 'The fundamental group of the circle is $\\pi_1(S^1) \\cong \\mathbb{Z}$',
            'expressions': ['\\pi_1(S^1)', '\\pi_1(S^1) \\cong \\mathbb{Z}']
        },
        {
            'front': 'Evaluate $\\int_0^1 x^2 dx$',
            'back': '$\\int_0^1 x^2 dx = \\left[\\frac{x^3}{3}\\right]_0^1 = \\frac{1}{3}$',
            'expressions': ['\\int_0^1 x^2 dx', '\\left[\\frac{x^3}{3}\\right]_0^1 = \\frac{1}{3}']
        }
    ]
    
    print(f"\nTesting {len(test_cards)} sample Anki cards...\n")
    
    success_count = 0
    
    for i, card in enumerate(test_cards, 1):
        print(f"Card {i}:")
        print(f"  Front: {card['front']}")
        print(f"  Back: {card['back']}")
        print(f"  Expressions to process: {len(card['expressions'])}")
        
        for j, expr in enumerate(card['expressions']):
            try:
                # Process expression
                result = engine.process_latex(expr)
                
                # Generate audio file
                audio_file = f"anki_test_{i}_{j}.mp3"
                success = await engine.speak_expression(result, output_file=audio_file)
                
                if success and Path(audio_file).exists():
                    file_size = Path(audio_file).stat().st_size
                    print(f"    ✅ Generated: {audio_file} ({file_size} bytes)")
                    print(f"       Speech: \"{result.processed}\"")
                    success_count += 1
                    
                    # Clean up test file
                    Path(audio_file).unlink()
                else:
                    print(f"    ❌ Failed to generate audio for: {expr}")
                    
            except Exception as e:
                print(f"    ❌ Error: {e}")
        
        print()
    
    total_expressions = sum(len(card['expressions']) for card in test_cards)
    print(f"\n📊 Results: {success_count}/{total_expressions} expressions processed successfully")
    
    if success_count == total_expressions:
        print("✅ All tests passed! MathSpeak is ready for Anki integration.")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    # Test batch processing simulation
    print("\n🔄 Testing batch processing simulation...")
    
    expressions = [
        "\\sum_{n=1}^\\infty \\frac{1}{n^2}",
        "e^{i\\pi} + 1 = 0",
        "\\nabla \\times \\vec{F} = 0"
    ]
    
    start_time = asyncio.get_event_loop().time()
    
    for expr in expressions:
        result = engine.process_latex(expr)
    
    elapsed = asyncio.get_event_loop().time() - start_time
    
    print(f"Processed {len(expressions)} expressions in {elapsed:.3f}s")
    print(f"Average: {elapsed/len(expressions)*1000:.1f}ms per expression")
    
    print("\n✨ Anki integration test complete!")


def main():
    """Run the test"""
    asyncio.run(test_anki_audio_generation())


if __name__ == "__main__":
    main()