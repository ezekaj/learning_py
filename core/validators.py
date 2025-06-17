#!/usr/bin/env python3
"""
Input Validation Module
Provides comprehensive validation for all user inputs and data
"""

import re
import json
import html
from typing import Any, Dict, List, Optional, Union, Tuple
from datetime import datetime
from core.error_handler import ValidationError, error_handler

class InputValidator:
    """Comprehensive input validation system"""
    
    def __init__(self):
        # Email regex pattern
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        )
        
        # Password requirements
        self.password_min_length = 8
        self.password_max_length = 128
        
        # Name requirements
        self.name_min_length = 2
        self.name_max_length = 50
        
        # Code validation patterns
        self.dangerous_patterns = [
            r'import\s+os',
            r'import\s+sys',
            r'import\s+subprocess',
            r'exec\s*\(',
            r'eval\s*\(',
            r'__import__',
            r'open\s*\(',
            r'file\s*\(',
            r'input\s*\(',
            r'raw_input\s*\('
        ]
    
    def validate_email(self, email: str) -> Tuple[bool, str]:
        """
        Validate email address
        
        Args:
            email: Email address to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        if not isinstance(email, str):
            return False, "Email must be a string"
        
        email = email.strip().lower()
        
        if len(email) > 254:  # RFC 5321 limit
            return False, "Email address is too long"
        
        if not self.email_pattern.match(email):
            return False, "Invalid email format"
        
        return True, ""
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "Password is required"
        
        if not isinstance(password, str):
            return False, "Password must be a string"
        
        if len(password) < self.password_min_length:
            return False, f"Password must be at least {self.password_min_length} characters"
        
        if len(password) > self.password_max_length:
            return False, f"Password must be no more than {self.password_max_length} characters"
        
        # Check for at least one letter and one number
        has_letter = any(c.isalpha() for c in password)
        has_number = any(c.isdigit() for c in password)
        
        if not has_letter:
            return False, "Password must contain at least one letter"
        
        if not has_number:
            return False, "Password must contain at least one number"
        
        return True, ""
    
    def validate_name(self, name: str) -> Tuple[bool, str]:
        """
        Validate user name
        
        Args:
            name: Name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name:
            return False, "Name is required"
        
        if not isinstance(name, str):
            return False, "Name must be a string"
        
        name = name.strip()
        
        if len(name) < self.name_min_length:
            return False, f"Name must be at least {self.name_min_length} characters"
        
        if len(name) > self.name_max_length:
            return False, f"Name must be no more than {self.name_max_length} characters"
        
        # Check for valid characters (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
        
        return True, ""
    
    def validate_experience_level(self, level: str) -> Tuple[bool, str]:
        """
        Validate experience level
        
        Args:
            level: Experience level to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        valid_levels = [
            "complete_beginner",
            "some_experience", 
            "intermediate",
            "advanced",
            "expert"
        ]
        
        if not level:
            return False, "Experience level is required"
        
        if level not in valid_levels:
            return False, f"Experience level must be one of: {', '.join(valid_levels)}"
        
        return True, ""
    
    def validate_learning_goals(self, goals: List[str]) -> Tuple[bool, str]:
        """
        Validate learning goals
        
        Args:
            goals: List of learning goals
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(goals, list):
            return False, "Learning goals must be a list"
        
        if len(goals) > 10:
            return False, "Maximum 10 learning goals allowed"
        
        valid_goals = [
            "web_development",
            "data_science",
            "automation",
            "game_development",
            "mobile_apps",
            "desktop_apps",
            "machine_learning",
            "cybersecurity",
            "general_programming",
            "career_change"
        ]
        
        for goal in goals:
            if not isinstance(goal, str):
                return False, "Each learning goal must be a string"
            
            if goal not in valid_goals:
                return False, f"Invalid learning goal: {goal}"
        
        return True, ""
    
    def validate_user_code(self, code: str) -> Tuple[bool, str]:
        """
        Validate user-submitted code for safety
        
        Args:
            code: Python code to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(code, str):
            return False, "Code must be a string"
        
        if len(code) > 10000:  # 10KB limit
            return False, "Code is too long (maximum 10,000 characters)"
        
        # Check for dangerous patterns
        for pattern in self.dangerous_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                return False, f"Code contains potentially dangerous operations: {pattern}"
        
        # Basic syntax check
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            return False, f"Syntax error in code: {str(e)}"
        
        return True, ""
    
    def validate_quiz_answers(self, answers: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate quiz answers
        
        Args:
            answers: Dictionary of quiz answers
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not isinstance(answers, dict):
            return False, "Answers must be a dictionary"
        
        if len(answers) > 50:  # Reasonable limit
            return False, "Too many answers provided"
        
        for question_id, answer in answers.items():
            # Validate question ID
            if not isinstance(question_id, str):
                return False, "Question IDs must be strings"
            
            if not re.match(r'^[a-zA-Z0-9_-]+$', question_id):
                return False, f"Invalid question ID format: {question_id}"
            
            # Validate answer (can be string, number, or list for multiple choice)
            if not isinstance(answer, (str, int, float, list)):
                return False, f"Invalid answer type for question {question_id}"
            
            if isinstance(answer, str) and len(answer) > 1000:
                return False, f"Answer too long for question {question_id}"
        
        return True, ""
    
    def sanitize_html(self, text: str) -> str:
        """
        Sanitize HTML content to prevent XSS
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        if not isinstance(text, str):
            return str(text)
        
        # Escape HTML characters
        sanitized = html.escape(text)
        
        # Remove any remaining script tags or javascript
        sanitized = re.sub(r'<script.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    def validate_json_data(self, data: str, max_size: int = 1024*1024) -> Tuple[bool, str, Optional[Dict]]:
        """
        Validate JSON data
        
        Args:
            data: JSON string to validate
            max_size: Maximum size in bytes
            
        Returns:
            Tuple of (is_valid, error_message, parsed_data)
        """
        if not isinstance(data, str):
            return False, "Data must be a string", None
        
        if len(data.encode('utf-8')) > max_size:
            return False, f"Data too large (maximum {max_size} bytes)", None
        
        try:
            parsed_data = json.loads(data)
            return True, "", parsed_data
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}", None
    
    def validate_file_upload(self, filename: str, content: bytes, 
                           allowed_extensions: List[str] = None,
                           max_size: int = 5*1024*1024) -> Tuple[bool, str]:
        """
        Validate file upload
        
        Args:
            filename: Name of the uploaded file
            content: File content as bytes
            allowed_extensions: List of allowed file extensions
            max_size: Maximum file size in bytes
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filename:
            return False, "Filename is required"
        
        # Check file size
        if len(content) > max_size:
            return False, f"File too large (maximum {max_size/1024/1024:.1f}MB)"
        
        # Check file extension
        if allowed_extensions:
            file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
            if file_ext not in [ext.lower() for ext in allowed_extensions]:
                return False, f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
        
        # Check for dangerous filenames
        dangerous_names = ['..', '/', '\\', '<', '>', ':', '"', '|', '?', '*']
        if any(char in filename for char in dangerous_names):
            return False, "Filename contains invalid characters"
        
        return True, ""
    
    def validate_registration_data(self, data: Dict[str, Any]) -> Tuple[bool, Dict[str, str]]:
        """
        Validate complete registration data
        
        Args:
            data: Registration data dictionary
            
        Returns:
            Tuple of (is_valid, error_messages_dict)
        """
        errors = {}
        
        # Validate email
        email_valid, email_error = self.validate_email(data.get('email', ''))
        if not email_valid:
            errors['email'] = email_error
        
        # Validate password
        password_valid, password_error = self.validate_password(data.get('password', ''))
        if not password_valid:
            errors['password'] = password_error
        
        # Validate name
        name_valid, name_error = self.validate_name(data.get('name', ''))
        if not name_valid:
            errors['name'] = name_error
        
        # Validate experience level
        level_valid, level_error = self.validate_experience_level(
            data.get('experience_level', '')
        )
        if not level_valid:
            errors['experience_level'] = level_error
        
        # Validate learning goals
        goals_valid, goals_error = self.validate_learning_goals(
            data.get('learning_goals', [])
        )
        if not goals_valid:
            errors['learning_goals'] = goals_error
        
        return len(errors) == 0, errors

# Global validator instance
validator = InputValidator()
