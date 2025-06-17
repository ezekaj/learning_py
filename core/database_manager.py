#!/usr/bin/env python3
"""
Database Manager
Provides safe data operations, backup mechanisms, and data integrity
"""

import json
import os
import shutil
import hashlib
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import threading
import tempfile

# Try to import fcntl for Unix systems, use alternative for Windows
try:
    import fcntl
    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False

from .error_handler import error_handler, UserDataError, FileOperationError
from .validators import validator

class DatabaseManager:
    """Safe database operations with backup and recovery"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.backup_dir = self.data_dir / "backups"
        self.temp_dir = self.data_dir / "temp"
        
        # Create directories
        self.data_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)
        
        # File locks for thread safety
        self._locks = {}
        self._lock_manager = threading.Lock()
        
        # Backup settings
        self.max_backups = 50
        self.backup_interval = 3600  # 1 hour
        self.last_backup = {}
        
        # Data validation schemas
        self.schemas = {
            "user_progress": self._get_user_schema(),
            "lessons": self._get_lesson_schema(),
            "quizzes": self._get_quiz_schema(),
            "challenges": self._get_challenge_schema()
        }
    
    def _get_file_lock(self, file_path: str) -> threading.Lock:
        """Get or create a lock for a specific file"""
        with self._lock_manager:
            if file_path not in self._locks:
                self._locks[file_path] = threading.Lock()
            return self._locks[file_path]
    
    def _get_user_schema(self) -> Dict:
        """Get user data validation schema"""
        return {
            "type": "object",
            "required": ["name", "email", "created_at", "points", "level"],
            "properties": {
                "name": {"type": "string", "minLength": 1, "maxLength": 100},
                "email": {"type": "string", "format": "email"},
                "created_at": {"type": "string"},
                "points": {"type": "integer", "minimum": 0},
                "level": {"type": "integer", "minimum": 1},
                "lessons_completed": {"type": "integer", "minimum": 0},
                "achievements": {"type": "array", "items": {"type": "string"}}
            }
        }
    
    def _get_lesson_schema(self) -> Dict:
        """Get lesson data validation schema"""
        return {
            "type": "object",
            "required": ["id", "title", "description", "difficulty"],
            "properties": {
                "id": {"type": "string", "pattern": "^lesson_[a-zA-Z0-9_]+$"},
                "title": {"type": "string", "minLength": 1, "maxLength": 200},
                "description": {"type": "string", "minLength": 1},
                "difficulty": {"type": "string", "enum": ["beginner", "intermediate", "advanced", "expert"]}
            }
        }
    
    def _get_quiz_schema(self) -> Dict:
        """Get quiz data validation schema"""
        return {
            "type": "object",
            "required": ["id", "title", "questions"],
            "properties": {
                "id": {"type": "string", "pattern": "^quiz_[a-zA-Z0-9_]+$"},
                "title": {"type": "string", "minLength": 1, "maxLength": 200},
                "questions": {"type": "integer", "minimum": 1, "maximum": 100}
            }
        }
    
    def _get_challenge_schema(self) -> Dict:
        """Get challenge data validation schema"""
        return {
            "type": "object",
            "required": ["id", "title", "difficulty"],
            "properties": {
                "id": {"type": "string", "pattern": "^challenge_[a-zA-Z0-9_]+$"},
                "title": {"type": "string", "minLength": 1, "maxLength": 200},
                "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]}
            }
        }
    
    def validate_data(self, data: Any, schema_name: str) -> tuple[bool, str]:
        """Validate data against schema"""
        try:
            schema = self.schemas.get(schema_name)
            if not schema:
                return False, f"Unknown schema: {schema_name}"
            
            # Basic validation (simplified - in production use jsonschema library)
            if schema["type"] == "object":
                if not isinstance(data, dict):
                    return False, "Data must be an object"
                
                # Check required fields
                for field in schema.get("required", []):
                    if field not in data:
                        return False, f"Missing required field: {field}"
                
                # Validate properties
                for field, value in data.items():
                    if field in schema.get("properties", {}):
                        prop_schema = schema["properties"][field]
                        if not self._validate_property(value, prop_schema):
                            return False, f"Invalid value for field: {field}"
            
            return True, ""
            
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _validate_property(self, value: Any, prop_schema: Dict) -> bool:
        """Validate a single property"""
        prop_type = prop_schema.get("type")
        
        if prop_type == "string":
            if not isinstance(value, str):
                return False
            min_len = prop_schema.get("minLength", 0)
            max_len = prop_schema.get("maxLength", float('inf'))
            return min_len <= len(value) <= max_len
        
        elif prop_type == "integer":
            if not isinstance(value, int):
                return False
            minimum = prop_schema.get("minimum", float('-inf'))
            maximum = prop_schema.get("maximum", float('inf'))
            return minimum <= value <= maximum
        
        elif prop_type == "array":
            return isinstance(value, list)
        
        return True
    
    def create_backup(self, file_path: str, force: bool = False) -> Optional[str]:
        """Create backup of a file"""
        try:
            file_path = Path(file_path)
            
            # Check if backup is needed
            if not force:
                last_backup_time = self.last_backup.get(str(file_path), 0)
                if time.time() - last_backup_time < self.backup_interval:
                    return None
            
            if not file_path.exists():
                return None
            
            # Create backup filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}_backup_{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name
            
            # Copy file to backup
            shutil.copy2(file_path, backup_path)
            
            # Update last backup time
            self.last_backup[str(file_path)] = time.time()
            
            # Clean old backups
            self._cleanup_old_backups(file_path.stem)
            
            error_handler.logger.info(f"Created backup: {backup_path}")
            return str(backup_path)
            
        except Exception as e:
            error_handler.handle_error(
                FileOperationError(f"Failed to create backup: {e}"),
                context={"file_path": str(file_path)}
            )
            return None
    
    def _cleanup_old_backups(self, file_stem: str):
        """Remove old backup files"""
        try:
            backup_pattern = f"{file_stem}_backup_*"
            backup_files = list(self.backup_dir.glob(backup_pattern))
            
            # Sort by modification time (newest first)
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # Remove excess backups
            for old_backup in backup_files[self.max_backups:]:
                old_backup.unlink()
                error_handler.logger.debug(f"Removed old backup: {old_backup}")
                
        except Exception as e:
            error_handler.logger.warning(f"Failed to cleanup old backups: {e}")
    
    def safe_write(self, file_path: str, data: Any, schema_name: str = None) -> bool:
        """Safely write data to file with validation and backup"""
        file_path = Path(file_path)
        lock = self._get_file_lock(str(file_path))
        
        with lock:
            try:
                # Validate data if schema provided
                if schema_name:
                    is_valid, error_msg = self.validate_data(data, schema_name)
                    if not is_valid:
                        raise UserDataError(f"Data validation failed: {error_msg}")
                
                # Create backup of existing file
                if file_path.exists():
                    self.create_backup(str(file_path))
                
                # Write to temporary file first
                temp_file = self.temp_dir / f"{file_path.name}.tmp"
                
                with open(temp_file, 'w', encoding='utf-8') as f:
                    if isinstance(data, (dict, list)):
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    else:
                        f.write(str(data))
                
                # Verify the written data
                if isinstance(data, (dict, list)):
                    with open(temp_file, 'r', encoding='utf-8') as f:
                        verification_data = json.load(f)
                    
                    if verification_data != data:
                        raise UserDataError("Data verification failed after write")
                
                # Atomic move to final location
                file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(temp_file), str(file_path))
                
                error_handler.logger.debug(f"Successfully wrote data to: {file_path}")
                return True
                
            except Exception as e:
                # Clean up temp file if it exists
                temp_file = self.temp_dir / f"{file_path.name}.tmp"
                if temp_file.exists():
                    temp_file.unlink()
                
                error_handler.handle_error(
                    UserDataError(f"Failed to write data: {e}"),
                    context={"file_path": str(file_path), "schema": schema_name}
                )
                return False
    
    def safe_read(self, file_path: str, schema_name: str = None) -> Optional[Any]:
        """Safely read data from file with validation"""
        file_path = Path(file_path)
        lock = self._get_file_lock(str(file_path))
        
        with lock:
            try:
                if not file_path.exists():
                    return None
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    if file_path.suffix.lower() == '.json':
                        data = json.load(f)
                    else:
                        data = f.read()
                
                # Validate data if schema provided
                if schema_name and isinstance(data, (dict, list)):
                    is_valid, error_msg = self.validate_data(data, schema_name)
                    if not is_valid:
                        error_handler.logger.warning(f"Data validation failed for {file_path}: {error_msg}")
                        # Try to restore from backup
                        return self._restore_from_backup(str(file_path))
                
                return data
                
            except json.JSONDecodeError as e:
                error_handler.handle_error(
                    UserDataError(f"Invalid JSON in file: {e}"),
                    context={"file_path": str(file_path)}
                )
                # Try to restore from backup
                return self._restore_from_backup(str(file_path))
                
            except Exception as e:
                error_handler.handle_error(
                    FileOperationError(f"Failed to read file: {e}"),
                    context={"file_path": str(file_path)}
                )
                return None
    
    def _restore_from_backup(self, file_path: str) -> Optional[Any]:
        """Restore data from the most recent backup"""
        try:
            file_path = Path(file_path)
            backup_pattern = f"{file_path.stem}_backup_*{file_path.suffix}"
            backup_files = list(self.backup_dir.glob(backup_pattern))
            
            if not backup_files:
                error_handler.logger.error(f"No backups found for {file_path}")
                return None
            
            # Get most recent backup
            latest_backup = max(backup_files, key=lambda x: x.stat().st_mtime)
            
            # Read backup data
            with open(latest_backup, 'r', encoding='utf-8') as f:
                if latest_backup.suffix.lower() == '.json':
                    data = json.load(f)
                else:
                    data = f.read()
            
            # Restore the file
            shutil.copy2(latest_backup, file_path)
            
            error_handler.logger.info(f"Restored {file_path} from backup: {latest_backup}")
            return data
            
        except Exception as e:
            error_handler.logger.error(f"Failed to restore from backup: {e}")
            return None
    
    def get_backup_info(self, file_path: str) -> List[Dict]:
        """Get information about available backups"""
        try:
            file_path = Path(file_path)
            backup_pattern = f"{file_path.stem}_backup_*{file_path.suffix}"
            backup_files = list(self.backup_dir.glob(backup_pattern))
            
            backup_info = []
            for backup_file in backup_files:
                stat = backup_file.stat()
                backup_info.append({
                    "file": str(backup_file),
                    "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "size": stat.st_size
                })
            
            # Sort by creation time (newest first)
            backup_info.sort(key=lambda x: x["created"], reverse=True)
            return backup_info
            
        except Exception as e:
            error_handler.logger.error(f"Failed to get backup info: {e}")
            return []

# Global database manager instance
db_manager = DatabaseManager()
