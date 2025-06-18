"""
Unit tests for progress tracking system
"""

import pytest
import json
import os
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

from core.progress_tracker import ProgressTracker

class TestProgressTracker:
    """Test the ProgressTracker class"""
    
    def test_initialization(self, temp_dir):
        """Test progress tracker initialization"""
        user_data_file = os.path.join(temp_dir, "test_progress.json")
        tracker = ProgressTracker(user_data_file=user_data_file)
        
        assert tracker.user_data_file == user_data_file
        assert isinstance(tracker.achievements, dict)
        assert len(tracker.achievements) > 0
    
    def test_calculate_level(self, test_progress_tracker):
        """Test level calculation"""
        test_cases = [
            (0, 1),      # 0 points = level 1
            (100, 2),    # 100 points = level 2
            (300, 3),    # 300 points = level 3
            (600, 4),    # 600 points = level 4
            (1000, 5),   # 1000 points = level 5
            (2500, 7)    # 2500 points = level 7
        ]
        
        for points, expected_level in test_cases:
            level = test_progress_tracker.calculate_level(points)
            assert level == expected_level, f"Points {points} should give level {expected_level}, got {level}"
    
    def test_calculate_points_for_level(self, test_progress_tracker):
        """Test points calculation for level"""
        test_cases = [
            (1, 0),      # Level 1 = 0 points
            (2, 100),    # Level 2 = 100 points
            (3, 300),    # Level 3 = 300 points
            (4, 600),    # Level 4 = 600 points
            (5, 1000)    # Level 5 = 1000 points
        ]
        
        for level, expected_points in test_cases:
            points = test_progress_tracker.calculate_points_for_level(level)
            assert points == expected_points, f"Level {level} should require {expected_points} points, got {points}"
    
    def test_update_user_progress(self, test_progress_tracker, sample_user_data):
        """Test updating user progress"""
        # Save sample data first
        test_progress_tracker.save_user_data(sample_user_data)
        
        # Update progress
        email = "test@example.com"
        progress_data = {
            "lessons_completed": 10,
            "points_earned": 50,
            "achievements": ["new_achievement"]
        }
        
        result = test_progress_tracker.update_user_progress(email, progress_data)
        assert result is True
        
        # Verify update
        user_data = test_progress_tracker.load_user_data()
        user = user_data[email]
        assert user["lessons_completed"] == 10
        assert user["points"] >= 200  # Original 150 + 50
    
    def test_check_achievements(self, test_progress_tracker):
        """Test achievement checking"""
        user_stats = {
            "lessons_completed": 1,
            "challenges_completed": 0,
            "quizzes_completed": 0,
            "streak": 1,
            "points": 10,
            "level": 1
        }
        
        new_achievements = test_progress_tracker.check_achievements(user_stats, [])
        
        # Should get "first_steps" achievement
        assert "first_steps" in new_achievements
    
    def test_streak_calculation(self, test_progress_tracker):
        """Test streak calculation"""
        # Test consecutive days
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        # User active today and yesterday
        last_activity = yesterday.isoformat()
        streak = test_progress_tracker.calculate_streak(last_activity, current_streak=5)
        assert streak == 6  # Streak should increase
        
        # User not active for 2 days
        two_days_ago = today - timedelta(days=2)
        last_activity = two_days_ago.isoformat()
        streak = test_progress_tracker.calculate_streak(last_activity, current_streak=5)
        assert streak == 1  # Streak should reset
    
    def test_get_user_stats(self, test_progress_tracker, sample_user_data):
        """Test getting user statistics"""
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        email = "test@example.com"
        stats = test_progress_tracker.get_user_stats(email)
        
        assert stats is not None
        assert stats["lessons_completed"] == 5
        assert stats["points"] == 150
        assert stats["level"] == 2
        assert "progress_percentage" in stats
        assert "next_level_points" in stats
    
    def test_get_leaderboard(self, test_progress_tracker, sample_user_data):
        """Test leaderboard generation"""
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        leaderboard = test_progress_tracker.get_leaderboard(limit=10)
        
        assert len(leaderboard) <= 10
        assert len(leaderboard) == 2  # We have 2 users in sample data
        
        # Should be sorted by points (descending)
        if len(leaderboard) > 1:
            assert leaderboard[0]["points"] >= leaderboard[1]["points"]
    
    def test_get_progress_analytics(self, test_progress_tracker, sample_user_data):
        """Test progress analytics"""
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        email = "test@example.com"
        analytics = test_progress_tracker.get_progress_analytics(email)
        
        assert analytics is not None
        assert "learning_velocity" in analytics
        assert "completion_rate" in analytics
        assert "strength_areas" in analytics
        assert "improvement_areas" in analytics
    
    def test_achievement_definitions(self, test_progress_tracker):
        """Test achievement definitions"""
        achievements = test_progress_tracker.achievements
        
        # Check that all achievements have required fields
        for achievement_id, achievement in achievements.items():
            assert "name" in achievement
            assert "description" in achievement
            assert "condition" in achievement
            assert "points" in achievement
            assert "icon" in achievement
    
    def test_achievement_conditions(self, test_progress_tracker):
        """Test specific achievement conditions"""
        # Test first_steps achievement
        user_stats = {"lessons_completed": 1}
        condition = test_progress_tracker.achievements["first_steps"]["condition"]
        assert condition(user_stats, [])
        
        # Test week_warrior achievement
        user_stats = {"streak": 7}
        condition = test_progress_tracker.achievements["week_warrior"]["condition"]
        assert condition(user_stats, [])
        
        # Test challenge_master achievement
        user_stats = {"challenges_completed": 10}
        condition = test_progress_tracker.achievements["challenge_master"]["condition"]
        assert condition(user_stats, [])
    
    def test_level_progression(self, test_progress_tracker):
        """Test level progression system"""
        # Test that levels require increasing points
        previous_points = 0
        for level in range(1, 11):
            points = test_progress_tracker.calculate_points_for_level(level)
            assert points >= previous_points
            previous_points = points
    
    def test_user_data_persistence(self, test_progress_tracker, sample_user_data):
        """Test user data persistence"""
        # Save data
        success = test_progress_tracker.save_user_data(sample_user_data)
        assert success
        
        # Load data
        loaded_data = test_progress_tracker.load_user_data()
        assert loaded_data == sample_user_data
    
    def test_invalid_user_operations(self, test_progress_tracker):
        """Test operations with invalid users"""
        # Try to get stats for non-existent user
        stats = test_progress_tracker.get_user_stats("nonexistent@example.com")
        assert stats is None
        
        # Try to update progress for non-existent user
        result = test_progress_tracker.update_user_progress(
            "nonexistent@example.com", 
            {"points_earned": 10}
        )
        assert result is False
    
    def test_progress_calculation_edge_cases(self, test_progress_tracker):
        """Test edge cases in progress calculation"""
        # Test with zero values
        level = test_progress_tracker.calculate_level(0)
        assert level == 1
        
        # Test with very high points
        level = test_progress_tracker.calculate_level(100000)
        assert level > 10
        
        # Test negative points (should not happen but handle gracefully)
        level = test_progress_tracker.calculate_level(-100)
        assert level == 1

class TestProgressAnalytics:
    """Test progress analytics functionality"""
    
    def test_learning_velocity_calculation(self, test_progress_tracker, sample_user_data):
        """Test learning velocity calculation"""
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        email = "test@example.com"
        analytics = test_progress_tracker.get_progress_analytics(email)
        
        velocity = analytics["learning_velocity"]
        assert "lessons_per_day" in velocity
        assert "points_per_day" in velocity
        assert velocity["lessons_per_day"] >= 0
        assert velocity["points_per_day"] >= 0
    
    def test_completion_rate_calculation(self, test_progress_tracker, sample_user_data):
        """Test completion rate calculation"""
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        email = "test@example.com"
        analytics = test_progress_tracker.get_progress_analytics(email)
        
        completion_rate = analytics["completion_rate"]
        assert "lessons" in completion_rate
        assert "challenges" in completion_rate
        assert "quizzes" in completion_rate
        
        # All rates should be between 0 and 100
        for rate in completion_rate.values():
            assert 0 <= rate <= 100
    
    def test_strength_and_improvement_areas(self, test_progress_tracker, sample_user_data):
        """Test strength and improvement area identification"""
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        email = "test@example.com"
        analytics = test_progress_tracker.get_progress_analytics(email)
        
        strength_areas = analytics["strength_areas"]
        improvement_areas = analytics["improvement_areas"]
        
        assert isinstance(strength_areas, list)
        assert isinstance(improvement_areas, list)
        
        # Should have at least one area in each category
        assert len(strength_areas) > 0 or len(improvement_areas) > 0

class TestProgressTrackerIntegration:
    """Test progress tracker integration with other systems"""
    
    def test_achievement_point_rewards(self, test_progress_tracker):
        """Test that achievements give appropriate point rewards"""
        user_stats = {"lessons_completed": 1}
        new_achievements = test_progress_tracker.check_achievements(user_stats, [])
        
        total_achievement_points = sum(
            test_progress_tracker.achievements[achievement]["points"]
            for achievement in new_achievements
        )
        
        assert total_achievement_points > 0
    
    def test_level_up_detection(self, test_progress_tracker, sample_user_data):
        """Test level up detection"""
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        email = "test@example.com"
        user_data = test_progress_tracker.load_user_data()
        current_level = user_data[email]["level"]
        
        # Add enough points to level up
        progress_data = {"points_earned": 500}
        test_progress_tracker.update_user_progress(email, progress_data)
        
        # Check if level increased
        updated_data = test_progress_tracker.load_user_data()
        new_level = updated_data[email]["level"]
        
        assert new_level >= current_level
    
    @patch('core.progress_tracker.datetime')
    def test_daily_activity_tracking(self, mock_datetime, test_progress_tracker, sample_user_data):
        """Test daily activity tracking"""
        # Mock current time
        mock_now = datetime(2023, 12, 1, 12, 0, 0)
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        
        # Save sample data
        test_progress_tracker.save_user_data(sample_user_data)
        
        email = "test@example.com"
        progress_data = {"lessons_completed": 1}
        
        test_progress_tracker.update_user_progress(email, progress_data)
        
        # Check that last_activity was updated
        user_data = test_progress_tracker.load_user_data()
        user = user_data[email]
        
        assert "last_activity" in user
        # Should be updated to current time (mocked)
        assert user["last_activity"].startswith("2023-12-01")
