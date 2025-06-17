#!/usr/bin/env python3
"""
🚀 QUICK START - REVOLUTIONARY PYTHON LEARNING PLATFORM
One-click setup and launch for the world's most advanced Python learning platform
"""

import subprocess
import sys
import os
import webbrowser
import time

def print_header():
    print("""
🚀 REVOLUTIONARY PYTHON LEARNING PLATFORM
==========================================
🤖 AI-Powered Tutoring | 🌐 Real-time Collaboration | 📱 Mobile PWA
🎮 Advanced Gamification | 🧠 Adaptive Learning

Quick Start Launcher
""")

def install_flask():
    """Install Flask if not available"""
    print("📦 Installing Flask...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "flask-socketio"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Flask installed successfully!")
        return True
    except:
        print("❌ Flask installation failed")
        return False

def check_flask():
    """Check if Flask is available"""
    try:
        import flask
        print("✅ Flask is available")
        return True
    except ImportError:
        print("⚠️  Flask not found, installing...")
        return install_flask()

def create_simple_app():
    """Create a simplified version of the app if the full version fails"""
    simple_app_code = '''
from flask import Flask, render_template_string
import webbrowser
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>🚀 Revolutionary Python Learning Platform</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .container { text-align: center; max-width: 800px; }
        .title { font-size: 3em; margin-bottom: 20px; }
        .subtitle { font-size: 1.2em; margin-bottom: 30px; opacity: 0.9; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 40px 0; }
        .feature { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; backdrop-filter: blur(10px); }
        .feature h3 { margin: 0 0 10px 0; font-size: 1.5em; }
        .status { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 30px; }
        .success { color: #4ade80; }
        .warning { color: #fbbf24; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">🚀 Revolutionary Python Learning Platform</h1>
        <p class="subtitle">The world's most advanced Python learning experience</p>
        
        <div class="features">
            <div class="feature">
                <h3>🤖 AI Tutoring</h3>
                <p>Pythia AI Assistant provides intelligent coding help</p>
            </div>
            <div class="feature">
                <h3>🌐 Collaboration</h3>
                <p>Real-time coding with other learners</p>
            </div>
            <div class="feature">
                <h3>📱 Mobile PWA</h3>
                <p>Learn anywhere with our mobile app</p>
            </div>
            <div class="feature">
                <h3>🎮 Gamification</h3>
                <p>Unlock achievements and level up</p>
            </div>
        </div>
        
        <div class="status">
            <h3 class="success">✅ Platform Successfully Launched!</h3>
            <p>Your revolutionary Python learning platform is now running.</p>
            <p class="warning">⚠️ Running in simplified mode. Install full dependencies for complete features.</p>
            <p><strong>Next Steps:</strong></p>
            <p>1. Install dependencies: <code>pip install flask flask-socketio</code></p>
            <p>2. Run full app: <code>python app.py</code></p>
        </div>
    </div>
</body>
</html>
    """)

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print("🚀 Starting Revolutionary Python Learning Platform...")
    print("📱 Opening browser at http://localhost:5000")
    print("🛑 Press Ctrl+C to stop")
    
    # Open browser in background
    threading.Thread(target=open_browser, daemon=True).start()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open('simple_app.py', 'w') as f:
        f.write(simple_app_code)
    
    print("✅ Created simplified app")

def main():
    print_header()
    
    # Check and install Flask
    if not check_flask():
        print("❌ Cannot proceed without Flask")
        return
    
    # Try to run the full app
    print("🚀 Attempting to launch full platform...")
    
    try:
        # Try importing our app
        import app
        print("✅ Full app loaded successfully!")
        print("🌐 Opening browser...")
        
        # Open browser
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        threading.Thread(target=open_browser, daemon=True).start()
        
        # This would run the app, but we can't do it directly here
        print("📍 To start the full app, run: python app.py")
        
    except Exception as e:
        print(f"⚠️  Full app not available: {e}")
        print("🔧 Creating simplified version...")
        
        create_simple_app()
        
        print("🚀 Launching simplified platform...")
        try:
            subprocess.run([sys.executable, "simple_app.py"])
        except KeyboardInterrupt:
            print("\\n👋 Platform stopped")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\n👋 Quick start interrupted")
    except Exception as e:
        print(f"\\n❌ Error: {e}")
        print("💡 Try running: python app.py")
    
    input("\\nPress Enter to exit...")
