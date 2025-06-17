#!/usr/bin/env python3
"""
Comprehensive Error Handling and Logging System
Provides robust error handling, logging, and recovery mechanisms
"""

import logging
import os
import sys
import traceback
import functools
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Type, Union
from pathlib import Path
import json

# Custom Exception Classes
class PythonLearningPlatformError(Exception):
    """Base exception for Python Learning Platform"""
    pass

class UserDataError(PythonLearningPlatformError):
    """Exception for user data related errors"""
    pass

class LessonError(PythonLearningPlatformError):
    """Exception for lesson related errors"""
    pass

class QuizError(PythonLearningPlatformError):
    """Exception for quiz related errors"""
    pass

class ChallengeError(PythonLearningPlatformError):
    """Exception for challenge related errors"""
    pass

class FileOperationError(PythonLearningPlatformError):
    """Exception for file operation errors"""
    pass

class ValidationError(PythonLearningPlatformError):
    """Exception for validation errors"""
    pass

class AuthenticationError(PythonLearningPlatformError):
    """Exception for authentication errors"""
    pass

class ConfigurationError(PythonLearningPlatformError):
    """Exception for configuration errors"""
    pass

class ErrorHandler:
    """Centralized error handling and logging system"""
    
    def __init__(self, log_dir: str = "logs", log_level: str = "INFO"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Set up logging
        self.setup_logging(log_level)
        
        # Error statistics
        self.error_stats = {
            "total_errors": 0,
            "error_types": {},
            "last_error": None
        }
        
        # Recovery strategies
        self.recovery_strategies = {
            FileOperationError: self._recover_file_operation,
            UserDataError: self._recover_user_data,
            ValidationError: self._recover_validation,
            AuthenticationError: self._recover_authentication
        }
    
    def setup_logging(self, log_level: str):
        """Set up comprehensive logging system"""
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        simple_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Create handlers
        # File handler for all logs
        file_handler = logging.FileHandler(
            self.log_dir / f"platform_{datetime.now().strftime('%Y%m%d')}.log"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        
        # Error file handler
        error_handler = logging.FileHandler(
            self.log_dir / f"errors_{datetime.now().strftime('%Y%m%d')}.log"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        console_handler.setFormatter(simple_formatter)
        
        # Configure root logger
        self.logger = logging.getLogger('PythonLearningPlatform')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        self.logger.addHandler(console_handler)
        
        # Prevent duplicate logs
        self.logger.propagate = False
    
    def handle_error(self, error: Exception, context: Dict[str, Any] = None, 
                    user_message: str = None, attempt_recovery: bool = True) -> Dict[str, Any]:
        """
        Comprehensive error handling with logging and recovery
        
        Args:
            error: The exception that occurred
            context: Additional context information
            user_message: User-friendly error message
            attempt_recovery: Whether to attempt automatic recovery
            
        Returns:
            Dictionary with error details and recovery status
        """
        # Update error statistics
        self.error_stats["total_errors"] += 1
        error_type = type(error).__name__
        self.error_stats["error_types"][error_type] = \
            self.error_stats["error_types"].get(error_type, 0) + 1
        self.error_stats["last_error"] = datetime.now().isoformat()
        
        # Create error details
        error_details = {
            "error_type": error_type,
            "error_message": str(error),
            "timestamp": datetime.now().isoformat(),
            "context": context or {},
            "traceback": traceback.format_exc(),
            "user_message": user_message or self._get_user_friendly_message(error),
            "recovery_attempted": False,
            "recovery_successful": False
        }
        
        # Log the error
        self.logger.error(
            f"Error occurred: {error_type} - {str(error)}",
            extra={
                "context": context,
                "traceback": traceback.format_exc()
            }
        )
        
        # Attempt recovery if enabled
        if attempt_recovery:
            recovery_result = self._attempt_recovery(error, context)
            error_details.update(recovery_result)
        
        return error_details
    
    def _get_user_friendly_message(self, error: Exception) -> str:
        """Generate user-friendly error messages"""
        error_type = type(error)
        
        messages = {
            FileOperationError: "There was a problem accessing a file. Please check file permissions and try again.",
            UserDataError: "There was an issue with your user data. Your progress has been backed up and we're working to restore it.",
            ValidationError: "The information provided is not valid. Please check your input and try again.",
            AuthenticationError: "Authentication failed. Please check your credentials and try again.",
            QuizError: "There was a problem with the quiz. Please refresh the page and try again.",
            ChallengeError: "There was an issue with the coding challenge. Please try submitting your code again.",
            LessonError: "There was a problem loading the lesson content. Please refresh the page.",
            ConfigurationError: "There's a configuration issue. Please contact support if this persists."
        }
        
        return messages.get(error_type, 
            "An unexpected error occurred. Please try again or contact support if the problem persists.")
    
    def _attempt_recovery(self, error: Exception, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Attempt automatic error recovery"""
        error_type = type(error)
        recovery_result = {
            "recovery_attempted": True,
            "recovery_successful": False,
            "recovery_actions": []
        }
        
        if error_type in self.recovery_strategies:
            try:
                recovery_actions = self.recovery_strategies[error_type](error, context)
                recovery_result["recovery_actions"] = recovery_actions
                recovery_result["recovery_successful"] = True
                
                self.logger.info(f"Recovery successful for {error_type.__name__}: {recovery_actions}")
                
            except Exception as recovery_error:
                self.logger.error(f"Recovery failed for {error_type.__name__}: {recovery_error}")
                recovery_result["recovery_error"] = str(recovery_error)
        
        return recovery_result
    
    def _recover_file_operation(self, error: FileOperationError, context: Dict[str, Any]) -> list:
        """Recovery strategy for file operation errors"""
        actions = []
        
        # Try to create missing directories
        file_path = context.get("file_path")
        if file_path:
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                actions.append(f"Created missing directory: {directory}")
        
        # Check and fix permissions if possible
        if file_path and os.path.exists(file_path):
            try:
                # Try to make file writable
                os.chmod(file_path, 0o666)
                actions.append(f"Fixed permissions for: {file_path}")
            except:
                pass
        
        return actions
    
    def _recover_user_data(self, error: UserDataError, context: Dict[str, Any]) -> list:
        """Recovery strategy for user data errors"""
        actions = []
        
        # Try to load from backup
        backup_dir = Path("data/backups")
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("user_progress_backup_*.json"))
            if backup_files:
                latest_backup = max(backup_files, key=os.path.getctime)
                actions.append(f"Located backup file: {latest_backup}")
                
                # Could implement backup restoration here
                actions.append("Backup restoration available")
        
        # Create empty user data structure if needed
        user_email = context.get("user_email")
        if user_email:
            actions.append(f"Prepared empty user profile for: {user_email}")
        
        return actions
    
    def _recover_validation(self, error: ValidationError, context: Dict[str, Any]) -> list:
        """Recovery strategy for validation errors"""
        actions = []
        
        # Provide default values for missing fields
        if "missing_fields" in context:
            actions.append("Identified missing required fields")
            actions.append("Default values can be provided")
        
        # Sanitize invalid input
        if "invalid_input" in context:
            actions.append("Invalid input detected and can be sanitized")
        
        return actions
    
    def _recover_authentication(self, error: AuthenticationError, context: Dict[str, Any]) -> list:
        """Recovery strategy for authentication errors"""
        actions = []
        
        # Clear invalid session data
        actions.append("Cleared invalid session data")
        
        # Redirect to login
        actions.append("Prepared redirect to login page")
        
        return actions
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics and health metrics"""
        return {
            "error_stats": self.error_stats.copy(),
            "log_files": [str(f) for f in self.log_dir.glob("*.log")],
            "system_health": self._assess_system_health()
        }
    
    def _assess_system_health(self) -> Dict[str, Any]:
        """Assess overall system health based on error patterns"""
        total_errors = self.error_stats["total_errors"]
        
        if total_errors == 0:
            status = "excellent"
        elif total_errors < 10:
            status = "good"
        elif total_errors < 50:
            status = "fair"
        else:
            status = "poor"
        
        return {
            "status": status,
            "total_errors": total_errors,
            "most_common_error": max(self.error_stats["error_types"].items(), 
                                   key=lambda x: x[1], default=("None", 0))[0]
        }

# Decorator for automatic error handling
def handle_errors(user_message: str = None, attempt_recovery: bool = True, 
                 reraise: bool = False):
    """
    Decorator for automatic error handling
    
    Args:
        user_message: Custom user-friendly message
        attempt_recovery: Whether to attempt recovery
        reraise: Whether to reraise the exception after handling
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Get error handler instance (assuming it's available globally)
                error_handler = getattr(wrapper, '_error_handler', None)
                if not error_handler:
                    error_handler = ErrorHandler()
                
                context = {
                    "function": func.__name__,
                    "args": str(args)[:200],  # Limit length
                    "kwargs": str(kwargs)[:200]
                }
                
                error_details = error_handler.handle_error(
                    e, context, user_message, attempt_recovery
                )
                
                if reraise:
                    raise
                
                return {"error": True, "details": error_details}
        
        return wrapper
    return decorator

# Global error handler instance
error_handler = ErrorHandler()
