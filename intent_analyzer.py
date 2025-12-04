"""
Intent Analyzer - Pure AI/NLP for understanding user commands
Uses Claude Sonnet 4.5 via OpenRouter to parse natural language into structured intent
"""

from openrouter_compat import genai
import json
import os
from typing import Dict, Any, Optional

class IntentAnalyzer:
    """Uses Claude Sonnet 4.5 (via OpenRouter) to understand user intent from natural language."""
    
    def __init__(self):
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel()
        
    def analyze(self, user_command: str) -> Dict[str, Any]:
        """
        Analyze user command using Gemini NLP to extract intent and parameters.
        
        Args:
            user_command: Natural language command from user
            
        Returns:
            Dictionary with structured intent:
            {
                'intent_type': str,      # e.g., 'messaging', 'search', 'media', 'automation'
                'target_app': str,       # e.g., 'whatsapp', 'youtube', 'browser', 'finder'
                'action': str,           # e.g., 'send_message', 'search', 'play', 'open'
                'parameters': dict,      # action-specific parameters
                'confidence': float,     # 0-1 confidence score
                'natural_response': str  # Human-friendly interpretation
            }
        """
        
        prompt = f"""You are an AI assistant that understands user commands for computer automation.

Analyze this command and extract the intent in JSON format:

USER COMMAND: "{user_command}"

Return a JSON object with these fields:
1. intent_type: category (greeting, question, thanks, messaging, search, media, automation, system_control, web_browsing, file_management)
2. target_app: which application to use (whatsapp, youtube, browser, finder, email, etc.) - use null if not applicable
3. action: specific action (send_message, search, play, open, close, click, type, etc.) - use null if not applicable
4. parameters: dictionary of action-specific parameters like:
   - For messaging: recipient, message, platform
   - For search: query, platform
   - For media: title, artist, platform
   - For automation: steps, targets
5. confidence: your confidence level (0.0 to 1.0)
6. natural_response: brief human-friendly summary of what you understood

IMPORTANT GUIDELINES:
- Simple greetings like "hi", "hello", "hey" should be classified as "greeting" with NO target_app or action
- Questions like "how are you", "what can you do" should be "question" type
- "thanks", "thank you" should be "thanks" type
- Only use "messaging" if there's a clear intent to send a message to someone
- Set confidence low (< 0.5) if the command is ambiguous or conversational

IMPORTANT: Return ONLY valid JSON, no other text.

Example for "hi":
{{
  "intent_type": "greeting",
  "target_app": null,
  "action": null,
  "parameters": {{}},
  "confidence": 0.95,
  "natural_response": "Hello! How can I help you today?"
}}

Example for "send hi to john on whatsapp":
{{
  "intent_type": "messaging",
  "target_app": "whatsapp",
  "action": "send_message",
  "parameters": {{
    "recipient": "john",
    "message": "hi",
    "platform": "whatsapp"
  }},
  "confidence": 0.95,
  "natural_response": "I'll send 'hi' to john via WhatsApp"
}}

Example for "open youtube and play shape of you":
{{
  "intent_type": "media",
  "target_app": "youtube",
  "action": "play",
  "parameters": {{
    "query": "shape of you",
    "platform": "youtube"
  }},
  "confidence": 0.90,
  "natural_response": "I'll open YouTube and play 'shape of you'"
}}
"""
        
        try:
            response = self.model.generate_content(prompt)
            if not response.text:
                raise ValueError("Model returned empty response")
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                lines = result_text.split('\n')
                result_text = '\n'.join(lines[1:-1])
            
            # Parse JSON
            intent = json.loads(result_text)
            
            # Validate required fields
            required_fields = ['intent_type', 'target_app', 'action', 'parameters', 'confidence', 'natural_response']
            for field in required_fields:
                if field not in intent:
                    intent[field] = None if field != 'parameters' else {}
            
            # Ensure confidence is a float
            if isinstance(intent['confidence'], (int, float)):
                intent['confidence'] = float(intent['confidence'])
            else:
                intent['confidence'] = 0.5
            
            return intent
            
        except json.JSONDecodeError as e:
            # Fallback: return basic intent with low confidence
            return {
                'intent_type': 'unknown',
                'target_app': None,
                'action': 'parse_failed',
                'parameters': {'raw_command': user_command, 'error': str(e)},
                'confidence': 0.1,
                'natural_response': f"I couldn't fully understand the command, but I'll try: {user_command}"
            }
        except Exception as e:
            print(f"Error in intent analysis: {e}")
            return {
                'intent_type': 'error',
                'target_app': None,
                'action': 'error',
                'parameters': {'error': str(e)},
                'confidence': 0.0,
                'natural_response': f"Error analyzing command: {e}"
            }
    
    def is_conversational(self, intent: Dict[str, Any]) -> bool:
        """
        Determine if the intent is conversational vs. actionable.
        
        Args:
            intent: Parsed intent from analyze()
            
        Returns:
            True if conversational (greeting, question, thanks), False if actionable command
        """
        conversational_types = ['greeting', 'question', 'thanks', 'unknown']
        
        # Low confidence suggests uncertainty - treat as conversational
        if intent.get('confidence', 0) < 0.4:
            return True
        
        # Check if intent type is conversational
        if intent.get('intent_type') in conversational_types:
            return True
        
        # Check if action is None or unclear
        if not intent.get('action') or intent.get('action') in ['parse_failed', 'error', 'unknown']:
            return True
        
        # Check if target_app is None/null and confidence is medium-low
        if not intent.get('target_app') and intent.get('confidence', 0) < 0.6:
            return True
        
        return False


# Example usage
if __name__ == "__main__":
    analyzer = IntentAnalyzer()
    
    # Test commands
    test_commands = [
        "send hi to john on whatsapp",
        "play some chill music",
        "open youtube and search for python tutorials",
        "message sarah saying I'm running late",
        "find the cheapest airpods on amazon",
        "hello how are you",  # conversational
        "what's the weather like"  # conversational/question
    ]
    
    for cmd in test_commands:
        print(f"\n{'='*70}")
        print(f"COMMAND: {cmd}")
        print(f"{'='*70}")
        
        intent = analyzer.analyze(cmd)
        print(f"Intent Type: {intent['intent_type']}")
        print(f"Target App: {intent['target_app']}")
        print(f"Action: {intent['action']}")
        print(f"Parameters: {json.dumps(intent['parameters'], indent=2)}")
        print(f"Confidence: {intent['confidence']}")
        print(f"Response: {intent['natural_response']}")
        print(f"Is Conversational: {analyzer.is_conversational(intent)}")
