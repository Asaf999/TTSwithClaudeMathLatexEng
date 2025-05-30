#!/usr/bin/env python3
"""
Torture Test - Try to Break MathSpeak
=====================================

Extreme test cases designed to find breaking points.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from core.engine import MathematicalTTSEngine
import time
import random
import string


def generate_random_latex(length: int) -> str:
    """Generate random LaTeX-like gibberish"""
    commands = ['\\frac', '\\int', '\\sum', '\\prod', '\\lim', '\\sqrt', '\\sin', '\\cos']
    symbols = ['x', 'y', 'z', 'a', 'b', 'c', '\\alpha', '\\beta', '\\gamma']
    operators = ['+', '-', '*', '/', '=', '<', '>']
    
    result = []
    for _ in range(length):
        choice = random.randint(0, 3)
        if choice == 0:
            result.append(random.choice(commands))
        elif choice == 1:
            result.append(random.choice(symbols))
        elif choice == 2:
            result.append(random.choice(operators))
        else:
            result.append('{' if random.random() > 0.5 else '}')
    
    return ' '.join(result)


def torture_test():
    """Run torture tests"""
    engine = MathematicalTTSEngine()
    failures = []
    
    print("😈 TORTURE TEST - Attempting to break MathSpeak")
    print("=" * 60)
    
    # Test 1: Extreme nesting
    print("\n1️⃣ Extreme Nesting Test")
    for depth in [10, 50, 100, 200]:
        expr = "\\frac{" * depth + "1" + "}{2}" * depth
        try:
            start = time.time()
            result = engine.process_latex(expr)
            duration = time.time() - start
            print(f"   Depth {depth}: ✅ Success ({duration:.2f}s)")
        except Exception as e:
            print(f"   Depth {depth}: ❌ Failed - {str(e)[:50]}")
            failures.append(f"Nesting depth {depth}")
    
    # Test 2: Memory exhaustion
    print("\n2️⃣ Memory Exhaustion Test")
    for size in [1000, 10000, 50000]:
        expr = "x + " * size + "y"
        try:
            start = time.time()
            result = engine.process_latex(expr)
            duration = time.time() - start
            print(f"   Size {size}: ✅ Success ({duration:.2f}s)")
        except Exception as e:
            print(f"   Size {size}: ❌ Failed - {str(e)[:50]}")
            failures.append(f"Expression size {size}")
    
    # Test 3: Pathological patterns
    print("\n3️⃣ Pathological Patterns Test")
    patterns = [
        ("Backslash flood", "\\" * 1000),
        ("Brace mismatch", "{" * 100 + "}" * 50),
        ("Empty groups", "{}" * 500),
        ("Nested subscripts", "x" + "_{a" * 50 + "}" * 50),
        ("Unicode bomb", "∫" * 100 + "∂" * 100 + "∇" * 100),
        ("Mixed delimiters", "({[<|" * 100 + "|>]})" * 100),
        ("Infinite fraction", "\\frac{\\frac{\\frac{1}{\\frac{2}{\\frac{3}{4}}}}{5}}{6}"),
        ("Command spam", "\\int\\sum\\prod\\lim" * 100),
    ]
    
    for name, pattern in patterns:
        try:
            start = time.time()
            result = engine.process_latex(pattern)
            duration = time.time() - start
            print(f"   {name}: ✅ Survived ({duration:.2f}s)")
        except Exception as e:
            print(f"   {name}: ❌ Failed - {str(e)[:50]}")
            failures.append(name)
    
    # Test 4: Random chaos
    print("\n4️⃣ Random Chaos Test")
    for i in range(10):
        chaos = generate_random_latex(random.randint(50, 200))
        try:
            start = time.time()
            result = engine.process_latex(chaos)
            duration = time.time() - start
            print(f"   Random {i+1}: ✅ Survived ({duration:.2f}s)")
        except Exception as e:
            print(f"   Random {i+1}: ❌ Failed - {str(e)[:50]}")
            failures.append(f"Random chaos {i+1}")
    
    # Test 5: Algorithmic complexity attacks
    print("\n5️⃣ Complexity Attack Test")
    
    # Exponential pattern matching
    evil_pattern = "a?" * 20 + "a" * 20  # Classic ReDoS pattern
    try:
        start = time.time()
        result = engine.process_latex(evil_pattern)
        duration = time.time() - start
        print(f"   ReDoS pattern: ✅ Survived ({duration:.2f}s)")
    except Exception as e:
        print(f"   ReDoS pattern: ❌ Failed - {str(e)[:50]}")
        failures.append("ReDoS attack")
    
    # Test 6: State corruption
    print("\n6️⃣ State Corruption Test")
    
    # Process valid
    engine.process_latex("x + y = z")
    
    # Process corrupting
    try:
        engine.process_latex("\\def\\x{\\x}\\x")
    except:
        pass
    
    # Try valid again
    try:
        result = engine.process_latex("a + b = c")
        print(f"   State recovery: ✅ Success")
    except Exception as e:
        print(f"   State recovery: ❌ Failed - {str(e)[:50]}")
        failures.append("State corruption")
    
    # Test 7: Encoding nightmares
    print("\n7️⃣ Encoding Nightmare Test")
    nightmares = [
        ("Null bytes", "x\x00y\x00z"),
        ("Control chars", "\x01\x02\x03\x04\x05"),
        ("Invalid UTF-8", b"\xff\xfe".decode('latin1')),
        ("Emoji overload", "🔥" * 100 + "💀" * 100),
        ("RTL override", "\u202Ex + y = z\u202C"),
        ("Zalgo text", "ḩ̷̺͇̤̰̺̪͓͇̀ë̵́ͅl̸̡̼̭̪͚̅̏̌̄̿̌͝͝l̴̢̹̣̟̰̩̬̪̇̊̈́̊͆o̷͎̫̊̈́̃̅̈"),
    ]
    
    for name, nightmare in nightmares:
        try:
            result = engine.process_latex(nightmare)
            print(f"   {name}: ✅ Survived")
        except Exception as e:
            print(f"   {name}: ❌ Failed - {str(e)[:50]}")
            failures.append(name)
    
    # Test 8: Resource limits
    print("\n8️⃣ Resource Limit Test")
    
    # CPU intensive
    cpu_heavy = "\\sum_{i=1}^{1000} \\sum_{j=1}^{1000} \\sum_{k=1}^{1000} i*j*k"
    try:
        start = time.time()
        result = engine.process_latex(cpu_heavy)
        duration = time.time() - start
        if duration > 10:
            print(f"   CPU heavy: ⚠️  Slow ({duration:.2f}s)")
            failures.append("CPU performance")
        else:
            print(f"   CPU heavy: ✅ Success ({duration:.2f}s)")
    except Exception as e:
        print(f"   CPU heavy: ❌ Failed - {str(e)[:50]}")
        failures.append("CPU intensive")
    
    # Summary
    print("\n" + "=" * 60)
    print("TORTURE TEST SUMMARY")
    print("=" * 60)
    
    if not failures:
        print("🎉 AMAZING! MathSpeak survived all torture tests!")
    else:
        print(f"💀 MathSpeak broke on {len(failures)} tests:")
        for f in failures:
            print(f"   - {f}")
    
    print(f"\nRobustness Score: {100 - (len(failures) * 2)}%")
    
    engine.shutdown()


if __name__ == "__main__":
    torture_test()