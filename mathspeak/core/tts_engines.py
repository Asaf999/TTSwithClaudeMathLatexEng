#!/usr/bin/env python3
"""
Text-to-Speech Engine Abstraction
==================================

Provides multiple TTS engine options with fallback support.
"""

import os
import asyncio
import logging
import subprocess
import tempfile
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from pathlib import Path
import platform

# Try to import various TTS libraries
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False


logger = logging.getLogger(__name__)


class TTSEngine(ABC):
    """Abstract base class for TTS engines"""
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this engine is available"""
        pass
    
    @abstractmethod
    async def synthesize(self, text: str, output_file: str, 
                        voice: Optional[str] = None, 
                        rate: Optional[str] = None) -> bool:
        """
        Synthesize speech from text.
        
        Args:
            text: Text to synthesize
            output_file: Path to save audio file
            voice: Voice to use (engine-specific)
            rate: Speech rate (engine-specific)
            
        Returns:
            True if successful
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get engine name"""
        pass
    
    @property
    @abstractmethod
    def requires_internet(self) -> bool:
        """Check if engine requires internet"""
        pass


class EdgeTTSEngine(TTSEngine):
    """Microsoft Edge TTS engine (online)"""
    
    def is_available(self) -> bool:
        return EDGE_TTS_AVAILABLE
    
    async def synthesize(self, text: str, output_file: str,
                        voice: Optional[str] = None,
                        rate: Optional[str] = None) -> bool:
        """Synthesize using edge-tts"""
        if not self.is_available():
            return False
        
        try:
            voice = voice or "en-US-AriaNeural"
            rate = rate or "+0%"
            
            communicate = edge_tts.Communicate(text, voice, rate=rate)
            await communicate.save(output_file)
            
            logger.info(f"EdgeTTS: Generated {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"EdgeTTS synthesis failed: {e}")
            return False
    
    @property
    def name(self) -> str:
        return "Microsoft Edge TTS"
    
    @property
    def requires_internet(self) -> bool:
        return True


class Pyttsx3Engine(TTSEngine):
    """Pyttsx3 engine (offline)"""
    
    def __init__(self):
        self._engine = None
        self._init_engine()
    
    def _init_engine(self):
        """Initialize pyttsx3 engine"""
        if PYTTSX3_AVAILABLE:
            try:
                self._engine = pyttsx3.init()
                # Set default properties
                self._engine.setProperty('rate', 150)
                self._engine.setProperty('volume', 0.9)
            except Exception as e:
                logger.error(f"Failed to initialize pyttsx3: {e}")
                self._engine = None
    
    def is_available(self) -> bool:
        return PYTTSX3_AVAILABLE and self._engine is not None
    
    async def synthesize(self, text: str, output_file: str,
                        voice: Optional[str] = None,
                        rate: Optional[str] = None) -> bool:
        """Synthesize using pyttsx3"""
        if not self.is_available():
            return False
        
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, self._synthesize_sync, text, output_file, voice, rate
            )
        except Exception as e:
            logger.error(f"Pyttsx3 synthesis failed: {e}")
            return False
    
    def _synthesize_sync(self, text: str, output_file: str,
                        voice: Optional[str] = None,
                        rate: Optional[str] = None) -> bool:
        """Synchronous synthesis"""
        try:
            # Set rate if provided
            if rate:
                # Convert from percentage to words per minute
                base_rate = 150
                if rate.startswith('+'):
                    percent = int(rate[1:-1])
                    wpm = base_rate + (base_rate * percent / 100)
                elif rate.startswith('-'):
                    percent = int(rate[1:-1])
                    wpm = base_rate - (base_rate * percent / 100)
                else:
                    wpm = base_rate
                
                self._engine.setProperty('rate', int(wpm))
            
            # Save to file
            self._engine.save_to_file(text, output_file)
            self._engine.runAndWait()
            
            logger.info(f"Pyttsx3: Generated {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Pyttsx3 sync synthesis failed: {e}")
            return False
    
    @property
    def name(self) -> str:
        return "Pyttsx3 (Offline)"
    
    @property
    def requires_internet(self) -> bool:
        return False


class GTTSEngine(TTSEngine):
    """Google TTS engine (online)"""
    
    def is_available(self) -> bool:
        return GTTS_AVAILABLE
    
    async def synthesize(self, text: str, output_file: str,
                        voice: Optional[str] = None,
                        rate: Optional[str] = None) -> bool:
        """Synthesize using gTTS"""
        if not self.is_available():
            return False
        
        try:
            # Run in thread pool
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                None, self._synthesize_sync, text, output_file, voice, rate
            )
        except Exception as e:
            logger.error(f"gTTS synthesis failed: {e}")
            return False
    
    def _synthesize_sync(self, text: str, output_file: str,
                        voice: Optional[str] = None,
                        rate: Optional[str] = None) -> bool:
        """Synchronous synthesis"""
        try:
            # gTTS doesn't support rate adjustment directly
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(output_file)
            
            logger.info(f"gTTS: Generated {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"gTTS sync synthesis failed: {e}")
            return False
    
    @property
    def name(self) -> str:
        return "Google TTS"
    
    @property
    def requires_internet(self) -> bool:
        return True


class EspeakEngine(TTSEngine):
    """Espeak engine (offline, Linux/Mac)"""
    
    def is_available(self) -> bool:
        """Check if espeak is installed"""
        try:
            result = subprocess.run(['which', 'espeak'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    async def synthesize(self, text: str, output_file: str,
                        voice: Optional[str] = None,
                        rate: Optional[str] = None) -> bool:
        """Synthesize using espeak"""
        if not self.is_available():
            return False
        
        try:
            # Build command
            cmd = ['espeak']
            
            # Add voice if specified
            if voice:
                cmd.extend(['-v', voice])
            else:
                cmd.extend(['-v', 'en'])
            
            # Add rate if specified
            if rate:
                # Convert percentage to words per minute
                base_rate = 175
                if rate.startswith('+'):
                    percent = int(rate[1:-1])
                    wpm = base_rate + (base_rate * percent / 100)
                elif rate.startswith('-'):
                    percent = int(rate[1:-1])
                    wpm = base_rate - (base_rate * percent / 100)
                else:
                    wpm = base_rate
                
                cmd.extend(['-s', str(int(wpm))])
            
            # Add output file and text
            cmd.extend(['-w', output_file, text])
            
            # Run command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"Espeak: Generated {output_file}")
                return True
            else:
                logger.error(f"Espeak failed with return code {process.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"Espeak synthesis failed: {e}")
            return False
    
    @property
    def name(self) -> str:
        return "Espeak (Offline)"
    
    @property
    def requires_internet(self) -> bool:
        return False


class TTSEngineManager:
    """Manages multiple TTS engines with fallback"""
    
    def __init__(self, prefer_offline: bool = False):
        self.prefer_offline = prefer_offline
        self.engines: List[TTSEngine] = []
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize all available engines"""
        # Order based on preference
        if self.prefer_offline:
            # Offline engines first
            self.engines = [
                Pyttsx3Engine(),
                EspeakEngine(),
                EdgeTTSEngine(),
                GTTSEngine(),
            ]
        else:
            # Online engines first (better quality)
            self.engines = [
                EdgeTTSEngine(),
                GTTSEngine(),
                Pyttsx3Engine(),
                EspeakEngine(),
            ]
        
        # Log available engines
        available = [e for e in self.engines if e.is_available()]
        logger.info(f"Available TTS engines: {[e.name for e in available]}")
        
        if not available:
            logger.warning("No TTS engines available!")
    
    async def synthesize(self, text: str, output_file: str,
                        voice: Optional[str] = None,
                        rate: Optional[str] = None,
                        engine_name: Optional[str] = None) -> bool:
        """
        Synthesize speech using available engines.
        
        Args:
            text: Text to synthesize
            output_file: Output file path
            voice: Voice to use
            rate: Speech rate
            engine_name: Specific engine to use
            
        Returns:
            True if successful
        """
        # If specific engine requested
        if engine_name:
            for engine in self.engines:
                if engine.name.lower() == engine_name.lower() and engine.is_available():
                    return await engine.synthesize(text, output_file, voice, rate)
            logger.error(f"Requested engine '{engine_name}' not available")
        
        # Try each engine in order
        for engine in self.engines:
            if engine.is_available():
                logger.info(f"Trying {engine.name}...")
                try:
                    success = await engine.synthesize(text, output_file, voice, rate)
                    if success and Path(output_file).exists():
                        logger.info(f"Successfully generated speech with {engine.name}")
                        return True
                except Exception as e:
                    logger.error(f"{engine.name} failed: {e}")
                    continue
        
        logger.error("All TTS engines failed")
        return False
    
    async def generate_speech(self, text: str, output_file: str,
                             voice: Optional[str] = None,
                             rate: Optional[str] = None,
                             engine_name: Optional[str] = None) -> bool:
        """
        Generate speech from text (alias for synthesize for backward compatibility).
        
        Args:
            text: Text to convert to speech
            output_file: Path where audio file should be saved
            voice: Voice to use (engine-specific)
            rate: Speech rate (engine-specific)
            engine_name: Specific engine to use
            
        Returns:
            True if successful, False otherwise
        """
        return await self.synthesize(text, output_file, voice, rate, engine_name)
    
    async def generate_speech_batch(self, 
                                   texts: List[str], 
                                   output_files: List[str],
                                   voice: Optional[str] = None,
                                   rate: Optional[str] = None,
                                   engine_name: Optional[str] = None,
                                   max_concurrent: int = 3) -> List[bool]:
        """
        Generate speech for multiple texts concurrently.
        
        Args:
            texts: List of texts to convert to speech
            output_files: List of output file paths
            voice: Voice to use for all texts
            rate: Speech rate for all texts
            engine_name: Specific engine to use
            max_concurrent: Maximum concurrent operations
            
        Returns:
            List of success flags for each text
        """
        if len(texts) != len(output_files):
            raise ValueError("texts and output_files must have the same length")
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def process_single(text: str, output_file: str) -> bool:
            async with semaphore:
                return await self.generate_speech(text, output_file, voice, rate, engine_name)
        
        tasks = [process_single(text, output_file) 
                for text, output_file in zip(texts, output_files)]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to False
        processed_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Error in batch processing: {result}")
                processed_results.append(False)
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_available_engines(self) -> List[Dict[str, Any]]:
        """Get information about available engines"""
        return [
            {
                'name': engine.name,
                'available': engine.is_available(),
                'requires_internet': engine.requires_internet
            }
            for engine in self.engines
        ]
    
    def has_offline_engine(self) -> bool:
        """Check if any offline engine is available"""
        return any(
            e.is_available() and not e.requires_internet 
            for e in self.engines
        )


# Install offline TTS engines if needed
def install_offline_tts():
    """Install offline TTS engines"""
    print("Installing offline TTS engines...")
    
    # Install pyttsx3
    if not PYTTSX3_AVAILABLE:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyttsx3'],
                         check=True)
            print("✅ Installed pyttsx3")
        except:
            print("❌ Failed to install pyttsx3")
    
    # Check for espeak
    if platform.system() in ['Linux', 'Darwin']:
        if subprocess.run(['which', 'espeak'], capture_output=True).returncode != 0:
            print("ℹ️  To install espeak:")
            if platform.system() == 'Linux':
                print("   sudo apt-get install espeak")
            else:
                print("   brew install espeak")
    
    print("Done!")