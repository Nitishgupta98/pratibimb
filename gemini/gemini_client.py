"""
Gemini AI Client for Pratibimb Platform
This module provides integration with Google's Gemini 1.5 Flash model
"""

import os
import sys
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from config.env
load_dotenv(os.path.join(os.path.dirname(__file__), 'config.env'))

class GeminiClient:
    """
    Client class for interacting with Google's Gemini AI model
    """
    
    def __init__(self):
        """Initialize the Gemini client with configuration from environment variables"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL_NAME', 'gemini-1.5-flash')
        self.temperature = float(os.getenv('GEMINI_TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('GEMINI_MAX_TOKENS', '2048'))
        self.top_p = float(os.getenv('GEMINI_TOP_P', '0.9'))
        self.top_k = int(os.getenv('GEMINI_TOP_K', '40'))
        
        self.model = None
        self._configure_client()
    
    def _configure_client(self):
        """Configure the Gemini client with API key and model settings"""
        if not self.api_key or self.api_key == 'your_activation_key_here':
            raise ValueError(
                "GEMINI_API_KEY not found or not set. "
                "Please set your activation key in gemini/config.env file"
            )
        
        try:
            # Configure the Gemini API
            genai.configure(api_key=self.api_key)
            
            # Initialize the model with generation config
            generation_config = {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "max_output_tokens": self.max_tokens,
            }
            
            self.model = genai.GenerativeModel(
                model_name=self.model_name,
                generation_config=generation_config
            )
            
            print(f"✅ Gemini client configured successfully!")
            print(f"📋 Model: {self.model_name}")
            print(f"🌡️  Temperature: {self.temperature}")
            print(f"🎯 Max Tokens: {self.max_tokens}")
            
        except Exception as e:
            raise ConnectionError(f"Failed to configure Gemini client: {str(e)}")
    
    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Gemini API
        
        Returns:
            Dict containing test results and model information
        """
        try:
            # Test prompt
            test_prompt = "Hello! Please confirm you are Gemini 1.5 Flash model and briefly describe your capabilities."
            
            print("🔗 Testing connection to Gemini API...")
            print(f"📤 Test prompt: {test_prompt}")
            
            # Generate response
            response = self.model.generate_content(test_prompt)
            
            result = {
                "success": True,
                "model_name": self.model_name,
                "api_key_valid": True,
                "response": response.text,
                "prompt_used": test_prompt,
                "configuration": {
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                    "top_p": self.top_p,
                    "top_k": self.top_k
                }
            }
            
            print("✅ Connection test successful!")
            print(f"📥 Response: {response.text[:200]}...")
            
            return result
            
        except Exception as e:
            error_result = {
                "success": False,
                "error": str(e),
                "model_name": self.model_name,
                "api_key_valid": False
            }
            
            print(f"❌ Connection test failed: {str(e)}")
            return error_result
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Gemini model
        
        Args:
            prompt (str): The input prompt
            **kwargs: Additional generation parameters
            
        Returns:
            str: Generated text response
        """
        try:
            if not self.model:
                raise RuntimeError("Gemini model not initialized. Check API key and configuration.")
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            raise RuntimeError(f"Text generation failed: {str(e)}")
    
    def generate_braille_description(self, text: str) -> str:
        """
        Generate braille-friendly descriptions using Gemini
        
        Args:
            text (str): Input text to convert to braille-friendly format
            
        Returns:
            str: Braille-friendly description
        """
        prompt = f"""
        Convert the following text into a braille-friendly format that is:
        1. Clear and descriptive
        2. Uses simple language
        3. Includes spatial descriptions where relevant
        4. Maintains the essential information
        
        Original text: {text}
        
        Please provide a braille-friendly version:
        """
        
        return self.generate_text(prompt)
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration
        
        Returns:
            Dict containing model information
        """
        return {
            "model_name": self.model_name,
            "api_key_configured": bool(self.api_key and self.api_key != 'your_activation_key_here'),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "client_ready": bool(self.model)
        }

def main():
    """Main function to test the Gemini client"""
    print("🚀 Initializing Gemini Client...")
    print("=" * 50)
    
    try:
        # Create client instance
        client = GeminiClient()
        
        # Display model info
        print("\n📊 Model Information:")
        info = client.get_model_info()
        for key, value in info.items():
            print(f"   {key}: {value}")
        
        # Test connection
        print("\n🧪 Running Connection Test:")
        print("-" * 30)
        test_result = client.test_connection()
        
        if test_result["success"]:
            print(f"\n🎉 SUCCESS! Gemini {client.model_name} is ready to use!")
            print(f"📝 Full Response: {test_result['response']}")
        else:
            print(f"\n💥 FAILED! Error: {test_result['error']}")
            
    except Exception as e:
        print(f"\n❌ Error initializing Gemini client: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your API key in gemini/config.env")
        print("2. Ensure you have internet connection")
        print("3. Verify the API key has proper permissions")

if __name__ == "__main__":
    main()
