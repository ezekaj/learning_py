@echo off
echo.
echo 🐍 ═══════════════════════════════════════════════════════════════ 🐍
echo                    PYTHON LEARNING JOURNEY
echo                        INSTANT START
echo 🐍 ═══════════════════════════════════════════════════════════════ 🐍
echo.

echo 🚀 Starting your Python learning journey...
echo.

REM Try to run the Python learning app
python start_learning.py

REM If that fails, try with py command
if errorlevel 1 (
    echo.
    echo 🔄 Trying alternative Python command...
    py start_learning.py
)

REM If that also fails, try the simple app directly
if errorlevel 1 (
    echo.
    echo 🔄 Trying direct app launch...
    python simple_app.py
)

REM Final fallback
if errorlevel 1 (
    echo.
    echo ❌ Having trouble starting the app automatically.
    echo 💡 Please try these commands manually:
    echo.
    echo    python start_learning.py
    echo    OR
    echo    python simple_app.py
    echo.
    echo 📍 Then open your browser to: http://localhost:5000
    echo.
)

echo.
echo 👋 Press any key to exit...
pause >nul
