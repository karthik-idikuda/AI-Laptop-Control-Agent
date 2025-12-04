"""
Fast Executor - Instant Action Handler
Bypasses slow vision analysis for common tasks using direct system commands.
"""

import os
import subprocess
import time
import re
import pyautogui
from macos_commands import MacOSCommands

class FastExecutor:
    """Handles instant execution of common commands"""
    
    def __init__(self):
        self.commands = MacOSCommands.get_all_commands()
        self.apps = MacOSCommands.get_app_list()
        
    def execute(self, prompt):
        """
        Try to execute a command instantly.
        Returns: (success, message)
        """
        prompt = prompt.lower().strip()
        
        # 1. Check for Direct App Launch ("open [app]")
        if prompt.startswith("open "):
            app_name = prompt[5:].strip()
            return self._open_app(app_name)
            
        # 2. Check for Web Search ("search [query]")
        if prompt.startswith("search ") or prompt.startswith("google "):
            query = prompt.replace("search ", "").replace("google ", "").strip()
            return self._web_search(query)
            
        # 3. Check for Typing ("type [text]")
        if prompt.startswith("type ") or prompt.startswith("write "):
            text = prompt.replace("type ", "").replace("write ", "").strip()
            return self._type_text(text)
            
        # 4. Check for Predefined Commands (Exact Match)
        if prompt in self.commands:
            return self._execute_predefined(prompt)
            
        # 5. Check for Predefined Commands (Fuzzy/Partial)
        # e.g. "turn up volume" -> "volume up"
        for cmd_name, cmd_data in self.commands.items():
            if cmd_name in prompt:
                return self._execute_predefined(cmd_name)
                
        return False, "No fast command found"

    def _open_app(self, app_name):
        """Open an application using macOS 'open' command"""
        # Check if it's a known app alias
        for key, data in self.apps.items():
            if key in app_name:
                app_name = data["app"]
                break
                
        try:
            subprocess.run(["open", "-a", app_name], check=True)
            return True, f"Opened {app_name}"
        except subprocess.CalledProcessError:
            # Try generic open if -a fails (might be a file or URL)
            try:
                subprocess.run(["open", app_name], check=True)
                return True, f"Opened {app_name}"
            except:
                return False, f"Could not open {app_name}"

    def _web_search(self, query):
        """Perform a Google search"""
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        subprocess.run(["open", url])
        return True, f"Searched for '{query}'"

    def _type_text(self, text):
        """Type text directly"""
        pyautogui.write(text, interval=0.05)
        return True, f"Typed: {text}"

    def _execute_predefined(self, cmd_name):
        """Execute a command from macos_commands.py"""
        data = self.commands[cmd_name]
        
        # Handle Hotkeys
        if "keys" in data:
            keys = data["keys"]
            # Convert 'command' to 'command' (pyautogui uses 'command')
            # macos_commands might use 'cmd' or 'command', pyautogui needs 'command'
            # But wait, pyautogui on mac uses 'command'.
            
            # Fix for special keys if needed
            fixed_keys = []
            for k in keys:
                if k == "cmd": fixed_keys.append("command")
                elif k == "ctrl": fixed_keys.append("ctrl")
                elif k == "opt": fixed_keys.append("option")
                else: fixed_keys.append(k)
                
            pyautogui.hotkey(*fixed_keys)
            return True, f"Executed shortcut: {cmd_name}"
            
        # Handle System Actions
        if "action" in data:
            action = data["action"]
            cmd = data.get("command", "")
            
            if action == "system":
                if cmd == "sleep":
                    subprocess.run(["pmset", "sleepnow"])
                elif cmd == "restart":
                    subprocess.run(["osascript", "-e", 'tell app "System Events" to restart'])
                elif cmd == "shutdown":
                    subprocess.run(["osascript", "-e", 'tell app "System Events" to shut down'])
                return True, f"System action: {cmd}"
                
            elif action == "network":
                if cmd == "wifi on":
                    subprocess.run(["networksetup", "-setairportpower", "en0", "on"])
                elif cmd == "wifi off":
                    subprocess.run(["networksetup", "-setairportpower", "en0", "off"])
                return True, f"Network action: {cmd}"
                
            elif action == "bluetooth":
                # Requires blueutil usually, but we can try generic
                return False, "Bluetooth requires blueutil installed"
                
        # Handle URL
        if "url" in data:
            subprocess.run(["open", data["url"]])
            return True, f"Opened URL: {data['url']}"
            
        return False, "Command type not supported yet"