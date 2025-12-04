"""
Computer Control Module - Mouse and Keyboard Automation
Uses pyautogui for cross-platform control.
"""

import pyautogui
import time
import platform

# Fail-safe to prevent runaway scripts
pyautogui.FAILSAFE = True

def click(x, y):
    """Moves the mouse to (x, y) and clicks."""
    try:
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Error clicking at ({x}, {y}): {e}")
        return False

def type_text(text):
    """Types the given text."""
    try:
        pyautogui.write(text, interval=0.05)
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Error typing text: {e}")
        return False

def press_key(key):
    """Presses a specific key (e.g., 'enter', 'space')."""
    try:
        pyautogui.press(key)
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Error pressing key {key}: {e}")
        return False

def hotkey(*keys):
    """Press a combination of keys (e.g., cmd+l for address bar)."""
    try:
        pyautogui.hotkey(*keys)
        time.sleep(0.5)
        return True
    except Exception as e:
        print(f"Error pressing hotkey {keys}: {e}")
        return False

def focus_browser_search():
    """Focus the browser search/address bar using keyboard shortcut."""
    if platform.system() == "Darwin":  # macOS
        return hotkey('command', 'l')
    else:  # Windows/Linux
        return hotkey('ctrl', 'l')

def get_screen_size():
    """Returns the screen width and height."""
    return pyautogui.size()
