#!/usr/bin/env python3
"""
Demo script to showcase the Mathematical TTS Engine
"""

from core.engine import MathematicalTTSEngine

def main():
    # Initialize the engine
    engine = MathematicalTTSEngine()
    
    # Test expressions
    test_expressions = [
        r"\frac{\sqrt{\pi}}{2}",
        r"\frac{\pi}{4}",
        r"\frac{e^2}{3}",
        r"\frac{1}{\sqrt{2}}",
        r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}",
        r"\lim_{x \to 0} \frac{\sin x}{x} = 1",
        r"\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}",
        r"e^{i\pi} + 1 = 0",
        r"\forall x \in \mathbb{R}, x^2 \geq 0",
        r"f(x) = \sqrt{x^2 + 1}",
    ]
    
    print("Mathematical TTS Engine Demo")
    print("=" * 80)
    print()
    
    for expr in test_expressions:
        result = engine.process_latex(expr)
        print(f"Input:  {expr}")
        print(f"Output: {result.processed}")
        print(f"Time:   {result.processing_time:.3f}s")
        if result.unknown_commands:
            print(f"Unknown: {result.unknown_commands}")
        print("-" * 80)
    
    # Show performance report
    print("\nPerformance Report:")
    print("=" * 80)
    report = engine.get_performance_report()
    print(f"Tokens per second: {report['metrics']['tokens_per_second']:.1f}")
    print(f"Cache hit rate: {report['cache']['cache_hit_rate']:.1%}")
    
    # Shutdown
    engine.shutdown()

if __name__ == "__main__":
    main()