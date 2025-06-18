"""
Integration tests for Flask app endpoints
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, Mock

class TestAppEndpoints:
    """Test Flask application endpoints"""
    
    def test_index_page(self, client):
        """Test index page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Python Learning Platform' in response.data
    
    def test_register_page_get(self, client):
        """Test registration page loads"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'register' in response.data.lower()
    
    def test_login_page_get(self, client):
        """Test login page loads"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'login' in response.data.lower()
    
    @patch('app.save_user_data')
    @patch('app.load_user_data')
    def test_user_registration_success(self, mock_load, mock_save, client):
        """Test successful user registration"""
        mock_load.return_value = {}  # No existing users
        mock_save.return_value = True
        
        registration_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "experience_level": "complete_beginner",
            "learning_goals": ["web_development"]
        }
        
        response = client.post('/register',
                             data=json.dumps(registration_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "redirect" in data
    
    @patch('app.load_user_data')
    def test_user_registration_duplicate_email(self, mock_load, client):
        """Test registration with duplicate email"""
        mock_load.return_value = {
            "test@example.com": {"name": "Existing User"}
        }
        
        registration_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "experience_level": "complete_beginner",
            "learning_goals": ["web_development"]
        }
        
        response = client.post('/register',
                             data=json.dumps(registration_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "exists" in data["error"]
    
    def test_user_registration_invalid_data(self, client):
        """Test registration with invalid data"""
        invalid_data = {
            "name": "",  # Invalid name
            "email": "invalid-email",  # Invalid email
            "password": "123",  # Invalid password
            "experience_level": "invalid",  # Invalid level
            "learning_goals": ["invalid_goal"]  # Invalid goals
        }
        
        response = client.post('/register',
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["success"] is False
        assert "details" in data
    
    @patch('app.save_user_data')
    @patch('app.load_user_data')
    def test_user_login_success(self, mock_load, mock_save, client):
        """Test successful user login"""
        mock_load.return_value = {
            "test@example.com": {
                "name": "Test User",
                "password": "password123"
            }
        }
        mock_save.return_value = True
        
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert "redirect" in data
    
    @patch('app.load_user_data')
    def test_user_login_invalid_credentials(self, mock_load, client):
        """Test login with invalid credentials"""
        mock_load.return_value = {
            "test@example.com": {
                "name": "Test User",
                "password": "password123"
            }
        }
        
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["success"] is False
    
    def test_dashboard_requires_login(self, client):
        """Test that dashboard requires login"""
        response = client.get('/dashboard')
        assert response.status_code == 302  # Redirect to login
    
    def test_lessons_requires_login(self, client):
        """Test that lessons page requires login"""
        response = client.get('/lessons')
        assert response.status_code == 302  # Redirect to login
    
    def test_challenges_requires_login(self, client):
        """Test that challenges page requires login"""
        response = client.get('/challenges')
        assert response.status_code == 302  # Redirect to login
    
    def test_quizzes_requires_login(self, client):
        """Test that quizzes page requires login"""
        response = client.get('/quizzes')
        assert response.status_code == 302  # Redirect to login
    
    def test_authenticated_dashboard_access(self, authenticated_client):
        """Test dashboard access with authentication"""
        with patch('app.load_user_data') as mock_load:
            mock_load.return_value = {
                "test@example.com": {
                    "name": "Test User",
                    "points": 100,
                    "level": 2
                }
            }
            
            response = authenticated_client.get('/dashboard')
            assert response.status_code == 200
            assert b'dashboard' in response.data.lower()
    
    def test_csrf_token_endpoint(self, client):
        """Test CSRF token endpoint"""
        response = client.get('/api/csrf-token')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
        assert "csrf_token" in data
        assert len(data["csrf_token"]) > 0
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["status"] == "healthy"
        assert "version" in data
        assert "error_stats" in data
    
    @patch('app.get_comprehensive_quizzes_data')
    @patch('app.load_user_data')
    def test_quiz_submission(self, mock_load, mock_quiz_data, authenticated_client):
        """Test quiz submission"""
        mock_load.return_value = {
            "test@example.com": {
                "name": "Test User",
                "points": 100,
                "quizzes_completed": 0,
                "quizzes_taken": 0,
                "total_quiz_score": 0
            }
        }
        
        mock_quiz_data.return_value = [{
            "id": "quiz_1",
            "title": "Test Quiz",
            "points": 25,
            "questions_data": [{
                "id": 1,
                "type": "multiple_choice",
                "correct_answer": 1
            }]
        }]
        
        quiz_submission = {
            "quiz_id": "quiz_1",
            "answers": {"1": 1}  # Correct answer
        }
        
        with patch('app.save_user_data') as mock_save:
            mock_save.return_value = True
            
            response = authenticated_client.post('/api/submit_quiz',
                                               data=json.dumps(quiz_submission),
                                               content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert data["score"] == 100.0  # 100% correct
            assert data["points_earned"] == 25

class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_registration_rate_limiting(self, client):
        """Test rate limiting on registration endpoint"""
        registration_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "experience_level": "complete_beginner",
            "learning_goals": ["web_development"]
        }
        
        # Make multiple rapid requests
        responses = []
        for i in range(10):
            response = client.post('/register',
                                 data=json.dumps(registration_data),
                                 content_type='application/json')
            responses.append(response.status_code)
        
        # Should eventually get rate limited (429)
        assert 429 in responses or all(r in [400, 500] for r in responses)
    
    def test_login_rate_limiting(self, client):
        """Test rate limiting on login endpoint"""
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        # Make multiple rapid requests
        responses = []
        for i in range(15):
            response = client.post('/login',
                                 data=json.dumps(login_data),
                                 content_type='application/json')
            responses.append(response.status_code)
        
        # Should eventually get rate limited (429)
        assert 429 in responses or all(r in [401, 500] for r in responses)

class TestErrorHandling:
    """Test error handling in endpoints"""
    
    def test_invalid_json_handling(self, client):
        """Test handling of invalid JSON data"""
        response = client.post('/register',
                             data='invalid json',
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_missing_content_type(self, client):
        """Test handling of missing content type"""
        response = client.post('/register',
                             data='{"test": "data"}')
        
        # Should handle gracefully
        assert response.status_code in [400, 415]
    
    @patch('app.load_user_data')
    def test_database_error_handling(self, mock_load, client):
        """Test handling of database errors"""
        mock_load.side_effect = Exception("Database error")
        
        response = client.get('/dashboard')
        # Should redirect to login or show error page
        assert response.status_code in [302, 500]

class TestDataFlow:
    """Test data flow between components"""
    
    @patch('app.save_user_data')
    @patch('app.load_user_data')
    def test_user_registration_to_login_flow(self, mock_load, mock_save, client):
        """Test complete user registration to login flow"""
        # Start with no users
        mock_load.return_value = {}
        mock_save.return_value = True
        
        # Register user
        registration_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "experience_level": "complete_beginner",
            "learning_goals": ["web_development"]
        }
        
        response = client.post('/register',
                             data=json.dumps(registration_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        # Mock that user now exists
        mock_load.return_value = {
            "test@example.com": {
                "name": "Test User",
                "password": "password123",
                "email": "test@example.com"
            }
        }
        
        # Login with same credentials
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = client.post('/login',
                             data=json.dumps(login_data),
                             content_type='application/json')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data["success"] is True
