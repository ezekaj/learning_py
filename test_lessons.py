#!/usr/bin/env python3
"""
🧪 TEST LESSONS FUNCTIONALITY
Quick test to verify lessons are working
"""

from flask import Flask, render_template_string

app = Flask(__name__)

# Sample lessons data
SAMPLE_LESSONS = [
    {
        "id": "lesson_1",
        "title": "Introduction to Python",
        "description": "What is Python, installation, and first program",
        "difficulty": "beginner",
        "estimated_time": 60,
        "exercises": 5,
        "points": 10,
        "objectives": [
            "Understand what Python is",
            "Install Python and set up development environment",
            "Write your first Python program",
            "Understand Python syntax basics"
        ]
    },
    {
        "id": "lesson_2", 
        "title": "Variables and Data Types",
        "description": "Learn about Python variables and basic data types",
        "difficulty": "beginner",
        "estimated_time": 75,
        "exercises": 8,
        "points": 10,
        "objectives": [
            "Understand variables and naming conventions",
            "Learn about basic data types",
            "Practice variable assignment",
            "Use built-in functions"
        ]
    },
    {
        "id": "lesson_3",
        "title": "Operators and Expressions", 
        "description": "Master Python operators and expressions",
        "difficulty": "beginner",
        "estimated_time": 70,
        "exercises": 10,
        "points": 10,
        "objectives": [
            "Learn arithmetic operators",
            "Understand comparison operators", 
            "Use logical operators",
            "Practice operator precedence"
        ]
    },
    {
        "id": "lesson_4",
        "title": "Strings and String Methods",
        "description": "Work with strings and string manipulation",
        "difficulty": "beginner", 
        "estimated_time": 80,
        "exercises": 12,
        "points": 10,
        "objectives": [
            "Create and manipulate strings",
            "Use string methods",
            "Format strings",
            "Handle string indexing and slicing"
        ]
    },
    {
        "id": "lesson_5",
        "title": "Lists and List Methods",
        "description": "Master Python lists and list operations",
        "difficulty": "beginner",
        "estimated_time": 90,
        "exercises": 15,
        "points": 15,
        "objectives": [
            "Create and modify lists",
            "Use list methods", 
            "Understand list indexing",
            "Practice list comprehensions"
        ]
    }
]

@app.route('/')
def home():
    return '''
    <h1>🧪 Lessons Test</h1>
    <p><a href="/test_lessons">Test Lessons Page</a></p>
    '''

@app.route('/test_lessons')
def test_lessons():
    """Test lessons page with simple template"""
    
    template = '''
<!DOCTYPE html>
<html>
<head>
    <title>🧪 Test Lessons</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
        .lesson { background: white; margin: 10px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .lesson h3 { color: #333; margin: 0 0 10px 0; }
        .lesson p { color: #666; margin: 5px 0; }
        .objectives { margin: 10px 0; }
        .objectives li { margin: 5px 0; }
        .meta { font-size: 0.9em; color: #888; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📚 Python Lessons Test</h1>
        <p>Testing if lessons data is working correctly</p>
    </div>
    
    <div class="stats">
        <p><strong>Total Lessons:</strong> {{ lessons|length }}</p>
        <p><strong>Status:</strong> {% if lessons %}✅ Lessons loaded successfully!{% else %}❌ No lessons found{% endif %}</p>
    </div>
    
    {% for lesson in lessons %}
    <div class="lesson">
        <h3>{{ loop.index }}. {{ lesson.get('title', 'No Title') }}</h3>
        <p><strong>Description:</strong> {{ lesson.get('description', 'No description') }}</p>
        
        <div class="meta">
            <span>🎯 Difficulty: {{ lesson.get('difficulty', 'Unknown') }}</span> |
            <span>⏱️ Time: {{ lesson.get('estimated_time', 0) }} min</span> |
            <span>📝 Exercises: {{ lesson.get('exercises', 0) }}</span> |
            <span>⭐ Points: {{ lesson.get('points', 0) }}</span>
        </div>
        
        {% if lesson.get('objectives') %}
        <div class="objectives">
            <strong>Learning Objectives:</strong>
            <ul>
                {% for objective in lesson.get('objectives', []) %}
                <li>{{ objective }}</li>
                {% endfor %}
            </ul>
        </div>
        {% endif %}
    </div>
    {% endfor %}
    
    {% if not lessons %}
    <div class="lesson" style="background: #ffebee; border-left: 4px solid #f44336;">
        <h3>❌ No Lessons Found</h3>
        <p>The lessons data is not being passed to the template correctly.</p>
    </div>
    {% endif %}
    
    <div style="margin-top: 30px; padding: 20px; background: #e8f5e8; border-radius: 8px;">
        <h3>🔧 Debug Info</h3>
        <p><strong>Lessons type:</strong> {{ lessons.__class__.__name__ }}</p>
        <p><strong>Lessons length:</strong> {{ lessons|length }}</p>
        <p><strong>First lesson keys:</strong> {{ lessons[0].keys() if lessons else 'None' }}</p>
    </div>
</body>
</html>
    '''
    
    return render_template_string(template, lessons=SAMPLE_LESSONS)

if __name__ == '__main__':
    print("🧪 Starting Lessons Test Server...")
    print("📍 Visit: http://localhost:5001/test_lessons")
    app.run(debug=True, port=5001)
