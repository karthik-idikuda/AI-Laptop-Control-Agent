from openrouter_compat import genai
import PIL.Image
import os
import json
import time
from config import OPENROUTER_API_KEY, MODEL_NAME, SCREENSHOTS_DIR, ERROR_SCREENSHOT_DIR
from prompts import SYSTEM_PROMPT
import pyautogui
from PIL import ImageChops
import math

genai.configure(api_key=OPENROUTER_API_KEY)

model = genai.GenerativeModel(MODEL_NAME)

def capture_screen(filename="screenshot.png"):
    """Captures the screen and saves it to the screenshots directory."""
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        return filepath
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

def analyze_screen(image_path, user_request, history=None):
    """
    Sends the screenshot and user request to Gemini Vision.
    Returns a structured dictionary with the next action.
    """
    try:
        img = PIL.Image.open(image_path)
        
        prompt_parts = [
            SYSTEM_PROMPT,
            f"User Request: {user_request}",
            "Current Screen:",
            img
        ]
        
        if history:
            prompt_parts.append(f"Action History: {history}")
            
        response = model.generate_content(prompt_parts)
        
        # Parse JSON from response
        text_response = response.text
        
        # Clean up markdown code blocks if present
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0]
        
        # Try to parse JSON
        try:
            parsed = json.loads(text_response.strip())
            # Ensure required fields exist
            if 'action' not in parsed:
                parsed['action'] = 'ERROR'
            if 'thought' not in parsed:
                parsed['thought'] = 'No thought provided'
            return parsed
        except json.JSONDecodeError as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Raw response: {text_response[:500]}")
            
            # Try to extract action and thought manually
            action = 'ERROR'
            thought = text_response[:200]
            
            # Look for action in text
            if 'CLICK' in text_response.upper():
                action = 'CLICK'
            elif 'TYPE' in text_response.upper():
                action = 'TYPE'
            elif 'PRESS' in text_response.upper():
                action = 'PRESS'
            elif 'DONE' in text_response.upper():
                action = 'DONE'
            
            return {
                "action": action,
                "thought": thought,
                "error": "Failed to parse JSON response"
            }
            
    except Exception as e:
        print(f"Error analyzing screen: {e}")
        return {"action": "ERROR", "thought": str(e)}


def capture_error_screenshot(error_label="error"):
    """Capture a screenshot when an error occurs."""
    timestamp = int(time.time())
    filename = f"{error_label}_{timestamp}.png"
    filepath = os.path.join(ERROR_SCREENSHOT_DIR, filename)
    
    try:
        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)
        print(f"📸 Error screenshot saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"Error capturing error screenshot: {e}")
        return None


def analyze_error_screenshot(image_path, user_request, error_message):
    """
    Analyze an error screenshot to understand what went wrong.
    Returns a dictionary with error analysis.
    """
    try:
        img = PIL.Image.open(image_path)
        
        prompt = f'''You are a computer vision AI controlling a computer to complete this task:

USER REQUEST: "{user_request}"

PREVIOUS ACTIONS:
{action_history if action_history else "No previous actions."}

CRITICAL RULES - KEYBOARD FIRST STRATEGY:
1. **ALWAYS prefer KEYBOARD over MOUSE for typing/entering data**
   - For calculator: TYPE "2+2" then PRESS Enter (DON'T click individual buttons)
   - For search: TYPE the search query (DON'T click each letter)
   - For forms: TYPE the text directly (DON'T click and type)
   
2. **Use MOUSE only for:**
   - Clicking buttons/links that cannot be activated by keyboard
   - Selecting UI elements
   - Navigating to input fields (then use keyboard)

3. **Action Priority:**
   - Can you TYPE it? → Use TYPE action
   - Can you PRESS a key? → Use PRESS action  
   - Need to click something? → Use CLICK action

4. **Examples:**
   - Calculator "2+2": TYPE "2+2" then PRESS "enter" ✅ (NOT: click 2, click +, click 2, click = ❌)
   - Search "music": TYPE "music" then PRESS "enter" ✅ (NOT: click letters ❌)
   - Form field: CLICK field, then TYPE text ✅ (NOT: click each letter ❌)

Analyze the attached screenshot and determine the NEXT action.

OUTPUT JSON FORMAT:
{{
    "thought": "explain what you see and why you chose this action - mention if keyboard is better than mouse",
    "action": "CLICK | TYPE | PRESS | DONE | ERROR",
    "coordinates": [x, y],  // only for CLICK
    "text": "text to type",  // only for TYPE
    "key": "enter"  // only for PRESS (enter, tab, space, escape, etc.)
}}

IMPORTANT GUIDELINES:
- Think keyboards-first: Can I TYPE or PRESS instead of CLICK?
- TYPE full expressions (e.g., "2+2", "hello world") not character-by-character
- Use PRESS for navigation (tab, enter, escape, arrows)
- Use CLICK only when keyboard cannot achieve the goal
- Return DONE when task is complete
- Return ERROR if stuck or impossible

Think step-by-step and choose the MOST EFFICIENT action (prefer keyboard).'''
        
        response = model.generate_content([prompt, img])
        text_response = response.text
        
        # Clean up markdown code blocks
        if "```json" in text_response:
            text_response = text_response.split("```json")[1].split("```")[0]
        elif "```" in text_response:
            text_response = text_response.split("```")[1].split("```")[0]
        
        try:
            analysis = json.loads(text_response.strip())
            return analysis
        except json.JSONDecodeError:
            return {
                "error_type": "analysis_failed",
                "error_description": text_response[:200],
                "suggested_recovery": "Try manual intervention",
                "requires_replanning": True
            }
            
    except Exception as e:
        print(f"Error analyzing error screenshot: {e}")
        return {
            "error_type": "unknown",
            "error_description": str(e),
            "suggested_recovery": "Unknown",
            "requires_replanning": True
        }


def compare_screenshots(before_path, after_path):
    """
    Compare two screenshots to detect if there was a meaningful change.
    Returns similarity score (0.0 to 1.0) - higher means more similar.
    """
    try:
        img1 = PIL.Image.open(before_path)
        img2 = PIL.Image.open(after_path)
        
        # Ensure same size
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)
        
        # Calculate difference
        diff = ImageChops.difference(img1, img2)
        
        # Calculate RMS (root mean square) difference
        stat = diff.convert('L').getextrema()
        
        # Get histogram and calculate similarity
        h = diff.histogram()
        sq = (value * ((idx % 256) ** 2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares / float(img1.size[0] * img1.size[1]))
        
        # Convert to similarity score (0-1, where 1 is identical)
        max_rms = 255 * math.sqrt(3)  # Maximum possible RMS for RGB
        similarity = 1.0 - (rms / max_rms)
        
        return similarity
        
    except Exception as e:
        print(f"Error comparing screenshots: {e}")
        return 0.0


def verify_action_success(before_path, after_path, expected_change, threshold=0.85):
    """
    Verify if an action was successful by comparing before/after screenshots.
    
    Args:
        before_path: Path to screenshot before action
        after_path: Path to screenshot after action
        expected_change: Description of expected change
        threshold: Similarity threshold (if too similar, action may have failed)
    
    Returns:
        dict with success status and analysis
    """
    similarity = compare_screenshots(before_path, after_path)
    
    # If screenshots are too similar, the action likely didn't work
    if similarity > threshold:
        return {
            "success": False,
            "reason": "Screen unchanged after action",
            "similarity": similarity
        }
    
    # Use vision to verify expected change occurred
    try:
        img_after = PIL.Image.open(after_path)
        
        prompt = f"""Look at this screenshot after an action was performed.

Expected change: {expected_change}

Did the expected change occur? Answer with JSON:
{{
  "success": true/false,
  "observed": "what you actually see",
  "matches_expectation": true/false
}}"""
        
        response = model.generate_content([prompt, img_after])
        text = response.text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        verification = json.loads(text.strip())
        verification["similarity"] = similarity
        return verification
        
    except Exception as e:
        return {
            "success": False,
            "reason": f"Verification failed: {str(e)}",
            "similarity": similarity
        }


def detect_error_state(image_path):
    """
    Detect if the current screenshot shows an error state.
    Returns True if error detected, False otherwise.
    """
    try:
        img = PIL.Image.open(image_path)
        
        prompt = """Look at this screenshot. Is there any error, crash dialog, or problem visible?

Common error indicators:
- Error dialog boxes
- Application crash messages
- "Not found" or "404" pages
- Permission denied messages
- Frozen/unresponsive UI

Answer with JSON:
{
  "has_error": true/false,
  "error_description": "description if error found, empty otherwise"
}"""
        
        response = model.generate_content([prompt, img])
        text = response.text.strip()
        
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        result = json.loads(text.strip())
        return result.get("has_error", False), result.get("error_description", "")
        
    except Exception as e:
        print(f"Error detecting error state: {e}")
        return False, ""

