import subprocess
import time
import os
import platform

def is_app_installed(app_name):
    """Checks if an application is installed (cross-platform)."""
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            # mdfind kMDItemKind="Application" -name "AppName"
            cmd = ["mdfind", f"kMDItemKind==Application", "-name", app_name]
            result = subprocess.run(cmd, capture_output=True, text=True)
            paths = result.stdout.strip().split('\n')
            
            # Filter for actual .app bundles that match the name closely
            for path in paths:
                if path.endswith(".app"):
                    filename = os.path.basename(path)
                    name_only = filename.replace(".app", "")
                    # Exact match or very close match (case-insensitive)
                    if app_manager_clean_name(app_name) == app_manager_clean_name(name_only):
                        return True
            return False
            
        elif system == "Windows":
            # On Windows, try to find common apps
            # Check if it's a built-in Windows app
            common_apps = {
                "calculator": "calc.exe",
                "notepad": "notepad.exe",
                "paint": "mspaint.exe",
                "wordpad": "write.exe",
                "file explorer": "explorer.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "task manager": "taskmgr.exe",
                "control panel": "control.exe",
                "whatsapp": "WhatsApp.exe",
            }
            
            clean_name = app_manager_clean_name(app_name)
            if clean_name in common_apps:
                return True
                
            # For other apps, assume they do NOT exist unless verified
            return False
        else:
            return True  # Assume available on other platforms
            
    except Exception as e:
        print(f"Error checking app installation: {e}")
        return False

def app_manager_clean_name(name):
    return name.lower().strip()

def open_app(app_name):
    """Opens an application (cross-platform)."""
    try:
        system = platform.system()
        
        if system == "Darwin":  # macOS
            subprocess.run(["open", "-a", app_name], check=True)
            time.sleep(2)  # Wait for app to open
            return True
            
        elif system == "Windows":
            # Map common app names to Windows executables
            common_apps = {
                "calculator": "calc.exe",
                "notepad": "notepad.exe",
                "paint": "mspaint.exe",
                "wordpad": "write.exe",
                "file explorer": "explorer.exe",
                "explorer": "explorer.exe",
                "cmd": "cmd.exe",
                "powershell": "powershell.exe",
                "task manager": "taskmgr.exe",
                "control panel": "control.exe",
            }
            
            clean_name = app_manager_clean_name(app_name)
            
            # Try common apps first
            if clean_name in common_apps:
                exe = common_apps[clean_name]
                subprocess.Popen(exe, shell=True)
                time.sleep(2)
                return True
            
            # Try to launch by name directly
            try:
                subprocess.Popen(f'start "" "{app_name}"', shell=True)
                time.sleep(2)
                return True
            except (subprocess.SubprocessError, OSError) as e:
                print(f"Failed to launch {app_name}: {e}")
                # Last resort: try the app name as-is
                try:
                    subprocess.Popen(app_name, shell=True)
                    time.sleep(2)
                    return True
                except Exception as e2:
                    print(f"All launch attempts failed: {e2}")
                    return False
                
        else:  # Linux or other
            subprocess.run(["xdg-open", app_name], check=True)
            time.sleep(2)
            return True
            
    except subprocess.CalledProcessError:
        print(f"Failed to open {app_name}")
        return False
    except Exception as e:
        print(f"Error opening app: {e}")
        return False
