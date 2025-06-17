#!/usr/bin/env python3
"""
Data Migration and Standardization for Python Learning Platform
Migrates legacy user data to standardized schema
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class UserDataMigration:
    """Handles migration of user data to standardized format"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.user_data_file = os.path.join(data_dir, "user_progress.json")
        self.backup_dir = os.path.join(data_dir, "backups")
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_standardized_user_profile(self, name: str, email: str, password: str = "",
                                       experience_level: str = "complete_beginner",
                                       learning_goals: List[str] = None) -> Dict[str, Any]:
        """Create a standardized user profile"""
        if learning_goals is None:
            learning_goals = []
            
        return {
            # Basic Information
            "name": name,
            "email": email,
            "password": password,
            "experience_level": experience_level,
            "learning_goals": learning_goals,
            
            # Timestamps (standardized to created_at)
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
            
            # Progress Tracking (standardized names)
            "lessons_completed": 0,
            "challenges_completed": 0,
            "quizzes_completed": 0,
            "quizzes_taken": 0,
            "projects_completed": 0,
            "playground_uses": 0,
            
            # Gamification
            "points": 0,
            "level": 1,
            "streak": 0,
            "achievements": [],
            
            # Performance Metrics
            "average_quiz_score": 0.0,
            "total_study_time": 0,
            "days_since_start": 0,
            
            # Detailed Progress (arrays of IDs)
            "completed_lesson_ids": [],
            "completed_challenge_ids": [],
            "completed_quiz_ids": [],
            "completed_project_ids": [],
            
            # Settings and Preferences
            "notifications_enabled": True,
            "theme": "default",
            "language": "en"
        }
    
    def migrate_legacy_profile(self, user_key: str, legacy_profile: Dict[str, Any]) -> Dict[str, Any]:
        """Migrate a legacy user profile to standardized format"""
        # Extract basic info
        name = legacy_profile.get("name", "Unknown User")
        email = legacy_profile.get("email", user_key if "@" in user_key else "")
        password = legacy_profile.get("password", "")
        experience_level = legacy_profile.get("experience_level", "complete_beginner")
        learning_goals = legacy_profile.get("learning_goals", [])
        
        # Create new standardized profile
        new_profile = self.create_standardized_user_profile(
            name=name,
            email=email,
            password=password,
            experience_level=experience_level,
            learning_goals=learning_goals
        )
        
        # Migrate timestamps
        timestamp_mappings = {
            "created_date": "created_at",
            "created_at": "created_at",
            "last_activity": "last_activity"
        }
        
        for old_field, new_field in timestamp_mappings.items():
            if old_field in legacy_profile:
                new_profile[new_field] = legacy_profile[old_field]
        
        # Migrate progress data
        progress_mappings = {
            "lessons_completed": "lessons_completed",
            "challenges_completed": "challenges_completed", 
            "quizzes_completed": "quizzes_completed",
            "quizzes_taken": "quizzes_taken",
            "playground_uses": "playground_uses",
            "points": "points",
            "level": "level",
            "streak": "streak",
            "achievements": "achievements",
            "average_quiz_score": "average_quiz_score",
            "days_since_start": "days_since_start"
        }
        
        for old_field, new_field in progress_mappings.items():
            if old_field in legacy_profile:
                new_profile[new_field] = legacy_profile[old_field]
        
        # Migrate arrays (convert old format to new)
        array_mappings = {
            "completed_lessons": "completed_lesson_ids",
            "completed_challenges": "completed_challenge_ids",
            "completed_quizzes": "completed_quiz_ids"
        }
        
        for old_field, new_field in array_mappings.items():
            if old_field in legacy_profile:
                new_profile[new_field] = legacy_profile[old_field]
        
        # Set current day if missing
        if "current_day" in legacy_profile:
            # Convert current_day to days_since_start if not already set
            if new_profile["days_since_start"] == 0:
                new_profile["days_since_start"] = legacy_profile["current_day"]
        
        return new_profile
    
    def load_user_data(self) -> Dict[str, Any]:
        """Load current user data"""
        try:
            if os.path.exists(self.user_data_file):
                with open(self.user_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading user data: {e}")
        return {}
    
    def save_user_data(self, data: Dict[str, Any]) -> bool:
        """Save user data with backup"""
        try:
            # Create backup first
            self.create_backup()
            
            # Save new data
            os.makedirs(self.data_dir, exist_ok=True)
            with open(self.user_data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving user data: {e}")
            return False
    
    def create_backup(self) -> bool:
        """Create backup of current user data"""
        try:
            if os.path.exists(self.user_data_file):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_file = os.path.join(self.backup_dir, f"user_progress_backup_{timestamp}.json")
                
                with open(self.user_data_file, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                print(f"Backup created: {backup_file}")
                return True
        except Exception as e:
            print(f"Error creating backup: {e}")
        return False
    
    def validate_profile(self, profile: Dict[str, Any]) -> bool:
        """Validate if profile follows standardized schema"""
        required_fields = [
            "name", "email", "experience_level", "created_at",
            "lessons_completed", "points", "level", "achievements",
            "completed_lesson_ids", "completed_challenge_ids"
        ]
        
        for field in required_fields:
            if field not in profile:
                return False
        
        return True
    
    def migrate_all_users(self) -> bool:
        """Migrate all user data to standardized format"""
        try:
            print("Starting user data migration...")
            
            # Load current data
            user_data = self.load_user_data()
            migrated_data = {}
            migration_count = 0
            
            for user_key, profile in user_data.items():
                if not self.validate_profile(profile):
                    print(f"Migrating user: {user_key}")
                    migrated_data[user_key] = self.migrate_legacy_profile(user_key, profile)
                    migration_count += 1
                else:
                    print(f"User already standardized: {user_key}")
                    migrated_data[user_key] = profile
            
            # Save migrated data
            if self.save_user_data(migrated_data):
                print(f"Migration completed successfully! Migrated {migration_count} users.")
                return True
            else:
                print("Failed to save migrated data")
                return False
                
        except Exception as e:
            print(f"Error during migration: {e}")
            return False
    
    def get_migration_report(self) -> Dict[str, Any]:
        """Generate a report of the current data state"""
        user_data = self.load_user_data()
        
        report = {
            "total_users": len(user_data),
            "standardized_users": 0,
            "legacy_users": 0,
            "users_needing_migration": [],
            "data_inconsistencies": []
        }
        
        for user_key, profile in user_data.items():
            if self.validate_profile(profile):
                report["standardized_users"] += 1
            else:
                report["legacy_users"] += 1
                report["users_needing_migration"].append(user_key)
                
                # Check for specific inconsistencies
                inconsistencies = []
                if "created_date" in profile and "created_at" not in profile:
                    inconsistencies.append("timestamp_format")
                if "completed_lessons" in profile and "completed_lesson_ids" not in profile:
                    inconsistencies.append("array_format")
                
                if inconsistencies:
                    report["data_inconsistencies"].append({
                        "user": user_key,
                        "issues": inconsistencies
                    })
        
        return report

def run_migration():
    """Run the data migration process"""
    migration = UserDataMigration()
    
    print("=== Python Learning Platform Data Migration ===")
    print()
    
    # Generate report
    report = migration.get_migration_report()
    print(f"Total users: {report['total_users']}")
    print(f"Standardized users: {report['standardized_users']}")
    print(f"Legacy users needing migration: {report['legacy_users']}")
    print()
    
    if report['legacy_users'] > 0:
        print("Users needing migration:")
        for user in report['users_needing_migration']:
            print(f"  - {user}")
        print()
        
        # Ask for confirmation
        response = input("Proceed with migration? (y/N): ").strip().lower()
        if response == 'y':
            success = migration.migrate_all_users()
            if success:
                print("\n✅ Migration completed successfully!")
            else:
                print("\n❌ Migration failed!")
        else:
            print("Migration cancelled.")
    else:
        print("✅ All users are already using the standardized format!")

if __name__ == "__main__":
    run_migration()
