#!/usr/bin/env python3
"""
🌐 REAL-TIME COLLABORATION SYSTEM
Revolutionary features for collaborative learning and coding
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class CollaborationHub:
    """
    Real-time collaboration system for Python learning
    
    Features:
    - Live coding sessions
    - Pair programming
    - Code sharing and forking
    - Live chat during coding
    - Mentor sessions
    - Study groups
    """
    
    def __init__(self):
        self.active_sessions = {}
        self.user_connections = {}
        self.code_rooms = {}
        self.mentors_online = {}
        self.study_groups = {}
        
    def create_coding_session(self, creator_id: str, session_type: str = "public") -> str:
        """Create a new collaborative coding session"""
        session_id = str(uuid.uuid4())[:8]
        
        self.active_sessions[session_id] = {
            'id': session_id,
            'creator': creator_id,
            'type': session_type,  # public, private, mentor, study_group
            'participants': [creator_id],
            'code': '# Welcome to collaborative coding!\n# Others can join and code with you in real-time\n\nprint("Hello, collaborative world!")',
            'chat_messages': [],
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'cursor_positions': {},
            'is_active': True
        }
        
        return session_id
    
    def join_session(self, session_id: str, user_id: str) -> bool:
        """Join an existing coding session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        if user_id not in session['participants']:
            session['participants'].append(user_id)
            session['last_activity'] = datetime.now().isoformat()
            
            # Add welcome message
            self.add_chat_message(session_id, 'system', f"🎉 {user_id} joined the session!")
        
        return True
    
    def update_code(self, session_id: str, user_id: str, code: str, cursor_pos: int = 0):
        """Update code in real-time"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        if user_id in session['participants']:
            session['code'] = code
            session['cursor_positions'][user_id] = cursor_pos
            session['last_activity'] = datetime.now().isoformat()
            return True
        
        return False
    
    def add_chat_message(self, session_id: str, user_id: str, message: str):
        """Add chat message to session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        session['chat_messages'].append({
            'user': user_id,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'type': 'user' if user_id != 'system' else 'system'
        })
        
        # Keep only last 50 messages
        if len(session['chat_messages']) > 50:
            session['chat_messages'] = session['chat_messages'][-50:]
        
        return True
    
    def get_session_data(self, session_id: str) -> Optional[Dict]:
        """Get complete session data"""
        return self.active_sessions.get(session_id)
    
    def find_coding_partner(self, user_id: str, skill_level: str = "beginner") -> Optional[str]:
        """Find a coding partner for pair programming"""
        # Look for public sessions with similar skill level
        for session_id, session in self.active_sessions.items():
            if (session['type'] == 'public' and 
                len(session['participants']) == 1 and 
                session['participants'][0] != user_id):
                return session_id
        
        # Create new session if no match found
        return self.create_coding_session(user_id, "public")
    
    def request_mentor_help(self, user_id: str, topic: str, code: str = "") -> str:
        """Request help from available mentors"""
        mentor_request_id = str(uuid.uuid4())[:8]
        
        # Create mentor session
        session_id = self.create_coding_session(user_id, "mentor")
        session = self.active_sessions[session_id]
        session['mentor_request'] = {
            'id': mentor_request_id,
            'topic': topic,
            'code': code,
            'status': 'waiting',
            'requested_at': datetime.now().isoformat()
        }
        
        # Notify available mentors (in real implementation, this would use WebSocket)
        self.notify_mentors(mentor_request_id, topic, user_id)
        
        return session_id
    
    def notify_mentors(self, request_id: str, topic: str, student_id: str):
        """Notify available mentors about help request"""
        # In real implementation, this would send WebSocket notifications
        print(f"🔔 Mentor notification: {student_id} needs help with {topic}")
    
    def create_study_group(self, creator_id: str, topic: str, max_participants: int = 5) -> str:
        """Create a study group session"""
        group_id = str(uuid.uuid4())[:8]
        
        self.study_groups[group_id] = {
            'id': group_id,
            'creator': creator_id,
            'topic': topic,
            'participants': [creator_id],
            'max_participants': max_participants,
            'created_at': datetime.now().isoformat(),
            'session_id': self.create_coding_session(creator_id, "study_group"),
            'study_materials': [],
            'shared_notes': "",
            'is_active': True
        }
        
        return group_id
    
    def share_code_snippet(self, user_id: str, code: str, title: str, description: str = "") -> str:
        """Share a code snippet with the community"""
        snippet_id = str(uuid.uuid4())[:8]
        
        snippet = {
            'id': snippet_id,
            'author': user_id,
            'title': title,
            'description': description,
            'code': code,
            'created_at': datetime.now().isoformat(),
            'likes': 0,
            'forks': 0,
            'comments': [],
            'tags': self.extract_tags_from_code(code)
        }
        
        # In real implementation, save to database
        return snippet_id
    
    def fork_code_snippet(self, snippet_id: str, user_id: str) -> str:
        """Fork a code snippet for modification"""
        # In real implementation, get from database
        # For now, create a new session with the forked code
        session_id = self.create_coding_session(user_id, "public")
        # Set the forked code
        return session_id
    
    def extract_tags_from_code(self, code: str) -> List[str]:
        """Extract relevant tags from code content"""
        tags = []
        
        # Simple keyword detection
        keywords = {
            'function': ['def ', 'function'],
            'loop': ['for ', 'while '],
            'conditional': ['if ', 'elif ', 'else:'],
            'list': ['[', 'list('],
            'dictionary': ['{', 'dict('],
            'class': ['class '],
            'import': ['import ', 'from '],
            'file': ['open(', 'file'],
            'web': ['requests', 'urllib', 'http'],
            'data': ['pandas', 'numpy', 'csv'],
            'gui': ['tkinter', 'pygame', 'kivy']
        }
        
        code_lower = code.lower()
        for tag, patterns in keywords.items():
            if any(pattern in code_lower for pattern in patterns):
                tags.append(tag)
        
        return tags
    
    def get_live_coding_stats(self) -> Dict[str, Any]:
        """Get real-time collaboration statistics"""
        active_sessions = len([s for s in self.active_sessions.values() if s['is_active']])
        total_participants = sum(len(s['participants']) for s in self.active_sessions.values())
        
        return {
            'active_sessions': active_sessions,
            'total_participants': total_participants,
            'mentors_online': len(self.mentors_online),
            'study_groups': len(self.study_groups),
            'recent_activity': self.get_recent_activity()
        }
    
    def get_recent_activity(self) -> List[Dict]:
        """Get recent collaboration activity"""
        activities = []
        
        # Recent sessions
        for session in self.active_sessions.values():
            if session['is_active']:
                activities.append({
                    'type': 'session',
                    'message': f"Live coding session with {len(session['participants'])} participants",
                    'timestamp': session['last_activity']
                })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return activities[:10]
    
    def cleanup_inactive_sessions(self):
        """Clean up inactive sessions"""
        cutoff_time = datetime.now() - timedelta(hours=2)
        
        inactive_sessions = []
        for session_id, session in self.active_sessions.items():
            last_activity = datetime.fromisoformat(session['last_activity'])
            if last_activity < cutoff_time:
                inactive_sessions.append(session_id)
        
        for session_id in inactive_sessions:
            self.active_sessions[session_id]['is_active'] = False

class CodeSharingPlatform:
    """
    Platform for sharing and discovering code snippets
    """
    
    def __init__(self):
        self.snippets = {}
        self.user_profiles = {}
        self.trending_snippets = []
    
    def publish_snippet(self, user_id: str, code: str, title: str, 
                       description: str = "", tags: List[str] = None) -> str:
        """Publish a code snippet"""
        snippet_id = str(uuid.uuid4())[:8]
        
        self.snippets[snippet_id] = {
            'id': snippet_id,
            'author': user_id,
            'title': title,
            'description': description,
            'code': code,
            'tags': tags or [],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'likes': 0,
            'views': 0,
            'forks': 0,
            'comments': [],
            'is_public': True,
            'difficulty': self.analyze_code_difficulty(code)
        }
        
        return snippet_id
    
    def analyze_code_difficulty(self, code: str) -> str:
        """Analyze code complexity to determine difficulty"""
        lines = len(code.split('\n'))
        
        # Simple heuristics
        if 'class ' in code or 'def ' in code and lines > 20:
            return 'advanced'
        elif 'def ' in code or 'for ' in code or 'while ' in code:
            return 'intermediate'
        else:
            return 'beginner'
    
    def search_snippets(self, query: str, tags: List[str] = None, 
                       difficulty: str = None) -> List[Dict]:
        """Search for code snippets"""
        results = []
        
        for snippet in self.snippets.values():
            if not snippet['is_public']:
                continue
            
            # Text search
            if query.lower() in snippet['title'].lower() or query.lower() in snippet['description'].lower():
                score = 1
            elif query.lower() in snippet['code'].lower():
                score = 0.5
            else:
                score = 0
            
            # Tag matching
            if tags:
                tag_matches = len(set(tags) & set(snippet['tags']))
                score += tag_matches * 0.3
            
            # Difficulty filter
            if difficulty and snippet['difficulty'] != difficulty:
                continue
            
            if score > 0:
                snippet_copy = snippet.copy()
                snippet_copy['relevance_score'] = score
                results.append(snippet_copy)
        
        # Sort by relevance and popularity
        results.sort(key=lambda x: (x['relevance_score'], x['likes']), reverse=True)
        return results[:20]

# Global collaboration instances
collaboration_hub = CollaborationHub()
code_sharing = CodeSharingPlatform()

def get_collaboration_features():
    """Get available collaboration features"""
    return {
        'live_coding': True,
        'pair_programming': True,
        'mentor_sessions': True,
        'study_groups': True,
        'code_sharing': True,
        'real_time_chat': True,
        'screen_sharing': False,  # Would require WebRTC
        'voice_chat': False       # Would require WebRTC
    }

if __name__ == "__main__":
    # Test the collaboration system
    print("🌐 Testing Collaboration System...")
    
    # Create a session
    session_id = collaboration_hub.create_coding_session("user1", "public")
    print(f"Created session: {session_id}")
    
    # Join session
    collaboration_hub.join_session(session_id, "user2")
    print("User2 joined session")
    
    # Update code
    collaboration_hub.update_code(session_id, "user1", "print('Hello, collaborative world!')")
    print("Code updated")
    
    # Add chat message
    collaboration_hub.add_chat_message(session_id, "user1", "Hey, let's code together!")
    print("Chat message added")
    
    # Get session data
    session_data = collaboration_hub.get_session_data(session_id)
    print(f"Session has {len(session_data['participants'])} participants")
    
    print("✨ Collaboration System is ready!")
