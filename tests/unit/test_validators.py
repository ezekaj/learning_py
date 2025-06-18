"""
Unit tests for input validation system
"""

import pytest
import json
from core.validators import InputValidator

class TestEmailValidation:
    """Test email validation"""
    
    def test_valid_emails(self, test_validator):
        """Test valid email addresses"""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@numbers.com",
            "a@b.co"
        ]
        
        for email in valid_emails:
            is_valid, error = test_validator.validate_email(email)
            assert is_valid, f"Email {email} should be valid, but got error: {error}"
    
    def test_invalid_emails(self, test_validator):
        """Test invalid email addresses"""
        invalid_emails = [
            "",
            "invalid-email",
            "@domain.com",
            "user@",
            "user@domain",
            "user.domain.com",
            "user name@domain.com",
            "user@domain .com"
        ]

        for email in invalid_emails:
            is_valid, error = test_validator.validate_email(email)
            assert not is_valid, f"Email {email} should be invalid"
            assert error != "", f"Error message should be provided for {email}"
    
    def test_email_case_normalization(self, test_validator):
        """Test email case normalization"""
        is_valid, error = test_validator.validate_email("TEST@EXAMPLE.COM")
        assert is_valid
    
    def test_email_length_limits(self, test_validator):
        """Test email length limits"""
        # Too long email
        long_email = "a" * 250 + "@example.com"
        is_valid, error = test_validator.validate_email(long_email)
        assert not is_valid
        assert "too long" in error

class TestPasswordValidation:
    """Test password validation"""
    
    def test_valid_passwords(self, test_validator):
        """Test valid passwords"""
        valid_passwords = [
            "password123",
            "MySecurePass1",
            "test123456",
            "abcdefgh1"
        ]
        
        for password in valid_passwords:
            is_valid, error = test_validator.validate_password(password)
            assert is_valid, f"Password {password} should be valid, but got error: {error}"
    
    def test_invalid_passwords(self, test_validator):
        """Test invalid passwords"""
        invalid_cases = [
            ("", "required"),
            ("123", "at least"),
            ("password", "number"),
            ("12345678", "letter"),
            ("a" * 130, "no more than")
        ]
        
        for password, expected_error_keyword in invalid_cases:
            is_valid, error = test_validator.validate_password(password)
            assert not is_valid, f"Password '{password}' should be invalid"
            assert expected_error_keyword.lower() in error.lower()
    
    def test_password_requirements(self, test_validator):
        """Test specific password requirements"""
        # No letters
        is_valid, error = test_validator.validate_password("12345678")
        assert not is_valid
        assert "letter" in error
        
        # No numbers
        is_valid, error = test_validator.validate_password("abcdefgh")
        assert not is_valid
        assert "number" in error

class TestNameValidation:
    """Test name validation"""
    
    def test_valid_names(self, test_validator):
        """Test valid names"""
        valid_names = [
            "John Doe",
            "Mary Jane",
            "O'Connor",
            "Jean-Pierre",
            "Smith",
            "Anna-Maria"
        ]
        
        for name in valid_names:
            is_valid, error = test_validator.validate_name(name)
            assert is_valid, f"Name '{name}' should be valid, but got error: {error}"
    
    def test_invalid_names(self, test_validator):
        """Test invalid names"""
        invalid_names = [
            "",
            "A",  # Too short
            "John123",  # Numbers
            "John@Doe",  # Special characters
            "A" * 60,  # Too long
            "John_Doe"  # Underscore
        ]
        
        for name in invalid_names:
            is_valid, error = test_validator.validate_name(name)
            assert not is_valid, f"Name '{name}' should be invalid"

class TestExperienceLevelValidation:
    """Test experience level validation"""
    
    def test_valid_experience_levels(self, test_validator):
        """Test valid experience levels"""
        valid_levels = [
            "complete_beginner",
            "some_experience",
            "intermediate",
            "advanced",
            "expert"
        ]
        
        for level in valid_levels:
            is_valid, error = test_validator.validate_experience_level(level)
            assert is_valid, f"Level '{level}' should be valid"
    
    def test_invalid_experience_levels(self, test_validator):
        """Test invalid experience levels"""
        invalid_levels = [
            "",
            "beginner",
            "pro",
            "master",
            "invalid_level"
        ]
        
        for level in invalid_levels:
            is_valid, error = test_validator.validate_experience_level(level)
            assert not is_valid, f"Level '{level}' should be invalid"

class TestLearningGoalsValidation:
    """Test learning goals validation"""
    
    def test_valid_learning_goals(self, test_validator):
        """Test valid learning goals"""
        valid_goals = [
            ["web_development"],
            ["data_science", "machine_learning"],
            ["automation", "general_programming"],
            []  # Empty list should be valid
        ]
        
        for goals in valid_goals:
            is_valid, error = test_validator.validate_learning_goals(goals)
            assert is_valid, f"Goals {goals} should be valid"
    
    def test_invalid_learning_goals(self, test_validator):
        """Test invalid learning goals"""
        invalid_goals = [
            "not_a_list",
            ["invalid_goal"],
            ["web_development"] * 15,  # Too many goals
            [123],  # Non-string goal
            ["web_development", "invalid_goal"]
        ]
        
        for goals in invalid_goals:
            is_valid, error = test_validator.validate_learning_goals(goals)
            assert not is_valid, f"Goals {goals} should be invalid"

class TestCodeValidation:
    """Test code validation"""
    
    def test_valid_code(self, test_validator):
        """Test valid Python code"""
        valid_code_samples = [
            "print('Hello, World!')",
            "x = 5\ny = 10\nprint(x + y)",
            "def hello():\n    return 'Hello'",
            "for i in range(5):\n    print(i)"
        ]
        
        for code in valid_code_samples:
            is_valid, error = test_validator.validate_user_code(code)
            assert is_valid, f"Code should be valid: {code}"
    
    def test_dangerous_code(self, test_validator):
        """Test dangerous code patterns"""
        dangerous_code_samples = [
            "import os",
            "import sys",
            "exec('malicious code')",
            "eval('dangerous')",
            "__import__('os')",
            "open('/etc/passwd')",
            "input('Enter password:')"
        ]
        
        for code in dangerous_code_samples:
            is_valid, error = test_validator.validate_user_code(code)
            assert not is_valid, f"Code should be rejected: {code}"
            assert "dangerous" in error.lower()
    
    def test_syntax_error_code(self, test_validator):
        """Test code with syntax errors"""
        syntax_error_code = [
            "print('unclosed string",
            "if True\n    print('missing colon')",
            "def function(\n    pass"
        ]
        
        for code in syntax_error_code:
            is_valid, error = test_validator.validate_user_code(code)
            assert not is_valid
            assert "syntax error" in error.lower()
    
    def test_code_length_limit(self, test_validator):
        """Test code length limits"""
        long_code = "print('hello')\n" * 1000  # Very long code
        is_valid, error = test_validator.validate_user_code(long_code)
        assert not is_valid
        assert "too long" in error.lower()

class TestQuizAnswerValidation:
    """Test quiz answer validation"""
    
    def test_valid_quiz_answers(self, test_validator):
        """Test valid quiz answers"""
        valid_answers = [
            {"question_1": "answer"},
            {"question_1": 1, "question_2": "text"},
            {"q1": ["option1", "option2"]},
            {"multiple_choice": 2}
        ]
        
        for answers in valid_answers:
            is_valid, error = test_validator.validate_quiz_answers(answers)
            assert is_valid, f"Answers should be valid: {answers}"
    
    def test_invalid_quiz_answers(self, test_validator):
        """Test invalid quiz answers"""
        invalid_answers = [
            "not_a_dict",
            {"invalid@id": "answer"},
            {"question_1": "x" * 2000},  # Too long answer
            {123: "answer"}  # Non-string question ID
        ]
        
        for answers in invalid_answers:
            is_valid, error = test_validator.validate_quiz_answers(answers)
            assert not is_valid, f"Answers should be invalid: {answers}"

class TestHTMLSanitization:
    """Test HTML sanitization"""
    
    def test_basic_sanitization(self, test_validator):
        """Test basic HTML sanitization"""
        # Test script tag removal
        script_input = "<script>alert('xss')</script>"
        sanitized = test_validator.sanitize_html(script_input)
        assert "<script>" not in sanitized

        # Test safe content preservation
        safe_input = "<p>Safe content</p>"
        sanitized = test_validator.sanitize_html(safe_input)
        assert "Safe content" in sanitized

        # Test javascript removal
        js_input = "javascript:alert('xss')"
        sanitized = test_validator.sanitize_html(js_input)
        assert "javascript:" not in sanitized

        # Test event handler removal
        event_input = "<img onerror='alert(1)' src='x'>"
        sanitized = test_validator.sanitize_html(event_input)
        assert "onerror" not in sanitized
    
    def test_preserve_safe_content(self, test_validator):
        """Test that safe content is preserved"""
        safe_content = "This is safe text with numbers 123 and symbols !@#"
        sanitized = test_validator.sanitize_html(safe_content)
        assert "safe text" in sanitized
        assert "123" in sanitized

class TestJSONValidation:
    """Test JSON validation"""
    
    def test_valid_json(self, test_validator):
        """Test valid JSON data"""
        valid_json_strings = [
            '{"key": "value"}',
            '{"number": 123, "boolean": true}',
            '[]',
            '{"nested": {"object": "value"}}'
        ]
        
        for json_str in valid_json_strings:
            is_valid, error, data = test_validator.validate_json_data(json_str)
            assert is_valid, f"JSON should be valid: {json_str}"
            assert data is not None
    
    def test_invalid_json(self, test_validator):
        """Test invalid JSON data"""
        invalid_json_strings = [
            '{"invalid": }',
            '{key: "value"}',  # Unquoted key
            "{'single': 'quotes'}",  # Single quotes
            '{"trailing": "comma",}'
        ]
        
        for json_str in invalid_json_strings:
            is_valid, error, data = test_validator.validate_json_data(json_str)
            assert not is_valid, f"JSON should be invalid: {json_str}"
            assert data is None
    
    def test_json_size_limit(self, test_validator):
        """Test JSON size limits"""
        large_json = '{"data": "' + 'x' * (2 * 1024 * 1024) + '"}'  # 2MB+ JSON
        is_valid, error, data = test_validator.validate_json_data(large_json)
        assert not is_valid
        assert "too large" in error.lower()

class TestRegistrationDataValidation:
    """Test complete registration data validation"""
    
    def test_valid_registration_data(self, test_validator):
        """Test valid registration data"""
        valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "experience_level": "complete_beginner",
            "learning_goals": ["web_development"]
        }
        
        is_valid, errors = test_validator.validate_registration_data(valid_data)
        assert is_valid
        assert len(errors) == 0
    
    def test_invalid_registration_data(self, test_validator):
        """Test invalid registration data"""
        invalid_data = {
            "name": "",  # Invalid name
            "email": "invalid-email",  # Invalid email
            "password": "123",  # Invalid password
            "experience_level": "invalid",  # Invalid level
            "learning_goals": ["invalid_goal"]  # Invalid goals
        }
        
        is_valid, errors = test_validator.validate_registration_data(invalid_data)
        assert not is_valid
        assert len(errors) > 0
        assert "name" in errors
        assert "email" in errors
        assert "password" in errors
        assert "experience_level" in errors
        assert "learning_goals" in errors
