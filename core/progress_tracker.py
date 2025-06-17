"""
Progress Tracker Module
Inspired by the best features from top GitHub repositories:
- Achievement system from gamification concepts
- Progress analytics from educational platforms
- Streak tracking from habit-building apps
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math

class ProgressTracker:
    """Track user progress, achievements, and learning analytics"""
    
    def __init__(self, user_data_file: str = "data/user_progress.json"):
        self.user_data_file = user_data_file
        self.achievements_file = "data/achievements.json"
        self.load_achievements_config()
    
    def load_achievements_config(self):
        """Load achievement configurations"""
        self.achievements_config = {
            "first_steps": {
                "name": "First Steps",
                "description": "Complete your first lesson",
                "icon": "🎯",
                "points": 10,
                "condition": {"type": "lessons_completed", "value": 1}
            },
            "week_warrior": {
                "name": "Week Warrior",
                "description": "Maintain a 7-day learning streak",
                "icon": "🔥",
                "points": 50,
                "condition": {"type": "streak", "value": 7}
            },
            "challenge_master": {
                "name": "Challenge Master",
                "description": "Complete 10 coding challenges",
                "icon": "⚔️",
                "points": 100,
                "condition": {"type": "challenges_completed", "value": 10}
            },
            "quiz_champion": {
                "name": "Quiz Champion",
                "description": "Score 100% on 5 quizzes",
                "icon": "🏆",
                "points": 75,
                "condition": {"type": "perfect_quizzes", "value": 5}
            },
            "python_novice": {
                "name": "Python Novice",
                "description": "Complete beginner level",
                "icon": "🐍",
                "points": 200,
                "condition": {"type": "level_completed", "value": "beginner"}
            },
            "code_explorer": {
                "name": "Code Explorer",
                "description": "Use code playground 20 times",
                "icon": "🧪",
                "points": 30,
                "condition": {"type": "playground_uses", "value": 20}
            },
            "project_builder": {
                "name": "Project Builder",
                "description": "Complete your first project",
                "icon": "🚀",
                "points": 150,
                "condition": {"type": "projects_completed", "value": 1}
            },
            "consistency_king": {
                "name": "Consistency King",
                "description": "Learn for 30 consecutive days",
                "icon": "👑",
                "points": 300,
                "condition": {"type": "streak", "value": 30}
            }
        }
    
    def update_progress(self, user_name: str, activity_type: str, details: Dict = None):
        """Update user progress for various activities"""
        user_data = self.load_user_data()
        
        if user_name not in user_data:
            return False
        
        user_profile = user_data[user_name]
        current_time = datetime.now().isoformat()
        
        # Update last activity
        user_profile["last_activity"] = current_time
        
        # Handle different activity types
        if activity_type == "lesson_completed":
            lesson_id = details.get("lesson_id")
            if lesson_id not in user_profile.get("completed_lessons", []):
                user_profile.setdefault("completed_lessons", []).append(lesson_id)
                user_profile["points"] = user_profile.get("points", 0) + 10
                self.update_streak(user_profile)
        
        elif activity_type == "challenge_completed":
            challenge_id = details.get("challenge_id")
            difficulty = details.get("difficulty", "easy")
            points_map = {"easy": 15, "medium": 25, "hard": 40}
            
            if challenge_id not in user_profile.get("completed_challenges", []):
                user_profile.setdefault("completed_challenges", []).append(challenge_id)
                user_profile["points"] = user_profile.get("points", 0) + points_map.get(difficulty, 15)
                self.update_streak(user_profile)
        
        elif activity_type == "quiz_completed":
            quiz_id = details.get("quiz_id")
            score = details.get("score", 0)
            max_score = details.get("max_score", 100)
            
            quiz_record = {
                "quiz_id": quiz_id,
                "score": score,
                "max_score": max_score,
                "percentage": (score / max_score) * 100 if max_score > 0 else 0,
                "date": current_time
            }
            
            user_profile.setdefault("quiz_history", []).append(quiz_record)
            
            # Award points based on score
            points = math.ceil((score / max_score) * 20) if max_score > 0 else 0
            user_profile["points"] = user_profile.get("points", 0) + points
            
            # Track perfect scores
            if score == max_score:
                user_profile.setdefault("perfect_quizzes", 0)
                user_profile["perfect_quizzes"] += 1
        
        elif activity_type == "playground_used":
            user_profile.setdefault("playground_uses", 0)
            user_profile["playground_uses"] += 1
            user_profile["points"] = user_profile.get("points", 0) + 1
        
        elif activity_type == "project_completed":
            project_id = details.get("project_id")
            if project_id not in user_profile.get("completed_projects", []):
                user_profile.setdefault("completed_projects", []).append(project_id)
                user_profile["points"] = user_profile.get("points", 0) + 100
                self.update_streak(user_profile)
        
        # Check for new achievements
        self.check_achievements(user_profile)
        
        # Save updated data
        self.save_user_data(user_data)
        return True
    
    def update_streak(self, user_profile: Dict):
        """Update user's learning streak"""
        last_activity = user_profile.get("last_activity")
        if not last_activity:
            user_profile["streak"] = 1
            user_profile["last_streak_date"] = datetime.now().date().isoformat()
            return
        
        last_streak_date = user_profile.get("last_streak_date")
        today = datetime.now().date()
        
        if last_streak_date:
            last_date = datetime.fromisoformat(last_streak_date).date()
            days_diff = (today - last_date).days
            
            if days_diff == 1:
                # Consecutive day
                user_profile["streak"] = user_profile.get("streak", 0) + 1
            elif days_diff > 1:
                # Streak broken
                user_profile["streak"] = 1
            # If days_diff == 0, same day, don't change streak
        else:
            user_profile["streak"] = 1
        
        user_profile["last_streak_date"] = today.isoformat()
    
    def check_achievements(self, user_profile: Dict):
        """Check and award new achievements"""
        current_achievements = set(user_profile.get("achievements", []))
        new_achievements = []
        
        for achievement_id, config in self.achievements_config.items():
            if achievement_id in current_achievements:
                continue
            
            condition = config["condition"]
            condition_type = condition["type"]
            required_value = condition["value"]
            
            achieved = False
            
            if condition_type == "lessons_completed":
                achieved = len(user_profile.get("completed_lessons", [])) >= required_value
            elif condition_type == "challenges_completed":
                achieved = len(user_profile.get("completed_challenges", [])) >= required_value
            elif condition_type == "streak":
                achieved = user_profile.get("streak", 0) >= required_value
            elif condition_type == "perfect_quizzes":
                achieved = user_profile.get("perfect_quizzes", 0) >= required_value
            elif condition_type == "playground_uses":
                achieved = user_profile.get("playground_uses", 0) >= required_value
            elif condition_type == "projects_completed":
                achieved = len(user_profile.get("completed_projects", [])) >= required_value
            elif condition_type == "level_completed":
                # This would need more complex logic based on lesson structure
                pass
            
            if achieved:
                new_achievements.append(achievement_id)
                user_profile.setdefault("achievements", []).append(achievement_id)
                user_profile["points"] = user_profile.get("points", 0) + config["points"]
        
        return new_achievements
    
    def get_progress_stats(self, user_name: str) -> Dict:
        """Get comprehensive progress statistics"""
        user_data = self.load_user_data()
        
        if user_name not in user_data:
            return {}
        
        user_profile = user_data[user_name]
        
        # Calculate level based on points
        points = user_profile.get("points", 0)
        level = self.calculate_level(points)
        
        # Calculate completion percentages
        total_lessons = 100  # This would be dynamic based on actual lesson count
        completed_lessons = len(user_profile.get("completed_lessons", []))
        lesson_completion = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        
        # Quiz statistics
        quiz_history = user_profile.get("quiz_history", [])
        avg_quiz_score = 0
        if quiz_history:
            total_percentage = sum(quiz["percentage"] for quiz in quiz_history)
            avg_quiz_score = total_percentage / len(quiz_history)
        
        return {
            "level": level,
            "points": points,
            "points_to_next_level": self.points_for_level(level + 1) - points,
            "streak": user_profile.get("streak", 0),
            "lessons_completed": completed_lessons,
            "lesson_completion_percentage": lesson_completion,
            "challenges_completed": len(user_profile.get("completed_challenges", [])),
            "projects_completed": len(user_profile.get("completed_projects", [])),
            "quizzes_taken": len(quiz_history),
            "average_quiz_score": avg_quiz_score,
            "perfect_quizzes": user_profile.get("perfect_quizzes", 0),
            "playground_uses": user_profile.get("playground_uses", 0),
            "achievements_count": len(user_profile.get("achievements", [])),
            "days_since_start": self.calculate_days_since_start(user_profile.get("created_date"))
        }
    
    def calculate_level(self, points: int) -> int:
        """Calculate user level based on points"""
        # Level progression: 0, 100, 250, 450, 700, 1000, 1350, 1750, 2200, 2700, 3250...
        level = 1
        while points >= self.points_for_level(level + 1):
            level += 1
        return level
    
    def points_for_level(self, level: int) -> int:
        """Calculate points required for a specific level"""
        if level <= 1:
            return 0
        # Exponential growth: level^2 * 50 - 50
        return (level - 1) ** 2 * 50
    
    def calculate_days_since_start(self, created_date: str) -> int:
        """Calculate days since user started"""
        if not created_date:
            return 0
        
        start_date = datetime.fromisoformat(created_date).date()
        today = datetime.now().date()
        return (today - start_date).days
    
    def get_leaderboard(self, limit: int = 10) -> List[Dict]:
        """Get top users leaderboard"""
        user_data = self.load_user_data()
        
        leaderboard = []
        for user_name, profile in user_data.items():
            leaderboard.append({
                "name": user_name,
                "points": profile.get("points", 0),
                "level": self.calculate_level(profile.get("points", 0)),
                "streak": profile.get("streak", 0),
                "lessons_completed": len(profile.get("completed_lessons", [])),
                "achievements": len(profile.get("achievements", []))
            })
        
        # Sort by points (descending)
        leaderboard.sort(key=lambda x: x["points"], reverse=True)
        
        return leaderboard[:limit]
    
    def load_user_data(self) -> Dict:
        """Load user data from file"""
        try:
            if os.path.exists(self.user_data_file):
                with open(self.user_data_file, 'r') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}
    
    def save_user_data(self, user_data: Dict):
        """Save user data to file"""
        try:
            os.makedirs(os.path.dirname(self.user_data_file), exist_ok=True)
            with open(self.user_data_file, 'w') as f:
                json.dump(user_data, f, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")
