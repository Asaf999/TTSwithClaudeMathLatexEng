#!/usr/bin/env python3
"""
Enhanced Abstract Base Classes for TTS Engines
===============================================

Provides improved abstractions with connection pooling, async support,
and better error handling.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass
from enum import Enum
import time
from contextlib import asynccontextmanager
import weakref

logger = logging.getLogger(__name__)


class EngineStatus(Enum):
    """Engine status enumeration"""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    ERROR = "error"
    BUSY = "busy"


@dataclass
class VoiceProfile:
    """Voice configuration profile"""
    voice_id: str
    language: str
    gender: Optional[str] = None
    age: Optional[str] = None
    rate: str = "+0%"
    pitch: str = "+0%"
    volume: str = "+0%"


@dataclass
class SynthesisRequest:
    """TTS synthesis request"""
    text: str
    output_file: str
    voice_profile: Optional[VoiceProfile] = None
    priority: int = 5  # 1-10, higher is more urgent
    timeout: float = 30.0


@dataclass
class SynthesisResult:
    """TTS synthesis result"""
    success: bool
    output_file: Optional[str] = None
    duration: Optional[float] = None
    error_message: Optional[str] = None
    engine_used: Optional[str] = None


class ConnectionPool:
    """Connection pool for TTS engines"""
    
    def __init__(self, max_connections: int = 5):
        self.max_connections = max_connections
        self.active_connections = 0
        self.connection_queue = asyncio.Queue()
        self._lock = asyncio.Lock()
    
    @asynccontextmanager
    async def acquire(self):
        """Acquire a connection from the pool"""
        async with self._lock:
            if self.active_connections < self.max_connections:
                self.active_connections += 1
                try:
                    yield
                finally:
                    self.active_connections -= 1
            else:
                # Wait for a connection to become available
                await self.connection_queue.get()
                try:
                    yield
                finally:
                    self.connection_queue.task_done()
                    # Signal that a connection is available
                    await self.connection_queue.put(None)


class EnhancedTTSEngine(ABC):
    """Enhanced abstract base class for TTS engines with advanced features"""
    
    def __init__(self, max_connections: int = 5):
        self.connection_pool = ConnectionPool(max_connections)
        self.status = EngineStatus.UNAVAILABLE
        self.last_error: Optional[str] = None
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_duration = 0.0
        self._initialize()
    
    def _initialize(self):
        """Initialize the engine and check availability"""
        try:
            if self.is_available():
                self.status = EngineStatus.AVAILABLE
                logger.info(f"{self.name} engine initialized successfully")
            else:
                self.status = EngineStatus.UNAVAILABLE
                logger.warning(f"{self.name} engine unavailable")
        except Exception as e:
            self.status = EngineStatus.ERROR
            self.last_error = str(e)
            logger.error(f"{self.name} engine initialization failed: {e}")
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get engine name"""
        pass
    
    @property
    @abstractmethod
    def requires_internet(self) -> bool:
        """Check if engine requires internet connection"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this engine is available for use"""
        pass
    
    @abstractmethod
    async def _synthesize_impl(
        self,
        request: SynthesisRequest
    ) -> SynthesisResult:
        """
        Internal synthesis implementation.
        
        This should be implemented by concrete engines and should not
        handle connection pooling or error tracking - that's handled
        by the base class.
        """
        pass
    
    @abstractmethod
    def get_available_voices(self) -> List[VoiceProfile]:
        """Get list of available voice profiles"""
        pass
    
    @abstractmethod
    def get_default_voice(self) -> VoiceProfile:
        """Get default voice profile for this engine"""
        pass
    
    async def synthesize(self, request: SynthesisRequest) -> SynthesisResult:
        """
        Public synthesis method with connection pooling and error handling
        """
        if self.status != EngineStatus.AVAILABLE:
            return SynthesisResult(
                success=False,
                error_message=f"Engine {self.name} is not available: {self.last_error}"
            )
        
        start_time = time.time()
        self.request_count += 1
        
        try:
            async with self.connection_pool.acquire():
                self.status = EngineStatus.BUSY
                try:
                    result = await asyncio.wait_for(
                        self._synthesize_impl(request),
                        timeout=request.timeout
                    )
                    
                    # Update statistics
                    duration = time.time() - start_time
                    self.total_duration += duration
                    result.duration = duration
                    result.engine_used = self.name
                    
                    if result.success:
                        self.success_count += 1
                    else:
                        self.error_count += 1
                        
                    return result
                    
                finally:
                    self.status = EngineStatus.AVAILABLE
                    
        except asyncio.TimeoutError:
            self.error_count += 1
            return SynthesisResult(
                success=False,
                error_message=f"Synthesis timeout after {request.timeout}s"
            )
        except Exception as e:
            self.error_count += 1
            self.last_error = str(e)
            logger.error(f"Synthesis error in {self.name}: {e}")
            return SynthesisResult(
                success=False,
                error_message=str(e)
            )
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get engine performance statistics"""
        success_rate = self.success_count / max(self.request_count, 1)
        avg_duration = self.total_duration / max(self.success_count, 1)
        
        return {
            "name": self.name,
            "status": self.status.value,
            "request_count": self.request_count,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "success_rate": success_rate,
            "average_duration": avg_duration,
            "total_duration": self.total_duration,
            "last_error": self.last_error,
            "requires_internet": self.requires_internet
        }
    
    def reset_statistics(self):
        """Reset performance statistics"""
        self.request_count = 0
        self.success_count = 0
        self.error_count = 0
        self.total_duration = 0.0
        self.last_error = None


class EnhancedTTSManager:
    """Enhanced TTS manager with intelligent engine selection and load balancing"""
    
    def __init__(self):
        self.engines: List[EnhancedTTSEngine] = []
        self.fallback_order: List[str] = []
        self.request_queue = asyncio.PriorityQueue()
        self._is_processing = False
    
    def register_engine(self, engine: EnhancedTTSEngine, fallback_priority: int = 50):
        """Register a TTS engine with fallback priority"""
        self.engines.append(engine)
        # Store with priority for sorting (lower number = higher priority)
        self.fallback_order.append((fallback_priority, engine.name))
        self.fallback_order.sort()
        logger.info(f"Registered engine: {engine.name}")
    
    def get_available_engines(self) -> List[EnhancedTTSEngine]:
        """Get list of currently available engines"""
        return [e for e in self.engines if e.status == EngineStatus.AVAILABLE]
    
    def get_best_engine(
        self,
        prefer_offline: bool = False,
        voice_requirements: Optional[str] = None
    ) -> Optional[EnhancedTTSEngine]:
        """
        Select the best available engine based on criteria
        """
        available = self.get_available_engines()
        if not available:
            return None
        
        # Filter by internet requirement if needed
        if prefer_offline:
            available = [e for e in available if not e.requires_internet]
        
        # Filter by voice requirements if specified
        if voice_requirements:
            compatible = []
            for engine in available:
                voices = engine.get_available_voices()
                if any(voice_requirements.lower() in v.voice_id.lower() for v in voices):
                    compatible.append(engine)
            if compatible:
                available = compatible
        
        # Sort by success rate and average response time
        def engine_score(engine):
            stats = engine.get_statistics()
            success_rate = stats["success_rate"]
            avg_duration = stats["average_duration"]
            # Higher score is better (high success rate, low duration)
            return success_rate - (avg_duration / 10.0)
        
        available.sort(key=engine_score, reverse=True)
        return available[0] if available else None
    
    async def synthesize_with_fallback(
        self,
        request: SynthesisRequest,
        max_attempts: int = 3
    ) -> SynthesisResult:
        """
        Synthesize with automatic fallback to other engines
        """
        last_error = "No engines available"
        
        for priority, engine_name in self.fallback_order[:max_attempts]:
            engine = next((e for e in self.engines if e.name == engine_name), None)
            if not engine or engine.status != EngineStatus.AVAILABLE:
                continue
            
            logger.info(f"Attempting synthesis with {engine_name}")
            result = await engine.synthesize(request)
            
            if result.success:
                return result
            else:
                last_error = result.error_message
                logger.warning(f"Engine {engine_name} failed: {last_error}")
        
        return SynthesisResult(
            success=False,
            error_message=f"All engines failed. Last error: {last_error}"
        )
    
    def get_global_statistics(self) -> Dict[str, Any]:
        """Get statistics for all engines"""
        return {
            "engines": [engine.get_statistics() for engine in self.engines],
            "total_engines": len(self.engines),
            "available_engines": len(self.get_available_engines())
        }