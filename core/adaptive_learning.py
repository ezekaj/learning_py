#!/usr/bin/env python3
"""
Adaptive Learning System
Implements personalized learning paths, difficulty adjustment, and spaced repetition
"""

import math
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .error_handler import error_handler

class DifficultyLevel(Enum):
    """Difficulty levels for adaptive learning"""
    VERY_EASY = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5

class LearningStyle(Enum):
    """Learning style preferences"""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING = "reading"

@dataclass
class LearningItem:
    """Represents a learning item (lesson, challenge, quiz)"""
    id: str
    title: str
    type: str  # lesson, challenge, quiz
    difficulty: DifficultyLevel
    prerequisites: List[str]
    concepts: List[str]
    estimated_time: int  # minutes
    learning_styles: List[LearningStyle]

@dataclass
class UserPerformance:
    """User performance data for a learning item"""
    item_id: str
    attempts: int
    success_rate: float
    average_time: float
    last_attempt: datetime
    mastery_level: float  # 0.0 to 1.0

class AdaptiveDifficultyEngine:
    """Adjusts difficulty based on user performance"""
    
    def __init__(self):
        self.performance_window = 5  # Consider last 5 attempts
        self.difficulty_adjustment_threshold = 0.1
        
    def calculate_user_skill_level(self, performances: List[UserPerformance]) -> float:
        """Calculate user's current skill level (0.0 to 1.0)"""
        if not performances:
            return 0.0
        
        # Weight recent performances more heavily
        weighted_sum = 0.0
        weight_sum = 0.0
        
        for i, perf in enumerate(performances[-self.performance_window:]):
            weight = math.exp(-0.1 * (len(performances) - i - 1))  # Exponential decay
            weighted_sum += perf.mastery_level * weight
            weight_sum += weight
        
        return weighted_sum / weight_sum if weight_sum > 0 else 0.0
    
    def suggest_difficulty(self, user_skill: float, current_difficulty: DifficultyLevel) -> DifficultyLevel:
        """Suggest appropriate difficulty level"""
        # Map skill level to difficulty
        if user_skill < 0.3:
            target_difficulty = DifficultyLevel.VERY_EASY
        elif user_skill < 0.5:
            target_difficulty = DifficultyLevel.EASY
        elif user_skill < 0.7:
            target_difficulty = DifficultyLevel.MEDIUM
        elif user_skill < 0.9:
            target_difficulty = DifficultyLevel.HARD
        else:
            target_difficulty = DifficultyLevel.VERY_HARD
        
        # Gradual adjustment - don't jump more than one level
        current_value = current_difficulty.value
        target_value = target_difficulty.value
        
        if abs(target_value - current_value) <= 1:
            return target_difficulty
        elif target_value > current_value:
            return DifficultyLevel(current_value + 1)
        else:
            return DifficultyLevel(current_value - 1)
    
    def calculate_mastery_level(self, success_rate: float, attempts: int, time_efficiency: float) -> float:
        """Calculate mastery level for a learning item"""
        # Base mastery from success rate
        base_mastery = success_rate
        
        # Confidence factor based on number of attempts
        confidence = min(1.0, attempts / 3.0)  # Full confidence after 3 attempts
        
        # Time efficiency factor (1.0 = average time, >1.0 = faster than average)
        time_factor = min(1.0, time_efficiency)
        
        # Combined mastery score
        mastery = base_mastery * confidence * (0.7 + 0.3 * time_factor)
        
        return min(1.0, mastery)

class SpacedRepetitionEngine:
    """Implements spaced repetition algorithm for optimal review timing"""
    
    def __init__(self):
        self.initial_interval = 1  # days
        self.ease_factor = 2.5
        self.min_ease_factor = 1.3
        self.max_ease_factor = 3.0
        
    def calculate_next_review(self, performance: UserPerformance, quality: int) -> datetime:
        """
        Calculate next review date based on performance
        Quality: 0-5 scale (0=complete failure, 5=perfect recall)
        """
        if quality < 3:
            # Failed recall - reset interval
            interval = self.initial_interval
            ease_factor = max(self.min_ease_factor, performance.mastery_level * 2.5 - 0.8)
        else:
            # Successful recall - increase interval
            if performance.attempts == 1:
                interval = 1
            elif performance.attempts == 2:
                interval = 6
            else:
                # Use spaced repetition formula
                previous_interval = self._get_previous_interval(performance)
                ease_factor = self._calculate_ease_factor(performance.mastery_level, quality)
                interval = previous_interval * ease_factor
        
        # Add some randomization to avoid clustering
        interval *= random.uniform(0.9, 1.1)
        
        return datetime.now() + timedelta(days=interval)
    
    def _get_previous_interval(self, performance: UserPerformance) -> float:
        """Get the previous review interval"""
        # Simplified - in practice, this would be stored
        return max(1, performance.attempts - 1)
    
    def _calculate_ease_factor(self, mastery_level: float, quality: int) -> float:
        """Calculate ease factor based on recall quality"""
        ease_adjustment = 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        new_ease = self.ease_factor + ease_adjustment
        return max(self.min_ease_factor, min(self.max_ease_factor, new_ease))

class PersonalizedLearningPath:
    """Creates personalized learning paths for users"""
    
    def __init__(self):
        self.learning_items = {}
        self.prerequisite_graph = {}
        
    def add_learning_item(self, item: LearningItem):
        """Add a learning item to the system"""
        self.learning_items[item.id] = item
        self._update_prerequisite_graph(item)
    
    def _update_prerequisite_graph(self, item: LearningItem):
        """Update the prerequisite dependency graph"""
        if item.id not in self.prerequisite_graph:
            self.prerequisite_graph[item.id] = {
                'prerequisites': item.prerequisites,
                'dependents': []
            }
        
        # Update dependents for prerequisites
        for prereq_id in item.prerequisites:
            if prereq_id in self.prerequisite_graph:
                self.prerequisite_graph[prereq_id]['dependents'].append(item.id)
    
    def generate_learning_path(self, user_id: str, user_goals: List[str], 
                             user_performances: List[UserPerformance],
                             learning_style: LearningStyle) -> List[str]:
        """Generate personalized learning path"""
        # Get user's current skill level
        skill_level = self._calculate_overall_skill_level(user_performances)
        
        # Find completed items
        completed_items = {perf.item_id for perf in user_performances 
                          if perf.mastery_level >= 0.8}
        
        # Find available items (prerequisites met)
        available_items = self._get_available_items(completed_items)
        
        # Filter by learning style preference
        style_filtered = self._filter_by_learning_style(available_items, learning_style)
        
        # Sort by relevance to goals and difficulty
        sorted_items = self._sort_by_relevance(style_filtered, user_goals, skill_level)
        
        # Create optimal sequence
        learning_path = self._create_optimal_sequence(sorted_items, user_goals)
        
        return learning_path
    
    def _calculate_overall_skill_level(self, performances: List[UserPerformance]) -> float:
        """Calculate user's overall skill level"""
        if not performances:
            return 0.0
        
        return sum(perf.mastery_level for perf in performances) / len(performances)
    
    def _get_available_items(self, completed_items: set) -> List[str]:
        """Get items that are available (prerequisites met)"""
        available = []
        
        for item_id, item in self.learning_items.items():
            if item_id in completed_items:
                continue
            
            # Check if all prerequisites are completed
            if all(prereq in completed_items for prereq in item.prerequisites):
                available.append(item_id)
        
        return available
    
    def _filter_by_learning_style(self, item_ids: List[str], 
                                 learning_style: LearningStyle) -> List[str]:
        """Filter items by learning style preference"""
        filtered = []
        
        for item_id in item_ids:
            item = self.learning_items[item_id]
            if learning_style in item.learning_styles:
                filtered.append(item_id)
        
        # If no items match the preferred style, return all items
        return filtered if filtered else item_ids
    
    def _sort_by_relevance(self, item_ids: List[str], user_goals: List[str], 
                          skill_level: float) -> List[str]:
        """Sort items by relevance to user goals and appropriate difficulty"""
        def relevance_score(item_id: str) -> float:
            item = self.learning_items[item_id]
            
            # Goal relevance (how many concepts match user goals)
            goal_relevance = len(set(item.concepts) & set(user_goals)) / max(len(user_goals), 1)
            
            # Difficulty appropriateness
            difficulty_diff = abs(item.difficulty.value / 5.0 - skill_level)
            difficulty_score = 1.0 - difficulty_diff
            
            # Combine scores
            return 0.7 * goal_relevance + 0.3 * difficulty_score
        
        return sorted(item_ids, key=relevance_score, reverse=True)
    
    def _create_optimal_sequence(self, sorted_items: List[str], 
                               user_goals: List[str]) -> List[str]:
        """Create optimal learning sequence"""
        # Simple greedy approach - in practice, use more sophisticated algorithms
        sequence = []
        remaining_items = set(sorted_items)
        
        while remaining_items:
            # Find the best next item
            best_item = None
            best_score = -1
            
            for item_id in remaining_items:
                item = self.learning_items[item_id]
                
                # Check if prerequisites are in sequence
                prereqs_met = all(prereq in sequence for prereq in item.prerequisites)
                
                if prereqs_met:
                    # Calculate priority score
                    goal_match = len(set(item.concepts) & set(user_goals))
                    priority_score = goal_match + (1 / (item.difficulty.value + 1))
                    
                    if priority_score > best_score:
                        best_score = priority_score
                        best_item = item_id
            
            if best_item:
                sequence.append(best_item)
                remaining_items.remove(best_item)
            else:
                # No valid next item - add any remaining item
                sequence.extend(list(remaining_items))
                break
        
        return sequence

class LearningAnalytics:
    """Provides learning analytics and insights"""
    
    def __init__(self):
        self.analytics_cache = {}
    
    def generate_user_analytics(self, user_id: str, 
                               performances: List[UserPerformance]) -> Dict[str, Any]:
        """Generate comprehensive learning analytics for user"""
        if not performances:
            return {"error": "No performance data available"}
        
        # Learning velocity
        velocity = self._calculate_learning_velocity(performances)
        
        # Strength and weakness analysis
        strengths, weaknesses = self._analyze_strengths_weaknesses(performances)
        
        # Progress trends
        trends = self._calculate_progress_trends(performances)
        
        # Retention analysis
        retention = self._analyze_retention(performances)
        
        # Recommendations
        recommendations = self._generate_recommendations(performances)
        
        return {
            "user_id": user_id,
            "learning_velocity": velocity,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "trends": trends,
            "retention": retention,
            "recommendations": recommendations,
            "generated_at": datetime.now().isoformat()
        }
    
    def _calculate_learning_velocity(self, performances: List[UserPerformance]) -> Dict[str, float]:
        """Calculate how quickly user is learning"""
        if len(performances) < 2:
            return {"items_per_day": 0.0, "mastery_rate": 0.0}
        
        # Sort by last attempt
        sorted_perfs = sorted(performances, key=lambda p: p.last_attempt)
        
        # Calculate time span
        time_span = (sorted_perfs[-1].last_attempt - sorted_perfs[0].last_attempt).days
        if time_span == 0:
            time_span = 1
        
        # Items completed per day
        items_per_day = len(performances) / time_span
        
        # Average mastery rate
        mastery_rate = sum(p.mastery_level for p in performances) / len(performances)
        
        return {
            "items_per_day": items_per_day,
            "mastery_rate": mastery_rate
        }
    
    def _analyze_strengths_weaknesses(self, performances: List[UserPerformance]) -> Tuple[List[str], List[str]]:
        """Analyze user's strengths and weaknesses"""
        # Group by concept/topic (simplified)
        concept_performance = {}
        
        for perf in performances:
            # In practice, map items to concepts
            concept = perf.item_id.split('_')[0]  # Simplified concept extraction
            
            if concept not in concept_performance:
                concept_performance[concept] = []
            concept_performance[concept].append(perf.mastery_level)
        
        # Calculate average performance per concept
        concept_averages = {
            concept: sum(scores) / len(scores)
            for concept, scores in concept_performance.items()
        }
        
        # Identify strengths (top 30%) and weaknesses (bottom 30%)
        sorted_concepts = sorted(concept_averages.items(), key=lambda x: x[1], reverse=True)
        
        num_concepts = len(sorted_concepts)
        strength_count = max(1, num_concepts // 3)
        weakness_count = max(1, num_concepts // 3)
        
        strengths = [concept for concept, _ in sorted_concepts[:strength_count]]
        weaknesses = [concept for concept, _ in sorted_concepts[-weakness_count:]]
        
        return strengths, weaknesses
    
    def _calculate_progress_trends(self, performances: List[UserPerformance]) -> Dict[str, Any]:
        """Calculate learning progress trends"""
        if len(performances) < 3:
            return {"trend": "insufficient_data"}
        
        # Sort by attempt date
        sorted_perfs = sorted(performances, key=lambda p: p.last_attempt)
        
        # Calculate moving average of mastery levels
        window_size = min(5, len(sorted_perfs))
        moving_averages = []
        
        for i in range(window_size - 1, len(sorted_perfs)):
            window = sorted_perfs[i - window_size + 1:i + 1]
            avg = sum(p.mastery_level for p in window) / window_size
            moving_averages.append(avg)
        
        # Determine trend
        if len(moving_averages) >= 2:
            trend_slope = moving_averages[-1] - moving_averages[0]
            if trend_slope > 0.1:
                trend = "improving"
            elif trend_slope < -0.1:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"
        
        return {
            "trend": trend,
            "current_level": moving_averages[-1] if moving_averages else 0.0,
            "improvement_rate": trend_slope if 'trend_slope' in locals() else 0.0
        }
    
    def _analyze_retention(self, performances: List[UserPerformance]) -> Dict[str, Any]:
        """Analyze knowledge retention"""
        # Simplified retention analysis
        recent_performances = [p for p in performances 
                             if (datetime.now() - p.last_attempt).days <= 30]
        
        if not recent_performances:
            return {"retention_rate": 0.0, "items_at_risk": []}
        
        # Items that need review (low recent performance)
        items_at_risk = [p.item_id for p in recent_performances 
                        if p.mastery_level < 0.6]
        
        retention_rate = 1.0 - (len(items_at_risk) / len(recent_performances))
        
        return {
            "retention_rate": retention_rate,
            "items_at_risk": items_at_risk,
            "review_recommended": len(items_at_risk) > 0
        }
    
    def _generate_recommendations(self, performances: List[UserPerformance]) -> List[str]:
        """Generate personalized learning recommendations"""
        recommendations = []
        
        # Calculate overall performance
        avg_mastery = sum(p.mastery_level for p in performances) / len(performances)
        
        if avg_mastery < 0.5:
            recommendations.append("Focus on fundamentals - consider reviewing basic concepts")
        elif avg_mastery > 0.8:
            recommendations.append("Great progress! Ready for more challenging content")
        
        # Check for consistency
        mastery_variance = sum((p.mastery_level - avg_mastery) ** 2 for p in performances) / len(performances)
        
        if mastery_variance > 0.2:
            recommendations.append("Consider focusing on weaker areas for more consistent progress")
        
        # Check recent activity
        recent_activity = [p for p in performances 
                          if (datetime.now() - p.last_attempt).days <= 7]
        
        if len(recent_activity) < 3:
            recommendations.append("Try to maintain regular study sessions for better retention")
        
        return recommendations

# Global instances
adaptive_engine = AdaptiveDifficultyEngine()
spaced_repetition = SpacedRepetitionEngine()
learning_path_generator = PersonalizedLearningPath()
learning_analytics = LearningAnalytics()
