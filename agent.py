import time
import sys
import argparse
import threading
from urllib.parse import quote_plus
from app_manager import is_app_installed, open_app
from browser_controller import open_url
from vision_analyzer import capture_screen, analyze_screen
from computer_control import click, type_text, press_key, focus_browser_search
from action_verifier import verifier
import platform
from openrouter_compat import genai
from config import MODEL_NAME, API_KEY

class OSAgent:
    def __init__(self, model_name=MODEL_NAME, logger_callback=None):
        self.model_name = model_name
        self.logger_callback = logger_callback
        self.history = []
        
        # Initialize Gemini
        try:
            genai.configure(api_key=API_KEY)
        except Exception as e:
            self.log(f"Error configuring Gemini API: {e}. Please ensure API_KEY is set in config.py")
            sys.exit(1) # Exit if API key is not configured

        self.stop_flag = False
        # Basic control diagnostics
        try:
            import pyautogui
            start_pos = pyautogui.position()
            pyautogui.moveTo(10, 10, duration=0.2)
            pyautogui.moveTo(start_pos.x, start_pos.y, duration=0.2)
            self.log("✅ Input control diagnostic passed (mouse moved). If clicks still fail, grant Accessibility permissions in macOS: System Settings > Privacy & Security > Accessibility > enable Terminal/Python.")
        except Exception as e:
            self.log(f"⚠️ Input control diagnostic failed: {e}. You may need to grant Accessibility + Screen Recording permissions.")

    def log(self, message):
        print(message)
        if self.logger_callback:
            self.logger_callback(message)
    
    def run_with_plan(self, user_command, intent, plan):
        """Execute an AI-generated plan step by step using vision and Gemini.
        
        Args:
            user_command: Original user command
            intent: Parsed intent from IntentAnalyzer
            plan: Execution plan from ActionPlanner
        """
        self.stop_flag = False
        self.log("="*70)
        self.log(f"🎯 EXECUTING: {user_command}")
        self.log(f"📋 Plan: {intent.get('natural_response', 'AI-generated plan')}")
        self.log("="*70)
        
        for step in plan:
            if self.stop_flag:
                self.log("⚠️ Execution stopped by user")
                break
            
            step_num = step.get('step_number', 0)
            action_type = step.get('action_type', 'UNKNOWN')
            target = step.get('target', '')
            value = step.get('value', '')
            description = step.get('description', 'No description')
            
            self.log(f"\n📍 Step {step_num}: {description}")
            
            try:
                if action_type == 'OPEN_APP':
                    self._execute_open_app(target, value)
                elif action_type == 'WAIT':
                    self._execute_wait(target, value)
                elif action_type == 'FIND_AND_CLICK':
                    self._execute_find_and_click(target)
                elif action_type == 'TYPE':
                    self._execute_type(value)
                elif action_type == 'PRESS':
                    self._execute_press(value)
                elif action_type == 'VERIFY':
                    self._execute_verify(target)
                else:
                    self.log(f"⚠️ Unknown action type: {action_type}")
                
                time.sleep(1)  # Brief pause between steps
                
            except Exception as e:
                self.log(f"❌ Step {step_num} failed: {e}")
                # Continue to next step anyway
        
        self.log("\n" + "="*70)
        self.log("✅ Execution complete")
        self.log("="*70)
    
    def _execute_open_app(self, app_name, method='spotlight'):
        """Open an application."""
        self.log(f"  🚀 Opening {app_name}...")
        
        system = platform.system()
        
        # Use Spotlight only on macOS and if requested
        if method == 'spotlight' and system == 'Darwin':
            from computer_control import hotkey, type_text, press_key
            # Open Spotlight
            hotkey('command', 'space')
            time.sleep(0.5)
            # Type app name
            type_text(app_name)
            time.sleep(0.5)
            # Press Enter
            press_key('enter')
            time.sleep(3)  # Wait for app to open
            self.log(f"  ✅ Opened {app_name}")
        else:
            # Fallback to app_manager (works for Windows/Linux too)
            if open_app(app_name):
                time.sleep(3)
                self.log(f"  ✅ Opened {app_name}")
            else:
                self.log(f"  ⚠️ Could not open {app_name} (Desktop App)")
                self.log(f"  🔄 Attempting browser fallback...")
                
                fallback_url = self.get_browser_fallback_url(app_name)
                self.log(f"  🌐 Opening URL: {fallback_url}")
                
                # Use browser controller to open URL
                open_url(fallback_url)
                time.sleep(5)
                self.log(f"  ✅ Opened browser fallback")

    def get_browser_fallback_url(self, app_name):
        """Ask AI for a fallback URL for the given app."""
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            prompt = f"""User wants to open '{app_name}' but the desktop app is not installed.
            Provide a direct URL to use this application in the browser (e.g., https://web.whatsapp.com for WhatsApp, https://www.spotify.com for Spotify).
            
            If there is no direct web app, provide a Google Search URL for it.
            
            Return ONLY the URL, nothing else."""
            
            response = model.generate_content(prompt)
            url = response.text.strip()
            return url
        except Exception as e:
            self.log(f"Error getting fallback URL: {e}")
            return f"https://www.google.com/search?q={app_name}"
    
    def _execute_wait(self, condition, seconds):
        """Wait for a condition or duration."""
        try:
            wait_time = float(seconds)
        except (ValueError, TypeError) as e:
            self.log(f"Invalid wait time '{seconds}', using default 2s")
            wait_time = 2.0
        
        self.log(f"  ⏳ Waiting {wait_time}s for: {condition}")
        time.sleep(wait_time)
        self.log(f"  ✅ Wait complete")
    
    def _execute_find_and_click(self, target_description):
        """Find an element using vision and click it."""
        self.log(f"  🔍 Finding: {target_description}")
        
        # Capture current screen
        screenshot_path = capture_screen("current_screen.png")
        if not screenshot_path:
            self.log("  ❌ Could not capture screen")
            return
        
        # Use Gemini vision to analyze and find coordinates
        analysis_prompt = f"""Analyze this screenshot and find: {target_description}

Return a JSON object with:
{{
  "found": true/false,
  "coordinates": [x, y],
  "confidence": 0.0-1.0,
  "description": "what you see"
}}

If you cannot find it, set found to false and explain why."""
        
        try:
            # analyze_screen returns a dict
            result = analyze_screen(screenshot_path, analysis_prompt)
            
            if isinstance(result, dict):
                # Check for 'coordinates' directly (SYSTEM_PROMPT format) or 'found' (Prompt override format)
                coords = result.get('coordinates')
                if coords:
                    x, y = coords
                    self.log(f"  📍 Found at ({x}, {y}) - {result.get('description', result.get('thought', ''))}")
                    click(int(x), int(y))
                    time.sleep(0.5)
                    self.log(f"  ✅ Clicked on {target_description}")
                elif result.get('found') and result.get('coordinates'):
                    x, y = result['coordinates']
                    self.log(f"  📍 Found at ({x}, {y}) - {result.get('description')}")
                    click(int(x), int(y))
                    time.sleep(0.5)
                    self.log(f"  ✅ Clicked on {target_description}")
                else:
                    self.log(f"  ⚠️ Not found: {result.get('description', result.get('thought', 'unknown reason'))}")
            else:
                self.log(f"  ⚠️ Unexpected analysis result type: {type(result)}")
        
        except Exception as e:
            self.log(f"  ❌ Error finding element: {e}")
    
    def _execute_type(self, text):
        """Type text."""
        self.log(f"  ⌨️  Typing: {text}")
        type_text(text)
        time.sleep(0.3)
        self.log(f"  ✅ Typed text")
    
    def _execute_press(self, key):
        """Press a key."""
        self.log(f"  🔘 Pressing: {key}")
        press_key(key)
        time.sleep(0.3)
        self.log(f"  ✅ Pressed {key}")
    
    def _execute_verify(self, target):
        """Verify something on screen."""
        self.log(f"  🔎 Verifying: {target}")
        
        try:
            # Use the ActionVerifier which uses Gemini Vision
            result = verifier.verify_action("Verifying step", target)
            
            if result.get('success'):
                 self.log(f"  ✅ Verification passed: {result.get('what_happened')}")
            else:
                 self.log(f"  ⚠️ Verification warning: {result.get('what_happened')}")
        except Exception as e:
            self.log(f"  ⚠️ Verification failed with error: {e}")


    def stop(self):
        self.stop_flag = True

    def perform_google_search(self, query):
        """Open Google search results for the given query."""
        encoded = quote_plus(query)
        search_url = f"https://www.google.com/search?q={encoded}"
        self.log(f"Opening Google search for: {query}")
        open_url(search_url)
        time.sleep(5)

    def capture_diagnostic(self, label):
        """Capture a screenshot for debugging purposes."""
        timestamp = int(time.time())
        path = capture_screen(f"{label}_{timestamp}.png")
        if path:
            self.log(f"📸 Diagnostic screenshot saved: {path}")
        else:
            self.log("⚠️ Unable to capture diagnostic screenshot.")
        return path

    # --- Heuristic Support ---
    def apply_contextual_heuristics(self, user_command, history):
        """Perform heuristic UI interactions when AI vision lacks precise coordinates.

        Scenarios:
        - YouTube play request: attempt to focus address bar and load search if not done; click first result region.
        - Generic search request: press Cmd+L (or Ctrl+L) and retype refined query.
        Returns True if a heuristic action was attempted.
        """
        lc = user_command.lower()
        tried = False
        try:
            import platform, pyautogui
            is_mac = platform.system() == 'Darwin'
            screen_w, screen_h = pyautogui.size()

            def focus_location_bar():
                from computer_control import hotkey
                if is_mac:
                    hotkey('command', 'l')
                else:
                    hotkey('ctrl', 'l')
                time.sleep(0.5)

            # Heuristic for YouTube play
            if 'youtube' in lc and 'play' in lc:
                # If we have not yet typed a search (no TYPED history mentioning youtube.com/results)
                if not any('youtube.com/results' in h for h in history):
                    self.log("🎯 Heuristic: Focusing URL bar for YouTube search")
                    focus_location_bar()
                    query = lc
                    for word in ['open', 'youtube', 'and', 'play', 'the', 'song', 'video']:
                        query = query.replace(word, '')
                    query = query.strip() or 'music'
                    search_url = f"https://www.youtube.com/results?search_query={quote_plus(query)}"
                    self.log(f"Typing heuristic YouTube search URL: {search_url}")
                    type_text(search_url)
                    press_key('enter')
                    tried = True
                    time.sleep(4)
                # Attempt heuristic click in results region (approx first video tile)
                self.log("🎯 Heuristic: Attempting click in first video region")
                first_tile = (int(screen_w * 0.35), int(screen_h * 0.40))
                click(first_tile[0], first_tile[1])
                tried = True

            # Generic search heuristic if repeated failures
            elif 'open' in lc and ('search' in lc or 'find' in lc or 'google' in lc):
                self.log("🔍 Heuristic: Performing Google search fallback")
                focus_location_bar()
                refined = lc
                for word in ['open', 'search', 'google', 'find']:
                    refined = refined.replace(word, '')
                refined = refined.strip() or 'information'
                url = f"https://www.google.com/search?q={quote_plus(refined)}"
                type_text(url)
                press_key('enter')
                tried = True

        except Exception as e:
            self.log(f"⚠️ Heuristic error: {e}")
        return tried

    def run(self, user_command, intent=None):
        self.stop_flag = False
        self.log(f"Received command: {user_command}")
        
        # If intent is provided and it's conversational, skip execution
        if intent:
            intent_type = intent.get('intent_type', '')
            if intent_type in ['greeting', 'question', 'thanks', 'unknown']:
                self.log("✅ Conversational message - no automation needed")
                return
            
            # Use the provided intent instead of parsing again
            self.log(f"📋 Using AI-analyzed intent: {intent.get('intent_type', 'general')}")
            
            # Check for specific app/website context
            app_context = intent.get('app_context')
            target_app = intent.get('target_app')
            action = intent.get('action')
            params = intent.get('parameters', {})
            
            # For backwards compatibility, check if target_app could be a website
            # But prioritize trying as desktop app first
            target_website = None
        else:
            # Fallback to command parser if no intent provided
            from command_parser import parse_command
            intent_data = parse_command(user_command)
            target_app = intent_data.get('target_app')
            target_website = intent_data.get('target_website')
            action = intent_data.get('action')
            params = intent_data.get('params', {})

        # === PRIORITY 1: WEBSITES (including YouTube) ===
        # Handle specific websites directly, especially those that might be mistaken for desktop apps
        if target_website or target_app in ['youtube', 'gmail', 'linkedin', 'facebook', 'twitter', 'instagram']:
            # Special handling for YouTube
            if target_website == "youtube" or target_app == "youtube":
                youtube_url = "https://www.youtube.com"
                
                # Check if there's a search query in intent params
                search_query = None
                
                # Try to get from params
                if params:
                    search_query = params.get('query') or params.get('search_query')
                
                # Fallback: Try to extract from command string if not in params
                if not search_query and 'play' in user_command.lower():
                    import re
                    # Match "play [something]" or "play [something] on youtube"
                    match = re.search(r'play\s+(.*?)(?:\s+on\s+youtube|$)', user_command, re.IGNORECASE)
                    if match:
                        search_query = match.group(1).strip()
                
                if search_query:
                    # Direct YouTube search URL
                    youtube_url = f"https://www.youtube.com/results?search_query={quote_plus(search_query)}"
                    self.log(f"🎵 Opening YouTube with search: {search_query}")
                else:
                    self.log(f"🎵 Opening YouTube")
                
                # Open YouTube in browser
                if open_url(youtube_url):
                    self.log("✅ YouTube opened in browser")
                    time.sleep(11)  # Wait for page load and search results
                    
                    # If search query exists, vision loop will click on first video
                    if search_query:
                        self.log("🔍 Waiting for search results...")
                        time.sleep(3)
                        # DO NOT RETURN - continue to vision loop below
                    else:
                        return  # No search, just opened YouTube home
                else:
                    self.log("❌ Failed to open YouTube")
                    return # Exit run function after handling YouTube directly

            # Generic website handling for other prioritized sites
            self.log(f"🌐 Website detected: {target_website or target_app}")
            fallback_url = self.get_browser_fallback_url(target_website or target_app)
            self.log(f"Opening URL: {fallback_url}")
            open_url(fallback_url)
            
            # Wait longer for website to load
            self.log("⏳ Waiting for website to load...")
            time.sleep(8)
            self.log("⏳ Ensuring page is fully loaded...")
            time.sleep(3)
            
            # Special handling for specific sites (e.g., WhatsApp)
            if target_website == 'whatsapp' and action == 'send':
                self.log("Using WhatsApp Web send flow...")
                press_key('ctrl+f')
                time.sleep(0.5)
                if 'contact' in params:
                    self.log(f"Typing contact: {params['contact']}")
                    type_text(params['contact'])
                    press_key('enter')
                    time.sleep(1)
                if 'message' in params:
                    self.log(f"Typing message: {params['message']}")
                    type_text(params['message'])
                    press_key('enter')
                    
        # ---- PRIORITY 2: Try Desktop App First (if not handled as a prioritized website) ----
        elif target_app:
            self.log(f"🎯 Target app detected: {target_app}")
            
            # Try to open as desktop application
            if open_app(target_app):
                self.log(f"✅ Opened desktop app: {target_app}")
                self.log("⏳ Waiting for app to load...")
                time.sleep(8)
                # Continue to vision loop for automation
            else:
                # Desktop app not found - try web fallback
                self.log(f"⚠️ Desktop app '{target_app}' not found")
                self.log(f"🌐 Trying web version...")
                fallback_url = self.get_browser_fallback_url(target_app)
                self.log(f"Opening URL: {fallback_url}")
                open_url(fallback_url)
                
                # Wait for website to load
                self.log("⏳ Waiting for website to load...")
                time.sleep(8)
                self.log("⏳ Ensuring page is fully loaded...")
                time.sleep(3)
                
        # ---- PRIORITY 3: Search queries ----
        else:
            self.log("No specific app or website detected.")
            # Only do Google search if this is truly a search query
            if action and 'search' in action.lower():
                self.perform_google_search(user_command)
                time.sleep(5)
            else:
                self.log("⚠️ No clear action - will attempt with vision analysis")

        # ---- Continue with vision loop as before ----
        history = []
        max_steps = 30  # Increased for complex multi-step tasks
        last_action = None
        repeat_count = 0
        google_replan_triggered = False
        
        for step in range(max_steps):
            if self.stop_flag:
                self.log("🛑 Agent stopped by user.")
                break

            self.log(f"\n--- Step {step + 1} ---")
            
            # 1. Capture
            screenshot_path = capture_screen(f"step_{step}.png")
            if not screenshot_path:
                self.log("❌ Failed to capture screen. Aborting.")
                break

            # 2. Analyze with full history context (last 5 actions for better context)
            self.log("Analyzing screen...")
            recent_history = history[-5:] if len(history) > 5 else history
            history_str = "\n".join([f"Step {i+1}: {h}" for i, h in enumerate(recent_history)])
            
            try:
                analysis = analyze_screen(screenshot_path, user_command, history_str)
            except Exception as e:
                self.log(f"❌ Analysis error: {e}")
                self.capture_diagnostic("analysis_error")
                
                # Don't trigger Google search on early steps - page might still be loading
                if step < 3:
                    self.log("⏳ Page might still be loading, waiting longer...")
                    time.sleep(5)
                    continue
                elif not google_replan_triggered:
                    self.log("Attempting replanning via Google due to analysis failure...")
                    self.perform_google_search(user_command)
                    google_replan_triggered = True
                continue

            # Log full raw analysis dict for debugging
            try:
                self.log(f"🔍 Analysis raw: {analysis}")
            except Exception:
                pass
            
            thought = analysis.get('thought')
            self.log(f"💭 {thought}")
            
            action = analysis.get("action")
            self.log(f"Action: {action}")
            
            # Handle ERROR action gracefully
            if action == "ERROR":
                self.log(f"⚠️ Agent reported error: {thought}")
                self.capture_diagnostic("agent_error")
                
                # Don't trigger replanning on early steps - page might still be loading
                if step < 3:
                    self.log("⏳ Early in execution, page might still be loading...")
                    time.sleep(5)
                    continue
                elif not google_replan_triggered:
                    self.log("Triggering replanning via Google search...")
                    self.perform_google_search(user_command)
                    google_replan_triggered = True
                    time.sleep(2)
                    continue
                # Try to continue if not critical even after replanning
                if step > 0:
                    self.log("Attempting to continue after replanning...")
                    time.sleep(1)
                    continue
                else:
                    break
            
            # Check for repeated actions
            current_action_sig = f"{action}_{analysis.get('coordinates')}_{analysis.get('text')}"
            if current_action_sig == last_action:
                repeat_count += 1
                if repeat_count >= 2:
                    self.log("⚠️ Detected repetition. Trying alternative approach...")
                    if not google_replan_triggered:
                        self.log("Replanning via Google search for updated context...")
                        self.perform_google_search(user_command)
                        google_replan_triggered = True
                        repeat_count = 0
                        continue
                    # Force a different action or mark done
                    if action == "CLICK":
                        action = "PRESS"
                        analysis["key"] = "enter"
                    elif action == "TYPE":
                        action = "PRESS"
                        analysis["key"] = "enter"
                    repeat_count = 0
            else:
                repeat_count = 0
                last_action = current_action_sig
            
            # 3. Execute
            if action == "CLICK":
                coords = analysis.get("coordinates")
                if coords:
                    self.log(f"Clicking at {coords}")
                    success = click(coords[0], coords[1])
                    if success:
                        history.append(f"CLICKED at {coords}")
                    else:
                        history.append(f"CLICK FAILED at {coords}")
                        self.capture_diagnostic("click_fail")
                        if not google_replan_triggered:
                            self.perform_google_search(user_command)
                            google_replan_triggered = True
                else:
                    # Fallback heuristic click at center area
                    try:
                        import pyautogui
                        w, h = pyautogui.size()
                        fallback_point = (w//2, int(h*0.35))
                        self.log(f"⚠️ No coordinates provided. Fallback clicking center {fallback_point}.")
                        success = click(fallback_point[0], fallback_point[1])
                        if success:
                            history.append(f"FALLBACK CLICK {fallback_point}")
                        else:
                            history.append(f"FALLBACK CLICK FAILED {fallback_point}")
                            self.capture_diagnostic("fallback_click_fail")
                            if not google_replan_triggered:
                                self.perform_google_search(user_command)
                                google_replan_triggered = True
                        # If still no success, attempt contextual heuristics
                        if not success:
                            self.log("🔄 Trying contextual heuristics due to failed click.")
                            self.apply_contextual_heuristics(user_command, history)
                    except Exception as e:
                        self.log(f"❌ Fallback click error: {e}")
                        self.capture_diagnostic("fallback_click_error")
                        if not google_replan_triggered:
                            self.perform_google_search(user_command)
                            google_replan_triggered = True
            
            elif action == "TYPE":
                text = analysis.get("text")
                if text:
                    # Removed strict history check to allow retries if focus was lost
                    
                    self.log(f"Typing: '{text}'")
                    success = type_text(text)
                    if success:
                        history.append(f"TYPED '{text}'")
                    else:
                        history.append(f"TYPE FAILED '{text}'")
                        self.capture_diagnostic("type_fail")
                        if not google_replan_triggered:
                            self.perform_google_search(user_command)
                            google_replan_triggered = True
                else:
                    self.log("No text provided for TYPE.")
                    
            elif action == "PRESS":
                key = analysis.get("key")
                if key:
                    self.log(f"Pressing key: '{key}'")
                    success = press_key(key)
                    if success:
                        history.append(f"PRESSED '{key}'")
                    else:
                        history.append(f"PRESS FAILED '{key}'")
                        self.capture_diagnostic("press_fail")
                        if not google_replan_triggered:
                            self.perform_google_search(user_command)
                            google_replan_triggered = True
                        # Try heuristics if key press fails
                        self.apply_contextual_heuristics(user_command, history)
            
            elif action == "DONE":
                self.log("✅ Task completed successfully!")
                break
                
            else:
                self.log(f"⚠️ Unknown action: {action}")
                history.append(f"UNKNOWN ACTION: {action}")
                self.capture_diagnostic("unknown_action")
                if not google_replan_triggered:
                    self.perform_google_search(user_command)
                    google_replan_triggered = True
                # Attempt heuristic before proceeding
                self.apply_contextual_heuristics(user_command, history)
                
            time.sleep(1.5)  # Faster between steps

def main():
    parser = argparse.ArgumentParser(description="OS Agent - Autonomous Computer Control")
    parser.add_argument("command", nargs="*", help="The command to execute")
    args = parser.parse_args()
    
    user_command = " ".join(args.command)
    if not user_command:
        user_command = input("Enter your command: ")
        
    agent = OSAgent()
    agent.run(user_command)

if __name__ == "__main__":
    main()
