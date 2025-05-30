#!/usr/bin/env python3
"""
Test TTS Engine Installation
============================

Tests if TTS engines are properly installed and configured
"""

import asyncio
import tempfile
from pathlib import Path
import sys

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mathspeak.core.tts_engines import TTSEngineManager
    TTS_AVAILABLE = True
except ImportError as e:
    print(f"TTS engines not available: {e}")
    TTS_AVAILABLE = False

async def test_tts_engines():
    """Test all available TTS engines"""
    if not TTS_AVAILABLE:
        print("❌ TTS engines not available")
        return False
    
    print("Testing TTS Engine Installation")
    print("=" * 50)
    
    manager = TTSEngineManager()
    engines = manager.get_available_engines()
    
    print(f"\nFound {len(engines)} TTS engines:")
    for engine in engines:
        status = "✓" if engine['available'] else "✗"
        online = "(online)" if engine['requires_internet'] else "(offline)"
        print(f"  {status} {engine['name']} {online}")
    
    # Test speech generation with first available engine
    available_engines = [e for e in engines if e['available']]
    
    if not available_engines:
        print("\n❌ No TTS engines are available!")
        return False
    
    print(f"\nTesting speech generation with {available_engines[0]['name']}...")
    
    try:
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
            success = await manager.synthesize(
                text="The quadratic formula is x equals negative b plus or minus the square root of b squared minus four a c, all over two a",
                output_file=tmp.name,
                voice="en-US-AriaNeural"
            )
            
            if success and Path(tmp.name).exists():
                file_size = Path(tmp.name).stat().st_size
                print(f"✅ Speech generated successfully! ({file_size} bytes)")
                
                # Cleanup
                Path(tmp.name).unlink()
                return True
            else:
                print("❌ Speech generation failed")
                return False
                
    except Exception as e:
        print(f"❌ Error testing speech generation: {e}")
        return False

def main():
    """Run TTS engine tests"""
    if TTS_AVAILABLE:
        result = asyncio.run(test_tts_engines())
        return result
    else:
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 TTS engines are working correctly!")
    else:
        print("\n⚠️ TTS engines need configuration or are not available")
    
    sys.exit(0 if success else 1)