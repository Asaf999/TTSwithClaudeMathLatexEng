#!/usr/bin/env python3
"""Simple test for clean architecture."""

import sys
sys.path.append('/home/puncher/MathATTSVer2/TTSwithClaudeMathLatexEng')

from mathspeak_clean.infrastructure.config.settings import Settings
from mathspeak_clean.infrastructure.container import Container, reset_container
from mathspeak_clean.application.use_cases.process_expression import (
    ProcessExpressionUseCase,
    ProcessExpressionRequest
)

def test_clean_architecture():
    """Test basic clean architecture functionality."""
    print("Testing MathSpeak Clean Architecture\n")
    
    # Test 1: Enhanced mode (default)
    print("1. Testing Enhanced Mode (98% natural speech)")
    print("-" * 50)
    
    reset_container()
    container = Container()  # Uses default settings with enhanced=True
    use_case = container.get(ProcessExpressionUseCase)
    
    test_cases = [
        r"\frac{1}{2}",
        r"\frac{d}{dx} f(x)",
        r"\int_0^1 x^2 dx",
        r"P(A|B)",
        r"\sin^2(x) + \cos^2(x) = 1",
    ]
    
    for latex in test_cases:
        try:
            request = ProcessExpressionRequest(latex=latex)
            response = use_case.execute(request)
            print(f"✅ {latex:<25} → {response.result.speech}")
        except Exception as e:
            print(f"❌ {latex:<25} → ERROR: {e}")
    
    # Test 2: Standard mode
    print("\n2. Testing Standard Mode (Legacy patterns)")
    print("-" * 50)
    
    reset_container()
    settings = Settings(use_enhanced_processor=False)
    container = Container(settings)
    use_case = container.get(ProcessExpressionUseCase)
    
    for latex in test_cases[:3]:  # Test fewer cases
        try:
            request = ProcessExpressionRequest(latex=latex)
            response = use_case.execute(request)
            print(f"✅ {latex:<25} → {response.result.speech}")
        except Exception as e:
            print(f"❌ {latex:<25} → ERROR: {e}")
    
    # Test 3: Caching
    print("\n3. Testing Cache Performance")
    print("-" * 50)
    
    reset_container()
    container = Container()
    use_case = container.get(ProcessExpressionUseCase)
    
    import time
    
    # First call
    request = ProcessExpressionRequest(latex=r"\frac{1}{2}")
    start = time.time()
    response1 = use_case.execute(request)
    time1 = time.time() - start
    
    # Second call (should be cached)
    start = time.time()
    response2 = use_case.execute(request)
    time2 = time.time() - start
    
    print(f"First call:  {time1:.4f}s (cached: {response1.cached})")
    print(f"Second call: {time2:.4f}s (cached: {response2.cached})")
    if response2.cached and time2 < time1 / 5:
        print(f"✅ Cache working! {time1/time2:.1f}x speedup")
    else:
        print("⚠️  Cache might not be working optimally")
    
    # Test 4: Error handling
    print("\n4. Testing Error Handling")
    print("-" * 50)
    
    invalid_cases = [
        (r"", "Empty expression"),
        (r"\frac{1", "Unbalanced braces"),
        (r"x" * 20000, "Too long"),
    ]
    
    for latex, description in invalid_cases:
        try:
            request = ProcessExpressionRequest(latex=latex)
            response = use_case.execute(request)
            print(f"⚠️  {description} was accepted (unexpected)")
        except Exception as e:
            print(f"✅ {description} correctly rejected: {type(e).__name__}")
    
    print("\n✨ Clean architecture test complete!")

if __name__ == "__main__":
    test_clean_architecture()