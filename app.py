from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Application metadata
APP_VERSION = "2.0.0"
APP_NAME = "Python Learning Platform"
APP_DESCRIPTION = "Comprehensive Python learning platform with interactive lessons, challenges, and gamification"

def load_user_data():
    try:
        if os.path.exists("data/user_progress.json"):
            with open("data/user_progress.json", 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_user_data(data):
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/user_progress.json", 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving: {e}")

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
        'days_since_start': user.get('days_since_start', 0)
    }

def get_comprehensive_lessons_data():
    """
    Comprehensive Python learning curriculum with 50 lessons covering:
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
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    data = request.get_json()
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({"success": False, "error": "All fields required"}), 400

    user_data = load_user_data()
    if data['email'] in user_data:
        return jsonify({"success": False, "error": "Email exists"}), 400

    user_profile = {
        "name": data['name'],
        "email": data['email'],
        "password": data['password'],
        "experience_level": data.get('experience_level', 'complete_beginner'),
        "learning_goals": data.get('learning_goals', []),
        "created_at": datetime.now().isoformat(),
        "lessons_completed": 0,
        "points": 0,
        "level": 1,
        "streak": 0,
        "challenges_completed": 0,
        "quizzes_completed": 0,
        "quizzes_taken": 0,
        "playground_uses": 0,
        "average_quiz_score": 0,
        "days_since_start": 0,
        "achievements": []
    }

    user_data[data['email']] = user_profile
    save_user_data(user_data)
    session['user'] = data['email']
    session['first_time'] = True
    return jsonify({"success": True, "redirect": url_for('welcome_user')})

@app.route('/welcome_user')
def welcome_user():
    if 'user' not in session:
        return redirect(url_for('index'))
    
    user_data = load_user_data()
    user_profile = user_data.get(session['user'], {})
    session['show_dashboard_tour'] = True
    return render_template('welcome_user.html', user_profile=user_profile)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.get_json()
    if not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "error": "Email and password required"}), 400
    
    user_data = load_user_data()
    user = user_data.get(data['email'])
    
    if not user or user.get('password') != data['password']:
        return jsonify({"success": False, "error": "Invalid credentials"}), 401
    
    session['user'] = data['email']
    return jsonify({"success": True, "redirect": url_for('dashboard')})

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
    return render_template('lesson_detail.html', lesson_id=lesson_id)

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
    completed_challenges = user.get('completed_challenges', [])
    is_completed = challenge_id in completed_challenges

    return render_template('challenge_detail.html',
                         challenge=challenge,
                         is_completed=is_completed)

def get_comprehensive_quizzes_data():
    """
    Comprehensive quiz system covering:
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
def submit_quiz():
    if 'user' not in session:
        return jsonify({"success": False, "error": "Not logged in"}), 401

    data = request.get_json()
    quiz_id = data.get('quiz_id')
    user_answers = data.get('answers', {})

    # Get quiz data
    quizzes_data = get_comprehensive_quizzes_data()
    quiz = next((q for q in quizzes_data if q['id'] == quiz_id), None)

    if not quiz:
        return jsonify({"success": False, "error": "Quiz not found"}), 404

    # Calculate score
    correct_answers = 0
    total_questions = len(quiz.get('questions_data', []))

    if total_questions == 0:
        total_questions = quiz.get('questions', 5)  # Fallback for quizzes without detailed questions

    for question in quiz.get('questions_data', []):
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

    # Calculate percentage and points
    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    points_earned = int((percentage / 100) * quiz.get('points', 25))

    # Update user progress
    user_data = load_user_data()
    user = user_data.get(session['user'], {})

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

    # Save updated user data
    user_data[session['user']] = user
    save_user_data(user_data)

    return jsonify({
        "success": True,
        "score": percentage,
        "points_earned": points_earned,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "message": f"Quiz completed! You scored {percentage:.1f}% and earned {points_earned} points."
    })

@app.route('/playground')
def playground():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('playground.html')

@app.route('/achievements')
def achievements():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('achievements.html')

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

if __name__ == '__main__':
    print("🚀 Starting Python Learning Platform...")
    print("📍 Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
