#!/usr/bin/env python3
"""
Memory Management Module
Provides memory monitoring, optimization, and cleanup utilities
"""

import gc
import sys
import psutil
import threading
import time
import weakref
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import tracemalloc
from functools import wraps

from .error_handler import error_handler

class MemoryMonitor:
    """Monitor memory usage and provide optimization recommendations"""
    
    def __init__(self, check_interval: int = 60):
        self.check_interval = check_interval
        self.memory_history = []
        self.max_history = 100
        self.monitoring = False
        self.monitor_thread = None
        self.callbacks = []
        self.thresholds = {
            'warning': 80,  # 80% memory usage
            'critical': 90  # 90% memory usage
        }
        
    def start_monitoring(self):
        """Start memory monitoring in background thread"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        error_handler.logger.info("Memory monitoring started")
    
    def stop_monitoring(self):
        """Stop memory monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        error_handler.logger.info("Memory monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                memory_info = self.get_memory_info()
                self._record_memory_usage(memory_info)
                self._check_thresholds(memory_info)
                time.sleep(self.check_interval)
            except Exception as e:
                error_handler.logger.error(f"Memory monitoring error: {e}")
                time.sleep(self.check_interval)
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get current memory information"""
        process = psutil.Process()
        memory_info = process.memory_info()
        
        # System memory
        system_memory = psutil.virtual_memory()
        
        # Python-specific memory
        python_objects = len(gc.get_objects())
        
        return {
            'timestamp': datetime.now().isoformat(),
            'process_memory_mb': memory_info.rss / 1024 / 1024,
            'process_memory_percent': process.memory_percent(),
            'system_memory_percent': system_memory.percent,
            'system_available_mb': system_memory.available / 1024 / 1024,
            'python_objects': python_objects,
            'gc_counts': gc.get_count()
        }
    
    def _record_memory_usage(self, memory_info: Dict[str, Any]):
        """Record memory usage in history"""
        self.memory_history.append(memory_info)
        
        # Keep only recent history
        if len(self.memory_history) > self.max_history:
            self.memory_history = self.memory_history[-self.max_history:]
    
    def _check_thresholds(self, memory_info: Dict[str, Any]):
        """Check memory thresholds and trigger callbacks"""
        memory_percent = memory_info['system_memory_percent']
        
        if memory_percent >= self.thresholds['critical']:
            self._trigger_callbacks('critical', memory_info)
        elif memory_percent >= self.thresholds['warning']:
            self._trigger_callbacks('warning', memory_info)
    
    def _trigger_callbacks(self, level: str, memory_info: Dict[str, Any]):
        """Trigger registered callbacks"""
        for callback in self.callbacks:
            try:
                callback(level, memory_info)
            except Exception as e:
                error_handler.logger.error(f"Memory callback error: {e}")
    
    def add_callback(self, callback: Callable):
        """Add memory threshold callback"""
        self.callbacks.append(callback)
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        if not self.memory_history:
            return {}
        
        recent_memory = [entry['process_memory_mb'] for entry in self.memory_history[-10:]]
        
        return {
            'current': self.get_memory_info(),
            'average_mb': sum(recent_memory) / len(recent_memory),
            'peak_mb': max(recent_memory),
            'trend': self._calculate_trend(),
            'recommendations': self._get_recommendations()
        }
    
    def _calculate_trend(self) -> str:
        """Calculate memory usage trend"""
        if len(self.memory_history) < 5:
            return 'insufficient_data'
        
        recent = [entry['process_memory_mb'] for entry in self.memory_history[-5:]]
        if recent[-1] > recent[0] * 1.1:
            return 'increasing'
        elif recent[-1] < recent[0] * 0.9:
            return 'decreasing'
        else:
            return 'stable'
    
    def _get_recommendations(self) -> List[str]:
        """Get memory optimization recommendations"""
        recommendations = []
        current = self.get_memory_info()
        
        if current['process_memory_percent'] > 50:
            recommendations.append("Consider running garbage collection")
        
        if current['python_objects'] > 100000:
            recommendations.append("High number of Python objects - check for memory leaks")
        
        if self._calculate_trend() == 'increasing':
            recommendations.append("Memory usage is increasing - monitor for leaks")
        
        return recommendations

class ResourceManager:
    """Manage and cleanup resources automatically"""
    
    def __init__(self):
        self.resources = weakref.WeakSet()
        self.cleanup_callbacks = []
        
    def register_resource(self, resource: Any, cleanup_func: Optional[Callable] = None):
        """Register a resource for automatic cleanup"""
        self.resources.add(resource)
        if cleanup_func:
            self.cleanup_callbacks.append((weakref.ref(resource), cleanup_func))
    
    def cleanup_resources(self):
        """Cleanup all registered resources"""
        cleaned = 0
        
        for resource_ref, cleanup_func in self.cleanup_callbacks[:]:
            resource = resource_ref()
            if resource is None:
                # Resource already garbage collected
                self.cleanup_callbacks.remove((resource_ref, cleanup_func))
                continue
            
            try:
                cleanup_func(resource)
                cleaned += 1
            except Exception as e:
                error_handler.logger.warning(f"Resource cleanup failed: {e}")
        
        return cleaned
    
    def force_cleanup(self):
        """Force garbage collection and cleanup"""
        self.cleanup_resources()
        collected = gc.collect()
        error_handler.logger.info(f"Forced cleanup: {collected} objects collected")
        return collected

class MemoryProfiler:
    """Profile memory usage of functions and code blocks"""
    
    def __init__(self):
        self.profiles = {}
        self.tracing = False
    
    def start_tracing(self):
        """Start memory tracing"""
        if not self.tracing:
            tracemalloc.start()
            self.tracing = True
            error_handler.logger.info("Memory tracing started")
    
    def stop_tracing(self):
        """Stop memory tracing"""
        if self.tracing:
            tracemalloc.stop()
            self.tracing = False
            error_handler.logger.info("Memory tracing stopped")
    
    def profile_function(self, func_name: str = None):
        """Decorator to profile function memory usage"""
        def decorator(func):
            name = func_name or f"{func.__module__}.{func.__name__}"
            
            @wraps(func)
            def wrapper(*args, **kwargs):
                if not self.tracing:
                    return func(*args, **kwargs)
                
                # Take snapshot before
                snapshot_before = tracemalloc.take_snapshot()
                
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    # Take snapshot after
                    snapshot_after = tracemalloc.take_snapshot()
                    
                    # Calculate difference
                    top_stats = snapshot_after.compare_to(snapshot_before, 'lineno')
                    total_size = sum(stat.size for stat in top_stats)
                    
                    # Record profile
                    if name not in self.profiles:
                        self.profiles[name] = {
                            'calls': 0,
                            'total_memory': 0,
                            'peak_memory': 0,
                            'avg_memory': 0
                        }
                    
                    profile = self.profiles[name]
                    profile['calls'] += 1
                    profile['total_memory'] += total_size
                    profile['peak_memory'] = max(profile['peak_memory'], total_size)
                    profile['avg_memory'] = profile['total_memory'] / profile['calls']
            
            return wrapper
        return decorator
    
    def get_memory_profile(self) -> Dict[str, Any]:
        """Get memory profiling results"""
        return dict(self.profiles)
    
    def get_top_memory_consumers(self, limit: int = 10) -> List[tuple]:
        """Get functions with highest memory usage"""
        sorted_profiles = sorted(
            self.profiles.items(),
            key=lambda x: x[1]['avg_memory'],
            reverse=True
        )
        return sorted_profiles[:limit]

class MemoryOptimizer:
    """Optimize memory usage through various strategies"""
    
    @staticmethod
    def optimize_data_structures(data: Any) -> Any:
        """Optimize data structures for memory efficiency"""
        if isinstance(data, list):
            # Convert to tuple if immutable
            if all(isinstance(item, (str, int, float, bool, type(None))) for item in data):
                return tuple(data)
        
        elif isinstance(data, dict):
            # Use __slots__ for objects if possible
            # Remove None values
            return {k: v for k, v in data.items() if v is not None}
        
        return data
    
    @staticmethod
    def cleanup_globals():
        """Clean up global variables and modules"""
        # Force garbage collection
        collected = gc.collect()
        
        # Clear module caches
        if hasattr(sys, '_clear_type_cache'):
            sys._clear_type_cache()
        
        return collected
    
    @staticmethod
    def optimize_imports():
        """Optimize module imports"""
        # Remove unused modules (be careful with this)
        initial_modules = set(sys.modules.keys())
        
        # This is a placeholder - in practice, be very careful about removing modules
        # as it can break functionality
        
        return len(initial_modules)

# Global instances
memory_monitor = MemoryMonitor()
resource_manager = ResourceManager()
memory_profiler = MemoryProfiler()

def memory_limit(max_mb: int):
    """Decorator to limit function memory usage"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            initial_memory = psutil.Process().memory_info().rss / 1024 / 1024
            
            try:
                result = func(*args, **kwargs)
                
                final_memory = psutil.Process().memory_info().rss / 1024 / 1024
                memory_used = final_memory - initial_memory
                
                if memory_used > max_mb:
                    error_handler.logger.warning(
                        f"Function {func.__name__} used {memory_used:.1f}MB "
                        f"(limit: {max_mb}MB)"
                    )
                
                return result
            except MemoryError:
                error_handler.logger.error(f"Memory limit exceeded in {func.__name__}")
                raise
        
        return wrapper
    return decorator

def auto_cleanup(cleanup_func: Callable = None):
    """Decorator to automatically cleanup resources after function execution"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                if cleanup_func:
                    cleanup_func()
                else:
                    # Default cleanup
                    gc.collect()
        
        return wrapper
    return decorator

def get_memory_usage() -> Dict[str, float]:
    """Get current memory usage information"""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    return {
        'rss_mb': memory_info.rss / 1024 / 1024,
        'vms_mb': memory_info.vms / 1024 / 1024,
        'percent': process.memory_percent(),
        'available_mb': psutil.virtual_memory().available / 1024 / 1024
    }

def optimize_memory():
    """Run memory optimization procedures"""
    initial_memory = get_memory_usage()
    
    # Cleanup resources
    cleaned_resources = resource_manager.cleanup_resources()
    
    # Force garbage collection
    collected_objects = gc.collect()
    
    # Optimize globals
    MemoryOptimizer.cleanup_globals()
    
    final_memory = get_memory_usage()
    
    return {
        'initial_memory_mb': initial_memory['rss_mb'],
        'final_memory_mb': final_memory['rss_mb'],
        'memory_freed_mb': initial_memory['rss_mb'] - final_memory['rss_mb'],
        'cleaned_resources': cleaned_resources,
        'collected_objects': collected_objects
    }
