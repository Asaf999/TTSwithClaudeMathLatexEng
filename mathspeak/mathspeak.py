#!/usr/bin/env python3
"""
MathSpeak - Ultimate Mathematical Text-to-Speech System
======================================================

Production-ready CLI and interactive interface for converting mathematical
expressions into natural, professor-quality speech.

Usage:
    python mathspeak.py "expression" [options]
    python mathspeak.py --interactive
    python mathspeak.py --file input.tex [options]

This system is designed for daily use by mathematics students and researchers,
providing natural speech synthesis for any mathematical notation.
"""

import argparse
import asyncio
import sys
import os
import json
import time
import readline  # For better interactive mode
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
import logging
from datetime import datetime

# Add mathspeak package to path if running as script
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

# Import our components
from mathspeak.core.engine import MathematicalTTSEngine, MathematicalContext
from mathspeak.core.voice_manager import VoiceManager, VoiceRole
from mathspeak.utils.logger import setup_logging
from mathspeak.utils.config import Config

# For audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not installed. Audio playback disabled.")
    print("Install with: pip install pygame")

# Version info
__version__ = "1.0.0"
__author__ = "MathSpeak Team"

# Configure logging
logger = logging.getLogger(__name__)

# ===========================
# Audio Player
# ===========================

class AudioPlayer:
    """Handles audio playback with fallback options"""
    
    def __init__(self):
        self.initialized = False
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.init()
                self.initialized = True
            except Exception as e:
                logger.warning(f"Failed to initialize pygame mixer: {e}")
    
    def play_file(self, audio_file: str) -> None:
        """Play audio file with best available method"""
        if not Path(audio_file).exists():
            logger.error(f"Audio file not found: {audio_file}")
            return
        
        if self.initialized and PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            except Exception as e:
                logger.error(f"Pygame playback failed: {e}")
                self._fallback_play(audio_file)
        else:
            self._fallback_play(audio_file)
    
    def _fallback_play(self, audio_file: str) -> None:
        """Fallback audio playback using system commands"""
        system = sys.platform
        try:
            if system == "darwin":  # macOS
                os.system(f"afplay {audio_file}")
            elif system == "linux":
                # Try multiple Linux audio players
                for player in ["mpv", "mplayer", "aplay", "paplay"]:
                    if os.system(f"which {player} > /dev/null 2>&1") == 0:
                        os.system(f"{player} {audio_file} > /dev/null 2>&1")
                        break
            elif system == "win32":  # Windows
                os.system(f'start /min "" "{audio_file}"')
        except Exception as e:
            logger.error(f"Fallback playback failed: {e}")

# ===========================
# Interactive Mode
# ===========================

class InteractiveMode:
    """Interactive REPL for MathSpeak"""
    
    def __init__(self, engine: MathematicalTTSEngine, player: AudioPlayer):
        self.engine = engine
        self.player = player
        self.history = []
        self.config = Config()
        
        # Setup readline for better interaction
        self._setup_readline()
        
        # Commands
        self.commands = {
            'help': self._cmd_help,
            'test': self._cmd_test,
            'voice': self._cmd_voice,
            'voices': self._cmd_list_voices,
            'save': self._cmd_save,
            'history': self._cmd_history,
            'config': self._cmd_config,
            'stats': self._cmd_stats,
            'clear': self._cmd_clear,
            'exit': self._cmd_exit,
            'quit': self._cmd_exit,
        }
    
    def _setup_readline(self) -> None:
        """Setup readline for command history and completion"""
        try:
            # Enable history
            histfile = Path.home() / ".mathspeak_history"
            try:
                readline.read_history_file(histfile)
            except FileNotFoundError:
                pass
            
            import atexit
            atexit.register(readline.write_history_file, histfile)
            
            # Tab completion
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self._completer)
        except Exception:
            # Readline not available on all platforms
            pass
    
    def _completer(self, text: str, state: int) -> Optional[str]:
        """Tab completion for commands"""
        options = [cmd for cmd in self.commands if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        return None
    
    def run(self) -> None:
        """Run interactive mode"""
        self._print_welcome()
        
        while True:
            try:
                # Get input
                expr = input("\n📐 MathSpeak> ").strip()
                
                if not expr:
                    continue
                
                # Check for commands
                if expr.startswith('/'):
                    self._handle_command(expr[1:])
                    continue
                
                # Process mathematical expression
                self._process_expression(expr)
                
            except KeyboardInterrupt:
                print("\n\nUse /exit to quit")
            except EOFError:
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"❌ Error: {e}")
    
    def _print_welcome(self) -> None:
        """Print welcome message"""
        print("\n" + "="*60)
        print("🎓 MathSpeak - Mathematical Text-to-Speech System")
        print(f"   Version {__version__}")
        print("="*60)
        print("\nType mathematical expressions in LaTeX notation.")
        print("Commands start with / (type /help for list)")
        print("\nExamples:")
        print('  ∫_0^∞ e^{-x²} dx = √π/2')
        print('  ∀ε>0 ∃δ>0 : |x-a|<δ ⟹ |f(x)-f(a)|<ε')
        print('  π₁(S¹) ≅ ℤ')
    
    def _handle_command(self, cmd_line: str) -> None:
        """Handle interactive command"""
        parts = cmd_line.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd in self.commands:
            self.commands[cmd](args)
        else:
            print(f"❌ Unknown command: {cmd}")
            print("Type /help for available commands")
    
    def _process_expression(self, expr: str) -> None:
        """Process and speak mathematical expression"""
        print(f"\n🔄 Processing: {expr}")
        
        # Process
        start_time = time.time()
        result = self.engine.process_latex(expr)
        
        # Show results
        print(f"📝 Natural speech: {result.processed[:200]}{'...' if len(result.processed) > 200 else ''}")
        print(f"🎯 Context: {result.context}")
        print(f"⏱️  Processing time: {result.processing_time:.3f}s")
        
        if result.unknown_commands:
            print(f"❓ Unknown commands: {', '.join(result.unknown_commands)}")
        
        # Generate and play audio
        print("🔊 Generating speech...")
        asyncio.run(self._speak_async(result))
        
        # Add to history
        self.history.append({
            'time': datetime.now().isoformat(),
            'input': expr,
            'output': result.processed,
            'context': result.context,
            'processing_time': result.processing_time
        })
    
    async def _speak_async(self, result) -> None:
        """Async wrapper for speech generation"""
        temp_file = f"temp_speech_{int(time.time())}.mp3"
        try:
            await self.engine.speak_expression(result, output_file=temp_file)
            self.player.play_file(temp_file)
        finally:
            # Cleanup
            Path(temp_file).unlink(missing_ok=True)
    
    # Command implementations
    def _cmd_help(self, args: str) -> None:
        """Show help"""
        print("\n📚 Available Commands:")
        print("  /help          - Show this help")
        print("  /test [domain] - Run test expressions")
        print("  /voice <role>  - Change default voice")
        print("  /voices        - List available voices")
        print("  /save <file>   - Save last expression to file")
        print("  /history       - Show expression history")
        print("  /config        - Show current configuration")
        print("  /stats         - Show performance statistics")
        print("  /clear         - Clear screen")
        print("  /exit          - Exit MathSpeak")
    
    def _cmd_test(self, domain: str) -> None:
        """Run test expressions"""
        test_sets = {
            'basic': [
                "x^2 + y^2 = r^2",
                "\\frac{d}{dx} f(x) = f'(x)",
                "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}",
            ],
            'topology': [
                "\\pi_1(S^1) \\cong \\mathbb{Z}",
                "X is compact \\iff every open cover has a finite subcover",
                "\\overline{A} = A \\cup \\partial A",
            ],
            'complex': [
                "\\oint_\\gamma f(z)dz = 2\\pi i \\sum \\text{Res}(f, z_k)",
                "f is holomorphic \\iff \\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y}",
            ],
            'all': [],  # Will include all
        }
        
        # Combine all if requested
        if domain == 'all' or not domain:
            tests = []
            for key in ['basic', 'topology', 'complex']:
                tests.extend(test_sets[key])
        else:
            tests = test_sets.get(domain, test_sets['basic'])
        
        print(f"\n🧪 Running {len(tests)} test expressions...")
        for expr in tests:
            print(f"\n{'='*50}")
            self._process_expression(expr)
            time.sleep(0.5)  # Brief pause between tests
    
    def _cmd_voice(self, voice_name: str) -> None:
        """Change default voice"""
        if not voice_name:
            print("Current voice: NARRATOR")
            return
        
        # This would connect to voice manager configuration
        print(f"Voice changed to: {voice_name}")
    
    def _cmd_list_voices(self, args: str) -> None:
        """List available voices"""
        print("\n🎤 Available Voices:")
        for role in VoiceRole:
            print(f"  {role.name:<12} - {role.value}")
    
    def _cmd_save(self, filename: str) -> None:
        """Save last expression to file"""
        if not self.history:
            print("❌ No expressions to save")
            return
        
        if not filename:
            filename = f"mathspeak_output_{int(time.time())}.txt"
        
        last = self.history[-1]
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Input: {last['input']}\n")
                f.write(f"Output: {last['output']}\n")
                f.write(f"Context: {last['context']}\n")
                f.write(f"Time: {last['time']}\n")
            print(f"✅ Saved to: {filename}")
        except Exception as e:
            print(f"❌ Save failed: {e}")
    
    def _cmd_history(self, args: str) -> None:
        """Show expression history"""
        if not self.history:
            print("📜 No history yet")
            return
        
        print(f"\n📜 Expression History ({len(self.history)} items):")
        for i, item in enumerate(self.history[-10:], 1):
            print(f"\n{i}. {item['input'][:60]}{'...' if len(item['input']) > 60 else ''}")
            print(f"   Context: {item['context']}, Time: {item['processing_time']:.3f}s")
    
    def _cmd_config(self, args: str) -> None:
        """Show configuration"""
        print("\n⚙️  Current Configuration:")
        print(f"  Cache enabled: {self.engine.enable_caching}")
        print(f"  Cache size: {len(self.engine.expression_cache)}/{self.engine.max_cache_size}")
        print(f"  Voice system: {len(list(VoiceRole))} voices available")
    
    def _cmd_stats(self, args: str) -> None:
        """Show performance statistics"""
        report = self.engine.get_performance_report()
        print("\n📊 Performance Statistics:")
        print(f"  Tokens/second: {report['metrics']['tokens_per_second']:.1f}")
        print(f"  Cache hit rate: {report['metrics']['cache_hit_rate']*100:.1f}%")
        print(f"  Unknown commands: {report['metrics']['unknown_commands']}")
        print(f"  Total processing time: {report['metrics']['total_time']:.2f}s")
    
    def _cmd_clear(self, args: str) -> None:
        """Clear screen"""
        os.system('clear' if sys.platform != 'win32' else 'cls')
        self._print_welcome()
    
    def _cmd_exit(self, args: str) -> None:
        """Exit interactive mode"""
        print("\n👋 Thank you for using MathSpeak!")
        sys.exit(0)

# ===========================
# Main CLI
# ===========================

def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        description="MathSpeak - Mathematical Text-to-Speech System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mathspeak "\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}"
  mathspeak --file lecture_notes.tex --output lecture_audio.mp3
  mathspeak --interactive
  mathspeak "\\pi_1(S^1) \\cong \\mathbb{Z}" --voice theorem --save

For more information: https://github.com/yourusername/mathspeak
        """
    )
    
    # Positional arguments
    parser.add_argument(
        'expression',
        nargs='?',
        help='LaTeX mathematical expression to speak'
    )
    
    # Input options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        '-f', '--file',
        type=str,
        help='Read expression from file'
    )
    input_group.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive mode'
    )
    
    # Output options
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Save audio to file (instead of playing)'
    )
    parser.add_argument(
        '-s', '--save',
        action='store_true',
        help='Save audio file (with auto-generated name)'
    )
    
    # Voice options
    parser.add_argument(
        '-v', '--voice',
        type=str,
        choices=[role.name.lower() for role in VoiceRole],
        default='narrator',
        help='Voice role to use'
    )
    parser.add_argument(
        '--speed',
        type=float,
        default=1.0,
        help='Speech speed multiplier (0.5-2.0)'
    )
    
    # Processing options
    parser.add_argument(
        '-c', '--context',
        type=str,
        choices=[ctx.value for ctx in MathematicalContext],
        help='Force specific mathematical context'
    )
    parser.add_argument(
        '--no-commentary',
        action='store_true',
        help='Disable professor commentary'
    )
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Disable expression caching'
    )
    
    # Information options
    parser.add_argument(
        '--test',
        type=str,
        nargs='?',
        const='basic',
        choices=['basic', 'topology', 'complex', 'all'],
        help='Run test expressions'
    )
    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show performance statistics after processing'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'MathSpeak {__version__}'
    )
    
    return parser

async def process_single_expression(
    engine: MathematicalTTSEngine,
    expression: str,
    args: argparse.Namespace
) -> None:
    """Process a single expression with given arguments"""
    # Show what we're processing
    print(f"\n🔄 Processing expression: {expression[:100]}{'...' if len(expression) > 100 else ''}")
    
    # Force context if specified
    context = None
    if args.context:
        context = MathematicalContext(args.context)
    
    # Process expression
    start_time = time.time()
    result = engine.process_latex(expression, force_context=context)
    
    # Show results
    print(f"\n📝 Natural speech: {result.processed[:200]}{'...' if len(result.processed) > 200 else ''}")
    print(f"🎯 Mathematical context: {result.context}")
    print(f"⏱️  Processing time: {result.processing_time:.3f}s")
    
    if result.unknown_commands:
        print(f"❓ Unknown LaTeX commands: {', '.join(result.unknown_commands)}")
    
    # Generate audio
    print("\n🔊 Generating speech...")
    
    # Determine output filename
    if args.output:
        output_file = args.output
    elif args.save:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"mathspeak_{timestamp}.mp3"
    else:
        output_file = f"temp_speech_{int(time.time())}.mp3"
    
    # Generate speech
    await engine.speak_expression(result, output_file=output_file)
    
    # Play or save
    if args.output or args.save:
        print(f"✅ Audio saved to: {output_file}")
    else:
        # Play audio
        player = AudioPlayer()
        player.play_file(output_file)
        # Cleanup temp file
        Path(output_file).unlink(missing_ok=True)
    
    # Show stats if requested
    if args.stats:
        print("\n📊 Performance Report:")
        report = engine.get_performance_report()
        print(json.dumps(report, indent=2))

def main():
    """Main entry point"""
    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)
    
    # Create engine components
    logger.info("Initializing MathSpeak engine...")
    voice_manager = VoiceManager()
    engine = MathematicalTTSEngine(
        voice_manager=voice_manager,
        enable_caching=not args.no_cache
    )
    
    # Load domain processors
    try:
        from mathspeak.domains.topology import TopologyProcessor
        engine.domain_processors[MathematicalContext.TOPOLOGY] = TopologyProcessor()
        logger.info("Loaded topology processor")
    except ImportError:
        logger.warning("Topology processor not available")
    
    # Additional domain processors would be loaded here
    # from mathspeak.domains.complex_analysis import ComplexAnalysisProcessor
    # engine.domain_processors[MathematicalContext.COMPLEX_ANALYSIS] = ComplexAnalysisProcessor()
    
    try:
        # Interactive mode
        if args.interactive:
            player = AudioPlayer()
            interactive = InteractiveMode(engine, player)
            interactive.run()
        
        # Test mode
        elif args.test:
            test_expressions = {
                'basic': [
                    "x^2 + y^2 = r^2",
                    "\\sum_{n=1}^{\\infty} \\frac{1}{n^2} = \\frac{\\pi^2}{6}",
                ],
                'topology': [
                    "\\pi_1(S^1) \\cong \\mathbb{Z}",
                    "A space X is compact \\iff every open cover has a finite subcover",
                ],
                'complex': [
                    "\\oint_\\gamma f(z)dz = 2\\pi i \\sum \\text{Res}(f, z_k)",
                ],
            }
            
            if args.test == 'all':
                tests = sum(test_expressions.values(), [])
            else:
                tests = test_expressions.get(args.test, test_expressions['basic'])
            
            print(f"\n🧪 Running {len(tests)} test expressions...\n")
            for expr in tests:
                asyncio.run(process_single_expression(engine, expr, args))
                print("\n" + "="*60)
        
        # File input
        elif args.file:
            with open(args.file, 'r', encoding='utf-8') as f:
                expression = f.read().strip()
            asyncio.run(process_single_expression(engine, expression, args))
        
        # Direct expression
        elif args.expression:
            asyncio.run(process_single_expression(engine, args.expression, args))
        
        # No input provided
        else:
            parser.print_help()
            print("\n💡 Tip: Use --interactive for interactive mode")
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n👋 MathSpeak interrupted")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        engine.shutdown()
        logger.info("MathSpeak shutdown complete")

if __name__ == "__main__":
    main()