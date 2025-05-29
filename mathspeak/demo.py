#!/usr/bin/env python3
"""
MathSpeak Demo Script
====================

Demonstrates the capabilities of the MathSpeak system across various
mathematical domains.
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from mathspeak import MathSpeak


async def main():
    """Run the MathSpeak demo"""
    
    # Create MathSpeak instance
    ms = MathSpeak(debug=True)
    
    print("🎯 MathSpeak Ultimate Mathematical TTS System Demo")
    print("=" * 60)
    print()
    
    # Demo expressions covering different domains
    demo_expressions = [
        # Basic Calculus
        (
            "Calculus",
            r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"
        ),
        
        # Topology
        (
            "Topology", 
            r"A topological space (X, \tau) is called T_2 (Hausdorff) if \forall x,y \in X with x \neq y, \exists U,V \in \tau such that x \in U, y \in V, and U \cap V = \emptyset"
        ),
        
        # Complex Analysis
        (
            "Complex Analysis",
            r"By Cauchy's theorem, if f is holomorphic on \Omega and \gamma is a closed curve in \Omega, then \oint_\gamma f(z) dz = 0"
        ),
        
        # Numerical Analysis
        (
            "Numerical Analysis",
            r"The Newton-Raphson method: x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} converges quadratically when |f''(x)||f(x)| < |f'(x)|^2"
        ),
        
        # Differential Geometry (Manifolds)
        (
            "Differential Geometry",
            r"The tangent bundle TM = \bigsqcup_{p \in M} T_p M has a natural projection \pi: TM \to M"
        ),
        
        # Ordinary Differential Equations
        (
            "ODEs",
            r"For the second-order linear ODE y'' + p(x)y' + q(x)y = 0, the Wronskian W(y_1, y_2) = y_1 y_2' - y_2 y_1' determines linear independence"
        ),
        
        # Real Analysis
        (
            "Real Analysis",
            r"\forall \epsilon > 0, \exists \delta > 0 : |x - a| < \delta \Rightarrow |f(x) - f(a)| < \epsilon"
        ),
        
        # Set Theory
        (
            "Set Theory",
            r"A = \{x \in \mathbb{R} : x^2 < 4\} = (-2, 2)"
        ),
        
        # Linear Algebra
        (
            "Linear Algebra",
            r"\det(A - \lambda I) = 0 \iff \lambda \text{ is an eigenvalue of } A"
        ),
        
        # Number Theory
        (
            "Number Theory",
            r"\gcd(a,b) = \gcd(b, a \bmod b) \text{ for } b \neq 0"
        )
    ]
    
    # Process each expression
    for domain, expression in demo_expressions:
        print(f"\n🔷 {domain}")
        print(f"📝 LaTeX: {expression}")
        
        try:
            # Process the expression
            result = await ms.process_async(expression)
            
            print(f"🗣️  Speech: {result['speech']}")
            print(f"🎯 Context: {result['context']}")
            print(f"⏱️  Time: {result['processing_time']:.3f}s")
            
            # Generate audio file
            output_file = f"demo_{domain.lower().replace(' ', '_')}.mp3"
            # await ms.save_speech_async(expression, output_file)
            # print(f"🔊 Audio saved to: {output_file}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 60)
    
    # Interactive mode demo
    print("\n\n🎮 Interactive Mode Demo")
    print("=" * 60)
    print("You can use MathSpeak interactively with: mathspeak --interactive")
    print("Available commands:")
    print("  /help     - Show help")
    print("  /test     - Run test expressions")
    print("  /voice    - Change voice settings")
    print("  /save     - Save last result")
    print("  /history  - Show history")
    print("  /config   - Show configuration")
    print("  /exit     - Exit")
    
    # Performance stats
    print("\n\n📊 Performance Statistics")
    print("=" * 60)
    stats = ms.get_stats()
    print(f"Total expressions processed: {stats['total_expressions']}")
    print(f"Average processing time: {stats['average_time']:.3f}s")
    print(f"Cache hit rate: {stats['cache_hit_rate']:.1%}")
    print(f"Active domains: {', '.join(stats['domains_used'])}")
    
    print("\n✅ Demo complete!")


if __name__ == "__main__":
    asyncio.run(main())