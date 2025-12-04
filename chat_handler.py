from openrouter_compat import genai
from config import OPENROUTER_API_KEY, MODEL_NAME, CHAT_CONTEXT_WINDOW
from datetime import datetime

class ChatHandler:
    def __init__(self):
        genai.configure(api_key=OPENROUTER_API_KEY)
        self.model = genai.GenerativeModel(MODEL_NAME)
        self.chat_history = []
        self.system_context = """You are an AI assistant controlling a computer autonomously. 
You can chat with the user while performing tasks. Be helpful, concise, and informative.
When greeting or chatting, be friendly but brief. The user can ask you about:
- What you're currently doing
- Your progress on tasks
- General questions

Keep responses short and conversational."""
    
    def respond(self, user_message, current_task=None, status=None):
        """Generate a chat response based on user message and current context."""
        try:
            # Build context
            context_parts = [self.system_context]
            
            if current_task:
                context_parts.append(f"Current task: {current_task}")
            if status:
                context_parts.append(f"Current status: {status}")
            
            # Add recent history
            for msg in self.chat_history[-CHAT_CONTEXT_WINDOW:]:
                context_parts.append(f"{msg['role']}: {msg['content']}")
            
            # Add current message
            context_parts.append(f"User: {user_message}")
            
            # Generate response
            response = self.model.generate_content("\n".join(context_parts))
            response_text = response.text.strip()
            
            # Update history
            self.chat_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.now()
            })
            self.chat_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now()
            })
            
            return response_text
            
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def clear_history(self):
        """Clear chat history."""
        self.chat_history = []
