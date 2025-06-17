"""
Database Models for Python Learning Program
Modern educational platform with proper database structure
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """User model with comprehensive profile data"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    experience_level = db.Column(db.String(50), nullable=False, default='complete_beginner')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    points = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    streak = db.Column(db.Integer, default=0)
    last_streak_date = db.Column(db.Date, nullable=True)
    goals = db.Column(db.Text, nullable=True)  # JSON string of learning goals
    
    # Relationships
    lesson_progress = db.relationship('LessonProgress', backref='user', lazy=True)
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True)
    challenge_submissions = db.relationship('ChallengeSubmission', backref='user', lazy=True)
    achievements = db.relationship('UserAchievement', backref='user', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def get_goals(self):
        """Get user goals as list"""
        if self.goals:
            return json.loads(self.goals)
        return []
    
    def set_goals(self, goals_list):
        """Set user goals from list"""
        self.goals = json.dumps(goals_list)

class Course(db.Model):
    """Course model for organizing lessons"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.String(50), nullable=False)  # beginner, intermediate, advanced, expert
    order_index = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='course', lazy=True, order_by='Lesson.order_index')
    
    def __repr__(self):
        return f'<Course {self.title}>'

class Lesson(db.Model):
    """Lesson model with rich content"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)  # JSON string with rich content
    objectives = db.Column(db.Text, nullable=True)  # JSON string of learning objectives
    estimated_time = db.Column(db.Integer, default=60)  # minutes
    difficulty = db.Column(db.String(50), default='beginner')
    order_index = db.Column(db.Integer, nullable=False, default=0)
    points_reward = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    
    # Relationships
    exercises = db.relationship('Exercise', backref='lesson', lazy=True)
    progress_records = db.relationship('LessonProgress', backref='lesson', lazy=True)
    
    def __repr__(self):
        return f'<Lesson {self.title}>'
    
    def get_content(self):
        """Get lesson content as dict"""
        if self.content:
            return json.loads(self.content)
        return {}
    
    def set_content(self, content_dict):
        """Set lesson content from dict"""
        self.content = json.dumps(content_dict)
    
    def get_objectives(self):
        """Get learning objectives as list"""
        if self.objectives:
            return json.loads(self.objectives)
        return []
    
    def set_objectives(self, objectives_list):
        """Set learning objectives from list"""
        self.objectives = json.dumps(objectives_list)

class Exercise(db.Model):
    """Exercise model for hands-on practice"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    exercise_type = db.Column(db.String(50), nullable=False)  # code_completion, multiple_choice, coding_challenge
    content = db.Column(db.Text, nullable=True)  # JSON string with exercise data
    solution = db.Column(db.Text, nullable=True)  # JSON string with solution
    hints = db.Column(db.Text, nullable=True)  # JSON string with hints
    points_reward = db.Column(db.Integer, default=5)
    order_index = db.Column(db.Integer, nullable=False, default=0)
    
    # Foreign Keys
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    
    def __repr__(self):
        return f'<Exercise {self.title}>'
    
    def get_content(self):
        """Get exercise content as dict"""
        if self.content:
            return json.loads(self.content)
        return {}
    
    def get_solution(self):
        """Get exercise solution as dict"""
        if self.solution:
            return json.loads(self.solution)
        return {}
    
    def get_hints(self):
        """Get exercise hints as list"""
        if self.hints:
            return json.loads(self.hints)
        return []

class LessonProgress(db.Model):
    """Track user progress through lessons"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    status = db.Column(db.String(50), default='not_started')  # not_started, in_progress, completed
    progress_percentage = db.Column(db.Float, default=0.0)
    time_spent = db.Column(db.Integer, default=0)  # minutes
    completed_date = db.Column(db.DateTime, nullable=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id', name='unique_user_lesson'),)
    
    def __repr__(self):
        return f'<LessonProgress User:{self.user_id} Lesson:{self.lesson_id}>'

class Quiz(db.Model):
    """Quiz model for knowledge testing"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.String(50), default='beginner')
    time_limit = db.Column(db.Integer, nullable=True)  # seconds
    questions = db.Column(db.Text, nullable=False)  # JSON string with questions
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True)
    
    def __repr__(self):
        return f'<Quiz {self.title}>'
    
    def get_questions(self):
        """Get quiz questions as list"""
        if self.questions:
            return json.loads(self.questions)
        return []

class QuizAttempt(db.Model):
    """Track quiz attempts and scores"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    max_score = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=True)  # seconds
    answers = db.Column(db.Text, nullable=True)  # JSON string with user answers
    completed_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizAttempt User:{self.user_id} Quiz:{self.quiz_id}>'
    
    @property
    def percentage(self):
        """Calculate percentage score"""
        if self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0

class Challenge(db.Model):
    """Coding challenge model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(50), default='easy')
    category = db.Column(db.String(100), nullable=True)
    function_name = db.Column(db.String(100), nullable=False)
    parameters = db.Column(db.Text, nullable=True)  # JSON string
    return_type = db.Column(db.String(50), nullable=True)
    examples = db.Column(db.Text, nullable=True)  # JSON string
    test_cases = db.Column(db.Text, nullable=False)  # JSON string
    hints = db.Column(db.Text, nullable=True)  # JSON string
    time_limit = db.Column(db.Integer, default=5)  # seconds
    memory_limit = db.Column(db.Integer, default=128)  # MB
    points_reward = db.Column(db.Integer, default=25)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    submissions = db.relationship('ChallengeSubmission', backref='challenge', lazy=True)
    
    def __repr__(self):
        return f'<Challenge {self.title}>'

class ChallengeSubmission(db.Model):
    """Track challenge submissions"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # passed, failed, error
    score = db.Column(db.Float, default=0.0)
    execution_time = db.Column(db.Float, nullable=True)
    test_results = db.Column(db.Text, nullable=True)  # JSON string
    submitted_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ChallengeSubmission User:{self.user_id} Challenge:{self.challenge_id}>'

class Achievement(db.Model):
    """Achievement definitions"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='🏆')
    points_reward = db.Column(db.Integer, default=50)
    condition_type = db.Column(db.String(50), nullable=False)  # lessons_completed, streak, etc.
    condition_value = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user_achievements = db.relationship('UserAchievement', backref='achievement', lazy=True)
    
    def __repr__(self):
        return f'<Achievement {self.name}>'

class UserAchievement(db.Model):
    """Track user achievements"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'achievement_id', name='unique_user_achievement'),)
    
    def __repr__(self):
        return f'<UserAchievement User:{self.user_id} Achievement:{self.achievement_id}>'
