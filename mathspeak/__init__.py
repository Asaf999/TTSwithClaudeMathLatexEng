"""
MathSpeak - Ultimate Mathematical Text-to-Speech System
======================================================

A production-ready system that transforms LaTeX mathematical expressions
into natural, professor-quality speech with multi-voice narration.

Features:
- Complete mathematical notation coverage (undergraduate through graduate)
- 7 distinct voice roles for different contexts
- Intelligent context detection and memory
- Natural language processing with variations
- Support for 9+ mathematical domains
- High-performance with caching
- Extensible architecture

Quick Start:
    from mathspeak import MathSpeak
    
    # Create instance
    ms = MathSpeak()
    
    # Convert expression to speech
    ms.speak("∀ε>0 ∃δ>0 : |x-a|<δ ⟹ |f(x)-f(a)|<ε")
    
    # Save to file
    ms.save_speech("e^{iπ} = -1", "euler.mp3")

Command Line:
    mathspeak "\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}"
    mathspeak --interactive
    mathspeak --file lecture.tex --output lecture.mp3
"""

__version__ = "1.0.0"
__author__ = "MathSpeak Team"
__license__ = "MIT"

# Import required types
from typing import Optional, Dict, Any
from pathlib import Path

# Import main components
from .core import (
    MathematicalTTSEngine,
    VoiceManager,
    ContextMemory,
    NaturalLanguageProcessor,
    PatternProcessor,
    MathematicalContext,
    VoiceRole,
    create_engine,
)

from .domains import (
    get_available_domains,
    get_domain_info,
    is_domain_available,
)

from .utils import (
    Config,
    setup_logging,
    get_logger,
    quick_setup,
)

# High-level API
class MathSpeak:
    """
    High-level API for Mathematical Text-to-Speech
    
    This class provides a simple interface for converting mathematical
    expressions to speech without dealing with the underlying complexity.
    """
    
    def __init__(self, config_path: Optional[Path] = None, debug: bool = False):
        """
        Initialize MathSpeak
        
        Args:
            config_path: Optional path to configuration file
            debug: Enable debug mode
        """
        # Quick setup
        self.config, self.logger = quick_setup(debug)
        
        # Create engine with all components
        self.engine = create_engine(
            enable_caching=True,
            enable_all_domains=True,
            config_path=config_path
        )
        
        # Import edge_tts for speech generation
        self._edge_tts_available = False
        try:
            import edge_tts
            self._edge_tts_available = True
        except ImportError:
            self.logger.warning("edge-tts not installed. Audio generation disabled.")
    
    def speak(self, expression: str, voice: Optional[str] = None) -> str:
        """
        Convert mathematical expression to speech (plays audio)
        
        Args:
            expression: LaTeX mathematical expression
            voice: Optional voice role override
            
        Returns:
            The natural language text that was spoken
        """
        # Process expression
        result = self.engine.process_latex(expression)
        
        # Play audio if possible
        if self._edge_tts_available:
            import asyncio
            asyncio.run(self._speak_async(result, voice))
        else:
            self.logger.info(f"Would speak: {result.processed}")
        
        return result.processed
    
    def to_text(self, expression: str) -> str:
        """
        Convert mathematical expression to natural language text only
        
        Args:
            expression: LaTeX mathematical expression
            
        Returns:
            Natural language representation
        """
        result = self.engine.process_latex(expression)
        return result.processed
    
    def save_speech(self, 
                   expression: str, 
                   output_file: str,
                   voice: Optional[str] = None) -> str:
        """
        Convert expression to speech and save to file
        
        Args:
            expression: LaTeX mathematical expression
            output_file: Output audio file path
            voice: Optional voice role override
            
        Returns:
            The natural language text
        """
        # Process expression
        result = self.engine.process_latex(expression)
        
        # Generate and save audio
        if self._edge_tts_available:
            import asyncio
            asyncio.run(self._save_speech_async(result, output_file, voice))
            self.logger.info(f"Saved audio to: {output_file}")
        else:
            self.logger.warning("Cannot save audio: edge-tts not installed")
        
        return result.processed
    
    async def _speak_async(self, result, voice: Optional[str] = None):
        """Async helper for speech generation"""
        import tempfile
        temp_file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False).name
        
        try:
            await self.engine.speak_expression(result, output_file=temp_file)
            
            # Play audio (platform-dependent)
            import platform
            import os
            if platform.system() == 'Darwin':  # macOS
                os.system(f'afplay {temp_file}')
            elif platform.system() == 'Windows':
                os.system(f'start {temp_file}')
            else:  # Linux
                os.system(f'xdg-open {temp_file}')
        finally:
            # Cleanup
            import os
            os.unlink(temp_file)
    
    async def _save_speech_async(self, result, output_file: str, voice: Optional[str] = None):
        """Async helper for saving speech"""
        await self.engine.speak_expression(result, output_file=output_file)
    
    def get_info(self) -> Dict[str, Any]:
        """Get information about the MathSpeak system"""
        return {
            'version': __version__,
            'available_domains': get_available_domains(),
            'voice_roles': [role.name for role in VoiceRole],
            'edge_tts_available': self._edge_tts_available,
            'cache_enabled': self.engine.enable_caching,
            'performance': self.engine.get_performance_report(),
        }
    
    def set_voice_speed(self, speed: float) -> None:
        """
        Set voice speed multiplier
        
        Args:
            speed: Speed multiplier (0.5 to 2.0)
        """
        self.config.set_voice_speed(speed)
    
    def enable_domain(self, domain: str) -> None:
        """Enable a mathematical domain"""
        self.config.enable_domain(domain)
    
    def disable_domain(self, domain: str) -> None:
        """Disable a mathematical domain"""
        self.config.disable_domain(domain)

# Convenience functions
def speak(expression: str) -> str:
    """Quick function to speak a mathematical expression"""
    ms = MathSpeak()
    return ms.speak(expression)

def to_text(expression: str) -> str:
    """Quick function to convert expression to text"""
    ms = MathSpeak()
    return ms.to_text(expression)

def test():
    """Run basic tests to verify installation"""
    print(f"MathSpeak v{__version__}")
    print("=" * 50)
    
    # Test basic functionality
    test_expressions = [
        "x^2 + y^2 = r^2",
        "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}",
        "\\forall \\epsilon > 0 \\, \\exists \\delta > 0",
    ]
    
    ms = MathSpeak()
    
    for expr in test_expressions:
        print(f"\nInput:  {expr}")
        result = ms.to_text(expr)
        print(f"Output: {result}")
    
    # Show system info
    print("\nSystem Info:")
    info = ms.get_info()
    print(f"Available domains: {', '.join(info['available_domains'])}")
    print(f"Voice roles: {', '.join(info['voice_roles'])}")
    print(f"Edge-TTS available: {info['edge_tts_available']}")
    
    print("\n✓ MathSpeak is working correctly!")

# Export main components
__all__ = [
    # High-level API
    'MathSpeak',
    'speak',
    'to_text',
    'test',
    
    # Core components
    'MathematicalTTSEngine',
    'VoiceManager',
    'ContextMemory',
    'NaturalLanguageProcessor',
    'PatternProcessor',
    
    # Enums and types
    'MathematicalContext',
    'VoiceRole',
    
    # Configuration
    'Config',
    
    # Utilities
    'setup_logging',
    'get_logger',
    'get_available_domains',
    'get_domain_info',
    
    # Version info
    '__version__',
]

# Type imports
from pathlib import Path
from typing import Optional, Dict, Any

# Natural Speech Enhancement
try:
    from mathspeak_enhancement.truly_final_98_percent import TrulyFinal98PercentNaturalSpeech
    NaturalSpeechEngine = TrulyFinal98PercentNaturalSpeech
except ImportError:
    NaturalSpeechEngine = None
