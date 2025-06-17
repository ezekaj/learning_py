#!/usr/bin/env python3
"""
🎮 BUG HUNTING GAME - FIND AND FIX THE BUGS!
A fun way to learn debugging skills
"""

import random
import time

class BugHuntingGame:
    def __init__(self):
        self.score = 0
        self.level = 1
        self.bugs_found = 0
        
        # Collection of buggy code examples
        self.bug_challenges = [
            {
                "level": 1,
                "title": "Missing Colon",
                "buggy_code": """if x > 5
    print("Big number")""",
                "fixed_code": """if x > 5:
    print("Big number")""",
                "bug_type": "Syntax Error",
                "hint": "Look at the end of the if statement",
                "explanation": "Python requires a colon (:) after if statements"
            },
            {
                "level": 1,
                "title": "Mismatched Quotes",
                "buggy_code": """print("Hello World')""",
                "fixed_code": """print("Hello World")""",
                "bug_type": "Syntax Error", 
                "hint": "Check the quotation marks",
                "explanation": "Opening and closing quotes must match"
            },
            {
                "level": 1,
                "title": "Wrong Indentation",
                "buggy_code": """def greet():
print("Hello!")""",
                "fixed_code": """def greet():
    print("Hello!")""",
                "bug_type": "Indentation Error",
                "hint": "Python uses indentation to group code",
                "explanation": "Code inside functions must be indented"
            },
            {
                "level": 2,
                "title": "Division by Zero",
                "buggy_code": """def divide(a, b):
    return a / b

result = divide(10, 0)""",
                "fixed_code": """def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b

result = divide(10, 0)""",
                "bug_type": "Runtime Error",
                "hint": "What happens when you divide by zero?",
                "explanation": "Always check for zero before dividing"
            },
            {
                "level": 2,
                "title": "Undefined Variable",
                "buggy_code": """def calculate():
    result = x + y
    return result

answer = calculate()""",
                "fixed_code": """def calculate():
    x = 10
    y = 5
    result = x + y
    return result

answer = calculate()""",
                "bug_type": "Name Error",
                "hint": "Are all variables defined before use?",
                "explanation": "Variables must be defined before they can be used"
            },
            {
                "level": 2,
                "title": "Type Mismatch",
                "buggy_code": """age = "25"
next_year = age + 1""",
                "fixed_code": """age = "25"
next_year = int(age) + 1""",
                "bug_type": "Type Error",
                "hint": "Can you add a string and a number?",
                "explanation": "Convert string to integer before mathematical operations"
            },
            {
                "level": 3,
                "title": "Wrong Logic",
                "buggy_code": """def is_even(number):
    if number % 2 == 1:
        return True
    return False""",
                "fixed_code": """def is_even(number):
    if number % 2 == 0:
        return True
    return False""",
                "bug_type": "Logic Error",
                "hint": "What remainder do even numbers have when divided by 2?",
                "explanation": "Even numbers have remainder 0, not 1, when divided by 2"
            },
            {
                "level": 3,
                "title": "Off-by-One Error",
                "buggy_code": """def print_numbers(n):
    for i in range(1, n):
        print(i)

print_numbers(5)  # Should print 1,2,3,4,5""",
                "fixed_code": """def print_numbers(n):
    for i in range(1, n + 1):
        print(i)

print_numbers(5)  # Prints 1,2,3,4,5""",
                "bug_type": "Logic Error",
                "hint": "Check the range function carefully",
                "explanation": "range(1, n) goes from 1 to n-1, not n"
            },
            {
                "level": 3,
                "title": "Infinite Loop",
                "buggy_code": """count = 0
while count < 5:
    print(count)
    # Missing increment!""",
                "fixed_code": """count = 0
while count < 5:
    print(count)
    count += 1  # Don't forget to increment!""",
                "bug_type": "Logic Error",
                "hint": "What makes the loop condition change?",
                "explanation": "Loop variables must be updated to avoid infinite loops"
            }
        ]
    
    def print_banner(self):
        """Print game banner"""
        print("""
🎮 ═══════════════════════════════════════════════════════════════ 🎮
                        BUG HUNTING GAME
                    Find and Fix the Bugs! 🐛
🎮 ═══════════════════════════════════════════════════════════════ 🎮
        """)
    
    def show_stats(self):
        """Show current game statistics"""
        print(f"\n📊 GAME STATS:")
        print(f"   🎯 Score: {self.score}")
        print(f"   📈 Level: {self.level}")
        print(f"   🐛 Bugs Found: {self.bugs_found}")
    
    def present_challenge(self, challenge):
        """Present a bug challenge to the player"""
        print(f"\n🐛 BUG CHALLENGE #{self.bugs_found + 1}")
        print(f"📋 Title: {challenge['title']}")
        print(f"🏷️  Type: {challenge['bug_type']}")
        print(f"⭐ Level: {challenge['level']}")
        print("\n" + "="*50)
        print("🔍 BUGGY CODE:")
        print("="*50)
        print(challenge['buggy_code'])
        print("="*50)
        
        return challenge
    
    def get_user_choice(self):
        """Get user's choice for what to do"""
        print("\n🎯 What would you like to do?")
        print("1. 💡 Get a hint")
        print("2. 🔧 See the fix")
        print("3. 📚 Get explanation")
        print("4. ➡️  Next challenge")
        print("5. 🏃 Quit game")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1-5): "))
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("❌ Please enter a number between 1 and 5")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def show_hint(self, challenge):
        """Show hint for the current challenge"""
        print(f"\n💡 HINT: {challenge['hint']}")
    
    def show_fix(self, challenge):
        """Show the fixed code"""
        print("\n" + "="*50)
        print("✅ FIXED CODE:")
        print("="*50)
        print(challenge['fixed_code'])
        print("="*50)
        
        # Award points
        points = challenge['level'] * 10
        self.score += points
        self.bugs_found += 1
        
        print(f"\n🎉 Bug fixed! +{points} points!")
        
        # Level up check
        if self.bugs_found % 3 == 0:
            self.level += 1
            print(f"🆙 LEVEL UP! You're now level {self.level}!")
    
    def show_explanation(self, challenge):
        """Show detailed explanation"""
        print(f"\n📚 EXPLANATION:")
        print(f"   {challenge['explanation']}")
        
        # Show what type of error this is
        print(f"\n🏷️  ERROR TYPE: {challenge['bug_type']}")
        
        if challenge['bug_type'] == "Syntax Error":
            print("   • Caught before the program runs")
            print("   • Python can't understand the code")
            print("   • Usually easy to spot and fix")
        elif challenge['bug_type'] == "Runtime Error":
            print("   • Happens while the program is running")
            print("   • Code is valid but something goes wrong")
            print("   • Can be prevented with error handling")
        elif challenge['bug_type'] == "Logic Error":
            print("   • Code runs but produces wrong results")
            print("   • Hardest type of bug to find")
            print("   • Requires careful thinking about the logic")
    
    def play_game(self):
        """Main game loop"""
        self.print_banner()
        
        print("🎯 Welcome to Bug Hunting!")
        print("Your mission: Find and fix bugs in Python code!")
        print("Each bug you fix earns you points and experience.")
        print("Ready to become a debugging detective? 🕵️‍♂️")
        
        input("\nPress Enter to start hunting bugs...")
        
        # Shuffle challenges for variety
        challenges = self.bug_challenges.copy()
        random.shuffle(challenges)
        
        for challenge in challenges:
            self.show_stats()
            current_challenge = self.present_challenge(challenge)
            
            while True:
                choice = self.get_user_choice()
                
                if choice == 1:  # Hint
                    self.show_hint(current_challenge)
                elif choice == 2:  # Show fix
                    self.show_fix(current_challenge)
                    break  # Move to next challenge
                elif choice == 3:  # Explanation
                    self.show_explanation(current_challenge)
                elif choice == 4:  # Next challenge
                    print("⏭️  Moving to next challenge...")
                    break
                elif choice == 5:  # Quit
                    print("👋 Thanks for playing Bug Hunting!")
                    return
        
        # Game completed
        self.show_final_results()
    
    def show_final_results(self):
        """Show final game results"""
        print("\n" + "="*60)
        print("🎉 CONGRATULATIONS! YOU'VE COMPLETED BUG HUNTING!")
        print("="*60)
        
        self.show_stats()
        
        # Calculate performance
        if self.score >= 200:
            rank = "🏆 Bug Hunting Master"
        elif self.score >= 150:
            rank = "🥇 Senior Debugger"
        elif self.score >= 100:
            rank = "🥈 Junior Debugger"
        elif self.score >= 50:
            rank = "🥉 Bug Spotter"
        else:
            rank = "🔍 Debugging Apprentice"
        
        print(f"\n🏅 Your Rank: {rank}")
        
        print("\n🎯 What you've learned:")
        print("✅ How to spot syntax errors")
        print("✅ How to handle runtime errors")
        print("✅ How to think through logic errors")
        print("✅ Debugging techniques and strategies")
        
        print("\n💡 Keep practicing!")
        print("The more bugs you encounter and fix, the better debugger you become!")
        print("Remember: Every expert was once a beginner! 🚀")

def main():
    """Main function to start the game"""
    game = BugHuntingGame()
    
    try:
        game.play_game()
    except KeyboardInterrupt:
        print("\n\n👋 Game interrupted. Thanks for playing!")
        print("Come back anytime to hunt more bugs! 🐛")

if __name__ == "__main__":
    main()
