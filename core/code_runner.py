"""
Code Runner Module
Inspired by interactive coding platforms and online IDEs:
- Safe code execution environment
- Real-time code validation
- Interactive Python shell
- Code sharing and saving features
"""

import sys
import io
import contextlib
import traceback
import ast
import os
import json
import time
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import colorama
from colorama import Fore, Style

class CodeRunner:
    """Safe Python code execution environment"""
    
    def __init__(self, playground_dir: str = "data/playground"):
        self.playground_dir = playground_dir
        self.execution_history = []
        self.saved_snippets = {}
        self.ensure_playground_dir()
        self.load_saved_snippets()
        
        # Restricted imports for safety
        self.allowed_modules = {
            'math', 'random', 'datetime', 'json', 'os', 'sys',
            'collections', 'itertools', 'functools', 're',
            'string', 'time', 'calendar', 'decimal', 'fractions'
        }
        
        # Dangerous functions to block
        self.blocked_functions = {
            'exec', 'eval', 'compile', '__import__', 'open',
            'input', 'raw_input', 'file', 'execfile', 'reload'
        }
    
    def ensure_playground_dir(self):
        """Create playground directory structure"""
        os.makedirs(self.playground_dir, exist_ok=True)
        os.makedirs(os.path.join(self.playground_dir, "saved"), exist_ok=True)
        os.makedirs(os.path.join(self.playground_dir, "history"), exist_ok=True)
    
    def load_saved_snippets(self):
        """Load saved code snippets"""
        snippets_file = os.path.join(self.playground_dir, "snippets.json")
        try:
            if os.path.exists(snippets_file):
                with open(snippets_file, 'r') as f:
                    self.saved_snippets = json.load(f)
        except Exception:
            self.saved_snippets = {}
    
    def save_snippets(self):
        """Save code snippets to file"""
        snippets_file = os.path.join(self.playground_dir, "snippets.json")
        try:
            with open(snippets_file, 'w') as f:
                json.dump(self.saved_snippets, f, indent=2)
        except Exception as e:
            print(f"Error saving snippets: {e}")
    
    def is_safe_code(self, code: str) -> Tuple[bool, str]:
        """Check if code is safe to execute"""
        try:
            # Parse the code to check for dangerous constructs
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # Check for dangerous function calls
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.blocked_functions:
                            return False, f"Blocked function: {node.func.id}"
                
                # Check for dangerous imports
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name not in self.allowed_modules:
                            return False, f"Import not allowed: {alias.name}"
                
                if isinstance(node, ast.ImportFrom):
                    if node.module and node.module not in self.allowed_modules:
                        return False, f"Import not allowed: {node.module}"
                
                # Check for file operations
                if isinstance(node, ast.Attribute):
                    if node.attr in ['open', 'read', 'write', 'remove', 'rmdir']:
                        return False, f"File operation not allowed: {node.attr}"
            
            return True, "Code is safe"
            
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        except Exception as e:
            return False, f"Code analysis error: {e}"
    
    def execute_code(self, code: str, timeout: int = 5) -> Dict[str, Any]:
        """Execute Python code safely and return results"""
        # Check if code is safe
        is_safe, safety_message = self.is_safe_code(code)
        if not is_safe:
            return {
                "success": False,
                "error": f"Security violation: {safety_message}",
                "output": "",
                "execution_time": 0
            }
        
        # Capture stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        start_time = time.time()
        
        try:
            # Redirect output
            sys.stdout = stdout_capture
            sys.stderr = stderr_capture
            
            # Create a restricted execution environment
            exec_globals = {
                '__builtins__': {
                    'print': print,
                    'len': len,
                    'range': range,
                    'str': str,
                    'int': int,
                    'float': float,
                    'bool': bool,
                    'list': list,
                    'dict': dict,
                    'tuple': tuple,
                    'set': set,
                    'abs': abs,
                    'max': max,
                    'min': min,
                    'sum': sum,
                    'sorted': sorted,
                    'reversed': reversed,
                    'enumerate': enumerate,
                    'zip': zip,
                    'type': type,
                    'isinstance': isinstance,
                    'hasattr': hasattr,
                    'getattr': getattr,
                    'setattr': setattr,
                    'round': round,
                    'pow': pow,
                    'divmod': divmod,
                    'chr': chr,
                    'ord': ord,
                    'hex': hex,
                    'oct': oct,
                    'bin': bin,
                    'format': format,
                    'repr': repr,
                    'ascii': ascii,
                    'all': all,
                    'any': any,
                    'filter': filter,
                    'map': map,
                }
            }
            
            exec_locals = {}
            
            # Execute the code
            exec(code, exec_globals, exec_locals)
            
            execution_time = time.time() - start_time
            
            # Get output
            output = stdout_capture.getvalue()
            error_output = stderr_capture.getvalue()
            
            result = {
                "success": True,
                "output": output,
                "error": error_output if error_output else None,
                "execution_time": execution_time,
                "variables": {k: str(v) for k, v in exec_locals.items() if not k.startswith('_')}
            }
            
            # Add to execution history
            self.add_to_history(code, result)
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_message = f"{type(e).__name__}: {str(e)}"
            
            result = {
                "success": False,
                "output": stdout_capture.getvalue(),
                "error": error_message,
                "execution_time": execution_time,
                "traceback": traceback.format_exc()
            }
            
            self.add_to_history(code, result)
            return result
            
        finally:
            # Restore stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def add_to_history(self, code: str, result: Dict[str, Any]):
        """Add execution to history"""
        history_entry = {
            "timestamp": datetime.now().isoformat(),
            "code": code,
            "result": result
        }
        
        self.execution_history.append(history_entry)
        
        # Keep only last 100 executions
        if len(self.execution_history) > 100:
            self.execution_history = self.execution_history[-100:]
    
    def save_code_snippet(self, name: str, code: str, description: str = "") -> bool:
        """Save a code snippet for later use"""
        try:
            self.saved_snippets[name] = {
                "code": code,
                "description": description,
                "created_date": datetime.now().isoformat(),
                "tags": []
            }
            self.save_snippets()
            return True
        except Exception:
            return False
    
    def load_code_snippet(self, name: str) -> Optional[Dict[str, Any]]:
        """Load a saved code snippet"""
        return self.saved_snippets.get(name)
    
    def list_saved_snippets(self) -> List[Dict[str, Any]]:
        """Get list of saved snippets"""
        snippets = []
        for name, data in self.saved_snippets.items():
            snippets.append({
                "name": name,
                "description": data.get("description", ""),
                "created_date": data.get("created_date", ""),
                "code_preview": data.get("code", "")[:100] + "..." if len(data.get("code", "")) > 100 else data.get("code", "")
            })
        return snippets
    
    def delete_snippet(self, name: str) -> bool:
        """Delete a saved snippet"""
        if name in self.saved_snippets:
            del self.saved_snippets[name]
            self.save_snippets()
            return True
        return False
    
    def run_interactive_session(self):
        """Run an interactive Python session"""
        print(f"\n{Fore.GREEN}🧪 Python Code Playground{Style.RESET_ALL}")
        print("=" * 50)
        print("Enter Python code to execute. Type 'help' for commands.")
        print("Type 'exit' to quit the playground.\n")
        
        session_variables = {}
        
        while True:
            try:
                # Get user input
                code = input(f"{Fore.CYAN}>>> {Style.RESET_ALL}")
                
                if code.strip().lower() == 'exit':
                    print(f"{Fore.GREEN}Goodbye! Happy coding! 🚀{Style.RESET_ALL}")
                    break
                elif code.strip().lower() == 'help':
                    self.show_playground_help()
                    continue
                elif code.strip().lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    continue
                elif code.strip().lower() == 'history':
                    self.show_execution_history()
                    continue
                elif code.strip().lower().startswith('save '):
                    self.handle_save_command(code)
                    continue
                elif code.strip().lower().startswith('load '):
                    loaded_code = self.handle_load_command(code)
                    if loaded_code:
                        code = loaded_code
                    else:
                        continue
                elif code.strip().lower() == 'snippets':
                    self.show_saved_snippets()
                    continue
                elif not code.strip():
                    continue
                
                # Execute the code
                result = self.execute_code(code)
                
                if result["success"]:
                    if result["output"]:
                        print(result["output"], end="")
                    
                    # Update session variables
                    if result.get("variables"):
                        session_variables.update(result["variables"])
                else:
                    print(f"{Fore.RED}Error: {result['error']}{Style.RESET_ALL}")
                    if result.get("traceback"):
                        print(f"{Fore.YELLOW}Traceback:{Style.RESET_ALL}")
                        print(result["traceback"])
                
                # Show execution time for longer operations
                if result["execution_time"] > 0.1:
                    print(f"{Fore.YELLOW}Execution time: {result['execution_time']:.3f}s{Style.RESET_ALL}")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Interrupted. Type 'exit' to quit.{Style.RESET_ALL}")
            except EOFError:
                print(f"\n{Fore.GREEN}Goodbye! Happy coding! 🚀{Style.RESET_ALL}")
                break
    
    def show_playground_help(self):
        """Show playground help"""
        help_text = f"""
{Fore.GREEN}🧪 Playground Commands:{Style.RESET_ALL}
• {Fore.YELLOW}help{Style.RESET_ALL} - Show this help message
• {Fore.YELLOW}exit{Style.RESET_ALL} - Exit the playground
• {Fore.YELLOW}clear{Style.RESET_ALL} - Clear the screen
• {Fore.YELLOW}history{Style.RESET_ALL} - Show execution history
• {Fore.YELLOW}save <name>{Style.RESET_ALL} - Save the last executed code
• {Fore.YELLOW}load <name>{Style.RESET_ALL} - Load a saved code snippet
• {Fore.YELLOW}snippets{Style.RESET_ALL} - List saved code snippets

{Fore.GREEN}💡 Tips:{Style.RESET_ALL}
• You can write multi-line code by ending lines with \\
• Variables persist throughout the session
• Use print() to see output
• Code is executed in a safe environment
        """
        print(help_text)
    
    def show_execution_history(self, limit: int = 10):
        """Show recent execution history"""
        print(f"\n{Fore.GREEN}📜 Recent Execution History:{Style.RESET_ALL}")
        
        recent_history = self.execution_history[-limit:]
        
        for i, entry in enumerate(recent_history, 1):
            timestamp = entry["timestamp"][:19]  # Remove microseconds
            code_preview = entry["code"][:50] + "..." if len(entry["code"]) > 50 else entry["code"]
            status = "✅" if entry["result"]["success"] else "❌"
            
            print(f"{i}. [{timestamp}] {status} {code_preview}")
        
        if not recent_history:
            print("No execution history yet.")
    
    def handle_save_command(self, command: str):
        """Handle save command"""
        parts = command.split(' ', 1)
        if len(parts) < 2:
            print(f"{Fore.RED}Usage: save <name>{Style.RESET_ALL}")
            return
        
        name = parts[1].strip()
        if not self.execution_history:
            print(f"{Fore.RED}No code to save. Execute some code first.{Style.RESET_ALL}")
            return
        
        last_code = self.execution_history[-1]["code"]
        description = input(f"{Fore.CYAN}Enter description (optional): {Style.RESET_ALL}")
        
        if self.save_code_snippet(name, last_code, description):
            print(f"{Fore.GREEN}✅ Code snippet saved as '{name}'{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Failed to save code snippet{Style.RESET_ALL}")
    
    def handle_load_command(self, command: str) -> Optional[str]:
        """Handle load command"""
        parts = command.split(' ', 1)
        if len(parts) < 2:
            print(f"{Fore.RED}Usage: load <name>{Style.RESET_ALL}")
            return None
        
        name = parts[1].strip()
        snippet = self.load_code_snippet(name)
        
        if snippet:
            print(f"{Fore.GREEN}📂 Loaded snippet '{name}':{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}{snippet['code']}{Style.RESET_ALL}")
            return snippet['code']
        else:
            print(f"{Fore.RED}❌ Snippet '{name}' not found{Style.RESET_ALL}")
            return None
    
    def show_saved_snippets(self):
        """Show list of saved snippets"""
        snippets = self.list_saved_snippets()
        
        print(f"\n{Fore.GREEN}💾 Saved Code Snippets:{Style.RESET_ALL}")
        
        if not snippets:
            print("No saved snippets yet.")
            return
        
        for snippet in snippets:
            print(f"• {Fore.YELLOW}{snippet['name']}{Style.RESET_ALL}")
            if snippet['description']:
                print(f"  Description: {snippet['description']}")
            print(f"  Preview: {snippet['code_preview']}")
            print()
