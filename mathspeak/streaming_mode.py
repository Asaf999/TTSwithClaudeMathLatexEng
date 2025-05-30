#!/usr/bin/env python3
"""
MathSpeak Streaming Mode
========================

Real-time streaming audio generation for smooth document reading.
Processes lines ahead while playing current audio.
"""

import asyncio
import sys
import re
import time
from pathlib import Path
from typing import List, Optional, Tuple, AsyncIterator
from collections import deque
import threading
from queue import Queue, Empty
import tempfile
import logging

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

# Audio playback
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame not available. Audio preview disabled.")

logger = logging.getLogger(__name__)


class AudioBuffer:
    """Manages audio file buffering and playback"""
    
    def __init__(self, buffer_size: int = 3):
        self.buffer = deque(maxlen=buffer_size)
        self.current_file = None
        self.is_playing = False
        self.lock = threading.Lock()
        
    def add(self, audio_file: str) -> None:
        """Add audio file to buffer"""
        with self.lock:
            self.buffer.append(audio_file)
    
    def get_next(self) -> Optional[str]:
        """Get next audio file to play"""
        with self.lock:
            if self.buffer:
                return self.buffer.popleft()
        return None
    
    def is_empty(self) -> bool:
        """Check if buffer is empty"""
        with self.lock:
            return len(self.buffer) == 0
    
    def clear(self) -> None:
        """Clear the buffer"""
        with self.lock:
            # Clean up files
            for file in self.buffer:
                try:
                    Path(file).unlink(missing_ok=True)
                except:
                    pass
            self.buffer.clear()


class StreamingMathSpeak:
    """Streaming mode for MathSpeak with look-ahead processing"""
    
    def __init__(self, look_ahead: int = 2, prefer_offline: bool = False):
        """
        Initialize streaming mode
        
        Args:
            look_ahead: Number of lines to process ahead
            prefer_offline: Use offline TTS for lower latency
        """
        self.look_ahead = look_ahead
        self.voice_manager = VoiceManager()
        self.engine = MathematicalTTSEngine(
            voice_manager=self.voice_manager,
            enable_caching=True,
            prefer_offline_tts=prefer_offline
        )
        
        # Audio management
        self.audio_buffer = AudioBuffer(buffer_size=look_ahead + 1)
        self.temp_dir = tempfile.mkdtemp(prefix="mathspeak_stream_")
        self.file_counter = 0
        
        # Processing queue
        self.process_queue = asyncio.Queue(maxsize=look_ahead * 2)
        self.is_processing = True
        
        # Playback control
        self.current_channel = None
        self.playback_event = threading.Event()
        
    def split_document(self, content: str) -> List[str]:
        """Split document into processable chunks"""
        # Split by common delimiters
        lines = []
        
        # First split by paragraphs
        paragraphs = content.split('\n\n')
        
        for para in paragraphs:
            if not para.strip():
                continue
                
            # Check if paragraph is too long
            if len(para) > 200:
                # Split by sentences
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sent in sentences:
                    if sent.strip():
                        lines.append(sent.strip())
            else:
                lines.append(para.strip())
        
        # Further split very long lines
        final_lines = []
        for line in lines:
            if len(line) > 300:
                # Split at logical points
                parts = re.split(r'(?<=[,;:])\s+', line)
                current = ""
                for part in parts:
                    if len(current) + len(part) < 250:
                        current += " " + part if current else part
                    else:
                        if current:
                            final_lines.append(current)
                        current = part
                if current:
                    final_lines.append(current)
            else:
                final_lines.append(line)
        
        return final_lines
    
    async def process_line(self, line: str, index: int) -> Optional[str]:
        """Process a single line and generate audio"""
        if not line.strip():
            return None
            
        try:
            # Generate unique filename
            self.file_counter += 1
            audio_file = Path(self.temp_dir) / f"stream_{self.file_counter:04d}.mp3"
            
            # Check for math expressions
            has_math = any(pattern in line for pattern in ['$', '\\', 'frac', 'sum', 'int'])
            
            if has_math:
                # Process as LaTeX
                result = self.engine.process_latex(line)
                success = await self.engine.speak_expression(
                    result, 
                    output_file=str(audio_file)
                )
            else:
                # Process as plain text
                # Use TTS directly for non-math content
                success = await self.engine.tts_manager.synthesize(
                    text=line,
                    output_file=str(audio_file),
                    voice="en-US-AriaNeural",
                    rate="+0%"
                )
            
            if success and audio_file.exists():
                return str(audio_file)
                
        except Exception as e:
            logger.error(f"Error processing line {index}: {e}")
            
        return None
    
    async def process_worker(self):
        """Worker to process lines from queue"""
        while self.is_processing:
            try:
                line, index = await asyncio.wait_for(
                    self.process_queue.get(), 
                    timeout=1.0
                )
                
                # Process line
                audio_file = await self.process_line(line, index)
                
                if audio_file:
                    self.audio_buffer.add(audio_file)
                    print(f"  [Processed line {index + 1}]", end='\r')
                    
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Processing error: {e}")
    
    def play_audio_file(self, audio_file: str) -> None:
        """Play audio file (blocking)"""
        if not PYGAME_AVAILABLE:
            # Fallback to system player
            import subprocess
            try:
                if sys.platform == "darwin":
                    subprocess.run(["afplay", audio_file], check=True)
                elif sys.platform == "linux":
                    subprocess.run(["aplay", audio_file], check=True)
                else:
                    print(f"[Would play: {audio_file}]")
            except:
                pass
            return
            
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Playback error: {e}")
    
    def playback_worker(self):
        """Worker thread for continuous playback"""
        while self.is_processing or not self.audio_buffer.is_empty():
            audio_file = self.audio_buffer.get_next()
            
            if audio_file:
                print(f"\n🔊 Playing: Line {self.file_counter - self.audio_buffer.buffer.__len__()}")
                self.play_audio_file(audio_file)
                
                # Clean up played file
                try:
                    Path(audio_file).unlink()
                except:
                    pass
            else:
                # Wait for more audio
                time.sleep(0.1)
    
    async def stream_document(self, content: str, show_text: bool = True):
        """Stream process and play document"""
        print("🎯 MathSpeak Streaming Mode")
        print("=" * 50)
        print(f"Look-ahead: {self.look_ahead} lines")
        print(f"Offline mode: {self.engine.prefer_offline_tts}")
        print("=" * 50)
        
        # Split document
        lines = self.split_document(content)
        total_lines = len(lines)
        print(f"\n📄 Document has {total_lines} segments to process\n")
        
        # Start processing worker
        process_task = asyncio.create_task(self.process_worker())
        
        # Start playback thread
        playback_thread = threading.Thread(target=self.playback_worker, daemon=True)
        playback_thread.start()
        
        # Feed lines to processor
        for i, line in enumerate(lines):
            if show_text:
                print(f"\n[{i+1}/{total_lines}] {line[:80]}{'...' if len(line) > 80 else ''}")
            
            await self.process_queue.put((line, i))
            
            # Initial buffering
            if i < self.look_ahead:
                print(f"  [Buffering... {i+1}/{self.look_ahead}]")
                await asyncio.sleep(0.1)
        
        # Wait for processing to complete
        await self.process_queue.join()
        self.is_processing = False
        
        # Wait for playback to complete
        print("\n⏳ Waiting for playback to complete...")
        while not self.audio_buffer.is_empty():
            await asyncio.sleep(0.5)
        
        # Cleanup
        await process_task
        
        print("\n✅ Streaming complete!")
    
    async def stream_file(self, file_path: str, show_text: bool = True):
        """Stream process a file"""
        path = Path(file_path)
        if not path.exists():
            print(f"❌ File not found: {file_path}")
            return
            
        print(f"📂 Streaming file: {path.name}")
        
        # Read content
        content = path.read_text(encoding='utf-8')
        
        # Stream process
        await self.stream_document(content, show_text)
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass


async def interactive_streaming():
    """Interactive streaming mode"""
    print("🎤 MathSpeak Interactive Streaming")
    print("Enter text or LaTeX. Type 'quit' to exit.")
    print("Type '---' on a new line to start streaming.\n")
    
    streamer = StreamingMathSpeak(look_ahead=1, prefer_offline=True)
    
    try:
        while True:
            lines = []
            print("📝 Enter content (--- to process):")
            
            while True:
                line = input()
                if line == '---':
                    break
                if line.lower() == 'quit':
                    return
                lines.append(line)
            
            if lines:
                content = '\n'.join(lines)
                await streamer.stream_document(content, show_text=False)
                
    finally:
        streamer.cleanup()


def main():
    """Main entry point for streaming mode"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MathSpeak Streaming Mode - Real-time audio generation"
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='File to stream (optional, interactive if not provided)'
    )
    
    parser.add_argument(
        '--look-ahead',
        type=int,
        default=2,
        help='Number of lines to process ahead (default: 2)'
    )
    
    parser.add_argument(
        '--offline',
        action='store_true',
        help='Use offline TTS for lower latency'
    )
    
    parser.add_argument(
        '--no-text',
        action='store_true',
        help='Don\'t show text while playing'
    )
    
    parser.add_argument(
        '--speed',
        type=float,
        default=1.0,
        help='Speech speed (0.5-2.0)'
    )
    
    args = parser.parse_args()
    
    if args.file:
        # Stream file
        streamer = StreamingMathSpeak(
            look_ahead=args.look_ahead,
            prefer_offline=args.offline
        )
        
        try:
            asyncio.run(streamer.stream_file(
                args.file, 
                show_text=not args.no_text
            ))
        finally:
            streamer.cleanup()
    else:
        # Interactive mode
        asyncio.run(interactive_streaming())


if __name__ == "__main__":
    main()