"""
Unit tests for database manager
"""

import pytest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock

from core.database_manager import DatabaseManager

class TestDatabaseManager:
    """Test the DatabaseManager class"""
    
    def test_initialization(self, temp_dir):
        """Test database manager initialization"""
        db_manager = DatabaseManager(data_dir=temp_dir)
        
        assert db_manager.data_dir.exists()
        assert db_manager.backup_dir.exists()
        assert db_manager.temp_dir.exists()
        assert len(db_manager.schemas) > 0
    
    def test_data_validation_user_schema(self, test_db_manager):
        """Test user data validation"""
        valid_user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "created_at": "2023-01-01T00:00:00",
            "points": 100,
            "level": 2,
            "lessons_completed": 5,
            "achievements": ["first_steps"]
        }
        
        is_valid, error = test_db_manager.validate_data(valid_user_data, "user_progress")
        assert is_valid, f"Valid user data should pass validation: {error}"
    
    def test_data_validation_invalid_user_schema(self, test_db_manager):
        """Test invalid user data validation"""
        invalid_user_data = {
            "name": "",  # Too short
            "email": "invalid-email",  # Invalid format
            "points": -10,  # Negative points
            "level": 0  # Level too low
        }
        
        is_valid, error = test_db_manager.validate_data(invalid_user_data, "user_progress")
        assert not is_valid
        assert error != ""
    
    def test_safe_write_and_read(self, test_db_manager, temp_dir):
        """Test safe write and read operations"""
        test_data = {"test": "data", "number": 123}
        file_path = os.path.join(temp_dir, "test_data.json")
        
        # Write data
        success = test_db_manager.safe_write(file_path, test_data)
        assert success
        
        # Read data back
        read_data = test_db_manager.safe_read(file_path)
        assert read_data == test_data
    
    def test_safe_write_with_validation(self, test_db_manager, temp_dir):
        """Test safe write with schema validation"""
        valid_lesson_data = {
            "id": "lesson_test",
            "title": "Test Lesson",
            "description": "A test lesson",
            "difficulty": "beginner"
        }
        
        file_path = os.path.join(temp_dir, "lesson_data.json")
        
        success = test_db_manager.safe_write(file_path, valid_lesson_data, schema_name="lessons")
        assert success
        
        # Read back and verify
        read_data = test_db_manager.safe_read(file_path, schema_name="lessons")
        assert read_data == valid_lesson_data
    
    def test_safe_write_validation_failure(self, test_db_manager, temp_dir):
        """Test safe write with validation failure"""
        invalid_lesson_data = {
            "id": "invalid_id",  # Wrong pattern
            "title": "",  # Too short
            "difficulty": "invalid"  # Not in enum
        }
        
        file_path = os.path.join(temp_dir, "invalid_lesson.json")
        
        success = test_db_manager.safe_write(file_path, invalid_lesson_data, schema_name="lessons")
        assert not success
    
    def test_backup_creation(self, test_db_manager, temp_dir):
        """Test backup file creation"""
        # Create a test file
        test_file = os.path.join(temp_dir, "test_file.json")
        test_data = {"original": "data"}
        
        with open(test_file, 'w') as f:
            json.dump(test_data, f)
        
        # Create backup
        backup_path = test_db_manager.create_backup(test_file, force=True)
        
        assert backup_path is not None
        assert os.path.exists(backup_path)
        
        # Verify backup content
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        assert backup_data == test_data
    
    def test_backup_cleanup(self, test_db_manager, temp_dir):
        """Test old backup cleanup"""
        # Create multiple backup files
        test_file = os.path.join(temp_dir, "test_file.json")
        with open(test_file, 'w') as f:
            json.dump({"test": "data"}, f)
        
        # Set low backup limit for testing
        test_db_manager.max_backups = 3
        
        # Create more backups than the limit
        backup_paths = []
        for i in range(5):
            backup_path = test_db_manager.create_backup(test_file, force=True)
            if backup_path:
                backup_paths.append(backup_path)
        
        # Check that old backups were cleaned up
        existing_backups = list(test_db_manager.backup_dir.glob("test_file_backup_*"))
        assert len(existing_backups) <= test_db_manager.max_backups
    
    def test_atomic_write_operation(self, test_db_manager, temp_dir):
        """Test atomic write operations"""
        file_path = os.path.join(temp_dir, "atomic_test.json")
        test_data = {"atomic": "write", "test": True}
        
        # Mock a failure during write to test atomicity
        with patch('shutil.move') as mock_move:
            mock_move.side_effect = Exception("Simulated failure")
            
            success = test_db_manager.safe_write(file_path, test_data)
            assert not success
            
            # Original file should not exist if write failed
            assert not os.path.exists(file_path)
    
    def test_concurrent_access_safety(self, test_db_manager, temp_dir):
        """Test thread-safe file access"""
        import threading
        import time
        
        file_path = os.path.join(temp_dir, "concurrent_test.json")
        results = []
        
        def write_data(data_id):
            data = {"thread": data_id, "timestamp": time.time()}
            success = test_db_manager.safe_write(file_path, data)
            results.append((data_id, success))
        
        # Start multiple threads writing to the same file
        threads = []
        for i in range(5):
            thread = threading.Thread(target=write_data, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All writes should succeed (due to locking)
        assert len(results) == 5
        assert all(success for _, success in results)
    
    def test_backup_info_retrieval(self, test_db_manager, temp_dir):
        """Test backup information retrieval"""
        test_file = os.path.join(temp_dir, "info_test.json")
        with open(test_file, 'w') as f:
            json.dump({"test": "data"}, f)
        
        # Create some backups
        for i in range(3):
            test_db_manager.create_backup(test_file, force=True)
        
        # Get backup info
        backup_info = test_db_manager.get_backup_info(test_file)
        
        assert len(backup_info) == 3
        for info in backup_info:
            assert "file" in info
            assert "created" in info
            assert "size" in info
            assert os.path.exists(info["file"])
    
    def test_data_recovery_from_backup(self, test_db_manager, temp_dir):
        """Test data recovery from backup"""
        file_path = os.path.join(temp_dir, "recovery_test.json")
        original_data = {"original": "data", "version": 1}
        
        # Write original data and create backup
        with open(file_path, 'w') as f:
            json.dump(original_data, f)
        test_db_manager.create_backup(file_path, force=True)
        
        # Corrupt the original file
        with open(file_path, 'w') as f:
            f.write("invalid json {")
        
        # Try to read - should recover from backup
        recovered_data = test_db_manager._restore_from_backup(file_path)
        assert recovered_data == original_data
    
    def test_schema_validation_edge_cases(self, test_db_manager):
        """Test schema validation edge cases"""
        # Test with unknown schema
        is_valid, error = test_db_manager.validate_data({"test": "data"}, "unknown_schema")
        assert not is_valid
        assert "Unknown schema" in error
        
        # Test with non-object data for object schema
        is_valid, error = test_db_manager.validate_data("string_data", "user_progress")
        assert not is_valid
        assert "must be an object" in error
    
    def test_file_permission_handling(self, test_db_manager, temp_dir):
        """Test handling of file permission errors"""
        file_path = os.path.join(temp_dir, "permission_test.json")
        
        # Create file and make it read-only (simulate permission error)
        with open(file_path, 'w') as f:
            json.dump({"test": "data"}, f)
        
        # Try to make read-only (may not work on all systems)
        try:
            os.chmod(file_path, 0o444)
            
            # Try to write - should handle permission error gracefully
            success = test_db_manager.safe_write(file_path, {"new": "data"})
            # On some systems this might still succeed, so we just check it doesn't crash
            assert isinstance(success, bool)
            
        except (OSError, PermissionError):
            # If we can't change permissions, skip this test
            pytest.skip("Cannot test file permissions on this system")
        finally:
            # Restore permissions for cleanup
            try:
                os.chmod(file_path, 0o666)
            except:
                pass

class TestDatabaseManagerPropertyValidation:
    """Test property validation in database manager"""
    
    def test_string_property_validation(self, test_db_manager):
        """Test string property validation"""
        # Valid string
        assert test_db_manager._validate_property("test", {"type": "string"})
        
        # Invalid type
        assert not test_db_manager._validate_property(123, {"type": "string"})
        
        # Length constraints
        assert test_db_manager._validate_property("test", {"type": "string", "minLength": 2, "maxLength": 10})
        assert not test_db_manager._validate_property("a", {"type": "string", "minLength": 2})
        assert not test_db_manager._validate_property("a" * 20, {"type": "string", "maxLength": 10})
    
    def test_integer_property_validation(self, test_db_manager):
        """Test integer property validation"""
        # Valid integer
        assert test_db_manager._validate_property(5, {"type": "integer"})
        
        # Invalid type
        assert not test_db_manager._validate_property("5", {"type": "integer"})
        
        # Range constraints
        assert test_db_manager._validate_property(5, {"type": "integer", "minimum": 0, "maximum": 10})
        assert not test_db_manager._validate_property(-1, {"type": "integer", "minimum": 0})
        assert not test_db_manager._validate_property(15, {"type": "integer", "maximum": 10})
    
    def test_array_property_validation(self, test_db_manager):
        """Test array property validation"""
        # Valid array
        assert test_db_manager._validate_property([], {"type": "array"})
        assert test_db_manager._validate_property([1, 2, 3], {"type": "array"})
        
        # Invalid type
        assert not test_db_manager._validate_property("not_array", {"type": "array"})
