"""
Simple integration tests for Python Learning Platform
"""

import pytest
import tempfile
import os
import json
from unittest.mock import patch, Mock

def test_core_modules_integration():
    """Test that core modules can be imported and work together"""
    from core.error_handler import error_handler
    from core.validators import validator
    from core.database_manager import db_manager
    
    # Test that modules are properly initialized
    assert error_handler is not None
    assert validator is not None
    assert db_manager is not None
    
    # Test basic functionality integration
    test_email = "test@example.com"
    is_valid, error = validator.validate_email(test_email)
    assert is_valid
    
    # Test error handling integration
    try:
        raise ValueError("Test error")
    except ValueError as e:
        result = error_handler.handle_error(e)
        assert result["error_type"] == "ValueError"

def test_data_flow_integration():
    """Test data flow between validation, database, and error handling"""
    from core.validators import validator
    from core.database_manager import db_manager
    from core.error_handler import error_handler
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Test valid data flow
        valid_data = {
            "name": "Test User",
            "email": "test@example.com",
            "created_at": "2023-01-01T00:00:00",
            "points": 100,
            "level": 2
        }
        
        # Validate data
        is_valid, error = db_manager.validate_data(valid_data, "user_progress")
        assert is_valid
        
        # Write data safely
        test_file = os.path.join(temp_dir, "test_data.json")
        success = db_manager.safe_write(test_file, valid_data, schema_name="user_progress")
        assert success
        
        # Read data back
        read_data = db_manager.safe_read(test_file, schema_name="user_progress")
        assert read_data == valid_data

def test_app_basic_functionality():
    """Test basic app functionality without full Flask setup"""
    # Test that app module can be imported
    try:
        import app
        assert hasattr(app, 'app')
        assert hasattr(app, 'load_user_data')
        assert hasattr(app, 'save_user_data')
    except ImportError as e:
        pytest.skip(f"App module import failed: {e}")

def test_user_management_integration():
    """Test user management functionality integration"""
    from core.validators import validator
    
    # Test complete user registration validation
    registration_data = {
        "name": "Integration Test User",
        "email": "integration@test.com",
        "password": "testpass123",
        "experience_level": "complete_beginner",
        "learning_goals": ["web_development", "data_science"]
    }
    
    is_valid, errors = validator.validate_registration_data(registration_data)
    assert is_valid
    assert len(errors) == 0

def test_security_integration():
    """Test security features integration"""
    from core.security import csrf_protection, rate_limiter
    from core.validators import validator
    
    # Test CSRF token generation
    token = csrf_protection.generate_token("test_user")
    assert len(token) > 0
    
    # Test token validation
    is_valid = csrf_protection.validate_token(token, "test_user")
    assert is_valid
    
    # Test HTML sanitization
    dangerous_html = "<script>alert('xss')</script><p>Safe content</p>"
    sanitized = validator.sanitize_html(dangerous_html)
    assert "<script>" not in sanitized
    assert "Safe content" in sanitized

def test_file_operations_integration():
    """Test file operations integration"""
    from core.database_manager import db_manager
    
    with tempfile.TemporaryDirectory() as temp_dir:
        test_file = os.path.join(temp_dir, "integration_test.json")
        test_data = {"integration": "test", "data": [1, 2, 3]}
        
        # Test write operation
        success = db_manager.safe_write(test_file, test_data)
        assert success
        assert os.path.exists(test_file)
        
        # Test read operation
        read_data = db_manager.safe_read(test_file)
        assert read_data == test_data
        
        # Test backup creation
        backup_path = db_manager.create_backup(test_file, force=True)
        assert backup_path is not None
        assert os.path.exists(backup_path)

def test_error_handling_integration():
    """Test error handling integration across modules"""
    from core.error_handler import error_handler, UserDataError, ValidationError
    from core.validators import validator
    
    # Test validation error handling
    invalid_email = "invalid-email-format"
    is_valid, error_msg = validator.validate_email(invalid_email)
    assert not is_valid
    assert len(error_msg) > 0
    
    # Test error handler with validation error
    validation_error = ValidationError(f"Email validation failed: {error_msg}")
    result = error_handler.handle_error(validation_error)
    
    assert result["error_type"] == "ValidationError"
    assert "user_message" in result
    assert len(result["user_message"]) > 0

if __name__ == "__main__":
    # Run basic integration tests
    print("Running integration tests...")
    
    try:
        test_core_modules_integration()
        print("✅ Core modules integration test passed")
        
        test_data_flow_integration()
        print("✅ Data flow integration test passed")
        
        test_app_basic_functionality()
        print("✅ App basic functionality test passed")
        
        test_user_management_integration()
        print("✅ User management integration test passed")
        
        test_security_integration()
        print("✅ Security integration test passed")
        
        test_file_operations_integration()
        print("✅ File operations integration test passed")
        
        test_error_handling_integration()
        print("✅ Error handling integration test passed")
        
        print("\n🎉 All integration tests passed!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()
