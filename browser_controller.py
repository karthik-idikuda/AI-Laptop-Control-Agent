"""
Browser Controller Module - macOS Compatible
Opens URLs in Safari, Chrome, or default browser.
"""

import subprocess
import time
import platform

def open_url(url):
    """Opens a URL in the default browser (cross-platform, macOS-optimized)."""
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            # Use 'open' command which respects default browser
            subprocess.run(["open", url], check=True)
            time.sleep(2)  # Wait for browser to open
            return True
            
        elif system == "Windows":
            import webbrowser
            webbrowser.open(url)
            time.sleep(2)
            return True
            
        else:  # Linux
            subprocess.run(["xdg-open", url], check=True)
            time.sleep(2)
            return True
            
    except Exception as e:
        print(f"Error opening URL: {e}")
        return False

def open_url_in_browser(url, browser_name="Safari"):
    """
    Opens a URL in a specific browser on macOS.
    
    Args:
        url: The URL to open
        browser_name: Browser app name (e.g., "Safari", "Google Chrome", "Firefox")
    """
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            subprocess.run(["open", "-a", browser_name, url], check=True)
            time.sleep(2)
            return True
        else:
            # Fallback to default browser on other platforms
            return open_url(url)
            
    except Exception as e:
        print(f"Error opening URL in {browser_name}: {e}")
        # Fallback to default browser
        return open_url(url)
