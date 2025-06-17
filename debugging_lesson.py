#!/usr/bin/env python3
"""
🐛 DEBUGGING LESSON - INTERACTIVE PYTHON DEBUGGING TUTORIAL
Learn to find and fix bugs like a pro!
"""

import traceback
import sys

def print_header(title):
    """Print a nice header for each section"""
    print("\n" + "="*60)
    print(f"🐛 {title}")
    print("="*60)

def demonstrate_syntax_errors():
    """Show common syntax errors and how to fix them"""
    print_header("SYNTAX ERRORS - CAUGHT BEFORE RUNNING")
    
    print("🔴 Syntax errors prevent your code from running at all!")
    print("Python catches these before execution starts.\n")
    
    # Example 1: Missing colon
    print("❌ EXAMPLE 1: Missing colon")
    print("if x > 5")
    print("    print('Big number')")
    print("\n✅ FIXED VERSION:")
    print("if x > 5:")
    print("    print('Big number')")
    
    # Example 2: Mismatched parentheses
    print("\n❌ EXAMPLE 2: Mismatched parentheses")
    print('print("Hello World"')
    print("\n✅ FIXED VERSION:")
    print('print("Hello World")')
    
    # Example 3: Wrong indentation
    print("\n❌ EXAMPLE 3: Wrong indentation")
    print("def my_function():")
    print("print('Hello')")
    print("\n✅ FIXED VERSION:")
    print("def my_function():")
    print("    print('Hello')")
    
    input("\n📖 Press Enter to continue to Runtime Errors...")

def demonstrate_runtime_errors():
    """Show common runtime errors with interactive examples"""
    print_header("RUNTIME ERRORS - HAPPEN WHILE RUNNING")
    
    print("🟡 Runtime errors occur during program execution!")
    print("Let's see some common ones:\n")
    
    # ZeroDivisionError
    print("🔢 EXAMPLE 1: ZeroDivisionError")
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"❌ Error: {e}")
        print("✅ Fix: Check if denominator is zero before dividing")
    
    # NameError
    print("\n📝 EXAMPLE 2: NameError")
    try:
        print(undefined_variable)
    except NameError as e:
        print(f"❌ Error: {e}")
        print("✅ Fix: Define the variable before using it")
    
    # TypeError
    print("\n🔤 EXAMPLE 3: TypeError")
    try:
        result = "Hello" + 5
    except TypeError as e:
        print(f"❌ Error: {e}")
        print("✅ Fix: Convert number to string: 'Hello' + str(5)")
    
    # IndexError
    print("\n📋 EXAMPLE 4: IndexError")
    try:
        my_list = [1, 2, 3]
        print(my_list[5])
    except IndexError as e:
        print(f"❌ Error: {e}")
        print("✅ Fix: Check list length or use valid index")
    
    input("\n📖 Press Enter to continue to Logical Errors...")

def demonstrate_logical_errors():
    """Show logical errors - the trickiest ones!"""
    print_header("LOGICAL ERRORS - THE SNEAKY ONES")
    
    print("🟠 Logical errors are the hardest to find!")
    print("The code runs without errors but gives wrong results.\n")
    
    # Example 1: Wrong calculation
    print("🧮 EXAMPLE 1: Wrong calculation")
    def calculate_average_wrong(numbers):
        total = sum(numbers)
        average = total / len(numbers) + 1  # ❌ Why +1?
        return average
    
    def calculate_average_correct(numbers):
        total = sum(numbers)
        average = total / len(numbers)  # ✅ Correct
        return average
    
    test_numbers = [10, 20, 30]
    wrong_result = calculate_average_wrong(test_numbers)
    correct_result = calculate_average_correct(test_numbers)
    
    print(f"Numbers: {test_numbers}")
    print(f"❌ Wrong result: {wrong_result}")
    print(f"✅ Correct result: {correct_result}")
    
    # Example 2: Wrong condition
    print("\n🎂 EXAMPLE 2: Wrong condition")
    age = 25
    print(f"Age: {age}")
    
    # Wrong logic
    if age > 18:
        wrong_message = "You're a minor"
    else:
        wrong_message = "You're an adult"
    
    # Correct logic
    if age >= 18:
        correct_message = "You're an adult"
    else:
        correct_message = "You're a minor"
    
    print(f"❌ Wrong logic: {wrong_message}")
    print(f"✅ Correct logic: {correct_message}")
    
    input("\n📖 Press Enter to learn debugging techniques...")

def demonstrate_debugging_techniques():
    """Show practical debugging techniques"""
    print_header("DEBUGGING TECHNIQUES")
    
    print("🛠️ Here are the most effective debugging techniques:\n")
    
    # Print debugging
    print("1. 🖨️ PRINT DEBUGGING (Most Common)")
    print("Add print statements to see what's happening:")
    
    def buggy_function(numbers):
        print(f"🔍 Input: {numbers}")  # Debug print
        
        total = 0
        for i, num in enumerate(numbers):
            print(f"🔍 Step {i+1}: Adding {num}")  # Debug print
            total += num
            print(f"🔍 Running total: {total}")  # Debug print
        
        print(f"🔍 Final total: {total}")  # Debug print
        return total
    
    print("\nRunning buggy_function([5, 10, 15]):")
    result = buggy_function([5, 10, 15])
    
    # Error handling
    print("\n2. 🛡️ ERROR HANDLING")
    print("Use try/except to handle errors gracefully:")
    
    def safe_divide(a, b):
        try:
            result = a / b
            print(f"✅ {a} ÷ {b} = {result}")
            return result
        except ZeroDivisionError:
            print("❌ Error: Cannot divide by zero!")
            return None
        except TypeError:
            print("❌ Error: Both values must be numbers!")
            return None
    
    print("\nTesting safe_divide:")
    safe_divide(10, 2)    # Works
    safe_divide(10, 0)    # Handles error
    safe_divide("10", 2)  # Handles error
    
    input("\n📖 Press Enter to try interactive debugging...")

def interactive_debugging_exercise():
    """Interactive debugging exercise"""
    print_header("INTERACTIVE DEBUGGING EXERCISE")
    
    print("🎯 Let's debug some code together!")
    print("I'll show you buggy code, and you help find the problem.\n")
    
    # Exercise 1
    print("🐛 EXERCISE 1: Find the bug!")
    print("This function should calculate the area of a rectangle:")
    print()
    print("def calculate_area(length, width):")
    print("    area = length * width")
    print("    return area")
    print()
    print("length = 5")
    print("width = 3")
    print("result = calculate_area(length)")  # ❌ Missing argument!
    print("print(f'Area: {result}')")
    
    user_answer = input("\n🤔 What's wrong with this code? ")
    print("✅ ANSWER: Missing the 'width' argument in the function call!")
    print("   Should be: result = calculate_area(length, width)")
    
    # Exercise 2
    print("\n🐛 EXERCISE 2: Logic error!")
    print("This function should check if a number is even:")
    print()
    print("def is_even(number):")
    print("    if number % 2 == 1:")  # ❌ Wrong condition!
    print("        return True")
    print("    else:")
    print("        return False")
    
    user_answer = input("\n🤔 What's the logical error? ")
    print("✅ ANSWER: The condition is backwards!")
    print("   Should be: if number % 2 == 0:")
    print("   (Even numbers have remainder 0 when divided by 2)")
    
    input("\n📖 Press Enter to see debugging tools...")

def show_debugging_tools():
    """Show available debugging tools"""
    print_header("DEBUGGING TOOLS")
    
    print("🔧 Python provides many debugging tools:\n")
    
    print("1. 🖨️ PRINT STATEMENTS")
    print("   - Simplest method")
    print("   - Add print() to see variable values")
    print("   - Example: print(f'Debug: x = {x}')")
    
    print("\n2. 🏷️ LOGGING")
    print("   - Better than print for larger programs")
    print("   - Can control what gets printed")
    print("   - Example: logging.debug('Debug message')")
    
    print("\n3. 🔍 PDB DEBUGGER")
    print("   - Built-in Python debugger")
    print("   - Step through code line by line")
    print("   - Example: import pdb; pdb.set_trace()")
    
    print("\n4. 💻 IDE DEBUGGERS")
    print("   - Visual Studio Code")
    print("   - PyCharm")
    print("   - Set breakpoints with mouse clicks")
    
    print("\n5. 🎯 MODERN BREAKPOINTS")
    print("   - Python 3.7+ has breakpoint() function")
    print("   - Just add breakpoint() in your code")
    print("   - Automatically opens debugger")
    
    input("\n📖 Press Enter for debugging tips...")

def show_debugging_tips():
    """Show practical debugging tips"""
    print_header("DEBUGGING TIPS & BEST PRACTICES")
    
    tips = [
        "🧘 Don't panic - bugs are normal and expected!",
        "📖 Read error messages carefully - they contain clues",
        "🔍 Start with the first error - fix one at a time",
        "🎯 Isolate the problem - create minimal test case",
        "🖨️ Use print statements to trace execution",
        "🧪 Test with simple inputs first",
        "💭 Explain the problem to someone else (rubber duck debugging)",
        "⏰ Take breaks - fresh eyes spot bugs faster",
        "📝 Keep notes of what you've tried",
        "🔄 Use version control to track changes",
        "🎓 Learn from each bug - understand why it happened",
        "🛡️ Write defensive code - check inputs and handle errors"
    ]
    
    print("🏆 TOP DEBUGGING TIPS:\n")
    for i, tip in enumerate(tips, 1):
        print(f"{i:2d}. {tip}")
    
    print("\n🎯 REMEMBER:")
    print("Every expert programmer was once a beginner who made lots of mistakes!")
    print("Debugging is a skill that improves with practice.")
    print("The more bugs you fix, the better you become at preventing them!")

def main():
    """Main lesson function"""
    print("""
🐛 ═══════════════════════════════════════════════════════════════ 🐛
                    PYTHON DEBUGGING MASTERCLASS
                     Learn to Squash Bugs Like a Pro!
🐛 ═══════════════════════════════════════════════════════════════ 🐛

Welcome to the most important skill in programming: DEBUGGING! 🎯

Every programmer spends time debugging. The difference between beginners 
and experts is not that experts don't make mistakes - it's that they're 
better at finding and fixing them quickly!

Today you'll learn:
• Types of errors (Syntax, Runtime, Logical)
• Debugging techniques and tools
• Best practices for preventing bugs
• Interactive debugging exercises

Ready to become a debugging detective? Let's go! 🕵️‍♂️
    """)
    
    input("Press Enter to start the lesson...")
    
    try:
        demonstrate_syntax_errors()
        demonstrate_runtime_errors()
        demonstrate_logical_errors()
        demonstrate_debugging_techniques()
        interactive_debugging_exercise()
        show_debugging_tools()
        show_debugging_tips()
        
        print_header("CONGRATULATIONS! 🎉")
        print("You've completed the Debugging Masterclass!")
        print("You now know:")
        print("✅ The three types of errors")
        print("✅ How to use debugging techniques")
        print("✅ Best practices for finding bugs")
        print("✅ Tools available for debugging")
        print("\nKeep practicing, and remember:")
        print("🐛 Bugs are not failures - they're learning opportunities!")
        print("🚀 Happy debugging!")
        
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for learning about debugging!")
        print("Remember: Every bug you encounter makes you a better programmer!")

if __name__ == "__main__":
    main()
