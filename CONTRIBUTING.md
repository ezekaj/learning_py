# Contributing to Python Learning Platform

Thank you for your interest in contributing to the Python Learning Platform! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Git
- Basic knowledge of Flask (for web development contributions)
- Understanding of Python programming concepts

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/learning_py.git
   cd learning_py
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Run tests**
   ```bash
   python -m pytest tests/
   ```

## 📝 Types of Contributions

### 1. Adding Lessons
Create new learning content in the `data/lessons/` directory.

**Lesson Structure:**
```json
{
  "id": "lesson_new",
  "title": "Your Lesson Title",
  "description": "Brief description of the lesson",
  "difficulty": "beginner|intermediate|advanced|expert",
  "estimated_time": 45,
  "objectives": [
    "Learning objective 1",
    "Learning objective 2"
  ],
  "content": {
    "introduction": "Lesson introduction text",
    "sections": [
      {
        "title": "Section Title",
        "content": "Section content with examples",
        "code_examples": ["print('Hello, World!')"]
      }
    ]
  }
}
```

### 2. Creating Challenges
Add coding challenges in the `data/challenges/` directory.

**Challenge Structure:**
```json
{
  "id": "challenge_new",
  "title": "Challenge Title",
  "description": "Problem description",
  "difficulty": "easy|medium|hard",
  "function_name": "solution_function",
  "test_cases": [
    {
      "input": [1, 2],
      "expected_output": 3,
      "description": "Test case description"
    }
  ],
  "hints": ["Hint 1", "Hint 2"]
}
```

### 3. Adding Quizzes
Create quiz questions in the `data/quizzes/` directory.

**Quiz Structure:**
```json
{
  "id": "quiz_new",
  "title": "Quiz Title",
  "difficulty": "beginner|intermediate|advanced",
  "questions": [
    {
      "type": "multiple_choice",
      "question": "What is the output of print(2 + 2)?",
      "options": ["3", "4", "5", "Error"],
      "correct_answer": 1,
      "explanation": "2 + 2 equals 4 in Python"
    }
  ]
}
```

### 4. Code Contributions

#### Code Style Guidelines
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

#### Example Function:
```python
def calculate_user_progress(user_email: str, lesson_ids: List[str]) -> Dict[str, Any]:
    """
    Calculate comprehensive progress statistics for a user.
    
    Args:
        user_email: User's email address
        lesson_ids: List of completed lesson IDs
        
    Returns:
        Dictionary containing progress statistics
        
    Raises:
        ValueError: If user_email is invalid
    """
    # Implementation here
    pass
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_progress_tracker.py

# Run with coverage
python -m pytest tests/ --cov=core --cov-report=html
```

### Writing Tests
- Add tests for all new functionality
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

**Example Test:**
```python
import pytest
from core.progress_tracker import ProgressTracker

def test_update_progress_valid_user():
    """Test progress update for valid user."""
    tracker = ProgressTracker()
    result = tracker.update_progress("test@example.com", "lesson_completed", {"lesson_id": "lesson_1"})
    assert result is True

def test_update_progress_invalid_user():
    """Test progress update for invalid user."""
    tracker = ProgressTracker()
    with pytest.raises(ValueError):
        tracker.update_progress("", "lesson_completed", {})
```

## 📖 Documentation

### Updating Documentation
- Update README.md for major changes
- Add docstrings to new functions and classes
- Update API documentation for interface changes
- Include examples in documentation

### Documentation Style
- Use clear, concise language
- Include code examples
- Explain the "why" not just the "what"
- Keep documentation up to date with code changes

## 🔄 Pull Request Process

### Before Submitting
1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation

3. **Test your changes**
   ```bash
   python -m pytest tests/
   python app.py  # Test the web interface
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

### Commit Message Format
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test additions
- `refactor:` for code refactoring
- `style:` for formatting changes

### Submitting Pull Request
1. Push your branch to your fork
2. Create a pull request on GitHub
3. Fill out the pull request template
4. Wait for review and address feedback

## 🐛 Reporting Issues

### Bug Reports
Include the following information:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages (if any)

### Feature Requests
- Describe the feature clearly
- Explain the use case
- Provide examples if possible
- Consider implementation complexity

## 💬 Community Guidelines

- Be respectful and inclusive
- Help others learn and grow
- Provide constructive feedback
- Follow the code of conduct
- Ask questions if you're unsure

## 📞 Getting Help

- 📖 Read the [Documentation](https://ezekaj.github.io/learning_py/documentation.html)
- 💬 Start a [Discussion](https://github.com/ezekaj/learning_py/discussions)
- 🐛 Check existing [Issues](https://github.com/ezekaj/learning_py/issues)
- 📧 Contact maintainers for complex questions

Thank you for contributing to the Python Learning Platform! 🐍✨
