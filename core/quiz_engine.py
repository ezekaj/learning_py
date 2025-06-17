"""
Quiz Engine Module
Inspired by interactive tutorial systems and educational platforms:
- Multiple question types (multiple choice, code completion, true/false)
- Immediate feedback system
- Adaptive difficulty
- Progress tracking integration
"""

import json
import os
import random
import re
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import colorama
from colorama import Fore, Style

class QuizEngine:
    """Interactive quiz system with multiple question types"""
    
    def __init__(self, quiz_data_dir: str = "data/quizzes"):
        self.quiz_data_dir = quiz_data_dir
        self.current_quiz = None
        self.current_score = 0
        self.total_questions = 0
        self.ensure_quiz_data()
    
    def ensure_quiz_data(self):
        """Create quiz data directory and sample quizzes"""
        os.makedirs(self.quiz_data_dir, exist_ok=True)
        
        # Create sample quiz files if they don't exist
        sample_quizzes = {
            "python_basics": self.create_python_basics_quiz(),
            "data_types": self.create_data_types_quiz(),
            "control_structures": self.create_control_structures_quiz(),
            "functions": self.create_functions_quiz(),
            "oop_basics": self.create_oop_basics_quiz()
        }
        
        for quiz_name, quiz_data in sample_quizzes.items():
            quiz_file = os.path.join(self.quiz_data_dir, f"{quiz_name}.json")
            if not os.path.exists(quiz_file):
                with open(quiz_file, 'w') as f:
                    json.dump(quiz_data, f, indent=2)
    
    def create_python_basics_quiz(self) -> Dict:
        """Create a basic Python quiz"""
        return {
            "title": "Python Basics",
            "description": "Test your knowledge of Python fundamentals",
            "difficulty": "beginner",
            "time_limit": 300,  # 5 minutes
            "questions": [
                {
                    "id": "pb_001",
                    "type": "multiple_choice",
                    "question": "What is the correct way to create a comment in Python?",
                    "options": [
                        "// This is a comment",
                        "/* This is a comment */",
                        "# This is a comment",
                        "<!-- This is a comment -->"
                    ],
                    "correct_answer": 2,
                    "explanation": "In Python, comments start with the # symbol. Everything after # on that line is ignored by the Python interpreter."
                },
                {
                    "id": "pb_002",
                    "type": "code_completion",
                    "question": "Complete the code to print 'Hello, World!':",
                    "code_template": "print(___)",
                    "correct_answer": "'Hello, World!'",
                    "alternative_answers": ['"Hello, World!"'],
                    "explanation": "The print() function outputs text to the console. Strings can be enclosed in single or double quotes."
                },
                {
                    "id": "pb_003",
                    "type": "true_false",
                    "question": "Python is case-sensitive.",
                    "correct_answer": True,
                    "explanation": "Python is case-sensitive, meaning 'Variable' and 'variable' are treated as different identifiers."
                },
                {
                    "id": "pb_004",
                    "type": "multiple_choice",
                    "question": "Which of the following is NOT a valid Python variable name?",
                    "options": [
                        "my_variable",
                        "_private_var",
                        "2nd_variable",
                        "variable2"
                    ],
                    "correct_answer": 2,
                    "explanation": "Variable names cannot start with a number. '2nd_variable' is invalid because it starts with '2'."
                },
                {
                    "id": "pb_005",
                    "type": "code_output",
                    "question": "What will this code output?",
                    "code": "x = 5\ny = 3\nprint(x + y)",
                    "correct_answer": "8",
                    "explanation": "The code adds 5 + 3 = 8 and prints the result."
                }
            ]
        }
    
    def create_data_types_quiz(self) -> Dict:
        """Create a data types quiz"""
        return {
            "title": "Python Data Types",
            "description": "Test your understanding of Python data types",
            "difficulty": "beginner",
            "time_limit": 400,
            "questions": [
                {
                    "id": "dt_001",
                    "type": "multiple_choice",
                    "question": "What data type is the value 3.14?",
                    "options": ["int", "float", "str", "bool"],
                    "correct_answer": 1,
                    "explanation": "3.14 is a floating-point number, so its data type is float."
                },
                {
                    "id": "dt_002",
                    "type": "code_completion",
                    "question": "Complete the code to create a list with numbers 1, 2, 3:",
                    "code_template": "my_list = ___",
                    "correct_answer": "[1, 2, 3]",
                    "explanation": "Lists in Python are created using square brackets with comma-separated values."
                },
                {
                    "id": "dt_003",
                    "type": "true_false",
                    "question": "Strings in Python are mutable (can be changed after creation).",
                    "correct_answer": False,
                    "explanation": "Strings in Python are immutable. Once created, they cannot be changed. Operations on strings create new string objects."
                }
            ]
        }
    
    def create_control_structures_quiz(self) -> Dict:
        """Create a control structures quiz"""
        return {
            "title": "Control Structures",
            "description": "Test your knowledge of if statements, loops, and control flow",
            "difficulty": "intermediate",
            "time_limit": 600,
            "questions": [
                {
                    "id": "cs_001",
                    "type": "code_output",
                    "question": "What will this code output?",
                    "code": "for i in range(3):\n    print(i)",
                    "correct_answer": "0\n1\n2",
                    "explanation": "range(3) generates numbers 0, 1, 2. The loop prints each number on a new line."
                }
            ]
        }
    
    def create_functions_quiz(self) -> Dict:
        """Create a functions quiz"""
        return {
            "title": "Python Functions",
            "description": "Test your understanding of function definition and usage",
            "difficulty": "intermediate",
            "time_limit": 500,
            "questions": []
        }
    
    def create_oop_basics_quiz(self) -> Dict:
        """Create an OOP basics quiz"""
        return {
            "title": "Object-Oriented Programming Basics",
            "description": "Test your knowledge of classes and objects",
            "difficulty": "advanced",
            "time_limit": 700,
            "questions": []
        }
    
    def get_available_quizzes(self) -> List[Dict]:
        """Get list of available quizzes"""
        quizzes = []
        
        for filename in os.listdir(self.quiz_data_dir):
            if filename.endswith('.json'):
                quiz_path = os.path.join(self.quiz_data_dir, filename)
                try:
                    with open(quiz_path, 'r') as f:
                        quiz_data = json.load(f)
                        quizzes.append({
                            "id": filename[:-5],  # Remove .json extension
                            "title": quiz_data.get("title", "Unknown Quiz"),
                            "description": quiz_data.get("description", ""),
                            "difficulty": quiz_data.get("difficulty", "unknown"),
                            "question_count": len(quiz_data.get("questions", [])),
                            "time_limit": quiz_data.get("time_limit", 0)
                        })
                except Exception as e:
                    print(f"Error loading quiz {filename}: {e}")
        
        return sorted(quizzes, key=lambda x: x["difficulty"])
    
    def start_quiz(self, quiz_id: str, randomize: bool = True) -> bool:
        """Start a quiz session"""
        quiz_path = os.path.join(self.quiz_data_dir, f"{quiz_id}.json")
        
        if not os.path.exists(quiz_path):
            print(f"{Fore.RED}Quiz not found: {quiz_id}{Style.RESET_ALL}")
            return False
        
        try:
            with open(quiz_path, 'r') as f:
                self.current_quiz = json.load(f)
        except Exception as e:
            print(f"{Fore.RED}Error loading quiz: {e}{Style.RESET_ALL}")
            return False
        
        self.current_score = 0
        self.total_questions = len(self.current_quiz["questions"])
        
        if randomize and self.total_questions > 1:
            random.shuffle(self.current_quiz["questions"])
        
        print(f"\n{Fore.GREEN}🎯 {self.current_quiz['title']}{Style.RESET_ALL}")
        print(f"{self.current_quiz['description']}")
        print(f"Difficulty: {self.current_quiz['difficulty'].title()}")
        print(f"Questions: {self.total_questions}")
        
        if self.current_quiz.get("time_limit"):
            minutes = self.current_quiz["time_limit"] // 60
            seconds = self.current_quiz["time_limit"] % 60
            print(f"Time Limit: {minutes}m {seconds}s")
        
        print(f"\n{Fore.YELLOW}Press Enter to start...{Style.RESET_ALL}")
        input()
        
        return True
    
    def run_quiz(self) -> Dict:
        """Run the current quiz and return results"""
        if not self.current_quiz:
            return {"error": "No quiz loaded"}
        
        results = {
            "quiz_title": self.current_quiz["title"],
            "total_questions": self.total_questions,
            "correct_answers": 0,
            "score": 0,
            "percentage": 0,
            "answers": []
        }
        
        for i, question in enumerate(self.current_quiz["questions"], 1):
            print(f"\n{Fore.CYAN}Question {i}/{self.total_questions}{Style.RESET_ALL}")
            print("=" * 50)
            
            is_correct, user_answer = self.ask_question(question)
            
            results["answers"].append({
                "question_id": question["id"],
                "question": question["question"],
                "user_answer": user_answer,
                "correct": is_correct,
                "explanation": question.get("explanation", "")
            })
            
            if is_correct:
                results["correct_answers"] += 1
                self.current_score += 1
                print(f"{Fore.GREEN}✅ Correct!{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Incorrect.{Style.RESET_ALL}")
            
            # Show explanation
            if question.get("explanation"):
                print(f"{Fore.YELLOW}💡 {question['explanation']}{Style.RESET_ALL}")
            
            print()
        
        # Calculate final results
        results["score"] = self.current_score
        results["percentage"] = (self.current_score / self.total_questions) * 100
        
        self.show_quiz_results(results)
        return results
    
    def ask_question(self, question: Dict) -> Tuple[bool, Any]:
        """Ask a single question and return (is_correct, user_answer)"""
        question_type = question["type"]
        
        if question_type == "multiple_choice":
            return self.ask_multiple_choice(question)
        elif question_type == "true_false":
            return self.ask_true_false(question)
        elif question_type == "code_completion":
            return self.ask_code_completion(question)
        elif question_type == "code_output":
            return self.ask_code_output(question)
        else:
            print(f"{Fore.RED}Unknown question type: {question_type}{Style.RESET_ALL}")
            return False, None
    
    def ask_multiple_choice(self, question: Dict) -> Tuple[bool, int]:
        """Ask a multiple choice question"""
        print(f"{question['question']}\n")
        
        for i, option in enumerate(question["options"]):
            print(f"{i + 1}. {option}")
        
        while True:
            try:
                answer = int(input(f"\n{Fore.CYAN}Your answer (1-{len(question['options'])}): {Style.RESET_ALL}"))
                if 1 <= answer <= len(question["options"]):
                    is_correct = (answer - 1) == question["correct_answer"]
                    return is_correct, answer
                else:
                    print(f"{Fore.RED}Please enter a number between 1 and {len(question['options'])}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
    
    def ask_true_false(self, question: Dict) -> Tuple[bool, bool]:
        """Ask a true/false question"""
        print(f"{question['question']}\n")
        
        while True:
            answer = input(f"{Fore.CYAN}True or False (T/F): {Style.RESET_ALL}").strip().upper()
            if answer in ['T', 'TRUE']:
                user_answer = True
                break
            elif answer in ['F', 'FALSE']:
                user_answer = False
                break
            else:
                print(f"{Fore.RED}Please enter T/True or F/False{Style.RESET_ALL}")
        
        is_correct = user_answer == question["correct_answer"]
        return is_correct, user_answer
    
    def ask_code_completion(self, question: Dict) -> Tuple[bool, str]:
        """Ask a code completion question"""
        print(f"{question['question']}\n")
        print(f"Code: {question['code_template']}")
        
        user_answer = input(f"\n{Fore.CYAN}Complete the code (replace ___ with your answer): {Style.RESET_ALL}").strip()
        
        # Check against correct answer and alternatives
        correct_answers = [question["correct_answer"]]
        if "alternative_answers" in question:
            correct_answers.extend(question["alternative_answers"])
        
        is_correct = user_answer in correct_answers
        return is_correct, user_answer
    
    def ask_code_output(self, question: Dict) -> Tuple[bool, str]:
        """Ask what the code output will be"""
        print(f"{question['question']}\n")
        print("Code:")
        print(question["code"])
        
        user_answer = input(f"\n{Fore.CYAN}What will this code output? {Style.RESET_ALL}").strip()
        
        is_correct = user_answer == question["correct_answer"]
        return is_correct, user_answer
    
    def show_quiz_results(self, results: Dict):
        """Display quiz results"""
        print(f"\n{Fore.GREEN}🎉 Quiz Complete!{Style.RESET_ALL}")
        print("=" * 50)
        print(f"Quiz: {results['quiz_title']}")
        print(f"Score: {results['correct_answers']}/{results['total_questions']}")
        print(f"Percentage: {results['percentage']:.1f}%")
        
        # Performance feedback
        percentage = results['percentage']
        if percentage >= 90:
            print(f"{Fore.GREEN}🏆 Excellent! You've mastered this topic!{Style.RESET_ALL}")
        elif percentage >= 80:
            print(f"{Fore.YELLOW}👍 Great job! You have a solid understanding.{Style.RESET_ALL}")
        elif percentage >= 70:
            print(f"{Fore.YELLOW}📚 Good work! Review the topics you missed.{Style.RESET_ALL}")
        elif percentage >= 60:
            print(f"{Fore.RED}📖 Keep studying! You're getting there.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}💪 Don't give up! Review the material and try again.{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        input()
