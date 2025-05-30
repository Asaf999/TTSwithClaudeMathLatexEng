"""Unit tests for enhanced base engines."""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from core.base_engines import (
    EnhancedTTSEngine, 
    EnhancedTTSManager, 
    ConnectionPool,
    PooledConnection
)


class TestConnectionPool:
    """Test ConnectionPool functionality."""
    
    @pytest.fixture
    def pool(self):
        """Create a test connection pool."""
        return ConnectionPool(max_connections=3, timeout=1.0)
    
    def test_pool_initialization(self, pool):
        """Test pool is initialized correctly."""
        assert pool.max_connections == 3
        assert pool.timeout == 1.0
        assert len(pool._connections) == 0
        assert len(pool._in_use) == 0
    
    @pytest.mark.asyncio
    async def test_acquire_connection(self, pool):
        """Test acquiring a connection from pool."""
        conn = await pool.acquire()
        assert isinstance(conn, PooledConnection)
        assert len(pool._in_use) == 1
        assert conn in pool._in_use
    
    @pytest.mark.asyncio
    async def test_release_connection(self, pool):
        """Test releasing a connection back to pool."""
        conn = await pool.acquire()
        await pool.release(conn)
        assert len(pool._in_use) == 0
        assert len(pool._connections) == 1
        assert conn in pool._connections
    
    @pytest.mark.asyncio
    async def test_pool_limit(self, pool):
        """Test pool respects max connections limit."""
        connections = []
        for i in range(3):
            conn = await pool.acquire()
            connections.append(conn)
        
        # Pool should be at capacity
        assert len(pool._in_use) == 3
        
        # Trying to acquire should timeout
        with pytest.raises(asyncio.TimeoutError):
            await asyncio.wait_for(pool.acquire(), timeout=0.1)
    
    @pytest.mark.asyncio
    async def test_connection_reuse(self, pool):
        """Test connections are reused from pool."""
        conn1 = await pool.acquire()
        await pool.release(conn1)
        
        conn2 = await pool.acquire()
        assert conn1 is conn2  # Same connection reused


class TestEnhancedTTSEngine:
    """Test EnhancedTTSEngine functionality."""
    
    @pytest.fixture
    def mock_engine(self):
        """Create a mock TTS engine."""
        class MockTTSEngine(EnhancedTTSEngine):
            async def _initialize_connection(self):
                self._initialized = True
                return Mock()
            
            async def _synthesize_speech(self, text: str, voice: str = None) -> bytes:
                return b"mock_audio_data"
            
            async def _cleanup_connection(self, connection):
                pass
        
        return MockTTSEngine(pool_size=2)
    
    @pytest.mark.asyncio
    async def test_engine_initialization(self, mock_engine):
        """Test engine initializes properly."""
        await mock_engine.initialize()
        assert mock_engine._initialized
        assert mock_engine.connection_pool is not None
    
    @pytest.mark.asyncio
    async def test_speech_synthesis(self, mock_engine):
        """Test speech synthesis works."""
        await mock_engine.initialize()
        audio_data = await mock_engine.synthesize_speech("test text")
        assert audio_data == b"mock_audio_data"
        assert mock_engine.stats['total_requests'] == 1
        assert mock_engine.stats['successful_requests'] == 1
    
    @pytest.mark.asyncio
    async def test_error_handling(self, mock_engine):
        """Test error handling and statistics."""
        # Override to raise an exception
        mock_engine._synthesize_speech = AsyncMock(side_effect=Exception("Test error"))
        
        await mock_engine.initialize()
        
        with pytest.raises(Exception):
            await mock_engine.synthesize_speech("test text")
        
        assert mock_engine.stats['total_requests'] == 1
        assert mock_engine.stats['failed_requests'] == 1
    
    @pytest.mark.asyncio
    async def test_cleanup(self, mock_engine):
        """Test cleanup properly closes connections."""
        await mock_engine.initialize()
        await mock_engine.cleanup()
        # Pool should be cleaned up
        assert len(mock_engine.connection_pool._connections) == 0


class TestEnhancedTTSManager:
    """Test EnhancedTTSManager functionality."""
    
    @pytest.fixture
    def mock_manager(self):
        """Create a mock TTS manager."""
        manager = EnhancedTTSManager()
        
        # Create mock engines
        engine1 = Mock()
        engine1.synthesize_speech = AsyncMock(return_value=b"audio1")
        engine1.initialize = AsyncMock()
        engine1.cleanup = AsyncMock()
        engine1.is_available = AsyncMock(return_value=True)
        
        engine2 = Mock()
        engine2.synthesize_speech = AsyncMock(return_value=b"audio2")
        engine2.initialize = AsyncMock()
        engine2.cleanup = AsyncMock()
        engine2.is_available = AsyncMock(return_value=True)
        
        manager.engines = {"engine1": engine1, "engine2": engine2}
        manager.fallback_order = ["engine1", "engine2"]
        
        return manager
    
    @pytest.mark.asyncio
    async def test_manager_initialization(self, mock_manager):
        """Test manager initializes all engines."""
        await mock_manager.initialize()
        
        for engine in mock_manager.engines.values():
            engine.initialize.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_speech_synthesis_primary(self, mock_manager):
        """Test speech synthesis uses primary engine."""
        await mock_manager.initialize()
        
        audio = await mock_manager.synthesize_speech("test text", preferred_engine="engine1")
        assert audio == b"audio1"
        
        mock_manager.engines["engine1"].synthesize_speech.assert_called_once()
        mock_manager.engines["engine2"].synthesize_speech.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_fallback_mechanism(self, mock_manager):
        """Test fallback when primary engine fails."""
        await mock_manager.initialize()
        
        # Make first engine fail
        mock_manager.engines["engine1"].synthesize_speech.side_effect = Exception("Engine failed")
        
        audio = await mock_manager.synthesize_speech("test text", preferred_engine="engine1")
        assert audio == b"audio2"
        
        # Both engines should have been called
        mock_manager.engines["engine1"].synthesize_speech.assert_called_once()
        mock_manager.engines["engine2"].synthesize_speech.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_parallel_processing(self, mock_manager):
        """Test parallel processing of multiple requests."""
        await mock_manager.initialize()
        
        texts = ["text1", "text2", "text3"]
        results = await mock_manager.synthesize_batch(texts)
        
        assert len(results) == 3
        assert all(audio == b"audio1" for audio in results)
    
    @pytest.mark.asyncio
    async def test_cleanup(self, mock_manager):
        """Test cleanup properly closes all engines."""
        await mock_manager.initialize()
        await mock_manager.cleanup()
        
        for engine in mock_manager.engines.values():
            engine.cleanup.assert_called_once()


class TestPooledConnection:
    """Test PooledConnection functionality."""
    
    def test_connection_creation(self):
        """Test connection is created with proper attributes."""
        mock_conn = Mock()
        pooled = PooledConnection(mock_conn, connection_id="test_123")
        
        assert pooled.connection is mock_conn
        assert pooled.connection_id == "test_123"
        assert not pooled.in_use
        assert pooled.created_at is not None
    
    def test_connection_context_manager(self):
        """Test connection works as context manager."""
        mock_conn = Mock()
        pooled = PooledConnection(mock_conn)
        
        with pooled as conn:
            assert conn is mock_conn
            assert pooled.in_use
        
        assert not pooled.in_use
    
    def test_connection_age(self):
        """Test connection age calculation."""
        import time
        mock_conn = Mock()
        pooled = PooledConnection(mock_conn)
        
        time.sleep(0.01)  # Small delay
        age = pooled.age
        assert age > 0
        assert age < 1  # Should be very small