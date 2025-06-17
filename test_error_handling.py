#!/usr/bin/env python3
"""
Test Error Handling System
Comprehensive tests for the error handling and validation systems
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.error_handler import (
    ErrorHandler, error_handler,
    UserDataError, ValidationError, FileOperationError, AuthenticationError
)
from core.validators import validator

def test_error_handler():
    """Test the error handler functionality"""
    print("🧪 Testing Error Handler...")
    
    # Create a temporary error handler for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        test_handler = ErrorHandler(log_dir=temp_dir)
        
        # Test basic error handling
        try:
            raise UserDataError("Test user data error")
        except UserDataError as e:
            result = test_handler.handle_error(e, context={"test": "data"})
            assert result["error_type"] == "UserDataError"
            assert "Test user data error" in result["error_message"]
            print("  ✅ Basic error handling works")
        
        # Test error statistics
        stats = test_handler.get_error_statistics()
        assert stats["error_stats"]["total_errors"] == 1
        print("  ✅ Error statistics tracking works")
        
        # Test log file creation
        log_files = list(Path(temp_dir).glob("*.log"))
        assert len(log_files) > 0
        print("  ✅ Log files created successfully")

def test_input_validation():
    """Test the input validation system"""
    print("\n🧪 Testing Input Validation...")
    
    # Test email validation
    valid_email, _ = validator.validate_email("test@example.com")
    assert valid_email
    
    invalid_email, error = validator.validate_email("invalid-email")
    assert not invalid_email
    assert "Invalid email format" in error
    print("  ✅ Email validation works")
    
    # Test password validation
    valid_password, _ = validator.validate_password("password123")
    assert valid_password
    
    weak_password, error = validator.validate_password("123")
    assert not weak_password
    assert "at least" in error
    print("  ✅ Password validation works")
    
    # Test name validation
    valid_name, _ = validator.validate_name("John Doe")
    assert valid_name
    
    invalid_name, error = validator.validate_name("J@hn")
    assert not invalid_name
    assert "can only contain" in error
    print("  ✅ Name validation works")
    
    # Test code validation
    safe_code, _ = validator.validate_user_code("print('Hello, World!')")
    assert safe_code
    
    dangerous_code, error = validator.validate_user_code("import os; os.system('rm -rf /')")
    assert not dangerous_code
    assert "dangerous" in error
    print("  ✅ Code validation works")
    
    # Test registration data validation
    valid_data = {
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User",
        "experience_level": "complete_beginner",
        "learning_goals": ["web_development"]
    }
    
    is_valid, errors = validator.validate_registration_data(valid_data)
    assert is_valid
    assert len(errors) == 0
    
    invalid_data = {
        "email": "invalid-email",
        "password": "123",
        "name": "",
        "experience_level": "invalid_level",
        "learning_goals": ["invalid_goal"]
    }
    
    is_valid, errors = validator.validate_registration_data(invalid_data)
    assert not is_valid
    assert len(errors) > 0
    print("  ✅ Registration data validation works")

def test_html_sanitization():
    """Test HTML sanitization"""
    print("\n🧪 Testing HTML Sanitization...")
    
    # Test basic sanitization
    dangerous_html = "<script>alert('xss')</script><p>Safe content</p>"
    sanitized = validator.sanitize_html(dangerous_html)
    assert "<script>" not in sanitized
    assert "Safe content" in sanitized
    print("  ✅ HTML sanitization works")
    
    # Test JavaScript removal
    js_content = "javascript:alert('xss')"
    sanitized = validator.sanitize_html(js_content)
    assert "javascript:" not in sanitized
    print("  ✅ JavaScript removal works")

def test_file_operations():
    """Test file operation error handling"""
    print("\n🧪 Testing File Operations...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_handler = ErrorHandler(log_dir=temp_dir)
        
        # Test file permission error
        try:
            # Try to write to a non-existent directory without creating it
            with open("/nonexistent/path/file.txt", "w") as f:
                f.write("test")
        except (FileNotFoundError, PermissionError) as e:
            result = test_handler.handle_error(
                FileOperationError(f"File operation failed: {e}"),
                context={"file_path": "/nonexistent/path/file.txt"}
            )
            assert result["error_type"] == "FileOperationError"
            print("  ✅ File operation error handling works")

def test_json_validation():
    """Test JSON validation"""
    print("\n🧪 Testing JSON Validation...")
    
    # Test valid JSON
    valid_json = '{"key": "value", "number": 123}'
    is_valid, error, data = validator.validate_json_data(valid_json)
    assert is_valid
    assert data["key"] == "value"
    print("  ✅ Valid JSON parsing works")
    
    # Test invalid JSON
    invalid_json = '{"key": "value", "invalid": }'
    is_valid, error, data = validator.validate_json_data(invalid_json)
    assert not is_valid
    assert "Invalid JSON" in error
    assert data is None
    print("  ✅ Invalid JSON detection works")

def test_quiz_answer_validation():
    """Test quiz answer validation"""
    print("\n🧪 Testing Quiz Answer Validation...")
    
    # Test valid answers
    valid_answers = {
        "question_1": "answer1",
        "question_2": 2,
        "question_3": ["option1", "option2"]
    }
    
    is_valid, error = validator.validate_quiz_answers(valid_answers)
    assert is_valid
    print("  ✅ Valid quiz answers accepted")
    
    # Test invalid answers
    invalid_answers = {
        "invalid@id": "answer",
        "question_2": "x" * 2000  # Too long
    }
    
    is_valid, error = validator.validate_quiz_answers(invalid_answers)
    assert not is_valid
    print("  ✅ Invalid quiz answers rejected")

def test_error_recovery():
    """Test error recovery mechanisms"""
    print("\n🧪 Testing Error Recovery...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_handler = ErrorHandler(log_dir=temp_dir)
        
        # Test file operation recovery
        try:
            raise FileOperationError("Test file error")
        except FileOperationError as e:
            result = test_handler.handle_error(
                e, 
                context={"file_path": os.path.join(temp_dir, "test.txt")},
                attempt_recovery=True
            )
            assert result["recovery_attempted"]
            print("  ✅ Error recovery attempted")

def run_comprehensive_tests():
    """Run all error handling tests"""
    print("🚀 Running Comprehensive Error Handling Tests")
    print("=" * 60)
    
    try:
        test_error_handler()
        test_input_validation()
        test_html_sanitization()
        test_file_operations()
        test_json_validation()
        test_quiz_answer_validation()
        test_error_recovery()
        
        print("\n" + "=" * 60)
        print("🎉 All Error Handling Tests Passed!")
        print("✅ Error handling system is working correctly")
        print("✅ Input validation is functioning properly")
        print("✅ Security measures are in place")
        print("✅ Recovery mechanisms are operational")
        
        # Display error handler statistics
        stats = error_handler.get_error_statistics()
        print(f"\n📊 Error Handler Statistics:")
        print(f"   Total errors handled: {stats['error_stats']['total_errors']}")
        print(f"   System health: {stats['system_health']['status']}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)
