#!/usr/bin/env python3
"""
🚀 FIXED PYTHON LEARNING PLATFORM
Dashboard guaranteed to work!
"""

from flask import Flask, request, jsonify, session, redirect

app = Flask(__name__)
app.secret_key = 'fixed_secret_key_12345'

# Simple data storage
users = {}

@app.route('/')
def home():
    if 'user' in session:
        return dashboard()
    
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🐍 Python Learning Platform</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; text-align: center; min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; padding: 50px 20px; }
        h1 { font-size: 3em; margin-bottom: 20px; }
        p { font-size: 1.2em; margin-bottom: 30px; }
        .btn { display: inline-block; padding: 15px 30px; margin: 10px; background: white; color: #667eea; text-decoration: none; border-radius: 25px; font-weight: bold; font-size: 1.1em; }
        .btn:hover { background: #f0f0f0; }
        .form-container { background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px 0; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: none; border-radius: 8px; font-size: 1em; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: white; color: #667eea; border: none; border-radius: 8px; font-weight: bold; font-size: 1.1em; cursor: pointer; }
        button:hover { background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🐍 Python Learning Platform</h1>
        <p>Master Python with AI-powered learning!</p>
        
        <div style="margin: 40px 0;">
            <a href="#register" class="btn" onclick="showRegister()">🚀 Start Learning</a>
            <a href="#login" class="btn" onclick="showLogin()">🔑 Sign In</a>
        </div>
        
        <!-- Registration Form -->
        <div id="registerForm" class="form-container" style="display: none;">
            <h2>🚀 Create Account</h2>
            <form onsubmit="register(event)">
                <input type="text" id="regName" placeholder="Full Name" required>
                <input type="email" id="regEmail" placeholder="Email" required>
                <input type="password" id="regPassword" placeholder="Password" required>
                <button type="submit">Create Account</button>
            </form>
            <p><a href="#" onclick="showLogin()" style="color: white;">Have an account?</a></p>
        </div>
        
        <!-- Login Form -->
        <div id="loginForm" class="form-container" style="display: none;">
            <h2>🔑 Welcome Back</h2>
            <form onsubmit="login(event)">
                <input type="email" id="loginEmail" placeholder="Email" required>
                <input type="password" id="loginPassword" placeholder="Password" required>
                <button type="submit">Sign In</button>
            </form>
            <p><a href="#" onclick="showRegister()" style="color: white;">Need account?</a></p>
        </div>
    </div>
    
    <script>
        function showRegister() {
            document.getElementById('registerForm').style.display = 'block';
            document.getElementById('loginForm').style.display = 'none';
        }
        
        function showLogin() {
            document.getElementById('loginForm').style.display = 'block';
            document.getElementById('registerForm').style.display = 'none';
        }
        
        async function register(event) {
            event.preventDefault();
            
            const data = {
                name: document.getElementById('regName').value,
                email: document.getElementById('regEmail').value,
                password: document.getElementById('regPassword').value
            };
            
            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('🎉 Account created! Redirecting to dashboard...');
                    window.location.reload();
                } else {
                    alert('❌ ' + result.error);
                }
            } catch (error) {
                alert('❌ Error: ' + error);
            }
        }
        
        async function login(event) {
            event.preventDefault();
            
            const data = {
                email: document.getElementById('loginEmail').value,
                password: document.getElementById('loginPassword').value
            };
            
            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (result.success) {
                    alert('✅ Login successful! Loading dashboard...');
                    window.location.reload();
                } else {
                    alert('❌ ' + result.error);
                }
            } catch (error) {
                alert('❌ Error: ' + error);
            }
        }
    </script>
</body>
</html>
    '''

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Registration attempt: {data}")
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        if data['email'] in users:
            return jsonify({"success": False, "error": "Email already exists"}), 400
        
        # Create user
        users[data['email']] = {
            "name": data.get('name', 'User'),
            "email": data['email'],
            "password": data['password'],
            "lessons_completed": 0,
            "points": 0,
            "level": 1
        }
        
        session['user'] = data['email']
        print(f"User created and logged in: {data['email']}")
        return jsonify({"success": True})
        
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"success": False, "error": "Registration failed"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"Login attempt: {data}")
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"success": False, "error": "Email and password required"}), 400
        
        user = users.get(data['email'])
        
        if not user or user.get('password') != data['password']:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
        
        session['user'] = data['email']
        print(f"User logged in: {data['email']}")
        return jsonify({"success": True})
        
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"success": False, "error": "Login failed"}), 500

def dashboard():
    try:
        user_email = session.get('user')
        user = users.get(user_email, {})
        print(f"Dashboard for user: {user_email}")
        
        return f'''
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard - Python Learning</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin-bottom: 30px; position: relative; }}
        .logout {{ position: absolute; top: 20px; right: 20px; background: rgba(255,255,255,0.2); color: white; padding: 10px 20px; border-radius: 20px; text-decoration: none; }}
        .logout:hover {{ background: rgba(255,255,255,0.3); }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .actions {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin-bottom: 30px; }}
        .action-btn {{ background: white; padding: 20px; border-radius: 10px; text-decoration: none; color: #333; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.1); transition: transform 0.2s; }}
        .action-btn:hover {{ transform: translateY(-2px); }}
        .welcome {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; border-radius: 15px; text-align: center; }}
        .btn {{ display: inline-block; padding: 12px 24px; background: white; color: #4facfe; text-decoration: none; border-radius: 25px; font-weight: bold; margin: 10px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="/logout" class="logout">🚪 Logout</a>
            <h1>Welcome back, {user.get('name', 'User')}! 👋</h1>
            <p>Ready to continue your Python journey?</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{user.get('lessons_completed', 0)}</div>
                <div>📚 Lessons</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{user.get('points', 0)}</div>
                <div>⭐ Points</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{user.get('level', 1)}</div>
                <div>🏆 Level</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">0</div>
                <div>🔥 Streak</div>
            </div>
        </div>
        
        <div class="actions">
            <a href="/lessons" class="action-btn">
                <div style="font-size: 2em;">📚</div>
                <div><strong>Lessons</strong></div>
            </a>
            <a href="/playground" class="action-btn">
                <div style="font-size: 2em;">🧪</div>
                <div><strong>Playground</strong></div>
            </a>
            <a href="/challenges" class="action-btn">
                <div style="font-size: 2em;">🎮</div>
                <div><strong>Challenges</strong></div>
            </a>
            <a href="/quizzes" class="action-btn">
                <div style="font-size: 2em;">❓</div>
                <div><strong>Quizzes</strong></div>
            </a>
        </div>
        
        <div class="welcome">
            <h2>🎉 Welcome to Python Learning!</h2>
            <p>Your journey starts here. Complete lessons, solve challenges, and master Python!</p>
            <a href="/lessons" class="btn">🚀 Start Learning</a>
        </div>
    </div>
</body>
</html>
        '''
    except Exception as e:
        print(f"Dashboard error: {e}")
        return f"Dashboard error: {e}"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/lessons')
def lessons():
    if 'user' not in session:
        return redirect('/')
    
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Lessons</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 800px; margin: 0 auto; }
        .lesson { background: white; padding: 20px; margin: 15px 0; border-radius: 10px; }
        .btn { padding: 10px 20px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Python Lessons</h1>
        <div class="lesson">
            <h3>1. Introduction to Python</h3>
            <p>Learn Python basics</p>
            <a href="#" class="btn">Start Lesson</a>
        </div>
        <p><a href="/">← Back to Dashboard</a></p>
    </div>
</body>
</html>
    '''

if __name__ == '__main__':
    print("🚀 Starting FIXED Python Learning Platform...")
    print("📍 Visit: http://localhost:5000")
    print("✅ Dashboard WILL work!")
    app.run(debug=True, host='0.0.0.0', port=5000)
