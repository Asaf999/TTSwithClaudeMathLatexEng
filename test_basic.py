#!/usr/bin/env python3
"""
Basic test to check if core components work
"""

import sys
from pathlib import Path

# Test basic imports
try:
    # Test patterns_v2 directly
    from mathspeak.core.patterns_v2 import MathSpeechProcessor
    print("✓ Successfully imported MathSpeechProcessor from patterns_v2")
    
    # Test creating an instance
    processor = MathSpeechProcessor()
    print("✓ Successfully created MathSpeechProcessor instance")
    
    # Test basic processing
    test_expr = r"\int_0^1 x^2 dx"
    result = processor.process(test_expr)
    print(f"✓ Successfully processed expression: {test_expr}")
    print(f"  Result: {result[:100]}...")
    
except ImportError as e:
    print(f"✗ Import error: {e}")
    
    # Try alternative approach
    print("\nTrying alternative approach...")
    try:
        import mathspeak.core.patterns_v2 as pv2
        print("✓ Successfully imported patterns_v2 module")
        print(f"  Module has: {[x for x in dir(pv2) if not x.startswith('_')][:5]}...")
    except Exception as e2:
        print(f"✗ Alternative also failed: {e2}")

# Test TTS engines
try:
    from mathspeak.core.tts_engines import EdgeTTSEngine
    print("\n✓ Successfully imported EdgeTTSEngine")
    
    # Check if we can create an instance
    engine = EdgeTTSEngine()
    print("✓ Successfully created EdgeTTSEngine instance")
    
except Exception as e:
    print(f"\n✗ TTS engine error: {e}")

# Test voice manager
try:
    from mathspeak.core.voice_manager import VoiceManager, VoiceRole
    print("\n✓ Successfully imported VoiceManager")
    
    vm = VoiceManager()
    print("✓ Successfully created VoiceManager instance")
    print(f"  Available roles: {list(VoiceRole.__members__.keys())}")
    
except Exception as e:
    print(f"\n✗ Voice manager error: {e}")

print("\n" + "="*60)
print("Test completed")