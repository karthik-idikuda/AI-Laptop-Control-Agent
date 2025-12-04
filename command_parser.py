# command_parser.py
"""Simple command parser for OS Agent.
Extracts intent components from a natural language command.
This is a lightweight heuristic implementation suitable for the current prototype.
"""
import re
from typing import Dict, Any

# Define known apps and websites for simple matching
KNOWN_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "whatsapp": "WhatsApp.exe",
    "chrome": "chrome.exe",
    "firefox": "firefox.exe",
    # Add more as needed
}

KNOWN_WEBSITES = {
    "youtube": "youtube",
    "gmail": "gmail",
    "google": "google",
    "whatsapp": "whatsapp",
    "facebook": "facebook",
    # Add more as needed
}

def _extract_search_query(command: str, action_word: str) -> str:
    """Extracts the text following an action word as a search query.
    Example: "play song hello" with action_word='play' returns 'song hello'.
    """
    pattern = rf"{action_word}\s+(.*)"
    match = re.search(pattern, command, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return ""

def parse_command(user_command: str) -> Dict[str, Any]:
    """Parse a user command into a structured intent dictionary.

    Returns a dict with keys:
        - target_app: str | None
        - target_website: str | None
        - action: str | None (e.g., 'open', 'play', 'send')
        - params: dict with additional extracted parameters
    """
    command = user_command.lower()
    intent: Dict[str, Any] = {
        "target_app": None,
        "target_website": None,
        "action": None,
        "params": {}
    }

    # Detect action
    if any(word in command for word in ["open", "launch", "start"]):
        intent["action"] = "open"
    elif "play" in command:
        intent["action"] = "play"
    elif any(word in command for word in ["send", "message", "text"]):
        intent["action"] = "send"
    else:
        intent["action"] = None

    # Detect website
    for key, site in KNOWN_WEBSITES.items():
        if key in command:
            intent["target_website"] = site
            break

    # Detect app (only if no website matched)
    if not intent["target_website"]:
        for key, app in KNOWN_APPS.items():
            if key in command:
                intent["target_app"] = app
                break

    # Extract parameters based on action and target
    if intent["action"] == "play" and intent["target_website"] == "youtube":
        # Use the remainder of the command after 'play' as search query
        query = _extract_search_query(command, "play")
        # Remove common suffixes like "on youtube", "in youtube"
        query = query.replace("on youtube", "").replace("in youtube", "").strip()
        if query:
            intent["params"]["search_query"] = query
    elif intent["action"] == "send" and intent["target_website"] == "whatsapp":
        # Very naive extraction: look for "to <contact>" and "saying <message>"
        contact_match = re.search(r"to\s+(\w+)", command)
        message_match = re.search(r"saying\s+(.+)", command)
        if contact_match:
            intent["params"]["contact"] = contact_match.group(1)
        if message_match:
            intent["params"]["message"] = message_match.group(1).strip()
    elif intent["action"] == "open" and intent["target_website"]:
        # No extra params needed for generic open
        pass
    elif intent["action"] == "open" and intent["target_app"]:
        # No extra params needed for app launch
        pass

    return intent
