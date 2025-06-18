#!/usr/bin/env python3
"""
Social Learning System
Implements collaboration features, user profiles, and peer learning
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from .error_handler import error_handler
from .database_manager import db_manager

class FriendshipStatus(Enum):
    """Friendship status types"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"

class PostType(Enum):
    """Discussion post types"""
    QUESTION = "question"
    ANSWER = "answer"
    DISCUSSION = "discussion"
    CODE_SHARE = "code_share"
    ACHIEVEMENT = "achievement"

@dataclass
class UserProfile:
    """Extended user profile for social features"""
    user_id: str
    display_name: str
    bio: str
    avatar_url: str
    learning_goals: List[str]
    skills: List[str]
    achievements: List[str]
    reputation: int
    join_date: str
    last_active: str
    privacy_settings: Dict[str, bool]
    social_stats: Dict[str, int]

@dataclass
class Friendship:
    """Friendship relationship between users"""
    id: str
    requester_id: str
    recipient_id: str
    status: FriendshipStatus
    created_at: str
    updated_at: str

@dataclass
class DiscussionPost:
    """Discussion forum post"""
    id: str
    author_id: str
    title: str
    content: str
    post_type: PostType
    tags: List[str]
    parent_id: Optional[str]  # For replies
    votes: int
    created_at: str
    updated_at: str
    is_solved: bool

@dataclass
class CodeShare:
    """Shared code snippet"""
    id: str
    author_id: str
    title: str
    description: str
    code: str
    language: str
    tags: List[str]
    votes: int
    comments: List[str]
    created_at: str
    is_public: bool

class SocialLearningManager:
    """Manages social learning features"""
    
    def __init__(self, data_dir: str = "data/social"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        self.profiles_file = os.path.join(data_dir, "user_profiles.json")
        self.friendships_file = os.path.join(data_dir, "friendships.json")
        self.discussions_file = os.path.join(data_dir, "discussions.json")
        self.code_shares_file = os.path.join(data_dir, "code_shares.json")
        
        # Initialize data structures
        self.user_profiles = self._load_data(self.profiles_file, {})
        self.friendships = self._load_data(self.friendships_file, {})
        self.discussions = self._load_data(self.discussions_file, {})
        self.code_shares = self._load_data(self.code_shares_file, {})
    
    def _load_data(self, file_path: str, default: Any) -> Any:
        """Load data from file with error handling"""
        try:
            return db_manager.safe_read(file_path) or default
        except Exception as e:
            error_handler.logger.warning(f"Failed to load {file_path}: {e}")
            return default
    
    def _save_data(self, file_path: str, data: Any) -> bool:
        """Save data to file with error handling"""
        try:
            return db_manager.safe_write(file_path, data)
        except Exception as e:
            error_handler.logger.error(f"Failed to save {file_path}: {e}")
            return False
    
    def create_user_profile(self, user_id: str, display_name: str, 
                           bio: str = "", learning_goals: List[str] = None) -> UserProfile:
        """Create a new user profile"""
        profile = UserProfile(
            user_id=user_id,
            display_name=display_name,
            bio=bio,
            avatar_url="",
            learning_goals=learning_goals or [],
            skills=[],
            achievements=[],
            reputation=0,
            join_date=datetime.now().isoformat(),
            last_active=datetime.now().isoformat(),
            privacy_settings={
                "show_progress": True,
                "show_achievements": True,
                "allow_friend_requests": True,
                "show_online_status": True
            },
            social_stats={
                "friends_count": 0,
                "posts_count": 0,
                "helpful_answers": 0,
                "code_shares": 0
            }
        )
        
        self.user_profiles[user_id] = asdict(profile)
        self._save_data(self.profiles_file, self.user_profiles)
        
        return profile
    
    def get_user_profile(self, user_id: str) -> Optional[UserProfile]:
        """Get user profile by ID"""
        profile_data = self.user_profiles.get(user_id)
        if profile_data:
            return UserProfile(**profile_data)
        return None
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user profile"""
        if user_id not in self.user_profiles:
            return False
        
        # Update allowed fields
        allowed_fields = ['display_name', 'bio', 'avatar_url', 'learning_goals', 
                         'skills', 'privacy_settings']
        
        for field, value in updates.items():
            if field in allowed_fields:
                self.user_profiles[user_id][field] = value
        
        self.user_profiles[user_id]['last_active'] = datetime.now().isoformat()
        return self._save_data(self.profiles_file, self.user_profiles)
    
    def send_friend_request(self, requester_id: str, recipient_id: str) -> bool:
        """Send a friend request"""
        # Check if users exist
        if (requester_id not in self.user_profiles or 
            recipient_id not in self.user_profiles):
            return False
        
        # Check if friendship already exists
        existing = self._find_friendship(requester_id, recipient_id)
        if existing:
            return False
        
        # Create friendship request
        friendship_id = f"{requester_id}_{recipient_id}_{int(datetime.now().timestamp())}"
        friendship = Friendship(
            id=friendship_id,
            requester_id=requester_id,
            recipient_id=recipient_id,
            status=FriendshipStatus.PENDING,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        self.friendships[friendship_id] = asdict(friendship)
        return self._save_data(self.friendships_file, self.friendships)
    
    def respond_to_friend_request(self, friendship_id: str, accept: bool) -> bool:
        """Respond to a friend request"""
        if friendship_id not in self.friendships:
            return False
        
        friendship = self.friendships[friendship_id]
        
        if accept:
            friendship['status'] = FriendshipStatus.ACCEPTED.value
            # Update friend counts
            self._update_friend_count(friendship['requester_id'], 1)
            self._update_friend_count(friendship['recipient_id'], 1)
        else:
            # Remove the friendship request
            del self.friendships[friendship_id]
        
        friendship['updated_at'] = datetime.now().isoformat()
        return self._save_data(self.friendships_file, self.friendships)
    
    def get_friends(self, user_id: str) -> List[UserProfile]:
        """Get list of user's friends"""
        friends = []
        
        for friendship in self.friendships.values():
            if (friendship['status'] == FriendshipStatus.ACCEPTED.value and
                (friendship['requester_id'] == user_id or friendship['recipient_id'] == user_id)):
                
                friend_id = (friendship['recipient_id'] if friendship['requester_id'] == user_id 
                           else friendship['requester_id'])
                
                friend_profile = self.get_user_profile(friend_id)
                if friend_profile:
                    friends.append(friend_profile)
        
        return friends
    
    def get_friend_requests(self, user_id: str) -> List[Dict[str, Any]]:
        """Get pending friend requests for user"""
        requests = []
        
        for friendship in self.friendships.values():
            if (friendship['recipient_id'] == user_id and 
                friendship['status'] == FriendshipStatus.PENDING.value):
                
                requester_profile = self.get_user_profile(friendship['requester_id'])
                if requester_profile:
                    requests.append({
                        'friendship_id': friendship['id'],
                        'requester': asdict(requester_profile),
                        'created_at': friendship['created_at']
                    })
        
        return requests
    
    def create_discussion_post(self, author_id: str, title: str, content: str,
                             post_type: PostType, tags: List[str] = None,
                             parent_id: str = None) -> str:
        """Create a new discussion post"""
        post_id = f"post_{int(datetime.now().timestamp())}_{author_id}"
        
        post = DiscussionPost(
            id=post_id,
            author_id=author_id,
            title=title,
            content=content,
            post_type=post_type,
            tags=tags or [],
            parent_id=parent_id,
            votes=0,
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            is_solved=False
        )
        
        self.discussions[post_id] = asdict(post)
        
        # Update user stats
        self._update_user_stat(author_id, 'posts_count', 1)
        
        self._save_data(self.discussions_file, self.discussions)
        return post_id
    
    def get_discussion_posts(self, limit: int = 20, tags: List[str] = None,
                           post_type: PostType = None) -> List[Dict[str, Any]]:
        """Get discussion posts with filtering"""
        posts = []
        
        for post_data in self.discussions.values():
            # Filter by type
            if post_type and post_data['post_type'] != post_type.value:
                continue
            
            # Filter by tags
            if tags and not any(tag in post_data['tags'] for tag in tags):
                continue
            
            # Add author info
            author_profile = self.get_user_profile(post_data['author_id'])
            post_with_author = post_data.copy()
            post_with_author['author'] = asdict(author_profile) if author_profile else None
            
            posts.append(post_with_author)
        
        # Sort by creation date (newest first)
        posts.sort(key=lambda x: x['created_at'], reverse=True)
        
        return posts[:limit]
    
    def vote_on_post(self, post_id: str, user_id: str, vote_up: bool) -> bool:
        """Vote on a discussion post"""
        if post_id not in self.discussions:
            return False
        
        # In a full implementation, track individual votes to prevent duplicate voting
        vote_change = 1 if vote_up else -1
        self.discussions[post_id]['votes'] += vote_change
        self.discussions[post_id]['updated_at'] = datetime.now().isoformat()
        
        return self._save_data(self.discussions_file, self.discussions)
    
    def share_code(self, author_id: str, title: str, description: str,
                   code: str, language: str, tags: List[str] = None,
                   is_public: bool = True) -> str:
        """Share a code snippet"""
        share_id = f"code_{int(datetime.now().timestamp())}_{author_id}"
        
        code_share = CodeShare(
            id=share_id,
            author_id=author_id,
            title=title,
            description=description,
            code=code,
            language=language,
            tags=tags or [],
            votes=0,
            comments=[],
            created_at=datetime.now().isoformat(),
            is_public=is_public
        )
        
        self.code_shares[share_id] = asdict(code_share)
        
        # Update user stats
        self._update_user_stat(author_id, 'code_shares', 1)
        
        self._save_data(self.code_shares_file, self.code_shares)
        return share_id
    
    def get_code_shares(self, limit: int = 20, language: str = None,
                       tags: List[str] = None) -> List[Dict[str, Any]]:
        """Get public code shares"""
        shares = []
        
        for share_data in self.code_shares.values():
            if not share_data['is_public']:
                continue
            
            # Filter by language
            if language and share_data['language'] != language:
                continue
            
            # Filter by tags
            if tags and not any(tag in share_data['tags'] for tag in tags):
                continue
            
            # Add author info
            author_profile = self.get_user_profile(share_data['author_id'])
            share_with_author = share_data.copy()
            share_with_author['author'] = asdict(author_profile) if author_profile else None
            
            shares.append(share_with_author)
        
        # Sort by votes and creation date
        shares.sort(key=lambda x: (x['votes'], x['created_at']), reverse=True)
        
        return shares[:limit]
    
    def _find_friendship(self, user1_id: str, user2_id: str) -> Optional[Dict[str, Any]]:
        """Find existing friendship between two users"""
        for friendship in self.friendships.values():
            if ((friendship['requester_id'] == user1_id and friendship['recipient_id'] == user2_id) or
                (friendship['requester_id'] == user2_id and friendship['recipient_id'] == user1_id)):
                return friendship
        return None
    
    def _update_friend_count(self, user_id: str, change: int):
        """Update friend count for user"""
        if user_id in self.user_profiles:
            self.user_profiles[user_id]['social_stats']['friends_count'] += change
    
    def _update_user_stat(self, user_id: str, stat_name: str, change: int):
        """Update user social statistics"""
        if user_id in self.user_profiles:
            if 'social_stats' not in self.user_profiles[user_id]:
                self.user_profiles[user_id]['social_stats'] = {}
            
            current_value = self.user_profiles[user_id]['social_stats'].get(stat_name, 0)
            self.user_profiles[user_id]['social_stats'][stat_name] = current_value + change
            
            self._save_data(self.profiles_file, self.user_profiles)

# Global instance
social_manager = SocialLearningManager()
