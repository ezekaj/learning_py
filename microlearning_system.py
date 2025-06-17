#!/usr/bin/env python3
"""
🧠 REVOLUTIONARY MICROLEARNING SYSTEM
Adaptive microlearning with spaced repetition and AI-powered optimization
"""

import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

class SpacedRepetitionEngine:
    """
    Advanced spaced repetition system based on research from top platforms
    """
    
    def __init__(self):
        # Spaced repetition intervals (in hours)
        self.intervals = [1, 4, 24, 72, 168, 336, 720, 1440]  # 1h, 4h, 1d, 3d, 1w, 2w, 1m, 2m
        self.difficulty_multipliers = {
            'easy': 0.7,
            'medium': 1.0,
            'hard': 1.5,
            'very_hard': 2.0
        }
    
    def calculate_next_review(self, concept_id: str, user_performance: Dict, difficulty: str = 'medium') -> datetime:
        """Calculate when to review this concept next"""
        performance_history = user_performance.get(concept_id, [])
        
        if not performance_history:
            # First time learning - review in 1 hour
            return datetime.now() + timedelta(hours=1)
        
        # Calculate success rate
        recent_attempts = performance_history[-5:]  # Last 5 attempts
        success_rate = sum(attempt['correct'] for attempt in recent_attempts) / len(recent_attempts)
        
        # Determine interval index based on success rate
        if success_rate >= 0.9:
            interval_index = min(len(performance_history), len(self.intervals) - 1)
        elif success_rate >= 0.7:
            interval_index = min(len(performance_history) - 1, len(self.intervals) - 2)
        else:
            interval_index = max(0, len(performance_history) - 2)
        
        # Apply difficulty multiplier
        base_interval = self.intervals[interval_index]
        adjusted_interval = base_interval * self.difficulty_multipliers[difficulty]
        
        return datetime.now() + timedelta(hours=adjusted_interval)
    
    def get_concepts_to_review(self, user_id: str, user_data: Dict) -> List[Dict]:
        """Get concepts that are due for review"""
        concepts_to_review = []
        current_time = datetime.now()
        
        user_progress = user_data.get('spaced_repetition', {})
        
        for concept_id, concept_data in user_progress.items():
            next_review = datetime.fromisoformat(concept_data.get('next_review', current_time.isoformat()))
            
            if next_review <= current_time:
                concepts_to_review.append({
                    'concept_id': concept_id,
                    'priority': self.calculate_priority(concept_data),
                    'last_performance': concept_data.get('last_performance', 0.5)
                })
        
        # Sort by priority (highest first)
        concepts_to_review.sort(key=lambda x: x['priority'], reverse=True)
        return concepts_to_review
    
    def calculate_priority(self, concept_data: Dict) -> float:
        """Calculate review priority based on forgetting curve"""
        last_review = datetime.fromisoformat(concept_data.get('last_review', datetime.now().isoformat()))
        time_since_review = (datetime.now() - last_review).total_seconds() / 3600  # hours
        
        performance = concept_data.get('last_performance', 0.5)
        
        # Forgetting curve: priority increases with time and decreases with performance
        priority = time_since_review * (1 - performance) * 100
        return priority

class MicrolearningChunker:
    """
    Intelligent system to break lessons into optimal microlearning chunks
    """
    
    def __init__(self):
        self.optimal_chunk_time = 4  # 4 minutes per chunk
        self.max_concepts_per_chunk = 3
        self.chunk_types = [
            'concept_introduction',
            'example_walkthrough', 
            'practice_exercise',
            'knowledge_check',
            'real_world_application'
        ]
    
    def chunk_lesson(self, lesson_content: Dict) -> List[Dict]:
        """Break a lesson into optimal microlearning chunks"""
        chunks = []
        
        # Extract main concepts
        concepts = self.extract_concepts(lesson_content)
        
        # Create introduction chunk
        chunks.append(self.create_intro_chunk(lesson_content, concepts))
        
        # Create concept chunks
        for i, concept in enumerate(concepts):
            # Concept introduction
            chunks.append(self.create_concept_chunk(concept, i + 1))
            
            # Example walkthrough
            chunks.append(self.create_example_chunk(concept, i + 1))
            
            # Practice exercise
            chunks.append(self.create_practice_chunk(concept, i + 1))
            
            # Knowledge check
            chunks.append(self.create_knowledge_check(concept, i + 1))
        
        # Create summary chunk
        chunks.append(self.create_summary_chunk(lesson_content, concepts))
        
        return chunks
    
    def extract_concepts(self, lesson_content: Dict) -> List[Dict]:
        """Extract main concepts from lesson content"""
        # This would use NLP in a real implementation
        objectives = lesson_content.get('objectives', [])
        
        concepts = []
        for i, objective in enumerate(objectives):
            concepts.append({
                'id': f"concept_{i+1}",
                'title': objective,
                'description': f"Learn about {objective.lower()}",
                'difficulty': 'medium',
                'examples': [],
                'exercises': []
            })
        
        return concepts
    
    def create_intro_chunk(self, lesson_content: Dict, concepts: List[Dict]) -> Dict:
        """Create lesson introduction chunk"""
        return {
            'id': 'intro',
            'type': 'concept_introduction',
            'title': f"Welcome to {lesson_content.get('title', 'Python Lesson')}",
            'content': {
                'text': lesson_content.get('description', ''),
                'objectives': [concept['title'] for concept in concepts],
                'estimated_time': len(concepts) * 4,
                'difficulty': lesson_content.get('difficulty', 'medium')
            },
            'estimated_time': 2,
            'interactive_elements': [
                {
                    'type': 'progress_preview',
                    'data': {'total_chunks': len(concepts) * 4 + 2}
                }
            ]
        }
    
    def create_concept_chunk(self, concept: Dict, index: int) -> Dict:
        """Create concept introduction chunk"""
        return {
            'id': f"concept_{index}",
            'type': 'concept_introduction',
            'title': concept['title'],
            'content': {
                'text': concept['description'],
                'key_points': [
                    f"Understanding {concept['title'].lower()}",
                    f"When to use {concept['title'].lower()}",
                    f"Common patterns with {concept['title'].lower()}"
                ],
                'visual_aids': [
                    {
                        'type': 'diagram',
                        'description': f"Visual representation of {concept['title']}"
                    }
                ]
            },
            'estimated_time': 3,
            'interactive_elements': [
                {
                    'type': 'concept_highlighter',
                    'data': {'concept_id': concept['id']}
                }
            ]
        }
    
    def create_example_chunk(self, concept: Dict, index: int) -> Dict:
        """Create example walkthrough chunk"""
        return {
            'id': f"example_{index}",
            'type': 'example_walkthrough',
            'title': f"{concept['title']} - Example",
            'content': {
                'code_example': self.generate_code_example(concept),
                'explanation': f"Let's see {concept['title'].lower()} in action",
                'step_by_step': [
                    "Step 1: Understand the problem",
                    "Step 2: Write the code",
                    "Step 3: Test the solution"
                ]
            },
            'estimated_time': 4,
            'interactive_elements': [
                {
                    'type': 'code_stepper',
                    'data': {'concept_id': concept['id']}
                },
                {
                    'type': 'live_code_editor',
                    'data': {'editable': False, 'runnable': True}
                }
            ]
        }
    
    def create_practice_chunk(self, concept: Dict, index: int) -> Dict:
        """Create practice exercise chunk"""
        return {
            'id': f"practice_{index}",
            'type': 'practice_exercise',
            'title': f"Practice: {concept['title']}",
            'content': {
                'challenge': f"Now it's your turn to practice {concept['title'].lower()}",
                'instructions': [
                    "Read the problem carefully",
                    "Write your solution",
                    "Test your code",
                    "Submit when ready"
                ],
                'hints': [
                    f"Remember the key concepts of {concept['title'].lower()}",
                    "Start with a simple approach",
                    "Test with different inputs"
                ]
            },
            'estimated_time': 5,
            'interactive_elements': [
                {
                    'type': 'code_editor',
                    'data': {'concept_id': concept['id'], 'has_tests': True}
                },
                {
                    'type': 'hint_system',
                    'data': {'progressive_hints': True}
                }
            ]
        }
    
    def create_knowledge_check(self, concept: Dict, index: int) -> Dict:
        """Create knowledge check chunk"""
        return {
            'id': f"check_{index}",
            'type': 'knowledge_check',
            'title': f"Quick Check: {concept['title']}",
            'content': {
                'questions': self.generate_quiz_questions(concept),
                'feedback_immediate': True,
                'explanation_on_wrong': True
            },
            'estimated_time': 2,
            'interactive_elements': [
                {
                    'type': 'adaptive_quiz',
                    'data': {'concept_id': concept['id'], 'difficulty_adaptive': True}
                }
            ]
        }
    
    def create_summary_chunk(self, lesson_content: Dict, concepts: List[Dict]) -> Dict:
        """Create lesson summary chunk"""
        return {
            'id': 'summary',
            'type': 'lesson_summary',
            'title': f"Summary: {lesson_content.get('title', 'Python Lesson')}",
            'content': {
                'key_takeaways': [concept['title'] for concept in concepts],
                'next_steps': "Ready for the next lesson!",
                'review_schedule': "We'll review these concepts using spaced repetition"
            },
            'estimated_time': 3,
            'interactive_elements': [
                {
                    'type': 'progress_celebration',
                    'data': {'lesson_completed': True}
                },
                {
                    'type': 'next_lesson_preview',
                    'data': {'show_preview': True}
                }
            ]
        }
    
    def generate_code_example(self, concept: Dict) -> str:
        """Generate appropriate code example for concept"""
        examples = {
            'variables': 'name = "Python"\nage = 25\nprint(f"Hello, {name}! You are {age} years old.")',
            'functions': 'def greet(name):\n    return f"Hello, {name}!"\n\nresult = greet("Python")\nprint(result)',
            'loops': 'for i in range(5):\n    print(f"Count: {i}")',
            'conditionals': 'age = 18\nif age >= 18:\n    print("You can vote!")\nelse:\n    print("Too young to vote")'
        }
        
        concept_title = concept['title'].lower()
        for key, example in examples.items():
            if key in concept_title:
                return example
        
        return 'print("Hello, Python!")'
    
    def generate_quiz_questions(self, concept: Dict) -> List[Dict]:
        """Generate quiz questions for concept"""
        return [
            {
                'question': f"What is the main purpose of {concept['title'].lower()}?",
                'type': 'multiple_choice',
                'options': [
                    f"To implement {concept['title'].lower()}",
                    "To confuse programmers",
                    "To make code longer",
                    "To slow down programs"
                ],
                'correct': 0,
                'explanation': f"{concept['title']} is used to {concept['description'].lower()}"
            }
        ]

class AdaptiveDifficultyEngine:
    """
    AI system that adapts content difficulty based on user performance
    """
    
    def __init__(self):
        self.performance_window = 10  # Consider last 10 interactions
        self.difficulty_levels = ['very_easy', 'easy', 'medium', 'hard', 'very_hard']
        self.adaptation_threshold = 0.2  # 20% change triggers adaptation
    
    def calculate_user_level(self, user_performance: List[Dict]) -> str:
        """Calculate current user difficulty level"""
        if not user_performance:
            return 'medium'
        
        recent_performance = user_performance[-self.performance_window:]
        success_rate = sum(p.get('correct', 0) for p in recent_performance) / len(recent_performance)
        
        if success_rate >= 0.9:
            return 'hard'
        elif success_rate >= 0.7:
            return 'medium'
        elif success_rate >= 0.5:
            return 'easy'
        else:
            return 'very_easy'
    
    def adapt_content_difficulty(self, content: Dict, target_difficulty: str) -> Dict:
        """Adapt content to target difficulty level"""
        adapted_content = content.copy()
        
        if target_difficulty == 'very_easy':
            adapted_content['hints'] = adapted_content.get('hints', []) + [
                "Take your time",
                "Break the problem into small steps",
                "Don't worry about making mistakes"
            ]
            adapted_content['time_limit'] = adapted_content.get('time_limit', 300) * 2
        
        elif target_difficulty == 'hard':
            adapted_content['additional_constraints'] = [
                "Optimize for performance",
                "Handle edge cases",
                "Write clean, readable code"
            ]
            adapted_content['time_limit'] = adapted_content.get('time_limit', 300) * 0.7
        
        return adapted_content

# Global instances
spaced_repetition = SpacedRepetitionEngine()
microlearning_chunker = MicrolearningChunker()
adaptive_difficulty = AdaptiveDifficultyEngine()

def create_microlearning_lesson(lesson_data: Dict, user_id: str, user_data: Dict) -> Dict:
    """Create a complete microlearning lesson with spaced repetition"""
    
    # Chunk the lesson
    chunks = microlearning_chunker.chunk_lesson(lesson_data)
    
    # Adapt difficulty
    user_level = adaptive_difficulty.calculate_user_level(
        user_data.get('performance_history', [])
    )
    
    adapted_chunks = []
    for chunk in chunks:
        adapted_chunk = adaptive_difficulty.adapt_content_difficulty(chunk, user_level)
        adapted_chunks.append(adapted_chunk)
    
    # Add spaced repetition schedule
    concepts_to_review = spaced_repetition.get_concepts_to_review(user_id, user_data)
    
    return {
        'lesson_id': lesson_data.get('id'),
        'title': lesson_data.get('title'),
        'chunks': adapted_chunks,
        'total_estimated_time': sum(chunk.get('estimated_time', 0) for chunk in adapted_chunks),
        'difficulty_level': user_level,
        'spaced_repetition': {
            'concepts_to_review': concepts_to_review,
            'review_count': len(concepts_to_review)
        },
        'adaptive_features': {
            'difficulty_adapted': True,
            'personalized_hints': True,
            'spaced_repetition_enabled': True
        }
    }

if __name__ == "__main__":
    # Test the microlearning system
    print("🧠 Testing Revolutionary Microlearning System...")
    
    sample_lesson = {
        'id': 'variables_lesson',
        'title': 'Python Variables and Data Types',
        'description': 'Learn how to store and manipulate data in Python',
        'objectives': [
            'Create and use variables',
            'Understand different data types',
            'Practice variable naming conventions'
        ],
        'difficulty': 'beginner'
    }
    
    sample_user_data = {
        'performance_history': [
            {'correct': 1, 'time_taken': 120},
            {'correct': 0, 'time_taken': 180},
            {'correct': 1, 'time_taken': 90}
        ]
    }
    
    microlearning_lesson = create_microlearning_lesson(sample_lesson, 'test_user', sample_user_data)
    
    print(f"✅ Created microlearning lesson with {len(microlearning_lesson['chunks'])} chunks")
    print(f"📊 Total estimated time: {microlearning_lesson['total_estimated_time']} minutes")
    print(f"🎯 Difficulty level: {microlearning_lesson['difficulty_level']}")
    print(f"🧠 Spaced repetition: {microlearning_lesson['spaced_repetition']['review_count']} concepts to review")
    
    print("\n✨ Revolutionary Microlearning System is ready!")
