#!/usr/bin/env python3
"""
Advanced Caching System
=======================

High-performance caching with LRU eviction and statistics.
"""

import time
import hashlib
import pickle
import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Callable
from collections import OrderedDict
from dataclasses import dataclass, field
import logging
from functools import wraps
import threading


logger = logging.getLogger(__name__)


@dataclass
class CacheEntry:
    """A single cache entry with metadata"""
    key: str
    value: Any
    size: int
    hits: int = 0
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)
    computation_time: float = 0.0
    
    def access(self):
        """Record an access to this entry"""
        self.hits += 1
        self.last_accessed = time.time()


class LRUCache:
    """Thread-safe LRU cache with advanced features"""
    
    def __init__(self, max_size: int = 1000, max_memory_mb: int = 100):
        self.max_size = max_size
        self.max_memory_bytes = max_memory_mb * 1024 * 1024
        self.cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self.total_memory = 0
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'total_computation_saved': 0.0
        }
        self.lock = threading.RLock()
    
    def _estimate_size(self, obj: Any) -> int:
        """Estimate memory size of an object"""
        try:
            return len(pickle.dumps(obj))
        except:
            return 1000  # Default estimate
    
    def get(self, key: str) -> Optional[Any]:
        """Get a value from cache"""
        with self.lock:
            if key in self.cache:
                # Move to end (most recently used)
                entry = self.cache.pop(key)
                self.cache[key] = entry
                entry.access()
                
                self.stats['hits'] += 1
                self.stats['total_computation_saved'] += entry.computation_time
                
                logger.debug(f"Cache hit for key: {key[:20]}...")
                return entry.value
            else:
                self.stats['misses'] += 1
                logger.debug(f"Cache miss for key: {key[:20]}...")
                return None
    
    def put(self, key: str, value: Any, computation_time: float = 0.0) -> None:
        """Put a value in cache"""
        with self.lock:
            # Remove if already exists
            if key in self.cache:
                old_entry = self.cache.pop(key)
                self.total_memory -= old_entry.size
            
            # Create new entry
            size = self._estimate_size(value)
            entry = CacheEntry(
                key=key,
                value=value,
                size=size,
                computation_time=computation_time
            )
            
            # Check memory limit
            while self.total_memory + size > self.max_memory_bytes and self.cache:
                self._evict_lru()
            
            # Check size limit
            while len(self.cache) >= self.max_size:
                self._evict_lru()
            
            # Add to cache
            self.cache[key] = entry
            self.total_memory += size
            
            logger.debug(f"Cached key: {key[:20]}... (size: {size} bytes)")
    
    def _evict_lru(self) -> None:
        """Evict least recently used entry"""
        if not self.cache:
            return
        
        # Remove oldest (first item)
        key, entry = self.cache.popitem(last=False)
        self.total_memory -= entry.size
        self.stats['evictions'] += 1
        
        logger.debug(f"Evicted key: {key[:20]}... (freed {entry.size} bytes)")
    
    def clear(self) -> None:
        """Clear the cache"""
        with self.lock:
            self.cache.clear()
            self.total_memory = 0
            logger.info("Cache cleared")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                'size': len(self.cache),
                'memory_mb': self.total_memory / 1024 / 1024,
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'hit_rate': hit_rate,
                'evictions': self.stats['evictions'],
                'computation_time_saved': self.stats['total_computation_saved'],
                'avg_entry_size': self.total_memory / len(self.cache) if self.cache else 0
            }
    
    def __len__(self) -> int:
        """Return the number of items in cache"""
        with self.lock:
            return len(self.cache)
    
    def __contains__(self, key: str) -> bool:
        """Check if key is in cache"""
        with self.lock:
            return key in self.cache
    
    def set(self, key: str, value: Any, computation_time: float = 0.0) -> None:
        """Alias for put() method for compatibility"""
        self.put(key, value, computation_time)
    
    def keys(self):
        """Return cache keys"""
        with self.lock:
            return list(self.cache.keys())
    
    @property
    def size(self) -> int:
        """Property to get cache size"""
        return len(self)
    
    def save_to_disk(self, filepath: Path) -> None:
        """Save cache to disk"""
        with self.lock:
            data = {
                'cache': {k: (v.value, v.computation_time) for k, v in self.cache.items()},
                'stats': self.stats
            }
            
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"Cache saved to {filepath}")
    
    def load_from_disk(self, filepath: Path) -> None:
        """Load cache from disk"""
        if not filepath.exists():
            return
        
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            
            with self.lock:
                self.clear()
                for key, (value, comp_time) in data['cache'].items():
                    self.put(key, value, comp_time)
                
                self.stats.update(data.get('stats', {}))
            
            logger.info(f"Cache loaded from {filepath}")
        except Exception as e:
            logger.error(f"Failed to load cache: {e}")


class ExpressionCache:
    """Specialized cache for mathematical expressions"""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache = LRUCache(max_size=5000, max_memory_mb=200)
        self.cache_dir = cache_dir or Path.home() / '.mathspeak' / 'cache'
        self.cache_file = self.cache_dir / 'expressions.cache'
        
        # Load existing cache
        self.load()
    
    def _make_key(self, expression: str, context: str = "") -> str:
        """Create a cache key from expression and context"""
        combined = f"{expression}|{context}"
        return hashlib.sha256(combined.encode()).hexdigest()
    
    def get(self, expression: str, context: str = "") -> Optional[Any]:
        """Get processed expression from cache"""
        key = self._make_key(expression, context)
        return self.cache.get(key)
    
    def put(self, expression: str, result: Any, context: str = "", 
            computation_time: float = 0.0) -> None:
        """Cache a processed expression"""
        key = self._make_key(expression, context)
        self.cache.put(key, result, computation_time)
    
    def save(self) -> None:
        """Save cache to disk"""
        self.cache.save_to_disk(self.cache_file)
    
    def load(self) -> None:
        """Load cache from disk"""
        self.cache.load_from_disk(self.cache_file)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return self.cache.get_stats()


def cached(cache: LRUCache, key_func: Optional[Callable] = None):
    """Decorator for caching function results"""
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            # Check cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # Compute result
            start_time = time.time()
            result = func(*args, **kwargs)
            computation_time = time.time() - start_time
            
            # Cache result
            cache.put(key, result, computation_time)
            
            return result
        
        return wrapper
    
    return decorator


# Global expression cache instance
_expression_cache = None


def get_expression_cache() -> ExpressionCache:
    """Get the global expression cache"""
    global _expression_cache
    if _expression_cache is None:
        _expression_cache = ExpressionCache()
    return _expression_cache