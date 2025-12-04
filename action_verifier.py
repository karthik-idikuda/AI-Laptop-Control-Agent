"""
Action Verifier - Validates Operation Success
Takes screenshots and uses vision AI to verify actions completed correctly.
"""

import time
from vision_analyzer import capture_screen
from openrouter_compat import genai
from config import OPENROUTER_API_KEY, MODEL_NAME
from PIL import Image
import json

genai.configure(api_key=OPENROUTER_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

class ActionVerifier:
    def __init__(self):
        self.verification_history = []
    
    def verify_action(self, action_description, expected_result, timeout=5):
        """
        Verify if an action completed successfully.
        
        Args:
            action_description: What action was taken (e.g., "Clicked Send button")
            expected_result: What should happen (e.g., "Message sent confirmation appears")
            timeout: How long to wait before checking (seconds)
        
        Returns:
            dict: Verification result with success status and details
        """
        print(f"\n🔍 Verifying: {action_description}")
        print(f"   Expected: {expected_result}")
        
        # Wait for UI to update
        time.sleep(timeout)
        
        # Capture screen
        screenshot = capture_screen(f"verify_{int(time.time())}.png")
        
        # Analyze with AI
        prompt = f"""Action taken: {action_description}
Expected result: {expected_result}

Analyze this screenshot and determine:
1. Did the expected result occur? (yes/no)
2. What actually happened?
3. Any errors or unexpected behavior?

Output JSON:
{{
  "success": true/false,
  "what_happened": "description",
  "confidence": 0-100,
  "error_detected": "error message if any"
}}"""
        
        try:
            img = Image.open(screenshot)
            response = model.generate_content([prompt, img])
            
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            result = json.loads(text.strip())
            
            # Log result
            self.verification_history.append({
                "action": action_description,
                "expected": expected_result,
                "result": result,
                "timestamp": time.time(),
                "screenshot": screenshot
            })
            
            # Print result
            if result.get('success'):
                print(f"   ✅ SUCCESS: {result.get('what_happened')}")
                print(f"   Confidence: {result.get('confidence')}%")
            else:
                print(f"   ❌ FAILED: {result.get('what_happened')}")
                if result.get('error_detected'):
                    print(f"   Error: {result.get('error_detected')}")
            
            return result
            
        except Exception as e:
            print(f"   ⚠️ Verification error: {e}")
            return {
                "success": False,
                "what_happened": f"Verification failed: {str(e)}",
                "confidence": 0
            }
    
    def verify_element_exists(self, element_description):
        """
        Check if a UI element exists on screen.
        
        Args:
            element_description: What to look for (e.g., "Submit button")
        
        Returns:
            dict: Contains exists (bool) and coordinates if found
        """
        print(f"🔍 Checking for: {element_description}")
        
        screenshot = capture_screen("element_check.png")
        
        prompt = f"""Look for this element on the screen: {element_description}

Output JSON:
{{
  "exists": true/false,
  "coordinates": [x, y],  // if exists
  "description": "what you see"
}}"""
        
        try:
            img = Image.open(screenshot)
            response = model.generate_content([prompt, img])
            
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            
            result = json.loads(text.strip())
            
            if result.get('exists'):
                print(f"   ✅ Found: {result.get('description')}")
                if result.get('coordinates'):
                    print(f"   Location: {result.get('coordinates')}")
            else:
                print(f"   ❌ Not found")
            
            return result
            
        except Exception as e:
            print(f"   ⚠️ Check failed: {e}")
            return {"exists": False, "description": str(e)}
    
    def verify_text_appeared(self, text_to_find):
        """
        Check if specific text appeared on screen.
        
        Args:
            text_to_find: Text to search for
        
        Returns:
            bool: True if found
        """
        print(f"🔍 Looking for text: '{text_to_find}'")
        
        screenshot = capture_screen("text_check.png")
        
        prompt = f"""Is the text "{text_to_find}" visible on this screen?
Output JSON: {{"found": true/false, "exact_match": true/false}}"""
        
        try:
            img = Image.open(screenshot)
            response = model.generate_content([prompt, img])
            
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            
            result = json.loads(text.strip())
            
            if result.get('found'):
                print(f"   ✅ Text found!")
            else:
                print(f"   ❌ Text not found")
            
            return result.get('found', False)
            
        except Exception as e:
            print(f"   ⚠️ Check failed: {e}")
            return False
    
    def verify_page_loaded(self, page_identifier):
        """
        Verify a page/app loaded correctly.
        
        Args:
            page_identifier: What page (e.g., "YouTube homepage", "Gmail inbox")
        
        Returns:
            dict: Loading verification result
        """
        print(f"🔍 Verifying page loaded: {page_identifier}")
        
        screenshot = capture_screen("page_check.png")
        
        prompt = f"""Is the {page_identifier} loaded and ready?
Check for:
- Correct page/app is visible
- Main UI elements loaded
- No loading spinners
- No error messages

Output JSON:
{{
  "loaded": true/false,
  "ready": true/false,
  "issues": "any problems detected"
}}"""
        
        try:
            img = Image.open(screenshot)
            response = model.generate_content([prompt, img])
            
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            
            result = json.loads(text.strip())
            
            if result.get('loaded') and result.get('ready'):
                print(f"   ✅ Page ready!")
            else:
                print(f"   ⚠️ Page not ready: {result.get('issues')}")
            
            return result
            
        except Exception as e:
            print(f"   ⚠️ Check failed: {e}")
            return {"loaded": False, "ready": False, "issues": str(e)}
    
    def compare_before_after(self, before_screenshot, action_description):
        """
        Compare screen before and after action.
        
        Args:
            before_screenshot: Path to screenshot before action
            action_description: What action was performed
        
        Returns:
            dict: Comparison result
        """
        # Take after screenshot
        time.sleep(2)
        after_screenshot = capture_screen("after_action.png")
        
        print(f"🔍 Comparing before/after for: {action_description}")
        
        prompt = f"""Compare these two screenshots (before and after: {action_description}).

What changed? List all visible differences."""
        
        try:
            before_img = Image.open(before_screenshot)
            after_img = Image.open(after_screenshot)
            
            response = model.generate_content([
                prompt,
                "Before:",
                before_img,
                "After:",
                after_img
            ])
            
            changes = response.text
            print(f"   Changes detected:\n{changes}")
            
            return {"changes": changes, "screenshots": [before_screenshot, after_screenshot]}
            
        except Exception as e:
            print(f"   ⚠️ Comparison failed: {e}")
            return {"changes": str(e)}
    
    def get_verification_report(self):
        """Get summary of all verifications."""
        total = len(self.verification_history)
        successful = sum(1 for v in self.verification_history if v['result'].get('success'))
        
        print(f"\n📊 Verification Report:")
        print(f"   Total actions verified: {total}")
        print(f"   ✅ Successful: {successful}")
        print(f"   ❌ Failed: {total - successful}")
        print(f"   Success rate: {(successful/total*100) if total > 0 else 0:.1f}%")
        
        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "history": self.verification_history
        }

# Global verifier instance
verifier = ActionVerifier()

# Convenience functions
def verify(action, expected):
    """Quick verify function."""
    return verifier.verify_action(action, expected)

def check_element(element):
    """Quick element check."""
    return verifier.verify_element_exists(element)

def check_text(text):
    """Quick text check."""
    return verifier.verify_text_appeared(text)

# Usage example
if __name__ == "__main__":
    verifier = ActionVerifier()
    
    # Example 1: Verify button click
    # (After clicking a button)
    result = verifier.verify_action(
        action_description="Clicked Send button",
        expected_result="Message sent confirmation appears",
        timeout=3
    )
    
    # Example 2: Check if element exists
    element = verifier.verify_element_exists("Search bar")
    
    # Example 3: Check if text appeared
    found = verifier.verify_text_appeared("Success!")
    
    # Example 4: Verify page loaded
    page = verifier.verify_page_loaded("YouTube homepage")
    
    # Get report
    verifier.get_verification_report()
