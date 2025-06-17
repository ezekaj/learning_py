#!/usr/bin/env python3
"""
🚀 WORKING PYTHON LEARNING PLATFORM
Simplified version that definitely works
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Simple user data storage
def load_user_data():
    try:
        if os.path.exists("data/users.json"):
            with open("data/users.json", 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_user_data(data):
    try:
        os.makedirs("data", exist_ok=True)
        with open("data/users.json", 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving: {e}")
        return False

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>🐍 Python Learning Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-500 to-purple-600 min-h-screen">
    <div class="container mx-auto px-6 py-20 text-center text-white">
        <h1 class="text-6xl font-bold mb-6">🐍 Python Learning Platform</h1>
        <p class="text-2xl mb-8">Master Python with AI-powered learning</p>
        
        <div class="space-x-4">
            <a href="/register" class="bg-white text-blue-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-colors">
                🚀 Start Learning
            </a>
            <a href="/login" class="border-2 border-white text-white px-8 py-4 rounded-full font-bold text-lg hover:bg-white hover:text-blue-600 transition-colors">
                🔑 Sign In
            </a>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        users = load_user_data()
        if data['email'] in users:
            return jsonify({"success": False, "error": "Email already exists"}), 400
        
        # Create user
        users[data['email']] = {
            "name": data.get('name', 'User'),
            "email": data['email'],
            "password": data['password'],
            "created": datetime.now().isoformat(),
            "lessons_completed": 0,
            "points": 0,
            "level": 1
        }
        
        if save_user_data(users):
            session['user'] = data['email']
            return jsonify({"success": True, "redirect": "/dashboard"})
        else:
            return jsonify({"success": False, "error": "Failed to save user"}), 500
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Register - Python Learning</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-xl shadow-lg max-w-md w-full">
        <h2 class="text-2xl font-bold mb-6 text-center">🚀 Join Python Learning</h2>
        
        <form id="registerForm">
            <div class="mb-4">
                <input type="text" id="name" placeholder="Full Name" class="w-full p-3 border rounded-lg" required>
            </div>
            <div class="mb-4">
                <input type="email" id="email" placeholder="Email" class="w-full p-3 border rounded-lg" required>
            </div>
            <div class="mb-6">
                <input type="password" id="password" placeholder="Password" class="w-full p-3 border rounded-lg" required>
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white p-3 rounded-lg font-bold hover:bg-blue-700">
                Create Account
            </button>
        </form>
        
        <p class="text-center mt-4">
            <a href="/login" class="text-blue-600 hover:underline">Already have an account?</a>
        </p>
    </div>
    
    <script>
    document.getElementById('registerForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const data = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                window.location.href = result.redirect;
            } else {
                alert(result.error);
            }
        } catch (error) {
            alert('Error: ' + error);
        }
    });
    </script>
</body>
</html>
    ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        users = load_user_data()
        user = users.get(data['email'])
        
        if not user or user.get('password') != data['password']:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
        
        session['user'] = data['email']
        return jsonify({"success": True, "redirect": "/dashboard"})
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Login - Python Learning</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-xl shadow-lg max-w-md w-full">
        <h2 class="text-2xl font-bold mb-6 text-center">🔑 Welcome Back</h2>
        
        <form id="loginForm">
            <div class="mb-4">
                <input type="email" id="email" placeholder="Email" class="w-full p-3 border rounded-lg" required>
            </div>
            <div class="mb-6">
                <input type="password" id="password" placeholder="Password" class="w-full p-3 border rounded-lg" required>
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white p-3 rounded-lg font-bold hover:bg-blue-700">
                Sign In
            </button>
        </form>
        
        <p class="text-center mt-4">
            <a href="/register" class="text-blue-600 hover:underline">Need an account?</a>
        </p>
    </div>
    
    <script>
    document.getElementById('loginForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const data = {
            email: document.getElementById('email').value,
            password: document.getElementById('password').value
        };
        
        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                window.location.href = result.redirect;
            } else {
                alert(result.error);
            }
        } catch (error) {
            alert('Error: ' + error);
        }
    });
    </script>
</body>
</html>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    users = load_user_data()
    user = users.get(session['user'], {})
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Python Learning</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-6 py-8">
        <div class="flex justify-between items-center mb-8">
            <div>
                <h1 class="text-3xl font-bold text-gray-800">Welcome back, {{ user.name }}! 👋</h1>
                <p class="text-gray-600">Ready to continue your Python journey?</p>
            </div>
            <div class="flex space-x-4">
                <button onclick="startTour()" class="bg-blue-100 text-blue-600 px-4 py-2 rounded-lg hover:bg-blue-200">
                    <i class="fas fa-question-circle mr-2"></i>Take Tour
                </button>
                <a href="/logout" class="bg-red-100 text-red-600 px-4 py-2 rounded-lg hover:bg-red-200">
                    <i class="fas fa-sign-out-alt mr-2"></i>Logout
                </a>
            </div>
        </div>
        
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white p-6 rounded-xl shadow-lg">
                <div class="flex items-center">
                    <div class="text-3xl text-blue-600 mr-4">📚</div>
                    <div>
                        <div class="text-2xl font-bold">{{ user.lessons_completed or 0 }}</div>
                        <div class="text-gray-600">Lessons</div>
                    </div>
                </div>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-lg">
                <div class="flex items-center">
                    <div class="text-3xl text-green-600 mr-4">⭐</div>
                    <div>
                        <div class="text-2xl font-bold">{{ user.points or 0 }}</div>
                        <div class="text-gray-600">Points</div>
                    </div>
                </div>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-lg">
                <div class="flex items-center">
                    <div class="text-3xl text-purple-600 mr-4">🏆</div>
                    <div>
                        <div class="text-2xl font-bold">{{ user.level or 1 }}</div>
                        <div class="text-gray-600">Level</div>
                    </div>
                </div>
            </div>
            <div class="bg-white p-6 rounded-xl shadow-lg">
                <div class="flex items-center">
                    <div class="text-3xl text-orange-600 mr-4">🔥</div>
                    <div>
                        <div class="text-2xl font-bold">0</div>
                        <div class="text-gray-600">Streak</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="bg-white p-6 rounded-xl shadow-lg mb-8">
            <h2 class="text-xl font-bold mb-4">🚀 Quick Actions</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <a href="/lessons" class="bg-blue-100 text-blue-600 p-4 rounded-lg text-center hover:bg-blue-200">
                    <div class="text-2xl mb-2">📚</div>
                    <div class="font-medium">Lessons</div>
                </a>
                <a href="/playground" class="bg-green-100 text-green-600 p-4 rounded-lg text-center hover:bg-green-200">
                    <div class="text-2xl mb-2">🧪</div>
                    <div class="font-medium">Playground</div>
                </a>
                <a href="/challenges" class="bg-purple-100 text-purple-600 p-4 rounded-lg text-center hover:bg-purple-200">
                    <div class="text-2xl mb-2">🎮</div>
                    <div class="font-medium">Challenges</div>
                </a>
                <a href="/quizzes" class="bg-orange-100 text-orange-600 p-4 rounded-lg text-center hover:bg-orange-200">
                    <div class="text-2xl mb-2">❓</div>
                    <div class="font-medium">Quizzes</div>
                </a>
            </div>
        </div>
        
        <!-- Welcome Message -->
        <div class="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-6 rounded-xl">
            <h3 class="text-xl font-bold mb-2">🎉 Welcome to Python Learning!</h3>
            <p class="mb-4">Your personalized learning journey starts here. Complete lessons, solve challenges, and master Python programming!</p>
            <a href="/lessons" class="bg-white text-blue-600 px-6 py-2 rounded-lg font-medium hover:bg-gray-100">
                Start First Lesson
            </a>
        </div>
    </div>
    
    <script>
    function startTour() {
        alert('🎯 Dashboard tour coming soon! This will guide you through all features.');
    }
    </script>
</body>
</html>
    ''', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/lessons')
def lessons():
    if 'user' not in session:
        return redirect(url_for('home'))
    
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Lessons - Python Learning</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="container mx-auto px-6 py-8">
        <h1 class="text-3xl font-bold mb-8">📚 Python Lessons</h1>
        
        <div class="grid gap-6">
            <div class="bg-white p-6 rounded-xl shadow-lg">
                <h3 class="text-xl font-bold mb-2">1. Introduction to Python</h3>
                <p class="text-gray-600 mb-4">Learn the basics of Python programming</p>
                <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-500">⏱️ 30 minutes</span>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                        Start Lesson
                    </button>
                </div>
            </div>
            
            <div class="bg-white p-6 rounded-xl shadow-lg">
                <h3 class="text-xl font-bold mb-2">2. Variables and Data Types</h3>
                <p class="text-gray-600 mb-4">Master Python variables and data types</p>
                <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-500">⏱️ 45 minutes</span>
                    <button class="bg-gray-300 text-gray-600 px-4 py-2 rounded-lg" disabled>
                        Complete Lesson 1 First
                    </button>
                </div>
            </div>
        </div>
        
        <div class="mt-8">
            <a href="/dashboard" class="text-blue-600 hover:underline">← Back to Dashboard</a>
        </div>
    </div>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("🚀 Starting Python Learning Platform...")
    print("📍 Visit: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
