#!/usr/bin/env python3
"""
Security Module
Provides CSRF protection, rate limiting, and other security features
"""

import time
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from functools import wraps
from flask import request, session, jsonify, abort
import json
import os

from .error_handler import error_handler, ValidationError

class CSRFProtection:
    """CSRF (Cross-Site Request Forgery) protection"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.token_lifetime = 3600  # 1 hour in seconds
    
    def generate_token(self, user_id: str = None) -> str:
        """Generate a CSRF token"""
        timestamp = str(int(time.time()))
        user_id = user_id or session.get('user', 'anonymous')
        
        # Create token data
        token_data = f"{user_id}:{timestamp}:{secrets.token_hex(16)}"
        
        # Create signature
        signature = hashlib.sha256(
            f"{token_data}:{self.secret_key}".encode()
        ).hexdigest()
        
        token = f"{token_data}:{signature}"
        
        # Store in session
        session['csrf_token'] = token
        session['csrf_generated'] = timestamp
        
        return token
    
    def validate_token(self, token: str, user_id: str = None) -> bool:
        """Validate a CSRF token"""
        if not token:
            return False
        
        try:
            # Parse token
            parts = token.split(':')
            if len(parts) != 4:
                return False
            
            token_user, timestamp, random_part, signature = parts
            user_id = user_id or session.get('user', 'anonymous')
            
            # Check user match
            if token_user != user_id:
                return False
            
            # Check timestamp (token expiry)
            token_time = int(timestamp)
            current_time = int(time.time())
            if current_time - token_time > self.token_lifetime:
                return False
            
            # Verify signature
            token_data = f"{token_user}:{timestamp}:{random_part}"
            expected_signature = hashlib.sha256(
                f"{token_data}:{self.secret_key}".encode()
            ).hexdigest()
            
            return signature == expected_signature
            
        except (ValueError, TypeError) as e:
            error_handler.logger.warning(f"CSRF token validation error: {e}")
            return False
    
    def get_token_for_session(self) -> str:
        """Get or generate CSRF token for current session"""
        existing_token = session.get('csrf_token')
        generated_time = session.get('csrf_generated')
        
        # Check if existing token is still valid
        if existing_token and generated_time:
            try:
                if int(time.time()) - int(generated_time) < self.token_lifetime:
                    if self.validate_token(existing_token):
                        return existing_token
            except (ValueError, TypeError):
                pass
        
        # Generate new token
        return self.generate_token()

class RateLimiter:
    """Rate limiting for API endpoints"""
    
    def __init__(self, storage_file: str = "data/rate_limits.json"):
        self.storage_file = storage_file
        self.limits = {}
        self.load_limits()
    
    def load_limits(self):
        """Load rate limit data from file"""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r') as f:
                    self.limits = json.load(f)
        except Exception as e:
            error_handler.logger.warning(f"Failed to load rate limits: {e}")
            self.limits = {}
    
    def save_limits(self):
        """Save rate limit data to file"""
        try:
            os.makedirs(os.path.dirname(self.storage_file), exist_ok=True)
            with open(self.storage_file, 'w') as f:
                json.dump(self.limits, f, indent=2)
        except Exception as e:
            error_handler.logger.error(f"Failed to save rate limits: {e}")
    
    def is_allowed(self, identifier: str, limit: int, window: int) -> Tuple[bool, Dict]:
        """
        Check if request is allowed under rate limit
        
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            limit: Maximum requests allowed
            window: Time window in seconds
            
        Returns:
            Tuple of (is_allowed, info_dict)
        """
        current_time = time.time()
        
        # Clean old entries
        self.cleanup_old_entries(current_time, window)
        
        # Get or create limit data for identifier
        if identifier not in self.limits:
            self.limits[identifier] = []
        
        requests = self.limits[identifier]
        
        # Remove requests outside the window
        requests = [req_time for req_time in requests if current_time - req_time < window]
        
        # Check if limit exceeded
        if len(requests) >= limit:
            return False, {
                "allowed": False,
                "limit": limit,
                "window": window,
                "requests_made": len(requests),
                "reset_time": min(requests) + window
            }
        
        # Add current request
        requests.append(current_time)
        self.limits[identifier] = requests
        
        # Save periodically (every 10 requests to avoid too much I/O)
        if len(requests) % 10 == 0:
            self.save_limits()
        
        return True, {
            "allowed": True,
            "limit": limit,
            "window": window,
            "requests_made": len(requests),
            "remaining": limit - len(requests)
        }
    
    def cleanup_old_entries(self, current_time: float, max_age: int = 3600):
        """Clean up old rate limit entries"""
        for identifier in list(self.limits.keys()):
            requests = self.limits[identifier]
            # Keep only requests from the last hour
            recent_requests = [req_time for req_time in requests if current_time - req_time < max_age]
            
            if recent_requests:
                self.limits[identifier] = recent_requests
            else:
                del self.limits[identifier]
    
    def get_client_identifier(self) -> str:
        """Get unique identifier for the current client"""
        # Try to get user ID first
        if 'user' in session:
            return f"user:{session['user']}"
        
        # Fall back to IP address
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if client_ip:
            # Take first IP if there are multiple (proxy chain)
            client_ip = client_ip.split(',')[0].strip()
        else:
            client_ip = 'unknown'
        
        return f"ip:{client_ip}"

# Global instances
csrf_protection = CSRFProtection()
rate_limiter = RateLimiter()

def require_csrf_token(f):
    """Decorator to require CSRF token for POST requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            token = request.headers.get('X-CSRF-Token') or request.form.get('csrf_token')
            
            if not token:
                error_handler.logger.warning(f"Missing CSRF token for {request.endpoint}")
                return jsonify({"success": False, "error": "CSRF token required"}), 403
            
            if not csrf_protection.validate_token(token):
                error_handler.logger.warning(f"Invalid CSRF token for {request.endpoint}")
                return jsonify({"success": False, "error": "Invalid CSRF token"}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def rate_limit(requests_per_minute: int = 60, requests_per_hour: int = 1000):
    """Decorator to apply rate limiting"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            identifier = rate_limiter.get_client_identifier()
            
            # Check minute limit
            allowed_minute, info_minute = rate_limiter.is_allowed(
                f"{identifier}:minute", requests_per_minute, 60
            )
            
            # Check hour limit
            allowed_hour, info_hour = rate_limiter.is_allowed(
                f"{identifier}:hour", requests_per_hour, 3600
            )
            
            if not allowed_minute:
                error_handler.logger.warning(f"Rate limit exceeded (minute) for {identifier}")
                return jsonify({
                    "success": False,
                    "error": "Rate limit exceeded. Please try again later.",
                    "retry_after": int(info_minute["reset_time"] - time.time())
                }), 429
            
            if not allowed_hour:
                error_handler.logger.warning(f"Rate limit exceeded (hour) for {identifier}")
                return jsonify({
                    "success": False,
                    "error": "Hourly rate limit exceeded. Please try again later.",
                    "retry_after": int(info_hour["reset_time"] - time.time())
                }), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal"""
    import re
    
    # Remove path separators and dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = re.sub(r'\.\.', '', filename)  # Remove .. sequences
    filename = filename.strip('. ')  # Remove leading/trailing dots and spaces
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename or 'unnamed_file'

def validate_file_type(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate file type by extension"""
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in [ext.lower() for ext in allowed_extensions]
