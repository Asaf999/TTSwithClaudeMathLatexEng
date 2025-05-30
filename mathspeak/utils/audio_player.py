#!/usr/bin/env python3
"""
Audio Player Utilities
======================

Clean audio playback without pygame warnings.
"""

import os
import sys
import subprocess
import platform
import tempfile
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Suppress pygame warnings about AVX2
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

# Try to import pygame quietly
try:
    # Redirect stderr to suppress AVX2 warning
    import io
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()
    
    import pygame
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    # Restore stderr
    sys.stderr = old_stderr
    PYGAME_AVAILABLE = True
except Exception:
    PYGAME_AVAILABLE = False


class AudioPlayer:
    """Cross-platform audio player without warnings"""
    
    def __init__(self):
        self.system = platform.system()
        self.player_command = self._get_system_player()
        
    def _get_system_player(self) -> Optional[str]:
        """Get the best audio player for the system"""
        if self.system == "Darwin":  # macOS
            return "afplay"
        elif self.system == "Linux":
            # Try to find best player
            for player in ["mpv", "aplay", "paplay", "mplayer"]:
                if subprocess.run(["which", player], capture_output=True).returncode == 0:
                    return player
        elif self.system == "Windows":
            return "powershell"
        return None
    
    def play(self, audio_file: str, blocking: bool = True) -> bool:
        """
        Play audio file
        
        Args:
            audio_file: Path to audio file
            blocking: Wait for playback to complete
            
        Returns:
            True if playback started successfully
        """
        if not Path(audio_file).exists():
            logger.error(f"Audio file not found: {audio_file}")
            return False
        
        # Try pygame first (if available and no warnings)
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                if blocking:
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                
                return True
            except Exception as e:
                logger.debug(f"Pygame playback failed: {e}")
        
        # Fallback to system player
        if self.player_command:
            try:
                if self.system == "Windows":
                    # Windows PowerShell command
                    cmd = [
                        "powershell", "-c",
                        f"(New-Object Media.SoundPlayer '{audio_file}').PlaySync()"
                    ]
                else:
                    # Unix-like systems
                    cmd = [self.player_command, audio_file]
                
                if blocking:
                    subprocess.run(cmd, capture_output=True, check=True)
                else:
                    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                return True
                
            except Exception as e:
                logger.error(f"System player failed: {e}")
        
        return False
    
    def stop(self) -> None:
        """Stop current playback"""
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.stop()
            except:
                pass
    
    def pause(self) -> None:
        """Pause current playback"""
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.pause()
            except:
                pass
    
    def resume(self) -> None:
        """Resume paused playback"""
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.unpause()
            except:
                pass
    
    def get_volume(self) -> float:
        """Get current volume (0.0 to 1.0)"""
        if PYGAME_AVAILABLE:
            try:
                return pygame.mixer.music.get_volume()
            except:
                pass
        return 1.0
    
    def set_volume(self, volume: float) -> None:
        """Set volume (0.0 to 1.0)"""
        if PYGAME_AVAILABLE:
            try:
                pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
            except:
                pass


# Global player instance
_player = None


def get_audio_player() -> AudioPlayer:
    """Get the global audio player instance"""
    global _player
    if _player is None:
        _player = AudioPlayer()
    return _player


def play_audio(audio_file: str, blocking: bool = True) -> bool:
    """
    Convenience function to play audio
    
    Args:
        audio_file: Path to audio file
        blocking: Wait for playback to complete
        
    Returns:
        True if playback started successfully
    """
    player = get_audio_player()
    return player.play(audio_file, blocking)