#!/usr/bin/env python3
"""
🚀 START YOUR DEBUGGING JOURNEY
Quick launcher for all debugging learning resources
"""

import os
import sys

def print_banner():
    """Print welcome banner"""
    print("""
🐛 ═══════════════════════════════════════════════════════════════ 🐛
                    DEBUGGING LEARNING CENTER
                   Master the Art of Bug Hunting! 
🐛 ═══════════════════════════════════════════════════════════════ 🐛
    """)

def show_menu():
    """Show main menu options"""
    print("\n🎯 Choose your debugging adventure:")
    print()
    print("1. 📚 Read the Complete Bugs & Errors Guide")
    print("2. 🎓 Take the Interactive Debugging Lesson")
    print("3. 🎮 Play the Bug Hunting Game")
    print("4. 🔧 Quick Debugging Tips")
    print("5. 🆘 Emergency Bug Help")
    print("6. 🚪 Exit")
    print()

def show_guide_info():
    """Show information about the guide"""
    print("\n📚 COMPLETE BUGS & ERRORS GUIDE")
    print("="*50)
    print("This comprehensive guide covers:")
    print("✅ Types of errors (Syntax, Runtime, Logical)")
    print("✅ Common Python mistakes")
    print("✅ Debugging techniques and tools")
    print("✅ Best practices for error handling")
    print("✅ Real-world examples and solutions")
    print()
    
    if os.path.exists("BUGS_AND_ERRORS_GUIDE.md"):
        print("📖 The guide is available as: BUGS_AND_ERRORS_GUIDE.md")
        print("💡 Open it in any text editor or markdown viewer")
    else:
        print("❌ Guide file not found!")
    
    input("\nPress Enter to return to menu...")

def show_lesson_info():
    """Show information about the interactive lesson"""
    print("\n🎓 INTERACTIVE DEBUGGING LESSON")
    print("="*50)
    print("A hands-on tutorial that teaches:")
    print("✅ How to identify different types of errors")
    print("✅ Practical debugging techniques")
    print("✅ Interactive exercises")
    print("✅ Real debugging scenarios")
    print()
    
    if os.path.exists("debugging_lesson.py"):
        choice = input("🚀 Would you like to start the lesson now? (y/n): ").lower()
        if choice == 'y':
            print("\n🎯 Starting Interactive Debugging Lesson...")
            try:
                exec(open('debugging_lesson.py').read())
            except Exception as e:
                print(f"❌ Error running lesson: {e}")
                print("💡 Try running: python debugging_lesson.py")
        else:
            print("💡 You can run it later with: python debugging_lesson.py")
    else:
        print("❌ Lesson file not found!")
    
    input("\nPress Enter to return to menu...")

def show_game_info():
    """Show information about the bug hunting game"""
    print("\n🎮 BUG HUNTING GAME")
    print("="*50)
    print("A fun way to practice debugging:")
    print("✅ Find bugs in code challenges")
    print("✅ Earn points for each bug fixed")
    print("✅ Level up your debugging skills")
    print("✅ Learn from detailed explanations")
    print()
    
    if os.path.exists("bug_hunting_game.py"):
        choice = input("🎯 Ready to hunt some bugs? (y/n): ").lower()
        if choice == 'y':
            print("\n🎮 Starting Bug Hunting Game...")
            try:
                exec(open('bug_hunting_game.py').read())
            except Exception as e:
                print(f"❌ Error running game: {e}")
                print("💡 Try running: python bug_hunting_game.py")
        else:
            print("💡 You can play later with: python bug_hunting_game.py")
    else:
        print("❌ Game file not found!")
    
    input("\nPress Enter to return to menu...")

def show_quick_tips():
    """Show quick debugging tips"""
    print("\n🔧 QUICK DEBUGGING TIPS")
    print("="*50)
    
    tips = [
        ("🔍", "Read error messages carefully - they contain valuable clues"),
        ("🖨️", "Use print() statements to see what's happening in your code"),
        ("🎯", "Start with the first error - fix one at a time"),
        ("🧪", "Test with simple inputs first"),
        ("🔄", "Make small changes and test frequently"),
        ("💭", "Explain your code to someone else (or a rubber duck!)"),
        ("⏰", "Take breaks - fresh eyes spot bugs faster"),
        ("📝", "Keep notes of what you've tried"),
        ("🛡️", "Add error handling with try/except blocks"),
        ("🎓", "Learn from each bug - understand why it happened")
    ]
    
    print("🏆 TOP 10 DEBUGGING TIPS:")
    print()
    for i, (icon, tip) in enumerate(tips, 1):
        print(f"{i:2d}. {icon} {tip}")
    
    print("\n💡 REMEMBER:")
    print("Every programmer deals with bugs - even the experts!")
    print("Debugging is a skill that improves with practice.")
    print("Don't get frustrated - each bug makes you stronger! 💪")
    
    input("\nPress Enter to return to menu...")

def show_emergency_help():
    """Show emergency debugging help"""
    print("\n🆘 EMERGENCY BUG HELP")
    print("="*50)
    print("Got a bug you can't figure out? Here's what to do:")
    print()
    
    print("🔥 IMMEDIATE STEPS:")
    print("1. Don't panic! Take a deep breath 🧘")
    print("2. Read the error message completely")
    print("3. Look at the line number mentioned in the error")
    print("4. Check for common mistakes:")
    print("   • Missing colons (:)")
    print("   • Wrong indentation")
    print("   • Mismatched parentheses/quotes")
    print("   • Undefined variables")
    print("   • Type mismatches")
    print()
    
    print("🔍 DEBUGGING PROCESS:")
    print("1. Isolate the problem - create minimal test case")
    print("2. Add print statements to trace execution")
    print("3. Check your assumptions about what the code does")
    print("4. Test with simple, known inputs")
    print("5. Comment out sections to narrow down the issue")
    print()
    
    print("🆘 WHEN TO ASK FOR HELP:")
    print("• You've been stuck for more than 30 minutes")
    print("• You've tried multiple approaches")
    print("• The error message doesn't make sense")
    print("• You suspect it might be a complex issue")
    print()
    
    print("📞 WHERE TO GET HELP:")
    print("• Stack Overflow (stackoverflow.com)")
    print("• Python Discord communities")
    print("• Reddit r/learnpython")
    print("• Python documentation (docs.python.org)")
    print("• Local programming meetups")
    
    input("\nPress Enter to return to menu...")

def main():
    """Main function"""
    print_banner()
    
    print("🎯 Welcome to your debugging learning journey!")
    print("Debugging is one of the most important skills in programming.")
    print("Every expert programmer was once a beginner who made lots of mistakes!")
    print("The key is learning from each bug and getting better at finding them.")
    
    while True:
        try:
            show_menu()
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == '1':
                show_guide_info()
            elif choice == '2':
                show_lesson_info()
            elif choice == '3':
                show_game_info()
            elif choice == '4':
                show_quick_tips()
            elif choice == '5':
                show_emergency_help()
            elif choice == '6':
                print("\n👋 Happy debugging!")
                print("Remember: Every bug you encounter makes you a better programmer!")
                print("🚀 Keep coding and keep learning!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Thanks for visiting the Debugging Learning Center!")
            print("Come back anytime to sharpen your bug-hunting skills! 🐛")
            break
        except Exception as e:
            print(f"\n❌ Oops! An error occurred: {e}")
            print("💡 Looks like we found a bug in the bug learning program! 😄")
            print("This is actually a great example of how bugs can appear anywhere.")

if __name__ == "__main__":
    main()
