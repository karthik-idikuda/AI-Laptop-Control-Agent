import os
from dotenv import load_dotenv

load_dotenv()

# OpenRouter API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not found in .env file")

# For backward compatibility
GEMINI_API_KEY = OPENROUTER_API_KEY
API_KEY = OPENROUTER_API_KEY

# Screen capture settings
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Model settings - Using Gemini 2.5 Flash (Stable, Better Rate Limits)
MODEL_NAME = "gemini-2.5-flash"  # Stable GA model with better rate limits
OPENROUTER_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# Browser settings (macOS)
DEFAULT_BROWSER = "Safari"  # Primary browser for macOS
FALLBACK_BROWSER = "Google Chrome"  # Fallback browser for macOS

# Task execution settings
MAX_RETRIES = 3  # Maximum retry attempts before replanning
REPLAN_ON_ERROR = True  # Enable automatic replanning
RETRIES_PER_STRATEGY = 2  # Retries per strategy before trying next strategy

# Screen recording settings
ENABLE_SCREEN_RECORDING = False  # Enable screen recording during task execution (resource-intensive)
RECORDING_FPS = 10  # Frames per second for screen recording
MAX_RECORDING_DURATION = 300  # Maximum recording duration in seconds (5 minutes)
RECORDINGS_DIR = os.path.join(os.path.dirname(__file__), "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# Screenshot analysis settings
SCREENSHOT_COMPARISON_THRESHOLD = 0.85  # Similarity threshold for before/after comparison
ERROR_SCREENSHOT_DIR = os.path.join(SCREENSHOTS_DIR, "errors")
os.makedirs(ERROR_SCREENSHOT_DIR, exist_ok=True)

# Chat settings
ENABLE_CHAT = True  # Enable conversational interface
CHAT_CONTEXT_WINDOW = 10  # Number of messages to keep in context
