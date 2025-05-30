#!/usr/bin/env python3
"""
Timeout Utilities
=================

Provides timeout protection for long-running operations.
"""

import signal
import threading
import functools
import asyncio
from typing import TypeVar, Callable, Any, Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError


T = TypeVar('T')


class TimeoutError(Exception):
    """Raised when an operation times out"""
    pass


def timeout(seconds: float) -> Callable:
    """
    Decorator to add timeout to functions.
    Works with both sync and async functions.
    
    Args:
        seconds: Timeout in seconds
        
    Returns:
        Decorated function that will raise TimeoutError if it takes too long
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        if asyncio.iscoroutinefunction(func):
            # Async function
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs) -> T:
                try:
                    return await asyncio.wait_for(
                        func(*args, **kwargs),
                        timeout=seconds
                    )
                except asyncio.TimeoutError:
                    raise TimeoutError(
                        f"{func.__name__} timed out after {seconds} seconds"
                    )
            return async_wrapper
        else:
            # Sync function - use threading
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs) -> T:
                # Use a thread pool to run with timeout
                with ThreadPoolExecutor(max_workers=1) as executor:
                    future = executor.submit(func, *args, **kwargs)
                    try:
                        return future.result(timeout=seconds)
                    except FuturesTimeoutError:
                        # Try to cancel the future
                        future.cancel()
                        raise TimeoutError(
                            f"{func.__name__} timed out after {seconds} seconds"
                        )
            return sync_wrapper
    
    return decorator


class TimeoutContext:
    """Context manager for timeout operations"""
    
    def __init__(self, seconds: float, error_message: str = "Operation timed out"):
        self.seconds = seconds
        self.error_message = error_message
        self._timer = None
        self._timed_out = False
    
    def __enter__(self):
        def timeout_handler():
            self._timed_out = True
            raise TimeoutError(self.error_message)
        
        self._timer = threading.Timer(self.seconds, timeout_handler)
        self._timer.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._timer:
            self._timer.cancel()
        
        # If we timed out, ensure the exception is raised
        if self._timed_out and exc_type is None:
            raise TimeoutError(self.error_message)
        
        return False
    
    @property
    def is_timed_out(self) -> bool:
        """Check if the operation has timed out"""
        return self._timed_out


def with_timeout(func: Callable[..., T], timeout_seconds: float, 
                 *args, **kwargs) -> T:
    """
    Execute a function with timeout.
    
    Args:
        func: Function to execute
        timeout_seconds: Timeout in seconds
        *args: Positional arguments for func
        **kwargs: Keyword arguments for func
        
    Returns:
        Result of func
        
    Raises:
        TimeoutError: If function doesn't complete within timeout
    """
    @timeout(timeout_seconds)
    def wrapper():
        return func(*args, **kwargs)
    
    return wrapper()


class ProcessingTimeout:
    """Manages timeouts for mathematical expression processing"""
    
    # Default timeouts for different operations
    PARSE_TIMEOUT = 5.0          # Parsing LaTeX
    PROCESS_TIMEOUT = 10.0       # Processing expression
    DOMAIN_TIMEOUT = 5.0         # Domain-specific processing
    PATTERN_TIMEOUT = 3.0        # Pattern matching
    TTS_TIMEOUT = 30.0          # Text-to-speech generation
    
    @staticmethod
    def get_timeout(expression_length: int, operation: str = "process") -> float:
        """
        Calculate appropriate timeout based on expression length.
        
        Args:
            expression_length: Length of the expression
            operation: Type of operation
            
        Returns:
            Timeout in seconds
        """
        # Base timeouts
        base_timeouts = {
            'parse': ProcessingTimeout.PARSE_TIMEOUT,
            'process': ProcessingTimeout.PROCESS_TIMEOUT,
            'domain': ProcessingTimeout.DOMAIN_TIMEOUT,
            'pattern': ProcessingTimeout.PATTERN_TIMEOUT,
            'tts': ProcessingTimeout.TTS_TIMEOUT
        }
        
        base = base_timeouts.get(operation, ProcessingTimeout.PROCESS_TIMEOUT)
        
        # Scale with expression length
        # Every 1000 characters adds 1 second
        length_factor = expression_length / 1000
        
        # Minimum 1 second, maximum 60 seconds
        timeout = min(max(base + length_factor, 1.0), 60.0)
        
        return timeout


# Convenience decorators with common timeouts
quick_timeout = timeout(1.0)
standard_timeout = timeout(10.0)
long_timeout = timeout(30.0)