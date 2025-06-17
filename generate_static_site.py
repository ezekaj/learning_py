#!/usr/bin/env python3
"""
Static Site Generator for Python Learning Platform
Generates static HTML pages for GitHub Pages deployment
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path

def create_docs_directory():
    """Create and clean the docs directory"""
    docs_dir = Path("docs")
    if docs_dir.exists():
        shutil.rmtree(docs_dir)
    docs_dir.mkdir()
    return docs_dir

def copy_static_assets(docs_dir):
    """Copy static assets to docs directory"""
    static_dir = Path("static")
    if static_dir.exists():
        shutil.copytree(static_dir, docs_dir / "static")

def generate_index_page(docs_dir):
    """Generate the main index.html page"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐍 Python Learning Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .feature-card { transition: all 0.3s ease; }
        .feature-card:hover { transform: translateY(-4px) scale(1.02); }
    </style>
</head>
<body class="bg-gray-50">
    <!-- Hero Section -->
    <div class="gradient-bg text-white">
        <div class="container mx-auto px-6 py-20 text-center">
            <h1 class="text-6xl font-bold mb-6">
                🐍 Python Learning Platform
            </h1>
            <p class="text-2xl mb-8 opacity-90">
                Comprehensive Python learning platform with interactive lessons, challenges, and gamification
            </p>
            <div class="flex justify-center space-x-4">
                <a href="https://github.com/ezekaj/learning_py" class="bg-white text-purple-600 px-8 py-4 rounded-full font-bold text-lg hover:bg-gray-100 transition-colors">
                    <i class="fab fa-github mr-2"></i>View on GitHub
                </a>
                <a href="#features" class="bg-transparent border-2 border-white px-8 py-4 rounded-full font-bold text-lg hover:bg-white hover:text-purple-600 transition-colors">
                    <i class="fas fa-rocket mr-2"></i>Explore Features
                </a>
            </div>
        </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="container mx-auto px-6 py-16">
        <h2 class="text-4xl font-bold text-center mb-12 text-gray-800">
            🌟 Platform Features
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <!-- Comprehensive Curriculum -->
            <div class="feature-card bg-white rounded-xl shadow-lg p-8 text-center">
                <div class="text-5xl mb-4">📚</div>
                <h3 class="text-xl font-bold mb-4 text-gray-800">50+ Lessons</h3>
                <p class="text-gray-600 mb-4">
                    From beginner to expert level with structured learning paths
                </p>
                <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
                    Comprehensive
                </div>
            </div>

            <!-- Interactive Challenges -->
            <div class="feature-card bg-white rounded-xl shadow-lg p-8 text-center">
                <div class="text-5xl mb-4">🎮</div>
                <h3 class="text-xl font-bold mb-4 text-gray-800">Coding Challenges</h3>
                <p class="text-gray-600 mb-4">
                    Practice with real coding problems and automated testing
                </p>
                <div class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm font-medium">
                    Interactive
                </div>
            </div>

            <!-- Code Playground -->
            <div class="feature-card bg-white rounded-xl shadow-lg p-8 text-center">
                <div class="text-5xl mb-4">🧪</div>
                <h3 class="text-xl font-bold mb-4 text-gray-800">Code Playground</h3>
                <p class="text-gray-600 mb-4">
                    Safe environment to experiment and test Python code
                </p>
                <div class="bg-purple-100 text-purple-800 px-3 py-1 rounded-full text-sm font-medium">
                    Hands-on
                </div>
            </div>

            <!-- Progress Tracking -->
            <div class="feature-card bg-white rounded-xl shadow-lg p-8 text-center">
                <div class="text-5xl mb-4">📊</div>
                <h3 class="text-xl font-bold mb-4 text-gray-800">Progress Tracking</h3>
                <p class="text-gray-600 mb-4">
                    Monitor your learning journey with detailed analytics
                </p>
                <div class="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm font-medium">
                    Analytics
                </div>
            </div>

            <!-- Gamification -->
            <div class="feature-card bg-white rounded-xl shadow-lg p-8 text-center">
                <div class="text-5xl mb-4">🏆</div>
                <h3 class="text-xl font-bold mb-4 text-gray-800">Achievements</h3>
                <p class="text-gray-600 mb-4">
                    Earn points, levels, and badges for your accomplishments
                </p>
                <div class="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm font-medium">
                    Motivating
                </div>
            </div>

            <!-- AI Assistant -->
            <div class="feature-card bg-white rounded-xl shadow-lg p-8 text-center">
                <div class="text-5xl mb-4">🤖</div>
                <h3 class="text-xl font-bold mb-4 text-gray-800">AI Assistant</h3>
                <p class="text-gray-600 mb-4">
                    Get help and guidance from an intelligent tutoring system
                </p>
                <div class="bg-indigo-100 text-indigo-800 px-3 py-1 rounded-full text-sm font-medium">
                    Smart
                </div>
            </div>
        </div>
    </div>

    <!-- Getting Started -->
    <div class="bg-gray-100 py-16">
        <div class="container mx-auto px-6 text-center">
            <h2 class="text-4xl font-bold mb-8 text-gray-800">
                🚀 Getting Started
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
                <div class="bg-white p-6 rounded-xl shadow-lg">
                    <div class="text-3xl mb-4">1️⃣</div>
                    <h3 class="text-xl font-bold mb-2">Clone Repository</h3>
                    <p class="text-gray-600">Download the project from GitHub</p>
                    <code class="bg-gray-100 p-2 rounded text-sm block mt-2">git clone https://github.com/ezekaj/learning_py.git</code>
                </div>
                <div class="bg-white p-6 rounded-xl shadow-lg">
                    <div class="text-3xl mb-4">2️⃣</div>
                    <h3 class="text-xl font-bold mb-2">Install Dependencies</h3>
                    <p class="text-gray-600">Set up the Python environment</p>
                    <code class="bg-gray-100 p-2 rounded text-sm block mt-2">pip install -r requirements.txt</code>
                </div>
                <div class="bg-white p-6 rounded-xl shadow-lg">
                    <div class="text-3xl mb-4">3️⃣</div>
                    <h3 class="text-xl font-bold mb-2">Start Learning</h3>
                    <p class="text-gray-600">Run the application and begin</p>
                    <code class="bg-gray-100 p-2 rounded text-sm block mt-2">python app.py</code>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="gradient-bg text-white py-8">
        <div class="container mx-auto px-6 text-center">
            <p class="mb-4">
                Built with ❤️ for Python learners everywhere
            </p>
            <div class="flex justify-center space-x-6">
                <a href="https://github.com/ezekaj/learning_py" class="hover:text-gray-300">
                    <i class="fab fa-github text-2xl"></i>
                </a>
                <a href="documentation.html" class="hover:text-gray-300">
                    <i class="fas fa-book text-2xl"></i>
                </a>
            </div>
            <p class="mt-4 text-sm opacity-75">
                © 2025 Python Learning Platform. Open source project.
            </p>
        </div>
    </footer>
</body>
</html>"""
    
    with open(docs_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def generate_documentation_page(docs_dir):
    """Generate documentation page"""
    # Read the README content
    readme_path = Path("README.md")
    readme_content = ""
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
    
    # Escape backticks in readme content
    escaped_readme = readme_content.replace('`', '\\`')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation - Python Learning Platform</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/default.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/marked/5.1.1/marked.min.js"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow-lg">
        <div class="container mx-auto px-6 py-4">
            <div class="flex justify-between items-center">
                <a href="index.html" class="text-xl font-bold text-gray-800">🐍 Python Learning Platform</a>
                <a href="https://github.com/ezekaj/learning_py" class="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
                    View on GitHub
                </a>
            </div>
        </div>
    </nav>

    <div class="container mx-auto px-6 py-8">
        <div class="bg-white rounded-xl shadow-lg p-8">
            <div id="readme-content" class="prose max-w-none">
                <!-- README content will be inserted here -->
            </div>
        </div>
    </div>

    <script>
        // Convert markdown to HTML
        const readmeContent = `{escaped_readme}`;
        document.getElementById('readme-content').innerHTML = marked.parse(readmeContent);

        // Highlight code blocks
        hljs.highlightAll();
    </script>
</body>
</html>"""
    
    with open(docs_dir / "documentation.html", "w", encoding="utf-8") as f:
        f.write(html_content)

def main():
    """Main function to generate the static site"""
    print("🚀 Generating static site for GitHub Pages...")
    
    # Create docs directory
    docs_dir = create_docs_directory()
    print(f"✅ Created docs directory: {docs_dir}")
    
    # Copy static assets
    copy_static_assets(docs_dir)
    print("✅ Copied static assets")
    
    # Generate pages
    generate_index_page(docs_dir)
    print("✅ Generated index.html")
    
    generate_documentation_page(docs_dir)
    print("✅ Generated documentation.html")
    
    print(f"🎉 Static site generated successfully in {docs_dir}")
    print("📁 Files created:")
    for file in docs_dir.rglob("*"):
        if file.is_file():
            print(f"   - {file.relative_to(docs_dir)}")

if __name__ == "__main__":
    main()
