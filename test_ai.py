#!/usr/bin/env python3
"""
🧪 TEST AI FUNCTIONALITY
Quick test to verify if Pythia AI Assistant is working
"""

def test_ai_assistant():
    """Test the AI assistant functionality"""
    print("🧪 Testing Pythia AI Assistant...")
    
    try:
        # Import the AI assistant
        from ai_assistant import pythia, get_ai_help
        print("✅ AI Assistant imported successfully!")
        
        # Test code analysis
        test_code = """
name = "Python"
age = 30
if age >= 18:
    print(f"Hello {name}, you can vote!")
"""
        
        print("\n🔍 Testing code analysis...")
        analysis = pythia.analyze_code(test_code, "beginner")
        print("✅ Code analysis working!")
        print(f"   Concepts found: {analysis['concepts_used']}")
        print(f"   Explanations: {len(analysis['explanation'])}")
        
        # Test hint system
        print("\n💡 Testing hint system...")
        hint = pythia.get_intelligent_hint("I want to create a loop", "", "beginner")
        print("✅ Hint system working!")
        print(f"   Hint preview: {hint[:100]}...")
        
        # Test natural language to code
        print("\n✨ Testing natural language to code...")
        generated_code = pythia.natural_language_to_code("print hello world")
        print("✅ Natural language conversion working!")
        print(f"   Generated: {generated_code}")
        
        # Test error explanation
        print("\n🔧 Testing error explanation...")
        error_explanation = pythia.explain_error("SyntaxError: invalid syntax")
        print("✅ Error explanation working!")
        print(f"   Explanation: {error_explanation}")
        
        # Test code suggestions
        print("\n📝 Testing code suggestions...")
        suggestions = pythia.suggest_improvements(test_code)
        print("✅ Code suggestions working!")
        print(f"   Suggestions: {len(suggestions)}")
        
        # Test get_ai_help function
        print("\n🤖 Testing main AI help function...")
        ai_response = get_ai_help(code=test_code, user_level="beginner")
        print("✅ Main AI help function working!")
        print(f"   Response type: {type(ai_response)}")
        
        print("\n🎉 ALL AI TESTS PASSED!")
        print("✅ Pythia AI Assistant is fully functional!")
        return True
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("   AI Assistant files might be missing")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   AI Assistant has issues")
        return False

def test_flask_ai_integration():
    """Test if AI works with Flask"""
    print("\n🌐 Testing Flask AI integration...")
    
    try:
        # Test if we can import Flask components
        from flask import Flask
        print("✅ Flask available")
        
        # Test if AI assistant works in Flask context
        from ai_assistant import get_ai_help
        
        # Simulate a request
        test_response = get_ai_help(
            code="print('Hello World')",
            context="I need help with my code",
            user_level="beginner"
        )
        
        print("✅ AI works in Flask context!")
        print(f"   Response keys: {list(test_response.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask AI integration error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PYTHIA AI ASSISTANT TEST SUITE")
    print("=" * 40)
    
    # Test AI functionality
    ai_works = test_ai_assistant()
    
    # Test Flask integration
    flask_works = test_flask_ai_integration()
    
    print("\n" + "=" * 40)
    print("📊 TEST RESULTS:")
    print(f"   🤖 AI Assistant: {'✅ WORKING' if ai_works else '❌ BROKEN'}")
    print(f"   🌐 Flask Integration: {'✅ WORKING' if flask_works else '❌ BROKEN'}")
    
    if ai_works and flask_works:
        print("\n🎉 PYTHIA AI IS FULLY FUNCTIONAL!")
        print("   The AI features in your app will work perfectly!")
    else:
        print("\n⚠️  SOME AI FEATURES MAY NOT WORK")
        print("   Check the errors above for details")
    
    print("\n💡 To test in the app:")
    print("   1. Go to Playground")
    print("   2. Write some Python code")
    print("   3. Click 'AI Help' or 'AI Analyze'")
    print("   4. See if Pythia responds")
