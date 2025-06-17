#!/usr/bin/env python3
"""
Database Seeder for Python Learning Program
Creates sample courses, lessons, quizzes, and challenges
"""

from app import app, db
from models import Course, Lesson, Exercise, Quiz, Challenge, Achievement
import json

def create_sample_courses():
    """Create sample courses"""
    courses_data = [
        {
            "title": "Python Fundamentals",
            "description": "Learn Python basics from scratch",
            "difficulty_level": "beginner",
            "order_index": 1
        },
        {
            "title": "Python Problem Solving",
            "description": "Build problem-solving skills with Python",
            "difficulty_level": "intermediate", 
            "order_index": 2
        },
        {
            "title": "Python Mastery",
            "description": "Advanced Python concepts and techniques",
            "difficulty_level": "advanced",
            "order_index": 3
        },
        {
            "title": "Python Expertise",
            "description": "Expert-level Python and specialization",
            "difficulty_level": "expert",
            "order_index": 4
        }
    ]
    
    for course_data in courses_data:
        existing_course = Course.query.filter_by(title=course_data["title"]).first()
        if not existing_course:
            course = Course(**course_data)
            db.session.add(course)
    
    db.session.commit()
    print("✅ Sample courses created")

def create_sample_lessons():
    """Create sample lessons"""
    # Get the beginner course
    beginner_course = Course.query.filter_by(difficulty_level="beginner").first()
    
    if not beginner_course:
        print("❌ Beginner course not found")
        return
    
    lessons_data = [
        {
            "title": "Introduction to Python",
            "description": "What is Python, installation, and first program",
            "content": json.dumps({
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
                ]
            }),
            "objectives": json.dumps([
                "Understand what Python is",
                "Install Python and set up development environment", 
                "Write your first Python program",
                "Understand Python syntax basics"
            ]),
            "estimated_time": 60,
            "difficulty": "beginner",
            "order_index": 1,
            "points_reward": 10,
            "course_id": beginner_course.id
        },
        {
            "title": "Variables and Data Types",
            "description": "Learn about Python variables and basic data types",
            "content": json.dumps({
                "introduction": """
In this lesson, you'll learn about variables and data types in Python.
Variables are containers for storing data values, and Python has several built-in data types.
                """,
                "concepts": [
                    {
                        "title": "Variables",
                        "explanation": "Variables are used to store data. In Python, you don't need to declare the type.",
                        "example": "name = 'Python'\nage = 30\nprint(name, age)",
                        "output": "Python 30"
                    },
                    {
                        "title": "Data Types",
                        "explanation": "Python has several built-in data types: str, int, float, bool, list, dict, etc.",
                        "example": "text = 'Hello'\nnumber = 42\nfloating = 3.14\nis_true = True",
                        "output": "Variables created with different types"
                    }
                ]
            }),
            "objectives": json.dumps([
                "Understand variables and naming conventions",
                "Learn about basic data types",
                "Practice variable assignment",
                "Use built-in functions"
            ]),
            "estimated_time": 75,
            "difficulty": "beginner",
            "order_index": 2,
            "points_reward": 10,
            "course_id": beginner_course.id
        },
        {
            "title": "Operators and Expressions",
            "description": "Master Python operators and expressions",
            "content": json.dumps({
                "introduction": """
Operators are special symbols that perform operations on variables and values.
Python supports various types of operators for different operations.
                """,
                "concepts": [
                    {
                        "title": "Arithmetic Operators",
                        "explanation": "Used for mathematical operations: +, -, *, /, //, %, **",
                        "example": "a = 10\nb = 3\nprint(a + b, a - b, a * b, a / b)",
                        "output": "13 7 30 3.3333333333333335"
                    },
                    {
                        "title": "Comparison Operators", 
                        "explanation": "Used to compare values: ==, !=, <, >, <=, >=",
                        "example": "x = 5\ny = 10\nprint(x < y, x == y, x != y)",
                        "output": "True False True"
                    }
                ]
            }),
            "objectives": json.dumps([
                "Learn arithmetic operators",
                "Understand comparison operators",
                "Use logical operators",
                "Practice operator precedence"
            ]),
            "estimated_time": 70,
            "difficulty": "beginner",
            "order_index": 3,
            "points_reward": 10,
            "course_id": beginner_course.id
        },
        {
            "title": "Strings and String Methods",
            "description": "Work with strings and string manipulation",
            "content": json.dumps({
                "introduction": """
Strings are sequences of characters. Python provides many built-in methods
to work with strings effectively.
                """,
                "concepts": [
                    {
                        "title": "Creating Strings",
                        "explanation": "Strings can be created using single or double quotes",
                        "example": "name = 'Python'\nmessage = \"Hello, World!\"\nprint(name, message)",
                        "output": "Python Hello, World!"
                    },
                    {
                        "title": "String Methods",
                        "explanation": "Python provides many useful string methods",
                        "example": "text = 'python programming'\nprint(text.upper(), text.title(), text.replace('python', 'Python'))",
                        "output": "PYTHON PROGRAMMING Python Programming Python programming"
                    }
                ]
            }),
            "objectives": json.dumps([
                "Create and manipulate strings",
                "Use string methods",
                "Format strings",
                "Handle string indexing and slicing"
            ]),
            "estimated_time": 80,
            "difficulty": "beginner",
            "order_index": 4,
            "points_reward": 10,
            "course_id": beginner_course.id
        },
        {
            "title": "Lists and List Methods",
            "description": "Master Python lists and list operations",
            "content": json.dumps({
                "introduction": """
Lists are ordered collections of items. They are mutable, meaning you can
change their contents after creation.
                """,
                "concepts": [
                    {
                        "title": "Creating Lists",
                        "explanation": "Lists are created using square brackets",
                        "example": "fruits = ['apple', 'banana', 'orange']\nnumbers = [1, 2, 3, 4, 5]\nprint(fruits, numbers)",
                        "output": "['apple', 'banana', 'orange'] [1, 2, 3, 4, 5]"
                    },
                    {
                        "title": "List Methods",
                        "explanation": "Lists have many useful methods for manipulation",
                        "example": "my_list = [1, 2, 3]\nmy_list.append(4)\nmy_list.extend([5, 6])\nprint(my_list)",
                        "output": "[1, 2, 3, 4, 5, 6]"
                    }
                ]
            }),
            "objectives": json.dumps([
                "Create and modify lists",
                "Use list methods",
                "Understand list indexing",
                "Practice list comprehensions"
            ]),
            "estimated_time": 90,
            "difficulty": "beginner",
            "order_index": 5,
            "points_reward": 15,
            "course_id": beginner_course.id
        }
    ]
    
    for lesson_data in lessons_data:
        existing_lesson = Lesson.query.filter_by(title=lesson_data["title"]).first()
        if not existing_lesson:
            lesson = Lesson(**lesson_data)
            db.session.add(lesson)
    
    db.session.commit()
    print("✅ Sample lessons created")

def create_sample_exercises():
    """Create sample exercises for lessons"""
    # Get the first lesson
    first_lesson = Lesson.query.filter_by(order_index=1).first()
    
    if not first_lesson:
        print("❌ First lesson not found")
        return
    
    exercises_data = [
        {
            "title": "Your First Program",
            "description": "Write a program that prints your name",
            "exercise_type": "code_completion",
            "content": json.dumps({
                "starter_code": "# Write your code here\n",
                "instructions": "Use the print() function to display your name"
            }),
            "solution": json.dumps({
                "code": "print('Your Name')",
                "explanation": "The print() function outputs text to the console"
            }),
            "hints": json.dumps([
                "Use the print() function",
                "Put your name in quotes"
            ]),
            "points_reward": 5,
            "order_index": 1,
            "lesson_id": first_lesson.id
        },
        {
            "title": "Basic Arithmetic",
            "description": "Calculate and print the result of 15 + 25",
            "exercise_type": "code_completion",
            "content": json.dumps({
                "starter_code": "# Calculate 15 + 25\n",
                "instructions": "Calculate the sum and print the result"
            }),
            "solution": json.dumps({
                "code": "print(15 + 25)",
                "explanation": "You can print the calculation directly"
            }),
            "hints": json.dumps([
                "Use the + operator",
                "You can print the calculation directly"
            ]),
            "points_reward": 5,
            "order_index": 2,
            "lesson_id": first_lesson.id
        }
    ]
    
    for exercise_data in exercises_data:
        existing_exercise = Exercise.query.filter_by(title=exercise_data["title"]).first()
        if not existing_exercise:
            exercise = Exercise(**exercise_data)
            db.session.add(exercise)
    
    db.session.commit()
    print("✅ Sample exercises created")

def create_sample_achievements():
    """Create sample achievements"""
    achievements_data = [
        {
            "name": "First Steps",
            "description": "Complete your first lesson",
            "icon": "🎯",
            "points_reward": 10,
            "condition_type": "lessons_completed",
            "condition_value": 1
        },
        {
            "name": "Week Warrior",
            "description": "Maintain a 7-day learning streak",
            "icon": "🔥",
            "points_reward": 50,
            "condition_type": "streak",
            "condition_value": 7
        },
        {
            "name": "Challenge Master",
            "description": "Complete 10 coding challenges",
            "icon": "⚔️",
            "points_reward": 100,
            "condition_type": "challenges_completed",
            "condition_value": 10
        },
        {
            "name": "Quiz Champion",
            "description": "Score 100% on 5 quizzes",
            "icon": "🏆",
            "points_reward": 75,
            "condition_type": "perfect_quizzes",
            "condition_value": 5
        },
        {
            "name": "Python Novice",
            "description": "Complete beginner level",
            "icon": "🐍",
            "points_reward": 200,
            "condition_type": "level_completed",
            "condition_value": 1
        }
    ]
    
    for achievement_data in achievements_data:
        existing_achievement = Achievement.query.filter_by(name=achievement_data["name"]).first()
        if not existing_achievement:
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
    
    db.session.commit()
    print("✅ Sample achievements created")

def seed_database():
    """Main function to seed the database"""
    print("🌱 Seeding database with sample data...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created")
        
        # Create sample data
        create_sample_courses()
        create_sample_lessons()
        create_sample_exercises()
        create_sample_achievements()
        
        print("🎉 Database seeding completed!")

if __name__ == "__main__":
    seed_database()
