#!/usr/bin/env python3
"""
MathSpeak Final Demo - Demonstrating System Capabilities
========================================================
"""

import asyncio
import sys
from pathlib import Path

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine, MathematicalContext
from mathspeak.core.voice_manager import VoiceManager, VoiceRole
from mathspeak.utils.logger import setup_logging
import logging

# Setup logging
setup_logging(logging.INFO)

async def main():
    print("🎓 MathSpeak Final Demonstration")
    print("=" * 60)
    
    # Initialize engine
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(voice_manager=voice_manager)
    
    # Demo expressions
    demos = [
        ("Basic Arithmetic", "x^2 + y^2 = r^2"),
        ("Calculus", "\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}"),
        ("Topology", "\\pi_1(S^1) \\cong \\mathbb{Z}"),
        ("Complex Analysis", "\\oint_\\gamma f(z)dz = 2\\pi i \\sum \\text{Res}(f, z_k)"),
        ("Linear Algebra", "\\det(A - \\lambda I) = 0"),
    ]
    
    print("\n📊 Testing Various Mathematical Expressions:\n")
    
    for title, expr in demos:
        print(f"\n{title}:")
        print(f"  LaTeX: {expr}")
        
        # Process expression
        result = engine.process_latex(expr)
        
        print(f"  Speech: {result.processed[:80]}...")
        print(f"  Context: {result.context}")
        print(f"  Time: {result.processing_time:.3f}s")
        
        # Generate audio
        output_file = f"demo_{title.lower().replace(' ', '_')}.mp3"
        success = await engine.speak_expression(result, output_file)
        
        if success:
            print(f"  ✓ Audio saved: {output_file}")
        else:
            print(f"  ✗ Audio generation failed")
    
    # Performance report
    print("\n📈 Performance Report:")
    report = engine.get_performance_report()
    
    metrics = report.get('metrics', {})
    print(f"  Total expressions: {metrics.get('total_expressions', 0)}")
    print(f"  Processing time: {metrics.get('total_time', 0):.2f}s")
    print(f"  Cache hit rate: {metrics.get('cache_hit_rate', 0)*100:.1f}%")
    
    print("\n✅ Demo Complete!")
    print("Check the generated MP3 files to hear the mathematical expressions.")

if __name__ == "__main__":
    asyncio.run(main())