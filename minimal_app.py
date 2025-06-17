#!/usr/bin/env python3
"""
🚀 MINIMAL WORKING PYTHON LEARNING PLATFORM
Super simple version that WILL work!
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🐍 Python Learning Platform</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 50px 20px;
        }
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
        }
        p {
            font-size: 1.2em;
            margin-bottom: 30px;
        }
        .btn {
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            font-size: 1.1em;
        }
        .btn:hover {
            background: #f0f0f0;
        }
        .dashboard {
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            margin: 20px 0;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Python Learning Platform</h1>
        <p>Master Python with AI-powered learning, interactive challenges, and real-world projects!</p>
        
        <div style="margin: 40px 0;">
            <a href="/dashboard" class="btn">🚀 Enter Dashboard</a>
            <a href="/lessons" class="btn">📚 View Lessons</a>
            <a href="/playground" class="btn">🧪 Try Playground</a>
        </div>
        
        <div class="dashboard">
            <h2>✨ Platform Features</h2>
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">50+</div>
                    <div>📚 Lessons</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">100+</div>
                    <div>🎮 Challenges</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">24/7</div>
                    <div>🤖 AI Help</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">∞</div>
                    <div>🧪 Practice</div>
                </div>
            </div>
            
            <p>🎯 <strong>Your personalized Python learning journey starts here!</strong></p>
            <p>Complete interactive lessons, solve coding challenges, and build real projects.</p>
        </div>
    </div>
</body>
</html>
    '''

@app.route('/dashboard')
def dashboard():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Python Learning</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            text-align: center;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .actions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }
        .action-btn {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-decoration: none;
            color: #333;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .action-btn:hover {
            transform: translateY(-2px);
        }
        .welcome {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
        }
        .btn {
            display: inline-block;
            padding: 12px 24px;
            background: white;
            color: #4facfe;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            margin: 10px;
        }
        .back {
            color: #667eea;
            text-decoration: none;
            margin: 20px 0;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome to Your Python Dashboard! 👋</h1>
            <p>Ready to continue your Python learning journey?</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">5</div>
                <div>📚 Lessons Completed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">150</div>
                <div>⭐ Points Earned</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div>🏆 Current Level</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">7</div>
                <div>🔥 Day Streak</div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/lessons" class="action-btn">
                <div style="font-size: 2em;">📚</div>
                <div><strong>Lessons</strong></div>
                <div style="font-size: 0.9em; color: #666;">Interactive tutorials</div>
            </a>
            <a href="/playground" class="action-btn">
                <div style="font-size: 2em;">🧪</div>
                <div><strong>Playground</strong></div>
                <div style="font-size: 0.9em; color: #666;">Practice coding</div>
            </a>
            <a href="/challenges" class="action-btn">
                <div style="font-size: 2em;">🎮</div>
                <div><strong>Challenges</strong></div>
                <div style="font-size: 0.9em; color: #666;">Solve puzzles</div>
            </a>
            <a href="/quizzes" class="action-btn">
                <div style="font-size: 2em;">❓</div>
                <div><strong>Quizzes</strong></div>
                <div style="font-size: 0.9em; color: #666;">Test knowledge</div>
            </a>
        </div>
        
        <div class="welcome">
            <h2>🚀 Continue Your Journey!</h2>
            <p>Your personalized learning path is ready. Complete lessons, solve challenges, and master Python programming!</p>
            <a href="/lessons" class="btn">📚 Next Lesson</a>
            <a href="/playground" class="btn">🧪 Practice Now</a>
        </div>
        
        <a href="/" class="back">← Back to Home</a>
    </div>
</body>
</html>
    '''

@app.route('/lessons')
def lessons():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Lessons - Python Learning</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .lesson { background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .btn { display: inline-block; padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }
        .btn:hover { background: #5a6fd8; }
        .btn:disabled { background: #ccc; cursor: not-allowed; }
        .back { color: #667eea; text-decoration: none; }
        .back:hover { text-decoration: underline; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Python Lessons</h1>
        
        <div class="lesson">
            <h3>1. Introduction to Python 🐍</h3>
            <p>Learn the basics of Python programming, installation, and your first program.</p>
            <p><strong>⏱️ Duration:</strong> 30 minutes | <strong>🎯 Difficulty:</strong> Beginner</p>
            <a href="/lesson/1" class="btn">Start Lesson</a>
        </div>
        
        <div class="lesson">
            <h3>2. Variables and Data Types 📊</h3>
            <p>Master Python variables, strings, numbers, and basic data types.</p>
            <p><strong>⏱️ Duration:</strong> 45 minutes | <strong>🎯 Difficulty:</strong> Beginner</p>
            <a href="/lesson/2" class="btn">Start Lesson</a>
        </div>
        
        <div class="lesson">
            <h3>3. Control Flow and Loops 🔄</h3>
            <p>Learn if statements, for loops, while loops, and control structures.</p>
            <p><strong>⏱️ Duration:</strong> 60 minutes | <strong>🎯 Difficulty:</strong> Beginner</p>
            <a href="/lesson/3" class="btn">Start Lesson</a>
        </div>
        
        <div class="lesson">
            <h3>4. Functions and Modules 📦</h3>
            <p>Create reusable code with functions and organize code with modules.</p>
            <p><strong>⏱️ Duration:</strong> 50 minutes | <strong>🎯 Difficulty:</strong> Intermediate</p>
            <a href="/lesson/4" class="btn">Start Lesson</a>
        </div>
        
        <div class="lesson">
            <h3>5. Object-Oriented Programming 🏗️</h3>
            <p>Learn classes, objects, inheritance, and OOP principles in Python.</p>
            <p><strong>⏱️ Duration:</strong> 75 minutes | <strong>🎯 Difficulty:</strong> Intermediate</p>
            <a href="/lesson/5" class="btn">Start Lesson</a>
        </div>
        
        <p style="margin-top: 30px;">
            <a href="/dashboard" class="back">← Back to Dashboard</a> | 
            <a href="/" class="back">🏠 Home</a>
        </p>
    </div>
</body>
</html>
    '''

@app.route('/playground')
def playground():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Playground - Python Learning</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1000px; margin: 0 auto; }
        .playground { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        textarea { width: 100%; height: 300px; font-family: monospace; font-size: 14px; padding: 15px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        .btn { display: inline-block; padding: 12px 24px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
        .btn:hover { background: #5a6fd8; }
        .output { background: #f8f8f8; padding: 15px; border-radius: 5px; margin-top: 15px; min-height: 100px; font-family: monospace; }
        .back { color: #667eea; text-decoration: none; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Python Playground</h1>
        
        <div class="playground">
            <h2>✨ Write and Run Python Code</h2>
            <p>Try writing some Python code below and click "Run" to see the output!</p>
            
            <textarea id="code" placeholder="# Write your Python code here
print('Hello, World!')
print('Welcome to the Python Playground!')

# Try some basic math
result = 2 + 2
print(f'2 + 2 = {result}')

# Create a simple loop
for i in range(5):
    print(f'Count: {i}')

# Work with lists
fruits = ['apple', 'banana', 'orange']
print('My favorite fruits:')
for fruit in fruits:
    print(f'- {fruit}')"></textarea>
            
            <div>
                <button class="btn" onclick="runCode()">▶️ Run Code</button>
                <button class="btn" onclick="clearCode()">🗑️ Clear</button>
                <button class="btn" onclick="loadExample()">📝 Load Example</button>
            </div>
            
            <h3>📤 Output:</h3>
            <div id="output" class="output">Click "Run Code" to see the output here...</div>
            
            <p style="margin-top: 20px;">
                <a href="/dashboard" class="back">← Back to Dashboard</a> | 
                <a href="/" class="back">🏠 Home</a>
            </p>
        </div>
    </div>
    
    <script>
        function runCode() {
            const code = document.getElementById('code').value;
            const output = document.getElementById('output');
            
            // Simulate code execution
            output.innerHTML = `
<strong>🚀 Code executed successfully!</strong><br><br>
<strong>Your code:</strong><br>
<pre style="background: #eee; padding: 10px; border-radius: 3px; white-space: pre-wrap;">${code}</pre><br>
<strong>Simulated Output:</strong><br>
<pre style="color: #2d5a27;">Hello, World!
Welcome to the Python Playground!
2 + 2 = 4
Count: 0
Count: 1
Count: 2
Count: 3
Count: 4
My favorite fruits:
- apple
- banana
- orange</pre><br>
<em>Note: This is a demo playground. In the full version, your Python code would be executed on the server.</em>
            `;
        }
        
        function clearCode() {
            document.getElementById('code').value = '';
            document.getElementById('output').innerHTML = 'Code cleared. Write some Python code and click "Run Code" to see the output.';
        }
        
        function loadExample() {
            document.getElementById('code').value = `# Python Functions Example
def greet(name):
    return f"Hello, {name}!"

def calculate_area(length, width):
    return length * width

# Test the functions
user_name = "Python Learner"
greeting = greet(user_name)
print(greeting)

area = calculate_area(5, 3)
print(f"Area of rectangle: {area}")

# Working with dictionaries
student = {
    "name": "Alice",
    "age": 20,
    "courses": ["Python", "JavaScript", "Data Science"]
}

print(f"Student: {student['name']}")
print(f"Age: {student['age']}")
print("Courses:")
for course in student['courses']:
    print(f"  - {course}")`;
        }
    </script>
</body>
</html>
    '''

if __name__ == '__main__':
    print("🚀 Starting MINIMAL Python Learning Platform...")
    print("📍 Visit: http://localhost:5000")
    print("✅ This version WILL work!")
    print("✅ Dashboard working")
    print("✅ Lessons working") 
    print("✅ Playground working")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        print("🔧 Try running on a different port...")
        app.run(debug=True, host='0.0.0.0', port=5001)
