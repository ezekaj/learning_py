"""
Lesson Manager Module
Inspired by 30-Days-Of-Python structured approach:
- Progressive learning path
- Daily lessons with clear objectives
- Hands-on exercises
- Real-world examples
- Adaptive difficulty based on user progress
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
import colorama
from colorama import Fore, Style

class LessonManager:
    """Manage structured learning lessons"""
    
    def __init__(self, lessons_dir: str = "data/lessons"):
        self.lessons_dir = lessons_dir
        self.current_lesson = None
        self.lesson_structure = None
        self.ensure_lesson_structure()
        self.create_sample_lessons()
    
    def ensure_lesson_structure(self):
        """Create lesson directory structure"""
        levels = ["beginner", "intermediate", "advanced", "expert"]
        
        for level in levels:
            level_dir = os.path.join(self.lessons_dir, level)
            os.makedirs(level_dir, exist_ok=True)
        
        # Create lesson index file
        index_file = os.path.join(self.lessons_dir, "lesson_index.json")
        if not os.path.exists(index_file):
            self.create_lesson_index()
    
    def create_lesson_index(self):
        """Create the main lesson index structure"""
        lesson_structure = {
            "beginner": {
                "title": "Python Fundamentals",
                "description": "Learn Python basics from scratch",
                "estimated_days": 10,
                "lessons": [
                    {
                        "id": "day_01",
                        "title": "Introduction to Python",
                        "description": "What is Python, installation, and first program",
                        "objectives": [
                            "Understand what Python is",
                            "Install Python and set up development environment",
                            "Write your first Python program",
                            "Understand Python syntax basics"
                        ],
                        "topics": ["python_history", "installation", "hello_world", "syntax_basics"],
                        "exercises": 5,
                        "estimated_time": 60
                    },
                    {
                        "id": "day_02",
                        "title": "Variables and Data Types",
                        "description": "Learn about Python variables and basic data types",
                        "objectives": [
                            "Understand variables and naming conventions",
                            "Learn about basic data types",
                            "Practice variable assignment",
                            "Use built-in functions"
                        ],
                        "topics": ["variables", "data_types", "naming_conventions", "builtin_functions"],
                        "exercises": 8,
                        "estimated_time": 75
                    },
                    {
                        "id": "day_03",
                        "title": "Operators and Expressions",
                        "description": "Master Python operators and expressions",
                        "objectives": [
                            "Learn arithmetic operators",
                            "Understand comparison operators",
                            "Use logical operators",
                            "Practice operator precedence"
                        ],
                        "topics": ["arithmetic_operators", "comparison_operators", "logical_operators", "precedence"],
                        "exercises": 10,
                        "estimated_time": 70
                    },
                    {
                        "id": "day_04",
                        "title": "Strings and String Methods",
                        "description": "Work with strings and string manipulation",
                        "objectives": [
                            "Create and manipulate strings",
                            "Use string methods",
                            "Format strings",
                            "Handle string indexing and slicing"
                        ],
                        "topics": ["string_creation", "string_methods", "formatting", "indexing_slicing"],
                        "exercises": 12,
                        "estimated_time": 80
                    },
                    {
                        "id": "day_05",
                        "title": "Lists and List Methods",
                        "description": "Master Python lists and list operations",
                        "objectives": [
                            "Create and modify lists",
                            "Use list methods",
                            "Understand list indexing",
                            "Practice list comprehensions"
                        ],
                        "topics": ["list_creation", "list_methods", "indexing", "list_comprehensions"],
                        "exercises": 15,
                        "estimated_time": 90
                    }
                ]
            },
            "intermediate": {
                "title": "Python Problem Solving",
                "description": "Build problem-solving skills with Python",
                "estimated_days": 10,
                "lessons": [
                    {
                        "id": "day_11",
                        "title": "Functions and Scope",
                        "description": "Master function definition and scope concepts",
                        "objectives": [
                            "Define and call functions",
                            "Understand function parameters",
                            "Learn about scope and namespaces",
                            "Use lambda functions"
                        ],
                        "topics": ["function_definition", "parameters", "scope", "lambda_functions"],
                        "exercises": 12,
                        "estimated_time": 85
                    }
                ]
            },
            "advanced": {
                "title": "Python Mastery",
                "description": "Advanced Python concepts and techniques",
                "estimated_days": 10,
                "lessons": []
            },
            "expert": {
                "title": "Python Expertise",
                "description": "Expert-level Python and specialization",
                "estimated_days": 10,
                "lessons": []
            }
        }
        
        index_file = os.path.join(self.lessons_dir, "lesson_index.json")
        with open(index_file, 'w') as f:
            json.dump(lesson_structure, f, indent=2)
        
        self.lesson_structure = lesson_structure
    
    def create_sample_lessons(self):
        """Create sample lesson content files"""
        # Create Day 1 lesson
        day_01_content = {
            "lesson_id": "day_01",
            "title": "Introduction to Python",
            "content": {
                "introduction": """
Welcome to your Python learning journey! 🐍

Python is a high-level, interpreted programming language known for its simplicity and readability. 
Created by Guido van Rossum in 1991, Python has become one of the most popular programming languages 
in the world, used for web development, data science, artificial intelligence, automation, and more.

Why Python?
• Easy to learn and read
• Versatile and powerful
• Large community and ecosystem
• Cross-platform compatibility
• Extensive libraries and frameworks
                """,
                "concepts": [
                    {
                        "title": "What is Python?",
                        "explanation": "Python is an interpreted, high-level programming language with dynamic semantics.",
                        "example": "# This is a Python comment\nprint('Hello, Python!')",
                        "output": "Hello, Python!"
                    },
                    {
                        "title": "Python Syntax",
                        "explanation": "Python uses indentation to define code blocks, making it very readable.",
                        "example": "if True:\n    print('This is indented')\n    print('This too!')",
                        "output": "This is indented\nThis too!"
                    }
                ],
                "exercises": [
                    {
                        "id": "ex_01_01",
                        "title": "Your First Program",
                        "description": "Write a program that prints your name",
                        "starter_code": "# Write your code here\n",
                        "solution": "print('Your Name')",
                        "hints": ["Use the print() function", "Put your name in quotes"]
                    },
                    {
                        "id": "ex_01_02",
                        "title": "Basic Arithmetic",
                        "description": "Calculate and print the result of 15 + 25",
                        "starter_code": "# Calculate 15 + 25\n",
                        "solution": "print(15 + 25)",
                        "hints": ["Use the + operator", "You can print the calculation directly"]
                    }
                ]
            }
        }
        
        day_01_file = os.path.join(self.lessons_dir, "beginner", "day_01.json")
        if not os.path.exists(day_01_file):
            with open(day_01_file, 'w') as f:
                json.dump(day_01_content, f, indent=2)
    
    def load_lesson_structure(self) -> Dict:
        """Load the lesson structure from file"""
        index_file = os.path.join(self.lessons_dir, "lesson_index.json")
        try:
            with open(index_file, 'r') as f:
                self.lesson_structure = json.load(f)
                return self.lesson_structure
        except Exception as e:
            print(f"Error loading lesson structure: {e}")
            return {}
    
    def get_lesson_path(self, level: str, lesson_id: str) -> List[Dict]:
        """Get recommended learning path for user"""
        if not self.lesson_structure:
            self.load_lesson_structure()
        
        path = []
        levels = ["beginner", "intermediate", "advanced", "expert"]
        
        # Start from user's level
        start_index = levels.index(level) if level in levels else 0
        
        for level_name in levels[start_index:]:
            level_data = self.lesson_structure.get(level_name, {})
            lessons = level_data.get("lessons", [])
            
            for lesson in lessons:
                path.append({
                    "level": level_name,
                    "lesson_id": lesson["id"],
                    "title": lesson["title"],
                    "description": lesson["description"],
                    "estimated_time": lesson.get("estimated_time", 60),
                    "exercises": lesson.get("exercises", 0)
                })
        
        return path
    
    def load_lesson(self, level: str, lesson_id: str) -> Optional[Dict]:
        """Load a specific lesson"""
        lesson_file = os.path.join(self.lessons_dir, level, f"{lesson_id}.json")
        
        try:
            with open(lesson_file, 'r') as f:
                lesson_data = json.load(f)
                self.current_lesson = lesson_data
                return lesson_data
        except FileNotFoundError:
            print(f"{Fore.RED}Lesson not found: {lesson_id}{Style.RESET_ALL}")
            return None
        except Exception as e:
            print(f"{Fore.RED}Error loading lesson: {e}{Style.RESET_ALL}")
            return None
    
    def display_lesson(self, lesson_data: Dict):
        """Display lesson content in a formatted way"""
        print(f"\n{Fore.GREEN}📚 {lesson_data['title']}{Style.RESET_ALL}")
        print("=" * 60)
        
        content = lesson_data.get("content", {})
        
        # Show introduction
        if "introduction" in content:
            print(f"\n{Fore.CYAN}📖 Introduction:{Style.RESET_ALL}")
            print(content["introduction"])
        
        # Show concepts
        if "concepts" in content:
            print(f"\n{Fore.YELLOW}💡 Key Concepts:{Style.RESET_ALL}")
            for i, concept in enumerate(content["concepts"], 1):
                print(f"\n{i}. {Fore.YELLOW}{concept['title']}{Style.RESET_ALL}")
                print(f"   {concept['explanation']}")
                
                if "example" in concept:
                    print(f"\n   {Fore.GREEN}Example:{Style.RESET_ALL}")
                    print(f"   {concept['example']}")
                    
                    if "output" in concept:
                        print(f"\n   {Fore.BLUE}Output:{Style.RESET_ALL}")
                        print(f"   {concept['output']}")
        
        print(f"\n{Fore.CYAN}Ready to practice? Let's do some exercises!{Style.RESET_ALL}")
    
    def get_lesson_exercises(self, lesson_data: Dict) -> List[Dict]:
        """Get exercises for a lesson"""
        content = lesson_data.get("content", {})
        return content.get("exercises", [])
    
    def display_exercise(self, exercise: Dict, exercise_num: int, total_exercises: int):
        """Display a single exercise"""
        print(f"\n{Fore.GREEN}🎯 Exercise {exercise_num}/{total_exercises}: {exercise['title']}{Style.RESET_ALL}")
        print("-" * 50)
        print(f"{exercise['description']}")
        
        if "starter_code" in exercise:
            print(f"\n{Fore.YELLOW}Starter Code:{Style.RESET_ALL}")
            print(exercise["starter_code"])
    
    def check_exercise_solution(self, exercise: Dict, user_code: str) -> Dict:
        """Check if user's solution is correct"""
        # This is a simplified check - in a real implementation,
        # you'd want more sophisticated testing
        
        solution = exercise.get("solution", "")
        
        # Basic comparison (could be enhanced with actual code execution)
        is_correct = user_code.strip() == solution.strip()
        
        result = {
            "correct": is_correct,
            "user_code": user_code,
            "expected": solution,
            "hints": exercise.get("hints", [])
        }
        
        return result
    
    def run_interactive_lesson(self, level: str, lesson_id: str):
        """Run an interactive lesson session"""
        lesson_data = self.load_lesson(level, lesson_id)
        if not lesson_data:
            return False
        
        # Display lesson content
        self.display_lesson(lesson_data)
        
        input(f"\n{Fore.CYAN}Press Enter to continue to exercises...{Style.RESET_ALL}")
        
        # Run exercises
        exercises = self.get_lesson_exercises(lesson_data)
        if not exercises:
            print(f"{Fore.YELLOW}No exercises available for this lesson.{Style.RESET_ALL}")
            return True
        
        completed_exercises = 0
        
        for i, exercise in enumerate(exercises, 1):
            self.display_exercise(exercise, i, len(exercises))
            
            while True:
                print(f"\n{Fore.CYAN}Enter your solution (or 'hint' for a hint, 'skip' to skip):{Style.RESET_ALL}")
                user_input = input(">>> ").strip()
                
                if user_input.lower() == 'skip':
                    print(f"{Fore.YELLOW}Exercise skipped.{Style.RESET_ALL}")
                    break
                elif user_input.lower() == 'hint':
                    hints = exercise.get("hints", [])
                    if hints:
                        print(f"{Fore.BLUE}💡 Hint: {hints[0]}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}No hints available for this exercise.{Style.RESET_ALL}")
                    continue
                elif not user_input:
                    print(f"{Fore.RED}Please enter your solution.{Style.RESET_ALL}")
                    continue
                
                # Check solution
                result = self.check_exercise_solution(exercise, user_input)
                
                if result["correct"]:
                    print(f"{Fore.GREEN}✅ Correct! Well done!{Style.RESET_ALL}")
                    completed_exercises += 1
                    break
                else:
                    print(f"{Fore.RED}❌ Not quite right. Try again!{Style.RESET_ALL}")
                    if result["hints"]:
                        print(f"{Fore.BLUE}💡 Hint: {result['hints'][0]}{Style.RESET_ALL}")
        
        # Show lesson completion summary
        print(f"\n{Fore.GREEN}🎉 Lesson Complete!{Style.RESET_ALL}")
        print(f"Exercises completed: {completed_exercises}/{len(exercises)}")
        
        if completed_exercises == len(exercises):
            print(f"{Fore.GREEN}Perfect! You've mastered this lesson! 🏆{Style.RESET_ALL}")
        elif completed_exercises >= len(exercises) * 0.7:
            print(f"{Fore.YELLOW}Great job! You've got a good grasp of the concepts. 👍{Style.RESET_ALL}")
        else:
            print(f"{Fore.BLUE}Keep practicing! Review the concepts and try again. 📚{Style.RESET_ALL}")
        
        return True
    
    def get_available_lessons(self, level: str = None) -> List[Dict]:
        """Get list of available lessons"""
        if not self.lesson_structure:
            self.load_lesson_structure()
        
        lessons = []
        
        if level:
            level_data = self.lesson_structure.get(level, {})
            level_lessons = level_data.get("lessons", [])
            for lesson in level_lessons:
                lesson["level"] = level
                lessons.append(lesson)
        else:
            for level_name, level_data in self.lesson_structure.items():
                level_lessons = level_data.get("lessons", [])
                for lesson in level_lessons:
                    lesson["level"] = level_name
                    lessons.append(lesson)
        
        return lessons
