"""
Command History Manager - Saves and retrieves command history
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Any


class CommandHistory:
    """Manages command execution history"""
    
    def __init__(self, history_file: str = None):
        if history_file is None:
            # Use user's home directory
            home = os.path.expanduser("~")
            history_dir = os.path.join(home, ".osagent")
            os.makedirs(history_dir, exist_ok=True)
            self.history_file = os.path.join(history_dir, "history.json")
        else:
            self.history_file = history_file
        
        self.history: List[Dict[str, Any]] = []
        self.load()
    
    def add(self, command: str, success: bool = True, details: str = ""):
        """Add command to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "success": success,
            "details": details
        }
        self.history.append(entry)
        self.save()
    
    def get_recent(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent commands"""
        return self.history[-limit:]
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search history for matching commands"""
        query_lower = query.lower()
        return [
            entry for entry in self.history
            if query_lower in entry["command"].lower()
        ]
    
    def get_all(self) -> List[Dict[str, Any]]:
        """Get all history"""
        return self.history
    
    def clear(self):
        """Clear all history"""
        self.history = []
        self.save()
    
    def save(self):
        """Save history to file"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def load(self):
        """Load history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"Error loading history: {e}")
                self.history = []
        else:
            self.history = []
    
    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics"""
        if not self.history:
            return {
                "total_commands": 0,
                "success_rate": 0,
                "most_used": None
            }
        
        total = len(self.history)
        successful = sum(1 for entry in self.history if entry.get("success", False))
        
        # Count command frequency
        command_counts = {}
        for entry in self.history:
            cmd = entry["command"]
            command_counts[cmd] = command_counts.get(cmd, 0) + 1
        
        most_used = max(command_counts.items(), key=lambda x: x[1]) if command_counts else None
        
        return {
            "total_commands": total,
            "success_rate": (successful / total * 100) if total > 0 else 0,
            "most_used": most_used[0] if most_used else None,
            "most_used_count": most_used[1] if most_used else 0
        }
