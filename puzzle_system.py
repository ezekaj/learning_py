#!/usr/bin/env python3
"""
🧩 REVOLUTIONARY PUZZLE SYSTEM
Innovative coding puzzles that make learning Python absolutely engaging
"""

import json
import random
from typing import Dict, List, Any, Optional

class VisualCodePuzzles:
    """
    Visual programming puzzles inspired by Tetris, Jigsaw, and Logic Circuits
    """
    
    def __init__(self):
        self.puzzle_types = [
            'code_tetris',
            'programming_jigsaw', 
            'logic_circuits',
            'code_crossword',
            'syntax_sudoku'
        ]
    
    def create_code_tetris(self, concept: str, difficulty: str) -> Dict:
        """Code Tetris - Arrange falling code blocks to complete functions"""
        
        if concept == 'functions':
            blocks = [
                {'id': 'def_block', 'code': 'def calculate_area(length, width):', 'type': 'function_def', 'shape': 'L'},
                {'id': 'return_block', 'code': '    return length * width', 'type': 'return', 'shape': 'I'},
                {'id': 'call_block', 'code': 'result = calculate_area(5, 3)', 'type': 'function_call', 'shape': 'T'},
                {'id': 'print_block', 'code': 'print(f"Area: {result}")', 'type': 'output', 'shape': 'O'}
            ]
            
            target_function = """def calculate_area(length, width):
    return length * width

result = calculate_area(5, 3)
print(f"Area: {result}")"""
        
        elif concept == 'loops':
            blocks = [
                {'id': 'for_block', 'code': 'for i in range(5):', 'type': 'loop_start', 'shape': 'L'},
                {'id': 'print_block', 'code': '    print(f"Number: {i}")', 'type': 'loop_body', 'shape': 'I'},
                {'id': 'if_block', 'code': '    if i % 2 == 0:', 'type': 'condition', 'shape': 'T'},
                {'id': 'even_block', 'code': '        print("Even!")', 'type': 'conditional_body', 'shape': 'O'}
            ]
            
            target_function = """for i in range(5):
    print(f"Number: {i}")
    if i % 2 == 0:
        print("Even!")"""
        
        else:  # variables
            blocks = [
                {'id': 'name_block', 'code': 'name = "Python"', 'type': 'variable', 'shape': 'I'},
                {'id': 'age_block', 'code': 'age = 30', 'type': 'variable', 'shape': 'I'},
                {'id': 'greeting_block', 'code': 'greeting = f"Hello, {name}!"', 'type': 'variable', 'shape': 'L'},
                {'id': 'print_block', 'code': 'print(greeting)', 'type': 'output', 'shape': 'O'}
            ]
            
            target_function = """name = "Python"
age = 30
greeting = f"Hello, {name}!"
print(greeting)"""
        
        return {
            'type': 'code_tetris',
            'title': f'Code Tetris: {concept.title()}',
            'description': 'Arrange the falling code blocks to create a working program!',
            'blocks': blocks,
            'target': target_function,
            'grid_size': {'width': 10, 'height': 20},
            'difficulty': difficulty,
            'time_limit': 180,  # 3 minutes
            'scoring': {
                'perfect_placement': 100,
                'line_clear': 50,
                'time_bonus': True
            },
            'hints': [
                'Start with the function definition',
                'Pay attention to indentation',
                'The blocks must fit together logically'
            ]
        }
    
    def create_programming_jigsaw(self, concept: str, difficulty: str) -> Dict:
        """Programming Jigsaw - Piece together algorithms visually"""
        
        if concept == 'sorting':
            pieces = [
                {'id': 'piece_1', 'code': 'def bubble_sort(arr):', 'position': 'top_left', 'connections': ['bottom']},
                {'id': 'piece_2', 'code': '    n = len(arr)', 'position': 'top_middle', 'connections': ['top', 'bottom']},
                {'id': 'piece_3', 'code': '    for i in range(n):', 'position': 'middle_left', 'connections': ['top', 'bottom']},
                {'id': 'piece_4', 'code': '        for j in range(0, n-i-1):', 'position': 'middle_middle', 'connections': ['top', 'bottom']},
                {'id': 'piece_5', 'code': '            if arr[j] > arr[j+1]:', 'position': 'middle_right', 'connections': ['top', 'bottom']},
                {'id': 'piece_6', 'code': '                arr[j], arr[j+1] = arr[j+1], arr[j]', 'position': 'bottom_left', 'connections': ['top']},
                {'id': 'piece_7', 'code': '    return arr', 'position': 'bottom_right', 'connections': ['top']}
            ]
        
        elif concept == 'recursion':
            pieces = [
                {'id': 'piece_1', 'code': 'def factorial(n):', 'position': 'top', 'connections': ['bottom']},
                {'id': 'piece_2', 'code': '    if n <= 1:', 'position': 'middle_left', 'connections': ['top', 'right']},
                {'id': 'piece_3', 'code': '        return 1', 'position': 'middle_right', 'connections': ['left', 'bottom']},
                {'id': 'piece_4', 'code': '    else:', 'position': 'bottom_left', 'connections': ['top', 'right']},
                {'id': 'piece_5', 'code': '        return n * factorial(n-1)', 'position': 'bottom_right', 'connections': ['left']}
            ]
        
        else:  # basic algorithm
            pieces = [
                {'id': 'piece_1', 'code': 'def find_max(numbers):', 'position': 'top', 'connections': ['bottom']},
                {'id': 'piece_2', 'code': '    max_num = numbers[0]', 'position': 'middle_top', 'connections': ['top', 'bottom']},
                {'id': 'piece_3', 'code': '    for num in numbers[1:]:', 'position': 'middle', 'connections': ['top', 'bottom']},
                {'id': 'piece_4', 'code': '        if num > max_num:', 'position': 'middle_bottom', 'connections': ['top', 'bottom']},
                {'id': 'piece_5', 'code': '            max_num = num', 'position': 'bottom_middle', 'connections': ['top', 'bottom']},
                {'id': 'piece_6', 'code': '    return max_num', 'position': 'bottom', 'connections': ['top']}
            ]
        
        return {
            'type': 'programming_jigsaw',
            'title': f'Programming Jigsaw: {concept.title()}',
            'description': 'Piece together the algorithm by connecting the code fragments!',
            'pieces': pieces,
            'board_size': {'width': 800, 'height': 600},
            'difficulty': difficulty,
            'time_limit': 300,  # 5 minutes
            'validation': {
                'check_connections': True,
                'check_logic_flow': True,
                'check_syntax': True
            },
            'hints': [
                'Start with the function definition',
                'Follow the logical flow of the algorithm',
                'Check that pieces connect properly'
            ]
        }
    
    def create_logic_circuits(self, concept: str, difficulty: str) -> Dict:
        """Logic Circuits - Build programs using visual logic gates"""
        
        if concept == 'conditionals':
            components = [
                {'id': 'input_age', 'type': 'input', 'label': 'age', 'value_type': 'number'},
                {'id': 'input_license', 'type': 'input', 'label': 'has_license', 'value_type': 'boolean'},
                {'id': 'compare_18', 'type': 'comparator', 'operation': '>=', 'value': 18},
                {'id': 'and_gate', 'type': 'and_gate', 'inputs': 2},
                {'id': 'output_drive', 'type': 'output', 'label': 'can_drive', 'value_type': 'boolean'}
            ]
            
            connections = [
                {'from': 'input_age', 'to': 'compare_18'},
                {'from': 'compare_18', 'to': 'and_gate', 'input': 0},
                {'from': 'input_license', 'to': 'and_gate', 'input': 1},
                {'from': 'and_gate', 'to': 'output_drive'}
            ]
        
        elif concept == 'loops':
            components = [
                {'id': 'input_start', 'type': 'input', 'label': 'start', 'value_type': 'number'},
                {'id': 'input_end', 'type': 'input', 'label': 'end', 'value_type': 'number'},
                {'id': 'counter', 'type': 'counter', 'initial': 0},
                {'id': 'compare_end', 'type': 'comparator', 'operation': '<'},
                {'id': 'increment', 'type': 'increment', 'step': 1},
                {'id': 'output_numbers', 'type': 'output', 'label': 'numbers', 'value_type': 'list'}
            ]
            
            connections = [
                {'from': 'input_start', 'to': 'counter'},
                {'from': 'counter', 'to': 'compare_end', 'input': 0},
                {'from': 'input_end', 'to': 'compare_end', 'input': 1},
                {'from': 'compare_end', 'to': 'increment'},
                {'from': 'increment', 'to': 'counter'},
                {'from': 'counter', 'to': 'output_numbers'}
            ]
        
        else:  # basic logic
            components = [
                {'id': 'input_x', 'type': 'input', 'label': 'x', 'value_type': 'number'},
                {'id': 'input_y', 'type': 'input', 'label': 'y', 'value_type': 'number'},
                {'id': 'add_gate', 'type': 'add_gate', 'inputs': 2},
                {'id': 'multiply_2', 'type': 'multiplier', 'value': 2},
                {'id': 'output_result', 'type': 'output', 'label': 'result', 'value_type': 'number'}
            ]
            
            connections = [
                {'from': 'input_x', 'to': 'add_gate', 'input': 0},
                {'from': 'input_y', 'to': 'add_gate', 'input': 1},
                {'from': 'add_gate', 'to': 'multiply_2'},
                {'from': 'multiply_2', 'to': 'output_result'}
            ]
        
        return {
            'type': 'logic_circuits',
            'title': f'Logic Circuits: {concept.title()}',
            'description': 'Build the program logic using visual components and connections!',
            'components': components,
            'connections': connections,
            'canvas_size': {'width': 1000, 'height': 700},
            'difficulty': difficulty,
            'time_limit': 420,  # 7 minutes
            'test_cases': [
                {'inputs': {'age': 20, 'has_license': True}, 'expected': {'can_drive': True}},
                {'inputs': {'age': 16, 'has_license': True}, 'expected': {'can_drive': False}},
                {'inputs': {'age': 25, 'has_license': False}, 'expected': {'can_drive': False}}
            ],
            'hints': [
                'Connect inputs to logic gates',
                'Follow the data flow from left to right',
                'Test your circuit with different inputs'
            ]
        }

class MysteryCodeChallenges:
    """
    Story-driven coding mysteries and detective challenges
    """
    
    def __init__(self):
        self.mystery_types = [
            'bug_hunt',
            'code_archaeology',
            'syntax_sherlock',
            'algorithm_escape_room'
        ]
    
    def create_bug_hunt_mystery(self, difficulty: str) -> Dict:
        """Bug Hunt - Find hidden errors in story-based scenarios"""
        
        mysteries = {
            'easy': {
                'title': 'The Case of the Missing Output',
                'story': """
Detective Python was called to investigate a strange case. A programmer's code was supposed to greet users, but nothing appeared on the screen. The programmer swears the code is correct, but something is definitely wrong.

Can you help Detective Python solve this mystery?
                """,
                'buggy_code': """
def greet_user(name):
    greeting = f"Hello, {name}!"
    # The greeting should appear here
    
greet_user("Alice")
                """,
                'bug_type': 'missing_print',
                'clues': [
                    'The function creates a greeting message',
                    'The function is called with "Alice"',
                    'But nothing appears on the screen...',
                    'What happens to the greeting variable?'
                ],
                'solution': 'Add print(greeting) inside the function',
                'explanation': 'The function creates the greeting but never displays it. Adding print(greeting) will show the message.'
            },
            
            'medium': {
                'title': 'The Mysterious Infinite Loop',
                'story': """
A programmer at TechCorp reported that their counting program never stops running. It's supposed to count from 1 to 10, but it seems to go on forever. The office is in chaos as the program consumes all the computer's resources.

Detective Python needs your help to stop this runaway code!
                """,
                'buggy_code': """
def count_to_ten():
    counter = 1
    while counter <= 10:
        print(f"Count: {counter}")
        # Something is missing here...
    print("Counting complete!")

count_to_ten()
                """,
                'bug_type': 'infinite_loop',
                'clues': [
                    'The counter starts at 1',
                    'The loop should stop when counter > 10',
                    'But the counter never changes...',
                    'What should happen inside the loop?'
                ],
                'solution': 'Add counter += 1 inside the loop',
                'explanation': 'The counter variable never increases, so the condition counter <= 10 is always true, creating an infinite loop.'
            }
        }
        
        mystery = mysteries.get(difficulty, mysteries['easy'])
        
        return {
            'type': 'bug_hunt',
            'title': mystery['title'],
            'story': mystery['story'],
            'buggy_code': mystery['buggy_code'],
            'clues': mystery['clues'],
            'difficulty': difficulty,
            'time_limit': 600,  # 10 minutes
            'scoring': {
                'bug_found': 50,
                'correct_fix': 100,
                'explanation_bonus': 25,
                'time_bonus': True
            },
            'hints': [
                'Read the story carefully for context',
                'Look for what the code is supposed to do vs what it actually does',
                'Check for missing statements or incorrect logic'
            ]
        }
    
    def create_algorithm_escape_room(self, difficulty: str) -> Dict:
        """Algorithm Escape Room - Use coding to escape virtual rooms"""
        
        rooms = {
            'easy': {
                'title': 'Escape the Variable Vault',
                'story': """
You're trapped in a vault where the only way out is to solve the combination lock. The lock requires you to create the correct variables with specific values. The vault's AI will only open if you can demonstrate your understanding of Python variables.
                """,
                'challenges': [
                    {
                        'description': 'Create a variable called "key" with the value 42',
                        'solution': 'key = 42',
                        'test': 'key == 42'
                    },
                    {
                        'description': 'Create a variable called "password" with your name',
                        'solution': 'password = "YourName"',
                        'test': 'isinstance(password, str) and len(password) > 0'
                    },
                    {
                        'description': 'Create a variable called "unlocked" with the boolean value True',
                        'solution': 'unlocked = True',
                        'test': 'unlocked is True'
                    }
                ]
            },
            
            'medium': {
                'title': 'Escape the Function Factory',
                'story': """
You're trapped in an automated factory where machines are controlled by functions. To escape, you must program the machines correctly by writing functions that perform specific tasks. Each successful function brings you closer to freedom!
                """,
                'challenges': [
                    {
                        'description': 'Write a function called "open_door" that takes a code and returns True if the code is "ESCAPE"',
                        'solution': 'def open_door(code):\n    return code == "ESCAPE"',
                        'test': 'open_door("ESCAPE") == True and open_door("WRONG") == False'
                    },
                    {
                        'description': 'Write a function called "calculate_steps" that takes distance and returns distance * 2',
                        'solution': 'def calculate_steps(distance):\n    return distance * 2',
                        'test': 'calculate_steps(5) == 10 and calculate_steps(3) == 6'
                    }
                ]
            }
        }
        
        room = rooms.get(difficulty, rooms['easy'])
        
        return {
            'type': 'algorithm_escape_room',
            'title': room['title'],
            'story': room['story'],
            'challenges': room['challenges'],
            'current_challenge': 0,
            'difficulty': difficulty,
            'time_limit': 900,  # 15 minutes
            'atmosphere': {
                'background': 'dark_vault',
                'sound_effects': True,
                'tension_music': True
            },
            'scoring': {
                'challenge_solved': 100,
                'escape_bonus': 200,
                'time_bonus': True,
                'no_hints_bonus': 50
            }
        }

class CreativeCodingStudio:
    """
    Creative coding challenges - Art, Music, Games, Stories
    """
    
    def __init__(self):
        self.creative_types = [
            'art_generator',
            'music_maker',
            'game_builder',
            'story_generator'
        ]
    
    def create_art_generator_challenge(self, difficulty: str) -> Dict:
        """Create beautiful art with Python code"""
        
        challenges = {
            'easy': {
                'title': 'ASCII Art Creator',
                'description': 'Create beautiful patterns using text characters',
                'template': '''
# Create a simple pattern
def create_pattern(size):
    for i in range(size):
        # Your code here
        pass

create_pattern(5)
                ''',
                'examples': [
                    {'pattern': 'stars', 'code': 'print("*" * (i + 1))'},
                    {'pattern': 'pyramid', 'code': 'print(" " * (size - i - 1) + "*" * (2 * i + 1))'},
                    {'pattern': 'diamond', 'code': 'Complex diamond pattern'}
                ]
            },
            
            'medium': {
                'title': 'Color Pattern Generator',
                'description': 'Generate colorful patterns using Python',
                'template': '''
# Create colorful patterns
import random

def generate_color_pattern(width, height):
    colors = ["🔴", "🟡", "🟢", "🔵", "🟣"]
    for row in range(height):
        # Your creative code here
        pass

generate_color_pattern(10, 5)
                ''',
                'examples': [
                    {'pattern': 'rainbow', 'description': 'Create rainbow stripes'},
                    {'pattern': 'checkerboard', 'description': 'Alternating color pattern'},
                    {'pattern': 'random', 'description': 'Random colorful noise'}
                ]
            }
        }
        
        challenge = challenges.get(difficulty, challenges['easy'])
        
        return {
            'type': 'art_generator',
            'title': challenge['title'],
            'description': challenge['description'],
            'template_code': challenge['template'],
            'examples': challenge.get('examples', []),
            'difficulty': difficulty,
            'time_limit': 1200,  # 20 minutes
            'tools': {
                'live_preview': True,
                'color_palette': True,
                'pattern_library': True
            },
            'sharing': {
                'gallery_submission': True,
                'peer_voting': True,
                'featured_artwork': True
            }
        }

# Global puzzle system instances
visual_puzzles = VisualCodePuzzles()
mystery_challenges = MysteryCodeChallenges()
creative_studio = CreativeCodingStudio()

def create_daily_puzzle(user_level: str, user_interests: List[str]) -> Dict:
    """Create a personalized daily puzzle based on user preferences"""
    
    puzzle_types = ['visual', 'mystery', 'creative']
    selected_type = random.choice(puzzle_types)
    
    if selected_type == 'visual':
        concept = random.choice(['functions', 'loops', 'conditionals'])
        if 'tetris' in user_interests:
            return visual_puzzles.create_code_tetris(concept, user_level)
        elif 'jigsaw' in user_interests:
            return visual_puzzles.create_programming_jigsaw(concept, user_level)
        else:
            return visual_puzzles.create_logic_circuits(concept, user_level)
    
    elif selected_type == 'mystery':
        if 'detective' in user_interests:
            return mystery_challenges.create_bug_hunt_mystery(user_level)
        else:
            return mystery_challenges.create_algorithm_escape_room(user_level)
    
    else:  # creative
        return creative_studio.create_art_generator_challenge(user_level)

if __name__ == "__main__":
    # Test the puzzle system
    print("🧩 Testing Revolutionary Puzzle System...")
    
    # Test Code Tetris
    tetris_puzzle = visual_puzzles.create_code_tetris('functions', 'medium')
    print(f"✅ Code Tetris: {tetris_puzzle['title']}")
    
    # Test Bug Hunt Mystery
    mystery_puzzle = mystery_challenges.create_bug_hunt_mystery('easy')
    print(f"✅ Bug Hunt: {mystery_puzzle['title']}")
    
    # Test Creative Coding
    art_puzzle = creative_studio.create_art_generator_challenge('easy')
    print(f"✅ Art Generator: {art_puzzle['title']}")
    
    # Test Daily Puzzle
    daily_puzzle = create_daily_puzzle('medium', ['tetris', 'detective'])
    print(f"✅ Daily Puzzle: {daily_puzzle['title']}")
    
    print("\n🎮 Revolutionary Puzzle System is ready!")
