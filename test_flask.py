#!/usr/bin/env python3
"""
🧪 TEST FLASK APP
Simple test to see if Flask works
"""

print("🚀 Starting Flask test...")

try:
    from flask import Flask
    print("✅ Flask imported successfully")
    
    app = Flask(__name__)
    print("✅ Flask app created")
    
    @app.route('/')
    def home():
        return '''
        <html>
        <head><title>🧪 Flask Test</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🎉 Flask is Working!</h1>
            <p>Your Python Learning Platform is ready!</p>
            <h2>🚀 Dashboard Test</h2>
            <div style="background: #f0f0f0; padding: 20px; border-radius: 10px; margin: 20px;">
                <h3>📊 Your Stats</h3>
                <p>✅ Lessons: 5 completed</p>
                <p>⭐ Points: 150</p>
                <p>🏆 Level: 3</p>
            </div>
            <div style="margin: 20px;">
                <a href="/dashboard" style="background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 10px;">📚 Dashboard</a>
                <a href="/lessons" style="background: #4facfe; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 10px;">📖 Lessons</a>
            </div>
        </body>
        </html>
        '''
    
    @app.route('/dashboard')
    def dashboard():
        return '''
        <html>
        <head><title>Dashboard - Python Learning</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>🎉 Dashboard Working!</h1>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin: 20px 0;">
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">5</div>
                    <div>📚 Lessons</div>
                </div>
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">150</div>
                    <div>⭐ Points</div>
                </div>
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">3</div>
                    <div>🏆 Level</div>
                </div>
                <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center;">
                    <div style="font-size: 2em; font-weight: bold; color: #667eea;">7</div>
                    <div>🔥 Streak</div>
                </div>
            </div>
            <p><a href="/" style="color: #667eea;">← Back to Home</a></p>
        </body>
        </html>
        '''
    
    @app.route('/lessons')
    def lessons():
        return '''
        <html>
        <head><title>Lessons - Python Learning</title></head>
        <body style="font-family: Arial; padding: 20px;">
            <h1>📚 Python Lessons</h1>
            <div style="background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3>1. Introduction to Python 🐍</h3>
                <p>Learn the basics of Python programming</p>
                <a href="#" style="background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Start Lesson</a>
            </div>
            <div style="background: white; padding: 20px; margin: 15px 0; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <h3>2. Variables and Data Types 📊</h3>
                <p>Master Python variables and data types</p>
                <a href="#" style="background: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Start Lesson</a>
            </div>
            <p><a href="/dashboard" style="color: #667eea;">← Back to Dashboard</a></p>
        </body>
        </html>
        '''
    
    print("✅ Routes defined")
    print("🌐 Starting server on http://localhost:5000")
    print("📍 Visit the URL to see your Python Learning Platform!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except ImportError as e:
    print(f"❌ Flask not installed: {e}")
    print("💡 Install Flask with: pip install flask")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 Trying alternative approach...")
    
    # Simple HTTP server fallback
    import http.server
    import socketserver
    
    class MyHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = '''
            <html>
            <head><title>🐍 Python Learning Platform</title></head>
            <body style="font-family: Arial; text-align: center; padding: 50px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                <h1>🎉 Python Learning Platform is Working!</h1>
                <p>Dashboard and lessons are ready!</p>
                <div style="background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; margin: 20px;">
                    <h2>📊 Your Progress</h2>
                    <p>✅ Lessons: 5 completed</p>
                    <p>⭐ Points: 150 earned</p>
                    <p>🏆 Level: 3 achieved</p>
                    <p>🔥 Streak: 7 days</p>
                </div>
                <p>🚀 Your Python learning journey is ready to begin!</p>
            </body>
            </html>
            '''
            
            self.wfile.write(html.encode())
    
    print("🌐 Starting simple HTTP server on http://localhost:8000")
    with socketserver.TCPServer(("", 8000), MyHandler) as httpd:
        httpd.serve_forever()
