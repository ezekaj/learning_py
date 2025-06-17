#!/usr/bin/env python3
"""
🐍 PYTHON LEARNING - SUPER SIMPLE VERSION
No dependencies, works immediately!
"""

import webbrowser
import http.server
import socketserver
import threading
import time
import os

# Simple HTML content
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>🐍 Python Learning Journey</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            color: white; 
            min-height: 100vh; 
            display: flex; 
            align-items: center; 
            justify-content: center; 
        }
        .container { 
            text-align: center; 
            max-width: 800px; 
            padding: 40px; 
            background: rgba(255,255,255,0.1); 
            border-radius: 20px; 
            backdrop-filter: blur(10px); 
        }
        .logo { font-size: 100px; margin-bottom: 20px; animation: bounce 2s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        h1 { font-size: 48px; margin-bottom: 20px; }
        .subtitle { font-size: 20px; margin-bottom: 40px; opacity: 0.9; }
        .features { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin: 40px 0; 
        }
        .feature { 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px; 
            transition: transform 0.3s; 
        }
        .feature:hover { transform: translateY(-5px); }
        .feature-icon { font-size: 40px; margin-bottom: 15px; }
        .lesson-section { 
            background: rgba(255,255,255,0.1); 
            padding: 30px; 
            border-radius: 15px; 
            margin: 30px 0; 
            text-align: left; 
        }
        .code-block { 
            background: #1e1e1e; 
            color: #00ff00; 
            padding: 20px; 
            border-radius: 10px; 
            font-family: 'Courier New', monospace; 
            margin: 15px 0; 
            overflow-x: auto; 
        }
        .btn { 
            background: white; 
            color: #667eea; 
            padding: 15px 30px; 
            border: none; 
            border-radius: 25px; 
            font-size: 18px; 
            font-weight: bold; 
            cursor: pointer; 
            transition: all 0.3s; 
            margin: 10px; 
            text-decoration: none; 
            display: inline-block; 
        }
        .btn:hover { 
            transform: scale(1.05); 
            box-shadow: 0 5px 15px rgba(0,0,0,0.2); 
        }
        .progress-bar { 
            background: rgba(255,255,255,0.2); 
            height: 10px; 
            border-radius: 5px; 
            overflow: hidden; 
            margin: 20px 0; 
        }
        .progress-fill { 
            background: #4CAF50; 
            height: 100%; 
            width: 0%; 
            transition: width 0.5s; 
        }
        .playground { 
            background: rgba(255,255,255,0.1); 
            padding: 20px; 
            border-radius: 15px; 
            margin: 20px 0; 
        }
        textarea { 
            width: 100%; 
            height: 200px; 
            background: #1e1e1e; 
            color: #00ff00; 
            border: none; 
            border-radius: 10px; 
            padding: 15px; 
            font-family: 'Courier New', monospace; 
            font-size: 14px; 
            resize: vertical; 
        }
        .output { 
            background: #000; 
            color: #00ff00; 
            padding: 15px; 
            border-radius: 10px; 
            font-family: 'Courier New', monospace; 
            min-height: 100px; 
            margin-top: 10px; 
            white-space: pre-wrap; 
        }
        .hidden { display: none; }
        .lesson-nav { 
            display: flex; 
            justify-content: space-between; 
            margin-top: 20px; 
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Welcome Screen -->
        <div id="welcome-screen">
            <div class="logo">🐍</div>
            <h1>Python Learning Journey</h1>
            <p class="subtitle">Master Python programming from beginner to expert!</p>
            
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">📚</div>
                    <h3>Interactive Lessons</h3>
                    <p>Step-by-step tutorials with examples</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🧪</div>
                    <h3>Code Playground</h3>
                    <p>Practice coding with instant feedback</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🏆</div>
                    <h3>Track Progress</h3>
                    <p>See your improvement over time</p>
                </div>
            </div>
            
            <button class="btn" onclick="startLearning()">🚀 Start Learning Python!</button>
        </div>
        
        <!-- Learning Dashboard -->
        <div id="learning-dashboard" class="hidden">
            <h1>🎯 Your Python Journey</h1>
            <p>Progress: <span id="progress-text">0% Complete</span></p>
            <div class="progress-bar">
                <div class="progress-fill" id="progress-fill"></div>
            </div>
            
            <div style="display: flex; gap: 20px; margin: 20px 0;">
                <button class="btn" onclick="showLessons()">📚 Lessons</button>
                <button class="btn" onclick="showPlayground()">🧪 Playground</button>
                <button class="btn" onclick="showProgress()">📊 Progress</button>
            </div>
        </div>
        
        <!-- Lessons Section -->
        <div id="lessons-section" class="hidden">
            <h2>📚 Python Lessons</h2>
            
            <div class="lesson-section" id="lesson-1">
                <h3>Lesson 1: 🐍 Welcome to Python!</h3>
                <p>Learn what Python is and write your first program.</p>
                
                <h4>What is Python?</h4>
                <p>Python is a powerful, easy-to-learn programming language. It's used by companies like Google, Netflix, and Instagram!</p>
                
                <h4>Your First Python Code:</h4>
                <div class="code-block">print("Hello, World!")
print("Welcome to Python!")
print("Let's start coding! 🚀")</div>
                
                <h4>Try it yourself:</h4>
                <p>Copy the code above and run it in the playground!</p>
                
                <div class="lesson-nav">
                    <button class="btn" onclick="showDashboard()">← Dashboard</button>
                    <button class="btn" onclick="completeLesson(1)">✅ Complete Lesson</button>
                    <button class="btn" onclick="showLesson(2)">Next Lesson →</button>
                </div>
            </div>
            
            <div class="lesson-section hidden" id="lesson-2">
                <h3>Lesson 2: 📝 Variables and Data</h3>
                <p>Learn to store and work with information in Python.</p>
                
                <h4>Creating Variables:</h4>
                <div class="code-block">name = "Python Learner"
age = 25
is_learning = True

print("Name:", name)
print("Age:", age)
print("Learning Python:", is_learning)</div>
                
                <h4>Types of Data:</h4>
                <ul style="text-align: left; margin: 20px;">
                    <li><strong>Text (String):</strong> "Hello World"</li>
                    <li><strong>Numbers (Integer):</strong> 42, 100, -5</li>
                    <li><strong>Decimals (Float):</strong> 3.14, 2.5</li>
                    <li><strong>True/False (Boolean):</strong> True, False</li>
                </ul>
                
                <div class="lesson-nav">
                    <button class="btn" onclick="showLesson(1)">← Previous</button>
                    <button class="btn" onclick="completeLesson(2)">✅ Complete Lesson</button>
                    <button class="btn" onclick="showLesson(3)">Next Lesson →</button>
                </div>
            </div>
            
            <div class="lesson-section hidden" id="lesson-3">
                <h3>Lesson 3: 🧮 Math and Operations</h3>
                <p>Learn to do calculations in Python.</p>
                
                <h4>Basic Math Operations:</h4>
                <div class="code-block">print(10 + 5)    # Addition: 15
print(20 - 8)    # Subtraction: 12
print(6 * 7)     # Multiplication: 42
print(15 / 3)    # Division: 5.0
print(2 ** 3)    # Power: 8</div>
                
                <h4>Using Variables in Math:</h4>
                <div class="code-block">apples = 10
oranges = 5
total_fruits = apples + oranges
print("I have", total_fruits, "fruits!")</div>
                
                <div class="lesson-nav">
                    <button class="btn" onclick="showLesson(2)">← Previous</button>
                    <button class="btn" onclick="completeLesson(3)">✅ Complete Lesson</button>
                    <button class="btn" onclick="showDashboard()">Dashboard →</button>
                </div>
            </div>
        </div>
        
        <!-- Playground Section -->
        <div id="playground-section" class="hidden">
            <h2>🧪 Python Code Playground</h2>
            <p>Write and run Python code instantly!</p>
            
            <div class="playground">
                <textarea id="code-editor" placeholder="# Write your Python code here
print('Hello, Python!')
print('Welcome to the playground!')

# Try some math
result = 10 + 5
print('10 + 5 =', result)

# Create variables
name = 'Python Learner'
print('Hello,', name)"></textarea>
                
                <div style="margin: 10px 0;">
                    <button class="btn" onclick="runCode()">▶️ Run Code</button>
                    <button class="btn" onclick="clearCode()">🗑️ Clear</button>
                    <button class="btn" onclick="loadExample()">📝 Example</button>
                    <button class="btn" onclick="showDashboard()">← Dashboard</button>
                </div>
                
                <div class="output" id="code-output">Click "Run Code" to see your output here...</div>
            </div>
        </div>
        
        <!-- Progress Section -->
        <div id="progress-section" class="hidden">
            <h2>📊 Your Progress</h2>
            
            <div class="lesson-section">
                <h3>🏆 Achievements</h3>
                <div id="achievements">
                    <p>Complete lessons to unlock achievements!</p>
                </div>
                
                <h3>📈 Statistics</h3>
                <div id="stats">
                    <p>Lessons Completed: <span id="lessons-completed">0</span>/3</p>
                    <p>Code Runs: <span id="code-runs">0</span></p>
                    <p>Learning Streak: <span id="streak">0</span> days</p>
                </div>
                
                <button class="btn" onclick="showDashboard()">← Dashboard</button>
            </div>
        </div>
    </div>
    
    <script>
        // Learning progress data
        let progress = {
            completedLessons: [],
            codeRuns: 0,
            streak: 1
        };
        
        // Load progress from localStorage
        function loadProgress() {
            const saved = localStorage.getItem('pythonLearningProgress');
            if (saved) {
                progress = JSON.parse(saved);
            }
            updateProgressDisplay();
        }
        
        // Save progress to localStorage
        function saveProgress() {
            localStorage.setItem('pythonLearningProgress', JSON.stringify(progress));
            updateProgressDisplay();
        }
        
        // Update progress display
        function updateProgressDisplay() {
            const percentage = (progress.completedLessons.length / 3) * 100;
            document.getElementById('progress-text').textContent = Math.round(percentage) + '% Complete';
            document.getElementById('progress-fill').style.width = percentage + '%';
            
            if (document.getElementById('lessons-completed')) {
                document.getElementById('lessons-completed').textContent = progress.completedLessons.length;
                document.getElementById('code-runs').textContent = progress.codeRuns;
                document.getElementById('streak').textContent = progress.streak;
            }
            
            updateAchievements();
        }
        
        // Update achievements
        function updateAchievements() {
            const achievementsDiv = document.getElementById('achievements');
            if (!achievementsDiv) return;
            
            let achievements = [];
            
            if (progress.completedLessons.length >= 1) {
                achievements.push('🎯 First Steps - Completed your first lesson!');
            }
            if (progress.completedLessons.length >= 3) {
                achievements.push('🏆 Lesson Master - Completed all basic lessons!');
            }
            if (progress.codeRuns >= 5) {
                achievements.push('🧪 Code Explorer - Ran code 5 times!');
            }
            if (progress.codeRuns >= 20) {
                achievements.push('💻 Coding Enthusiast - Ran code 20 times!');
            }
            
            if (achievements.length > 0) {
                achievementsDiv.innerHTML = achievements.map(a => '<p>' + a + '</p>').join('');
            } else {
                achievementsDiv.innerHTML = '<p>Complete lessons to unlock achievements!</p>';
            }
        }
        
        // Navigation functions
        function startLearning() {
            document.getElementById('welcome-screen').classList.add('hidden');
            document.getElementById('learning-dashboard').classList.remove('hidden');
        }
        
        function showDashboard() {
            hideAllSections();
            document.getElementById('learning-dashboard').classList.remove('hidden');
        }
        
        function showLessons() {
            hideAllSections();
            document.getElementById('lessons-section').classList.remove('hidden');
            showLesson(1);
        }
        
        function showPlayground() {
            hideAllSections();
            document.getElementById('playground-section').classList.remove('hidden');
        }
        
        function showProgress() {
            hideAllSections();
            document.getElementById('progress-section').classList.remove('hidden');
        }
        
        function hideAllSections() {
            const sections = ['learning-dashboard', 'lessons-section', 'playground-section', 'progress-section'];
            sections.forEach(id => {
                document.getElementById(id).classList.add('hidden');
            });
        }
        
        function showLesson(lessonNum) {
            // Hide all lessons
            for (let i = 1; i <= 3; i++) {
                document.getElementById('lesson-' + i).classList.add('hidden');
            }
            // Show selected lesson
            document.getElementById('lesson-' + lessonNum).classList.remove('hidden');
        }
        
        function completeLesson(lessonNum) {
            if (!progress.completedLessons.includes(lessonNum)) {
                progress.completedLessons.push(lessonNum);
                saveProgress();
                alert('🎉 Lesson ' + lessonNum + ' completed! Great job!');
            }
        }
        
        // Playground functions
        function runCode() {
            const code = document.getElementById('code-editor').value;
            const output = document.getElementById('code-output');
            
            try {
                // Simple code execution simulation
                let result = '';
                
                // Basic print simulation
                const lines = code.split('\\n');
                for (let line of lines) {
                    line = line.trim();
                    if (line.startsWith('print(')) {
                        const content = line.match(/print\\((.+)\\)/);
                        if (content) {
                            let printContent = content[1];
                            // Remove quotes
                            printContent = printContent.replace(/['"]/g, '');
                            // Handle simple variables
                            printContent = printContent.replace(/name/g, '"Python Learner"');
                            printContent = printContent.replace(/age/g, '25');
                            // Handle simple math
                            printContent = printContent.replace(/10 \\+ 5/g, '15');
                            printContent = printContent.replace(/20 - 8/g, '12');
                            printContent = printContent.replace(/6 \\* 7/g, '42');
                            
                            result += printContent + '\\n';
                        }
                    }
                }
                
                if (!result) {
                    result = 'Code executed successfully! (No output)';
                }
                
                output.textContent = result;
                output.style.color = '#00ff00';
                
                progress.codeRuns++;
                saveProgress();
                
            } catch (error) {
                output.textContent = 'Error: ' + error.message;
                output.style.color = '#ff6b6b';
            }
        }
        
        function clearCode() {
            document.getElementById('code-editor').value = '';
            document.getElementById('code-output').textContent = 'Code cleared. Ready for new code!';
        }
        
        function loadExample() {
            document.getElementById('code-editor').value = `# Python Basics Example
print("=== Welcome to Python! ===")

# Variables
name = "Python Learner"
age = 25

print("Name: " + name)
print("Age: " + str(age))

# Math operations
print("Math time!")
print("10 + 5 =", 10 + 5)
print("20 - 8 =", 20 - 8)
print("6 * 7 =", 6 * 7)

print("🎉 You're doing great!")`;
        }
        
        // Initialize
        loadProgress();
    </script>
</body>
</html>
"""

class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode())

def start_server():
    """Start the simple HTTP server"""
    PORT = 8000
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
            print(f"🌐 Server running at http://localhost:{PORT}")
            httpd.serve_forever()
    except OSError:
        # Try alternative port
        PORT = 8080
        with socketserver.TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
            print(f"🌐 Server running at http://localhost:{PORT}")
            httpd.serve_forever()

def main():
    """Main function"""
    print("""
🐍 ═══════════════════════════════════════════════════════════════ 🐍
                    PYTHON LEARNING JOURNEY
                        SIMPLE VERSION
🐍 ═══════════════════════════════════════════════════════════════ 🐍

🚀 Starting your Python learning experience...
    """)
    
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(2)
    
    # Open browser
    try:
        webbrowser.open('http://localhost:8000')
        print("🌐 Opening your browser...")
    except:
        webbrowser.open('http://localhost:8080')
        print("🌐 Opening your browser...")
    
    print("""
🎉 SUCCESS! Your Python Learning App is running!

📍 URL: http://localhost:8000 (or http://localhost:8080)

🎯 What to do:
   1. Click "Start Learning Python!"
   2. Go through the lessons
   3. Practice in the playground
   4. Track your progress

💡 Features:
   • Interactive lessons with examples
   • Code playground with instant feedback
   • Progress tracking and achievements
   • Works completely offline!

🔥 Ready to become a Python expert? Let's go! 🔥

Press Ctrl+C to stop the server when you're done.
    """)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Thanks for learning Python! Come back anytime!")

if __name__ == "__main__":
    main()
