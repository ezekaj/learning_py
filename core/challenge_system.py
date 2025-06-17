"""
Challenge System Module
Inspired by coding challenge platforms like HackerRank, LeetCode, and Codewars:
- Progressive difficulty levels
- Automated testing
- Multiple solution approaches
- Performance tracking
- Hint system
"""

import json
import os
import time
import ast
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import colorama
from colorama import Fore, Style

class ChallengeSystem:
    """Interactive coding challenge system"""
    
    def __init__(self, challenges_dir: str = "data/challenges"):
        self.challenges_dir = challenges_dir
        self.current_challenge = None
        self.ensure_challenge_structure()
        self.create_sample_challenges()
    
    def ensure_challenge_structure(self):
        """Create challenge directory structure"""
        difficulties = ["easy", "medium", "hard", "expert"]
        categories = ["basics", "algorithms", "data_structures", "math", "strings", "lists"]
        
        for difficulty in difficulties:
            for category in categories:
                challenge_dir = os.path.join(self.challenges_dir, difficulty, category)
                os.makedirs(challenge_dir, exist_ok=True)
    
    def create_sample_challenges(self):
        """Create sample challenges"""
        # Easy challenges
        easy_challenges = [
            {
                "id": "easy_001",
                "title": "Hello World",
                "category": "basics",
                "difficulty": "easy",
                "description": "Write a function that returns 'Hello, World!'",
                "function_name": "hello_world",
                "parameters": [],
                "return_type": "str",
                "examples": [
                    {"input": [], "output": "Hello, World!"}
                ],
                "test_cases": [
                    {"input": [], "expected": "Hello, World!", "hidden": False}
                ],
                "hints": [
                    "Return the string 'Hello, World!' exactly as shown",
                    "Make sure to include the comma and exclamation mark"
                ],
                "time_limit": 1,
                "memory_limit": 128,
                "points": 10
            },
            {
                "id": "easy_002",
                "title": "Sum Two Numbers",
                "category": "math",
                "difficulty": "easy",
                "description": "Write a function that takes two numbers and returns their sum",
                "function_name": "sum_two_numbers",
                "parameters": ["a: int", "b: int"],
                "return_type": "int",
                "examples": [
                    {"input": [3, 5], "output": 8},
                    {"input": [-1, 1], "output": 0}
                ],
                "test_cases": [
                    {"input": [3, 5], "expected": 8, "hidden": False},
                    {"input": [-1, 1], "expected": 0, "hidden": False},
                    {"input": [0, 0], "expected": 0, "hidden": True},
                    {"input": [100, 200], "expected": 300, "hidden": True}
                ],
                "hints": [
                    "Use the + operator to add two numbers",
                    "The function should return the result, not print it"
                ],
                "time_limit": 1,
                "memory_limit": 128,
                "points": 15
            },
            {
                "id": "easy_003",
                "title": "Find Maximum",
                "category": "basics",
                "difficulty": "easy",
                "description": "Write a function that finds the maximum number in a list",
                "function_name": "find_maximum",
                "parameters": ["numbers: List[int]"],
                "return_type": "int",
                "examples": [
                    {"input": [[1, 3, 2]], "output": 3},
                    {"input": [[-1, -5, -2]], "output": -1}
                ],
                "test_cases": [
                    {"input": [[1, 3, 2]], "expected": 3, "hidden": False},
                    {"input": [[-1, -5, -2]], "expected": -1, "hidden": False},
                    {"input": [[5]], "expected": 5, "hidden": True},
                    {"input": [[10, 20, 30, 40, 50]], "expected": 50, "hidden": True}
                ],
                "hints": [
                    "You can use the built-in max() function",
                    "Or iterate through the list to find the maximum manually"
                ],
                "time_limit": 2,
                "memory_limit": 128,
                "points": 20
            }
        ]
        
        # Medium challenges
        medium_challenges = [
            {
                "id": "medium_001",
                "title": "Palindrome Check",
                "category": "strings",
                "difficulty": "medium",
                "description": "Write a function that checks if a string is a palindrome (reads the same forwards and backwards)",
                "function_name": "is_palindrome",
                "parameters": ["s: str"],
                "return_type": "bool",
                "examples": [
                    {"input": ["racecar"], "output": True},
                    {"input": ["hello"], "output": False}
                ],
                "test_cases": [
                    {"input": ["racecar"], "expected": True, "hidden": False},
                    {"input": ["hello"], "expected": False, "hidden": False},
                    {"input": [""], "expected": True, "hidden": True},
                    {"input": ["a"], "expected": True, "hidden": True},
                    {"input": ["Aa"], "expected": False, "hidden": True}
                ],
                "hints": [
                    "Compare the string with its reverse",
                    "You can use string slicing: s[::-1]",
                    "Consider case sensitivity"
                ],
                "time_limit": 3,
                "memory_limit": 128,
                "points": 30
            }
        ]
        
        # Save challenges to files
        for challenge in easy_challenges:
            self.save_challenge(challenge)
        
        for challenge in medium_challenges:
            self.save_challenge(challenge)
    
    def save_challenge(self, challenge: Dict):
        """Save a challenge to file"""
        difficulty = challenge["difficulty"]
        category = challenge["category"]
        challenge_id = challenge["id"]
        
        challenge_file = os.path.join(
            self.challenges_dir, difficulty, category, f"{challenge_id}.json"
        )
        
        if not os.path.exists(challenge_file):
            with open(challenge_file, 'w') as f:
                json.dump(challenge, f, indent=2)
    
    def load_challenge(self, challenge_id: str) -> Optional[Dict]:
        """Load a challenge by ID"""
        # Search through all difficulty and category folders
        for difficulty in ["easy", "medium", "hard", "expert"]:
            for category in ["basics", "algorithms", "data_structures", "math", "strings", "lists"]:
                challenge_file = os.path.join(
                    self.challenges_dir, difficulty, category, f"{challenge_id}.json"
                )
                
                if os.path.exists(challenge_file):
                    try:
                        with open(challenge_file, 'r') as f:
                            challenge = json.load(f)
                            self.current_challenge = challenge
                            return challenge
                    except Exception as e:
                        print(f"Error loading challenge: {e}")
        
        return None
    
    def get_available_challenges(self, difficulty: str = None, category: str = None) -> List[Dict]:
        """Get list of available challenges"""
        challenges = []
        
        difficulties = [difficulty] if difficulty else ["easy", "medium", "hard", "expert"]
        categories = [category] if category else ["basics", "algorithms", "data_structures", "math", "strings", "lists"]
        
        for diff in difficulties:
            for cat in categories:
                challenge_dir = os.path.join(self.challenges_dir, diff, cat)
                
                if os.path.exists(challenge_dir):
                    for filename in os.listdir(challenge_dir):
                        if filename.endswith('.json'):
                            challenge_file = os.path.join(challenge_dir, filename)
                            try:
                                with open(challenge_file, 'r') as f:
                                    challenge = json.load(f)
                                    challenges.append({
                                        "id": challenge["id"],
                                        "title": challenge["title"],
                                        "difficulty": challenge["difficulty"],
                                        "category": challenge["category"],
                                        "points": challenge.get("points", 0),
                                        "description": challenge["description"][:100] + "..." if len(challenge["description"]) > 100 else challenge["description"]
                                    })
                            except Exception:
                                continue
        
        return sorted(challenges, key=lambda x: (x["difficulty"], x["points"]))
    
    def display_challenge(self, challenge: Dict):
        """Display challenge information"""
        print(f"\n{Fore.GREEN}🎯 {challenge['title']}{Style.RESET_ALL}")
        print("=" * 60)
        print(f"Difficulty: {self.get_difficulty_color(challenge['difficulty'])}{challenge['difficulty'].title()}{Style.RESET_ALL}")
        print(f"Category: {challenge['category'].title()}")
        print(f"Points: {challenge.get('points', 0)}")
        print(f"Time Limit: {challenge.get('time_limit', 'No limit')} seconds")
        
        print(f"\n{Fore.CYAN}📝 Description:{Style.RESET_ALL}")
        print(challenge["description"])
        
        print(f"\n{Fore.YELLOW}📋 Function Signature:{Style.RESET_ALL}")
        params = ", ".join(challenge.get("parameters", []))
        return_type = challenge.get("return_type", "Any")
        print(f"def {challenge['function_name']}({params}) -> {return_type}:")
        
        if challenge.get("examples"):
            print(f"\n{Fore.BLUE}💡 Examples:{Style.RESET_ALL}")
            for i, example in enumerate(challenge["examples"], 1):
                input_str = ", ".join(map(str, example["input"])) if example["input"] else ""
                print(f"{i}. {challenge['function_name']}({input_str}) → {example['output']}")
    
    def get_difficulty_color(self, difficulty: str) -> str:
        """Get color for difficulty level"""
        colors = {
            "easy": Fore.GREEN,
            "medium": Fore.YELLOW,
            "hard": Fore.RED,
            "expert": Fore.MAGENTA
        }
        return colors.get(difficulty, Fore.WHITE)
    
    def run_challenge(self, challenge_id: str) -> Dict:
        """Run a coding challenge"""
        challenge = self.load_challenge(challenge_id)
        if not challenge:
            return {"error": f"Challenge {challenge_id} not found"}
        
        self.display_challenge(challenge)
        
        print(f"\n{Fore.CYAN}Write your solution:{Style.RESET_ALL}")
        print("(Type 'hint' for a hint, 'examples' to see examples again, 'submit' when ready)")
        
        user_code = ""
        hints_used = 0
        
        while True:
            line = input(">>> ").strip()
            
            if line.lower() == 'submit':
                if not user_code.strip():
                    print(f"{Fore.RED}Please write your solution first.{Style.RESET_ALL}")
                    continue
                break
            elif line.lower() == 'hint':
                hints = challenge.get("hints", [])
                if hints_used < len(hints):
                    print(f"{Fore.BLUE}💡 Hint {hints_used + 1}: {hints[hints_used]}{Style.RESET_ALL}")
                    hints_used += 1
                else:
                    print(f"{Fore.YELLOW}No more hints available.{Style.RESET_ALL}")
                continue
            elif line.lower() == 'examples':
                if challenge.get("examples"):
                    print(f"\n{Fore.BLUE}💡 Examples:{Style.RESET_ALL}")
                    for i, example in enumerate(challenge["examples"], 1):
                        input_str = ", ".join(map(str, example["input"])) if example["input"] else ""
                        print(f"{i}. {challenge['function_name']}({input_str}) → {example['output']}")
                continue
            elif line.lower() == 'clear':
                user_code = ""
                print(f"{Fore.GREEN}Code cleared. Start over.{Style.RESET_ALL}")
                continue
            
            user_code += line + "\n"
        
        # Test the solution
        return self.test_solution(challenge, user_code, hints_used)
    
    def test_solution(self, challenge: Dict, user_code: str, hints_used: int) -> Dict:
        """Test user's solution against test cases"""
        print(f"\n{Fore.YELLOW}🧪 Testing your solution...{Style.RESET_ALL}")
        
        try:
            # Parse and validate the code
            tree = ast.parse(user_code)
            
            # Check if function is defined
            function_name = challenge["function_name"]
            function_found = False
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and node.name == function_name:
                    function_found = True
                    break
            
            if not function_found:
                return {
                    "success": False,
                    "error": f"Function '{function_name}' not found in your code",
                    "score": 0
                }
            
            # Execute the code
            exec_globals = {}
            exec(user_code, exec_globals)
            
            user_function = exec_globals.get(function_name)
            if not user_function:
                return {
                    "success": False,
                    "error": f"Function '{function_name}' not accessible",
                    "score": 0
                }
            
            # Run test cases
            test_cases = challenge.get("test_cases", [])
            passed_tests = 0
            failed_tests = []
            
            for i, test_case in enumerate(test_cases):
                try:
                    start_time = time.time()
                    result = user_function(*test_case["input"])
                    execution_time = time.time() - start_time
                    
                    # Check time limit
                    time_limit = challenge.get("time_limit", float('inf'))
                    if execution_time > time_limit:
                        failed_tests.append({
                            "test_case": i + 1,
                            "error": f"Time limit exceeded ({execution_time:.2f}s > {time_limit}s)",
                            "input": test_case["input"],
                            "hidden": test_case.get("hidden", False)
                        })
                        continue
                    
                    # Check result
                    if result == test_case["expected"]:
                        passed_tests += 1
                        if not test_case.get("hidden", False):
                            print(f"{Fore.GREEN}✅ Test {i + 1}: Passed{Style.RESET_ALL}")
                    else:
                        failed_tests.append({
                            "test_case": i + 1,
                            "error": f"Expected {test_case['expected']}, got {result}",
                            "input": test_case["input"],
                            "expected": test_case["expected"],
                            "actual": result,
                            "hidden": test_case.get("hidden", False)
                        })
                        if not test_case.get("hidden", False):
                            print(f"{Fore.RED}❌ Test {i + 1}: Failed{Style.RESET_ALL}")
                            print(f"   Input: {test_case['input']}")
                            print(f"   Expected: {test_case['expected']}")
                            print(f"   Got: {result}")
                
                except Exception as e:
                    failed_tests.append({
                        "test_case": i + 1,
                        "error": f"Runtime error: {str(e)}",
                        "input": test_case["input"],
                        "hidden": test_case.get("hidden", False)
                    })
                    if not test_case.get("hidden", False):
                        print(f"{Fore.RED}❌ Test {i + 1}: Runtime Error{Style.RESET_ALL}")
                        print(f"   Error: {str(e)}")
            
            # Calculate score
            total_tests = len(test_cases)
            success_rate = passed_tests / total_tests if total_tests > 0 else 0
            base_points = challenge.get("points", 0)
            
            # Reduce points for hints used
            hint_penalty = hints_used * 0.1
            final_score = max(0, base_points * success_rate * (1 - hint_penalty))
            
            # Show results
            print(f"\n{Fore.CYAN}📊 Results:{Style.RESET_ALL}")
            print(f"Tests passed: {passed_tests}/{total_tests}")
            print(f"Success rate: {success_rate * 100:.1f}%")
            print(f"Points earned: {final_score:.0f}/{base_points}")
            
            if hints_used > 0:
                print(f"Hints used: {hints_used} (penalty applied)")
            
            if passed_tests == total_tests:
                print(f"\n{Fore.GREEN}🎉 Congratulations! All tests passed!{Style.RESET_ALL}")
            elif success_rate >= 0.8:
                print(f"\n{Fore.YELLOW}👍 Great job! Most tests passed.{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}💪 Keep trying! Review the failed test cases.{Style.RESET_ALL}")
            
            return {
                "success": passed_tests == total_tests,
                "passed_tests": passed_tests,
                "total_tests": total_tests,
                "success_rate": success_rate,
                "score": final_score,
                "hints_used": hints_used,
                "failed_tests": failed_tests
            }
            
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"Syntax error: {str(e)}",
                "score": 0
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Execution error: {str(e)}",
                "score": 0
            }
    
    def show_challenge_menu(self):
        """Show challenge selection menu"""
        print(f"\n{Fore.GREEN}🎮 Coding Challenges{Style.RESET_ALL}")
        print("=" * 50)
        
        challenges = self.get_available_challenges()
        
        if not challenges:
            print("No challenges available yet.")
            return None
        
        # Group by difficulty
        by_difficulty = {}
        for challenge in challenges:
            difficulty = challenge["difficulty"]
            if difficulty not in by_difficulty:
                by_difficulty[difficulty] = []
            by_difficulty[difficulty].append(challenge)
        
        # Display challenges
        for difficulty in ["easy", "medium", "hard", "expert"]:
            if difficulty in by_difficulty:
                color = self.get_difficulty_color(difficulty)
                print(f"\n{color}{difficulty.upper()} CHALLENGES:{Style.RESET_ALL}")
                
                for i, challenge in enumerate(by_difficulty[difficulty], 1):
                    print(f"{i}. {challenge['title']} ({challenge['points']} points)")
                    print(f"   {challenge['description']}")
        
        print(f"\n{Fore.CYAN}Enter challenge ID to start (e.g., 'easy_001'):{Style.RESET_ALL}")
        return input(">>> ").strip()
