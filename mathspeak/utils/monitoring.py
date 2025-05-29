#!/usr/bin/env python3
"""
Performance Monitoring Utilities
================================

Provides utilities for monitoring system performance and resource usage.
"""

import time
import psutil
import logging
import functools
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


logger = logging.getLogger(__name__)


@dataclass
class PerformanceMetrics:
    """Container for performance metrics"""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    cpu_percent: Optional[float] = None
    memory_mb: Optional[float] = None
    function_name: str = ""
    args_size: int = 0
    result_size: int = 0
    error: Optional[str] = None
    
    @property
    def duration(self) -> float:
        """Calculate duration in seconds"""
        if self.end_time:
            return self.end_time - self.start_time
        return time.time() - self.start_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for logging"""
        return {
            'function': self.function_name,
            'duration_ms': round(self.duration * 1000, 2),
            'cpu_percent': self.cpu_percent,
            'memory_mb': self.memory_mb,
            'args_size': self.args_size,
            'result_size': self.result_size,
            'error': self.error,
            'timestamp': datetime.fromtimestamp(self.start_time).isoformat()
        }


class PerformanceMonitor:
    """Monitor performance metrics for the application"""
    
    def __init__(self, max_history: int = 1000):
        self.max_history = max_history
        self.metrics_history = []
        self.process = psutil.Process()
        
    def record_metric(self, metric: PerformanceMetrics) -> None:
        """Record a performance metric"""
        self.metrics_history.append(metric)
        
        # Keep only recent history
        if len(self.metrics_history) > self.max_history:
            self.metrics_history = self.metrics_history[-self.max_history:]
    
    def get_current_resources(self) -> Dict[str, float]:
        """Get current CPU and memory usage"""
        return {
            'cpu_percent': self.process.cpu_percent(interval=0.1),
            'memory_mb': self.process.memory_info().rss / 1024 / 1024
        }
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        if not self.metrics_history:
            return {'message': 'No metrics recorded'}
        
        durations = [m.duration for m in self.metrics_history if not m.error]
        errors = [m for m in self.metrics_history if m.error]
        
        return {
            'total_operations': len(self.metrics_history),
            'successful_operations': len(durations),
            'failed_operations': len(errors),
            'average_duration_ms': round(sum(durations) / len(durations) * 1000, 2) if durations else 0,
            'min_duration_ms': round(min(durations) * 1000, 2) if durations else 0,
            'max_duration_ms': round(max(durations) * 1000, 2) if durations else 0,
            'current_resources': self.get_current_resources()
        }
    
    def export_metrics(self, filepath: str) -> None:
        """Export metrics to JSON file"""
        data = {
            'summary': self.get_summary(),
            'history': [m.to_dict() for m in self.metrics_history]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


# Global monitor instance
_monitor = PerformanceMonitor()


def monitor_performance(func: Callable) -> Callable:
    """
    Decorator to monitor function performance.
    
    Usage:
        @monitor_performance
        def my_function(arg1, arg2):
            # function body
            return result
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        metric = PerformanceMetrics(function_name=func.__name__)
        
        # Estimate input size
        try:
            metric.args_size = len(str(args)) + len(str(kwargs))
        except:
            metric.args_size = 0
        
        # Get initial resources
        resources = _monitor.get_current_resources()
        metric.cpu_percent = resources['cpu_percent']
        
        try:
            # Execute function
            result = func(*args, **kwargs)
            
            # Estimate output size
            try:
                metric.result_size = len(str(result))
            except:
                metric.result_size = 0
            
            return result
            
        except Exception as e:
            metric.error = str(e)
            raise
            
        finally:
            # Record end time and resources
            metric.end_time = time.time()
            end_resources = _monitor.get_current_resources()
            metric.memory_mb = end_resources['memory_mb']
            
            # Record metric
            _monitor.record_metric(metric)
            
            # Log if slow
            if metric.duration > 1.0:
                logger.warning(f"Slow operation: {metric.function_name} took {metric.duration:.2f}s")
    
    return wrapper


def get_performance_summary() -> Dict[str, Any]:
    """Get global performance summary"""
    return _monitor.get_summary()


def export_performance_metrics(filepath: str) -> None:
    """Export global performance metrics"""
    _monitor.export_metrics(filepath)


class Timer:
    """Context manager for timing code blocks"""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = time.time()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        
        if duration > 0.1:  # Log if takes more than 100ms
            logger.info(f"{self.name} took {duration:.3f}s")
        
        return False
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time"""
        if self.end_time:
            return self.end_time - self.start_time
        elif self.start_time:
            return time.time() - self.start_time
        return 0.0