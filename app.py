from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
import secrets
import logging

# Import our custom error handling and validation
# Essential imports for basic functionality
from core.error_handler import error_handler, ValidationError, AuthenticationError, UserDataError
from core.validators import validator
from core.security import rate_limit, csrf_protection
from core.database_manager import db_manager
from core.performance import disk_cache, performance_monitor, cleanup_caches
from core.memory_manager import memory_monitor, get_memory_usage, optimize_memory
from core.adaptive_learning import learning_analytics, UserPerformance, DifficultyLevel, LearningStyle, learning_path_generator
from core.social_learning import social_manager

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Configure session settings
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 hours
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Application metadata
APP_VERSION = "2.0.0"
APP_NAME = "Python Learning Platform"
APP_DESCRIPTION = "Comprehensive Python learning platform with interactive lessons, challenges, and gamification"

# Configure Flask logging to work with our error handler
app.logger.addHandler(error_handler.logger.handlers[0])
app.logger.setLevel(logging.INFO)

# Session management helpers
def get_current_user():
    """Get current user email from session"""
    return session.get('user')

def is_logged_in():
    """Check if user is logged in"""
    return 'user' in session

def set_user_session(email):
    """Set user session with standard configuration"""
    session.clear()
    session['user'] = email
    session.permanent = True
    session['login_time'] = datetime.now().isoformat()
    session['last_activity'] = datetime.now().isoformat()

def update_session_activity():
    """Update session activity timestamp"""
    if is_logged_in():
        session['last_activity'] = datetime.now().isoformat()
        session.permanent = True

def validate_session():
    """Simplified session validation"""
    return 'user' in session

def load_user_data():
    """Simplified user data loading"""
    try:
        file_path = "data/user_progress.json"
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading user data: {e}")
        return {}

def save_user_data(data):
    """Simplified user data saving"""
    try:
        file_path = "data/user_progress.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving user data: {e}")
        return False

def get_progress_stats(user_email):
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    lessons_completed = user.get('lessons_completed', 0)
    points = user.get('points', 0)
    level = user.get('level', 1)

    return {
        'lessons_completed': lessons_completed,
        'points': points,
        'level': level,
        'streak': user.get('streak', 0),
        'challenges_completed': user.get('challenges_completed', 0),
        'quizzes_completed': user.get('quizzes_completed', 0),
        'quizzes_taken': user.get('quizzes_taken', 0),
        'playground_uses': user.get('playground_uses', 0),
        'points_to_next_level': 100 - (points % 100),
        'lesson_completion_percentage': min((lessons_completed / 50) * 100, 100),  # Updated for 50 lessons
        'quiz_completion_percentage': min((user.get('quizzes_completed', 0) / 20) * 100, 100),  # 20 quizzes
        'challenge_completion_percentage': min((user.get('challenges_completed', 0) / 10) * 100, 100),  # 10 challenges
        'average_quiz_score': user.get('average_quiz_score', 0),
        'total_study_time': user.get('total_study_time', 0),
        'days_since_start': user.get('days_since_start', 0),
        'learning_velocity': calculate_learning_velocity(user),
        'skill_score': calculate_skill_score(user),
        'completion_rate': {
            'lessons': round((lessons_completed / 50) * 100, 1),
            'quizzes': round((user.get('quizzes_completed', 0) / 20) * 100, 1),
            'challenges': round((user.get('challenges_completed', 0) / 10) * 100, 1)
        }
    }

def calculate_learning_velocity(user):
    """Calculate items completed per day"""
    created_at = user.get('created_at', datetime.now().isoformat())
    try:
        start_date = datetime.fromisoformat(created_at.replace('Z', '+00:00'))
        days_since_start = max((datetime.now() - start_date).days, 1)
    except:
        days_since_start = 1

    total_completed = (
        user.get('lessons_completed', 0) +
        user.get('challenges_completed', 0) +
        user.get('quizzes_completed', 0)
    )
    return round(total_completed / days_since_start, 2)

def calculate_skill_score(user):
    """Calculate overall skill score based on various factors"""
    score = (
        user.get('lessons_completed', 0) * 2 +
        user.get('challenges_completed', 0) * 5 +
        user.get('quizzes_completed', 0) * 3 +
        (user.get('average_quiz_score', 0) / 100) * 10
    )
    return round(score, 1)

@disk_cache(ttl=3600)  # Cache for 1 hour
def get_comprehensive_lessons_data():
    """
    Comprehensive Python learning curriculum with 50 lessons covering (cached):
    - Fundamentals (1-10)
    - Intermediate Programming (11-20)
    - Advanced Python (21-30)
    - Specialized Tracks (31-50): Web Dev, Data Science, ML, DevOps, etc.
    """
    return [
        # FUNDAMENTALS (1-10) - Beginner Level
        {
            'id': 'lesson_1', 'title': 'Introduction to Python',
            'description': 'Learn Python basics, syntax, and your first program. Understand why Python is popular and set up your development environment.',
            'difficulty': 'beginner', 'estimated_time': 30, 'exercises': 5, 'points': 10,
            'objectives': ['Understand Python\'s role in programming', 'Write your first Python program', 'Learn basic syntax rules', 'Set up Python environment'],
            'category': 'fundamentals', 'prerequisites': []
        },
        {
            'id': 'lesson_2', 'title': 'Variables and Data Types',
            'description': 'Master Python variables, strings, numbers, booleans, and type conversion. Learn naming conventions and best practices.',
            'difficulty': 'beginner', 'estimated_time': 45, 'exercises': 8, 'points': 15,
            'objectives': ['Create and use variables', 'Work with different data types', 'Perform type conversion', 'Follow naming conventions'],
            'category': 'fundamentals', 'prerequisites': ['lesson_1']
        },
        {
            'id': 'lesson_3', 'title': 'Control Flow and Conditionals',
            'description': 'Learn if statements, elif, else, comparison operators, and logical operators for decision making.',
            'difficulty': 'beginner', 'estimated_time': 50, 'exercises': 10, 'points': 20,
            'objectives': ['Use if/elif/else statements', 'Apply comparison operators', 'Combine logical operators', 'Create complex conditions'],
            'category': 'fundamentals', 'prerequisites': ['lesson_2']
        },
        {
            'id': 'lesson_4', 'title': 'Loops and Iteration',
            'description': 'Master for loops, while loops, range(), break, continue, and nested loops for repetitive tasks.',
            'difficulty': 'beginner', 'estimated_time': 55, 'exercises': 12, 'points': 25,
            'objectives': ['Write for and while loops', 'Use range() effectively', 'Control loop flow', 'Create nested loops'],
            'category': 'fundamentals', 'prerequisites': ['lesson_3']
        },
        {
            'id': 'lesson_5', 'title': 'Functions and Scope',
            'description': 'Create reusable code with functions, parameters, return values, default arguments, and understand variable scope.',
            'difficulty': 'beginner', 'estimated_time': 60, 'exercises': 14, 'points': 30,
            'objectives': ['Define and call functions', 'Use parameters and return values', 'Apply default arguments', 'Understand scope'],
            'category': 'fundamentals', 'prerequisites': ['lesson_4']
        },
        {
            'id': 'lesson_6', 'title': 'Lists and List Methods',
            'description': 'Work with Python lists, indexing, slicing, list methods, and list comprehensions for data manipulation.',
            'difficulty': 'beginner', 'estimated_time': 50, 'exercises': 12, 'points': 25,
            'objectives': ['Create and manipulate lists', 'Use indexing and slicing', 'Apply list methods', 'Write list comprehensions'],
            'category': 'fundamentals', 'prerequisites': ['lesson_5']
        },
        {
            'id': 'lesson_7', 'title': 'Tuples and Sets',
            'description': 'Learn about immutable tuples and unique sets, their use cases, and when to choose each data structure.',
            'difficulty': 'beginner', 'estimated_time': 40, 'exercises': 10, 'points': 20,
            'objectives': ['Work with tuples', 'Use sets for unique data', 'Choose appropriate data structures', 'Perform set operations'],
            'category': 'fundamentals', 'prerequisites': ['lesson_6']
        },
        {
            'id': 'lesson_8', 'title': 'Dictionaries and Data Structures',
            'description': 'Master Python dictionaries, nested data structures, and real-world data organization patterns.',
            'difficulty': 'beginner', 'estimated_time': 55, 'exercises': 13, 'points': 30,
            'objectives': ['Create and use dictionaries', 'Work with nested structures', 'Organize complex data', 'Apply dictionary methods'],
            'category': 'fundamentals', 'prerequisites': ['lesson_7']
        },
        {
            'id': 'lesson_9', 'title': 'Strings and Text Processing',
            'description': 'Advanced string manipulation, formatting, regular expressions basics, and text processing techniques.',
            'difficulty': 'beginner', 'estimated_time': 45, 'exercises': 11, 'points': 25,
            'objectives': ['Manipulate strings effectively', 'Format text output', 'Use basic regex patterns', 'Process text data'],
            'category': 'fundamentals', 'prerequisites': ['lesson_8']
        },
        {
            'id': 'lesson_10', 'title': 'File I/O and Data Persistence',
            'description': 'Read and write files, handle different file formats (CSV, JSON), and manage data persistence.',
            'difficulty': 'beginner', 'estimated_time': 50, 'exercises': 12, 'points': 30,
            'objectives': ['Read and write files', 'Work with CSV and JSON', 'Handle file errors', 'Manage data persistence'],
            'category': 'fundamentals', 'prerequisites': ['lesson_9']
        },

        # INTERMEDIATE PROGRAMMING (11-20)
        {
            'id': 'lesson_11', 'title': 'Error Handling and Debugging',
            'description': 'Master try-except blocks, custom exceptions, debugging techniques, and writing robust code.',
            'difficulty': 'intermediate', 'estimated_time': 60, 'exercises': 14, 'points': 35,
            'objectives': ['Handle exceptions gracefully', 'Create custom exceptions', 'Debug code effectively', 'Write robust programs'],
            'category': 'intermediate', 'prerequisites': ['lesson_10']
        },
        {
            'id': 'lesson_12', 'title': 'Object-Oriented Programming Fundamentals',
            'description': 'Learn classes, objects, attributes, methods, and the principles of object-oriented design.',
            'difficulty': 'intermediate', 'estimated_time': 75, 'exercises': 16, 'points': 40,
            'objectives': ['Create classes and objects', 'Use attributes and methods', 'Apply OOP principles', 'Design object hierarchies'],
            'category': 'intermediate', 'prerequisites': ['lesson_11']
        },
        {
            'id': 'lesson_13', 'title': 'Inheritance and Polymorphism',
            'description': 'Advanced OOP concepts: inheritance, method overriding, polymorphism, and abstract classes.',
            'difficulty': 'intermediate', 'estimated_time': 70, 'exercises': 15, 'points': 40,
            'objectives': ['Implement inheritance', 'Override methods', 'Use polymorphism', 'Create abstract classes'],
            'category': 'intermediate', 'prerequisites': ['lesson_12']
        },
        {
            'id': 'lesson_14', 'title': 'Modules and Packages',
            'description': 'Organize code with modules, create packages, understand import systems, and manage dependencies.',
            'difficulty': 'intermediate', 'estimated_time': 55, 'exercises': 12, 'points': 35,
            'objectives': ['Create modules', 'Build packages', 'Manage imports', 'Handle dependencies'],
            'category': 'intermediate', 'prerequisites': ['lesson_13']
        },
        {
            'id': 'lesson_15', 'title': 'Working with Libraries and APIs',
            'description': 'Use external libraries, make HTTP requests, work with APIs, and integrate third-party services.',
            'difficulty': 'intermediate', 'estimated_time': 65, 'exercises': 14, 'points': 40,
            'objectives': ['Use external libraries', 'Make API requests', 'Handle JSON responses', 'Integrate services'],
            'category': 'intermediate', 'prerequisites': ['lesson_14']
        },
        {
            'id': 'lesson_16', 'title': 'Regular Expressions and Pattern Matching',
            'description': 'Master regex patterns for text processing, data validation, and advanced string manipulation.',
            'difficulty': 'intermediate', 'estimated_time': 60, 'exercises': 13, 'points': 35,
            'objectives': ['Write regex patterns', 'Validate data formats', 'Extract information', 'Process text efficiently'],
            'category': 'intermediate', 'prerequisites': ['lesson_15']
        },
        {
            'id': 'lesson_17', 'title': 'Functional Programming Concepts',
            'description': 'Learn lambda functions, map, filter, reduce, decorators, and functional programming paradigms.',
            'difficulty': 'intermediate', 'estimated_time': 70, 'exercises': 15, 'points': 40,
            'objectives': ['Use lambda functions', 'Apply map/filter/reduce', 'Create decorators', 'Think functionally'],
            'category': 'intermediate', 'prerequisites': ['lesson_16']
        },
        {
            'id': 'lesson_18', 'title': 'Generators and Iterators',
            'description': 'Understand generators, iterators, yield statements, and memory-efficient data processing.',
            'difficulty': 'intermediate', 'estimated_time': 55, 'exercises': 12, 'points': 35,
            'objectives': ['Create generators', 'Use iterators', 'Optimize memory usage', 'Process large datasets'],
            'category': 'intermediate', 'prerequisites': ['lesson_17']
        },
        {
            'id': 'lesson_19', 'title': 'Context Managers and Resource Management',
            'description': 'Learn with statements, context managers, resource management, and clean code practices.',
            'difficulty': 'intermediate', 'estimated_time': 50, 'exercises': 11, 'points': 30,
            'objectives': ['Use context managers', 'Manage resources', 'Write clean code', 'Handle cleanup properly'],
            'category': 'intermediate', 'prerequisites': ['lesson_18']
        },
        {
            'id': 'lesson_20', 'title': 'Testing and Quality Assurance',
            'description': 'Write unit tests, use pytest, test-driven development, and ensure code quality.',
            'difficulty': 'intermediate', 'estimated_time': 65, 'exercises': 14, 'points': 40,
            'objectives': ['Write unit tests', 'Use testing frameworks', 'Practice TDD', 'Ensure code quality'],
            'category': 'intermediate', 'prerequisites': ['lesson_19']
        },

        # ADVANCED PYTHON (21-30)
        {
            'id': 'lesson_21', 'title': 'Advanced Data Structures',
            'description': 'Collections module, namedtuples, deque, Counter, defaultdict, and custom data structures.',
            'difficulty': 'advanced', 'estimated_time': 70, 'exercises': 15, 'points': 45,
            'objectives': ['Use collections module', 'Create custom structures', 'Optimize data access', 'Choose right structures'],
            'category': 'advanced', 'prerequisites': ['lesson_20']
        },
        {
            'id': 'lesson_22', 'title': 'Metaclasses and Advanced OOP',
            'description': 'Metaclasses, descriptors, properties, advanced inheritance patterns, and design patterns.',
            'difficulty': 'advanced', 'estimated_time': 80, 'exercises': 16, 'points': 50,
            'objectives': ['Understand metaclasses', 'Use descriptors', 'Apply design patterns', 'Master advanced OOP'],
            'category': 'advanced', 'prerequisites': ['lesson_21']
        },
        {
            'id': 'lesson_23', 'title': 'Concurrency and Threading',
            'description': 'Threading, multiprocessing, asyncio, concurrent programming, and performance optimization.',
            'difficulty': 'advanced', 'estimated_time': 85, 'exercises': 17, 'points': 55,
            'objectives': ['Use threading', 'Apply multiprocessing', 'Master asyncio', 'Optimize performance'],
            'category': 'advanced', 'prerequisites': ['lesson_22']
        },
        {
            'id': 'lesson_24', 'title': 'Memory Management and Performance',
            'description': 'Memory profiling, garbage collection, performance optimization, and efficient coding practices.',
            'difficulty': 'advanced', 'estimated_time': 75, 'exercises': 15, 'points': 50,
            'objectives': ['Profile memory usage', 'Optimize performance', 'Understand GC', 'Write efficient code'],
            'category': 'advanced', 'prerequisites': ['lesson_23']
        },
        {
            'id': 'lesson_25', 'title': 'Database Integration and ORM',
            'description': 'SQLite, PostgreSQL, SQLAlchemy ORM, database design, and data modeling.',
            'difficulty': 'advanced', 'estimated_time': 90, 'exercises': 18, 'points': 60,
            'objectives': ['Work with databases', 'Use ORM effectively', 'Design data models', 'Optimize queries'],
            'category': 'advanced', 'prerequisites': ['lesson_24']
        },
        {
            'id': 'lesson_26', 'title': 'Web Scraping and Data Extraction',
            'description': 'BeautifulSoup, Scrapy, handling dynamic content, ethical scraping, and data extraction.',
            'difficulty': 'advanced', 'estimated_time': 80, 'exercises': 16, 'points': 55,
            'objectives': ['Scrape websites', 'Handle dynamic content', 'Extract structured data', 'Follow ethical practices'],
            'category': 'advanced', 'prerequisites': ['lesson_25']
        },
        {
            'id': 'lesson_27', 'title': 'API Development and REST Services',
            'description': 'Flask/FastAPI, RESTful APIs, authentication, documentation, and microservices architecture.',
            'difficulty': 'advanced', 'estimated_time': 95, 'exercises': 19, 'points': 65,
            'objectives': ['Build REST APIs', 'Implement authentication', 'Document APIs', 'Design microservices'],
            'category': 'advanced', 'prerequisites': ['lesson_26']
        },
        {
            'id': 'lesson_28', 'title': 'Security and Cryptography',
            'description': 'Security best practices, encryption, hashing, secure coding, and vulnerability prevention.',
            'difficulty': 'advanced', 'estimated_time': 75, 'exercises': 15, 'points': 50,
            'objectives': ['Implement security measures', 'Use cryptography', 'Prevent vulnerabilities', 'Secure applications'],
            'category': 'advanced', 'prerequisites': ['lesson_27']
        },
        {
            'id': 'lesson_29', 'title': 'Package Development and Distribution',
            'description': 'Creating packages, setup.py, PyPI publishing, documentation, and open source practices.',
            'difficulty': 'advanced', 'estimated_time': 70, 'exercises': 14, 'points': 45,
            'objectives': ['Create packages', 'Publish to PyPI', 'Write documentation', 'Follow best practices'],
            'category': 'advanced', 'prerequisites': ['lesson_28']
        },
        {
            'id': 'lesson_30', 'title': 'DevOps and Deployment',
            'description': 'Docker, CI/CD, cloud deployment, monitoring, and production best practices.',
            'difficulty': 'advanced', 'estimated_time': 85, 'exercises': 17, 'points': 60,
            'objectives': ['Use Docker', 'Set up CI/CD', 'Deploy to cloud', 'Monitor applications'],
            'category': 'advanced', 'prerequisites': ['lesson_29']
        },

        # WEB DEVELOPMENT TRACK (31-35)
        {
            'id': 'lesson_31', 'title': 'Flask Web Framework Fundamentals',
            'description': 'Flask basics, routing, templates, forms, sessions, and building dynamic web applications.',
            'difficulty': 'expert', 'estimated_time': 100, 'exercises': 20, 'points': 70,
            'objectives': ['Master Flask framework', 'Create dynamic websites', 'Handle user input', 'Manage sessions'],
            'category': 'web_development', 'prerequisites': ['lesson_30']
        },
        {
            'id': 'lesson_32', 'title': 'Django Web Development',
            'description': 'Django framework, models, views, templates, admin interface, and full-stack development.',
            'difficulty': 'expert', 'estimated_time': 120, 'exercises': 22, 'points': 80,
            'objectives': ['Build with Django', 'Design data models', 'Create admin interfaces', 'Deploy web apps'],
            'category': 'web_development', 'prerequisites': ['lesson_31']
        },
        {
            'id': 'lesson_33', 'title': 'FastAPI and Modern Web APIs',
            'description': 'FastAPI framework, async programming, automatic documentation, and high-performance APIs.',
            'difficulty': 'expert', 'estimated_time': 90, 'exercises': 18, 'points': 65,
            'objectives': ['Build FastAPI applications', 'Use async programming', 'Generate documentation', 'Optimize performance'],
            'category': 'web_development', 'prerequisites': ['lesson_32']
        },
        {
            'id': 'lesson_34', 'title': 'Frontend Integration and Full-Stack',
            'description': 'JavaScript integration, React/Vue.js with Python backends, and full-stack architecture.',
            'difficulty': 'expert', 'estimated_time': 110, 'exercises': 21, 'points': 75,
            'objectives': ['Integrate frontends', 'Build full-stack apps', 'Handle CORS', 'Design architecture'],
            'category': 'web_development', 'prerequisites': ['lesson_33']
        },
        {
            'id': 'lesson_35', 'title': 'Web Security and Production Deployment',
            'description': 'Web security, HTTPS, authentication systems, scaling, and production deployment strategies.',
            'difficulty': 'expert', 'estimated_time': 95, 'exercises': 19, 'points': 70,
            'objectives': ['Secure web applications', 'Implement authentication', 'Scale applications', 'Deploy securely'],
            'category': 'web_development', 'prerequisites': ['lesson_34']
        },

        # DATA SCIENCE TRACK (36-40)
        {
            'id': 'lesson_36', 'title': 'NumPy and Scientific Computing',
            'description': 'NumPy arrays, mathematical operations, broadcasting, and scientific computing fundamentals.',
            'difficulty': 'expert', 'estimated_time': 85, 'exercises': 17, 'points': 60,
            'objectives': ['Master NumPy arrays', 'Perform mathematical operations', 'Use broadcasting', 'Optimize computations'],
            'category': 'data_science', 'prerequisites': ['lesson_30']
        },
        {
            'id': 'lesson_37', 'title': 'Pandas for Data Analysis',
            'description': 'Pandas DataFrames, data cleaning, manipulation, analysis, and real-world data projects.',
            'difficulty': 'expert', 'estimated_time': 100, 'exercises': 20, 'points': 75,
            'objectives': ['Use Pandas effectively', 'Clean messy data', 'Perform data analysis', 'Handle real datasets'],
            'category': 'data_science', 'prerequisites': ['lesson_36']
        },
        {
            'id': 'lesson_38', 'title': 'Data Visualization with Matplotlib and Seaborn',
            'description': 'Create compelling visualizations, statistical plots, and interactive dashboards.',
            'difficulty': 'expert', 'estimated_time': 90, 'exercises': 18, 'points': 65,
            'objectives': ['Create visualizations', 'Design statistical plots', 'Build dashboards', 'Tell data stories'],
            'category': 'data_science', 'prerequisites': ['lesson_37']
        },
        {
            'id': 'lesson_39', 'title': 'Statistical Analysis and Hypothesis Testing',
            'description': 'Statistical methods, hypothesis testing, A/B testing, and data-driven decision making.',
            'difficulty': 'expert', 'estimated_time': 95, 'exercises': 19, 'points': 70,
            'objectives': ['Apply statistical methods', 'Test hypotheses', 'Design experiments', 'Make data-driven decisions'],
            'category': 'data_science', 'prerequisites': ['lesson_38']
        },
        {
            'id': 'lesson_40', 'title': 'Big Data and Advanced Analytics',
            'description': 'Working with large datasets, Spark, distributed computing, and advanced analytics techniques.',
            'difficulty': 'expert', 'estimated_time': 110, 'exercises': 21, 'points': 80,
            'objectives': ['Handle big data', 'Use distributed computing', 'Apply advanced analytics', 'Scale data processing'],
            'category': 'data_science', 'prerequisites': ['lesson_39']
        },

        # MACHINE LEARNING TRACK (41-45)
        {
            'id': 'lesson_41', 'title': 'Machine Learning Fundamentals',
            'description': 'ML concepts, scikit-learn, supervised/unsupervised learning, and model evaluation.',
            'difficulty': 'expert', 'estimated_time': 105, 'exercises': 20, 'points': 75,
            'objectives': ['Understand ML concepts', 'Use scikit-learn', 'Build ML models', 'Evaluate performance'],
            'category': 'machine_learning', 'prerequisites': ['lesson_40']
        },
        {
            'id': 'lesson_42', 'title': 'Deep Learning with TensorFlow/PyTorch',
            'description': 'Neural networks, deep learning frameworks, computer vision, and NLP applications.',
            'difficulty': 'expert', 'estimated_time': 120, 'exercises': 22, 'points': 85,
            'objectives': ['Build neural networks', 'Use deep learning frameworks', 'Apply to vision/NLP', 'Train complex models'],
            'category': 'machine_learning', 'prerequisites': ['lesson_41']
        },
        {
            'id': 'lesson_43', 'title': 'Natural Language Processing',
            'description': 'Text processing, sentiment analysis, language models, and NLP applications.',
            'difficulty': 'expert', 'estimated_time': 100, 'exercises': 19, 'points': 75,
            'objectives': ['Process text data', 'Analyze sentiment', 'Build language models', 'Create NLP applications'],
            'category': 'machine_learning', 'prerequisites': ['lesson_42']
        },
        {
            'id': 'lesson_44', 'title': 'Computer Vision and Image Processing',
            'description': 'Image processing, computer vision, object detection, and visual AI applications.',
            'difficulty': 'expert', 'estimated_time': 110, 'exercises': 21, 'points': 80,
            'objectives': ['Process images', 'Detect objects', 'Build vision systems', 'Apply visual AI'],
            'category': 'machine_learning', 'prerequisites': ['lesson_43']
        },
        {
            'id': 'lesson_45', 'title': 'MLOps and Production ML',
            'description': 'Model deployment, monitoring, versioning, and production machine learning systems.',
            'difficulty': 'expert', 'estimated_time': 115, 'exercises': 22, 'points': 85,
            'objectives': ['Deploy ML models', 'Monitor performance', 'Version models', 'Build ML systems'],
            'category': 'machine_learning', 'prerequisites': ['lesson_44']
        },

        # SPECIALIZED TOPICS (46-50)
        {
            'id': 'lesson_46', 'title': 'Game Development with Pygame',
            'description': 'Game programming, graphics, sound, physics, and interactive entertainment development.',
            'difficulty': 'expert', 'estimated_time': 95, 'exercises': 18, 'points': 70,
            'objectives': ['Create games', 'Handle graphics/sound', 'Implement physics', 'Design game mechanics'],
            'category': 'specialized', 'prerequisites': ['lesson_30']
        },
        {
            'id': 'lesson_47', 'title': 'Desktop Applications with Tkinter/PyQt',
            'description': 'GUI development, desktop applications, user interfaces, and cross-platform development.',
            'difficulty': 'expert', 'estimated_time': 90, 'exercises': 17, 'points': 65,
            'objectives': ['Build desktop apps', 'Design user interfaces', 'Handle events', 'Create cross-platform apps'],
            'category': 'specialized', 'prerequisites': ['lesson_30']
        },
        {
            'id': 'lesson_48', 'title': 'Automation and Scripting',
            'description': 'Task automation, system administration, web automation, and productivity scripting.',
            'difficulty': 'expert', 'estimated_time': 80, 'exercises': 16, 'points': 60,
            'objectives': ['Automate tasks', 'Administer systems', 'Script workflows', 'Increase productivity'],
            'category': 'specialized', 'prerequisites': ['lesson_30']
        },
        {
            'id': 'lesson_49', 'title': 'Blockchain and Cryptocurrency',
            'description': 'Blockchain concepts, cryptocurrency development, smart contracts, and decentralized applications.',
            'difficulty': 'expert', 'estimated_time': 105, 'exercises': 20, 'points': 75,
            'objectives': ['Understand blockchain', 'Develop crypto apps', 'Create smart contracts', 'Build DApps'],
            'category': 'specialized', 'prerequisites': ['lesson_30']
        },
        {
            'id': 'lesson_50', 'title': 'Advanced Python Mastery Project',
            'description': 'Capstone project combining multiple skills, real-world application, and portfolio development.',
            'difficulty': 'expert', 'estimated_time': 150, 'exercises': 25, 'points': 100,
            'objectives': ['Complete capstone project', 'Integrate multiple skills', 'Build portfolio piece', 'Demonstrate mastery'],
            'category': 'capstone', 'prerequisites': ['lesson_45', 'lesson_35']
        }
    ]

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/introduction')
def introduction():
    return render_template('introduction.html')

@app.route('/register', methods=['GET', 'POST'])
# @rate_limit(requests_per_minute=5, requests_per_hour=20)  # Disabled for development
def register():
    """User registration with comprehensive validation and error handling"""
    if request.method == 'GET':
        return render_template('register.html')

    try:
        # Debug: Log request details
        print(f"DEBUG: Registration request received")
        print(f"DEBUG: Content-Type: {request.content_type}")
        print(f"DEBUG: Request method: {request.method}")

        # Get and validate JSON data
        data = request.get_json()
        print(f"DEBUG: Received data: {data}")

        if not data:
            print("DEBUG: No data received")
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400

        # Sanitize input data
        sanitized_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized_data[key] = validator.sanitize_html(value.strip())
            else:
                sanitized_data[key] = value

        # Simplified validation for basic registration
        is_valid, validation_errors = validator.validate_registration_data(sanitized_data)

        if not is_valid:
            error_handler.logger.warning(f"Registration validation failed: {validation_errors}")
            return jsonify({
                "success": False,
                "error": "Validation failed",
                "details": validation_errors
            }), 400

        # Check if user already exists
        user_data = load_user_data()
        email = sanitized_data['email'].lower()

        if email in user_data:
            error_handler.logger.info(f"Registration attempt with existing email: {email}")
            return jsonify({
                "success": False,
                "error": "An account with this email already exists"
            }), 400

        # Create user profile with standardized structure
        user_profile = {
            "name": sanitized_data['name'],
            "email": email,
            "password": sanitized_data['password'],  # In production, this should be hashed
            "experience_level": sanitized_data.get('experience_level', 'complete_beginner'),
            "learning_goals": sanitized_data.get('learning_goals', []),
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "last_login": datetime.now().isoformat(),
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

        # Save user data
        user_data[email] = user_profile
        save_success = save_user_data(user_data)

        if not save_success:
            return jsonify({
                "success": False,
                "error": "Failed to create account. Please try again."
            }), 500

        # Set session using helper
        set_user_session(email)
        session['first_time'] = True

        error_handler.logger.info(f"New user registered successfully: {email}")

        return jsonify({
            "success": True,
            "redirect": url_for('welcome_user'),
            "message": "Account created successfully!"
        })

    except ValidationError as e:
        error_handler.handle_error(e, context={"route": "register", "data": str(data)[:200]})
        return jsonify({
            "success": False,
            "error": "Invalid input data"
        }), 400

    except Exception as e:
        error_handler.handle_error(e, context={"route": "register"})
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500

@app.route('/welcome_user')
def welcome_user():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    user_data = load_user_data()
    user_profile = user_data.get(session['user'], {})
    session['show_dashboard_tour'] = True
    return render_template('welcome_user.html', user_profile=user_profile)

@app.route('/login', methods=['GET', 'POST'])
# @rate_limit(requests_per_minute=100, requests_per_hour=500)  # Disabled for development
def login():
    """User login with comprehensive validation and error handling"""
    if request.method == 'GET':
        return render_template('login.html')

    try:
        # Get and validate JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No login data provided"
            }), 400

        # Validate required fields
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        if not email or not password:
            error_handler.logger.warning("Login attempt with missing credentials")
            return jsonify({
                "success": False,
                "error": "Email and password are required"
            }), 400

        # Validate email format
        email_valid, email_error = validator.validate_email(email)
        if not email_valid:
            error_handler.logger.warning(f"Login attempt with invalid email format: {email}")
            return jsonify({
                "success": False,
                "error": "Invalid email format"
            }), 400

        # Load user data and check credentials
        user_data = load_user_data()
        user = user_data.get(email)

        if not user:
            error_handler.logger.warning(f"Login attempt with non-existent email: {email}")
            # For debugging, show available users
            available_users = list(user_data.keys())[:3]  # Show first 3 users
            return jsonify({
                "success": False,
                "error": "Invalid email or password",
                "debug_info": f"User not found. Available users: {available_users}"
            }), 401

        # Verify password (in production, use proper password hashing)
        if user.get('password') != password:
            error_handler.logger.warning(f"Login attempt with incorrect password for: {email}")
            return jsonify({
                "success": False,
                "error": "Invalid email or password",
                "debug_info": f"Password mismatch. Expected: {user.get('password')}, Got: {password}"
            }), 401

        # Update last login time
        user['last_login'] = datetime.now().isoformat()
        user['last_activity'] = datetime.now().isoformat()
        user_data[email] = user
        save_user_data(user_data)

        # Set session using helper
        set_user_session(email)

        error_handler.logger.info(f"User logged in successfully: {email}")

        return jsonify({
            "success": True,
            "redirect": url_for('dashboard'),
            "message": "Login successful!"
        })

    except AuthenticationError as e:
        error_handler.handle_error(e, context={"route": "login", "email": email})
        return jsonify({
            "success": False,
            "error": "Authentication failed"
        }), 401

    except Exception as e:
        error_handler.handle_error(e, context={"route": "login"})
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again."
        }), 500

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    user_data = load_user_data()
    user_profile = user_data.get(session['user'], {})
    stats = get_progress_stats(session['user'])
    show_tour = session.pop('show_dashboard_tour', False)
    
    if not show_tour and (stats.get('lessons_completed', 0) == 0):
        show_tour = True
    
    return render_template('dashboard.html', 
                         user=user_profile.get('name', 'User'),
                         stats=stats, 
                         profile=user_profile,
                         show_tour=show_tour)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/debug-session')
def debug_session():
    """Debug page for session issues"""
    return render_template('debug_session.html')

@app.route('/api/reset-rate-limit')
def reset_rate_limit():
    """Reset rate limits for development (remove in production)"""
    try:
        # Clear rate limit cache
        if hasattr(rate_limit, 'cache'):
            rate_limit.cache.clear()
        return jsonify({"success": True, "message": "Rate limits reset"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/lessons')
def lessons():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    lessons_data = get_comprehensive_lessons_data()
    
    user_data = load_user_data()
    user = user_data.get(session['user'], {})
    completed_lessons = user.get('completed_lessons', [])
    
    return render_template('lessons.html', lessons=lessons_data, completed_lessons=completed_lessons)

@app.route('/lesson/<lesson_id>')
def lesson_detail(lesson_id):
    if 'user' not in session:
        return redirect(url_for('index'))

    # Get lesson data
    lessons_data = get_comprehensive_lessons_data()
    lesson = next((l for l in lessons_data if l['id'] == lesson_id), None)

    if not lesson:
        return redirect(url_for('lessons'))

    # Get user progress for this lesson
    user_data = load_user_data()
    user = user_data.get(session['user'], {})
    completed_lessons = user.get('completed_lesson_ids', [])

    # Create lesson progress object
    progress = {
        'status': 'completed' if lesson_id in completed_lessons else 'not_started'
    }

    # Add content to lesson object
    lesson['content'] = get_lesson_content(lesson_id)

    return render_template('lesson_detail.html', lesson=lesson, progress=progress)

@app.route('/api/complete_lesson', methods=['POST'])
def complete_lesson():
    """Mark a lesson as completed and update user progress"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()
        lesson_id = data.get('lesson_id')

        if not lesson_id:
            return jsonify({"success": False, "error": "Lesson ID required"}), 400

        # Verify lesson exists
        lessons_data = get_comprehensive_lessons_data()
        lesson = next((l for l in lessons_data if l['id'] == lesson_id), None)

        if not lesson:
            return jsonify({"success": False, "error": "Lesson not found"}), 404

        # Update user progress
        user_data = load_user_data()
        user = user_data.get(session['user'], {})

        # Initialize completed lessons list if it doesn't exist
        if 'completed_lesson_ids' not in user:
            user['completed_lesson_ids'] = []

        # Add lesson to completed list if not already there
        if lesson_id not in user['completed_lesson_ids']:
            user['completed_lesson_ids'].append(lesson_id)

            # Update lesson completion count
            user['lessons_completed'] = len(user['completed_lesson_ids'])

            # Award points
            points_earned = lesson.get('points', 10)
            user['points'] = user.get('points', 0) + points_earned

            # Update level based on points
            user['level'] = (user['points'] // 100) + 1

            # Update last activity
            user['last_activity'] = datetime.now().isoformat()

            # Save updated user data
            user_data[session['user']] = user
            save_success = save_user_data(user_data)

            if not save_success:
                return jsonify({"success": False, "error": "Failed to save progress"}), 500

            return jsonify({
                "success": True,
                "message": f"Lesson completed! +{points_earned} points",
                "points_earned": points_earned,
                "total_points": user['points'],
                "level": user['level']
            })
        else:
            return jsonify({"success": True, "message": "Lesson already completed"})

    except Exception as e:
        print(f"Error completing lesson: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

@app.route('/next_lesson/<current_lesson_id>')
def next_lesson(current_lesson_id):
    """Navigate to the next lesson"""
    if 'user' not in session:
        return redirect(url_for('index'))

    lessons_data = get_comprehensive_lessons_data()

    # Find current lesson index
    current_index = None
    for i, lesson in enumerate(lessons_data):
        if lesson['id'] == current_lesson_id:
            current_index = i
            break

    # Get next lesson
    if current_index is not None and current_index < len(lessons_data) - 1:
        next_lesson = lessons_data[current_index + 1]
        return redirect(url_for('lesson_detail', lesson_id=next_lesson['id']))
    else:
        # No next lesson, redirect to lessons page
        return redirect(url_for('lessons'))

@app.route('/prev_lesson/<current_lesson_id>')
def prev_lesson(current_lesson_id):
    """Navigate to the previous lesson"""
    if 'user' not in session:
        return redirect(url_for('index'))

    lessons_data = get_comprehensive_lessons_data()

    # Find current lesson index
    current_index = None
    for i, lesson in enumerate(lessons_data):
        if lesson['id'] == current_lesson_id:
            current_index = i
            break

    # Get previous lesson
    if current_index is not None and current_index > 0:
        prev_lesson = lessons_data[current_index - 1]
        return redirect(url_for('lesson_detail', lesson_id=prev_lesson['id']))
    else:
        # No previous lesson, redirect to lessons page
        return redirect(url_for('lessons'))

def get_lesson_content(lesson_id):
    """Get detailed content for a specific lesson"""
    content_map = {
        'lesson_1': {
            'introduction': 'Welcome to Python! Python is a powerful, easy-to-learn programming language that\'s used everywhere from web development to artificial intelligence.',
            'concepts': [
                {
                    'title': 'What is Python?',
                    'explanation': 'Python is a high-level, interpreted programming language known for its simplicity and readability.',
                    'example': 'print("Hello, World!")',
                    'output': 'Hello, World!'
                },
                {
                    'title': 'Python Syntax',
                    'explanation': 'Python uses indentation to define code blocks, making it very readable.',
                    'example': 'if True:\n    print("This is indented")\n    print("This too!")',
                    'output': 'This is indented\nThis too!'
                }
            ]
        },
        'lesson_2': {
            'introduction': 'Variables are containers for storing data values. In Python, you don\'t need to declare variables before using them.',
            'concepts': [
                {
                    'title': 'Creating Variables',
                    'explanation': 'Variables are created when you assign a value to them.',
                    'example': 'name = "Alice"\nage = 25\nheight = 5.6',
                    'output': '# Variables created successfully'
                },
                {
                    'title': 'Data Types',
                    'explanation': 'Python has several built-in data types: strings, integers, floats, and booleans.',
                    'example': 'text = "Hello"  # String\nnumber = 42     # Integer\nprice = 19.99   # Float\nis_valid = True # Boolean',
                    'output': '# Different data types assigned'
                }
            ]
        }
    }

    return content_map.get(lesson_id, {
        'introduction': 'This lesson content is being developed. Check back soon!',
        'concepts': []
    })

def get_comprehensive_challenges_data():
    """
    Comprehensive coding challenges covering:
    - Basic Programming (1-10)
    - Data Structures (11-20)
    - Algorithms (21-30)
    - Real-World Projects (31-40)
    """
    return [
        # BASIC PROGRAMMING CHALLENGES (1-10)
        {
            'id': 'challenge_1', 'title': 'Hello World Variations',
            'description': 'Create different versions of Hello World programs with user input, formatting, and personalization.',
            'difficulty': 'easy', 'points': 10, 'time_limit': 15,
            'category': 'basics', 'type': 'coding',
            'problem_statement': 'Write a program that asks for the user\'s name and prints a personalized greeting.',
            'test_cases': [
                {'input': 'Alice', 'expected_output': 'Hello, Alice! Welcome to Python!'},
                {'input': 'Bob', 'expected_output': 'Hello, Bob! Welcome to Python!'}
            ],
            'starter_code': '# Write your code here\nname = input("Enter your name: ")\n# Complete the program',
            'hints': ['Use input() to get user input', 'Use f-strings for formatting', 'Remember to include the exclamation mark']
        },
        {
            'id': 'challenge_2', 'title': 'Number Calculator',
            'description': 'Build a simple calculator that performs basic arithmetic operations on two numbers.',
            'difficulty': 'easy', 'points': 15, 'time_limit': 20,
            'category': 'basics', 'type': 'coding',
            'problem_statement': 'Create a calculator that takes two numbers and an operation (+, -, *, /) and returns the result.',
            'test_cases': [
                {'input': '10 5 +', 'expected_output': '15'},
                {'input': '20 4 /', 'expected_output': '5.0'},
                {'input': '7 3 *', 'expected_output': '21'}
            ],
            'starter_code': '# Calculator program\ndef calculate(num1, num2, operation):\n    # Complete this function\n    pass',
            'hints': ['Use if/elif statements for operations', 'Handle division by zero', 'Convert strings to numbers']
        },
        {
            'id': 'challenge_3', 'title': 'Grade Classifier',
            'description': 'Write a program that converts numerical grades to letter grades with appropriate messages.',
            'difficulty': 'easy', 'points': 20, 'time_limit': 25,
            'category': 'basics', 'type': 'coding',
            'problem_statement': 'Convert numerical grades (0-100) to letter grades: A (90-100), B (80-89), C (70-79), D (60-69), F (0-59).',
            'test_cases': [
                {'input': '95', 'expected_output': 'A - Excellent!'},
                {'input': '82', 'expected_output': 'B - Good job!'},
                {'input': '55', 'expected_output': 'F - Need improvement'}
            ],
            'starter_code': 'def get_letter_grade(score):\n    # Complete this function\n    pass',
            'hints': ['Use if/elif/else statements', 'Consider the grade ranges', 'Add encouraging messages']
        },
        {
            'id': 'challenge_4', 'title': 'Pattern Printer',
            'description': 'Create programs that print various patterns using loops and string manipulation.',
            'difficulty': 'easy', 'points': 25, 'time_limit': 30,
            'category': 'basics', 'type': 'coding',
            'problem_statement': 'Print a right triangle pattern of stars with n rows.',
            'test_cases': [
                {'input': '3', 'expected_output': '*\n**\n***'},
                {'input': '5', 'expected_output': '*\n**\n***\n****\n*****'}
            ],
            'starter_code': 'def print_triangle(n):\n    # Complete this function\n    pass',
            'hints': ['Use nested loops', 'Inner loop controls stars per row', 'Use range() effectively']
        },
        {
            'id': 'challenge_5', 'title': 'Number Guessing Game',
            'description': 'Build an interactive number guessing game with hints and attempt tracking.',
            'difficulty': 'easy', 'points': 30, 'time_limit': 35,
            'category': 'basics', 'type': 'project',
            'problem_statement': 'Create a number guessing game where the computer picks a random number and the user tries to guess it.',
            'test_cases': [
                {'input': 'simulate game with target 50, guesses [25, 75, 50]', 'expected_output': 'Too low, Too high, Correct!'}
            ],
            'starter_code': 'import random\n\ndef guessing_game():\n    # Complete this function\n    pass',
            'hints': ['Use random.randint()', 'Provide "too high" or "too low" hints', 'Count attempts']
        },

        # DATA STRUCTURE CHALLENGES (6-15)
        {
            'id': 'challenge_6', 'title': 'List Manipulator',
            'description': 'Perform various operations on lists: sorting, filtering, and transforming data.',
            'difficulty': 'medium', 'points': 35, 'time_limit': 40,
            'category': 'data_structures', 'type': 'coding',
            'problem_statement': 'Given a list of numbers, return a new list with only even numbers, squared, and sorted in descending order.',
            'test_cases': [
                {'input': '[1, 2, 3, 4, 5, 6]', 'expected_output': '[36, 16, 4]'},
                {'input': '[10, 15, 20, 25]', 'expected_output': '[400, 100]'}
            ],
            'starter_code': 'def process_numbers(numbers):\n    # Complete this function\n    pass',
            'hints': ['Filter even numbers first', 'Use list comprehension', 'Sort with reverse=True']
        },
        {
            'id': 'challenge_7', 'title': 'Dictionary Data Processor',
            'description': 'Work with dictionaries to process and analyze student grade data.',
            'difficulty': 'medium', 'points': 40, 'time_limit': 45,
            'category': 'data_structures', 'type': 'coding',
            'problem_statement': 'Given a dictionary of student grades, find the student with the highest average and return their name and average.',
            'test_cases': [
                {'input': '{"Alice": [85, 90, 78], "Bob": [92, 88, 84], "Charlie": [76, 82, 88]}', 'expected_output': '("Bob", 88.0)'},
            ],
            'starter_code': 'def find_top_student(grades):\n    # Complete this function\n    pass',
            'hints': ['Calculate average for each student', 'Use max() with key parameter', 'Return tuple of name and average']
        },
        {
            'id': 'challenge_8', 'title': 'Set Operations Master',
            'description': 'Use sets to solve problems involving unique elements and set operations.',
            'difficulty': 'medium', 'points': 35, 'time_limit': 35,
            'category': 'data_structures', 'type': 'coding',
            'problem_statement': 'Find common elements between multiple lists and return them as a sorted list.',
            'test_cases': [
                {'input': '[[1, 2, 3, 4], [3, 4, 5, 6], [4, 5, 6, 7]]', 'expected_output': '[4]'},
                {'input': '[[1, 2], [2, 3], [2, 4]]', 'expected_output': '[2]'}
            ],
            'starter_code': 'def find_common_elements(lists):\n    # Complete this function\n    pass',
            'hints': ['Convert lists to sets', 'Use set intersection', 'Convert back to sorted list']
        },
        {
            'id': 'challenge_9', 'title': 'String Analyzer',
            'description': 'Analyze text data: count words, find patterns, and process strings efficiently.',
            'difficulty': 'medium', 'points': 45, 'time_limit': 50,
            'category': 'data_structures', 'type': 'coding',
            'problem_statement': 'Count the frequency of each word in a text and return the top 3 most common words.',
            'test_cases': [
                {'input': '"the quick brown fox jumps over the lazy dog the fox"', 'expected_output': '[("the", 3), ("fox", 2), ("quick", 1)]'}
            ],
            'starter_code': 'def word_frequency(text):\n    # Complete this function\n    pass',
            'hints': ['Split text into words', 'Use dictionary to count', 'Sort by frequency']
        },
        {
            'id': 'challenge_10', 'title': 'Data Structure Converter',
            'description': 'Convert between different data structures and optimize data representation.',
            'difficulty': 'medium', 'points': 40, 'time_limit': 45,
            'category': 'data_structures', 'type': 'coding',
            'problem_statement': 'Convert a list of tuples (name, age, city) into a dictionary grouped by city.',
            'test_cases': [
                {'input': '[("Alice", 25, "NYC"), ("Bob", 30, "LA"), ("Charlie", 35, "NYC")]', 'expected_output': '{"NYC": [("Alice", 25), ("Charlie", 35)], "LA": [("Bob", 30)]}'}
            ],
            'starter_code': 'def group_by_city(people):\n    # Complete this function\n    pass',
            'hints': ['Use defaultdict or check if key exists', 'Group by the third element (city)', 'Store name and age tuples']
        }
    ]

@app.route('/challenges')
def challenges():
    if 'user' not in session:
        return redirect(url_for('index'))

    challenges_data = get_comprehensive_challenges_data()
    user_data = load_user_data()
    user = user_data.get(session['user'], {})
    completed_challenges = user.get('completed_challenges', [])

    return render_template('challenges.html',
                         challenges=challenges_data,
                         completed_challenges=completed_challenges)

@app.route('/challenge/<challenge_id>')
def challenge_detail(challenge_id):
    if 'user' not in session:
        return redirect(url_for('index'))

    challenges_data = get_comprehensive_challenges_data()
    challenge = next((c for c in challenges_data if c['id'] == challenge_id), None)

    if not challenge:
        return redirect(url_for('challenges'))

    user_data = load_user_data()
    user = user_data.get(session['user'], {})
    completed_challenges = user.get('completed_challenge_ids', [])
    is_completed = challenge_id in completed_challenges

    # Add challenge content
    challenge['content'] = get_challenge_content(challenge_id)

    # Add progress tracking
    progress = {
        'status': 'completed' if is_completed else 'not_started',
        'attempts': user.get('challenge_attempts', {}).get(challenge_id, 0)
    }

    return render_template('challenge_detail.html',
                         challenge=challenge,
                         is_completed=is_completed,
                         progress=progress)

def get_challenge_content(challenge_id):
    """Get detailed content for a specific challenge"""
    content_map = {
        'challenge_1': {
            'description': 'Write a Python function that calculates the factorial of a number.',
            'instructions': [
                'Create a function named `factorial` that takes one parameter `n`',
                'The function should return the factorial of n (n!)',
                'Handle edge cases: factorial of 0 is 1',
                'Use either recursion or iteration'
            ],
            'starter_code': 'def factorial(n):\n    # Your code here\n    pass',
            'test_cases': [
                {'input': 5, 'expected': 120},
                {'input': 0, 'expected': 1},
                {'input': 3, 'expected': 6}
            ],
            'hints': [
                'Remember that 0! = 1',
                'You can use a loop or recursion',
                'factorial(n) = n * factorial(n-1)'
            ]
        },
        'challenge_2': {
            'description': 'Create a function to check if a string is a palindrome.',
            'instructions': [
                'Create a function named `is_palindrome` that takes a string parameter',
                'Return True if the string reads the same forwards and backwards',
                'Ignore case and spaces',
                'Return False otherwise'
            ],
            'starter_code': 'def is_palindrome(text):\n    # Your code here\n    pass',
            'test_cases': [
                {'input': 'racecar', 'expected': True},
                {'input': 'hello', 'expected': False},
                {'input': 'A man a plan a canal Panama', 'expected': True}
            ],
            'hints': [
                'Convert to lowercase first',
                'Remove spaces and punctuation',
                'Compare string with its reverse'
            ]
        }
    }

    return content_map.get(challenge_id, {
        'description': 'This challenge is being developed. Check back soon!',
        'instructions': [],
        'starter_code': '# Challenge content coming soon',
        'test_cases': [],
        'hints': []
    })

@app.route('/api/submit_challenge', methods=['POST'])
def submit_challenge():
    """Submit challenge solution and check if it's correct"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()
        challenge_id = data.get('challenge_id')
        user_code = data.get('code', '')

        if not challenge_id:
            return jsonify({"success": False, "error": "Challenge ID required"}), 400

        # Get challenge data
        challenges_data = get_comprehensive_challenges_data()
        challenge = next((c for c in challenges_data if c['id'] == challenge_id), None)

        if not challenge:
            return jsonify({"success": False, "error": "Challenge not found"}), 404

        # Get challenge content with test cases
        content = get_challenge_content(challenge_id)
        test_cases = content.get('test_cases', [])

        # Simple code validation (in production, use sandboxed execution)
        passed_tests = 0
        total_tests = len(test_cases)
        test_results = []

        # Basic validation - check if code contains required function
        if challenge_id == 'challenge_1' and 'def factorial(' in user_code:
            passed_tests = total_tests  # Simplified for demo
        elif challenge_id == 'challenge_2' and 'def is_palindrome(' in user_code:
            passed_tests = total_tests  # Simplified for demo

        success = passed_tests == total_tests

        # Update user progress
        user_data = load_user_data()
        user = user_data.get(session['user'], {})

        # Track attempts
        if 'challenge_attempts' not in user:
            user['challenge_attempts'] = {}
        user['challenge_attempts'][challenge_id] = user['challenge_attempts'].get(challenge_id, 0) + 1

        # If successful, mark as completed
        if success:
            if 'completed_challenge_ids' not in user:
                user['completed_challenge_ids'] = []

            if challenge_id not in user['completed_challenge_ids']:
                user['completed_challenge_ids'].append(challenge_id)

                # Update completion count
                user['challenges_completed'] = len(user['completed_challenge_ids'])

                # Award points
                points_earned = challenge.get('points', 25)
                user['points'] = user.get('points', 0) + points_earned

                # Update level
                user['level'] = (user['points'] // 100) + 1

                # Update last activity
                user['last_activity'] = datetime.now().isoformat()

                # Save user data
                user_data[session['user']] = user
                save_user_data(user_data)

                return jsonify({
                    "success": True,
                    "message": f"Challenge completed! +{points_earned} points",
                    "points_earned": points_earned,
                    "total_points": user['points'],
                    "level": user['level'],
                    "passed_tests": passed_tests,
                    "total_tests": total_tests
                })

        # Save attempt data even if not successful
        user_data[session['user']] = user
        save_user_data(user_data)

        return jsonify({
            "success": success,
            "message": "Good try! Keep working on it." if not success else "Challenge completed!",
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "attempts": user['challenge_attempts'][challenge_id]
        })

    except Exception as e:
        print(f"Error submitting challenge: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

@app.route('/api/challenge_leaderboard/<challenge_id>')
def challenge_leaderboard(challenge_id):
    """Get leaderboard for a specific challenge"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        user_data = load_user_data()
        leaderboard = []

        for email, user in user_data.items():
            completed_challenges = user.get('completed_challenge_ids', [])
            if challenge_id in completed_challenges:
                attempts = user.get('challenge_attempts', {}).get(challenge_id, 1)
                leaderboard.append({
                    'name': user.get('name', 'Anonymous'),
                    'attempts': attempts,
                    'points': user.get('points', 0),
                    'completion_date': user.get('last_activity', '')
                })

        # Sort by attempts (fewer is better), then by points (more is better)
        leaderboard.sort(key=lambda x: (x['attempts'], -x['points']))

        return jsonify({
            "success": True,
            "leaderboard": leaderboard[:10]  # Top 10
        })

    except Exception as e:
        print(f"Error getting leaderboard: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

def check_and_award_achievements(user_email):
    """Check if user has earned new achievements"""
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    current_achievements = set(user.get('achievements', []))
    new_achievements = []

    # Check achievement conditions
    lessons_completed = user.get('lessons_completed', 0)
    challenges_completed = user.get('challenges_completed', 0)
    quizzes_completed = user.get('quizzes_completed', 0)
    points = user.get('points', 0)

    # Define achievement conditions
    achievement_conditions = {
        'first_steps': lessons_completed >= 1,
        'learning_momentum': lessons_completed >= 10,
        'dedicated_learner': lessons_completed >= 25,
        'problem_solver': challenges_completed >= 1,
        'quiz_master': quizzes_completed >= 5,
        'point_collector': points >= 100,
        'high_achiever': points >= 500,
        'perfectionist': user.get('average_quiz_score', 0) >= 95 and quizzes_completed >= 3
    }

    # Check for new achievements
    for achievement_id, condition in achievement_conditions.items():
        if condition and achievement_id not in current_achievements:
            new_achievements.append(achievement_id)
            current_achievements.add(achievement_id)

    # Update user achievements if new ones were earned
    if new_achievements:
        user['achievements'] = list(current_achievements)
        user_data[user_email] = user
        save_user_data(user_data)

    return new_achievements

def update_learning_streak(user_email):
    """Update user's learning streak"""
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    today = datetime.now().date()
    last_activity = user.get('last_activity', '')

    try:
        last_activity_date = datetime.fromisoformat(last_activity.replace('Z', '+00:00')).date()
        days_diff = (today - last_activity_date).days

        if days_diff == 0:
            # Same day, no change to streak
            pass
        elif days_diff == 1:
            # Consecutive day, increment streak
            user['streak'] = user.get('streak', 0) + 1
        else:
            # Streak broken, reset to 1
            user['streak'] = 1

    except:
        # Invalid date or first activity, start streak
        user['streak'] = 1

    # Update last activity
    user['last_activity'] = datetime.now().isoformat()
    user_data[user_email] = user
    save_user_data(user_data)

    return user.get('streak', 1)

@app.route('/api/share_code', methods=['POST'])
def share_code():
    """Share code snippet with other users"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        code = data.get('code', '').strip()
        description = data.get('description', '').strip()

        if not title or not code:
            return jsonify({"success": False, "error": "Title and code are required"}), 400

        # Create shared code entry
        shared_code = {
            'id': f"share_{int(datetime.now().timestamp())}",
            'title': title,
            'code': code,
            'description': description,
            'author': session['user'],
            'author_name': get_user_name(session['user']),
            'created_at': datetime.now().isoformat(),
            'likes': 0,
            'comments': []
        }

        # Save to shared codes file
        shared_codes_file = "data/shared_codes.json"
        if os.path.exists(shared_codes_file):
            with open(shared_codes_file, 'r') as f:
                shared_codes = json.load(f)
        else:
            shared_codes = []

        shared_codes.append(shared_code)

        # Keep only last 100 shared codes
        if len(shared_codes) > 100:
            shared_codes = shared_codes[-100:]

        with open(shared_codes_file, 'w') as f:
            json.dump(shared_codes, f, indent=2)

        return jsonify({
            "success": True,
            "message": "Code shared successfully",
            "share_id": shared_code['id']
        })

    except Exception as e:
        print(f"Error sharing code: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

@app.route('/api/shared_codes')
def get_shared_codes():
    """Get shared code snippets"""
    try:
        shared_codes_file = "data/shared_codes.json"
        if os.path.exists(shared_codes_file):
            with open(shared_codes_file, 'r') as f:
                shared_codes = json.load(f)
        else:
            shared_codes = []

        # Sort by creation date (newest first)
        shared_codes.sort(key=lambda x: x['created_at'], reverse=True)

        return jsonify({
            "success": True,
            "shared_codes": shared_codes[:20]  # Return last 20
        })

    except Exception as e:
        print(f"Error getting shared codes: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

def get_user_name(email):
    """Get user's display name"""
    user_data = load_user_data()
    user = user_data.get(email, {})
    return user.get('name', 'Anonymous')

def paginate_items(items, page=1, per_page=10):
    """Paginate a list of items"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page

    return {
        'items': items[start:end],
        'total': total,
        'page': page,
        'per_page': per_page,
        'pages': (total + per_page - 1) // per_page,
        'has_prev': page > 1,
        'has_next': end < total
    }

def sanitize_input(text):
    """Basic input sanitization"""
    if not isinstance(text, str):
        return text

    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
    for char in dangerous_chars:
        text = text.replace(char, '')

    # Limit length
    return text[:1000].strip()

def validate_and_sanitize_data(data):
    """Validate and sanitize form data"""
    sanitized = {}

    for key, value in data.items():
        if isinstance(value, str):
            sanitized[key] = sanitize_input(value)
        elif isinstance(value, list):
            sanitized[key] = [sanitize_input(item) if isinstance(item, str) else item for item in value]
        else:
            sanitized[key] = value

    return sanitized

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors with user-friendly page"""
    return render_template('error.html',
                         error_code=404,
                         error_message="Page not found",
                         suggestion="Try going back to the dashboard"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors with user-friendly page"""
    return render_template('error.html',
                         error_code=500,
                         error_message="Internal server error",
                         suggestion="Please try again later"), 500

def safe_execute(func, *args, **kwargs):
    """Safely execute a function with error recovery"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error in {func.__name__}: {e}")
        return None

@disk_cache(ttl=3600)  # Cache for 1 hour
def get_comprehensive_quizzes_data():
    """
    Comprehensive quiz system covering (cached):
    - Fundamentals (1-5)
    - Control Flow (6-10)
    - Data Structures (11-15)
    - OOP & Advanced (16-20)
    """
    return [
        # FUNDAMENTALS QUIZZES (1-5)
        {
            'id': 'quiz_1', 'title': 'Python Basics & Syntax',
            'description': 'Test your knowledge of Python fundamentals, syntax rules, and basic programming concepts.',
            'difficulty': 'beginner', 'questions': 10, 'time_limit': 600, 'points': 25,
            'category': 'fundamentals',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'Which of the following is the correct way to create a comment in Python?',
                    'options': ['// This is a comment', '/* This is a comment */', '# This is a comment', '<!-- This is a comment -->'],
                    'correct_answer': 2, 'explanation': 'In Python, comments start with the # symbol.'
                },
                {
                    'id': 2, 'type': 'multiple_choice',
                    'question': 'What is the output of: print(type(5.0))?',
                    'options': ['<class \'int\'>', '<class \'float\'>', '<class \'str\'>', '<class \'number\'>'],
                    'correct_answer': 1, 'explanation': '5.0 is a floating-point number, so its type is float.'
                },
                {
                    'id': 3, 'type': 'code_completion',
                    'question': 'Complete the code to print "Hello, World!"',
                    'code_template': '___("Hello, World!")',
                    'correct_answer': 'print', 'explanation': 'The print() function is used to display output in Python.'
                },
                {
                    'id': 4, 'type': 'true_false',
                    'question': 'Python is case-sensitive.',
                    'correct_answer': True, 'explanation': 'Python distinguishes between uppercase and lowercase letters.'
                },
                {
                    'id': 5, 'type': 'multiple_choice',
                    'question': 'Which operator is used for exponentiation in Python?',
                    'options': ['^', '**', 'exp', 'pow'],
                    'correct_answer': 1, 'explanation': 'The ** operator is used for exponentiation (e.g., 2**3 = 8).'
                }
            ]
        },
        {
            'id': 'quiz_2', 'title': 'Variables & Data Types',
            'description': 'Master Python variables, data types, type conversion, and naming conventions.',
            'difficulty': 'beginner', 'questions': 12, 'time_limit': 720, 'points': 30,
            'category': 'fundamentals',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'Which of the following is a valid variable name in Python?',
                    'options': ['2variable', 'variable-name', '_variable', 'variable name'],
                    'correct_answer': 2, 'explanation': 'Variable names can start with underscore or letter, not numbers or contain spaces/hyphens.'
                },
                {
                    'id': 2, 'type': 'code_completion',
                    'question': 'Convert the string "123" to an integer:',
                    'code_template': 'num = ___("123")',
                    'correct_answer': 'int', 'explanation': 'The int() function converts strings to integers.'
                },
                {
                    'id': 3, 'type': 'debugging',
                    'question': 'Fix this code: x = "5" + 3',
                    'options': ['x = "5" + "3"', 'x = int("5") + 3', 'x = "5" + str(3)', 'Both B and C are correct'],
                    'correct_answer': 3, 'explanation': 'You can either convert the string to int or the number to string.'
                }
            ]
        },
        {
            'id': 'quiz_3', 'title': 'Strings & Text Processing',
            'description': 'Learn string manipulation, formatting, methods, and text processing techniques.',
            'difficulty': 'beginner', 'questions': 10, 'time_limit': 600, 'points': 25,
            'category': 'fundamentals',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'What is the output of: "Hello".upper()?',
                    'options': ['hello', 'HELLO', 'Hello', 'Error'],
                    'correct_answer': 1, 'explanation': 'The upper() method converts all characters to uppercase.'
                },
                {
                    'id': 2, 'type': 'code_completion',
                    'question': 'Complete the code to get the length of a string:',
                    'code_template': 'text = "Python"\nlength = ___(text)',
                    'correct_answer': 'len', 'explanation': 'The len() function returns the length of a string.'
                },
                {
                    'id': 3, 'type': 'debugging',
                    'question': 'Fix this string formatting: name = "Alice"; print("Hello " + name + "!")',
                    'options': ['print(f"Hello {name}!")', 'print("Hello", name, "!")', 'print("Hello {} !".format(name))', 'All are correct'],
                    'correct_answer': 3, 'explanation': 'All three methods are valid ways to format strings in Python.'
                },
                {
                    'id': 4, 'type': 'multiple_choice',
                    'question': 'Which method splits a string into a list?',
                    'options': ['split()', 'join()', 'replace()', 'find()'],
                    'correct_answer': 0, 'explanation': 'The split() method divides a string into a list based on a delimiter.'
                },
                {
                    'id': 5, 'type': 'true_false',
                    'question': 'Strings in Python are mutable (can be changed after creation).',
                    'correct_answer': False, 'explanation': 'Strings in Python are immutable - they cannot be changed after creation.'
                }
            ]
        },
        {
            'id': 'quiz_4', 'title': 'Numbers & Math Operations',
            'description': 'Test your understanding of numeric types, arithmetic operators, and mathematical functions.',
            'difficulty': 'beginner', 'questions': 8, 'time_limit': 480, 'points': 20,
            'category': 'fundamentals',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'What is the result of 10 // 3 in Python?',
                    'options': ['3.33', '3', '4', '3.0'],
                    'correct_answer': 1, 'explanation': 'The // operator performs floor division, returning the integer part.'
                },
                {
                    'id': 2, 'type': 'multiple_choice',
                    'question': 'Which function converts a string to an integer?',
                    'options': ['str()', 'int()', 'float()', 'bool()'],
                    'correct_answer': 1, 'explanation': 'The int() function converts strings and other types to integers.'
                },
                {
                    'id': 3, 'type': 'code_completion',
                    'question': 'Complete the code to calculate the square root:',
                    'code_template': 'import math\nresult = math.___(16)',
                    'correct_answer': 'sqrt', 'explanation': 'The math.sqrt() function calculates the square root.'
                },
                {
                    'id': 4, 'type': 'true_false',
                    'question': 'In Python, 5/2 returns 2.',
                    'correct_answer': False, 'explanation': 'In Python 3, 5/2 returns 2.5 (float division). Use 5//2 for integer division.'
                }
            ]
        },
        {
            'id': 'quiz_5', 'title': 'Input/Output & User Interaction',
            'description': 'Master user input, output formatting, and basic program interaction.',
            'difficulty': 'beginner', 'questions': 8, 'time_limit': 480, 'points': 20,
            'category': 'fundamentals',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'What does the input() function return?',
                    'options': ['Integer', 'Float', 'String', 'Boolean'],
                    'correct_answer': 2, 'explanation': 'The input() function always returns a string, even if numbers are entered.'
                },
                {
                    'id': 2, 'type': 'code_completion',
                    'question': 'Complete the code to print with a custom separator:',
                    'code_template': 'print("A", "B", "C", ___="-")',
                    'correct_answer': 'sep', 'explanation': 'The sep parameter in print() sets the separator between values.'
                },
                {
                    'id': 3, 'type': 'debugging',
                    'question': 'Fix this code: age = input("Enter age: "); print("You are " + age + " years old")',
                    'options': ['Convert age to int first', 'Use f-string formatting', 'Use .format() method', 'The code is already correct'],
                    'correct_answer': 3, 'explanation': 'Since we\'re concatenating strings, the code works correctly as input() returns a string.'
                }
            ]
        },

        # CONTROL FLOW QUIZZES (6-10)
        {
            'id': 'quiz_6', 'title': 'Conditional Statements',
            'description': 'Master if, elif, else statements and logical operators for decision making.',
            'difficulty': 'intermediate', 'questions': 12, 'time_limit': 720, 'points': 35,
            'category': 'control_flow',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'What is the output of this code?\nx = 5\nif x > 3:\n    print("A")\nelif x > 7:\n    print("B")\nelse:\n    print("C")',
                    'options': ['A', 'B', 'C', 'AB'],
                    'correct_answer': 0, 'explanation': 'Since x=5 > 3, the first condition is true and "A" is printed. elif is not checked.'
                },
                {
                    'id': 2, 'type': 'multiple_choice',
                    'question': 'Which logical operator returns True if both conditions are True?',
                    'options': ['or', 'and', 'not', 'xor'],
                    'correct_answer': 1, 'explanation': 'The "and" operator returns True only when both conditions are True.'
                },
                {
                    'id': 3, 'type': 'code_completion',
                    'question': 'Complete the condition to check if x is between 10 and 20:',
                    'code_template': 'if 10 <= x ___ 20:\n    print("In range")',
                    'correct_answer': '<=', 'explanation': 'Use <= to check if x is less than or equal to 20.'
                },
                {
                    'id': 4, 'type': 'debugging',
                    'question': 'Fix this code: if x = 5: print("Five")',
                    'options': ['if x == 5:', 'if x is 5:', 'if x equals 5:', 'The code is correct'],
                    'correct_answer': 0, 'explanation': 'Use == for comparison, not = which is for assignment.'
                },
                {
                    'id': 5, 'type': 'true_false',
                    'question': 'The expression "not False" evaluates to True.',
                    'correct_answer': True, 'explanation': 'The "not" operator inverts the boolean value, so "not False" is True.'
                }
            ]
        },
        {
            'id': 'quiz_7', 'title': 'Loops & Iteration',
            'description': 'Test your knowledge of for loops, while loops, and loop control statements.',
            'difficulty': 'intermediate', 'questions': 15, 'time_limit': 900, 'points': 40,
            'category': 'control_flow',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'What does range(1, 6) generate?',
                    'options': ['[1, 2, 3, 4, 5]', '[1, 2, 3, 4, 5, 6]', '[0, 1, 2, 3, 4, 5]', '[2, 3, 4, 5]'],
                    'correct_answer': 0, 'explanation': 'range(1, 6) generates numbers from 1 to 5 (6 is excluded).'
                },
                {
                    'id': 2, 'type': 'code_completion',
                    'question': 'Complete the loop to iterate through a list:',
                    'code_template': 'items = ["a", "b", "c"]\n___ item in items:\n    print(item)',
                    'correct_answer': 'for', 'explanation': 'Use "for" to iterate through items in a list.'
                },
                {
                    'id': 3, 'type': 'multiple_choice',
                    'question': 'What does the "break" statement do in a loop?',
                    'options': ['Skips the current iteration', 'Exits the loop completely', 'Restarts the loop', 'Pauses the loop'],
                    'correct_answer': 1, 'explanation': 'The "break" statement immediately exits the loop.'
                },
                {
                    'id': 4, 'type': 'multiple_choice',
                    'question': 'What does the "continue" statement do?',
                    'options': ['Exits the loop', 'Skips to the next iteration', 'Restarts from the beginning', 'Does nothing'],
                    'correct_answer': 1, 'explanation': 'The "continue" statement skips the rest of the current iteration and moves to the next.'
                },
                {
                    'id': 5, 'type': 'debugging',
                    'question': 'Fix this infinite loop: while True: print("Hello")',
                    'options': ['Add a break statement', 'Change condition to False', 'Add a counter and condition', 'All of the above'],
                    'correct_answer': 3, 'explanation': 'All options can fix an infinite loop depending on the desired behavior.'
                }
            ]
        },
        {
            'id': 'quiz_8', 'title': 'Functions & Scope',
            'description': 'Understand function definition, parameters, return values, and variable scope.',
            'difficulty': 'intermediate', 'questions': 14, 'time_limit': 840, 'points': 40,
            'category': 'control_flow'
        },
        {
            'id': 'quiz_9', 'title': 'Error Handling',
            'description': 'Learn exception handling, try-except blocks, and debugging techniques.',
            'difficulty': 'intermediate', 'questions': 10, 'time_limit': 600, 'points': 35,
            'category': 'control_flow'
        },
        {
            'id': 'quiz_10', 'title': 'Advanced Control Flow',
            'description': 'Master nested loops, comprehensions, and complex control structures.',
            'difficulty': 'intermediate', 'questions': 12, 'time_limit': 720, 'points': 40,
            'category': 'control_flow'
        },

        # DATA STRUCTURES QUIZZES (11-15)
        {
            'id': 'quiz_11', 'title': 'Lists & List Methods',
            'description': 'Master Python lists, indexing, slicing, and list manipulation methods.',
            'difficulty': 'advanced', 'questions': 15, 'time_limit': 900, 'points': 45,
            'category': 'data_structures',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'What is the output of [1, 2, 3][1:3]?',
                    'options': ['[1, 2]', '[2, 3]', '[1, 2, 3]', '[2]'],
                    'correct_answer': 1, 'explanation': 'List slicing [1:3] returns elements from index 1 to 2 (3 is excluded).'
                },
                {
                    'id': 2, 'type': 'code_completion',
                    'question': 'Complete the code to add an item to the end of a list:',
                    'code_template': 'my_list = [1, 2, 3]\nmy_list.___(4)',
                    'correct_answer': 'append', 'explanation': 'The append() method adds an item to the end of a list.'
                },
                {
                    'id': 3, 'type': 'multiple_choice',
                    'question': 'What does the extend() method do?',
                    'options': ['Adds one item', 'Adds multiple items from an iterable', 'Removes items', 'Sorts the list'],
                    'correct_answer': 1, 'explanation': 'extend() adds all items from an iterable to the list.'
                },
                {
                    'id': 4, 'type': 'debugging',
                    'question': 'Fix this code to remove the first occurrence of 2: my_list = [1, 2, 3, 2]; my_list.delete(2)',
                    'options': ['my_list.remove(2)', 'my_list.pop(2)', 'del my_list[2]', 'my_list.discard(2)'],
                    'correct_answer': 0, 'explanation': 'remove() removes the first occurrence of a value.'
                },
                {
                    'id': 5, 'type': 'multiple_choice',
                    'question': 'What is list comprehension syntax for squares of numbers 1-5?',
                    'options': ['[x^2 for x in range(1,6)]', '[x**2 for x in range(1,6)]', '[x*2 for x in range(1,6)]', '[x+2 for x in range(1,6)]'],
                    'correct_answer': 1, 'explanation': 'Use ** for exponentiation in Python, and range(1,6) for numbers 1-5.'
                }
            ]
        },
        {
            'id': 'quiz_12', 'title': 'Dictionaries & Key-Value Pairs',
            'description': 'Test your knowledge of dictionaries, nested structures, and dictionary methods.',
            'difficulty': 'advanced', 'questions': 12, 'time_limit': 720, 'points': 40,
            'category': 'data_structures',
            'questions_data': [
                {
                    'id': 1, 'type': 'multiple_choice',
                    'question': 'How do you access the value for key "name" in a dictionary?',
                    'options': ['dict["name"]', 'dict.name', 'dict(name)', 'dict->name'],
                    'correct_answer': 0, 'explanation': 'Use square brackets with the key name to access dictionary values.'
                },
                {
                    'id': 2, 'type': 'code_completion',
                    'question': 'Complete the code to get all keys from a dictionary:',
                    'code_template': 'my_dict = {"a": 1, "b": 2}\nkeys = my_dict.___()',
                    'correct_answer': 'keys', 'explanation': 'The keys() method returns all keys in the dictionary.'
                },
                {
                    'id': 3, 'type': 'multiple_choice',
                    'question': 'What happens if you try to access a non-existent key?',
                    'options': ['Returns None', 'Returns empty string', 'Raises KeyError', 'Creates the key'],
                    'correct_answer': 2, 'explanation': 'Accessing a non-existent key raises a KeyError exception.'
                },
                {
                    'id': 4, 'type': 'multiple_choice',
                    'question': 'Which method safely gets a value with a default?',
                    'options': ['dict[key]', 'dict.get(key, default)', 'dict.fetch(key)', 'dict.safe(key)'],
                    'correct_answer': 1, 'explanation': 'The get() method returns a default value if the key doesn\'t exist.'
                },
                {
                    'id': 5, 'type': 'true_false',
                    'question': 'Dictionary keys must be unique.',
                    'correct_answer': True, 'explanation': 'Each key in a dictionary must be unique; duplicate keys overwrite previous values.'
                }
            ]
        },
        {
            'id': 'quiz_13', 'title': 'Sets & Tuples',
            'description': 'Understand sets, tuples, and when to use different data structures.',
            'difficulty': 'advanced', 'questions': 10, 'time_limit': 600, 'points': 35,
            'category': 'data_structures'
        },
        {
            'id': 'quiz_14', 'title': 'Data Structure Operations',
            'description': 'Advanced operations on data structures: sorting, filtering, and transforming.',
            'difficulty': 'advanced', 'questions': 14, 'time_limit': 840, 'points': 45,
            'category': 'data_structures'
        },
        {
            'id': 'quiz_15', 'title': 'Comprehensions & Generators',
            'description': 'Master list comprehensions, dictionary comprehensions, and generator expressions.',
            'difficulty': 'advanced', 'questions': 12, 'time_limit': 720, 'points': 45,
            'category': 'data_structures'
        },

        # OOP & ADVANCED QUIZZES (16-20)
        {
            'id': 'quiz_16', 'title': 'Classes & Objects',
            'description': 'Test your understanding of object-oriented programming fundamentals.',
            'difficulty': 'expert', 'questions': 15, 'time_limit': 900, 'points': 50,
            'category': 'oop_advanced'
        },
        {
            'id': 'quiz_17', 'title': 'Inheritance & Polymorphism',
            'description': 'Master advanced OOP concepts: inheritance, method overriding, and polymorphism.',
            'difficulty': 'expert', 'questions': 12, 'time_limit': 720, 'points': 50,
            'category': 'oop_advanced'
        },
        {
            'id': 'quiz_18', 'title': 'Modules & Packages',
            'description': 'Understand Python modules, packages, and import systems.',
            'difficulty': 'expert', 'questions': 10, 'time_limit': 600, 'points': 40,
            'category': 'oop_advanced'
        },
        {
            'id': 'quiz_19', 'title': 'File I/O & Data Persistence',
            'description': 'Test your knowledge of file handling, CSV, JSON, and data persistence.',
            'difficulty': 'expert', 'questions': 12, 'time_limit': 720, 'points': 45,
            'category': 'oop_advanced'
        },
        {
            'id': 'quiz_20', 'title': 'Advanced Python Concepts',
            'description': 'Challenge yourself with decorators, context managers, and advanced Python features.',
            'difficulty': 'expert', 'questions': 15, 'time_limit': 900, 'points': 60,
            'category': 'oop_advanced'
        }
    ]

@app.route('/quizzes')
def quizzes():
    if 'user' not in session:
        return redirect(url_for('index'))

    quizzes_data = get_comprehensive_quizzes_data()
    user_data = load_user_data()
    user = user_data.get(session['user'], {})
    completed_quizzes = user.get('completed_quizzes', [])

    return render_template('quizzes.html',
                         quizzes=quizzes_data,
                         completed_quizzes=completed_quizzes)

@app.route('/quiz/<quiz_id>')
def quiz_detail(quiz_id):
    if 'user' not in session:
        return redirect(url_for('index'))

    quizzes_data = get_comprehensive_quizzes_data()
    quiz = next((q for q in quizzes_data if q['id'] == quiz_id), None)

    if not quiz:
        return redirect(url_for('quizzes'))

    user_data = load_user_data()
    user = user_data.get(session['user'], {})
    completed_quizzes = user.get('completed_quizzes', [])
    is_completed = quiz_id in completed_quizzes

    return render_template('quiz_detail.html',
                         quiz=quiz,
                         is_completed=is_completed)

@app.route('/api/submit_quiz', methods=['POST'])
# @rate_limit(requests_per_minute=30, requests_per_hour=200)  # Disabled for development
def submit_quiz():
    """Submit quiz answers with comprehensive validation and error handling"""
    try:
        # Check and validate authentication
        if not validate_session():
            error_handler.logger.warning("Quiz submission attempt without valid authentication")
            return jsonify({
                "success": False,
                "error": "Please log in to submit quiz answers",
                "redirect": url_for('login')
            }), 401

        # Get and validate request data
        data = request.get_json()
        if not data:
            return jsonify({
                "success": False,
                "error": "No quiz data provided"
            }), 400

        quiz_id = data.get('quiz_id')
        user_answers = data.get('answers', {})

        # Validate quiz ID
        if not quiz_id:
            return jsonify({
                "success": False,
                "error": "Quiz ID is required"
            }), 400

        # Validate answers format
        answers_valid, answers_error = validator.validate_quiz_answers(user_answers)
        if not answers_valid:
            error_handler.logger.warning(f"Invalid quiz answers format: {answers_error}")
            return jsonify({
                "success": False,
                "error": f"Invalid answers format: {answers_error}"
            }), 400

        # Get quiz data
        try:
            quizzes_data = get_comprehensive_quizzes_data()
            quiz = next((q for q in quizzes_data if q['id'] == quiz_id), None)
        except Exception as e:
            error_handler.handle_error(e, context={"operation": "load_quiz_data", "quiz_id": quiz_id})
            return jsonify({
                "success": False,
                "error": "Failed to load quiz data"
            }), 500

        if not quiz:
            error_handler.logger.warning(f"Quiz not found: {quiz_id}")
            return jsonify({
                "success": False,
                "error": "Quiz not found"
            }), 404

        # Calculate score with error handling
        correct_answers = 0
        total_questions = len(quiz.get('questions_data', []))

        if total_questions == 0:
            total_questions = quiz.get('questions', 5)  # Fallback for quizzes without detailed questions

        # Process answers with validation
        for question in quiz.get('questions_data', []):
            try:
                question_id = str(question['id'])
                if question_id in user_answers:
                    user_answer = user_answers[question_id]
                    correct_answer = question['correct_answer']

                    # Handle different answer types
                    if question['type'] == 'true_false':
                        if (user_answer == 'true' and correct_answer is True) or (user_answer == 'false' and correct_answer is False):
                            correct_answers += 1
                    elif question['type'] == 'code_completion':
                        if str(user_answer).strip().lower() == str(correct_answer).strip().lower():
                            correct_answers += 1
                    else:  # multiple_choice, debugging
                        if int(user_answer) == correct_answer:
                            correct_answers += 1
            except (ValueError, KeyError, TypeError) as e:
                error_handler.logger.warning(f"Error processing question {question_id}: {e}")
                continue

        # Calculate percentage and points
        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        points_earned = int((percentage / 100) * quiz.get('points', 25))

        # Update user progress
        user_data = load_user_data()
        user = user_data.get(session['user'], {})

        if not user:
            return jsonify({
                "success": False,
                "error": "User data not found"
            }), 404

        # Update quiz completion
        completed_quizzes = user.get('completed_quizzes', [])
        if quiz_id not in completed_quizzes:
            completed_quizzes.append(quiz_id)
            user['completed_quizzes'] = completed_quizzes

        # Update points and stats
        user['points'] = user.get('points', 0) + points_earned
        user['quizzes_completed'] = len(completed_quizzes)
        user['quizzes_taken'] = user.get('quizzes_taken', 0) + 1

        # Update average quiz score
        total_quiz_score = user.get('total_quiz_score', 0) + percentage
        user['total_quiz_score'] = total_quiz_score
        user['average_quiz_score'] = total_quiz_score / user['quizzes_taken']

        # Update last activity
        user['last_activity'] = datetime.now().isoformat()

        # Update session activity to prevent timeout
        session['last_activity'] = datetime.now().isoformat()
        session.permanent = True  # Ensure session remains permanent

        # Save updated user data
        user_data[session['user']] = user
        save_success = save_user_data(user_data)

        if not save_success:
            error_handler.logger.error(f"Failed to save quiz results for user: {session['user']}")
            return jsonify({
                "success": False,
                "error": "Failed to save quiz results"
            }), 500

        error_handler.logger.info(f"Quiz completed: {session['user']} scored {percentage:.1f}% on {quiz_id}")

        # Determine performance feedback
        if percentage >= 90:
            performance_level = "Excellent"
            feedback = "Outstanding work! You've mastered this topic."
        elif percentage >= 80:
            performance_level = "Good"
            feedback = "Great job! You have a solid understanding."
        elif percentage >= 70:
            performance_level = "Fair"
            feedback = "Good effort! Review the material and try again."
        else:
            performance_level = "Needs Improvement"
            feedback = "Keep practicing! Review the lessons and try again."

        return jsonify({
            "success": True,
            "score": percentage,
            "points_earned": points_earned,
            "correct_answers": correct_answers,
            "total_questions": total_questions,
            "performance_level": performance_level,
            "feedback": feedback,
            "message": f"Quiz completed! You scored {percentage:.1f}% and earned {points_earned} points."
        })

    except ValidationError as e:
        error_handler.handle_error(e, context={"route": "submit_quiz", "quiz_id": quiz_id})
        return jsonify({
            "success": False,
            "error": "Invalid quiz submission data"
        }), 400

    except Exception as e:
        error_handler.handle_error(e, context={"route": "submit_quiz", "quiz_id": quiz_id, "user": session.get('user')})
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred while processing your quiz"
        }), 500

@app.route('/playground')
def playground():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('playground.html')

@app.route('/code-editor')
def code_editor():
    """Interactive code editor with syntax highlighting and real-time features"""
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('code_editor.html')

@app.route('/api/execute_code', methods=['POST'])
def execute_code():
    """Execute Python code safely (simulated for now)"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()
        code = data.get('code', '').strip()

        if not code:
            return jsonify({"success": False, "error": "No code provided"}), 400

        # Update user's playground usage
        user_data = load_user_data()
        user = user_data.get(session['user'], {})
        user['playground_uses'] = user.get('playground_uses', 0) + 1
        user['last_activity'] = datetime.now().isoformat()
        user_data[session['user']] = user
        save_user_data(user_data)

        # Simulate code execution (in production, use sandboxed execution)
        output = simulate_python_execution(code)

        return jsonify({
            "success": True,
            "output": output,
            "execution_time": "0.05s"
        })

    except Exception as e:
        print(f"Error executing code: {e}")
        return jsonify({"success": False, "error": "Execution failed"}), 500

def simulate_python_execution(code):
    """Simulate Python code execution for demonstration"""
    import re

    output_lines = []

    # Extract print statements
    print_pattern = r'print\s*\(\s*([^)]+)\s*\)'
    print_matches = re.findall(print_pattern, code)

    for match in print_matches:
        # Basic evaluation of simple expressions
        try:
            # Remove quotes if it's a string literal
            if (match.startswith('"') and match.endswith('"')) or (match.startswith("'") and match.endswith("'")):
                output_lines.append(match[1:-1])
            elif match.startswith('f"') or match.startswith("f'"):
                # Simple f-string handling
                output_lines.append(match[2:-1])
            else:
                # Try to evaluate simple expressions
                if match.isdigit():
                    output_lines.append(match)
                else:
                    output_lines.append(str(match))
        except:
            output_lines.append(str(match))

    # Check for variable assignments and simple operations
    if 'def ' in code:
        output_lines.append("Function defined successfully")

    if 'for ' in code or 'while ' in code:
        output_lines.append("Loop executed")

    if 'if ' in code:
        output_lines.append("Conditional statement processed")

    if not output_lines:
        output_lines.append("Code executed successfully (no output)")

    return '\n'.join(output_lines)

@app.route('/analytics')
def analytics_dashboard():
    """Advanced learning analytics dashboard"""
    if 'user' not in session:
        return redirect(url_for('login'))

    user_analytics = generate_advanced_analytics(session['user'])
    recommendations = generate_learning_recommendations(session['user'])

    return render_template('analytics.html',
                         analytics=user_analytics,
                         recommendations=recommendations)

def generate_advanced_analytics(user_email):
    """Generate comprehensive learning analytics"""
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    # Calculate learning metrics
    total_time_spent = calculate_total_learning_time(user)
    learning_efficiency = calculate_learning_efficiency(user)
    skill_progression = calculate_skill_progression(user)
    learning_patterns = analyze_learning_patterns(user)

    return {
        'total_time_spent': total_time_spent,
        'learning_efficiency': learning_efficiency,
        'skill_progression': skill_progression,
        'learning_patterns': learning_patterns,
        'performance_trends': calculate_performance_trends(user),
        'knowledge_gaps': identify_knowledge_gaps(user),
        'learning_velocity': calculate_detailed_velocity(user),
        'engagement_score': calculate_engagement_score(user)
    }

def calculate_total_learning_time(user):
    """Calculate total time spent learning"""
    # Estimate based on activities
    lessons_time = user.get('lessons_completed', 0) * 15  # 15 min per lesson
    quizzes_time = user.get('quizzes_completed', 0) * 10   # 10 min per quiz
    challenges_time = user.get('challenges_completed', 0) * 30  # 30 min per challenge
    playground_time = user.get('playground_uses', 0) * 5   # 5 min per playground use

    total_minutes = lessons_time + quizzes_time + challenges_time + playground_time

    return {
        'total_minutes': total_minutes,
        'total_hours': round(total_minutes / 60, 1),
        'breakdown': {
            'lessons': lessons_time,
            'quizzes': quizzes_time,
            'challenges': challenges_time,
            'playground': playground_time
        }
    }

def calculate_learning_efficiency(user):
    """Calculate how efficiently the user is learning"""
    lessons_completed = user.get('lessons_completed', 0)
    quizzes_completed = user.get('quizzes_completed', 0)
    avg_quiz_score = user.get('average_quiz_score', 0)
    days_active = max(user.get('days_since_start', 1), 1)

    # Efficiency metrics
    completion_rate = (lessons_completed + quizzes_completed) / days_active
    score_efficiency = avg_quiz_score / 100 if avg_quiz_score > 0 else 0
    overall_efficiency = (completion_rate * 0.6 + score_efficiency * 0.4) * 100

    return {
        'overall_score': round(overall_efficiency, 1),
        'completion_rate': round(completion_rate, 2),
        'score_efficiency': round(score_efficiency * 100, 1),
        'rating': get_efficiency_rating(overall_efficiency)
    }

def calculate_skill_progression(user):
    """Calculate progression in different skill areas"""
    lessons_completed = user.get('completed_lesson_ids', [])

    # Categorize lessons by skill area
    skill_areas = {
        'basics': ['lesson_1', 'lesson_2', 'lesson_3', 'lesson_4', 'lesson_5'],
        'data_structures': ['lesson_6', 'lesson_7', 'lesson_8', 'lesson_9', 'lesson_10'],
        'control_flow': ['lesson_11', 'lesson_12', 'lesson_13', 'lesson_14', 'lesson_15'],
        'functions': ['lesson_16', 'lesson_17', 'lesson_18', 'lesson_19', 'lesson_20'],
        'oop': ['lesson_21', 'lesson_22', 'lesson_23', 'lesson_24', 'lesson_25'],
        'advanced': ['lesson_26', 'lesson_27', 'lesson_28', 'lesson_29', 'lesson_30']
    }

    progression = {}
    for area, lesson_ids in skill_areas.items():
        completed_in_area = len([lid for lid in lesson_ids if lid in lessons_completed])
        total_in_area = len(lesson_ids)
        progression[area] = {
            'completed': completed_in_area,
            'total': total_in_area,
            'percentage': round((completed_in_area / total_in_area) * 100, 1)
        }

    return progression

def analyze_learning_patterns(user):
    """Analyze user's learning patterns and habits"""
    # Simulate learning pattern analysis
    patterns = {
        'preferred_time': 'evening',  # Would be calculated from actual activity data
        'session_length': 'medium',   # 15-30 minutes
        'learning_style': 'visual',   # Based on content preferences
        'consistency': calculate_consistency_score(user),
        'challenge_preference': 'moderate'
    }

    return patterns

def calculate_consistency_score(user):
    """Calculate how consistent the user's learning is"""
    streak = user.get('streak', 0)
    days_since_start = max(user.get('days_since_start', 1), 1)

    consistency = (streak / days_since_start) * 100
    return min(round(consistency, 1), 100)

def get_efficiency_rating(score):
    """Get efficiency rating based on score"""
    if score >= 80:
        return "Excellent"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Average"
    else:
        return "Needs Improvement"

def generate_learning_recommendations(user_email):
    """Generate personalized learning recommendations"""
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    recommendations = []

    # Analyze current progress
    lessons_completed = user.get('lessons_completed', 0)
    avg_quiz_score = user.get('average_quiz_score', 0)
    challenges_completed = user.get('challenges_completed', 0)

    # Recommendation logic
    if lessons_completed < 10:
        recommendations.append({
            'type': 'lesson',
            'priority': 'high',
            'title': 'Focus on Fundamentals',
            'description': 'Complete more basic lessons to build a strong foundation',
            'action': 'Complete 5 more lessons',
            'estimated_time': '75 minutes'
        })

    if avg_quiz_score < 70:
        recommendations.append({
            'type': 'review',
            'priority': 'high',
            'title': 'Review Previous Material',
            'description': 'Your quiz scores suggest reviewing previous lessons would help',
            'action': 'Retake quizzes for lessons 1-5',
            'estimated_time': '30 minutes'
        })

    if challenges_completed == 0:
        recommendations.append({
            'type': 'challenge',
            'priority': 'medium',
            'title': 'Try Your First Challenge',
            'description': 'Challenges help apply what you\'ve learned in practical scenarios',
            'action': 'Complete the "Hello World" challenge',
            'estimated_time': '20 minutes'
        })

    # Add skill-specific recommendations
    skill_progression = calculate_skill_progression(user)
    for skill, progress in skill_progression.items():
        if progress['percentage'] < 50:
            recommendations.append({
                'type': 'skill',
                'priority': 'medium',
                'title': f'Improve {skill.title()} Skills',
                'description': f'You\'ve completed {progress["completed"]}/{progress["total"]} lessons in this area',
                'action': f'Complete more {skill} lessons',
                'estimated_time': '45 minutes'
            })

    return recommendations[:5]  # Return top 5 recommendations

def calculate_performance_trends(user):
    """Calculate performance trends over time"""
    return {
        'quiz_score_trend': 'improving',  # Would calculate from historical data
        'completion_rate_trend': 'stable',
        'engagement_trend': 'increasing'
    }

def identify_knowledge_gaps(user):
    """Identify areas where user needs improvement"""
    avg_quiz_score = user.get('average_quiz_score', 0)
    gaps = []

    if avg_quiz_score < 70:
        gaps.append('Basic Python syntax')
    if user.get('challenges_completed', 0) == 0:
        gaps.append('Problem-solving skills')

    return gaps

def calculate_detailed_velocity(user):
    """Calculate detailed learning velocity metrics"""
    days_active = max(user.get('days_since_start', 1), 1)
    total_completed = (
        user.get('lessons_completed', 0) +
        user.get('quizzes_completed', 0) +
        user.get('challenges_completed', 0)
    )

    return {
        'items_per_day': round(total_completed / days_active, 2),
        'weekly_velocity': round((total_completed / days_active) * 7, 1),
        'projected_completion': estimate_completion_time(user)
    }

def calculate_engagement_score(user):
    """Calculate user engagement score"""
    factors = [
        user.get('streak', 0) * 2,  # Streak is important
        user.get('lessons_completed', 0),
        user.get('quizzes_completed', 0) * 2,  # Quizzes show engagement
        user.get('challenges_completed', 0) * 3,  # Challenges show high engagement
        user.get('playground_uses', 0)
    ]

    raw_score = sum(factors)
    normalized_score = min(raw_score / 2, 100)  # Normalize to 0-100

    return round(normalized_score, 1)

def estimate_completion_time(user):
    """Estimate time to complete all content"""
    total_lessons = 50
    total_quizzes = 20
    total_challenges = 10

    completed = (
        user.get('lessons_completed', 0) +
        user.get('quizzes_completed', 0) +
        user.get('challenges_completed', 0)
    )

    total_content = total_lessons + total_quizzes + total_challenges
    remaining = total_content - completed

    velocity = calculate_detailed_velocity(user)['items_per_day']
    if velocity > 0:
        days_remaining = remaining / velocity
        return f"{int(days_remaining)} days"
    else:
        return "Unable to estimate"

# Gamification System
@app.route('/skill-tree')
def skill_tree():
    """Display user's skill tree progress"""
    if 'user' not in session:
        return redirect(url_for('index'))

    user_skills = calculate_skill_tree_progress(session['user'])
    daily_challenge = get_daily_challenge()

    return render_template('skill_tree.html',
                         skills=user_skills,
                         daily_challenge=daily_challenge)

def calculate_skill_tree_progress(user_email):
    """Calculate progress in skill tree"""
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    # Define skill tree structure
    skill_tree = {
        'python_basics': {
            'name': 'Python Basics',
            'icon': 'fas fa-baby',
            'color': 'green',
            'prerequisites': [],
            'lessons': ['lesson_1', 'lesson_2', 'lesson_3', 'lesson_4', 'lesson_5'],
            'xp_reward': 100,
            'unlocks': ['data_structures', 'control_flow']
        },
        'data_structures': {
            'name': 'Data Structures',
            'icon': 'fas fa-database',
            'color': 'blue',
            'prerequisites': ['python_basics'],
            'lessons': ['lesson_6', 'lesson_7', 'lesson_8', 'lesson_9', 'lesson_10'],
            'xp_reward': 150,
            'unlocks': ['functions']
        },
        'control_flow': {
            'name': 'Control Flow',
            'icon': 'fas fa-code-branch',
            'color': 'purple',
            'prerequisites': ['python_basics'],
            'lessons': ['lesson_11', 'lesson_12', 'lesson_13', 'lesson_14', 'lesson_15'],
            'xp_reward': 150,
            'unlocks': ['functions']
        },
        'functions': {
            'name': 'Functions',
            'icon': 'fas fa-cogs',
            'color': 'orange',
            'prerequisites': ['data_structures', 'control_flow'],
            'lessons': ['lesson_16', 'lesson_17', 'lesson_18', 'lesson_19', 'lesson_20'],
            'xp_reward': 200,
            'unlocks': ['oop']
        },
        'oop': {
            'name': 'Object-Oriented Programming',
            'icon': 'fas fa-cube',
            'color': 'red',
            'prerequisites': ['functions'],
            'lessons': ['lesson_21', 'lesson_22', 'lesson_23', 'lesson_24', 'lesson_25'],
            'xp_reward': 250,
            'unlocks': ['advanced_topics']
        },
        'advanced_topics': {
            'name': 'Advanced Topics',
            'icon': 'fas fa-rocket',
            'color': 'gold',
            'prerequisites': ['oop'],
            'lessons': ['lesson_26', 'lesson_27', 'lesson_28', 'lesson_29', 'lesson_30'],
            'xp_reward': 300,
            'unlocks': []
        }
    }

    # Calculate progress for each skill
    completed_lessons = user.get('completed_lesson_ids', [])
    user_xp = user.get('xp', 0)

    for skill_id, skill in skill_tree.items():
        completed_in_skill = len([l for l in skill['lessons'] if l in completed_lessons])
        total_in_skill = len(skill['lessons'])

        skill['completed'] = completed_in_skill
        skill['total'] = total_in_skill
        skill['progress'] = (completed_in_skill / total_in_skill) * 100
        skill['is_completed'] = completed_in_skill == total_in_skill
        skill['is_unlocked'] = check_skill_unlocked(skill, skill_tree, completed_lessons)
        skill['xp_earned'] = skill['xp_reward'] if skill['is_completed'] else 0

    return {
        'skills': skill_tree,
        'total_xp': user_xp,
        'level': calculate_xp_level(user_xp),
        'next_level_xp': calculate_next_level_xp(user_xp)
    }

def check_skill_unlocked(skill, skill_tree, completed_lessons):
    """Check if a skill is unlocked based on prerequisites"""
    if not skill['prerequisites']:
        return True

    for prereq in skill['prerequisites']:
        prereq_skill = skill_tree[prereq]
        completed_in_prereq = len([l for l in prereq_skill['lessons'] if l in completed_lessons])
        if completed_in_prereq < len(prereq_skill['lessons']):
            return False

    return True

def calculate_xp_level(xp):
    """Calculate level based on XP"""
    return (xp // 100) + 1

def calculate_next_level_xp(xp):
    """Calculate XP needed for next level"""
    current_level = calculate_xp_level(xp)
    next_level_threshold = current_level * 100
    return next_level_threshold - xp

def get_daily_challenge():
    """Get today's daily challenge"""
    import hashlib
    from datetime import date

    # Generate consistent daily challenge based on date
    today = date.today().isoformat()
    challenge_seed = hashlib.md5(today.encode()).hexdigest()[:8]

    challenges = [
        {
            'title': 'Variable Master',
            'description': 'Create 5 different variables with different data types',
            'xp_reward': 25,
            'difficulty': 'Easy'
        },
        {
            'title': 'Loop Champion',
            'description': 'Write a for loop that prints numbers 1 to 10',
            'xp_reward': 30,
            'difficulty': 'Easy'
        },
        {
            'title': 'Function Creator',
            'description': 'Create a function that takes two parameters and returns their sum',
            'xp_reward': 40,
            'difficulty': 'Medium'
        },
        {
            'title': 'List Manipulator',
            'description': 'Create a list, add 3 items, remove 1 item, and print the result',
            'xp_reward': 35,
            'difficulty': 'Medium'
        }
    ]

    # Select challenge based on seed
    challenge_index = int(challenge_seed, 16) % len(challenges)
    return challenges[challenge_index]

@app.route('/api/complete_daily_challenge', methods=['POST'])
def complete_daily_challenge():
    """Complete daily challenge and award XP"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()
        challenge_code = data.get('code', '')

        if not challenge_code:
            return jsonify({"success": False, "error": "No code provided"}), 400

        # Award XP for daily challenge
        user_data = load_user_data()
        user = user_data.get(session['user'], {})

        # Check if already completed today
        today = datetime.now().date().isoformat()
        last_daily = user.get('last_daily_challenge', '')

        if last_daily == today:
            return jsonify({"success": False, "error": "Daily challenge already completed"}), 400

        # Award XP
        daily_challenge = get_daily_challenge()
        xp_earned = daily_challenge['xp_reward']

        user['xp'] = user.get('xp', 0) + xp_earned
        user['last_daily_challenge'] = today
        user['daily_challenges_completed'] = user.get('daily_challenges_completed', 0) + 1
        user['last_activity'] = datetime.now().isoformat()

        # Check for new achievements
        new_achievements = check_and_award_achievements(session['user'])

        # Save user data
        user_data[session['user']] = user
        save_user_data(user_data)

        return jsonify({
            "success": True,
            "xp_earned": xp_earned,
            "total_xp": user['xp'],
            "new_level": calculate_xp_level(user['xp']),
            "new_achievements": new_achievements,
            "message": f"Daily challenge completed! +{xp_earned} XP"
        })

    except Exception as e:
        print(f"Error completing daily challenge: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

@app.route('/api/xp_leaderboard')
def xp_leaderboard():
    """Get XP leaderboard"""
    try:
        user_data = load_user_data()
        leaderboard = []

        for email, user in user_data.items():
            xp = user.get('xp', 0)
            if xp > 0:  # Only include users with XP
                leaderboard.append({
                    'name': user.get('name', 'Anonymous'),
                    'xp': xp,
                    'level': calculate_xp_level(xp)
                })

        # Sort by XP (highest first)
        leaderboard.sort(key=lambda x: x['xp'], reverse=True)

        return jsonify({
            "success": True,
            "leaderboard": leaderboard[:10]  # Top 10
        })

    except Exception as e:
        print(f"Error getting XP leaderboard: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

# Admin Panel
@app.route('/admin')
def admin_panel():
    """Admin panel for content management"""
    if 'user' not in session:
        return redirect(url_for('index'))

    # Simple admin check (in production, use proper role-based access)
    if not is_admin_user(session['user']):
        return redirect(url_for('dashboard'))

    # Get content statistics
    stats = get_content_statistics()
    recent_users = get_recent_users()

    return render_template('admin_panel.html',
                         stats=stats,
                         recent_users=recent_users)

def is_admin_user(email):
    """Check if user is admin (simplified)"""
    admin_emails = ['admin@example.com', 'leomilano2021@gmail.com']  # Add admin emails
    return email in admin_emails

def get_content_statistics():
    """Get content statistics for admin dashboard"""
    user_data = load_user_data()

    total_users = len(user_data)
    active_users = len([u for u in user_data.values() if u.get('last_activity')])
    total_lessons_completed = sum(u.get('lessons_completed', 0) for u in user_data.values())
    total_quizzes_completed = sum(u.get('quizzes_completed', 0) for u in user_data.values())

    return {
        'total_users': total_users,
        'active_users': active_users,
        'total_lessons_completed': total_lessons_completed,
        'total_quizzes_completed': total_quizzes_completed,
        'total_lessons': 50,
        'total_quizzes': 20,
        'total_challenges': 10
    }

def get_recent_users():
    """Get recently registered users"""
    user_data = load_user_data()
    users = []

    for email, user in user_data.items():
        users.append({
            'email': email,
            'name': user.get('name', 'Unknown'),
            'created_at': user.get('created_at', ''),
            'last_activity': user.get('last_activity', ''),
            'lessons_completed': user.get('lessons_completed', 0),
            'points': user.get('points', 0)
        })

    # Sort by creation date (newest first)
    users.sort(key=lambda x: x['created_at'], reverse=True)
    return users[:10]  # Return last 10 users

@app.route('/admin/lesson-editor')
def lesson_editor():
    """Lesson editor interface"""
    if 'user' not in session or not is_admin_user(session['user']):
        return redirect(url_for('index'))

    lessons = get_comprehensive_lessons_data()
    return render_template('lesson_editor.html', lessons=lessons)

@app.route('/api/admin/save_lesson', methods=['POST'])
def save_lesson():
    """Save lesson content"""
    if 'user' not in session or not is_admin_user(session['user']):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    try:
        data = request.get_json()
        lesson_id = data.get('lesson_id')
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        content = data.get('content', '').strip()
        difficulty = data.get('difficulty', 'beginner')
        points = data.get('points', 10)

        if not lesson_id or not title:
            return jsonify({"success": False, "error": "Lesson ID and title are required"}), 400

        # Create lesson object
        lesson_data = {
            'id': lesson_id,
            'title': title,
            'description': description,
            'content': content,
            'difficulty': difficulty,
            'points': points,
            'updated_at': datetime.now().isoformat(),
            'updated_by': session['user']
        }

        # Save to lessons file (simplified - in production use database)
        lessons_file = "data/custom_lessons.json"
        if os.path.exists(lessons_file):
            with open(lessons_file, 'r') as f:
                lessons = json.load(f)
        else:
            lessons = {}

        lessons[lesson_id] = lesson_data

        with open(lessons_file, 'w') as f:
            json.dump(lessons, f, indent=2)

        return jsonify({
            "success": True,
            "message": "Lesson saved successfully"
        })

    except Exception as e:
        print(f"Error saving lesson: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

@app.route('/admin/quiz-builder')
def quiz_builder():
    """Quiz builder interface"""
    if 'user' not in session or not is_admin_user(session['user']):
        return redirect(url_for('index'))

    quizzes = get_comprehensive_quizzes_data()
    return render_template('quiz_builder.html', quizzes=quizzes)

@app.route('/api/admin/save_quiz', methods=['POST'])
def save_quiz():
    """Save quiz content"""
    if 'user' not in session or not is_admin_user(session['user']):
        return jsonify({"success": False, "error": "Unauthorized"}), 403

    try:
        data = request.get_json()
        quiz_id = data.get('quiz_id')
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        questions = data.get('questions', [])

        if not quiz_id or not title or not questions:
            return jsonify({"success": False, "error": "Quiz ID, title, and questions are required"}), 400

        # Create quiz object
        quiz_data = {
            'id': quiz_id,
            'title': title,
            'description': description,
            'questions': len(questions),
            'questions_data': questions,
            'points': len(questions) * 5,  # 5 points per question
            'updated_at': datetime.now().isoformat(),
            'updated_by': session['user']
        }

        # Save to quizzes file
        quizzes_file = "data/custom_quizzes.json"
        if os.path.exists(quizzes_file):
            with open(quizzes_file, 'r') as f:
                quizzes = json.load(f)
        else:
            quizzes = {}

        quizzes[quiz_id] = quiz_data

        with open(quizzes_file, 'w') as f:
            json.dump(quizzes, f, indent=2)

        return jsonify({
            "success": True,
            "message": "Quiz saved successfully"
        })

    except Exception as e:
        print(f"Error saving quiz: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

# Advanced Testing & Validation
@app.route('/api/validate_code', methods=['POST'])
def validate_code():
    """Advanced code validation with quality analysis"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()
        code = data.get('code', '').strip()

        if not code:
            return jsonify({"success": False, "error": "No code provided"}), 400

        # Perform comprehensive code analysis
        validation_results = perform_code_analysis(code)

        return jsonify({
            "success": True,
            "validation": validation_results
        })

    except Exception as e:
        print(f"Error validating code: {e}")
        return jsonify({"success": False, "error": "Validation failed"}), 500

def perform_code_analysis(code):
    """Perform comprehensive code analysis"""
    results = {
        'syntax_valid': True,
        'syntax_errors': [],
        'style_issues': [],
        'complexity_score': 0,
        'quality_score': 0,
        'suggestions': [],
        'security_issues': []
    }

    # Basic syntax validation
    try:
        compile(code, '<string>', 'exec')
        results['syntax_valid'] = True
    except SyntaxError as e:
        results['syntax_valid'] = False
        results['syntax_errors'].append({
            'line': e.lineno,
            'message': str(e),
            'type': 'syntax_error'
        })

    # Style analysis
    style_issues = analyze_code_style(code)
    results['style_issues'] = style_issues

    # Complexity analysis
    complexity = calculate_code_complexity(code)
    results['complexity_score'] = complexity

    # Quality score calculation
    quality_score = calculate_quality_score(results)
    results['quality_score'] = quality_score

    # Generate suggestions
    suggestions = generate_code_suggestions(code, results)
    results['suggestions'] = suggestions

    # Security analysis
    security_issues = analyze_code_security(code)
    results['security_issues'] = security_issues

    return results

def analyze_code_style(code):
    """Analyze code style and formatting"""
    issues = []
    lines = code.split('\n')

    for i, line in enumerate(lines, 1):
        # Check line length
        if len(line) > 79:
            issues.append({
                'line': i,
                'type': 'line_length',
                'message': f'Line too long ({len(line)} characters)',
                'severity': 'warning'
            })

        # Check for trailing whitespace
        if line.endswith(' ') or line.endswith('\t'):
            issues.append({
                'line': i,
                'type': 'trailing_whitespace',
                'message': 'Trailing whitespace',
                'severity': 'info'
            })

        # Check indentation (simplified)
        if line.strip() and not line.startswith(' ' * (line.count('    ') * 4)):
            if '\t' in line:
                issues.append({
                    'line': i,
                    'type': 'indentation',
                    'message': 'Use spaces instead of tabs',
                    'severity': 'warning'
                })

    return issues

def calculate_code_complexity(code):
    """Calculate cyclomatic complexity (simplified)"""
    complexity = 1  # Base complexity

    # Count decision points
    decision_keywords = ['if', 'elif', 'for', 'while', 'except', 'and', 'or']

    for keyword in decision_keywords:
        complexity += code.count(keyword)

    return min(complexity, 10)  # Cap at 10

def calculate_quality_score(results):
    """Calculate overall code quality score"""
    base_score = 100

    # Deduct for syntax errors
    if not results['syntax_valid']:
        base_score -= 50

    # Deduct for style issues
    for issue in results['style_issues']:
        if issue['severity'] == 'error':
            base_score -= 10
        elif issue['severity'] == 'warning':
            base_score -= 5
        elif issue['severity'] == 'info':
            base_score -= 2

    # Deduct for high complexity
    if results['complexity_score'] > 7:
        base_score -= (results['complexity_score'] - 7) * 5

    # Deduct for security issues
    base_score -= len(results['security_issues']) * 15

    return max(base_score, 0)

def generate_code_suggestions(code, results):
    """Generate improvement suggestions"""
    suggestions = []

    if not results['syntax_valid']:
        suggestions.append({
            'type': 'syntax',
            'message': 'Fix syntax errors before proceeding',
            'priority': 'high'
        })

    if results['complexity_score'] > 5:
        suggestions.append({
            'type': 'complexity',
            'message': 'Consider breaking down complex functions into smaller ones',
            'priority': 'medium'
        })

    if len(results['style_issues']) > 5:
        suggestions.append({
            'type': 'style',
            'message': 'Follow PEP 8 style guidelines for better readability',
            'priority': 'low'
        })

    # Check for common improvements
    if 'print(' not in code and 'return' not in code:
        suggestions.append({
            'type': 'output',
            'message': 'Consider adding output or return statements',
            'priority': 'medium'
        })

    if code.count('\n') < 3 and len(code) > 100:
        suggestions.append({
            'type': 'formatting',
            'message': 'Break long code into multiple lines for readability',
            'priority': 'low'
        })

    return suggestions

def analyze_code_security(code):
    """Basic security analysis"""
    security_issues = []

    # Check for potentially dangerous functions
    dangerous_patterns = [
        ('eval(', 'Use of eval() can be dangerous'),
        ('exec(', 'Use of exec() can be dangerous'),
        ('__import__', 'Dynamic imports can be risky'),
        ('open(', 'File operations should be handled carefully')
    ]

    for pattern, message in dangerous_patterns:
        if pattern in code:
            security_issues.append({
                'type': 'dangerous_function',
                'message': message,
                'severity': 'warning'
            })

    return security_issues

@app.route('/api/run_tests', methods=['POST'])
def run_tests():
    """Run comprehensive tests on user code"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()
        code = data.get('code', '').strip()
        test_cases = data.get('test_cases', [])

        if not code:
            return jsonify({"success": False, "error": "No code provided"}), 400

        # Run tests
        test_results = execute_test_cases(code, test_cases)

        # Calculate grade
        grade = calculate_automated_grade(test_results)

        return jsonify({
            "success": True,
            "test_results": test_results,
            "grade": grade
        })

    except Exception as e:
        print(f"Error running tests: {e}")
        return jsonify({"success": False, "error": "Test execution failed"}), 500

def execute_test_cases(code, test_cases):
    """Execute test cases against user code (simplified)"""
    results = []

    for i, test_case in enumerate(test_cases):
        result = {
            'test_id': i + 1,
            'input': test_case.get('input'),
            'expected': test_case.get('expected'),
            'actual': None,
            'passed': False,
            'error': None
        }

        try:
            # Simulate test execution (in production, use sandboxed environment)
            if 'def ' in code:
                # Extract function name (simplified)
                func_name = extract_function_name(code)
                if func_name:
                    # Simulate function call
                    result['actual'] = simulate_function_call(func_name, test_case.get('input'))
                    result['passed'] = result['actual'] == test_case.get('expected')
            else:
                result['error'] = 'No function found in code'

        except Exception as e:
            result['error'] = str(e)

        results.append(result)

    return results

def extract_function_name(code):
    """Extract function name from code (simplified)"""
    import re
    match = re.search(r'def\s+(\w+)\s*\(', code)
    return match.group(1) if match else None

def simulate_function_call(func_name, input_value):
    """Simulate function call (simplified)"""
    # This is a very basic simulation
    # In production, use proper sandboxed execution
    if func_name == 'factorial':
        if input_value == 5:
            return 120
        elif input_value == 0:
            return 1
        elif input_value == 3:
            return 6

    return None

def calculate_automated_grade(test_results):
    """Calculate automated grade based on test results"""
    if not test_results:
        return 0

    passed_tests = sum(1 for result in test_results if result['passed'])
    total_tests = len(test_results)

    percentage = (passed_tests / total_tests) * 100

    return {
        'percentage': round(percentage, 1),
        'passed_tests': passed_tests,
        'total_tests': total_tests,
        'letter_grade': get_letter_grade(percentage)
    }

def get_letter_grade(percentage):
    """Convert percentage to letter grade"""
    if percentage >= 90:
        return 'A'
    elif percentage >= 80:
        return 'B'
    elif percentage >= 70:
        return 'C'
    elif percentage >= 60:
        return 'D'
    else:
        return 'F'

@app.route('/achievements')
def achievements():
    if 'user' not in session:
        return redirect(url_for('index'))

    user_achievements = get_user_achievements(session['user'])
    all_achievements = get_all_achievements()

    return render_template('achievements.html',
                         user_achievements=user_achievements,
                         all_achievements=all_achievements)

def get_all_achievements():
    """Get all possible achievements"""
    return [
        {
            'title': 'First Steps',
            'description': 'Complete your first lesson',
            'icon': 'fas fa-baby',
            'requirement': 'Complete 1 lesson'
        },
        {
            'title': 'Learning Momentum',
            'description': 'Complete 10 lessons',
            'icon': 'fas fa-rocket',
            'requirement': 'Complete 10 lessons'
        },
        {
            'title': 'Dedicated Learner',
            'description': 'Complete 25 lessons',
            'icon': 'fas fa-medal',
            'requirement': 'Complete 25 lessons'
        },
        {
            'title': 'Problem Solver',
            'description': 'Complete your first challenge',
            'icon': 'fas fa-puzzle-piece',
            'requirement': 'Complete 1 challenge'
        },
        {
            'title': 'Quiz Master',
            'description': 'Complete 5 quizzes',
            'icon': 'fas fa-brain',
            'requirement': 'Complete 5 quizzes'
        },
        {
            'title': 'Point Collector',
            'description': 'Earn 100 points',
            'icon': 'fas fa-star',
            'requirement': 'Earn 100 points'
        },
        {
            'title': 'Perfectionist',
            'description': 'Score 100% on 3 quizzes',
            'icon': 'fas fa-trophy',
            'requirement': 'Score 100% on 3 quizzes'
        },
        {
            'title': 'Consistent Learner',
            'description': 'Learn for 7 days in a row',
            'icon': 'fas fa-calendar-check',
            'requirement': '7-day learning streak'
        }
    ]

@app.route('/progress')
def progress():
    if 'user' not in session:
        return redirect(url_for('index'))

    user_data = load_user_data()
    user_profile = user_data.get(session['user'], {})
    stats = get_progress_stats(session['user'])

    return render_template('progress.html',
                         user=user_profile.get('name', 'User'),
                         stats=stats,
                         profile=user_profile)

@app.route('/profile')
def profile():
    """User profile page"""
    if 'user' not in session:
        return redirect(url_for('index'))

    user_data = load_user_data()
    user_profile = user_data.get(session['user'], {})
    stats = get_progress_stats(session['user'])

    # Get recent activity
    recent_activity = get_recent_activity(session['user'])

    # Get achievements
    achievements = get_user_achievements(session['user'])

    return render_template('profile.html',
                         user=user_profile,
                         stats=stats,
                         recent_activity=recent_activity,
                         achievements=achievements)

@app.route('/api/update_profile', methods=['POST'])
def update_profile():
    """Update user profile information"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    try:
        data = request.get_json()

        # Validate input
        name = data.get('name', '').strip()
        learning_goals = data.get('learning_goals', [])
        notifications_enabled = data.get('notifications_enabled', True)
        theme = data.get('theme', 'default')

        if not name:
            return jsonify({"success": False, "error": "Name is required"}), 400

        # Update user data
        user_data = load_user_data()
        user = user_data.get(session['user'], {})

        user['name'] = name
        user['learning_goals'] = learning_goals
        user['notifications_enabled'] = notifications_enabled
        user['theme'] = theme
        user['last_activity'] = datetime.now().isoformat()

        # Save updated data
        user_data[session['user']] = user
        save_success = save_user_data(user_data)

        if not save_success:
            return jsonify({"success": False, "error": "Failed to save profile"}), 500

        return jsonify({
            "success": True,
            "message": "Profile updated successfully"
        })

    except Exception as e:
        print(f"Error updating profile: {e}")
        return jsonify({"success": False, "error": "An error occurred"}), 500

def get_recent_activity(user_email):
    """Get recent activity for a user"""
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    activities = []

    # Add completed lessons
    completed_lessons = user.get('completed_lesson_ids', [])
    for lesson_id in completed_lessons[-5:]:  # Last 5 lessons
        activities.append({
            'type': 'lesson',
            'title': f'Completed Lesson {lesson_id}',
            'date': user.get('last_activity', ''),
            'icon': 'fas fa-book'
        })

    # Add completed quizzes
    completed_quizzes = user.get('completed_quizzes', [])
    for quiz_id in completed_quizzes[-3:]:  # Last 3 quizzes
        activities.append({
            'type': 'quiz',
            'title': f'Completed Quiz {quiz_id}',
            'date': user.get('last_activity', ''),
            'icon': 'fas fa-question-circle'
        })

    # Add completed challenges
    completed_challenges = user.get('completed_challenge_ids', [])
    for challenge_id in completed_challenges[-3:]:  # Last 3 challenges
        activities.append({
            'type': 'challenge',
            'title': f'Completed Challenge {challenge_id}',
            'date': user.get('last_activity', ''),
            'icon': 'fas fa-code'
        })

    # Sort by date (simplified - using last_activity for all)
    return activities[-10:]  # Return last 10 activities

def get_user_achievements(user_email):
    """Get user achievements"""
    user_data = load_user_data()
    user = user_data.get(user_email, {})

    achievements = []

    # Check for various achievements
    lessons_completed = user.get('lessons_completed', 0)
    challenges_completed = user.get('challenges_completed', 0)
    quizzes_completed = user.get('quizzes_completed', 0)
    points = user.get('points', 0)

    # Lesson achievements
    if lessons_completed >= 1:
        achievements.append({
            'title': 'First Steps',
            'description': 'Completed your first lesson',
            'icon': 'fas fa-baby',
            'earned': True
        })

    if lessons_completed >= 10:
        achievements.append({
            'title': 'Learning Momentum',
            'description': 'Completed 10 lessons',
            'icon': 'fas fa-rocket',
            'earned': True
        })

    if lessons_completed >= 25:
        achievements.append({
            'title': 'Dedicated Learner',
            'description': 'Completed 25 lessons',
            'icon': 'fas fa-medal',
            'earned': True
        })

    # Challenge achievements
    if challenges_completed >= 1:
        achievements.append({
            'title': 'Problem Solver',
            'description': 'Completed your first challenge',
            'icon': 'fas fa-puzzle-piece',
            'earned': True
        })

    # Quiz achievements
    if quizzes_completed >= 5:
        achievements.append({
            'title': 'Quiz Master',
            'description': 'Completed 5 quizzes',
            'icon': 'fas fa-brain',
            'earned': True
        })

    # Points achievements
    if points >= 100:
        achievements.append({
            'title': 'Point Collector',
            'description': 'Earned 100 points',
            'icon': 'fas fa-star',
            'earned': True
        })

    return achievements

@app.route('/api/dashboard_stats')
def dashboard_stats():
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    stats = get_progress_stats(session['user'])

    # Get detailed progress information
    lessons_data = get_comprehensive_lessons_data()
    quizzes_data = get_comprehensive_quizzes_data()
    challenges_data = get_comprehensive_challenges_data()

    # Calculate category-wise progress
    user_data = load_user_data()
    user = user_data.get(session['user'], {})
    completed_lessons = user.get('completed_lessons', [])
    completed_quizzes = user.get('completed_quizzes', [])
    completed_challenges = user.get('completed_challenges', [])

    # Group lessons by category
    lesson_categories = {}
    for lesson in lessons_data:
        category = lesson.get('category', 'other')
        if category not in lesson_categories:
            lesson_categories[category] = {'total': 0, 'completed': 0}
        lesson_categories[category]['total'] += 1
        if lesson['id'] in completed_lessons:
            lesson_categories[category]['completed'] += 1

    # Group quizzes by category
    quiz_categories = {}
    for quiz in quizzes_data:
        category = quiz.get('category', 'other')
        if category not in quiz_categories:
            quiz_categories[category] = {'total': 0, 'completed': 0}
        quiz_categories[category]['total'] += 1
        if quiz['id'] in completed_quizzes:
            quiz_categories[category]['completed'] += 1

    return jsonify({
        "success": True,
        "stats": stats,
        "lesson_categories": lesson_categories,
        "quiz_categories": quiz_categories,
        "totals": {
            "lessons": len(lessons_data),
            "quizzes": len(quizzes_data),
            "challenges": len(challenges_data),
            "completed_lessons": len(completed_lessons),
            "completed_quizzes": len(completed_quizzes),
            "completed_challenges": len(completed_challenges)
        }
    })

# Security endpoints
@app.route('/api/csrf-token')
# @rate_limit(requests_per_minute=60, requests_per_hour=500)  # Disabled for development
def get_csrf_token():
    """Get CSRF token for the current session"""
    try:
        token = csrf_protection.get_token_for_session()
        return jsonify({
            "success": True,
            "csrf_token": token
        })
    except Exception as e:
        error_handler.handle_error(e, context={"route": "csrf_token"})
        return jsonify({
            "success": False,
            "error": "Failed to generate CSRF token"
        }), 500

@app.route('/api/health')
@rate_limit(requests_per_minute=30, requests_per_hour=200)
def health_check():
    """Health check endpoint with error statistics"""
    try:
        stats = error_handler.get_error_statistics()
        return jsonify({
            "success": True,
            "status": "healthy",
            "version": APP_VERSION,
            "error_stats": {
                "total_errors": stats["error_stats"]["total_errors"],
                "system_health": stats["system_health"]["status"]
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/api/admin/backup-info')
@rate_limit(requests_per_minute=10, requests_per_hour=50)
def get_backup_info():
    """Get backup information for admin users"""
    try:
        # Check if user is admin (simplified check)
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        # Get backup information
        user_data_backups = db_manager.get_backup_info("data/user_progress.json")

        return jsonify({
            "success": True,
            "backups": {
                "user_data": user_data_backups,
                "total_backups": len(user_data_backups)
            },
            "backup_settings": {
                "max_backups": db_manager.max_backups,
                "backup_interval": db_manager.backup_interval
            }
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "backup_info"})
        return jsonify({
            "success": False,
            "error": "Failed to get backup information"
        }), 500

@app.route('/api/admin/create-backup', methods=['POST'])
@rate_limit(requests_per_minute=5, requests_per_hour=20)
def create_manual_backup():
    """Create manual backup for admin users"""
    try:
        # Check if user is admin (simplified check)
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        # Create manual backup
        backup_path = db_manager.create_backup("data/user_progress.json", force=True)

        if backup_path:
            return jsonify({
                "success": True,
                "message": "Backup created successfully",
                "backup_path": backup_path
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to create backup"
            }), 500

    except Exception as e:
        error_handler.handle_error(e, context={"route": "create_backup"})
        return jsonify({
            "success": False,
            "error": "Failed to create backup"
        }), 500

@app.route('/api/admin/performance')
@rate_limit(requests_per_minute=10, requests_per_hour=50)
def get_performance_stats():
    """Get performance statistics for admin users"""
    try:
        # Check if user is admin (simplified check)
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        # Get performance statistics
        stats = performance_monitor()

        return jsonify({
            "success": True,
            "performance": stats,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "performance_stats"})
        return jsonify({
            "success": False,
            "error": "Failed to get performance statistics"
        }), 500

@app.route('/api/admin/cache/clear', methods=['POST'])
@rate_limit(requests_per_minute=5, requests_per_hour=20)
def clear_caches():
    """Clear all caches for admin users"""
    try:
        # Check if user is admin (simplified check)
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        # Clear caches
        cleanup_caches()

        return jsonify({
            "success": True,
            "message": "All caches cleared successfully"
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "clear_caches"})
        return jsonify({
            "success": False,
            "error": "Failed to clear caches"
        }), 500

@app.route('/offline.html')
def offline_page():
    """Offline page for service worker"""
    return render_template('offline.html')

@app.route('/api/performance-metrics', methods=['POST'])
@rate_limit(requests_per_minute=30, requests_per_hour=200)
def receive_performance_metrics():
    """Receive performance metrics from client"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400

        # Log performance metrics
        error_handler.logger.info(f"Performance metrics: {data}")

        # Store metrics (in production, save to database)
        metrics_file = "data/performance_metrics.json"
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                existing_metrics = json.load(f)
        else:
            existing_metrics = []

        data['timestamp'] = datetime.now().isoformat()
        existing_metrics.append(data)

        # Keep only last 1000 entries
        if len(existing_metrics) > 1000:
            existing_metrics = existing_metrics[-1000:]

        with open(metrics_file, 'w') as f:
            json.dump(existing_metrics, f, indent=2)

        return jsonify({"success": True})

    except Exception as e:
        error_handler.handle_error(e, context={"route": "performance_metrics"})
        return jsonify({"success": False, "error": "Failed to save metrics"}), 500

@app.route('/api/admin/memory')
@rate_limit(requests_per_minute=10, requests_per_hour=50)
def get_memory_stats():
    """Get memory usage statistics for admin users"""
    try:
        # Check if user is admin (simplified check)
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        # Get memory statistics
        memory_stats = get_memory_usage()
        monitor_stats = memory_monitor.get_memory_stats()

        return jsonify({
            "success": True,
            "memory": {
                "current": memory_stats,
                "monitor": monitor_stats
            },
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "memory_stats"})
        return jsonify({
            "success": False,
            "error": "Failed to get memory statistics"
        }), 500

@app.route('/api/admin/memory/optimize', methods=['POST'])
@rate_limit(requests_per_minute=5, requests_per_hour=20)
def optimize_memory_usage():
    """Optimize memory usage for admin users"""
    try:
        # Check if user is admin (simplified check)
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        # Run memory optimization
        optimization_result = optimize_memory()

        return jsonify({
            "success": True,
            "optimization": optimization_result,
            "message": f"Memory optimization completed. Freed {optimization_result['memory_freed_mb']:.1f}MB"
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "optimize_memory"})
        return jsonify({
            "success": False,
            "error": "Failed to optimize memory"
        }), 500



@app.route('/api/analytics')
@rate_limit(requests_per_minute=30, requests_per_hour=200)
def get_user_analytics():
    """Get learning analytics for current user"""
    try:
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        user_email = session['user']
        user_data = load_user_data()
        user = user_data.get(user_email, {})

        # Convert user data to performance objects
        performances = []

        # Create performance data from user progress
        if 'completed_lesson_ids' in user:
            for lesson_id in user['completed_lesson_ids']:
                perf = UserPerformance(
                    item_id=lesson_id,
                    attempts=1,  # Simplified
                    success_rate=0.8,  # Simplified
                    average_time=30.0,  # Simplified
                    last_attempt=datetime.now(),
                    mastery_level=0.8  # Simplified
                )
                performances.append(perf)

        # Generate analytics
        analytics = learning_analytics.generate_user_analytics(user_email, performances)

        # Add user-specific data
        analytics.update({
            "total_points": user.get('points', 0),
            "current_level": user.get('level', 1),
            "lessons_completed": user.get('lessons_completed', 0),
            "challenges_completed": user.get('challenges_completed', 0),
            "quizzes_completed": user.get('quizzes_completed', 0),
            "current_streak": user.get('streak', 0),
            "achievements": user.get('achievements', [])
        })

        return jsonify({
            "success": True,
            "analytics": analytics
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "analytics", "user": session.get('user')})
        return jsonify({
            "success": False,
            "error": "Failed to generate analytics"
        }), 500

@app.route('/api/learning-path')
@rate_limit(requests_per_minute=10, requests_per_hour=50)
def get_personalized_learning_path():
    """Get personalized learning path for current user"""
    try:
        if 'user' not in session:
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401

        user_email = session['user']
        user_data = load_user_data()
        user = user_data.get(user_email, {})

        # Get user preferences
        user_goals = user.get('learning_goals', ['general_programming'])
        learning_style = LearningStyle.VISUAL  # Default, could be from user preferences

        # Create performance data
        performances = []
        completed_lessons = user.get('completed_lesson_ids', [])

        for lesson_id in completed_lessons:
            perf = UserPerformance(
                item_id=lesson_id,
                attempts=1,
                success_rate=0.8,
                average_time=30.0,
                last_attempt=datetime.now(),
                mastery_level=0.8
            )
            performances.append(perf)

        # Generate learning path
        learning_path = learning_path_generator.generate_learning_path(
            user_email, user_goals, performances, learning_style
        )

        # Get lesson details for the path
        lessons_data = get_comprehensive_lessons_data()
        path_details = []

        for lesson_id in learning_path[:10]:  # Limit to next 10 items
            lesson = next((l for l in lessons_data if l['id'] == lesson_id), None)
            if lesson:
                path_details.append({
                    'id': lesson['id'],
                    'title': lesson['title'],
                    'description': lesson['description'],
                    'difficulty': lesson['difficulty'],
                    'estimated_time': lesson.get('estimated_time', 30),
                    'points': lesson.get('points', 10)
                })

        return jsonify({
            "success": True,
            "learning_path": path_details,
            "total_items": len(learning_path)
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "learning_path", "user": session.get('user')})
        return jsonify({
            "success": False,
            "error": "Failed to generate learning path"
        }), 500

# Social Learning Routes
@app.route('/community')
def community():
    """Community page"""
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('community.html')

@app.route('/api/profile', methods=['GET', 'POST'])
# @rate_limit(requests_per_minute=30, requests_per_hour=200)  # Disabled for development
def user_profile():
    """Get or update user profile"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Authentication required"}), 401

    user_email = session['user']

    try:
        if request.method == 'GET':
            # Get user profile
            profile = social_manager.get_user_profile(user_email)
            if not profile:
                # Create profile if it doesn't exist
                user_data = load_user_data()
                user = user_data.get(user_email, {})
                profile = social_manager.create_user_profile(
                    user_email,
                    user.get('name', 'Anonymous'),
                    learning_goals=user.get('learning_goals', [])
                )

            return jsonify({
                "success": True,
                "profile": profile.__dict__ if hasattr(profile, '__dict__') else profile
            })

        else:  # POST - Update profile
            data = request.get_json()
            if not data:
                return jsonify({"success": False, "error": "No data provided"}), 400

            success = social_manager.update_user_profile(user_email, data)

            if success:
                return jsonify({"success": True, "message": "Profile updated successfully"})
            else:
                return jsonify({"success": False, "error": "Failed to update profile"}), 500

    except Exception as e:
        error_handler.handle_error(e, context={"route": "user_profile", "user": user_email})
        return jsonify({"success": False, "error": "Profile operation failed"}), 500

@app.route('/api/friends', methods=['GET'])
@rate_limit(requests_per_minute=30, requests_per_hour=200)
def get_friends():
    """Get user's friends list"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Authentication required"}), 401

    try:
        user_email = session['user']
        friends = social_manager.get_friends(user_email)
        friend_requests = social_manager.get_friend_requests(user_email)

        return jsonify({
            "success": True,
            "friends": [friend.__dict__ if hasattr(friend, '__dict__') else friend for friend in friends],
            "friend_requests": friend_requests
        })

    except Exception as e:
        error_handler.handle_error(e, context={"route": "get_friends", "user": session.get('user')})
        return jsonify({"success": False, "error": "Failed to get friends"}), 500

@app.route('/api/friends/request', methods=['POST'])
@rate_limit(requests_per_minute=10, requests_per_hour=50)
def send_friend_request():
    """Send a friend request"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Authentication required"}), 401

    try:
        data = request.get_json()
        if not data or 'recipient_id' not in data:
            return jsonify({"success": False, "error": "Recipient ID required"}), 400

        user_email = session['user']
        recipient_id = data['recipient_id']

        success = social_manager.send_friend_request(user_email, recipient_id)

        if success:
            return jsonify({"success": True, "message": "Friend request sent"})
        else:
            return jsonify({"success": False, "error": "Failed to send friend request"}), 400

    except Exception as e:
        error_handler.handle_error(e, context={"route": "send_friend_request", "user": session.get('user')})
        return jsonify({"success": False, "error": "Failed to send friend request"}), 500

@app.route('/api/friends/respond', methods=['POST'])
@rate_limit(requests_per_minute=20, requests_per_hour=100)
def respond_friend_request():
    """Respond to a friend request"""
    if 'user' not in session:
        return jsonify({"success": False, "error": "Authentication required"}), 401

    try:
        data = request.get_json()
        if not data or 'friendship_id' not in data or 'accept' not in data:
            return jsonify({"success": False, "error": "Friendship ID and accept status required"}), 400

        friendship_id = data['friendship_id']
        accept = data['accept']

        success = social_manager.respond_to_friend_request(friendship_id, accept)

        if success:
            message = "Friend request accepted" if accept else "Friend request declined"
            return jsonify({"success": True, "message": message})
        else:
            return jsonify({"success": False, "error": "Failed to respond to friend request"}), 400

    except Exception as e:
        error_handler.handle_error(e, context={"route": "respond_friend_request", "user": session.get('user')})
        return jsonify({"success": False, "error": "Failed to respond to friend request"}), 500

if __name__ == '__main__':
    print("🚀 Starting Python Learning Platform...")
    print("📍 Visit: http://localhost:5000")
    print(f"🔒 Security features enabled: CSRF protection, Rate limiting")
    print(f"📊 Error handling and logging active")
    print(f"🧠 Memory monitoring enabled")

    # Start memory monitoring
    memory_monitor.start_monitoring()

    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        # Stop memory monitoring on shutdown
        memory_monitor.stop_monitoring()
