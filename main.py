#!/usr/bin/env python3
"""
Python Learning Program - From Beginner to Expert
Inspired by the best features from top-rated GitHub repositories:
- 30-Days-Of-Python (46.9k stars): Structured progression
- Interactive-Tutorials (4.3k stars): Interactive execution
- Python Practice repos: Coding challenges
- Exercism: Test-driven approach

Author: AI Assistant
Version: 1.0
"""

import os
import json
import time
from datetime import datetime
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored output
colorama.init()

class PythonLearningProgram:
    """Main class for the Python Learning Program"""
    
    def __init__(self):
        self.current_user = None
        self.user_data_file = "data/user_progress.json"
        self.lessons_data_file = "data/lessons.json"
        self.ensure_data_directories()
        self.load_user_data()
        
    def ensure_data_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            "data", "data/lessons", "data/quizzes", "data/exercises", 
            "data/projects", "modules", "modules/beginner", 
            "modules/intermediate", "modules/advanced", "modules/expert",
            "core", "utils", "tests"
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def load_user_data(self):
        """Load user progress data"""
        try:
            if os.path.exists(self.user_data_file):
                with open(self.user_data_file, 'r') as f:
                    self.user_data = json.load(f)
            else:
                self.user_data = {}
        except Exception as e:
            print(f"Error loading user data: {e}")
            self.user_data = {}
    
    def save_user_data(self):
        """Save user progress data"""
        try:
            with open(self.user_data_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except Exception as e:
            print(f"Error saving user data: {e}")
    
    def display_banner(self):
        """Display the program banner"""
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗
║                    🐍 PYTHON LEARNING PROGRAM 🐍                            ║
║                        From Beginner to Expert                              ║
║                                                                              ║
║  📚 Structured Learning Path    🎯 Interactive Challenges                   ║
║  🏆 Achievement System          💡 Real-world Projects                      ║
║  📊 Progress Tracking           🤝 Community Features                       ║
╚══════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)
    
    def display_main_menu(self):
        """Display the main menu"""
        menu = f"""
{Fore.GREEN}🎯 MAIN MENU{Style.RESET_ALL}
{Fore.YELLOW}1.{Style.RESET_ALL} 📖 Start Learning Journey
{Fore.YELLOW}2.{Style.RESET_ALL} 🎮 Practice Challenges
{Fore.YELLOW}3.{Style.RESET_ALL} 🧪 Code Playground
{Fore.YELLOW}4.{Style.RESET_ALL} 📊 View Progress
{Fore.YELLOW}5.{Style.RESET_ALL} 🏆 Achievements
{Fore.YELLOW}6.{Style.RESET_ALL} 🎯 Take Quiz
{Fore.YELLOW}7.{Style.RESET_ALL} 🚀 Projects
{Fore.YELLOW}8.{Style.RESET_ALL} ⚙️  Settings
{Fore.YELLOW}9.{Style.RESET_ALL} ❓ Help
{Fore.YELLOW}0.{Style.RESET_ALL} 🚪 Exit

{Fore.CYAN}Choose an option (0-9):{Style.RESET_ALL} """
        return input(menu)
    
    def setup_user_profile(self):
        """Setup user profile for new users"""
        print(f"\n{Fore.GREEN}🎉 Welcome to Python Learning Program!{Style.RESET_ALL}")
        print("Let's set up your learning profile...\n")
        
        name = input(f"{Fore.CYAN}Enter your name: {Style.RESET_ALL}")
        
        print(f"\n{Fore.YELLOW}What's your current Python experience level?{Style.RESET_ALL}")
        print("1. Complete Beginner (Never coded before)")
        print("2. Some Programming Experience (Other languages)")
        print("3. Basic Python Knowledge")
        print("4. Intermediate Python Knowledge")
        
        while True:
            try:
                level = int(input(f"{Fore.CYAN}Choose (1-4): {Style.RESET_ALL}"))
                if 1 <= level <= 4:
                    break
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and 4{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
        
        level_names = {
            1: "complete_beginner",
            2: "some_programming",
            3: "basic_python",
            4: "intermediate_python"
        }
        
        user_profile = {
            "name": name,
            "experience_level": level_names[level],
            "created_date": datetime.now().isoformat(),
            "current_day": 1,
            "completed_lessons": [],
            "completed_challenges": [],
            "points": 0,
            "achievements": [],
            "streak": 0,
            "last_activity": datetime.now().isoformat()
        }
        
        self.user_data[name] = user_profile
        self.current_user = name
        self.save_user_data()
        
        print(f"\n{Fore.GREEN}✅ Profile created successfully!{Style.RESET_ALL}")
        print(f"Welcome, {name}! Let's start your Python journey! 🚀")
        time.sleep(2)
    
    def select_user(self):
        """Select or create user profile"""
        if not self.user_data:
            self.setup_user_profile()
            return
        
        print(f"\n{Fore.GREEN}👥 User Profiles{Style.RESET_ALL}")
        users = list(self.user_data.keys())
        
        for i, user in enumerate(users, 1):
            profile = self.user_data[user]
            print(f"{i}. {user} (Day {profile.get('current_day', 1)}, "
                  f"{profile.get('points', 0)} points)")
        
        print(f"{len(users) + 1}. Create New Profile")
        
        while True:
            try:
                choice = int(input(f"\n{Fore.CYAN}Select user (1-{len(users) + 1}): {Style.RESET_ALL}"))
                if 1 <= choice <= len(users):
                    self.current_user = users[choice - 1]
                    print(f"\n{Fore.GREEN}Welcome back, {self.current_user}!{Style.RESET_ALL}")
                    break
                elif choice == len(users) + 1:
                    self.setup_user_profile()
                    break
                else:
                    print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
    
    def run(self):
        """Main program loop"""
        self.display_banner()
        self.select_user()
        
        while True:
            try:
                choice = self.display_main_menu()
                
                if choice == '1':
                    self.start_learning_journey()
                elif choice == '2':
                    self.practice_challenges()
                elif choice == '3':
                    self.code_playground()
                elif choice == '4':
                    self.view_progress()
                elif choice == '5':
                    self.view_achievements()
                elif choice == '6':
                    self.take_quiz()
                elif choice == '7':
                    self.view_projects()
                elif choice == '8':
                    self.settings()
                elif choice == '9':
                    self.show_help()
                elif choice == '0':
                    print(f"\n{Fore.GREEN}Thanks for learning with us! Keep coding! 🚀{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}Program interrupted. Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
    
    def start_learning_journey(self):
        """Start the structured learning journey"""
        from modules.lesson_manager import LessonManager
        from core.progress_tracker import ProgressTracker

        lesson_manager = LessonManager()
        progress_tracker = ProgressTracker()

        print(f"\n{Fore.GREEN}📖 Learning Journey{Style.RESET_ALL}")

        # Get user's current level
        user_profile = self.user_data.get(self.current_user, {})
        experience_level = user_profile.get("experience_level", "complete_beginner")

        # Map experience to lesson level
        level_mapping = {
            "complete_beginner": "beginner",
            "some_programming": "beginner",
            "basic_python": "intermediate",
            "intermediate_python": "advanced"
        }

        current_level = level_mapping.get(experience_level, "beginner")

        # Show available lessons
        lessons = lesson_manager.get_available_lessons(current_level)

        if not lessons:
            print(f"{Fore.YELLOW}No lessons available for your level yet.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Available Lessons for {current_level.title()} Level:{Style.RESET_ALL}")
        for i, lesson in enumerate(lessons, 1):
            status = "✅" if lesson["id"] in user_profile.get("completed_lessons", []) else "📚"
            print(f"{i}. {status} {lesson['title']}")
            print(f"   {lesson['description']}")
            print(f"   Estimated time: {lesson.get('estimated_time', 60)} minutes")

        print(f"\n{Fore.YELLOW}Options:{Style.RESET_ALL}")
        print("1. Start next lesson")
        print("2. Choose specific lesson")
        print("3. Back to main menu")

        choice = input(f"\n{Fore.CYAN}Your choice (1-3): {Style.RESET_ALL}")

        if choice == '1':
            # Find next uncompleted lesson
            completed_lessons = user_profile.get("completed_lessons", [])
            next_lesson = None
            for lesson in lessons:
                if lesson["id"] not in completed_lessons:
                    next_lesson = lesson
                    break

            if next_lesson:
                success = lesson_manager.run_interactive_lesson(current_level, next_lesson["id"])
                if success:
                    # Update progress
                    progress_tracker.update_progress(
                        self.current_user,
                        "lesson_completed",
                        {"lesson_id": next_lesson["id"]}
                    )
                    self.load_user_data()  # Refresh user data
            else:
                print(f"{Fore.GREEN}🎉 You've completed all lessons in this level!{Style.RESET_ALL}")
                input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

        elif choice == '2':
            try:
                lesson_num = int(input(f"{Fore.CYAN}Enter lesson number: {Style.RESET_ALL}"))
                if 1 <= lesson_num <= len(lessons):
                    selected_lesson = lessons[lesson_num - 1]
                    success = lesson_manager.run_interactive_lesson(current_level, selected_lesson["id"])
                    if success:
                        progress_tracker.update_progress(
                            self.current_user,
                            "lesson_completed",
                            {"lesson_id": selected_lesson["id"]}
                        )
                        self.load_user_data()
                else:
                    print(f"{Fore.RED}Invalid lesson number{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")

    def practice_challenges(self):
        """Practice coding challenges"""
        from core.challenge_system import ChallengeSystem
        from core.progress_tracker import ProgressTracker

        challenge_system = ChallengeSystem()
        progress_tracker = ProgressTracker()

        while True:
            challenge_id = challenge_system.show_challenge_menu()

            if not challenge_id:
                break

            if challenge_id.lower() == 'back':
                break

            # Run the challenge
            result = challenge_system.run_challenge(challenge_id)

            if "error" not in result:
                # Update progress
                if result.get("success"):
                    progress_tracker.update_progress(
                        self.current_user,
                        "challenge_completed",
                        {
                            "challenge_id": challenge_id,
                            "difficulty": challenge_system.current_challenge.get("difficulty", "easy"),
                            "score": result.get("score", 0)
                        }
                    )
                    self.load_user_data()

            print(f"\n{Fore.CYAN}Press Enter to continue or type 'back' to return...{Style.RESET_ALL}")
            if input().lower() == 'back':
                break

    def code_playground(self):
        """Interactive code playground"""
        from core.code_runner import CodeRunner
        from core.progress_tracker import ProgressTracker

        code_runner = CodeRunner()
        progress_tracker = ProgressTracker()

        # Update progress for using playground
        progress_tracker.update_progress(
            self.current_user,
            "playground_used",
            {}
        )

        # Run interactive session
        code_runner.run_interactive_session()
    
    def view_progress(self):
        """View user progress"""
        from core.progress_tracker import ProgressTracker

        if not self.current_user:
            print(f"{Fore.RED}No user selected{Style.RESET_ALL}")
            return

        progress_tracker = ProgressTracker()
        stats = progress_tracker.get_progress_stats(self.current_user)

        if not stats:
            print(f"{Fore.RED}No progress data found{Style.RESET_ALL}")
            return

        print(f"\n{Fore.GREEN}📊 Progress Report for {self.current_user}{Style.RESET_ALL}")
        print("=" * 60)

        # Level and Points
        print(f"{Fore.YELLOW}🏆 Level:{Style.RESET_ALL} {stats['level']}")
        print(f"{Fore.YELLOW}💎 Points:{Style.RESET_ALL} {stats['points']}")
        print(f"{Fore.YELLOW}📈 Points to Next Level:{Style.RESET_ALL} {stats['points_to_next_level']}")

        # Learning Progress
        print(f"\n{Fore.CYAN}📚 Learning Progress:{Style.RESET_ALL}")
        print(f"Lessons Completed: {stats['lessons_completed']}")
        print(f"Lesson Completion: {stats['lesson_completion_percentage']:.1f}%")
        print(f"Challenges Completed: {stats['challenges_completed']}")
        print(f"Projects Completed: {stats['projects_completed']}")

        # Quiz Performance
        print(f"\n{Fore.BLUE}🎯 Quiz Performance:{Style.RESET_ALL}")
        print(f"Quizzes Taken: {stats['quizzes_taken']}")
        print(f"Average Score: {stats['average_quiz_score']:.1f}%")
        print(f"Perfect Scores: {stats['perfect_quizzes']}")

        # Activity Stats
        print(f"\n{Fore.MAGENTA}⚡ Activity Stats:{Style.RESET_ALL}")
        print(f"Current Streak: {stats['streak']} days")
        print(f"Playground Uses: {stats['playground_uses']}")
        print(f"Achievements Unlocked: {stats['achievements_count']}")
        print(f"Days Since Start: {stats['days_since_start']}")

        # Progress Bar for Level
        level = stats['level']
        current_points = stats['points']
        points_for_current_level = progress_tracker.points_for_level(level)
        points_for_next_level = progress_tracker.points_for_level(level + 1)

        if points_for_next_level > points_for_current_level:
            level_progress = (current_points - points_for_current_level) / (points_for_next_level - points_for_current_level)
            progress_bar_length = 20
            filled_length = int(progress_bar_length * level_progress)
            bar = "█" * filled_length + "░" * (progress_bar_length - filled_length)
            print(f"\n{Fore.GREEN}Level Progress: [{bar}] {level_progress * 100:.1f}%{Style.RESET_ALL}")

        # Show leaderboard position
        leaderboard = progress_tracker.get_leaderboard()
        user_position = None
        for i, entry in enumerate(leaderboard, 1):
            if entry["name"] == self.current_user:
                user_position = i
                break

        if user_position:
            print(f"\n{Fore.YELLOW}🏅 Leaderboard Position: #{user_position}{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def view_achievements(self):
        """View user achievements"""
        from core.progress_tracker import ProgressTracker

        progress_tracker = ProgressTracker()

        if not self.current_user:
            print(f"{Fore.RED}No user selected{Style.RESET_ALL}")
            return

        user_profile = self.user_data[self.current_user]
        achievements = user_profile.get("achievements", [])

        print(f"\n{Fore.GREEN}🏆 Achievements for {self.current_user}{Style.RESET_ALL}")
        print("=" * 50)

        if not achievements:
            print(f"{Fore.YELLOW}No achievements yet. Keep learning to unlock them!{Style.RESET_ALL}")
        else:
            for achievement_id in achievements:
                achievement_config = progress_tracker.achievements_config.get(achievement_id, {})
                if achievement_config:
                    icon = achievement_config.get("icon", "🏆")
                    name = achievement_config.get("name", "Unknown Achievement")
                    description = achievement_config.get("description", "")
                    points = achievement_config.get("points", 0)

                    print(f"{icon} {Fore.YELLOW}{name}{Style.RESET_ALL}")
                    print(f"   {description}")
                    print(f"   Points: {points}")
                    print()

        # Show available achievements
        print(f"\n{Fore.CYAN}🎯 Available Achievements:{Style.RESET_ALL}")
        for achievement_id, config in progress_tracker.achievements_config.items():
            if achievement_id not in achievements:
                icon = config.get("icon", "🏆")
                name = config.get("name", "Unknown Achievement")
                description = config.get("description", "")
                points = config.get("points", 0)

                print(f"{icon} {Fore.WHITE}{name}{Style.RESET_ALL} (Locked)")
                print(f"   {description}")
                print(f"   Points: {points}")
                print()

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")

    def take_quiz(self):
        """Take a quiz"""
        from core.quiz_engine import QuizEngine
        from core.progress_tracker import ProgressTracker

        quiz_engine = QuizEngine()
        progress_tracker = ProgressTracker()

        print(f"\n{Fore.GREEN}🎯 Quiz System{Style.RESET_ALL}")

        # Get available quizzes
        quizzes = quiz_engine.get_available_quizzes()

        if not quizzes:
            print(f"{Fore.YELLOW}No quizzes available yet.{Style.RESET_ALL}")
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Available Quizzes:{Style.RESET_ALL}")
        for i, quiz in enumerate(quizzes, 1):
            difficulty_color = {
                "beginner": Fore.GREEN,
                "intermediate": Fore.YELLOW,
                "advanced": Fore.RED
            }.get(quiz["difficulty"], Fore.WHITE)

            print(f"{i}. {quiz['title']}")
            print(f"   {quiz['description']}")
            print(f"   Difficulty: {difficulty_color}{quiz['difficulty'].title()}{Style.RESET_ALL}")
            print(f"   Questions: {quiz['question_count']}")
            if quiz['time_limit']:
                minutes = quiz['time_limit'] // 60
                seconds = quiz['time_limit'] % 60
                print(f"   Time Limit: {minutes}m {seconds}s")
            print()

        try:
            choice = int(input(f"{Fore.CYAN}Select quiz (1-{len(quizzes)}): {Style.RESET_ALL}"))
            if 1 <= choice <= len(quizzes):
                selected_quiz = quizzes[choice - 1]

                # Start the quiz
                if quiz_engine.start_quiz(selected_quiz["id"]):
                    results = quiz_engine.run_quiz()

                    # Update progress
                    progress_tracker.update_progress(
                        self.current_user,
                        "quiz_completed",
                        {
                            "quiz_id": selected_quiz["id"],
                            "score": results["score"],
                            "max_score": results["total_questions"]
                        }
                    )
                    self.load_user_data()
            else:
                print(f"{Fore.RED}Invalid choice{Style.RESET_ALL}")
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")

        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def view_projects(self):
        """View available projects"""
        print(f"\n{Fore.GREEN}🚀 Projects{Style.RESET_ALL}")
        print("This feature will be implemented with project modules...")
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def settings(self):
        """Program settings"""
        print(f"\n{Fore.GREEN}⚙️ Settings{Style.RESET_ALL}")
        print("This feature will be implemented...")
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
    
    def show_help(self):
        """Show help information"""
        help_text = f"""
{Fore.GREEN}❓ HELP - Python Learning Program{Style.RESET_ALL}

{Fore.YELLOW}🎯 Program Features:{Style.RESET_ALL}
• Structured 30+ day learning path from beginner to expert
• Interactive coding challenges with immediate feedback
• Code playground for experimentation
• Progress tracking and achievement system
• Quizzes to test your knowledge
• Real-world projects to build your portfolio

{Fore.YELLOW}📚 Learning Path:{Style.RESET_ALL}
• Beginner (Days 1-10): Python basics, syntax, data types
• Intermediate (Days 11-20): Functions, OOP, file handling
• Advanced (Days 21-30): Advanced concepts, libraries
• Expert (Days 31+): Specialization tracks, projects

{Fore.YELLOW}🏆 Achievement System:{Style.RESET_ALL}
• Earn points for completing lessons and challenges
• Unlock badges for milestones
• Maintain learning streaks
• Compare progress with the community

{Fore.YELLOW}💡 Tips:{Style.RESET_ALL}
• Practice daily to maintain your streak
• Don't skip the exercises - they're crucial for learning
• Use the code playground to experiment
• Take quizzes to reinforce your knowledge
        """
        print(help_text)
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    try:
        # Check if colorama is installed
        import colorama
        program = PythonLearningProgram()
        program.run()
    except ImportError:
        print("Installing required dependencies...")
        os.system("pip install colorama")
        print("Please run the program again.")
