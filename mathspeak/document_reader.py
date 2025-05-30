#!/usr/bin/env python3
"""
MathSpeak Document Reader
=========================

Advanced document reader with paragraph-by-paragraph streaming,
navigation controls, and smart buffering.
"""

import asyncio
import sys
import os
import re
import time
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import tempfile
import json
from queue import Queue, Empty
import hashlib

# Add mathspeak to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mathspeak.core.engine import MathematicalTTSEngine
from mathspeak.core.voice_manager import VoiceManager

# Try to import keyboard for controls
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Note: Install 'keyboard' package for playback controls")

# Audio playback
try:
    import pygame
    pygame.mixer.init()
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False


@dataclass
class DocumentSection:
    """Represents a section of the document"""
    index: int
    content: str
    has_math: bool
    audio_file: Optional[str] = None
    duration: Optional[float] = None
    processed: bool = False


class DocumentReader:
    """Advanced document reader with navigation"""
    
    def __init__(self, prefer_offline: bool = True):
        self.voice_manager = VoiceManager()
        self.engine = MathematicalTTSEngine(
            voice_manager=self.voice_manager,
            enable_caching=True,
            prefer_offline_tts=prefer_offline
        )
        
        # Document management
        self.sections: List[DocumentSection] = []
        self.current_section = 0
        self.total_sections = 0
        
        # Audio management
        self.temp_dir = tempfile.mkdtemp(prefix="mathspeak_reader_")
        self.audio_cache: Dict[int, str] = {}
        self.is_playing = False
        self.is_paused = False
        
        # Processing
        self.process_queue = asyncio.Queue()
        self.processing_active = True
        
        # Controls
        self.commands = Queue()
        
    def parse_document(self, content: str) -> List[DocumentSection]:
        """Parse document into sections"""
        sections = []
        
        # Split by double newlines (paragraphs)
        paragraphs = re.split(r'\n\s*\n', content)
        
        # Also split by common section markers
        section_patterns = [
            r'^#+\s+',  # Markdown headers
            r'^\\section\{',  # LaTeX sections
            r'^\\subsection\{',
            r'^Chapter\s+\d+',
            r'^Section\s+\d+',
            r'^\d+\.\s+',  # Numbered sections
        ]
        
        current_sections = []
        
        for para in paragraphs:
            if not para.strip():
                continue
                
            # Check if it's a section header
            is_header = any(re.match(pattern, para.strip()) for pattern in section_patterns)
            
            # Check for math content
            has_math = any(indicator in para for indicator in ['$', '\\', 'frac', 'int', 'sum'])
            
            # Split very long paragraphs
            if len(para) > 500 and not is_header:
                # Split at sentence boundaries
                sentences = re.split(r'(?<=[.!?])\s+', para)
                temp_section = ""
                
                for sent in sentences:
                    if len(temp_section) + len(sent) < 400:
                        temp_section += " " + sent if temp_section else sent
                    else:
                        if temp_section:
                            sections.append(DocumentSection(
                                index=len(sections),
                                content=temp_section.strip(),
                                has_math=has_math
                            ))
                        temp_section = sent
                
                if temp_section:
                    sections.append(DocumentSection(
                        index=len(sections),
                        content=temp_section.strip(),
                        has_math=has_math
                    ))
            else:
                sections.append(DocumentSection(
                    index=len(sections),
                    content=para.strip(),
                    has_math=has_math
                ))
        
        return sections
    
    async def process_section(self, section: DocumentSection) -> bool:
        """Process a single section"""
        try:
            # Generate filename
            content_hash = hashlib.md5(section.content.encode()).hexdigest()[:8]
            audio_file = Path(self.temp_dir) / f"section_{section.index:04d}_{content_hash}.mp3"
            
            # Check cache
            if audio_file.exists():
                section.audio_file = str(audio_file)
                section.processed = True
                return True
            
            # Process based on content type
            if section.has_math:
                result = self.engine.process_latex(section.content)
                success = await self.engine.speak_expression(
                    result,
                    output_file=str(audio_file)
                )
            else:
                # Plain text
                success = await self.engine.tts_manager.synthesize(
                    text=section.content,
                    output_file=str(audio_file),
                    voice="en-US-AriaNeural",
                    rate="+0%"
                )
            
            if success and audio_file.exists():
                section.audio_file = str(audio_file)
                section.processed = True
                
                # Estimate duration (rough)
                file_size = audio_file.stat().st_size
                section.duration = file_size / 10000  # Rough estimate
                
                return True
                
        except Exception as e:
            print(f"Error processing section {section.index}: {e}")
            
        return False
    
    async def process_worker(self):
        """Background worker for processing sections"""
        while self.processing_active:
            try:
                # Process current section and look ahead
                start_idx = max(0, self.current_section - 1)
                end_idx = min(len(self.sections), self.current_section + 3)
                
                for i in range(start_idx, end_idx):
                    section = self.sections[i]
                    if not section.processed:
                        await self.process_section(section)
                        self._update_progress()
                
                # Wait a bit before checking again
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"Processing error: {e}")
                await asyncio.sleep(1)
    
    def _update_progress(self):
        """Update progress display"""
        processed = sum(1 for s in self.sections if s.processed)
        total = len(self.sections)
        
        # Progress bar
        bar_width = 30
        filled = int(bar_width * processed / total)
        bar = "█" * filled + "░" * (bar_width - filled)
        
        print(f"\r[{bar}] {processed}/{total} sections ready", end="", flush=True)
    
    def play_section(self, section: DocumentSection):
        """Play a section's audio"""
        if not section.audio_file or not Path(section.audio_file).exists():
            print(f"\n⚠️ Audio not ready for section {section.index}")
            return
            
        self.is_playing = True
        
        # Show section info
        print(f"\n\n📖 Section {section.index + 1}/{len(self.sections)}")
        print("-" * 50)
        
        # Show text preview
        preview = section.content[:150] + "..." if len(section.content) > 150 else section.content
        print(f"📝 {preview}")
        print("-" * 50)
        
        if PYGAME_AVAILABLE:
            pygame.mixer.music.load(section.audio_file)
            pygame.mixer.music.play()
            
            # Wait for completion or interruption
            while pygame.mixer.music.get_busy() and self.is_playing and not self.is_paused:
                time.sleep(0.1)
                
                # Check for commands
                try:
                    cmd = self.commands.get_nowait()
                    self.handle_command(cmd)
                except Empty:
                    pass
        else:
            # Fallback
            print(f"[Playing audio for section {section.index}]")
            time.sleep(2)  # Simulate playback
        
        self.is_playing = False
    
    def handle_command(self, cmd: str):
        """Handle playback commands"""
        if cmd == "pause":
            if PYGAME_AVAILABLE:
                if self.is_paused:
                    pygame.mixer.music.unpause()
                    self.is_paused = False
                    print("\n▶️ Resumed")
                else:
                    pygame.mixer.music.pause()
                    self.is_paused = True
                    print("\n⏸️ Paused")
        
        elif cmd == "next":
            if PYGAME_AVAILABLE:
                pygame.mixer.music.stop()
            self.is_playing = False
            print("\n⏭️ Next section")
        
        elif cmd == "previous":
            if PYGAME_AVAILABLE:
                pygame.mixer.music.stop()
            self.current_section = max(0, self.current_section - 2)
            self.is_playing = False
            print("\n⏮️ Previous section")
        
        elif cmd == "stop":
            if PYGAME_AVAILABLE:
                pygame.mixer.music.stop()
            self.is_playing = False
            self.processing_active = False
            print("\n⏹️ Stopped")
    
    def keyboard_listener(self):
        """Listen for keyboard controls"""
        if not KEYBOARD_AVAILABLE:
            return
            
        print("\n🎮 Controls: Space=Pause/Resume, →=Next, ←=Previous, Esc=Stop")
        
        keyboard.add_hotkey('space', lambda: self.commands.put('pause'))
        keyboard.add_hotkey('right', lambda: self.commands.put('next'))
        keyboard.add_hotkey('left', lambda: self.commands.put('previous'))
        keyboard.add_hotkey('esc', lambda: self.commands.put('stop'))
    
    async def read_document(self, content: str, start_section: int = 0):
        """Read document with streaming audio"""
        print("📚 MathSpeak Document Reader")
        print("=" * 50)
        
        # Parse document
        self.sections = self.parse_document(content)
        self.total_sections = len(self.sections)
        self.current_section = start_section
        
        print(f"📄 Document has {self.total_sections} sections")
        print(f"🔊 Starting from section {start_section + 1}")
        
        # Start background processing
        process_task = asyncio.create_task(self.process_worker())
        
        # Setup keyboard controls
        if KEYBOARD_AVAILABLE:
            self.keyboard_listener()
        
        # Start reading
        while self.current_section < self.total_sections and self.processing_active:
            section = self.sections[self.current_section]
            
            # Wait for section to be ready
            wait_time = 0
            while not section.processed and wait_time < 30:
                print(f"\r⏳ Preparing section {self.current_section + 1}...", end="", flush=True)
                await asyncio.sleep(0.5)
                wait_time += 0.5
            
            if section.processed:
                self.play_section(section)
            else:
                print(f"\n❌ Failed to process section {self.current_section + 1}")
            
            self.current_section += 1
        
        # Cleanup
        self.processing_active = False
        await process_task
        
        print("\n\n✅ Document reading complete!")
        print(f"📊 Read {self.current_section}/{self.total_sections} sections")
    
    async def read_file(self, file_path: str, start_section: int = 0):
        """Read a file"""
        path = Path(file_path)
        if not path.exists():
            print(f"❌ File not found: {file_path}")
            return
            
        print(f"📂 Reading: {path.name}")
        
        content = path.read_text(encoding='utf-8')
        await self.read_document(content, start_section)
    
    def cleanup(self):
        """Clean up resources"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="MathSpeak Document Reader - Smooth document reading experience"
    )
    
    parser.add_argument(
        'file',
        help='Document file to read'
    )
    
    parser.add_argument(
        '--start',
        type=int,
        default=0,
        help='Starting section (default: 0)'
    )
    
    parser.add_argument(
        '--offline',
        action='store_true',
        help='Use offline TTS for lower latency'
    )
    
    parser.add_argument(
        '--no-controls',
        action='store_true',
        help='Disable keyboard controls'
    )
    
    args = parser.parse_args()
    
    # Disable keyboard if requested
    if args.no_controls:
        global KEYBOARD_AVAILABLE
        KEYBOARD_AVAILABLE = False
    
    reader = DocumentReader(prefer_offline=args.offline)
    
    try:
        asyncio.run(reader.read_file(args.file, args.start))
    except KeyboardInterrupt:
        print("\n\n👋 Reading interrupted")
    finally:
        reader.cleanup()


if __name__ == "__main__":
    main()