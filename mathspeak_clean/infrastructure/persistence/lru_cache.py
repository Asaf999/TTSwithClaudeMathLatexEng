"""LRU cache implementation."""

import time
from collections import OrderedDict
from threading import Lock
from typing import Any, Optional

from mathspeak_clean.shared.types import Cache


class LRUCache(Cache):
    """Thread-safe LRU (Least Recently Used) cache implementation.
    
    This cache automatically evicts least recently used items when
    the cache reaches its maximum size.
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 3600) -> None:
        """Initialize LRU cache.
        
        Args:
            max_size: Maximum number of items in cache
            default_ttl: Default time-to-live in seconds
        """
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self._lock = Lock()
        self._hits = 0
        self._misses = 0
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if found and not expired, None otherwise
        """
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None
            
            value, expiry_time = self._cache[key]
            
            # Check if expired
            if expiry_time and time.time() > expiry_time:
                del self._cache[key]
                self._misses += 1
                return None
            
            # Move to end (most recently used)
            self._cache.move_to_end(key)
            self._hits += 1
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds, None for default
        """
        with self._lock:
            # Calculate expiry time
            ttl = ttl or self.default_ttl
            expiry_time = time.time() + ttl if ttl > 0 else None
            
            # Remove oldest item if cache is full
            if key not in self._cache and len(self._cache) >= self.max_size:
                # Remove least recently used item
                self._cache.popitem(last=False)
            
            # Add or update item
            self._cache[key] = (value, expiry_time)
            
            # Move to end (most recently used)
            if key in self._cache:
                self._cache.move_to_end(key)
    
    def delete(self, key: str) -> None:
        """Delete value from cache.
        
        Args:
            key: Cache key
        """
        with self._lock:
            self._cache.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0
    
    def size(self) -> int:
        """Get current cache size.
        
        Returns:
            Number of items in cache
        """
        with self._lock:
            return len(self._cache)
    
    def get_stats(self) -> dict:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        with self._lock:
            total_requests = self._hits + self._misses
            hit_rate = self._hits / total_requests if total_requests > 0 else 0
            
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": hit_rate,
                "total_requests": total_requests,
            }
    
    def evict_expired(self) -> int:
        """Manually evict expired items.
        
        Returns:
            Number of items evicted
        """
        with self._lock:
            current_time = time.time()
            expired_keys = []
            
            for key, (_, expiry_time) in self._cache.items():
                if expiry_time and current_time > expiry_time:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._cache[key]
            
            return len(expired_keys)