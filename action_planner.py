"""
Action Planner - Dynamic execution planning using Claude Sonnet 4.5
Generates step-by-step execution plans based on parsed intent
"""

from openrouter_compat import genai
import json
import os
from typing import Dict, Any, List, Optional

class ActionPlanner:
    """Uses Claude Sonnet 4.5 (via OpenRouter) to generate dynamic execution plans."""
    
    def __init__(self):
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel()
    
    def create_plan(self, intent: Dict[str, Any], screen_context: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Generate an execution plan based on the parsed intent.
        
        Args:
            intent: Structured intent from IntentAnalyzer
            screen_context: Optional current screen state description
            
        Returns:
            List of steps to execute:
            [
                {
                    'step_number': int,
                    'action_type': str,  # OPEN_APP, CLICK, TYPE, PRESS, WAIT, FIND_AND_CLICK
                    'target': str,       # what to interact with
                    'value': str,        # value to type or key to press
                    'description': str,  # human-readable description
                    'verification': str  # what to verify after this step
                },
                ...
            ]
        """
        
        prompt = f"""You are an AI that creates step-by-step execution plans for computer automation.

PARSED INTENT:
{json.dumps(intent, indent=2)}

{f"CURRENT SCREEN CONTEXT: {screen_context}" if screen_context else ""}

Generate a detailed execution plan as a JSON array of steps. Each step should have:
1. step_number: sequential number starting from 1
2. action_type: one of [OPEN_APP, FIND_AND_CLICK, TYPE, PRESS, WAIT, VERIFY]
3. target: what element to interact with (e.g., "search box", "contact name", "send button")
4. value: value to type or key to press (for TYPE and PRESS actions)
5. description: human-readable description of what this step does
6. verification: what to check to confirm this step succeeded

ACTION TYPES:
- OPEN_APP: Open an application (target = app name, value = method like "spotlight" or "launchpad")
- FIND_AND_CLICK: Find an element on screen and click it (target = description of element)
- TYPE: Type text (value = text to type)
- PRESS: Press a key (value = key name like "enter", "escape", "command+space")
- WAIT: Wait for condition (target = what to wait for, value = max seconds)
- VERIFY: Verify something on screen (target = what to verify)

Example for "send hi to john on whatsapp":
[
  {{
    "step_number": 1,
    "action_type": "OPEN_APP",
    "target": "whatsapp",
    "value": "spotlight",
    "description": "Open WhatsApp using Spotlight search",
    "verification": "WhatsApp window is visible"
  }},
  {{
    "step_number": 2,
    "action_type": "WAIT",
    "target": "whatsapp_interface",
    "value": "3",
    "description": "Wait for WhatsApp to fully load",
    "verification": "Chat interface is visible"
  }},
  {{
    "step_number": 3,
    "action_type": "FIND_AND_CLICK",
    "target": "search box or new chat button",
    "value": "",
    "description": "Click the search box to find contact",
    "verification": "Search box is active"
  }},
  {{
    "step_number": 4,
    "action_type": "TYPE",
    "target": "search box",
    "value": "john",
    "description": "Type the contact name",
    "verification": "Search results show contact"
  }},
  {{
    "step_number": 5,
    "action_type": "FIND_AND_CLICK",
    "target": "contact result for john",
    "value": "",
    "description": "Click on john's contact",
    "verification": "Chat with john is open"
  }},
  {{
    "step_number": 6,
    "action_type": "FIND_AND_CLICK",
    "target": "message input box",
    "value": "",
    "description": "Click the message input field",
    "verification": "Input field is focused"
  }},
  {{
    "step_number": 7,
    "action_type": "TYPE",
    "target": "message input",
    "value": "hi",
    "description": "Type the message",
    "verification": "Message appears in input box"
  }},
  {{
    "step_number": 8,
    "action_type": "PRESS",
    "target": "send",
    "value": "enter",
    "description": "Press Enter to send message",
    "verification": "Message appears in chat history"
  }}
]

IMPORTANT: Return ONLY valid JSON array, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                lines = result_text.split('\n')
                result_text = '\n'.join(lines[1:-1])
            
            # Parse JSON
            plan = json.loads(result_text)
            
            # Validate it's a list
            if not isinstance(plan, list):
                raise ValueError("Plan must be a list of steps")
            
            # Validate each step has required fields
            for step in plan:
                if 'step_number' not in step:
                    step['step_number'] = plan.index(step) + 1
                if 'action_type' not in step:
                    step['action_type'] = 'UNKNOWN'
                if 'target' not in step:
                    step['target'] = ''
                if 'value' not in step:
                    step['value'] = ''
                if 'description' not in step:
                    step['description'] = 'No description'
                if 'verification' not in step:
                    step['verification'] = 'No verification'
            
            return plan
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Response text: {result_text}")
            # Fallback: create a simple plan
            return self._create_fallback_plan(intent)
        except Exception as e:
            print(f"Error creating plan: {e}")
            return self._create_fallback_plan(intent)
    
    def _create_fallback_plan(self, intent: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create a basic fallback plan when AI planning fails."""
        target_app = intent.get('target_app', 'unknown')
        action = intent.get('action', 'unknown')
        
        return [
            {
                'step_number': 1,
                'action_type': 'OPEN_APP',
                'target': target_app,
                'value': 'spotlight',
                'description': f'Open {target_app}',
                'verification': f'{target_app} is visible'
            },
            {
                'step_number': 2,
                'action_type': 'WAIT',
                'target': 'app_loaded',
                'value': '3',
                'description': 'Wait for app to load',
                'verification': 'App interface is ready'
            }
        ]
    
    def replan(self, original_intent: Dict[str, Any], failed_step: Dict[str, Any], 
               error_description: str, screen_context: str) -> List[Dict[str, Any]]:
        """
        Create an alternative plan when a step fails.
        
        Args:
            original_intent: The original parsed intent
            failed_step: The step that failed
            error_description: Description of what went wrong
            screen_context: Current screen state
            
        Returns:
            New execution plan
        """
        
        prompt = f"""A step in our automation plan failed. Create an alternative approach.

ORIGINAL INTENT:
{json.dumps(original_intent, indent=2)}

FAILED STEP:
{json.dumps(failed_step, indent=2)}

ERROR: {error_description}

CURRENT SCREEN STATE: {screen_context}

Generate a NEW execution plan that:
1. Accounts for the current screen state
2. Tries a different approach to achieve the same goal
3. Includes verification steps
4. Returns a JSON array of steps (same format as before)

IMPORTANT: Return ONLY valid JSON array, no other text.
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            if result_text.startswith('```'):
                lines = result_text.split('\n')
                result_text = '\n'.join(lines[1:-1])
            
            plan = json.loads(result_text)
            return plan if isinstance(plan, list) else []
            
        except Exception as e:
            print(f"Error in replanning: {e}")
            return []


# Example usage
if __name__ == "__main__":
    from intent_analyzer import IntentAnalyzer
    
    analyzer = IntentAnalyzer()
    planner = ActionPlanner()
    
    # Test command
    command = "send hi to john on whatsapp"
    
    print(f"{'='*70}")
    print(f"COMMAND: {command}")
    print(f"{'='*70}\n")
    
    # Step 1: Analyze intent
    intent = analyzer.analyze(command)
    print("INTENT:")
    print(json.dumps(intent, indent=2))
    print()
    
    # Step 2: Create plan
    plan = planner.create_plan(intent)
    print("EXECUTION PLAN:")
    for step in plan:
        print(f"\nStep {step['step_number']}: {step['description']}")
        print(f"  Action: {step['action_type']}")
        print(f"  Target: {step['target']}")
        if step['value']:
            print(f"  Value: {step['value']}")
        print(f"  Verify: {step['verification']}")
