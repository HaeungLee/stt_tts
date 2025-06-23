import os
import json
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.types import GenerateContentConfig, Modality

class GemmaClient:
    def __init__(self, api_key: str = None, model: str = "gemma-3-27b-it"):
        """
        Initialize the Gemma client.
        
        Args:
            api_key: Google AI API key (if None, will try to load from .env)
            model: Model to use (default: gemini-1.5-pro)
        """
        # Load environment variables
        load_dotenv()
        
        # Set API key (parameter takes precedence over .env)
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        if not self.api_key:
            raise ValueError("Google API key not provided. Set GOOGLE_API_KEY in .env file or pass as parameter.")
        
        # Configure the client
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = model
        
        # Default generation config (for reference, not directly used in API calls)
        self.generation_config = {
            "max_output_tokens": 200  # Limited to 20 tokens to manage API usage
        }
        
        # Conversation history
        self.conversation_history: List[Dict[str, str]] = []
    
    def generate_response(self, prompt: str, context: List[Dict[str, str]] = None, max_tokens: int = 20, **kwargs) -> str:
        """
        Generate a response using the Gemma model.
        
        Args:
            prompt: The user's input prompt
            context: Optional conversation history in the format [{"role": "user", "content": "..."}, ...]
            **kwargs: Additional generation parameters (temperature, max_tokens, etc.)
            
        Returns:
            str: Generated response text
        """
        try:
            # Prepare the content input
            if context or self.conversation_history:
                # Use conversation history if available
                messages = context or self.conversation_history.copy()
                messages.append({"role": "user", "parts": [{"text": prompt}]})
                content_input = messages
            else:
                # For simple prompt, just use the text directly
                content_input = prompt
            
            # Generate response using the same pattern as gemini_service.py
            # Note: Generation parameters are not supported directly in the API call
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=content_input
            )
            
            # Extract response text using the same method as gemini_service.py
            content_text = ""
            if hasattr(response, 'candidates') and response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'text') and part.text:
                        content_text += part.text
            
            if content_text:
                # Update conversation history if needed (only if not using external context)
                if not context:
                    self._update_conversation_history(prompt, content_text)
                return content_text.strip()
            else:
                return "Sorry, I couldn't generate a response. Please try again."
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"An error occurred: {str(e)}"
    
    def _update_conversation_history(self, user_input: str, assistant_response: str, max_history: int = 10):
        """
        Update the conversation history.
        
        Args:
            user_input: The user's input
            assistant_response: The assistant's response
            max_history: Maximum number of conversation turns to keep
        """
        # Add user message
        self.conversation_history.append({"role": "user", "parts": [{"text": user_input}]})
        
        # Add assistant response
        self.conversation_history.append({"role": "model", "parts": [{"text": assistant_response}]})
        
        # Trim history if needed
        if len(self.conversation_history) > max_history * 2:  # *2 because each turn has user and assistant
            self.conversation_history = self.conversation_history[-max_history*2:]
    
    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_available_models(self) -> List[str]:
        """
        Get a list of available models.
        
        Returns:
            List[str]: List of available model names
        """
        try:
            # This might need adjustment based on actual API response structure
            models = self.client.models.list_models()
            return [model.name for model in models] if hasattr(models, '__iter__') else []
        except Exception as e:
            print(f"Error fetching available models: {e}")
            return []

def test_gemma_client():
    """Test function for Gemma client"""
    print("Testing Gemma Client...")
    
    try:
        # Initialize client
        client = GemmaClient()
        
        # List available models
        print("\nAvailable models:")
        models = client.get_available_models()
        for model in models[:5]:  # Show first 5 models
            print(f"- {model}")
        
        # Test single prompt with token limit
        test_prompt = "안녕하세요! 오늘 날씨가 정말 좋네요. 오늘 하루 어떻게 보내실 건가요?"
        print(f"\nTesting with prompt: '{test_prompt}'")
        
        response = client.generate_response(
            prompt=test_prompt
        )
        
        print("\nResponse:")
        print(response)
        
        # Test conversation history
        print("\nTesting conversation history...")
        client.clear_conversation_history()
        
        # First message
        msg1 = "안녕하세요!"
        print(f"\nYou: {msg1}")
        resp1 = client.generate_response(msg1)
        print(f"AI: {resp1}")
        
        # Second message (should have context)
        msg2 = "방금 무슨 말을 했지?"
        print(f"\nYou: {msg2}")
        resp2 = client.generate_response(msg2)
        print(f"AI: {resp2}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error in test: {e}")
        raise

if __name__ == "__main__":
    test_gemma_client()
