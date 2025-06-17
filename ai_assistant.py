#!/usr/bin/env python3
"""
🤖 PYTHIA - AI CODING ASSISTANT
Revolutionary AI tutor that makes learning Python absolutely amazing!
"""

import re
import ast
import random
from typing import Dict, List, Any, Optional

class PythiaAI:
    """
    Pythia - Your Personal AI Python Tutor
    
    Features:
    - Smart code analysis and explanation
    - Intelligent hints based on context
    - Error explanation in plain English
    - Code improvement suggestions
    - Natural language to code conversion
    - Adaptive learning assistance
    """
    
    def __init__(self):
        self.personality_responses = [
            "🐍 Let me help you with that!",
            "✨ Great question! Here's what I think:",
            "🎯 I can see what you're trying to do!",
            "🚀 Let's solve this together!",
            "💡 Ah, I have an idea for you!",
            "🌟 You're on the right track!",
            "🔥 This is a perfect learning moment!"
        ]
        
        self.encouragement = [
            "You're doing great! 🌟",
            "Keep going, you've got this! 💪",
            "Every expert was once a beginner! 🚀",
            "Mistakes are just learning opportunities! 💡",
            "You're thinking like a programmer! 🧠",
            "That's exactly how you learn to code! ✨",
            "Progress, not perfection! 🎯"
        ]
        
        self.code_patterns = {
            'print': {
                'explanation': "The print() function displays output to the screen",
                'example': "print('Hello, World!')",
                'tip': "Use print() to see what your variables contain!"
            },
            'variable': {
                'explanation': "Variables store data that you can use later",
                'example': "name = 'Python'\nage = 30",
                'tip': "Choose descriptive variable names like 'user_age' instead of 'x'"
            },
            'if': {
                'explanation': "If statements let you make decisions in your code",
                'example': "if age >= 18:\n    print('You can vote!')",
                'tip': "Don't forget the colon (:) after your if condition!"
            },
            'for': {
                'explanation': "For loops repeat code for each item in a sequence",
                'example': "for i in range(5):\n    print(i)",
                'tip': "Use for loops when you know how many times to repeat"
            },
            'while': {
                'explanation': "While loops repeat code as long as a condition is true",
                'example': "count = 0\nwhile count < 5:\n    print(count)\n    count += 1",
                'tip': "Be careful not to create infinite loops!"
            },
            'function': {
                'explanation': "Functions are reusable blocks of code",
                'example': "def greet(name):\n    return f'Hello, {name}!'",
                'tip': "Functions help you avoid repeating code!"
            }
        }
    
    def analyze_code(self, code: str, user_level: str = "beginner") -> Dict[str, Any]:
        """
        Analyze code and provide intelligent insights
        """
        analysis = {
            'explanation': [],
            'suggestions': [],
            'complexity': 'beginner',
            'concepts_used': [],
            'potential_issues': [],
            'encouragement': random.choice(self.encouragement)
        }
        
        try:
            # Parse the code to understand structure
            tree = ast.parse(code)
            
            # Analyze different code elements
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis['concepts_used'].append('functions')
                    analysis['explanation'].append(f"✨ You defined a function called '{node.name}'!")
                    
                elif isinstance(node, ast.For):
                    analysis['concepts_used'].append('loops')
                    analysis['explanation'].append("🔄 You're using a for loop - great for repetition!")
                    
                elif isinstance(node, ast.While):
                    analysis['concepts_used'].append('loops')
                    analysis['explanation'].append("🔄 You're using a while loop - perfect for conditions!")
                    
                elif isinstance(node, ast.If):
                    analysis['concepts_used'].append('conditionals')
                    analysis['explanation'].append("🎯 You're using conditional logic - smart thinking!")
                    
                elif isinstance(node, ast.Assign):
                    analysis['concepts_used'].append('variables')
                    if hasattr(node.targets[0], 'id'):
                        var_name = node.targets[0].id
                        analysis['explanation'].append(f"📝 You created a variable called '{var_name}'!")
        
        except SyntaxError as e:
            analysis['potential_issues'].append(f"Syntax error: {self.explain_syntax_error(str(e))}")
        
        # Add suggestions based on analysis
        if 'functions' in analysis['concepts_used']:
            analysis['suggestions'].append("💡 Great use of functions! They make code reusable and organized.")
        
        if 'loops' in analysis['concepts_used']:
            analysis['suggestions'].append("🔄 Loops are powerful! You're automating repetitive tasks.")
        
        if len(analysis['concepts_used']) > 2:
            analysis['complexity'] = 'intermediate'
            analysis['suggestions'].append("🚀 You're combining multiple concepts - that's advanced thinking!")
        
        return analysis
    
    def get_intelligent_hint(self, context: str, error_msg: str = "", user_level: str = "beginner") -> str:
        """
        Provide contextual hints based on what the user is trying to do
        """
        hints = []
        
        # Analyze context for keywords
        context_lower = context.lower()
        
        if 'print' in context_lower:
            hints.append("💡 Remember: print() needs parentheses and quotes around text!")
            hints.append("Example: print('Hello, World!')")
        
        if 'variable' in context_lower or '=' in context:
            hints.append("📝 Variables store data: name = 'Python'")
            hints.append("💡 Variable names should be descriptive!")
        
        if 'if' in context_lower:
            hints.append("🎯 If statements need a colon: if condition:")
            hints.append("💡 Don't forget to indent the code inside!")
        
        if 'loop' in context_lower or 'for' in context_lower:
            hints.append("🔄 For loops: for item in sequence:")
            hints.append("💡 Use range() for numbers: for i in range(5):")
        
        if 'function' in context_lower or 'def' in context_lower:
            hints.append("✨ Functions: def function_name():")
            hints.append("💡 Use return to send back a value!")
        
        if error_msg:
            hints.append(f"🔧 Error help: {self.explain_error(error_msg)}")
        
        if not hints:
            hints = [
                "🤔 Try breaking the problem into smaller steps!",
                "💡 What do you want your code to do?",
                "🎯 Start with a simple example and build up!",
                "📚 Check the lesson examples for inspiration!"
            ]
        
        return f"{random.choice(self.personality_responses)}\n\n" + "\n".join(hints[:3])
    
    def explain_error(self, error_msg: str) -> str:
        """
        Explain errors in plain English
        """
        error_explanations = {
            'SyntaxError': "🔧 Syntax Error: Python doesn't understand your code structure",
            'NameError': "📝 Name Error: You're using a variable that doesn't exist",
            'IndentationError': "📐 Indentation Error: Your code isn't properly indented",
            'TypeError': "🔄 Type Error: You're mixing incompatible data types",
            'ValueError': "💥 Value Error: The value you're using isn't valid",
            'IndexError': "📋 Index Error: You're trying to access an item that doesn't exist",
            'KeyError': "🔑 Key Error: The dictionary key you're looking for doesn't exist"
        }
        
        for error_type, explanation in error_explanations.items():
            if error_type in error_msg:
                return explanation
        
        return "🤔 Something went wrong. Let's debug this together!"
    
    def explain_syntax_error(self, error_msg: str) -> str:
        """
        Provide specific help for syntax errors
        """
        if 'invalid syntax' in error_msg:
            return "Check for missing colons (:), parentheses (), or quotes!"
        elif 'unexpected EOF' in error_msg:
            return "You might have unclosed parentheses or quotes!"
        elif 'invalid character' in error_msg:
            return "There might be a special character that doesn't belong!"
        else:
            return "Double-check your Python syntax!"
    
    def suggest_improvements(self, code: str) -> List[str]:
        """
        Suggest code improvements and best practices
        """
        suggestions = []
        
        # Check for common improvements
        if 'print(' in code and code.count('print(') > 3:
            suggestions.append("💡 Consider using a loop instead of multiple print statements!")
        
        # Check variable naming
        if re.search(r'\b[a-z]\b\s*=', code):
            suggestions.append("📝 Use descriptive variable names instead of single letters!")
        
        # Check for magic numbers
        if re.search(r'\b\d{2,}\b', code):
            suggestions.append("🔢 Consider using named constants for large numbers!")
        
        # Check for long lines
        lines = code.split('\n')
        long_lines = [i+1 for i, line in enumerate(lines) if len(line) > 80]
        if long_lines:
            suggestions.append(f"📏 Consider breaking long lines (lines {long_lines})!")
        
        # Check for comments
        if '#' not in code and len(code.split('\n')) > 5:
            suggestions.append("💬 Add comments to explain what your code does!")
        
        if not suggestions:
            suggestions.append("✨ Your code looks great! Keep up the good work!")
        
        return suggestions
    
    def natural_language_to_code(self, description: str) -> str:
        """
        Convert natural language descriptions to Python code
        """
        description_lower = description.lower()
        
        # Simple pattern matching for common requests
        if 'print' in description_lower and 'hello' in description_lower:
            return "print('Hello, World!')"
        
        elif 'variable' in description_lower and 'name' in description_lower:
            return "name = 'Your Name Here'"
        
        elif 'loop' in description_lower and 'number' in description_lower:
            return "for i in range(10):\n    print(i)"
        
        elif 'function' in description_lower:
            return "def my_function():\n    # Your code here\n    return result"
        
        elif 'if' in description_lower or 'condition' in description_lower:
            return "if condition:\n    # Do something\nelse:\n    # Do something else"
        
        elif 'list' in description_lower:
            return "my_list = [1, 2, 3, 4, 5]"
        
        else:
            return f"# {description}\n# Let me help you break this down into steps!"
    
    def get_learning_path_suggestion(self, current_concepts: List[str], user_level: str) -> str:
        """
        Suggest next learning steps based on current progress
        """
        learning_paths = {
            'beginner': [
                'variables', 'print_statements', 'basic_math', 'strings', 
                'conditionals', 'loops', 'lists', 'functions'
            ],
            'intermediate': [
                'dictionaries', 'file_handling', 'error_handling', 'classes',
                'modules', 'list_comprehensions', 'decorators'
            ],
            'advanced': [
                'generators', 'context_managers', 'metaclasses', 'async_programming',
                'testing', 'packaging', 'performance_optimization'
            ]
        }
        
        path = learning_paths.get(user_level, learning_paths['beginner'])
        
        # Find next concept to learn
        for concept in path:
            if concept not in current_concepts:
                return f"🎯 Ready for the next step? Let's learn about {concept.replace('_', ' ')}!"
        
        return "🚀 You've mastered this level! Time to move to the next difficulty!"
    
    def get_motivational_message(self, progress_data: Dict) -> str:
        """
        Generate personalized motivational messages
        """
        messages = [
            f"🌟 You've completed {progress_data.get('lessons_completed', 0)} lessons! Amazing progress!",
            f"🔥 Your coding streak is {progress_data.get('streak', 0)} days! Keep it up!",
            f"🏆 You've earned {progress_data.get('points', 0)} points! You're becoming a Python expert!",
            f"🚀 Level {progress_data.get('level', 1)} achieved! Your skills are growing!",
            "💡 Every line of code you write makes you a better programmer!",
            "🎯 Remember: The best way to learn programming is by doing!",
            "✨ You're not just learning Python, you're learning to think like a programmer!"
        ]
        
        return random.choice(messages)

# Global AI assistant instance
pythia = PythiaAI()

def get_ai_help(code: str = "", context: str = "", error_msg: str = "", user_level: str = "beginner") -> Dict[str, Any]:
    """
    Main function to get AI assistance
    """
    if code:
        analysis = pythia.analyze_code(code, user_level)
        analysis['suggestions'].extend(pythia.suggest_improvements(code))
        return analysis
    
    elif context or error_msg:
        hint = pythia.get_intelligent_hint(context, error_msg, user_level)
        return {'hint': hint, 'type': 'contextual_help'}
    
    else:
        return {'message': 'Hi! I\'m Pythia, your AI coding assistant! How can I help you today? 🤖✨'}

if __name__ == "__main__":
    # Test the AI assistant
    print("🤖 Testing Pythia AI Assistant...")
    
    # Test code analysis
    test_code = """
name = "Python"
age = 30
if age >= 18:
    print(f"Hello {name}, you can vote!")
"""
    
    result = get_ai_help(code=test_code)
    print("\n📊 Code Analysis:")
    for explanation in result['explanation']:
        print(f"  {explanation}")
    
    # Test hint system
    hint_result = get_ai_help(context="I want to create a loop", user_level="beginner")
    print(f"\n💡 Hint: {hint_result['hint']}")
    
    print("\n✨ Pythia AI Assistant is ready!")
