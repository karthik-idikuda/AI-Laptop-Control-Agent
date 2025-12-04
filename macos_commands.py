"""
macOS Command Library - Predefined A-Z Commands
Complete database of macOS keyboard shortcuts, system commands, and automations.
"""

class MacOSCommands:
    """Comprehensive macOS command library"""
    
    # === SYSTEM SHORTCUTS ===
    SYSTEM_SHORTCUTS = {
        # Spotlight & Search
        "open spotlight": {"keys": ["command", "space"], "description": "Open Spotlight Search"},
        "search spotlight": {"keys": ["command", "space"], "description": "Search with Spotlight"},
        
        # Screenshots
        "take screenshot": {"keys": ["command", "shift", "3"], "description": "Capture entire screen"},
        "screenshot area": {"keys": ["command", "shift", "4"], "description": "Capture selected area"},
        "screenshot window": {"keys": ["command", "shift", "4", "space"], "description": "Capture window"},
        "screenshot touch bar": {"keys": ["command", "shift", "6"], "description": "Capture Touch Bar"},
        
        # Mission Control & Spaces
        "show mission control": {"keys": ["control", "up"], "description": "Show all windows"},
        "show desktop": {"keys": ["f11"], "description": "Show desktop"},
        "application windows": {"keys": ["control", "down"], "description": "Show app windows"},
        
        # System
        "lock screen": {"keys": ["control", "command", "q"], "description": "Lock screen"},
        "force quit": {"keys": ["command", "option", "escape"], "description": "Force quit dialog"},
        "restart": {"action": "system", "command": "restart", "description": "Restart Mac"},
        "shutdown": {"action": "system", "command": "shutdown", "description": "Shut down Mac"},
        "sleep": {"action": "system", "command": "sleep", "description": "Put Mac to sleep"},
        
        # Display
        "increase brightness": {"keys": ["f2"], "description": "Increase screen brightness"},
        "decrease brightness": {"keys": ["f1"], "description": "Decrease screen brightness"},
        
        # Volume
        "mute": {"keys": ["f10"], "description": "Mute audio"},
        "volume up": {"keys": ["f12"], "description": "Increase volume"},
        "volume down": {"keys": ["f11"], "description": "Decrease volume"},
        
        # Keyboard
        "show emoji": {"keys": ["control", "command", "space"], "description": "Show emoji picker"},
        "character viewer": {"keys": ["control", "command", "space"], "description": "Show characters"},
    }
    
    # === APPLICATION COMMANDS ===
    APPLICATIONS = {
        # Productivity
        "calculator": {"app": "Calculator", "category": "utility"},
        "calendar": {"app": "Calendar", "category": "productivity"},
        "contacts": {"app": "Contacts", "category": "productivity"},
        "reminders": {"app": "Reminders", "category": "productivity"},
        "notes": {"app": "Notes", "category": "productivity"},
        "mail": {"app": "Mail", "category": "productivity"},
        "messages": {"app": "Messages", "category": "communication"},
        "facetime": {"app": "FaceTime", "category": "communication"},
        
        # Development
        "terminal": {"app": "Terminal", "category": "development"},
        "xcode": {"app": "Xcode", "category": "development"},
        
        # Creativity
        "photos": {"app": "Photos", "category": "media"},
        "photo booth": {"app": "Photo Booth", "category": "media"},
        "preview": {"app": "Preview", "category": "utility"},
        "quicktime": {"app": "QuickTime Player", "category": "media"},
        "music": {"app": "Music", "category": "media"},
        "podcasts": {"app": "Podcasts", "category": "media"},
        "tv": {"app": "TV", "category": "media"},
        "books": {"app": "Books", "category": "media"},
        
        # Browsers
        "safari": {"app": "Safari", "category": "internet"},
        "chrome": {"app": "Google Chrome", "category": "internet"},
        "firefox": {"app": "Firefox", "category": "internet"},
        "edge": {"app": "Microsoft Edge", "category": "internet"},
        
        # System
        "finder": {"app": "Finder", "category": "system"},
        "system preferences": {"app": "System Preferences", "category": "system"},
        "system settings": {"app": "System Settings", "category": "system"},
        "activity monitor": {"app": "Activity Monitor", "category": "utility"},
        "disk utility": {"app": "Disk Utility", "category": "utility"},
        "keychain access": {"app": "Keychain Access", "category": "utility"},
        "console": {"app": "Console", "category": "utility"},
        
        # Office
        "pages": {"app": "Pages", "category": "productivity"},
        "numbers": {"app": "Numbers", "category": "productivity"},
        "keynote": {"app": "Keynote", "category": "productivity"},
        
        # App Store
        "app store": {"app": "App Store", "category": "system"},
    }
    
    # === FINDER SHORTCUTS ===
    FINDER_SHORTCUTS = {
        "new finder window": {"keys": ["command", "n"], "app": "Finder"},
        "new folder": {"keys": ["command", "shift", "n"], "app": "Finder"},
        "open file": {"keys": ["command", "o"], "app": "Finder"},
        "close window": {"keys": ["command", "w"], "app": "Finder"},
        "get info": {"keys": ["command", "i"], "app": "Finder"},
        "duplicate": {"keys": ["command", "d"], "app": "Finder"},
        "make alias": {"keys": ["command", "l"], "app": "Finder"},
        "show original": {"keys": ["command", "r"], "app": "Finder"},
        "add to dock": {"keys": ["control", "shift", "command", "t"], "app": "Finder"},
        "quick look": {"keys": ["space"], "app": "Finder"},
        "move to trash": {"keys": ["command", "delete"], "app": "Finder"},
        "empty trash": {"keys": ["command", "shift", "delete"], "app": "Finder"},
        "go to folder": {"keys": ["command", "shift", "g"], "app": "Finder"},
        "go to home": {"keys": ["command", "shift", "h"], "app": "Finder"},
        "go to desktop": {"keys": ["command", "shift", "d"], "app": "Finder"},
        "go to documents": {"keys": ["command", "shift", "o"], "app": "Finder"},
        "go to downloads": {"keys": ["command", "option", "l"], "app": "Finder"},
        "go to applications": {"keys": ["command", "shift", "a"], "app": "Finder"},
        "go to utilities": {"keys": ["command", "shift", "u"], "app": "Finder"},
    }
    
    # === TEXT EDITING SHORTCUTS ===
    TEXT_SHORTCUTS = {
        "select all": {"keys": ["command", "a"], "description": "Select all text"},
        "copy": {"keys": ["command", "c"], "description": "Copy"},
        "cut": {"keys": ["command", "x"], "description": "Cut"},
        "paste": {"keys": ["command", "v"], "description": "Paste"},
        "undo": {"keys": ["command", "z"], "description": "Undo"},
        "redo": {"keys": ["command", "shift", "z"], "description": "Redo"},
        "bold": {"keys": ["command", "b"], "description": "Bold text"},
        "italic": {"keys": ["command", "i"], "description": "Italic text"},
        "underline": {"keys": ["command", "u"], "description": "Underline text"},
        "save": {"keys": ["command", "s"], "description": "Save"},
        "save as": {"keys": ["command", "shift", "s"], "description": "Save as"},
        "print": {"keys": ["command", "p"], "description": "Print"},
        "find": {"keys": ["command", "f"], "description": "Find"},
        "replace": {"keys": ["command", "option", "f"], "description": "Find and replace"},
    }
    
    # === SAFARI SHORTCUTS ===
    SAFARI_SHORTCUTS = {
        "new tab": {"keys": ["command", "t"], "app": "Safari"},
        "new window": {"keys": ["command", "n"], "app": "Safari"},
        "new private window": {"keys": ["command", "shift", "n"], "app": "Safari"},
        "close tab": {"keys": ["command", "w"], "app": "Safari"},
        "reopen closed tab": {"keys": ["command", "shift", "t"], "app": "Safari"},
        "next tab": {"keys": ["control", "tab"], "app": "Safari"},
        "previous tab": {"keys": ["control", "shift", "tab"], "app": "Safari"},
        "reload page": {"keys": ["command", "r"], "app": "Safari"},
        "stop loading": {"keys": ["command", "."], "app": "Safari"},
        "show bookmarks": {"keys": ["command", "option", "b"], "app": "Safari"},
        "add bookmark": {"keys": ["command", "d"], "app": "Safari"},
        "show downloads": {"keys": ["command", "option", "l"], "app": "Safari"},
        "show history": {"keys": ["command", "y"], "app": "Safari"},
        "clear history": {"keys": ["command", "option", "e"], "app": "Safari"},
        "zoom in": {"keys": ["command", "+"], "app": "Safari"},
        "zoom out": {"keys": ["command", "-"], "app": "Safari"},
        "actual size": {"keys": ["command", "0"], "app": "Safari"},
        "full screen": {"keys": ["control", "command", "f"], "app": "Safari"},
    }
    
    # === WIFI & NETWORK ===
    NETWORK_COMMANDS = {
        "turn on wifi": {"action": "network", "command": "wifi on", "description": "Enable WiFi"},
        "turn off wifi": {"action": "network", "command": "wifi off", "description": "Disable WiFi"},
        "turn on bluetooth": {"action": "bluetooth", "command": "on", "description": "Enable Bluetooth"},
        "turn off bluetooth": {"action": "bluetooth", "command": "off", "description": "Disable Bluetooth"},
        "turn on airplane mode": {"action": "airplane", "command": "on", "description": "Enable airplane mode"},
        "turn off airplane mode": {"action": "airplane", "command": "off", "description": "Disable airplane mode"},
    }
    
    # === FILE OPERATIONS ===
    FILE_OPERATIONS = {
        "create file": {"action": "file", "operation": "create"},
        "delete file": {"action": "file", "operation": "delete"},
        "rename file": {"action": "file", "operation": "rename"},
        "move file": {"action": "file", "operation": "move"},
        "copy file": {"action": "file", "operation": "copy"},
        "compress": {"action": "file", "operation": "compress"},
        "extract": {"action": "file", "operation": "extract"},
    }
    
    # === WINDOW MANAGEMENT ===
    WINDOW_SHORTCUTS = {
        "minimize": {"keys": ["command", "m"], "description": "Minimize window"},
        "hide app": {"keys": ["command", "h"], "description": "Hide application"},
        "hide others": {"keys": ["command", "option", "h"], "description": "Hide other apps"},
        "show all": {"keys": ["command", "option", "h"], "description": "Show all windows"},
        "close window": {"keys": ["command", "w"], "description": "Close window"},
        "quit app": {"keys": ["command", "q"], "description": "Quit application"},
        "cycle windows": {"keys": ["command", "`"], "description": "Cycle through windows"},
        "full screen": {"keys": ["control", "command", "f"], "description": "Toggle fullscreen"},
    }
    
    # === VOICE & ACCESSIBILITY ===
    ACCESSIBILITY = {
        "start dictation": {"keys": ["fn", "fn"], "description": "Start voice dictation"},
        "enable voice over": {"keys": ["command", "f5"], "description": "Toggle VoiceOver"},
        "zoom in": {"keys": ["command", "option", "+"], "description": "Zoom in (accessibility)"},
        "zoom out": {"keys": ["command", "option", "-"], "description": "Zoom out (accessibility)"},
        "invert colors": {"keys": ["control", "command", "option", "8"], "description": "Invert colors"},
    }
    
    # === QUICK ACTIONS (Alphabetical A-Z) ===
    QUICK_ACTIONS = {
        # A
        "activate siri": {"keys": ["command", "space"], "hold": True, "description": "Activate Siri"},
        "app switcher": {"keys": ["command", "tab"], "description": "Switch applications"},
        
        # B
        "back": {"keys": ["command", "["], "description": "Go back"},
        "bluetooth settings": {"app": "System Settings", "navigate": "Bluetooth"},
        
        # C
        "close all windows": {"keys": ["command", "option", "w"], "description": "Close all windows"},
        "copy screenshot to clipboard": {"keys": ["command", "control", "shift", "4"], "description": "Screenshot to clipboard"},
        
        # D
        "dock preferences": {"app": "System Settings", "navigate": "Desktop & Dock"},
        "do not disturb": {"action": "notification_center", "command": "dnd toggle"},
        
        # E
        "eject": {"keys": ["command", "e"], "description": "Eject disk"},
        "energy saver": {"app": "System Settings", "navigate": "Battery"},
        
        # F
        "forward": {"keys": ["command", "]"], "description": "Go forward"},
        "find cursor": {"shake": "mouse", "description": "Shake mouse to find cursor"},
        
        # G
        "go to line": {"keys": ["command", "l"], "description": "Go to line (text editors)"},
        "grab screenshot": {"keys": ["command", "shift", "5"], "description": "Screenshot & recording options"},
        
        # H
        "home page": {"keys": ["command", "home"], "description": "Go to home page"},
        "help menu": {"keys": ["command", "shift", "?"], "description": "Open help menu"},
        
        # I
        "inspector": {"keys": ["command", "option", "i"], "description": "Web inspector"},
        "icloud settings": {"app": "System Settings", "navigate": "Apple ID"},
        
        # J (JavaScript console for browsers)
        "javascript console": {"keys": ["command", "option", "j"], "description": "Open JS console"},
        
        # K (Keyboard shortcuts)
        "keyboard settings": {"app": "System Settings", "navigate": "Keyboard"},
        
        # L
        "location bar": {"keys": ["command", "l"], "description": "Focus address bar"},
        "launchpad": {"keys": ["f4"], "description": "Open Launchpad"},
        
        # M
        "mail new message": {"keys": ["command", "n"], "app": "Mail"},
        "minimize all": {"keys": ["command", "option", "m"], "description": "Minimize all windows"},
        
        # N
        "notification center": {"keys": ["fn", "n"], "description": "Show notifications"},
        "network settings": {"app": "System Settings", "navigate": "Network"},
        
        # O
        "open location": {"keys": ["command", "shift", "g"], "description": "Go to folder path"},
        
        # P
        "page down": {"keys": ["pagedown"], "description": "Scroll down one page"},
        "page up": {"keys": ["pageup"], "description": "Scroll up one page"},
        "privacy settings": {"app": "System Settings", "navigate": "Privacy & Security"},
        
        # Q
        "quit all": {"action": "quit_all_apps", "description": "Quit all applications"},
        
        # R
        "refresh": {"keys": ["command", "r"], "description": "Refresh/Reload"},
        "recently opened": {"keys": ["command", "shift", "t"], "description": "Recently closed tabs"},
        
        # S
        "share": {"keys": ["command", "shift", "s"], "description": "Share menu"},
        "show hidden files": {"keys": ["command", "shift", "."], "app": "Finder"},
        "sound settings": {"app": "System Settings", "navigate": "Sound"},
        
        # T
        "terminal new tab": {"keys": ["command", "t"], "app": "Terminal"},
        "text size larger": {"keys": ["command", "+"], "description": "Increase text size"},
        "text size smaller": {"keys": ["command", "-"], "description": "Decrease text size"},
        
        # U
        "users settings": {"app": "System Settings", "navigate": "Users & Groups"},
        
        # V
        "view options": {"keys": ["command", "j"], "app": "Finder"},
        "voice control": {"keys": ["fn", "command", "f5"], "description": "Toggle voice control"},
        
        # W
        "wallpaper settings": {"app": "System Settings", "navigate": "Wallpaper"},
        "wifi settings": {"app": "System Settings", "navigate": "Wi-Fi"},
        
        # X (Extra shortcuts)
        "cut line": {"keys": ["command", "x"], "description": "Cut line"},
        
        # Y (YouTube and other Y actions)
        "youtube": {"url": "https://youtube.com", "description": "Open YouTube"},
        
        # Z
        "zoom toggle": {"keys": ["command", "option", "8"], "description": "Toggle zoom"},
    }
    
    @classmethod
    def get_all_commands(cls):
        """Get all available commands"""
        all_commands = {}
        all_commands.update(cls.SYSTEM_SHORTCUTS)
        all_commands.update(cls.FINDER_SHORTCUTS)
        all_commands.update(cls.TEXT_SHORTCUTS)
        all_commands.update(cls.SAFARI_SHORTCUTS)
        all_commands.update(cls.NETWORK_COMMANDS)
        all_commands.update(cls.FILE_OPERATIONS)
        all_commands.update(cls.WINDOW_SHORTCUTS)
        all_commands.update(cls.ACCESSIBILITY)
        all_commands.update(cls.QUICK_ACTIONS)
        return all_commands
    
    @classmethod
    def search_command(cls, query):
        """Search for a command by name"""
        query_lower = query.lower()
        all_commands = cls.get_all_commands()
        
        # Exact match
        if query_lower in all_commands:
            return {query_lower: all_commands[query_lower]}
        
        # Partial match
        matches = {}
        for cmd_name, cmd_data in all_commands.items():
            if query_lower in cmd_name or any(query_lower in word for word in cmd_name.split()):
                matches[cmd_name] = cmd_data
        
        return matches
    
    @classmethod
    def get_app_list(cls):
        """Get list of all applications"""
        return cls.APPLICATIONS
    
    @classmethod
    def execute_shortcut(cls, shortcut_name):
        """Execute a predefined shortcut"""
        all_commands = cls.get_all_commands()
        
        if shortcut_name.lower() not in all_commands:
            return None
        
        command_data = all_commands[shortcut_name.lower()]
        
        if "keys" in command_data:
            from computer_control import hotkey
            keys = command_data["keys"]
            hotkey(*keys)
            return {"success": True, "type": "hotkey", "keys": keys}
        
        elif "app" in command_data:
            from app_manager import open_app
            app = command_data.get("app")
            if open_app(app):
                return {"success": True, "type": "app", "app": app}
            return {"success": False, "type": "app", "app": app}
        
        elif "url" in command_data:
            from browser_controller import open_url
            url = command_data["url"]
            if open_url(url):
                return {"success": True, "type": "url", "url": url}
            return {"success": False, "type": "url", "url": url}
        
        elif "action" in command_data:
            return {"success": False, "type": "action", "action": command_data["action"], 
                    "note": "Requires system-level permissions"}
        
        return None
