#!/usr/bin/env python3
"""
🧪 Simple Test App
Test basic Flask functionality
"""

from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'test_secret_key'

@app.route('/')
def home():
    return '''
    <h1>🧪 Test App</h1>
    <p>App is running!</p>
    <a href="/register">Test Registration</a>
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        print(f"Registration data: {data}")
        
        # Simple validation
        if not data or not data.get('email'):
            return jsonify({"success": False, "error": "Email required"}), 400
        
        # Save to simple file
        try:
            os.makedirs("data", exist_ok=True)
            with open("data/test_users.json", 'w') as f:
                json.dump({"test": "data"}, f)
            print("Data saved successfully")
        except Exception as e:
            print(f"Error saving: {e}")
            return jsonify({"success": False, "error": str(e)}), 500
        
        return jsonify({"success": True, "message": "Registration successful!"})
    
    return '''
    <h2>Test Registration</h2>
    <form id="testForm">
        <input type="email" id="email" placeholder="Email" required><br><br>
        <button type="submit">Register</button>
    </form>
    
    <script>
    document.getElementById('testForm').addEventListener('submit', async function(e) {
        e.preventDefault();
        const email = document.getElementById('email').value;
        
        try {
            const response = await fetch('/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email: email})
            });
            
            const result = await response.json();
            alert(JSON.stringify(result));
        } catch (error) {
            alert('Error: ' + error);
        }
    });
    </script>
    '''

if __name__ == '__main__':
    print("🚀 Starting simple test app...")
    app.run(debug=True, host='0.0.0.0', port=5001)
