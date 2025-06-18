"""
Unit tests for error handling system
"""

import pytest
import tempfile
import os
from unittest.mock import patch, Mock
from datetime import datetime

from core.error_handler import (
    ErrorHandler, 
    UserDataError, 
    ValidationError, 
    FileOperationError,
    AuthenticationError,
    handle_errors
)

class TestErrorHandler:
    """Test the ErrorHandler class"""
    
    def test_error_handler_initialization(self, temp_dir):
        """Test error handler initialization"""
        handler = ErrorHandler(log_dir=temp_dir)
        
        assert handler.log_dir.exists()
        assert handler.error_stats["total_errors"] == 0
        assert isinstance(handler.error_stats["error_types"], dict)
        assert handler.logger is not None
    
    def test_handle_error_basic(self, test_error_handler):
        """Test basic error handling"""
        error = UserDataError("Test error message")
        
        result = test_error_handler.handle_error(error)
        
        assert result["error_type"] == "UserDataError"
        assert result["error_message"] == "Test error message"
        assert "timestamp" in result
        assert "traceback" in result
        assert "user_message" in result
    
    def test_handle_error_with_context(self, test_error_handler):
        """Test error handling with context"""
        error = ValidationError("Invalid input")
        context = {"field": "email", "value": "invalid-email"}
        
        result = test_error_handler.handle_error(error, context=context)
        
        assert result["context"] == context
        assert result["error_type"] == "ValidationError"
    
    def test_handle_error_with_user_message(self, test_error_handler):
        """Test error handling with custom user message"""
        error = FileOperationError("File not found")
        user_message = "Please check the file path"
        
        result = test_error_handler.handle_error(error, user_message=user_message)
        
        assert result["user_message"] == user_message
    
    def test_error_statistics_tracking(self, test_error_handler):
        """Test error statistics tracking"""
        # Handle multiple errors
        test_error_handler.handle_error(UserDataError("Error 1"))
        test_error_handler.handle_error(UserDataError("Error 2"))
        test_error_handler.handle_error(ValidationError("Error 3"))
        
        stats = test_error_handler.get_error_statistics()
        
        assert stats["error_stats"]["total_errors"] == 3
        assert stats["error_stats"]["error_types"]["UserDataError"] == 2
        assert stats["error_stats"]["error_types"]["ValidationError"] == 1
    
    def test_user_friendly_messages(self, test_error_handler):
        """Test user-friendly error messages"""
        errors_and_messages = [
            (FileOperationError("Test"), "file"),
            (UserDataError("Test"), "user data"),
            (ValidationError("Test"), "not valid"),
            (AuthenticationError("Test"), "Authentication failed")
        ]
        
        for error, expected_keyword in errors_and_messages:
            result = test_error_handler.handle_error(error)
            assert expected_keyword.lower() in result["user_message"].lower()
    
    def test_recovery_attempt(self, test_error_handler):
        """Test error recovery mechanisms"""
        error = FileOperationError("Test file error")
        context = {"file_path": "/test/path/file.txt"}
        
        result = test_error_handler.handle_error(
            error, 
            context=context, 
            attempt_recovery=True
        )
        
        assert result["recovery_attempted"] is True
        assert "recovery_actions" in result
    
    def test_system_health_assessment(self, test_error_handler):
        """Test system health assessment"""
        # No errors - should be excellent
        stats = test_error_handler.get_error_statistics()
        assert stats["system_health"]["status"] == "excellent"
        
        # Add some errors
        for i in range(5):
            test_error_handler.handle_error(UserDataError(f"Error {i}"))
        
        stats = test_error_handler.get_error_statistics()
        assert stats["system_health"]["status"] == "good"
    
    def test_log_file_creation(self, test_error_handler):
        """Test that log files are created"""
        test_error_handler.handle_error(UserDataError("Test error"))
        
        log_files = list(test_error_handler.log_dir.glob("*.log"))
        assert len(log_files) > 0
        
        # Check that error was logged
        error_log = next((f for f in log_files if "error" in f.name), None)
        if error_log:
            content = error_log.read_text()
            assert "UserDataError" in content

class TestErrorDecorator:
    """Test the error handling decorator"""
    
    def test_handle_errors_decorator_success(self, test_error_handler):
        """Test decorator with successful function"""
        @handle_errors(user_message="Custom error message")
        def successful_function(x, y):
            return x + y
        
        # Attach error handler to function
        successful_function._error_handler = test_error_handler
        
        result = successful_function(2, 3)
        assert result == 5
    
    def test_handle_errors_decorator_with_error(self, test_error_handler):
        """Test decorator with function that raises error"""
        @handle_errors(user_message="Custom error message", reraise=False)
        def failing_function():
            raise ValueError("Test error")
        
        # Attach error handler to function
        failing_function._error_handler = test_error_handler
        
        result = failing_function()
        assert result["error"] is True
        assert "details" in result
    
    def test_handle_errors_decorator_reraise(self, test_error_handler):
        """Test decorator with reraise=True"""
        @handle_errors(reraise=True)
        def failing_function():
            raise ValueError("Test error")
        
        # Attach error handler to function
        failing_function._error_handler = test_error_handler
        
        with pytest.raises(ValueError):
            failing_function()

class TestCustomExceptions:
    """Test custom exception classes"""
    
    def test_custom_exception_inheritance(self):
        """Test that custom exceptions inherit properly"""
        from core.error_handler import PythonLearningPlatformError
        
        exceptions = [
            UserDataError,
            ValidationError,
            FileOperationError,
            AuthenticationError
        ]
        
        for exc_class in exceptions:
            assert issubclass(exc_class, PythonLearningPlatformError)
            assert issubclass(exc_class, Exception)
    
    def test_custom_exception_messages(self):
        """Test custom exception messages"""
        message = "Test error message"
        
        error = UserDataError(message)
        assert str(error) == message
        
        error = ValidationError(message)
        assert str(error) == message

class TestErrorRecovery:
    """Test error recovery mechanisms"""
    
    def test_file_operation_recovery(self, test_error_handler, temp_dir):
        """Test file operation error recovery"""
        error = FileOperationError("Test file error")
        context = {"file_path": os.path.join(temp_dir, "test", "file.txt")}
        
        result = test_error_handler._attempt_recovery(error, context)
        
        assert result["recovery_attempted"] is True
        assert len(result["recovery_actions"]) > 0
    
    def test_user_data_recovery(self, test_error_handler, temp_dir):
        """Test user data error recovery"""
        # Create a mock backup directory
        backup_dir = os.path.join(temp_dir, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        # Create a mock backup file
        backup_file = os.path.join(backup_dir, "user_progress_backup_20231201_120000.json")
        with open(backup_file, 'w') as f:
            f.write('{"test": "data"}')
        
        error = UserDataError("Test user data error")
        context = {"user_email": "test@example.com"}
        
        result = test_error_handler._attempt_recovery(error, context)
        
        assert result["recovery_attempted"] is True
        assert len(result["recovery_actions"]) > 0
    
    def test_validation_recovery(self, test_error_handler):
        """Test validation error recovery"""
        error = ValidationError("Test validation error")
        context = {"missing_fields": ["email", "name"]}
        
        result = test_error_handler._attempt_recovery(error, context)
        
        assert result["recovery_attempted"] is True
        assert len(result["recovery_actions"]) > 0
    
    def test_authentication_recovery(self, test_error_handler):
        """Test authentication error recovery"""
        error = AuthenticationError("Test auth error")
        context = {"user_id": "test_user"}
        
        result = test_error_handler._attempt_recovery(error, context)
        
        assert result["recovery_attempted"] is True
        assert len(result["recovery_actions"]) > 0
