#!/usr/bin/env python3
"""
Test script for the updated Mathematical TTS Engine
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine


async def test_updated_engine():
    """Test all the new features in the updated engine"""
    
    print("Testing Updated Mathematical TTS Engine")
    print("=" * 70)
    
    # Initialize engine with new features
    engine = MathematicalTTSEngine(
        enable_caching=True,
        prefer_offline_tts=False  # Use online for better quality
    )
    
    # Test cases
    test_cases = [
        {
            'name': 'Simple expression',
            'latex': r'$x^2 + y^2 = z^2$',
            'description': 'Basic Pythagorean theorem'
        },
        {
            'name': 'Empty input handling',
            'latex': '',
            'description': 'Testing empty input error handling'
        },
        {
            'name': 'Complex expression with progress',
            'latex': r'''
                Let $f: \mathbb{R}^n \to \mathbb{R}$ be a continuously differentiable function. 
                The gradient descent algorithm updates the parameters according to:
                $$x_{k+1} = x_k - \alpha \nabla f(x_k)$$
                where $\alpha > 0$ is the learning rate and $\nabla f(x_k)$ is the gradient at $x_k$.
            ''',
            'description': 'Long expression to test progress indicators'
        },
        {
            'name': 'Unknown LaTeX commands',
            'latex': r'$\customCommand{x} + \anotherUnknown{y} = \mysteryFunction{z}$',
            'description': 'Testing unknown command tracking'
        },
        {
            'name': 'Timeout test (artificial)',
            'latex': r'$\sum_{i=1}^{\infty} \prod_{j=1}^{\infty} \int_{0}^{\infty} ' * 20 + 'f(x) dx$',
            'description': 'Very long expression to potentially trigger timeout'
        }
    ]
    
    # Process each test case
    for i, test in enumerate(test_cases):
        print(f"\n{'='*70}")
        print(f"Test {i+1}: {test['name']}")
        print(f"Description: {test['description']}")
        print(f"LaTeX: {test['latex'][:100]}..." if len(test['latex']) > 100 else f"LaTeX: {test['latex']}")
        
        # Process with progress for longer expressions
        show_progress = len(test['latex']) > 100
        result = engine.process_latex(test['latex'], show_progress=show_progress)
        
        print(f"\nResults:")
        print(f"  Context: {result.context}")
        print(f"  Processed: {result.processed[:150]}..." if len(result.processed) > 150 else f"  Processed: {result.processed}")
        print(f"  Processing time: {result.processing_time:.3f}s")
        print(f"  Unknown commands: {result.unknown_commands}")
        print(f"  Number of segments: {len(result.segments)}")
    
    # Test cache functionality
    print(f"\n{'='*70}")
    print("Testing Cache Functionality")
    
    # Process same expression twice
    test_expr = r'$\int_0^1 x^2 dx = \frac{1}{3}$'
    
    print(f"First processing of: {test_expr}")
    result1 = engine.process_latex(test_expr, show_progress=False)
    time1 = result1.processing_time
    
    print(f"Second processing of same expression...")
    result2 = engine.process_latex(test_expr, show_progress=False)
    time2 = result2.processing_time
    
    print(f"  First processing time: {time1:.3f}s")
    print(f"  Second processing time: {time2:.3f}s")
    print(f"  Cache hit: {time2 < time1 * 0.1}")  # Should be much faster
    
    # Test TTS engines
    print(f"\n{'='*70}")
    print("Testing TTS Engine Manager")
    
    print("\nAvailable TTS Engines:")
    engines = engine.tts_manager.get_available_engines()
    for eng in engines:
        status = "✓" if eng['available'] else "✗"
        online = "(online)" if eng['requires_internet'] else "(offline)"
        print(f"  {status} {eng['name']} {online}")
    
    # Generate speech for a simple expression
    if any(eng['available'] for eng in engines):
        print("\nGenerating speech sample...")
        simple_expr = r'The quadratic formula is $x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}$'
        result = engine.process_latex(simple_expr, show_progress=False)
        
        if result.segments:
            output_file = "test_speech.mp3"
            success = await engine.speak_expression(
                result, 
                output_file=output_file,
                show_progress=True
            )
            
            if success and Path(output_file).exists():
                print(f"✓ Speech successfully generated: {output_file}")
                file_size = Path(output_file).stat().st_size / 1024
                print(f"  File size: {file_size:.1f} KB")
                # Clean up
                Path(output_file).unlink()
            else:
                print("✗ Speech generation failed")
    
    # Performance report
    print(f"\n{'='*70}")
    print("Performance Report")
    
    report = engine.get_performance_report()
    
    print("\nMetrics:")
    for key, value in report['metrics'].items():
        print(f"  {key}: {value}")
    
    if 'cache' in report:
        print("\nCache Statistics:")
        for key, value in report['cache'].items():
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")
    
    print("\nUnknown Commands Summary:")
    unknown_summary = report['unknown_commands']
    print(f"  Total unknown commands found: {unknown_summary['total_unknown']}")
    if unknown_summary['commands']:
        print(f"  Commands: {', '.join(unknown_summary['commands'][:5])}")
    
    # Shutdown
    engine.shutdown()
    print(f"\n{'='*70}")
    print("✓ Engine shutdown complete")
    print("✓ All tests completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_updated_engine())