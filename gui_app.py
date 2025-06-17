#!/usr/bin/env python3
"""
Beautiful GUI for Python Learning Program
Inspired by top educational platforms: Duolingo, Codecademy, Khan Academy, FreeCodeCamp, Coursera
Features: Modern design, dark/light mode, gamification, progress tracking, animations
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import threading
import time

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ModernProgressBar(ctk.CTkFrame):
    """Custom animated progress bar with percentage"""
    
    def __init__(self, parent, width=300, height=20, **kwargs):
        super().__init__(parent, width=width, height=height, **kwargs)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ctk.CTkProgressBar(
            self, 
            width=width-40, 
            height=height-4,
            progress_color=("#1f538d", "#14375e"),
            fg_color=("#d0d0d0", "#404040")
        )
        self.progress_bar.pack(side="left", padx=5, pady=2)
        
        self.percentage_label = ctk.CTkLabel(
            self, 
            text="0%", 
            font=ctk.CTkFont(size=12, weight="bold"),
            width=30
        )
        self.percentage_label.pack(side="right", padx=5)
    
    def set_progress(self, value):
        """Set progress value (0.0 to 1.0)"""
        self.progress_bar.set(value)
        percentage = int(value * 100)
        self.percentage_label.configure(text=f"{percentage}%")
    
    def animate_to(self, target_value, duration=1.0):
        """Animate progress to target value"""
        current_value = self.progress_bar.get()
        steps = 30
        step_size = (target_value - current_value) / steps
        step_duration = duration / steps
        
        def animate_step(step):
            if step <= steps:
                new_value = current_value + (step_size * step)
                self.set_progress(new_value)
                self.after(int(step_duration * 1000), lambda: animate_step(step + 1))
        
        animate_step(1)

class AchievementCard(ctk.CTkFrame):
    """Beautiful achievement card widget"""
    
    def __init__(self, parent, title, description, icon, points, unlocked=False, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.unlocked = unlocked
        
        # Configure colors based on unlock status
        if unlocked:
            bg_color = ("#f0f8ff", "#1a1a2e")
            text_color = ("#000000", "#ffffff")
            icon_color = "#ffd700"  # Gold
        else:
            bg_color = ("#f5f5f5", "#2a2a2a")
            text_color = ("#666666", "#888888")
            icon_color = "#cccccc"  # Gray
        
        self.configure(fg_color=bg_color)
        
        # Icon
        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=24),
            text_color=icon_color,
            width=50,
            height=50
        )
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="w")
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=text_color,
            anchor="w"
        )
        self.title_label.grid(row=0, column=1, padx=5, pady=(10, 2), sticky="ew")
        
        # Description
        self.desc_label = ctk.CTkLabel(
            self,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=text_color,
            anchor="w",
            wraplength=200
        )
        self.desc_label.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="ew")
        
        # Points
        self.points_label = ctk.CTkLabel(
            self,
            text=f"{points}pts",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=("#ff6b35", "#ff8c42") if unlocked else text_color,
            width=50
        )
        self.points_label.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        
        self.grid_columnconfigure(1, weight=1)

class LessonCard(ctk.CTkFrame):
    """Interactive lesson card with progress"""
    
    def __init__(self, parent, lesson_data, on_click=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.lesson_data = lesson_data
        self.on_click = on_click
        
        # Configure hover effects
        self.configure(cursor="hand2")
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Lesson title
        self.title_label = ctk.CTkLabel(
            self,
            text=lesson_data.get("title", "Unknown Lesson"),
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w"
        )
        self.title_label.pack(fill="x", padx=15, pady=(15, 5))
        
        # Description
        self.desc_label = ctk.CTkLabel(
            self,
            text=lesson_data.get("description", ""),
            font=ctk.CTkFont(size=12),
            anchor="w",
            wraplength=300,
            justify="left"
        )
        self.desc_label.pack(fill="x", padx=15, pady=(0, 10))
        
        # Progress and stats frame
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Difficulty badge
        difficulty = lesson_data.get("difficulty", "beginner")
        difficulty_colors = {
            "beginner": "#4CAF50",
            "intermediate": "#FF9800", 
            "advanced": "#F44336",
            "expert": "#9C27B0"
        }
        
        self.difficulty_badge = ctk.CTkLabel(
            stats_frame,
            text=difficulty.title(),
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=difficulty_colors.get(difficulty, "#4CAF50"),
            corner_radius=10,
            width=80,
            height=20
        )
        self.difficulty_badge.pack(side="left", padx=(0, 10))
        
        # Time estimate
        time_est = lesson_data.get("estimated_time", 60)
        self.time_label = ctk.CTkLabel(
            stats_frame,
            text=f"⏱️ {time_est}min",
            font=ctk.CTkFont(size=11),
            text_color=("#666666", "#aaaaaa")
        )
        self.time_label.pack(side="left", padx=(0, 10))
        
        # Exercise count
        exercises = lesson_data.get("exercises", 0)
        self.exercise_label = ctk.CTkLabel(
            stats_frame,
            text=f"📝 {exercises} exercises",
            font=ctk.CTkFont(size=11),
            text_color=("#666666", "#aaaaaa")
        )
        self.exercise_label.pack(side="left")
        
        # Completion status
        completed = lesson_data.get("completed", False)
        if completed:
            self.status_label = ctk.CTkLabel(
                stats_frame,
                text="✅ Completed",
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color="#4CAF50"
            )
            self.status_label.pack(side="right")
    
    def _on_click(self, event):
        if self.on_click:
            self.on_click(self.lesson_data)
    
    def _on_enter(self, event):
        self.configure(fg_color=("#e8f4fd", "#1a1a2e"))
    
    def _on_leave(self, event):
        self.configure(fg_color=("gray90", "gray13"))

class PythonLearningGUI:
    """Main GUI Application"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🐍 Python Learning Program - From Beginner to Expert")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Initialize data
        self.current_user = None
        self.user_data = {}
        self.load_user_data()
        
        # Create main interface
        self.setup_main_layout()
        self.create_sidebar()
        self.create_main_content()
        
        # Show welcome screen if no user
        if not self.current_user:
            self.show_welcome_screen()
        else:
            self.show_dashboard()
    
    def setup_main_layout(self):
        """Setup the main layout structure"""
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Create main frames
        self.sidebar_frame = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
    
    def create_sidebar(self):
        """Create the beautiful sidebar navigation"""
        # Logo and title
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=20)
        
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🐍",
            font=ctk.CTkFont(size=32)
        )
        logo_label.pack()
        
        title_label = ctk.CTkLabel(
            logo_frame,
            text="Python Learning",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=(5, 0))
        
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="Beginner to Expert",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        subtitle_label.pack()
        
        # User info (if logged in)
        if self.current_user:
            self.create_user_info_sidebar()
        
        # Navigation buttons
        nav_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        nav_buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📚 Lessons", self.show_lessons),
            ("🎮 Challenges", self.show_challenges),
            ("🧪 Playground", self.show_playground),
            ("🎯 Quizzes", self.show_quizzes),
            ("📊 Progress", self.show_progress),
            ("🏆 Achievements", self.show_achievements),
            ("⚙️ Settings", self.show_settings)
        ]
        
        self.nav_buttons = {}
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                height=40,
                anchor="w",
                font=ctk.CTkFont(size=14),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray20")
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[text] = btn
        
        # Theme toggle
        theme_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        theme_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="🌙 Dark Mode",
            command=self.toggle_theme,
            font=ctk.CTkFont(size=12)
        )
        self.theme_switch.pack()
        self.theme_switch.select() if ctk.get_appearance_mode() == "Dark" else self.theme_switch.deselect()
    
    def create_user_info_sidebar(self):
        """Create user info section in sidebar"""
        user_frame = ctk.CTkFrame(self.sidebar_frame)
        user_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # User avatar (using emoji)
        avatar_label = ctk.CTkLabel(
            user_frame,
            text="👤",
            font=ctk.CTkFont(size=24)
        )
        avatar_label.pack(pady=(15, 5))
        
        # User name
        name_label = ctk.CTkLabel(
            user_frame,
            text=self.current_user,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack()
        
        # User stats
        user_profile = self.user_data.get(self.current_user, {})
        level = self.calculate_level(user_profile.get("points", 0))
        
        stats_label = ctk.CTkLabel(
            user_frame,
            text=f"Level {level} • {user_profile.get('points', 0)} pts",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray70")
        )
        stats_label.pack(pady=(0, 15))
    
    def create_main_content(self):
        """Create the main content area"""
        # Header
        self.header_frame = ctk.CTkFrame(self.main_frame, height=80, corner_radius=10)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.header_frame.pack_propagate(False)
        
        # Content area
        self.content_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def show_welcome_screen(self):
        """Show welcome screen for new users"""
        self.clear_content()
        
        # Welcome header
        welcome_label = ctk.CTkLabel(
            self.content_frame,
            text="🎉 Welcome to Python Learning Program!",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        welcome_label.pack(pady=(40, 20))
        
        subtitle_label = ctk.CTkLabel(
            self.content_frame,
            text="Your journey from beginner to expert starts here",
            font=ctk.CTkFont(size=16),
            text_color=("gray50", "gray70")
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Features showcase
        features_frame = ctk.CTkFrame(self.content_frame)
        features_frame.pack(fill="x", pady=20)
        
        features_title = ctk.CTkLabel(
            features_frame,
            text="✨ What You'll Get",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        features_title.pack(pady=(20, 15))
        
        features = [
            "📚 Structured lessons from beginner to expert",
            "🎮 Interactive coding challenges",
            "🧪 Safe code playground for experimentation", 
            "🎯 Comprehensive quizzes with instant feedback",
            "🏆 Achievement system to track your progress",
            "📊 Detailed analytics and progress tracking"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(
                features_frame,
                text=feature,
                font=ctk.CTkFont(size=14),
                anchor="w"
            )
            feature_label.pack(fill="x", padx=40, pady=5)
        
        # Get started button
        start_button = ctk.CTkButton(
            self.content_frame,
            text="🚀 Get Started",
            command=self.show_user_setup,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#1f538d", "#14375e"),
            hover_color=("#14375e", "#0d2a4a")
        )
        start_button.pack(pady=40)
    
    def show_user_setup(self):
        """Show user setup dialog"""
        dialog = UserSetupDialog(self.root, self.on_user_created)
    
    def on_user_created(self, user_data):
        """Callback when user is created"""
        self.current_user = user_data["name"]
        self.user_data[self.current_user] = user_data
        self.save_user_data()
        
        # Refresh sidebar and show dashboard
        self.create_sidebar()
        self.show_dashboard()
    
    def show_dashboard(self):
        """Show the main dashboard"""
        self.clear_content()
        self.update_header("🏠 Dashboard", "Your learning overview")
        
        if not self.current_user:
            self.show_welcome_screen()
            return
        
        user_profile = self.user_data.get(self.current_user, {})
        
        # Stats cards row
        stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        stats_frame.pack(fill="x", pady=20)
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Create stat cards
        stats = [
            ("Level", self.calculate_level(user_profile.get("points", 0)), "🏆"),
            ("Points", user_profile.get("points", 0), "💎"),
            ("Streak", user_profile.get("streak", 0), "🔥"),
            ("Lessons", len(user_profile.get("completed_lessons", [])), "📚")
        ]
        
        for i, (title, value, icon) in enumerate(stats):
            self.create_stat_card(stats_frame, title, value, icon, i)
        
        # Progress section
        progress_frame = ctk.CTkFrame(self.content_frame)
        progress_frame.pack(fill="x", pady=20)
        
        progress_title = ctk.CTkLabel(
            progress_frame,
            text="📈 Your Progress",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        progress_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Overall progress bar
        overall_progress = ModernProgressBar(progress_frame, width=400)
        overall_progress.pack(padx=20, pady=10)
        
        # Calculate and animate progress
        total_lessons = 30  # Example total
        completed = len(user_profile.get("completed_lessons", []))
        progress_value = completed / total_lessons if total_lessons > 0 else 0
        overall_progress.animate_to(progress_value)
        
        # Recent achievements
        self.show_recent_achievements(user_profile)
        
        # Quick actions
        self.show_quick_actions()
    
    def create_stat_card(self, parent, title, value, icon, column):
        """Create a beautiful stat card"""
        card = ctk.CTkFrame(parent)
        card.grid(row=0, column=column, padx=10, pady=10, sticky="ew")
        
        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=ctk.CTkFont(size=24)
        )
        icon_label.pack(pady=(15, 5))
        
        value_label = ctk.CTkLabel(
            card,
            text=str(value),
            font=ctk.CTkFont(size=20, weight="bold")
        )
        value_label.pack()
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray70")
        )
        title_label.pack(pady=(0, 15))
    
    def show_recent_achievements(self, user_profile):
        """Show recent achievements section"""
        achievements_frame = ctk.CTkFrame(self.content_frame)
        achievements_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(
            achievements_frame,
            text="🏆 Recent Achievements",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Show recent achievements (placeholder)
        recent_achievements = user_profile.get("achievements", [])[-3:]  # Last 3
        
        if recent_achievements:
            for achievement_id in recent_achievements:
                # Create achievement card (simplified for demo)
                achievement_card = ctk.CTkFrame(achievements_frame)
                achievement_card.pack(fill="x", padx=20, pady=5)
                
                achievement_label = ctk.CTkLabel(
                    achievement_card,
                    text=f"🎉 {achievement_id.replace('_', ' ').title()}",
                    font=ctk.CTkFont(size=14)
                )
                achievement_label.pack(pady=10)
        else:
            no_achievements = ctk.CTkLabel(
                achievements_frame,
                text="Complete lessons to unlock achievements!",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray70")
            )
            no_achievements.pack(padx=20, pady=10)
    
    def show_quick_actions(self):
        """Show quick action buttons"""
        actions_frame = ctk.CTkFrame(self.content_frame)
        actions_frame.pack(fill="x", pady=20)
        
        title = ctk.CTkLabel(
            actions_frame,
            text="⚡ Quick Actions",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title.pack(anchor="w", padx=20, pady=(20, 10))
        
        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        actions = [
            ("📚 Continue Learning", self.show_lessons, "#4CAF50"),
            ("🎮 Take Challenge", self.show_challenges, "#FF9800"),
            ("🧪 Open Playground", self.show_playground, "#2196F3"),
            ("🎯 Take Quiz", self.show_quizzes, "#9C27B0")
        ]
        
        for i, (text, command, color) in enumerate(actions):
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                command=command,
                height=40,
                font=ctk.CTkFont(size=14),
                fg_color=color,
                hover_color=self.darken_color(color)
            )
            btn.pack(side="left", expand=True, fill="x", padx=5)
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        # Simple darkening by reducing RGB values
        if color.startswith("#"):
            r = int(color[1:3], 16)
            g = int(color[3:5], 16) 
            b = int(color[5:7], 16)
            
            r = max(0, r - 30)
            g = max(0, g - 30)
            b = max(0, b - 30)
            
            return f"#{r:02x}{g:02x}{b:02x}"
        return color
