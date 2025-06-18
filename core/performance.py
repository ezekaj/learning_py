#!/usr/bin/env python3
"""
Performance Optimization Module
Provides caching, profiling, and optimization utilities
"""

import time
import functools
import threading
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, Callable
import hashlib
import pickle
from pathlib import Path

from .error_handler import error_handler

class MemoryCache:
    """Thread-safe in-memory cache with TTL support"""
    
    def __init__(self, default_ttl: int = 3600, max_size: int = 1000):
        self.cache = {}
        self.timestamps = {}
        self.access_times = {}
        self.default_ttl = default_ttl
        self.max_size = max_size
        self._lock = threading.RLock()
    
    def _is_expired(self, key: str) -> bool:
        """Check if cache entry is expired"""
        if key not in self.timestamps:
            return True
        
        expiry_time = self.timestamps[key] + timedelta(seconds=self.default_ttl)
        return datetime.now() > expiry_time
    
    def _cleanup_expired(self):
        """Remove expired entries"""
        current_time = datetime.now()
        expired_keys = []
        
        for key, timestamp in self.timestamps.items():
            expiry_time = timestamp + timedelta(seconds=self.default_ttl)
            if current_time > expiry_time:
                expired_keys.append(key)
        
        for key in expired_keys:
            self._remove_key(key)
    
    def _remove_key(self, key: str):
        """Remove a key from all cache structures"""
        self.cache.pop(key, None)
        self.timestamps.pop(key, None)
        self.access_times.pop(key, None)
    
    def _evict_lru(self):
        """Evict least recently used items if cache is full"""
        if len(self.cache) >= self.max_size:
            # Find least recently used key
            lru_key = min(self.access_times.keys(), key=lambda k: self.access_times[k])
            self._remove_key(lru_key)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self._lock:
            if key not in self.cache or self._is_expired(key):
                return None
            
            # Update access time
            self.access_times[key] = datetime.now()
            return self.cache[key]
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        with self._lock:
            # Cleanup expired entries periodically
            if len(self.cache) % 100 == 0:
                self._cleanup_expired()
            
            # Evict LRU if necessary
            self._evict_lru()
            
            # Set new value
            self.cache[key] = value
            self.timestamps[key] = datetime.now()
            self.access_times[key] = datetime.now()
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        with self._lock:
            if key in self.cache:
                self._remove_key(key)
                return True
            return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            self.cache.clear()
            self.timestamps.clear()
            self.access_times.clear()
    
    def stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self._lock:
            return {
                "size": len(self.cache),
                "max_size": self.max_size,
                "hit_ratio": getattr(self, '_hit_count', 0) / max(getattr(self, '_total_requests', 1), 1)
            }

class FileCache:
    """Persistent file-based cache"""
    
    def __init__(self, cache_dir: str = "data/cache", default_ttl: int = 3600):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = default_ttl
        self._lock = threading.RLock()
    
    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for key"""
        # Create safe filename from key
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{safe_key}.cache"
    
    def _is_expired(self, cache_path: Path) -> bool:
        """Check if cache file is expired"""
        if not cache_path.exists():
            return True
        
        file_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
        expiry_time = file_time + timedelta(seconds=self.default_ttl)
        return datetime.now() > expiry_time
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from file cache"""
        with self._lock:
            cache_path = self._get_cache_path(key)
            
            if not cache_path.exists() or self._is_expired(cache_path):
                return None
            
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                error_handler.logger.warning(f"Failed to read cache file {cache_path}: {e}")
                return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in file cache"""
        with self._lock:
            cache_path = self._get_cache_path(key)
            
            try:
                with open(cache_path, 'wb') as f:
                    pickle.dump(value, f)
            except Exception as e:
                error_handler.logger.warning(f"Failed to write cache file {cache_path}: {e}")
    
    def delete(self, key: str) -> bool:
        """Delete key from file cache"""
        with self._lock:
            cache_path = self._get_cache_path(key)
            
            if cache_path.exists():
                try:
                    cache_path.unlink()
                    return True
                except Exception as e:
                    error_handler.logger.warning(f"Failed to delete cache file {cache_path}: {e}")
            
            return False
    
    def cleanup_expired(self) -> int:
        """Clean up expired cache files"""
        with self._lock:
            cleaned = 0
            
            for cache_file in self.cache_dir.glob("*.cache"):
                if self._is_expired(cache_file):
                    try:
                        cache_file.unlink()
                        cleaned += 1
                    except Exception as e:
                        error_handler.logger.warning(f"Failed to delete expired cache file {cache_file}: {e}")
            
            return cleaned

class PerformanceProfiler:
    """Performance profiling utilities"""
    
    def __init__(self):
        self.profiles = {}
        self._lock = threading.RLock()
    
    def profile_function(self, func_name: str = None):
        """Decorator to profile function execution time"""
        def decorator(func):
            name = func_name or f"{func.__module__}.{func.__name__}"
            
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    return result
                finally:
                    duration = time.time() - start_time
                    self._record_execution(name, duration)
            
            return wrapper
        return decorator
    
    def _record_execution(self, func_name: str, duration: float):
        """Record function execution time"""
        with self._lock:
            if func_name not in self.profiles:
                self.profiles[func_name] = {
                    "total_calls": 0,
                    "total_time": 0.0,
                    "min_time": float('inf'),
                    "max_time": 0.0,
                    "avg_time": 0.0
                }
            
            profile = self.profiles[func_name]
            profile["total_calls"] += 1
            profile["total_time"] += duration
            profile["min_time"] = min(profile["min_time"], duration)
            profile["max_time"] = max(profile["max_time"], duration)
            profile["avg_time"] = profile["total_time"] / profile["total_calls"]
    
    def get_profile_report(self) -> Dict[str, Any]:
        """Get performance profile report"""
        with self._lock:
            return dict(self.profiles)
    
    def get_slowest_functions(self, limit: int = 10) -> list:
        """Get slowest functions by average execution time"""
        with self._lock:
            sorted_profiles = sorted(
                self.profiles.items(),
                key=lambda x: x[1]["avg_time"],
                reverse=True
            )
            return sorted_profiles[:limit]

# Global instances
memory_cache = MemoryCache()
file_cache = FileCache()
profiler = PerformanceProfiler()

def cached(ttl: int = 3600, use_file_cache: bool = False):
    """Decorator for caching function results"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key_data = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"
            cache_key = hashlib.md5(key_data.encode()).hexdigest()
            
            # Try to get from cache
            cache_instance = file_cache if use_file_cache else memory_cache
            cached_result = cache_instance.get(cache_key)
            
            if cached_result is not None:
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_instance.set(cache_key, result)
            
            return result
        
        return wrapper
    return decorator

def optimize_json_loading(file_path: str) -> Optional[Dict]:
    """Optimized JSON file loading with caching"""
    @cached(ttl=1800, use_file_cache=True)  # 30 minutes cache
    def _load_json_cached(path: str, mtime: float):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            error_handler.logger.error(f"Failed to load JSON file {path}: {e}")
            return None
    
    if not os.path.exists(file_path):
        return None
    
    # Include file modification time in cache key to invalidate on changes
    mtime = os.path.getmtime(file_path)
    return _load_json_cached(file_path, mtime)

def batch_process(items: list, batch_size: int = 100, processor_func: Callable = None):
    """Process items in batches for better performance"""
    if not processor_func:
        return items
    
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        batch_results = processor_func(batch)
        results.extend(batch_results)
    
    return results

def lazy_load_data(data_loader: Callable, cache_key: str = None):
    """Lazy loading with caching"""
    if cache_key:
        cached_data = memory_cache.get(cache_key)
        if cached_data is not None:
            return cached_data
    
    data = data_loader()
    
    if cache_key:
        memory_cache.set(cache_key, data)
    
    return data

def performance_monitor():
    """Get current performance statistics"""
    return {
        "memory_cache": memory_cache.stats(),
        "profiler": profiler.get_profile_report(),
        "slowest_functions": profiler.get_slowest_functions(5)
    }

def cleanup_caches():
    """Clean up all caches"""
    memory_cache.clear()
    expired_count = file_cache.cleanup_expired()
    error_handler.logger.info(f"Cleaned up {expired_count} expired cache files")

# Performance optimization decorators
def profile(func_name: str = None):
    """Shorthand for profiling decorator"""
    return profiler.profile_function(func_name)

def memoize(ttl: int = 3600):
    """Shorthand for memory caching decorator"""
    return cached(ttl=ttl, use_file_cache=False)

def disk_cache(ttl: int = 3600):
    """Shorthand for file caching decorator"""
    return cached(ttl=ttl, use_file_cache=True)
