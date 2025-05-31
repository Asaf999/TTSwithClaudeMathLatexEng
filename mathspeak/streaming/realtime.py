#!/usr/bin/env python3
"""
Real-time Mathematical Streaming Processor
==========================================

Processes mathematical content in real-time with intelligent chunking,
lookahead buffering, and context preservation.
"""

import asyncio
import re
import time
import logging
from collections import deque
from typing import AsyncIterator, Optional, Dict, List, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ChunkType(Enum):
    """Type of content chunk"""
    TEXT = "text"
    MATH_INLINE = "math_inline"
    MATH_DISPLAY = "math_display"
    MIXED = "mixed"


@dataclass
class ProcessedChunk:
    """A processed chunk of content"""
    type: ChunkType
    original: str
    processed: str
    audio: Optional[bytes] = None
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    

class RealtimeMathProcessor:
    """Process mathematical content in real-time with intelligent chunking"""
    
    def __init__(self, 
                 lookback_sentences: int = 3,
                 lookahead_chars: int = 200,
                 chunk_timeout: float = 0.5,
                 engine = None):
        """
        Initialize real-time processor
        
        Args:
            lookback_sentences: Number of sentences to keep for context
            lookahead_chars: Characters to look ahead for complete expressions
            chunk_timeout: Maximum time to wait for more content
            engine: MathSpeechProcessor instance
        """
        self.lookback = deque(maxlen=lookback_sentences)
        self.lookahead_chars = lookahead_chars
        self.chunk_timeout = chunk_timeout
        self.buffer = ""
        self.math_mode = False
        self.engine = engine
        self.context_memory = {}  # Remember defined symbols
        
        # Regex patterns
        self.math_patterns = {
            'display': re.compile(r'\$\$([^$]+)\$\$'),
            'inline': re.compile(r'\$([^$]+)\$'),
            'latex_inline': re.compile(r'\\\((.+?)\\\)'),
            'latex_display': re.compile(r'\\\[(.+?)\\\]'),
        }
        
        self.sentence_end_pattern = re.compile(r'[.!?]\s+')
        
    async def process_stream(self, 
                           text_stream: AsyncIterator[str]) -> AsyncIterator[ProcessedChunk]:
        """
        Process streaming text input and yield processed chunks
        
        Args:
            text_stream: Async iterator of text chunks
            
        Yields:
            ProcessedChunk objects with text and optional audio
        """
        async for chunk in text_stream:
            self.buffer += chunk
            
            # Process complete sentences or math expressions
            async for result in self._process_buffer():
                yield result
                
        # Process remaining buffer
        if self.buffer:
            async for result in self._process_buffer(force=True):
                yield result
                
    async def _process_buffer(self, force: bool = False) -> AsyncIterator[ProcessedChunk]:
        """Process buffer content when appropriate"""
        
        while True:
            # Check for complete math expression
            math_chunk = self._find_complete_math()
            if math_chunk:
                yield await self._process_math(math_chunk)
                continue
                
            # Check for complete sentence
            sentence = self._find_complete_sentence()
            if sentence or (force and self.buffer):
                text = sentence or self.buffer
                if sentence:
                    self.buffer = self.buffer[len(sentence):]
                else:
                    self.buffer = ""
                    
                if self._contains_math(text):
                    yield await self._process_mixed_content(text)
                else:
                    yield await self._process_text(text)
                    
                if not force:
                    self.lookback.append(text)
                continue
                
            break
            
    def _find_complete_math(self) -> Optional[Tuple[str, str, ChunkType]]:
        """Find complete math expression in buffer"""
        
        # Check display math first (higher priority)
        for pattern_name, pattern in [
            ('display', self.math_patterns['display']),
            ('latex_display', self.math_patterns['latex_display'])
        ]:
            match = pattern.search(self.buffer)
            if match:
                # Check if we might get more content
                if len(self.buffer) < match.end() + self.lookahead_chars:
                    # Look for closing delimiter
                    if ('$$' in self.buffer[match.end():] or 
                        '\\]' in self.buffer[match.end():]):
                        expr = match.group(0)
                        content = match.group(1)
                        self.buffer = self.buffer[match.end():]
                        return (expr, content, ChunkType.MATH_DISPLAY)
                else:
                    expr = match.group(0)
                    content = match.group(1)
                    self.buffer = self.buffer[match.end():]
                    return (expr, content, ChunkType.MATH_DISPLAY)
        
        # Check inline math
        for pattern_name, pattern in [
            ('inline', self.math_patterns['inline']),
            ('latex_inline', self.math_patterns['latex_inline'])
        ]:
            match = pattern.search(self.buffer)
            if match:
                # For inline math, be more aggressive about processing
                expr = match.group(0)
                content = match.group(1)
                self.buffer = self.buffer[match.end():]
                return (expr, content, ChunkType.MATH_INLINE)
                
        return None
        
    def _find_complete_sentence(self) -> Optional[str]:
        """Find complete sentence in buffer"""
        match = self.sentence_end_pattern.search(self.buffer)
        if match:
            sentence = self.buffer[:match.end()].strip()
            return sentence
            
        # Also check for paragraph breaks
        if '\n\n' in self.buffer:
            idx = self.buffer.index('\n\n')
            return self.buffer[:idx].strip()
            
        return None
        
    def _contains_math(self, text: str) -> bool:
        """Check if text contains any math expressions"""
        return any(
            pattern.search(text) 
            for pattern in self.math_patterns.values()
        )
        
    async def _process_math(self, math_data: Tuple[str, str, ChunkType]) -> ProcessedChunk:
        """Process pure math expression"""
        original, content, chunk_type = math_data
        
        # Get context from lookback
        context = ' '.join(self.lookback)
        
        # Update context memory if this defines a symbol
        self._update_context_memory(content)
        
        # Process with engine if available
        if self.engine:
            try:
                from ..core.engine import ProcessedExpression
                result = self.engine.process_latex(content)
                processed_text = result.processed
            except:
                # Fallback processing
                processed_text = self._basic_math_processing(content)
        else:
            processed_text = self._basic_math_processing(content)
            
        # Generate audio if available
        audio = await self._generate_audio(processed_text, voice='narrator')
        
        return ProcessedChunk(
            type=chunk_type,
            original=original,
            processed=processed_text,
            audio=audio,
            context={
                'lookback': list(self.lookback),
                'memory': dict(self.context_memory)
            }
        )
        
    async def _process_text(self, text: str) -> ProcessedChunk:
        """Process plain text"""
        # Update context if this defines something
        self._update_context_memory(text)
        
        # Generate audio if available
        audio = await self._generate_audio(text, voice='narrator')
        
        return ProcessedChunk(
            type=ChunkType.TEXT,
            original=text,
            processed=text,
            audio=audio,
            context={
                'lookback': list(self.lookback),
                'memory': dict(self.context_memory)
            }
        )
        
    async def _process_mixed_content(self, text: str) -> ProcessedChunk:
        """Process text with embedded math"""
        segments = self._split_mixed_content(text)
        
        processed_parts = []
        audio_segments = []
        
        for segment in segments:
            if segment['type'] == 'math':
                # Process math
                if self.engine:
                    try:
                        result = self.engine.process_latex(segment['content'])
                        processed_parts.append(result.processed)
                    except:
                        processed_parts.append(self._basic_math_processing(segment['content']))
                else:
                    processed_parts.append(self._basic_math_processing(segment['content']))
            else:
                # Keep text as is
                processed_parts.append(segment['content'])
                
            # Generate audio for segment
            audio = await self._generate_audio(processed_parts[-1], voice='narrator')
            if audio:
                audio_segments.append(audio)
                
        # Combine everything
        processed_text = ' '.join(processed_parts)
        combined_audio = self._combine_audio(audio_segments) if audio_segments else None
        
        return ProcessedChunk(
            type=ChunkType.MIXED,
            original=text,
            processed=processed_text,
            audio=combined_audio,
            context={
                'lookback': list(self.lookback),
                'memory': dict(self.context_memory)
            }
        )
        
    def _split_mixed_content(self, text: str) -> List[Dict[str, str]]:
        """Split text into math and non-math segments"""
        segments = []
        
        # Combined pattern for all math types
        combined_pattern = r'(\$\$[^$]+\$\$|\$[^$]+\$|\\\([^)]+\\\)|\\\[[^\]]+\\\])'
        
        parts = re.split(combined_pattern, text)
        
        for i, part in enumerate(parts):
            if not part:
                continue
                
            if i % 2 == 0:  # Text segment
                if part.strip():
                    segments.append({'type': 'text', 'content': part})
            else:  # Math segment
                # Extract content without delimiters
                content = part
                if part.startswith('$$') and part.endswith('$$'):
                    content = part[2:-2]
                elif part.startswith('$') and part.endswith('$'):
                    content = part[1:-1]
                elif part.startswith('\\(') and part.endswith('\\)'):
                    content = part[2:-2]
                elif part.startswith('\\[') and part.endswith('\\]'):
                    content = part[2:-2]
                    
                segments.append({'type': 'math', 'content': content})
                
        return segments
        
    def _basic_math_processing(self, latex: str) -> str:
        """Basic math processing without full engine"""
        # Simple replacements for common patterns
        replacements = [
            (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'\1 over \2'),
            (r'\^2', ' squared'),
            (r'\^3', ' cubed'),
            (r'\^{([^}]+)}', r' to the power of \1'),
            (r'_\{([^}]+)\}', r' sub \1'),
            (r'\\sum', 'sum'),
            (r'\\int', 'integral'),
            (r'\\infty', 'infinity'),
            (r'\\pi', 'pi'),
            (r'\\alpha', 'alpha'),
            (r'\\beta', 'beta'),
            (r'\\gamma', 'gamma'),
        ]
        
        result = latex
        for pattern, replacement in replacements:
            result = re.sub(pattern, replacement, result)
            
        return result
        
    def _update_context_memory(self, text: str):
        """Update context memory with defined symbols"""
        # Look for patterns like "let x = ..." or "define y as ..."
        define_patterns = [
            r'[Ll]et\s+(\w+)\s*=',
            r'[Dd]efine\s+(\w+)\s+as',
            r'(\w+)\s+is\s+defined\s+as',
            r'(\w+)\s*:=',
        ]
        
        for pattern in define_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                self.context_memory[match] = True
                
    async def _generate_audio(self, text: str, voice: str = 'narrator') -> Optional[bytes]:
        """Generate audio for text (placeholder)"""
        # In production, this would call the actual TTS engine
        # For now, return None
        await asyncio.sleep(0.01)  # Simulate processing
        return None
        
    def _combine_audio(self, segments: List[bytes]) -> Optional[bytes]:
        """Combine audio segments (placeholder)"""
        if not segments:
            return None
        # In production, this would concatenate audio
        return b''.join(segments)


class LiveMathStreamHandler:
    """Handle live math dictation via WebSocket or other streaming interface"""
    
    def __init__(self, engine = None):
        self.processor = RealtimeMathProcessor(engine=engine)
        self.active_connections = set()
        
    async def handle_text_stream(self, text_stream: AsyncIterator[str]) -> AsyncIterator[Dict[str, Any]]:
        """
        Handle streaming text and yield results
        
        Args:
            text_stream: Async iterator of text chunks
            
        Yields:
            Dict with processed results
        """
        async for chunk in self.processor.process_stream(text_stream):
            yield {
                'type': chunk.type.value,
                'original': chunk.original,
                'text': chunk.processed,
                'audio': chunk.audio,
                'context': chunk.context,
                'timestamp': chunk.timestamp
            }
            
    async def handle_websocket(self, websocket):
        """Handle WebSocket connection for live streaming"""
        self.active_connections.add(websocket)
        
        try:
            async def text_generator():
                while True:
                    message = await websocket.receive_text()
                    if message == "END_STREAM":
                        break
                    yield message
                    
            async for result in self.handle_text_stream(text_generator()):
                await websocket.send_json(result)
                
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            self.active_connections.remove(websocket)
            
            
# Convenience function for testing
async def demo_streaming():
    """Demo streaming functionality"""
    processor = RealtimeMathProcessor()
    
    async def demo_stream():
        """Simulate streaming input"""
        chunks = [
            "The integral ",
            "$\\int_0^\\infty e^{-x^2} dx$ ",
            "equals $\\frac{\\sqrt{\\pi}}{2}$. ",
            "This is known as the Gaussian integral. ",
            "For the general case, $$\\int_{-\\infty}^{\\infty} e^{-ax^2} dx = \\sqrt{\\frac{\\pi}{a}}$$ ",
            "where $a > 0$."
        ]
        
        for chunk in chunks:
            yield chunk
            await asyncio.sleep(0.1)  # Simulate typing delay
            
    print("Streaming demo:")
    print("-" * 50)
    
    async for result in processor.process_stream(demo_stream()):
        print(f"\nChunk type: {result.type.value}")
        print(f"Original: {result.original}")
        print(f"Processed: {result.processed}")
        print(f"Context: {len(result.context.get('lookback', []))} lookback items")


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_streaming())