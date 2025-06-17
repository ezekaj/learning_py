#!/usr/bin/env python3
"""
Test script to verify the Python Learning Program components work correctly
"""

import sys
import os

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        import colorama
        from colorama import Fore, Style
        colorama.init()
        print(f"{Fore.GREEN}✅ colorama imported successfully{Style.RESET_ALL}")
        
        from core.progress_tracker import ProgressTracker
        print(f"{Fore.GREEN}✅ ProgressTracker imported successfully{Style.RESET_ALL}")
        
        from core.quiz_engine import QuizEngine
        print(f"{Fore.GREEN}✅ QuizEngine imported successfully{Style.RESET_ALL}")
        
        from core.code_runner import CodeRunner
        print(f"{Fore.GREEN}✅ CodeRunner imported successfully{Style.RESET_ALL}")
        
        from core.challenge_system import ChallengeSystem
        print(f"{Fore.GREEN}✅ ChallengeSystem imported successfully{Style.RESET_ALL}")
        
        from modules.lesson_manager import LessonManager
        print(f"{Fore.GREEN}✅ LessonManager imported successfully{Style.RESET_ALL}")
        
        return True
        
    except ImportError as e:
        print(f"{Fore.RED}❌ Import error: {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
        return False

def test_progress_tracker():
    """Test ProgressTracker functionality"""
    print(f"\n🧪 Testing ProgressTracker...")
    
    try:
        from core.progress_tracker import ProgressTracker
        from colorama import Fore, Style
        
        tracker = ProgressTracker()
        
        # Test creating a user profile
        test_user = "test_user"
        tracker.update_progress(test_user, "lesson_completed", {"lesson_id": "test_lesson"})
        
        # Test getting stats
        stats = tracker.get_progress_stats(test_user)
        if stats:
            print(f"{Fore.GREEN}✅ ProgressTracker working correctly{Style.RESET_ALL}")
            print(f"   Test user level: {stats.get('level', 'N/A')}")
            print(f"   Test user points: {stats.get('points', 'N/A')}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  ProgressTracker created but no stats returned{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ ProgressTracker test failed: {e}{Style.RESET_ALL}")
        return False

def test_quiz_engine():
    """Test QuizEngine functionality"""
    print(f"\n🧪 Testing QuizEngine...")
    
    try:
        from core.quiz_engine import QuizEngine
        from colorama import Fore, Style
        
        quiz_engine = QuizEngine()
        
        # Test getting available quizzes
        quizzes = quiz_engine.get_available_quizzes()
        
        if quizzes:
            print(f"{Fore.GREEN}✅ QuizEngine working correctly{Style.RESET_ALL}")
            print(f"   Available quizzes: {len(quizzes)}")
            for quiz in quizzes[:2]:  # Show first 2 quizzes
                print(f"   - {quiz['title']} ({quiz['difficulty']})")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  QuizEngine created but no quizzes found{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ QuizEngine test failed: {e}{Style.RESET_ALL}")
        return False

def test_code_runner():
    """Test CodeRunner functionality"""
    print(f"\n🧪 Testing CodeRunner...")
    
    try:
        from core.code_runner import CodeRunner
        from colorama import Fore, Style
        
        code_runner = CodeRunner()
        
        # Test executing simple code
        test_code = "print('Hello, World!')"
        result = code_runner.execute_code(test_code)
        
        if result.get("success") and "Hello, World!" in result.get("output", ""):
            print(f"{Fore.GREEN}✅ CodeRunner working correctly{Style.RESET_ALL}")
            print(f"   Test code executed successfully")
            print(f"   Output: {result.get('output', '').strip()}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  CodeRunner test had issues{Style.RESET_ALL}")
            print(f"   Result: {result}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ CodeRunner test failed: {e}{Style.RESET_ALL}")
        return False

def test_challenge_system():
    """Test ChallengeSystem functionality"""
    print(f"\n🧪 Testing ChallengeSystem...")
    
    try:
        from core.challenge_system import ChallengeSystem
        from colorama import Fore, Style
        
        challenge_system = ChallengeSystem()
        
        # Test getting available challenges
        challenges = challenge_system.get_available_challenges()
        
        if challenges:
            print(f"{Fore.GREEN}✅ ChallengeSystem working correctly{Style.RESET_ALL}")
            print(f"   Available challenges: {len(challenges)}")
            for challenge in challenges[:2]:  # Show first 2 challenges
                print(f"   - {challenge['title']} ({challenge['difficulty']})")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  ChallengeSystem created but no challenges found{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ ChallengeSystem test failed: {e}{Style.RESET_ALL}")
        return False

def test_lesson_manager():
    """Test LessonManager functionality"""
    print(f"\n🧪 Testing LessonManager...")
    
    try:
        from modules.lesson_manager import LessonManager
        from colorama import Fore, Style
        
        lesson_manager = LessonManager()
        
        # Test getting available lessons
        lessons = lesson_manager.get_available_lessons("beginner")
        
        if lessons:
            print(f"{Fore.GREEN}✅ LessonManager working correctly{Style.RESET_ALL}")
            print(f"   Available beginner lessons: {len(lessons)}")
            for lesson in lessons[:2]:  # Show first 2 lessons
                print(f"   - {lesson['title']}")
            return True
        else:
            print(f"{Fore.YELLOW}⚠️  LessonManager created but no lessons found{Style.RESET_ALL}")
            return False
            
    except Exception as e:
        print(f"{Fore.RED}❌ LessonManager test failed: {e}{Style.RESET_ALL}")
        return False

def main():
    """Run all tests"""
    print("🐍 Python Learning Program - Component Tests")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Progress Tracker", test_progress_tracker),
        ("Quiz Engine", test_quiz_engine),
        ("Code Runner", test_code_runner),
        ("Challenge System", test_challenge_system),
        ("Lesson Manager", test_lesson_manager)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The program should work correctly.")
        print("\nYou can now run: python main.py")
    elif passed >= total * 0.8:
        print("👍 Most tests passed! The program should mostly work.")
        print("\nYou can try running: python main.py")
    else:
        print("⚠️  Several tests failed. There may be issues with the program.")
        print("\nPlease check the error messages above.")

if __name__ == "__main__":
    main()
