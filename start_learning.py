#!/usr/bin/env python3
"""
🐍 PYTHON LEARNING - INSTANT START!
This script will get you started immediately, no matter what!
"""

import sys
import subprocess
import webbrowser
import time
import os

def print_banner():
    """Print welcome banner"""
    print("""
🌟 ═══════════════════════════════════════════════════════════════ 🌟
                    🐍 PYTHON LEARNING JOURNEY 🐍
                        INSTANT START SCRIPT
🌟 ═══════════════════════════════════════════════════════════════ 🌟
    """)

def check_python():
    """Check Python installation"""
    print("🔍 Checking Python installation...")
    
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 6:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Perfect!")
            return True
        else:
            print(f"⚠️  Python {version.major}.{version.minor} detected - Please upgrade to Python 3.6+")
            return False
    except Exception as e:
        print(f"❌ Python check failed: {e}")
        return False

def install_flask():
    """Install Flask if needed"""
    print("\n📦 Checking Flask installation...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__} is already installed!")
        return True
    except ImportError:
        print("📥 Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully!")
            return True
        except Exception as e:
            print(f"❌ Failed to install Flask: {e}")
            return False

def start_simple_version():
    """Start the simple learning app"""
    print("\n🚀 Starting your Python Learning Journey...")
    
    try:
        # Import and run the simple app
        print("📱 Launching web application...")
        
        # Start the app in a separate process
        import threading
        
        def run_app():
            try:
                exec(open('simple_app.py').read())
            except Exception as e:
                print(f"❌ App error: {e}")
        
        # Start app in background
        app_thread = threading.Thread(target=run_app, daemon=True)
        app_thread.start()
        
        # Wait a moment for the app to start
        time.sleep(3)
        
        # Open browser
        print("🌐 Opening your browser...")
        webbrowser.open('http://localhost:5000')
        
        print("""
🎉 SUCCESS! Your Python Learning App is running!

📍 URL: http://localhost:5000
🎯 What to do:
   1. Enter your name
   2. Click "Start Learning Python!"
   3. Begin with Lesson 1
   4. Practice in the Playground

💡 Tips:
   • Complete lessons to earn points
   • Try the code playground
   • Practice with the exercises

🔥 Ready to become a Python expert? Let's go! 🔥
        """)
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Thanks for learning Python! Come back anytime!")
            
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        return False

def start_command_line_version():
    """Fallback: Start command line version"""
    print("\n🖥️  Starting Command Line Python Learning...")
    
    lessons = [
        {
            "title": "🐍 Welcome to Python!",
            "content": """
Welcome to Python programming! 🎉

Python is an amazing language that's:
✅ Easy to learn
✅ Powerful and versatile  
✅ Used by top companies
✅ Perfect for beginners

Let's start with your first Python code:

print("Hello, World!")
print("Welcome to Python!")

Try typing this in your Python interpreter!
            """
        },
        {
            "title": "📝 Variables and Data",
            "content": """
Variables store information in Python:

name = "Python Learner"
age = 25
is_learning = True

print("Name:", name)
print("Age:", age)
print("Learning:", is_learning)

Try creating your own variables!
            """
        }
    ]
    
    print("\n📚 Available Lessons:")
    for i, lesson in enumerate(lessons, 1):
        print(f"{i}. {lesson['title']}")
    
    while True:
        try:
            choice = input("\n🎯 Choose a lesson (1-2) or 'q' to quit: ").strip()
            
            if choice.lower() == 'q':
                print("👋 Happy coding!")
                break
            
            lesson_num = int(choice) - 1
            if 0 <= lesson_num < len(lessons):
                lesson = lessons[lesson_num]
                print(f"\n{lesson['title']}")
                print("=" * 50)
                print(lesson['content'])
                
                input("\n📖 Press Enter when you're ready to continue...")
            else:
                print("❌ Invalid choice. Please try again.")
                
        except ValueError:
            print("❌ Please enter a number or 'q'.")
        except KeyboardInterrupt:
            print("\n👋 Thanks for learning!")
            break

def main():
    """Main function"""
    print_banner()
    
    # Check Python
    if not check_python():
        print("\n❌ Please install Python 3.6+ and try again.")
        input("Press Enter to exit...")
        return
    
    # Try to install Flask and start web version
    if install_flask():
        print("\n🎯 Choose your learning experience:")
        print("1. 🌐 Web App (Recommended)")
        print("2. 🖥️  Command Line")
        
        try:
            choice = input("\nEnter your choice (1 or 2): ").strip()
            
            if choice == "1" or choice == "":
                start_simple_version()
            elif choice == "2":
                start_command_line_version()
            else:
                print("Starting web app by default...")
                start_simple_version()
                
        except KeyboardInterrupt:
            print("\n👋 See you later!")
    else:
        print("\n🖥️  No worries! Starting command line version...")
        start_command_line_version()

if __name__ == "__main__":
    main()
