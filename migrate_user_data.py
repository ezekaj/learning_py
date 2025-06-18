#!/usr/bin/env python3
"""
User Data Migration Script
Standardizes user data structure across all users
"""

import json
import os
from datetime import datetime

def migrate_user_data():
    """Migrate user data to standardized structure"""
    
    # Load current user data
    user_file = "data/user_progress.json"
    if not os.path.exists(user_file):
        print("No user data file found")
        return
    
    with open(user_file, 'r') as f:
        user_data = json.load(f)
    
    print(f"Found {len(user_data)} users to migrate")
    
    # Standard user structure
    standard_fields = {
        "name": "",
        "email": "",
        "password": "",
        "experience_level": "complete_beginner",
        "learning_goals": [],
        "created_at": "",
        "last_activity": "",
        "last_login": "",
        "lessons_completed": 0,
        "challenges_completed": 0,
        "quizzes_completed": 0,
        "quizzes_taken": 0,
        "projects_completed": 0,
        "playground_uses": 0,
        "points": 0,
        "level": 1,
        "streak": 0,
        "achievements": [],
        "average_quiz_score": 0.0,
        "total_study_time": 0,
        "days_since_start": 0,
        "completed_lesson_ids": [],
        "completed_challenge_ids": [],
        "completed_quiz_ids": [],
        "completed_project_ids": [],
        "notifications_enabled": True,
        "theme": "default",
        "language": "en"
    }
    
    migrated_count = 0
    
    for email, user in user_data.items():
        print(f"Migrating user: {email}")
        
        # Create new standardized user record
        new_user = standard_fields.copy()
        
        # Migrate existing fields
        new_user["name"] = user.get("name", "")
        new_user["email"] = email if "@" in email else user.get("email", "")
        new_user["password"] = user.get("password", "")
        new_user["experience_level"] = user.get("experience_level", "complete_beginner")
        new_user["learning_goals"] = user.get("learning_goals", [])
        
        # Handle date field inconsistency
        if "created_at" in user:
            new_user["created_at"] = user["created_at"]
        elif "created_date" in user:
            new_user["created_at"] = user["created_date"]
        else:
            new_user["created_at"] = datetime.now().isoformat()
        
        # Handle activity dates
        new_user["last_activity"] = user.get("last_activity", new_user["created_at"])
        new_user["last_login"] = user.get("last_login", new_user["created_at"])
        
        # Migrate progress data
        new_user["lessons_completed"] = user.get("lessons_completed", 0)
        new_user["challenges_completed"] = user.get("challenges_completed", 0)
        new_user["quizzes_completed"] = user.get("quizzes_completed", 0)
        new_user["quizzes_taken"] = user.get("quizzes_taken", 0)
        new_user["projects_completed"] = user.get("projects_completed", 0)
        new_user["playground_uses"] = user.get("playground_uses", 0)
        
        # Migrate scoring data
        new_user["points"] = user.get("points", 0)
        new_user["level"] = user.get("level", 1)
        new_user["streak"] = user.get("streak", 0)
        new_user["achievements"] = user.get("achievements", [])
        new_user["average_quiz_score"] = user.get("average_quiz_score", 0.0)
        new_user["total_study_time"] = user.get("total_study_time", 0)
        new_user["days_since_start"] = user.get("days_since_start", 0)
        
        # Migrate completion lists
        new_user["completed_lesson_ids"] = user.get("completed_lesson_ids", user.get("completed_lessons", []))
        new_user["completed_challenge_ids"] = user.get("completed_challenge_ids", user.get("completed_challenges", []))
        new_user["completed_quiz_ids"] = user.get("completed_quiz_ids", user.get("completed_quizzes", []))
        new_user["completed_project_ids"] = user.get("completed_project_ids", [])
        
        # Migrate preferences
        new_user["notifications_enabled"] = user.get("notifications_enabled", True)
        new_user["theme"] = user.get("theme", "default")
        new_user["language"] = user.get("language", "en")
        
        # Update user data
        user_data[email] = new_user
        migrated_count += 1
    
    # Create backup
    backup_file = f"data/user_progress_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_file, 'w') as f:
        json.dump(user_data, f, indent=2)
    
    print(f"Created backup: {backup_file}")
    
    # Save migrated data
    with open(user_file, 'w') as f:
        json.dump(user_data, f, indent=2)
    
    print(f"Successfully migrated {migrated_count} users")
    print("Migration completed!")

if __name__ == "__main__":
    migrate_user_data()
