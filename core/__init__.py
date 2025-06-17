"""
Core modules for the Python Learning Platform
Provides essential functionality for the learning system
"""

from .progress_tracker import ProgressTracker
from .quiz_engine import QuizEngine
from .challenge_system import ChallengeSystem
from .code_runner import CodeRunner

__all__ = [
    'ProgressTracker',
    'QuizEngine', 
    'ChallengeSystem',
    'CodeRunner'
]

__version__ = "2.0.0"
