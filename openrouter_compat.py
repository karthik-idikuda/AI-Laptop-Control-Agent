"""
OpenRouter API wrapper to provide Gemini-compatible interface
Uses OpenAI client to connect to OpenRouter's Claude Sonnet 4.5
"""

from openai import OpenAI
from config import OPENROUTER_API_KEY, MODEL_NAME, OPENROUTER_BASE_URL
import json

class GenerativeModel:
    """Wrapper to make OpenRouter compatible with Gemini API interface"""
    
    def __init__(self, model_name=None):
        self.model_name = model_name or MODEL_NAME
        self.client = OpenAI(
            api_key=OPENROUTER_API_KEY,
            base_url=OPENROUTER_BASE_URL
        )
    
    def generate_content(self, prompt_parts):
        """Generate content using OpenRouter's Claude model"""
        
        # Handle different input formats
        if isinstance(prompt_parts, str):
            # Simple string prompt
            messages = [{"role": "user", "content": prompt_parts}]
        elif isinstance(prompt_parts, list):
            # List of parts (text and/or images)
            messages = self._convert_parts_to_messages(prompt_parts)
        else:
            messages = [{"role": "user", "content": str(prompt_parts)}]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=4000
            )
            
            # Create response object similar to Gemini
            return GenerativeResponse(response.choices[0].message.content)
        except Exception as e:
            print(f"OpenRouter API error: {e}")
            raise
    
    def _convert_parts_to_messages(self, parts):
        """Convert Gemini-style parts to OpenAI-style messages"""
        content_parts = []
        
        for part in parts:
            if isinstance(part, str):
                # Text content
                content_parts.append({"type": "text", "text": part})
            else:
                # Try to handle as PIL Image
                try:
                    import base64
                    import io
                    from PIL import Image
                    
                    # Check if it's a PIL Image
                    if isinstance(part, Image.Image):
                        # Convert PIL Image to base64
                        img_byte_arr = io.BytesIO()
                        part.save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        img_base64 = base64.b64encode(img_byte_arr).decode('utf-8')
                        
                        content_parts.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{img_base64}"
                            }
                        })
                    else:
                        # If not an image, convert to text
                        content_parts.append({"type": "text", "text": str(part)})
                except Exception as e:
                    print(f"Error processing image part: {e}")
                    content_parts.append({"type": "text", "text": str(part)})
        
        # Create message with content
        messages = []
        if content_parts:
            messages.append({"role": "user", "content": content_parts})
        
        return messages


class GenerativeResponse:
    """Wrapper for OpenRouter response to match Gemini interface"""
    
    def __init__(self, text_content):
        self.text = text_content


def configure(api_key):
    """Configure function for compatibility (does nothing as we use OpenAI client)"""
    pass


# Create compatible interface
class genai:
    """Module-level interface compatible with google.generativeai"""
    
    @staticmethod
    def configure(api_key):
        configure(api_key)
    
    @staticmethod
    def GenerativeModel(model_name=None):
        return GenerativeModel(model_name)
