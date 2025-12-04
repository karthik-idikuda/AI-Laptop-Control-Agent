import logging
import sys
import time
import argparse
from logging.handlers import RotatingFileHandler
from agent import OSAgent  as BaseOSAgent
from chat_handler import ChatHandler
from intent_analyzer import IntentAnalyzer
from action_planner import ActionPlanner
from config import ENABLE_CHAT

# Configure logging with rotation
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Rotating file handler: max 10MB per file, keep 5 backups
file_handler = RotatingFileHandler(
    'agent.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

class OSAgent:
    """AI-powered OS Agent using Gemini 2.5 Flash for NLP and planning."""
    
    def __init__(self):
        self.base_agent = BaseOSAgent()
        self.chat_handler = ChatHandler() if ENABLE_CHAT else None
        self.intent_analyzer = IntentAnalyzer()
        self.action_planner = ActionPlanner()
        
    def execute_command(self, command):
        """Execute command using AI pipeline (GUI-compatible)."""
        try:
            logger.info(f"Analyzing command: {command}")
            
            # Step 1: Use AI to understand intent
            intent = self.intent_analyzer.analyze(command)
            logger.info(f"Intent: {intent['intent_type']} | App: {intent['target_app']} | Action: {intent['action']}")
            logger.info(f"AI Response: {intent['natural_response']}")
            
            # Step 2: Check if conversational vs actionable
            if self.intent_analyzer.is_conversational(intent):
                response = self._handle_chat(command, intent)
                print(f"🤖 Agent: {response}")
                return {'success': True, 'details': response, 'attempts': 1}
            
            # Step 3: Execute autonomously
            logger.info("Starting autonomous execution loop...")
            print(f"\n🤖 Starting Autonomous Loop for: {command}")
            
            # Execute via base agent using the autonomous loop
            self.base_agent.run(command, intent)
            
            return {'success': True, 'details': 'Autonomous execution completed', 'attempts': 1}
            
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'details': str(e), 'attempts': 1}
    
    def _handle_chat(self, message, intent=None):
        """Handle conversational messages."""
        if not self.chat_handler:
            return intent['natural_response'] if intent else "Hello! How can I help you today?"
        
        try:
            return self.chat_handler.respond(message)
        except Exception as e:
            logger.error(f"Chat handler error: {e}")
            return intent['natural_response'] if intent else "I'm having trouble processing that. Please try again."


def main():
    """Main entry point with configuration validation"""
    # Validate configuration first
    from config_validator import ConfigValidator
    if not ConfigValidator.validate_all():
        logger.error("Configuration validation failed. Please fix the errors above.")
        sys.exit(1)
    
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='OS Agent - AI Control System')
    parser.add_argument('--gui', action='store_true', 
                        help='Launch with advanced animated GUI')
    parser.add_argument('command', nargs='*', 
                        help='Command to execute (optional)')
    
    args = parser.parse_args()
    
    # Launch GUI if requested
    if args.gui:
        logger.info("Launching Sticky Animated GUI...")
        try:
            from gui_sticky import main as gui_main
            gui_main()
        except ImportError as e:
            logger.error(f"Failed to import Sticky GUI: {e}")
            logger.error("Make sure PyQt5 is installed: pip install PyQt5")
            sys.exit(1)
        return
    
    # CLI mode
    logger.info("=" * 60)
    logger.info("AI-POWERED OS AGENT - GEMINI 2.5 FLASH")
    logger.info("=" * 60)
    
    agent = OSAgent()
    
    # Check if command provided as argument
    if args.command:
        command = " ".join(args.command)
        logger.info(f"User command: {command}")
        agent.execute_command(command)
    else:
        # Interactive mode
        logger.info("Interactive mode. Type 'quit' to exit.")
        while True:
            try:
                command = input("\n💬 You: ").strip()
                if command.lower() in ['quit', 'exit', 'bye']:
                    logger.info("Goodbye!")
                    break
                if command:
                    agent.execute_command(command)
            except KeyboardInterrupt:
                logger.info("\nInterrupted by user")
                break
    
    logger.info("=" * 60)
    logger.info("Agent session ended")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()