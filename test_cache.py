#!/usr/bin/env python3
"""Test script to verify cache functionality"""

import time
from mathspeak.core.engine import MathematicalTTSEngine

def test_cache():
    """Test cache functionality"""
    print("Testing MathSpeak cache system...")
    
    # Create engine
    engine = MathematicalTTSEngine(enable_caching=True)
    
    # Test expression
    expr = r"\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}"
    
    # First run (should miss cache)
    print("\n1. First run (cache miss expected):")
    start = time.time()
    result1 = engine.process_latex(expr)
    time1 = time.time() - start
    print(f"   Time: {time1:.3f}s")
    print(f"   Result: {result1.processed[:50]}...")
    
    # Get cache stats
    stats = engine._get_cache_stats()
    print(f"   Cache stats: hits={stats.get('hits', 0)}, misses={stats.get('misses', 0)}, size={stats.get('size', 0)}")
    
    # Second run (should hit cache)
    print("\n2. Second run (cache hit expected):")
    start = time.time()
    result2 = engine.process_latex(expr)
    time2 = time.time() - start
    print(f"   Time: {time2:.3f}s")
    print(f"   Speedup: {time1/time2:.1f}x")
    
    # Get cache stats again
    stats = engine._get_cache_stats()
    print(f"   Cache stats: hits={stats.get('hits', 0)}, misses={stats.get('misses', 0)}, size={stats.get('size', 0)}")
    
    # Test with different expression
    print("\n3. Different expression (cache miss expected):")
    expr2 = r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}"
    start = time.time()
    result3 = engine.process_latex(expr2)
    time3 = time.time() - start
    print(f"   Time: {time3:.3f}s")
    
    stats = engine._get_cache_stats()
    print(f"   Cache stats: hits={stats.get('hits', 0)}, misses={stats.get('misses', 0)}, size={stats.get('size', 0)}")
    
    # Test persistence
    print("\n4. Testing cache persistence:")
    engine.shutdown()
    
    # Create new engine
    engine2 = MathematicalTTSEngine(enable_caching=True)
    
    # Try same expression (should hit persisted cache)
    start = time.time()
    result4 = engine2.process_latex(expr)
    time4 = time.time() - start
    print(f"   Time after reload: {time4:.3f}s")
    
    stats = engine2._get_cache_stats()
    print(f"   Cache stats: hits={stats.get('hits', 0)}, misses={stats.get('misses', 0)}, size={stats.get('size', 0)}")
    
    print("\n✓ Cache test complete!")
    
    # Show final stats
    if hasattr(engine2.expression_cache, 'get_stats'):
        final_stats = engine2.expression_cache.get_stats()
        print(f"\nFinal cache statistics:")
        print(f"   Total requests: {final_stats['hits'] + final_stats['misses']}")
        print(f"   Hit rate: {final_stats['hit_rate']:.1%}")
        print(f"   Memory usage: {final_stats['memory_mb']:.2f} MB")
        print(f"   Computation time saved: {final_stats.get('computation_time_saved', 0):.2f}s")

if __name__ == "__main__":
    test_cache()