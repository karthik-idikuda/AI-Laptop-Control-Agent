"""
Global Keyboard Shortcuts - System-wide hotkeys for agent control
"""

from pynput import keyboard
from pynput.keyboard import Key, KeyCode
import threading
from typing import Callable, Optional


class GlobalShortcuts:
    """Manages global keyboard shortcuts"""
    
    def __init__(self):
        self.listener: Optional[keyboard.Listener] = None
        self.callbacks = {}
        self.current_keys = set()
        
    def register(self, keys: list, callback: Callable):
        """
        Register a keyboard shortcut
        
        Args:
            keys: List of keys (e.g., [Key.cmd, KeyCode.from_char('a')])
            callback: Function to call when shortcut is pressed
        """
        # Convert to hashable tuple
        key_combo = frozenset(self._normalize_keys(keys))
        self.callbacks[key_combo] = callback
    
    def _normalize_keys(self, keys):
        """Normalize keys to a consistent format"""
        normalized = []
        for key in keys:
            if isinstance(key, str):
                # Convert string to KeyCode
                normalized.append(KeyCode.from_char(key.lower()))
            else:
                normalized.append(key)
        return normalized
    
    def start(self):
        """Start listening for shortcuts"""
        if self.listener is None or not self.listener.running:
            self.listener = keyboard.Listener(
                on_press=self._on_press,
                on_release=self._on_release
            )
            self.listener.start()
            print("🎹 Global shortcuts enabled")
    
    def stop(self):
        """Stop listening for shortcuts"""
        if self.listener and self.listener.running:
            self.listener.stop()
            print("🎹 Global shortcuts disabled")
    
    def _on_press(self, key):
        """Handle key press"""
        self.current_keys.add(key)
        
        # Check if current combination matches any registered shortcut
        current_combo = frozenset(self.current_keys)
        if current_combo in self.callbacks:
            # Execute callback in separate thread to not block listener
            callback = self.callbacks[current_combo]
            threading.Thread(target=callback, daemon=True).start()
    
    def _on_release(self, key):
        """Handle key release"""
        if key in self.current_keys:
            self.current_keys.remove(key)


# Global instance
global_shortcuts = GlobalShortcuts()


# Convenience functions for macOS shortcuts
def cmd_shift(char: str):
    """Create Cmd+Shift+char combination"""
    return [Key.cmd, Key.shift, char]

def cmd_key(char: str):
    """Create Cmd+char combination"""
    return [Key.cmd, char]

def ctrl_key(char: str):
    """Create Ctrl+char combination"""
    return [Key.ctrl, char]
