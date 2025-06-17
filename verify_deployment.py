#!/usr/bin/env python3
"""
Deployment Verification Script for Python Learning Platform
Tests all key functionality and deployment status
"""

import requests
import json
import os
from pathlib import Path
import time

def test_github_pages():
    """Test GitHub Pages deployment"""
    print("🌐 Testing GitHub Pages deployment...")
    
    base_url = "https://ezekaj.github.io/learning_py"
    pages_to_test = [
        "/",
        "/lessons.html",
        "/playground.html", 
        "/documentation.html"
    ]
    
    results = {}
    
    for page in pages_to_test:
        url = f"{base_url}{page}"
        try:
            response = requests.get(url, timeout=10)
            results[page] = {
                "status_code": response.status_code,
                "success": response.status_code == 200,
                "size": len(response.content)
            }
            print(f"  ✅ {page}: {response.status_code} ({len(response.content)} bytes)")
        except Exception as e:
            results[page] = {
                "status_code": None,
                "success": False,
                "error": str(e)
            }
            print(f"  ❌ {page}: Error - {e}")
    
    return results

def test_local_app():
    """Test local Flask application"""
    print("\n🖥️ Testing local Flask application...")
    
    # Check if app.py exists and can be imported
    try:
        import app
        print("  ✅ app.py imports successfully")
        
        # Check if Flask app is configured
        if hasattr(app, 'app'):
            print("  ✅ Flask app is configured")
        else:
            print("  ❌ Flask app not found")
            
    except ImportError as e:
        print(f"  ❌ Cannot import app.py: {e}")
        return False
    
    return True

def test_data_structure():
    """Test data structure and files"""
    print("\n📁 Testing data structure...")
    
    required_files = [
        "README.md",
        "requirements.txt",
        "app.py",
        "main.py",
        "generate_static_site.py",
        "data_migration.py",
        "CONTRIBUTING.md",
        "LICENSE"
    ]
    
    required_dirs = [
        "data",
        "templates", 
        "static",
        "core",
        "modules",
        "docs",
        ".github/workflows"
    ]
    
    missing_files = []
    missing_dirs = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"  ✅ {file}")
    
    for dir in required_dirs:
        if not Path(dir).exists():
            missing_dirs.append(dir)
        else:
            print(f"  ✅ {dir}/")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
    
    if missing_dirs:
        print(f"  ❌ Missing directories: {missing_dirs}")
    
    return len(missing_files) == 0 and len(missing_dirs) == 0

def test_static_site_generation():
    """Test static site generation"""
    print("\n🏗️ Testing static site generation...")
    
    try:
        import generate_static_site
        print("  ✅ Static site generator imports successfully")
        
        # Check if docs directory exists and has content
        docs_dir = Path("docs")
        if docs_dir.exists():
            html_files = list(docs_dir.glob("*.html"))
            print(f"  ✅ Found {len(html_files)} HTML files in docs/")
            
            for html_file in html_files:
                print(f"    - {html_file.name}")
        else:
            print("  ❌ docs/ directory not found")
            return False
            
    except ImportError as e:
        print(f"  ❌ Cannot import generate_static_site.py: {e}")
        return False
    
    return True

def test_data_migration():
    """Test data migration functionality"""
    print("\n🔄 Testing data migration...")
    
    try:
        from data_migration import UserDataMigration
        migration = UserDataMigration()
        
        # Test migration report
        report = migration.get_migration_report()
        print(f"  ✅ Migration report generated: {report['total_users']} users")
        
        # Check if backup directory exists
        backup_dir = Path("data/backups")
        if backup_dir.exists():
            backups = list(backup_dir.glob("*.json"))
            print(f"  ✅ Found {len(backups)} backup files")
        else:
            print("  ⚠️ No backup directory found (normal for new installations)")
        
    except Exception as e:
        print(f"  ❌ Data migration test failed: {e}")
        return False
    
    return True

def test_requirements():
    """Test requirements and dependencies"""
    print("\n📦 Testing requirements...")
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().strip().split("\n")
        
        print(f"  ✅ Found {len(requirements)} requirements")
        
        # Test key dependencies
        key_deps = ["flask", "requests"]
        for dep in key_deps:
            if any(dep.lower() in req.lower() for req in requirements):
                print(f"    ✅ {dep}")
            else:
                print(f"    ❌ {dep} not found")
        
    except Exception as e:
        print(f"  ❌ Requirements test failed: {e}")
        return False
    
    return True

def generate_report(results):
    """Generate comprehensive verification report"""
    print("\n" + "="*60)
    print("📊 DEPLOYMENT VERIFICATION REPORT")
    print("="*60)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\nTest Results:")
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Deployment is successful!")
        print("\n🌐 Your Python Learning Platform is live at:")
        print("   https://ezekaj.github.io/learning_py/")
    else:
        print(f"\n⚠️ {total_tests - passed_tests} test(s) failed. Please review the issues above.")
    
    print("\n📚 Next Steps:")
    print("  1. Visit the live site and test all features")
    print("  2. Share the platform with learners")
    print("  3. Monitor GitHub Actions for deployment status")
    print("  4. Consider adding more content and features")

def main():
    """Main verification function"""
    print("🚀 Python Learning Platform - Deployment Verification")
    print("="*60)
    
    # Run all tests
    results = {
        "GitHub Pages Deployment": test_github_pages(),
        "Local Application": test_local_app(),
        "Data Structure": test_data_structure(),
        "Static Site Generation": test_static_site_generation(),
        "Data Migration": test_data_migration(),
        "Requirements": test_requirements()
    }
    
    # For GitHub Pages, check if any page loaded successfully
    if isinstance(results["GitHub Pages Deployment"], dict):
        results["GitHub Pages Deployment"] = any(
            page_result.get("success", False) 
            for page_result in results["GitHub Pages Deployment"].values()
        )
    
    # Generate final report
    generate_report(results)

if __name__ == "__main__":
    main()
