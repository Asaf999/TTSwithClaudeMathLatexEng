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
from mathspeak.utils.user_errors import handle_user_error, format_error

# For audio playback - use our clean audio player
from mathspeak.utils.audio_player import get_audio_player, play_audio

# Version info
__version__ = "1.0.0"
__author__ = "MathSpeak Team"

# Configure logging
logger = logging.getLogger(__name__)

# ===========================
# Audio Player
# ===========================

# Audio player is now imported from utils.audio_player

# ===========================
# Interactive Mode
# ===========================

class InteractiveMode:
    """Interactive REPL for MathSpeak"""
    
    def __init__(self, engine: MathematicalTTSEngine):
        self.engine = engine
        self.player = get_audio_player()
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
        try:
            result = self.engine.process_latex(expr)
        except Exception as e:
            print(format_error(e, verbose=False))
            return
        
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
            self.player.play(temp_file)
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
        
        # Get cache size safely
        if hasattr(self.engine.expression_cache, '__len__'):
            cache_size = len(self.engine.expression_cache)
        elif hasattr(self.engine.expression_cache, 'size'):
            cache_size = self.engine.expression_cache.size
        else:
            cache_size = "unknown"
        
        print(f"  Cache size: {cache_size}/{self.engine.max_cache_size}")
        print(f"  Voice system: {len(list(VoiceRole))} voices available")
    
    def _cmd_stats(self, args: str) -> None:
        """Show performance statistics"""
        report = self.engine.get_performance_report()
        print("\n📊 Performance Statistics:")
        
        # Metrics
        metrics = report.get('metrics', {})
        print(f"  Tokens/second: {metrics.get('tokens_per_second', 0):.1f}")
        print(f"  Cache hit rate: {metrics.get('cache_hit_rate', 0)*100:.1f}%")
        print(f"  Unknown commands: {metrics.get('unknown_commands', 0)}")
        print(f"  Total processing time: {metrics.get('total_time', 0):.2f}s")
        
        # Cache info
        if 'cache' in report:
            cache = report['cache']
            print(f"\n💾 Cache Status:")
            print(f"  Current size: {cache.get('size', 0)}/{cache.get('max_size', 0)}")
            if 'hit_rate' in cache:
                print(f"  Session hit rate: {cache['hit_rate']*100:.1f}%")
        
        # TTS engines
        if hasattr(self.engine, 'tts_manager'):
            print(f"\n🔊 TTS Engines:")
            try:
                engines = self.engine.tts_manager.get_available_engines()
                for eng in engines:
                    status = "✓" if eng['available'] else "✗"
                    print(f"  {status} {eng['name']}")
            except:
                print("  Engine status unavailable")
    
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
        default='',
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
    parser.add_argument(
        '--offline',
        action='store_true',
        help='Prefer offline TTS engines (espeak-ng, pyttsx3)'
    )
    parser.add_argument(
        '--stream',
        action='store_true',
        help='Stream mode - generate and play audio on-the-fly'
    )
    parser.add_argument(
        '--look-ahead',
        type=int,
        default=2,
        help='Lines to process ahead in stream mode (default: 2)'
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
        '--batch',
        type=str,
        metavar='FILE',
        help='Process multiple expressions from a file (one per line)'
    )
    parser.add_argument(
        '--batch-output',
        type=str,
        metavar='DIR',
        default='.',
        help='Output directory for batch processing (default: current directory)'
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
    
    try:
        result = engine.process_latex(expression, force_context=context, show_progress=True)
    except Exception as e:
        # Use user-friendly error formatting
        print(format_error(e, verbose=args.debug))
        return
    
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
        play_audio(output_file)
        # Cleanup temp file
        Path(output_file).unlink(missing_ok=True)
    
    # Show stats if requested
    if args.stats:
        try:
            print("\n📊 Performance Report:")
            report = engine.get_performance_report()
            
            # Pretty print the report
            print("\nMetrics:")
            metrics = report.get('metrics', {})
            for key, value in metrics.items():
                if isinstance(value, float):
                    print(f"  {key}: {value:.2f}")
                else:
                    print(f"  {key}: {value}")
            
            if 'cache' in report:
                print("\nCache:")
                cache_info = report['cache']
                for key, value in cache_info.items():
                    if isinstance(value, float):
                        print(f"  {key}: {value:.2f}")
                    else:
                        print(f"  {key}: {value}")
            
            if 'unknown_commands' in report:
                print("\nUnknown Commands:")
                try:
                    unk = report['unknown_commands']
                    if isinstance(unk, dict):
                        print(f"  Total: {unk.get('total_unknown', 0)}")
                        if unk.get('commands'):
                            commands = unk['commands'][:5] if isinstance(unk.get('commands'), list) else []
                            if commands:
                                print(f"  Commands: {', '.join(commands)}...")
                    else:
                        print(f"  Total: {unk}")
                except Exception as e:
                    print(f"  Error displaying unknown commands: {str(e)}")
                    
        except Exception as e:
            print(f"\n❌ Error generating performance report: {str(e)}")
            print("Core functionality is working, but statistics are unavailable.")

async def process_batch(engine: MathematicalTTSEngine, 
                       batch_file: str, 
                       output_dir: str,
                       args: argparse.Namespace) -> None:
    """Process multiple expressions from a file"""
    from pathlib import Path
    import asyncio
    
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Read expressions from file
    try:
        with open(batch_file, 'r', encoding='utf-8') as f:
            expressions = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"❌ Error reading batch file: {e}")
        return
    
    if not expressions:
        print("❌ No expressions found in batch file")
        return
    
    print(f"\n📦 Processing batch of {len(expressions)} expressions...")
    
    # Progress tracking
    from mathspeak.utils.progress import BatchProgress
    batch_progress = BatchProgress(expressions, "Processing expressions")
    
    async def process_one(idx: int, expr: str) -> Tuple[int, bool, str]:
        """Process a single expression"""
        try:
            # Process
            result = engine.process_latex(expr, show_progress=False)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"mathspeak_{idx+1:04d}_{timestamp}.mp3"
            output_file = output_path / filename
            
            # Generate speech
            success = await engine.speak_expression(
                result, 
                output_file=str(output_file),
                show_progress=False
            )
            
            if success:
                return idx, True, f"✓ {filename}"
            else:
                return idx, False, f"✗ Failed to generate speech"
                
        except Exception as e:
            return idx, False, f"✗ Error: {str(e)[:50]}"
    
    # Process in parallel with limited concurrency
    semaphore = asyncio.Semaphore(3)  # Limit concurrent processing
    
    async def process_with_semaphore(idx: int, expr: str):
        async with semaphore:
            return await process_one(idx, expr)
    
    # Create tasks
    tasks = [
        process_with_semaphore(i, expr) 
        for i, expr in enumerate(expressions)
    ]
    
    # Process with progress
    batch_progress.progress.start()
    results = []
    
    for future in asyncio.as_completed(tasks):
        idx, success, message = await future
        results.append((idx, success, message))
        batch_progress.progress.update()
        
        # Show individual result
        expr_preview = expressions[idx][:50] + "..." if len(expressions[idx]) > 50 else expressions[idx]
        print(f"  [{idx+1}/{len(expressions)}] {message} - {expr_preview}")
    
    batch_progress.progress.finish()
    
    # Summary
    successful = sum(1 for _, success, _ in results if success)
    print(f"\n✅ Batch processing complete!")
    print(f"  Successful: {successful}/{len(expressions)}")
    print(f"  Output directory: {output_path.absolute()}")
    
    # Save batch report
    report_file = output_path / f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("MathSpeak Batch Processing Report\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Date: {datetime.now().isoformat()}\n")
        f.write(f"Total expressions: {len(expressions)}\n")
        f.write(f"Successful: {successful}\n")
        f.write(f"Failed: {len(expressions) - successful}\n\n")
        
        f.write("Results:\n")
        f.write("-" * 50 + "\n")
        for idx, success, message in sorted(results):
            status = "SUCCESS" if success else "FAILED"
            f.write(f"{idx+1:4d}. [{status}] {message}\n")
            f.write(f"      Expression: {expressions[idx][:100]}...\n\n")
    
    print(f"  Report saved: {report_file.name}")

@handle_user_error(verbose_arg='debug')
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
        enable_caching=not args.no_cache,
        prefer_offline_tts=args.offline  # Use offline engines if requested
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
            interactive = InteractiveMode(engine)
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
        
        # Batch mode
        elif args.batch:
            asyncio.run(process_batch(engine, args.batch, args.batch_output, args))
        
        # Streaming mode
        elif args.stream:
            from mathspeak.streaming_mode import StreamingMathSpeak
            streamer = StreamingMathSpeak(
                look_ahead=args.look_ahead,
                prefer_offline=args.offline
            )
            
            try:
                if args.file:
                    # Stream file
                    asyncio.run(streamer.stream_file(args.file))
                elif args.expression:
                    # Stream single expression
                    asyncio.run(streamer.stream_document(args.expression))
                else:
                    # Interactive streaming
                    from mathspeak.streaming_mode import interactive_streaming
                    asyncio.run(interactive_streaming())
            finally:
                streamer.cleanup()
        
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