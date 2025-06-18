"""
Pytest configuration and fixtures for Python Learning Platform tests
"""

import pytest
import tempfile
import shutil
import os
import json
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

# Add the project root to Python path
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.error_handler import ErrorHandler
from core.validators import InputValidator
from core.database_manager import DatabaseManager
from core.progress_tracker import ProgressTracker

@pytest.fixture(scope="session")
def app():
    """Create Flask app for testing"""
    import app as flask_app
    
    # Configure for testing
    flask_app.app.config['TESTING'] = True
    flask_app.app.config['WTF_CSRF_ENABLED'] = False
    flask_app.app.config['SECRET_KEY'] = 'test-secret-key'
    
    return flask_app.app

@pytest.fixture(scope="function")
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture(scope="function")
def temp_dir():
    """Create temporary directory for tests"""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture(scope="function")
def test_error_handler(temp_dir):
    """Create error handler for testing"""
    return ErrorHandler(log_dir=temp_dir)

@pytest.fixture(scope="function")
def test_validator():
    """Create validator for testing"""
    return InputValidator()

@pytest.fixture(scope="function")
def test_db_manager(temp_dir):
    """Create database manager for testing"""
    return DatabaseManager(data_dir=temp_dir)

@pytest.fixture(scope="function")
def test_progress_tracker(temp_dir):
    """Create progress tracker for testing"""
    user_data_file = os.path.join(temp_dir, "user_progress.json")
    return ProgressTracker(user_data_file=user_data_file)

@pytest.fixture(scope="function")
def sample_user_data():
    """Sample user data for testing"""
    return {
        "test@example.com": {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "experience_level": "complete_beginner",
            "learning_goals": ["web_development"],
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "lessons_completed": 5,
            "challenges_completed": 3,
            "quizzes_completed": 2,
            "points": 150,
            "level": 2,
            "streak": 7,
            "achievements": ["first_steps", "week_warrior"],
            "completed_lesson_ids": ["lesson_1", "lesson_2", "lesson_3"],
            "completed_challenge_ids": ["challenge_1", "challenge_2"],
            "completed_quiz_ids": ["quiz_1"]
        },
        "advanced@example.com": {
            "name": "Advanced User",
            "email": "advanced@example.com",
            "password": "advanced123",
            "experience_level": "advanced",
            "learning_goals": ["machine_learning", "data_science"],
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "lessons_completed": 25,
            "challenges_completed": 15,
            "quizzes_completed": 12,
            "points": 850,
            "level": 5,
            "streak": 15,
            "achievements": ["first_steps", "week_warrior", "challenge_master"],
            "completed_lesson_ids": [f"lesson_{i}" for i in range(1, 26)],
            "completed_challenge_ids": [f"challenge_{i}" for i in range(1, 16)],
            "completed_quiz_ids": [f"quiz_{i}" for i in range(1, 13)]
        }
    }

@pytest.fixture(scope="function")
def sample_lesson_data():
    """Sample lesson data for testing"""
    return [
        {
            "id": "lesson_1",
            "title": "Introduction to Python",
            "description": "Learn Python basics",
            "difficulty": "beginner",
            "category": "fundamentals",
            "estimated_time": 30,
            "points": 10,
            "exercises": 5,
            "objectives": ["Understand Python syntax", "Write first program"]
        },
        {
            "id": "lesson_2", 
            "title": "Variables and Data Types",
            "description": "Master Python variables",
            "difficulty": "beginner",
            "category": "fundamentals",
            "estimated_time": 45,
            "points": 15,
            "exercises": 8,
            "objectives": ["Use variables", "Understand data types"]
        }
    ]

@pytest.fixture(scope="function")
def sample_quiz_data():
    """Sample quiz data for testing"""
    return [
        {
            "id": "quiz_1",
            "title": "Python Basics Quiz",
            "description": "Test your Python knowledge",
            "difficulty": "beginner",
            "category": "fundamentals",
            "questions": 5,
            "points": 25,
            "questions_data": [
                {
                    "id": 1,
                    "type": "multiple_choice",
                    "question": "What is Python?",
                    "options": ["A snake", "A programming language", "A game", "A book"],
                    "correct_answer": 1,
                    "explanation": "Python is a programming language"
                }
            ]
        }
    ]

@pytest.fixture(scope="function")
def sample_challenge_data():
    """Sample challenge data for testing"""
    return [
        {
            "id": "challenge_1",
            "title": "Hello World Challenge",
            "description": "Write a Hello World program",
            "difficulty": "easy",
            "category": "fundamentals",
            "points": 20,
            "function_name": "hello_world",
            "test_cases": [
                {
                    "input": [],
                    "expected_output": "Hello, World!",
                    "description": "Basic hello world"
                }
            ]
        }
    ]

@pytest.fixture(scope="function")
def mock_session():
    """Mock Flask session for testing"""
    with patch('flask.session') as mock_session:
        mock_session.__getitem__ = Mock(side_effect=lambda key: {
            'user': 'test@example.com'
        }.get(key))
        mock_session.__setitem__ = Mock()
        mock_session.__contains__ = Mock(return_value=True)
        mock_session.get = Mock(side_effect=lambda key, default=None: {
            'user': 'test@example.com'
        }.get(key, default))
        yield mock_session

@pytest.fixture(scope="function")
def authenticated_client(client, mock_session):
    """Client with authenticated session"""
    with client.session_transaction() as sess:
        sess['user'] = 'test@example.com'
    return client

@pytest.fixture(autouse=True)
def cleanup_test_files():
    """Cleanup test files after each test"""
    yield
    # Clean up any test files that might have been created
    test_files = [
        "test_user_progress.json",
        "test_data.json",
        "test_backup.json"
    ]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)

# Custom markers for test categorization
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.slow = pytest.mark.slow
pytest.mark.security = pytest.mark.security
pytest.mark.performance = pytest.mark.performance
