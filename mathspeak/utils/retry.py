#!/usr/bin/env python3
"""
Retry Utilities
==============

Provides retry logic for transient failures.
"""

import asyncio
import functools
import logging
from typing import TypeVar, Callable, Any, Union, Type, Tuple


logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry(
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
) -> Callable:
    """
    Decorator for retrying functions with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        import time
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )
            
            if last_exception:
                raise last_exception
            return None  # Should never reach here
        
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs) -> T:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                            f"Retrying in {current_delay}s..."
                        )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"All {max_attempts} attempts failed for {func.__name__}: {e}"
                        )
            
            if last_exception:
                raise last_exception
            return None  # Should never reach here
        
        # Return appropriate wrapper based on function type
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class RetryableError(Exception):
    """Base class for errors that should trigger a retry"""
    pass


class NonRetryableError(Exception):
    """Base class for errors that should not trigger a retry"""
    pass


def is_retryable_error(error: Exception) -> bool:
    """
    Determine if an error should trigger a retry.
    
    Args:
        error: The exception to check
        
    Returns:
        True if the error is retryable
    """
    # Network-related errors are typically retryable
    retryable_errors = (
        ConnectionError,
        TimeoutError,
        RetryableError,
    )
    
    # Specific error messages that indicate transient issues
    retryable_messages = [
        "connection reset",
        "timeout",
        "temporarily unavailable",
        "rate limit",
    ]
    
    if isinstance(error, retryable_errors):
        return True
    
    error_message = str(error).lower()
    return any(msg in error_message for msg in retryable_messages)


# Convenience decorators with common configurations
retry_on_network_error = retry(
    max_attempts=3,
    delay=1.0,
    backoff=2.0,
    exceptions=(ConnectionError, TimeoutError)
)

retry_on_timeout = retry(
    max_attempts=2,
    delay=0.5,
    backoff=1.5,
    exceptions=(TimeoutError,)
)