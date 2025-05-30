#!/usr/bin/env python3
"""
Progress Indicators
===================

Provides progress tracking for long-running operations.
"""

import time
import sys
import threading
from typing import Optional, Callable, Any
from contextlib import contextmanager
import logging


logger = logging.getLogger(__name__)


class ProgressIndicator:
    """Simple progress indicator for console output"""
    
    def __init__(self, total: Optional[int] = None, 
                 description: str = "Processing",
                 show_percentage: bool = True,
                 show_time: bool = True):
        self.total = total
        self.description = description
        self.show_percentage = show_percentage and total is not None
        self.show_time = show_time
        self.current = 0
        self.start_time = None
        self._lock = threading.Lock()
        self._stop_flag = False
        self._spinner_thread = None
    
    def start(self):
        """Start the progress indicator"""
        self.start_time = time.time()
        self.current = 0
        self._stop_flag = False
        
        if self.total is None:
            # Start spinner for indeterminate progress
            self._start_spinner()
        else:
            self._update_display()
    
    def _start_spinner(self):
        """Start spinner animation for indeterminate progress"""
        def spinner():
            chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
            idx = 0
            while not self._stop_flag:
                with self._lock:
                    elapsed = time.time() - self.start_time if self.start_time else 0
                    time_str = f" [{elapsed:.1f}s]" if self.show_time else ""
                    sys.stdout.write(f"\r{chars[idx]} {self.description}{time_str}")
                    sys.stdout.flush()
                idx = (idx + 1) % len(chars)
                time.sleep(0.1)
        
        self._spinner_thread = threading.Thread(target=spinner, daemon=True)
        self._spinner_thread.start()
    
    def update(self, amount: int = 1):
        """Update progress by amount"""
        with self._lock:
            self.current = min(self.current + amount, self.total or self.current + amount)
            if self.total is not None:
                self._update_display()
    
    def set_progress(self, current: int):
        """Set absolute progress"""
        with self._lock:
            self.current = min(current, self.total or current)
            if self.total is not None:
                self._update_display()
    
    def _update_display(self):
        """Update the progress display"""
        if self.total is None:
            return
        
        # Calculate percentage
        percentage = (self.current / self.total) * 100 if self.total > 0 else 0
        
        # Calculate elapsed time
        elapsed = time.time() - self.start_time if self.start_time else 0
        
        # Build progress bar
        bar_length = 30
        filled = int(bar_length * self.current / self.total) if self.total > 0 else 0
        bar = '█' * filled + '░' * (bar_length - filled)
        
        # Build display string
        parts = [f"\r{self.description}: [{bar}]"]
        
        if self.show_percentage:
            parts.append(f" {percentage:.1f}%")
        
        if self.show_time:
            parts.append(f" [{elapsed:.1f}s]")
        
        # Estimate remaining time
        if self.current > 0 and percentage < 100:
            rate = self.current / elapsed if elapsed > 0 else 0
            remaining = (self.total - self.current) / rate if rate > 0 else 0
            parts.append(f" ETA: {remaining:.1f}s")
        
        sys.stdout.write(''.join(parts))
        sys.stdout.flush()
    
    def finish(self, message: Optional[str] = None):
        """Finish the progress indicator"""
        self._stop_flag = True
        
        if self._spinner_thread:
            self._spinner_thread.join(timeout=0.5)
        
        with self._lock:
            if message:
                sys.stdout.write(f"\r{message}\n")
            else:
                elapsed = time.time() - self.start_time if self.start_time else 0
                sys.stdout.write(f"\r{self.description}: Complete! [{elapsed:.1f}s]\n")
            sys.stdout.flush()
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is None:
            self.finish()
        else:
            self.finish(f"{self.description}: Failed!")
        return False


class BatchProgress:
    """Progress tracking for batch operations"""
    
    def __init__(self, items: list, description: str = "Processing batch"):
        self.items = items
        self.total = len(items)
        self.description = description
        self.progress = ProgressIndicator(total=self.total, description=description)
        self.results = []
        self.errors = []
    
    def process(self, func: Callable[[Any], Any], 
                show_items: bool = False) -> list:
        """
        Process items with progress tracking.
        
        Args:
            func: Function to apply to each item
            show_items: Whether to show current item in description
            
        Returns:
            List of results
        """
        self.progress.start()
        
        try:
            for i, item in enumerate(self.items):
                if show_items:
                    item_desc = str(item)[:50] + "..." if len(str(item)) > 50 else str(item)
                    self.progress.description = f"{self.description} ({item_desc})"
                
                try:
                    result = func(item)
                    self.results.append(result)
                except Exception as e:
                    logger.error(f"Error processing item {i}: {e}")
                    self.errors.append((i, item, e))
                    self.results.append(None)
                
                self.progress.update()
            
            if self.errors:
                self.progress.finish(
                    f"{self.description}: Complete with {len(self.errors)} errors"
                )
            else:
                self.progress.finish()
            
        except KeyboardInterrupt:
            self.progress.finish(f"{self.description}: Interrupted!")
            raise
        
        return self.results


@contextmanager
def progress_context(description: str = "Processing", 
                    total: Optional[int] = None):
    """
    Context manager for progress indication.
    
    Example:
        with progress_context("Loading data", total=100) as progress:
            for i in range(100):
                # Do work
                progress.update()
    """
    progress = ProgressIndicator(total=total, description=description)
    try:
        yield progress
    finally:
        pass  # Progress handles its own cleanup


class ProgressLogger:
    """Log-based progress tracking for non-interactive environments"""
    
    def __init__(self, total: Optional[int] = None,
                 description: str = "Processing",
                 log_interval: int = 10):
        self.total = total
        self.description = description
        self.log_interval = log_interval
        self.current = 0
        self.start_time = time.time()
        self.last_log_percent = 0
    
    def update(self, amount: int = 1):
        """Update progress"""
        self.current += amount
        
        if self.total:
            percent = int((self.current / self.total) * 100)
            if percent >= self.last_log_percent + self.log_interval:
                elapsed = time.time() - self.start_time
                rate = self.current / elapsed if elapsed > 0 else 0
                remaining = (self.total - self.current) / rate if rate > 0 else 0
                
                logger.info(
                    f"{self.description}: {percent}% "
                    f"({self.current}/{self.total}) "
                    f"[{elapsed:.1f}s elapsed, {remaining:.1f}s remaining]"
                )
                self.last_log_percent = percent
    
    def finish(self):
        """Log completion"""
        elapsed = time.time() - self.start_time
        if self.total:
            logger.info(
                f"{self.description}: Complete! "
                f"({self.total} items in {elapsed:.1f}s, "
                f"{self.total/elapsed:.1f} items/s)"
            )
        else:
            logger.info(
                f"{self.description}: Complete! "
                f"({self.current} items in {elapsed:.1f}s)"
            )


def track_progress(func: Callable) -> Callable:
    """
    Decorator to add progress tracking to functions.
    
    The decorated function should accept a 'progress' keyword argument.
    """
    def wrapper(*args, **kwargs):
        # Check if progress tracking is requested
        show_progress = kwargs.pop('show_progress', False)
        
        if show_progress:
            # Try to determine total from first argument if it's a list
            total = len(args[0]) if args and hasattr(args[0], '__len__') else None
            
            with progress_context(
                description=f"Running {func.__name__}",
                total=total
            ) as progress:
                kwargs['progress'] = progress
                return func(*args, **kwargs)
        else:
            # No progress tracking
            kwargs['progress'] = None
            return func(*args, **kwargs)
    
    return wrapper