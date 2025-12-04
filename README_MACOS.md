# OS Agent - macOS Installation & Usage Guide

## Overview
This is an AI-powered OS Agent using Gemini 2.5 Flash for natural language processing and computer control. This version is fully optimized for **macOS**.

## Requirements

### System Requirements
- **macOS** 10.14 (Mojave) or later
- Python 3.8 or higher
- Internet connection

### Python Dependencies
Install all required Python packages:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install google-generativeai PyQt5 pyautogui python-dotenv opencv-python pillow numpy
```

### macOS Permissions

The agent needs certain permissions to function:

1. **Accessibility**: System Preferences → Security & Privacy → Privacy → Accessibility
   - Add Terminal (or your Python IDE) to the list
   - This allows the agent to control mouse and keyboard

2. **Screen Recording**: System Preferences → Security & Privacy → Privacy → Screen Recording
   - Add Terminal (or your Python IDE) to the list
   - This allows the agent to capture screenshots

## Setup

1. **Clone or Download** this repository

2. **Create a `.env` file** in the project root:

```bash
OPENROUTER_API_KEY=your_gemini_api_key_here
```

Get your API key from: https://aistudio.google.com/app/apikey

3. **Configure macOS-specific settings**

The `config.py` file is already configured for macOS with:
- **Default Browser**: Safari
- **Fallback Browser**: Google Chrome

## Usage

### GUI Mode (Recommended)

Launch the professional GUI:

```bash
python main.py --gui
```

The GUI features:
- Modern macOS-native design with SF Pro Display font
- Real-time execution logs
- Simple command input interface
- Stop/Start controls

### CLI Mode

For command-line usage:

```bash
# Interactive mode
python main.py

# Direct command
python main.py "open safari and search for python tutorials"
```

## Features

### 1. **Application Control**
- Open macOS applications (Safari, Notes, Calculator, etc.)
- Launch apps using Spotlight search
- Fallback to browser if app not installed

### 2. **Web Automation**
- Control Safari or Chrome
- Perform Google searches
- Navigate and interact with web pages

### 3. **Intelligent Vision**
- Screenshot analysis using Gemini Vision
- Find and click UI elements
- Verify actions were successful

### 4. **Natural Language**
- Conversational chat interface
- Intent understanding
- Context-aware responses

## macOS-Specific Commands

The agent works best with natural language commands like:

```
"open safari"
"search for machine learning tutorials"
"open calculator"
"take a screenshot"
"open notes and create a new note"
"search youtube for python tutorials"
```

## Troubleshooting

### Permission Issues

If the agent can't control your computer:
1. Go to **System Preferences → Security & Privacy → Privacy**
2. Select **Accessibility** and **Screen Recording**
3. Add your Terminal or IDE to both lists
4. Restart your Terminal/IDE

### PyAutoGUI Failsafe

If the mouse goes to the top-left corner, the script will stop (safety feature). To disable:

```python
# In computer_control.py
pyautogui.FAILSAFE = False  # Not recommended
```

### Font Issues

If SF Pro Display doesn't render properly, the GUI will fallback to system default fonts (Helvetica). You can also manually edit `gui_advanced.py` to use a different font:

```python
QFont('Helvetica Neue', 10)  # Alternative macOS font
```

### Browser Issues

If the default browser (Safari) doesn't work:
1. Edit `config.py`
2. Change `DEFAULT_BROWSER = "Google Chrome"`
3. Make sure Chrome is installed

## Converting HTML to PDF (macOS)

Use the included shell script:

```bash
./convert.sh
```

This script:
- Uses Google Chrome in headless mode if available
- Falls back to Safari with manual save option
- Automatically opens the generated PDF

## Project Structure

```
os agent/
├── main.py                  # Entry point
├── agent.py                 # Core agent logic
├── gui_advanced.py          # macOS-optimized GUI
├── config.py                # macOS configuration
├── app_manager.py           # Application control
├── computer_control.py      # Mouse/keyboard automation
├── vision_analyzer.py       # Screenshot analysis
├── intent_analyzer.py       # NLP intent detection
├── action_planner.py        # Action planning
├── action_verifier.py       # Action verification
├── chat_handler.py          # Conversational interface
├── convert.sh              # HTML to PDF (macOS)
└── .env                    # API keys (create this)
```

## Tips for Best Results

1. **Be Specific**: "Open Safari and search for Python" works better than just "Python"
2. **Wait for Actions**: The agent waits between actions for UI to load
3. **Use Natural Language**: Speak naturally, as you would to a human
4. **Screen Position**: Keep the GUI away from screen corners (PyAutoGUI failsafe)

## Limitations

- Requires macOS accessibility permissions
- Works best with common macOS applications
- Internet connection required for AI processing
- May not work with all third-party applications

## Support

For issues specific to macOS:
1. Check System Preferences → Security & Privacy permissions
2. Ensure Python 3.8+ is installed
3. Verify all dependencies are installed
4. Check that your API key is valid

## License

This project is for educational and research purposes.

## Credits

- Built with Google Gemini 2.5 Flash
- GUI: PyQt5
- Automation: PyAutoGUI
- Vision: OpenCV + Pillow
